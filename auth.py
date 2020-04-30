from itsdangerous import URLSafeSerializer
from flask_mail import Message
from config import Config
from flask import url_for, render_template

DEFAULT_SERIALIZER = URLSafeSerializer(Config.SECRET_KEY)


def generate_confirmation_token(email: str, serializer=DEFAULT_SERIALIZER):
    return serializer.dumps(email)


def decode_token_to_email(token, serializer=DEFAULT_SERIALIZER):
    email = serializer.loads(token)
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
    unsubscribe_url = url_for('api.unsubscribe', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url, unsub_url=unsubscribe_url)
    return html
