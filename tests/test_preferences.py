import pytest

from preferences import DefaultPreferences
from tests.fixtures import test_locations

# TODO these tests are pretty feeble, but I don't know how to mock the submission of forms with different values

test_location = test_locations[0]

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

    def test_loading_of_values_from_db(self, test_form, test_db, user_with_hot_preferences):
        test_form.initialize_from_db(user_with_hot_preferences.preferences)

        assert test_form.day_start.default != DefaultPreferences.day_start
        assert test_form.day_end.default != DefaultPreferences.day_end
        assert test_form.activities.default != DefaultPreferences.activities
        assert test_form.temperature.default != DefaultPreferences.temperature

    @pytest.mark.skip('Incomplete implementation')
    def test_update_preferences_from_form(self):
        pass

