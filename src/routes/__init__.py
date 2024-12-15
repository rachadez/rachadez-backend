from flask import Flask

from .hello import hello_blueprint


def register(app: Flask) -> None:
    app.register_blueprint(hello_blueprint)