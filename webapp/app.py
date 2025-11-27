# Packages
from datetime import timedelta
from canonicalwebteam.flask_base.app import FlaskBase
from flask import render_template
import talisker
import flask
from flask_caching import Cache

from canonicalwebteam.discourse import (
    Docs,
    DocParser,
    DiscourseAPI,
)
from canonicalwebteam.search import build_search_view
from canonicalwebteam.cookie_service import CookieConsent


# Rename your project below
app = FlaskBase(
    __name__,
    "microk8s.io",
    template_folder="../templates",
    static_folder="../static",
    template_404="404.html",
    template_500="500.html",
)

session = talisker.requests.get_session()

# Configuration for shared cookie service

# Configure Flask session
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=365)
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = True

# Initialize Flask-Caching
app.config["CACHE_TYPE"] = "SimpleCache"
cache = Cache(app)


# Set up cache functions for cookie consent service
def get_cache(key):
    return cache.get(key)


def set_cache(key, value, timeout):
    cache.set(key, value, timeout)


cookie_service = CookieConsent().init_app(
    app,
    get_cache_func=get_cache,
    set_cache_func=set_cache,
    start_health_check=True,
)

discourse = Docs(
    parser=DocParser(
        api=DiscourseAPI(
            base_url="https://discuss.kubernetes.io/", session=session
        ),
        index_topic_id=11243,
        url_prefix="/docs",
    ),
    document_template="docs/document.html",
    url_prefix="/docs",
)
app.add_url_rule(
    "/docs/search",
    "docs-search",
    build_search_view(
        app=app,
        session=session,
        site="microk8s.io/docs",
        template_path="docs/search.html",
    ),
)
discourse.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/contact-us")
def contact():
    return render_template("contact-us.html")


@app.route("/thank-you")
def thankyou():
    return render_template("thank-you.html")


@app.route("/features")
def features():
    return render_template("/features/index.html")


@app.route("/compare")
def compare():
    return render_template("/compare/index.html")


@app.route("/tutorials")
def tutorials():
    return render_template("/tutorials/index.html")


@app.route("/resources")
def resources():
    return render_template("/resources/index.html")


@app.route("/isv")
def isv():
    return render_template("/isv/index.html")


@app.route("/isv/contact-us")
def isv_contact():
    return render_template("/isv/contact-us.html")


@app.route("/sitemap.xml")
def sitemap_index():
    xml_sitemap = flask.render_template("sitemap/sitemap-index.xml")
    response = flask.make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"

    return response


@app.route("/sitemap-links.xml")
def sitemap_links():
    xml_sitemap = flask.render_template("sitemap/sitemap-links.xml")
    response = flask.make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"

    return response
