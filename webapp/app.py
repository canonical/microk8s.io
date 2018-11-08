import flask
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.debug import DebuggedApplication

import talisker.flask
from webapp.handlers import add_headers, clear_trailing_slash
from webapp.microk8s.views import microk8s


def create_app(testing=False):
    app = flask.Flask(
        __name__, template_folder="../templates", static_folder="../static"
    )

    app.testing = testing

    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.url_map.strict_slashes = False

    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app)

    if not app.testing:
        talisker.flask.register(app)

    app.before_request(clear_trailing_slash)
    app.after_request(add_headers)

    init_handler(app)
    init_blueprint(app)

    return app


def init_handler(app):
    @app.errorhandler(404)
    def page_not_found(error):
        """
        For 404 pages, display the 404.html template,
        passing through the error description.
        """

        return flask.render_template("404.html", error=error.description), 404

    @app.route("/_status/check")
    def health_check():
        """ Health check end point used by Talisker.
        """
        return ("", 200)


def init_blueprint(app):
    app.register_blueprint(microk8s)
