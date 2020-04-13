from app import create_app, db


def initialize_db():
    app = create_app()
    db.create_all(app=app)
