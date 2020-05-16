from itsdangerous import URLSafeSerializer
from flask_mail import Message
from config import Config

DEFAULT_SERIALIZER = URLSafeSerializer(Config.SECRET_KEY)


def generate_confirmation_token(email: str, serializer=DEFAULT_SERIALIZER):
    return serializer.dumps(email)


def decode_token_to_email(token, serializer=DEFAULT_SERIALIZER):
    email = serializer.loads(token)
    return email


def send_email(to, subject, template, mail):
    msg = Message(subject,
                  recipients=[to],
                  html=template,
                  sender=Config.MAIL_DEFAULT_SENDER)

    mail.send(msg)

