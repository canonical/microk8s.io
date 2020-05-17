# Packages
from canonicalwebteam.flask_base.app import FlaskBase
from flask import render_template

from canonicalwebteam.discourse_docs import (
    DiscourseDocs,
    DocParser,
    DiscourseAPI,
)

# Rename your project below
app = FlaskBase(
    __name__,
    "dqlite.io",
    template_folder="../templates",
    static_folder="../static",
    template_404="404.html",
    template_500="500.html",
)

doc_parser = DocParser(
    api=DiscourseAPI(base_url="https://discourse.ubuntu.com/"),
    index_topic_id=15536,
    category_id=41,
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
