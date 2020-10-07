# Packages
from canonicalwebteam.flask_base.app import FlaskBase
from flask import render_template
import talisker

from canonicalwebteam.discourse_docs import (
    DiscourseDocs,
    DocParser,
    DiscourseAPI,
)

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
doc_parser = DocParser(
    api=DiscourseAPI(
        base_url="https://discuss.kubernetes.io/", session=session
    ),
    index_topic_id=11243,
    url_prefix="/docs",
)
if app.debug:
    doc_parser.api.session.adapters["https://"].timeout = 99
discourse_docs = DiscourseDocs(
    parser=doc_parser,
    document_template="docs/document.html",
    url_prefix="/docs",
)
discourse_docs.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/contact-us")
def contact():
    return render_template("contact-us.html")


@app.route("/thank-you")
def thankyou():
    return render_template("thank-you.html")


@app.route("/high-availability")
def ha():
    return render_template("high-availability.html")
