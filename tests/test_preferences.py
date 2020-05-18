import pytest

from forms import PreferencesForm
from preferences import DefaultPreferences
import actions
import models
from tests.fixtures import setup_test_app, test_app, test_client, test_db, test_locations


# TODO these tests are pretty feeble, but I don't know how to mock the submission of forms with different values
test_email = 'test@gmail.com'
test_location = test_locations[0]


@pytest.fixture(scope='module')
def test_form(test_client, test_app):
    with test_app.app_context(), test_app.test_request_context():
        form = PreferencesForm()
        yield form


@pytest.fixture(scope='module')
def user_with_non_default_preferences(test_db):
    user = actions.add_new_user_to_db_with_default_preferences(email=test_email,
                                                               location=actions.add_or_return_location(test_location.place))

    # Retrieve existing preferences, we don't want to add an entirely new row
    prefs = user.preferences
    prefs.day_start = 9
    prefs.day_end = 16
    prefs.temperature = 'hot'
    prefs.activities = [models.Activity(name='rowing'), models.Activity(name='swimming')]

    models.db.session.add(user)
    models.db.session.commit()
    yield user


class TestPreferencesForm:

    def test_default_day_start_is_int(self, test_form):
        assert isinstance(test_form.day_start.default, int)

    def test_default_day_end_is_int(self, test_form):
        assert isinstance(test_form.day_end.default, int)

    def test_default_temperature_pref_is_str(self, test_form):
        # This should probably be an Enum but I've had trouble with migrating Enums to keeping it simple
        assert isinstance(test_form.temperature.default, str)

    def test_default_activities_are_none(self, test_form):
        assert test_form.activities.default is None

    def test_loading_of_values_from_db(self, test_form, test_db, user_with_non_default_preferences):
        test_form.initialize_from_db(user_with_non_default_preferences.preferences)

        assert test_form.day_start.default != DefaultPreferences.day_start
        assert test_form.day_end.default != DefaultPreferences.day_end
        assert test_form.activities.default != DefaultPreferences.activities
        assert test_form.temperature.default != DefaultPreferences.temperature

    def test_update_preferences_from_form(self):
        pass