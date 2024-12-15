from flask import Blueprint


hello_blueprint = Blueprint("hello", __name__, url_prefix="/")

@hello_blueprint.route("/")
def hello():
    return "<p>Hello World!</p>"