import auth
from flask_mail import Mail
from tests.fixtures import test_client, test_app, setup_test_app
from actions import compose_verification_email, compose_unsubscribe_email


def test_send_email(test_client):
    mail = Mail(test_client.application)
    auth.send_email('berkerboy@gmail.com',
                     'test_email', 'test_email', mail)


def test_compose_verification_email(test_app):
    with test_app.app_context(), test_app.test_request_context():
        html = compose_verification_email('test@gmail.com')
    assert '/unsubscribe' in html


def test_compose_unsubscribe_email(test_app):
    with test_app.app_context(), test_app.test_request_context():
        html = compose_unsubscribe_email('test@gmail.com')
    assert '/unsubscribe' in html
