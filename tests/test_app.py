import auth
from tests.fixtures import test_client, setup_test_app, test_db, test_locations
import actions


def test_app_runs(test_client):
    response = test_client.get('ping')
    assert response.status_code == 200
    assert response.data == b'pong'


def test_unsub(test_client, test_db):
    test_email = 'test@email.com'
    new_user = actions.add_user(test_email,
                                location=actions.add_or_return_location('Montreal, Canada'))
    token = auth.generate_confirmation_token(new_user.email)

    response = test_client.get(f'unsubscribe/{token}')

    print(response)

# TODO figure out mocking of forms and test the other routes here

