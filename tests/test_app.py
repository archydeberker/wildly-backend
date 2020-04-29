from tests.fixtures import test_client, setup_test_app


def test_app_runs(test_client):
    response = test_client.get('ping')
    assert response.status_code == 200
    assert response.data == b'pong'

# TODO figure out mocking of forms and test the other routes here