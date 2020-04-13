from tests.fixtures import setup_test_app


def test_app_runs(setup_test_app):

    response = setup_test_app.ping('/')


