import pytest

from forms import PreferencesForm
from tests.fixtures import setup_test_app, test_app, test_client


# TODO these tests are pretty feeble, but I don't know how to mock the submission of forms with different values


@pytest.fixture(scope='module')
def test_form(test_client, test_app):
    with test_app.app_context(), test_app.test_request_context():
        form = PreferencesForm()
        yield form


class TestPreferencesForm:
    def test_default_day_start_is_int(self, test_form):
        assert isinstance(test_form.day_start.default, int)

    def test_default_day_end_is_int(self, test_form):
        assert isinstance(test_form.day_end.default, int)

    def test_default_temperature_pref_is_int(self, test_form):
        assert isinstance(test_form.temperature.default, int)

    def test_default_activities_are_none(self, test_form):
        assert test_form.activities.default is None

