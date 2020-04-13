import os
import secrets


class Config(object):
    SECRET_KEY = os.environ.get('TOKEN_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///db.sqlite"
    )

    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # mail accounts
    MAIL_DEFAULT_SENDER = 'archy.deberker@gmail.com'

