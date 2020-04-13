from tests.fixtures import test_client, setup_test_app


def test_app_runs(test_client):
    response = test_client.get('ping')
    assert response.status_code == 200
    assert response.data == b'pong'


def test_add_user(test_client):

    response = test_client.post('/api/add-user',
                                json=dict(email='test@gmail.com', postcode='ABC DEF'))

    j = response.json

    assert response.status_code == 200
    assert j['email'] == 'test@gmail.com'
    assert j['postcode'] == 'ABC DEF'
