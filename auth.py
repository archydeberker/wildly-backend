from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from config import Config
from flask import url_for, render_template


def generate_confirmation_token(email: str):
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    return serializer.dumps(email)


def decode_token_to_email(token, expiration_in_hours=10):
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    email = serializer.loads(token,
                             max_age=expiration_in_hours * 3600)

    return email


def send_verification_email(to, subject, template, mail):
    msg = Message(subject,
                  recipients=[to],
                  html=template,
                  sender=Config.MAIL_DEFAULT_SENDER)

    mail.send(msg)


def compose_verification_email(email: str):
    token = generate_confirmation_token(email)
    confirm_url = url_for('api.confirm_email', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    return html