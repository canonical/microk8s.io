from flask import Blueprint, render_template

microk8s = Blueprint(
    "microk8s", __name__, template_folder="/templates", static_folder="/static"
)


@microk8s.route("/")
def index():
    return render_template("microk8s/index.html")
