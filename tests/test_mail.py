import auth
from app import Mail
from tests.fixtures import test_client, setup_test_app


def test_send_email(test_client):
    mail = Mail(test_client.application)
    auth.send_verification_email('archy.deberker@gmail.com',
                     'test_email', 'test_email')