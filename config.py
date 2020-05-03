import os

import constants

file_path = os.path.abspath(os.getcwd())


class Config(object):
    SECRET_KEY = constants.SECRET_KEY
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///db.sqlite"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = os.environ.get('WEATHER_WINDOW_MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('WEATHER_WINDOW_MAIL_PASSWORD')

    # mail accounts
    MAIL_DEFAULT_SENDER = 'weatherwindowapp@gmail.com'


class TestConfig(Config):
    db_filepath = os.path.join(file_path, "test_db.sqlite")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///tests/test_db.sqlite"
