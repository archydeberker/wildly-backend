from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from config import Config


def generate_confirmation_token(email: str):
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    return serializer.dumps(email)


def decode_token_to_email(token, expiration_in_hours=10):
    print(token)
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

