from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)

    return app


def main():
    app = create_app()

    app.run("localhost", 5001)


if __name__ == '__main__':
    main()