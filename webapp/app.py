# Packages
from canonicalwebteam.flask_base.app import FlaskBase
from flask import render_template

# Rename your project below
app = FlaskBase(
    __name__,
    "dqlite.io",
    template_folder="../templates",
    static_folder="../static",
    template_404="404.html",
    template_500="500.html",
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/docs")
def docs():
    return render_template("docs/index.html")


@app.route("/docs/faq")
def faq():
    return render_template("docs/faq.html")


@app.route("/docs/protocol")
def protocol():
    return render_template("docs/protocol.html")
