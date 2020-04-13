from itsdangerous import URLSafeTimedSerializer


def generate_confirmation_token(app, email: str):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dump(email)


def decode_token_to_email(app, token, expiration_in_hours=10):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token,
                                 max_age=expiration_in_hours * 3600)
    except:
        return None

    return email


def send_verification_email(email: str):
    pass



