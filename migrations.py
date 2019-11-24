from app import db, create_app


def initialize_db():
    app = create_app()
    db.create_all(app=app)

