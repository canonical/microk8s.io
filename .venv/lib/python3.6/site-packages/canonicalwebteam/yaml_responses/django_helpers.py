# Core packages
import os

# Third party packages
import yaml
from django.shortcuts import redirect, render
from django.conf.urls import url
from yamlloader import ordereddict


def _create_view(view_callback, url_mapping, settings={}):
    """
    Create a view function to execute the callback function with the
    url_arguments
    """

    def url_view(request, *args, **kwargs):
        return view_callback(request, url_mapping, settings, *args, **kwargs)

    return url_view


def _create_views_from_yaml(yaml_filepath, view_callback, settings={}):
    """
    Givan a YAML file mapping URL paths to values, e.g.:

        path/one: {"some": "value"}
        path/two: {"another": "value"}

    Create a Django URL pattern from each value, so that when that path
    is requested, view_callback is run, passing the mapped value.

    Returns a list of Django urlpatterns.
    """

    urlpatterns = []

    if os.path.isfile(yaml_filepath):
        with open(yaml_filepath) as yaml_paths_file:
            url_paths = yaml.load(
                yaml_paths_file.read(), Loader=ordereddict.CLoader
            )
            if url_paths:
                for url_path, url_mapping in url_paths.items():
                    urlpatterns.append(
                        url(
                            r"^{0}$".format(url_path),
                            _create_view(view_callback, url_mapping, settings),
                        )
                    )

    return urlpatterns


def _redirect_to_target(request, url_mapping, settings, *args, **kwargs):
    location = url_mapping.format(**kwargs)
    query = request.META["QUERY_STRING"]

    if query:
        location += "?" + query

    return redirect(location, permanent=settings.get("permanent", False))


def _deleted_callback(request, url_mapping, settings, *args, **kwargs):
    return render(request, "410.html", url_mapping, status=410)


def create_redirect_views(path="redirects.yaml", permanent=False):
    return _create_views_from_yaml(
        path, _redirect_to_target, settings={"permanent": permanent}
    )


def create_deleted_views(path="deleted.yaml", view_callback=_deleted_callback):
    return _create_views_from_yaml(path, view_callback)
