from app import db
from app_factory import create_app


def initialize_db():
    app = create_app()
    db.create_all(app=app)
