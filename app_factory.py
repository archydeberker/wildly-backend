from flask import Flask
from flask_migrate import Migrate

from actions import mail
from config import Config
from models import db
from routes import api


def create_app(db=db, config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    print(f"Using database at {app.config['SQLALCHEMY_DATABASE_URI']}")

    app.register_blueprint(api)
    app.app_context().push()

    db.init_app(app)
    db.session.commit()

    mail.init_app(app)

    Migrate(app, db)

    return app