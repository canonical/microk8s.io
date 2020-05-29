# Standard library
import os
import re

# Packages
import flask
import yaml
from yamlloader import ordereddict


class YamlRegexMap:
    def __init__(self, filepath):
        """
        Given the path to a YAML file of RegEx mappings like:

            hello/(?P<person>.*)?: "/say-hello?name={person}"
            google/(?P<search>.*)?: "https://google.com/?q={search}"

        Return a list of compiled Regex matches and destination strings:

            [
                (<regex>, "/say-hello?name={person}"),
                (<regex>, "https://google.com/?q={search}"),
            ]
        """

        self.matches = []

        if os.path.isfile(filepath):
            with open(filepath) as redirects_file:
                lines = yaml.load(redirects_file, Loader=ordereddict.CLoader)

                if lines:
                    for url_match, target_url in lines.items():
                        if url_match[0] != "/":
                            url_match = "/" + url_match

                        self.matches.append(
                            (re.compile(url_match), target_url)
                        )

    def get_target(self, url_path):
        for (match, target) in self.matches:
            result = match.fullmatch(url_path)

            if result:
                parts = {}
                for name, value in result.groupdict().items():
                    parts[name] = value or ""

                target_url = target.format(**parts)

                if flask.request.query_string:
                    target_url += "?" + flask.request.query_string.decode(
                        "utf-8"
                    )

                return target_url


def _deleted_callback(context):
    return flask.render_template("410.html", **context), 410


def prepare_redirects(path="redirects.yaml", permanent=False):
    """
    Create a regex map from the provided yaml file,
    and return a view function "apply_redirects" which encloses
    the maps to return a 302 redirect where relevant.

    Usage:
        import flask
        from canonicalwebteam.yaml_responses.flask import prepare_redirects
        app = flask.Flask(__name__)
        # Regular (temporary) redirects
        app.before_request(prepare_redirects())
        # Permanent redirects
        app.before_request(prepare_redirects(
            path='permanent_redirects.yaml', permanent=True
        ))
    """

    redirect_map = YamlRegexMap(path)

    def _apply_redirects():
        """
        Process the two mappings defined above
        of permanent and temporary redirects to target URLs,
        to send the appropriate redirect responses
        """

        redirect_url = redirect_map.get_target(flask.request.path)

        return_code = 301 if permanent else 302

        if redirect_url:
            return flask.redirect(redirect_url, code=return_code)

    return _apply_redirects


def prepare_deleted(path="deleted.yaml", view_callback=_deleted_callback):
    """
    Handlers to return 410 responses for deleted URLs loaded from
    deleted.yaml

    Basic usage:
        import flask
        from canonicalwebteam.yaml_responses.flask import prepare_deleted
        app = flask.Flask(__name__)
        app.before_request(prepare_deleted())  # Will load 410.html

    Custom usage:
        def deleted_callback(context):
            context['extra_arg'] = 'value'

            return render_template('410.html', **context), 410

        app.before_request(
            prepare_deleted(
                path="deleted.yaml",
                view_callback=deleted_callback
            )
        )
    """

    deleted_urls = {}

    if os.path.isfile(path):
        with open(path) as deleted_file:
            deleted_urls = yaml.load(deleted_file, Loader=ordereddict.CLoader)

    def _show_deleted():
        """
        Process the two mappings defined above
        of permanent and temporary redirects to target URLs,
        to send the appropriate redirect responses
        """

        if deleted_urls:
            for url_match, context in deleted_urls.items():
                url_match = str(url_match)

                if url_match[0] != "/":
                    url_match = "/" + url_match

                if not context:
                    context = {}

                if re.compile(url_match).fullmatch(flask.request.path):
                    return view_callback(context)

    return _show_deleted
