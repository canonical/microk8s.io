import flask
from requests.exceptions import HTTPError

from canonicalwebteam.discourse_docs.exceptions import (
    PathNotFoundError,
    RedirectFoundError,
)


class DiscourseDocs(object):
    """
    A Flask extension object to create a Blueprint
    to serve documentation pages, pulling the documentation content
    from Discourse.

    :param api: A DiscourseAPI for retrieving Discourse topics
    :param index_topic_id: ID of a forum topic containing nav & URL map
    :param category_id: Only show docs from topics in this forum category
    :param url_prefix: URL prefix for hosting under (Default: /docs)
    :param document_template: Path to a template for docs pages
                              (Default: docs/document.html)
    """

    def __init__(
        self,
        parser,
        document_template="docs/document.html",
        url_prefix="/docs",
        blueprint_name="discourse_docs",
    ):
        self.blueprint = flask.Blueprint(blueprint_name, __name__)
        self.url_prefix = url_prefix
        self.parser = parser
        category_id = self.parser.category_id

        @self.blueprint.route("/sitemap.txt")
        def sitemap_view():
            """
            Show a list of all URLs in the URL map
            """

            self.parser.parse()

            urls = []

            for key, value in self.parser.url_map.items():
                if type(key) is str:
                    urls.append(flask.request.host_url.strip("/") + key)

            return (
                "\n".join(urls),
                {"Content-Type": "text/plain; charset=utf-8"},
            )

        @self.blueprint.route("/")
        @self.blueprint.route("/<path:path>")
        def document_view(path=""):
            """
            A Flask view function to serve
            topics pulled from Discourse as documentation pages.
            """

            path = "/" + path
            self.parser.parse()

            if path == "/":
                document = self.parser.index_document
            else:
                try:
                    topic_id = self.parser.resolve_path(path)
                except RedirectFoundError as redirect:
                    return flask.redirect(redirect.target_url)
                except PathNotFoundError:
                    return flask.abort(404)

                if topic_id == self.parser.index_topic_id:
                    return flask.redirect(self.url_prefix)

                try:
                    topic = self.parser.api.get_topic(topic_id)
                except HTTPError as http_error:
                    return flask.abort(http_error.response.status_code)

                document = self.parser.parse_topic(topic)

                if category_id and topic["category_id"] != category_id:
                    forum_topic_url = (
                        f'{parser.api.base_url}{document["topic_path"]}'
                    )
                    return flask.redirect(forum_topic_url)

                if (
                    topic_id not in self.parser.url_map
                    and document["topic_path"] != path
                ):
                    return flask.redirect(document["topic_path"])

            response = flask.make_response(
                flask.render_template(
                    document_template,
                    document=document,
                    navigation=self.parser.navigation,
                    forum_url=self.parser.api.base_url,
                    metadata=self.parser.metadata,
                )
            )

            for message in self.parser.warnings:
                flask.current_app.logger.warning(message)
                response.headers.add(
                    "Warning",
                    f'199 canonicalwebteam.discourse-docs "{message}"',
                )

            return response

    def init_app(self, app):
        """
        Attach the discourse docs blueprint to the application
        at the specified `url_prefix`
        """

        app.register_blueprint(self.blueprint, url_prefix=self.url_prefix)
