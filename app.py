from flask import Flask
from flask_migrate import Migrate
from config import Config

from actions import mail
from models import db
from routes import api


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    print(f"Using database at {app.config['SQLALCHEMY_DATABASE_URI']}")

    app.register_blueprint(api)

    db.init_app(app)

    mail.init_app(app)

    Migrate(app, db)

    return app


app = create_app()

if __name__ == "__main__":
    app.app_context().push()
    db.create_all()

    app.run(
        debug=True, port=5001
    )

