import os

from flask import Flask
from flask_migrate import Migrate

from models import db
from routes import api


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///db.sqlite"
    )

    print(f"Using database at {app.config['SQLALCHEMY_DATABASE_URI']}")

    app.register_blueprint(api)

    db.init_app(app)

    Migrate(app, db)

    return app


app = create_app()

if __name__ == "__main__":

    app.run(
        debug=True, port=5001
    )
