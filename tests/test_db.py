import datetime

import pytest
from sqlalchemy.exc import IntegrityError

import actions
import models
import preferences
from models import db
from preferences import DefaultPreferences
from tests.fixtures import test_db, setup_test_app, test_locations

USER_EMAIL = 'tmp@gmail.com'


def test_db_creation(test_db):
    assert test_db


class TestUser:

    location = test_locations[0]

    def test_add_new_user(self, test_db):

        user = dict(email=USER_EMAIL, location=actions.add_or_return_location(self.location.place))

        new_user = models.User(**user)

        db.session.add(new_user)
        db.session.commit()

    def test_list_users(self, test_db):
        all_users = models.User.query.all()
        assert len(all_users) == 1

    def test_reject_new_user_with_duplicate_email(self, test_db):
        with pytest.raises(IntegrityError):
            self.test_add_new_user(test_db)

        db.session.rollback()

    def test_retrieval_of_location(self, test_db):
        location = actions.retrieve_location_for_user(dict(email=USER_EMAIL))
        assert location.place == self.location.place

    def test_setting_of_verified(self, test_db):
        user = actions.add_or_return_user(email=USER_EMAIL)
        assert user.email_verified is False
        actions.set_email_verified(user)
        assert user.email_verified is True

    def test_user_deletion(self, test_db):
        actions.delete_user(email=USER_EMAIL)
        all_users = models.User.query.all()
        assert len(all_users) == 0

        # Add back the user
        actions.add_or_return_user(email=USER_EMAIL,
                                   location=actions.add_or_return_location(self.location.place))
        
    def test_user_reg_date(self, test_db):
        user = actions.add_or_return_user(USER_EMAIL)

        assert user.registered.date() == datetime.date.today()


class TestLocations:
    @pytest.mark.runfirst
    def test_add_new_location(self, test_db):
        new_location = models.Location(
            place="London UK",
            latitude=43.8054,
            longitude=-71.8126,
        )

        db.session.add(new_location)
        db.session.commit()

    def test_list_locations(self, test_db):
        all_locations = models.Location.query.all()
        assert all_locations[-1].place == "London UK"

    def test_retrieve_users_for_locations(self, test_db):
        location = models.Location.query.first()
        assert isinstance(location.users, list)


class TestForecasts:
    location = test_locations[0]

    def test_add_new_forecast(self, test_db):
        u = models.User.query.first()

        new_forecast = models.Forecast(location_id=u.location.id,
                                       recorded_timestamp=datetime.datetime.now(),
                                       weather_timestamp=datetime.datetime.now())

        db.session.add(new_forecast)
        db.session.commit()

    def test_retrieve_forecasts_for_location(self, test_db):

        # Get the user we added in the TestUser class
        u = models.User.query.first()

        print(u.location.forecasts)

        assert isinstance(u.location.forecasts, list)
        assert len(u.location.forecasts) == 1

    # @pytest.mark.parametrize('location', test_locations)
    def test_addition_of_forecast_to_db(self, test_db):

        location = actions.get_location_by_place(place=self.location.place)
        actions.add_tomorrows_forecast_to_db(location)


class TestPreferences:
    location = test_locations[0]
    new_user_email = "new@gmail.com"
    activity = "rowing"

    def test_create_preferences_row_with_default_values(self):
        preference_row = preferences.create_default_preference_row()
        assert preference_row.day_start == DefaultPreferences.day_start
        assert preference_row.day_end == DefaultPreferences.day_end
        assert preference_row.temperature == DefaultPreferences.temperature
        assert preference_row.activities == DefaultPreferences.activities

    def test_preferences_cannot_be_created_without_a_user(self):

        preference_row = preferences.create_default_preference_row()

        models.db.session.add(preference_row)
        with pytest.raises(IntegrityError):
            db.session.commit()

        db.session.rollback()

    def test_assigning_default_preferences_to_existing_user(self):
        """If an existing user does not have any preferences, we should be able to assign some"""
        all_users = models.User.query.all()
        assert len(all_users) > 0
        user = all_users[0]

        user_preferences = user.preferences
        assert user_preferences is None

        # Now create some preferences and associate with that user
        preference_row = preferences.create_default_preference_row()
        preference_row.user_id = user.id

        db.session.add(preference_row)
        db.session.commit()

        # And confirm that now the user has preferences attached
        user = models.User.query.filter_by(id=user.id).first()
        assert user.preferences is not None
        assert user.preferences.temperature == DefaultPreferences.temperature
        assert user.preferences.day_start == DefaultPreferences.day_start
        assert user.preferences.day_end == DefaultPreferences.day_end

    def test_new_user_has_default_preferences_assigned(self):

        # Add a new user with default preferences
        location = actions.get_location_by_place(self.location.place)
        _ = actions.add_new_user_to_db_with_default_preferences(self.new_user_email, location)

        # Check that when retrieved, those preferences are correct
        user = actions.get_user(self.new_user_email)

        assert user.preferences is not None
        assert user.preferences.temperature == DefaultPreferences.temperature
        assert user.preferences.day_start == DefaultPreferences.day_start
        assert user.preferences.day_end == DefaultPreferences.day_end

    def test_updating_of_simple_preferences(self):
        # Get preferences for our test user
        prefs = actions.get_user(self.new_user_email).preferences
        old_day_start, old_day_end, old_temperature = prefs.day_start, prefs.day_end, prefs.temperature
        prefs.day_start = 6
        prefs.day_end = 22
        prefs.temperature = 'hot'

        db.session.add(prefs)
        db.session.commit()
        new_preferences = actions.get_user(self.new_user_email).preferences

        assert new_preferences.day_start != old_day_start
        assert new_preferences.day_end != old_day_end
        assert new_preferences.temperature != old_temperature


class TestActivities:
    new_user_email = "new@gmail.com"
    activity = "rowing"
    activity2 = "basketball"

    def test_add_new_activity_to_table(self):
        activity_row = actions.add_activity(self.activity)

        all_activities = models.Activity.query.all()

        assert activity_row in all_activities

    def test_add_first_activity_to_user_preferences(self):
        activity_row = actions.add_or_return_activity(self.activity)

        # Get preferences for our test user
        prefs = actions.get_user(self.new_user_email).preferences

        prefs.activities.append(activity_row)

        db.session.add(prefs)
        db.session.commit()

        prefs = actions.get_user(self.new_user_email).preferences

        assert self.activity in [activity.name for activity in prefs.activities]

    def test_append_activity_to_user_preferences(self):
        user = actions.get_user(self.new_user_email)
        new_activity = actions.add_or_return_activity(self.activity2)

        user.preferences.activities.append(new_activity)

        db.session.add(user)
        db.session.commit()

        user = actions.get_user(self.new_user_email)

        assert len(user.preferences.activities) is 2

    def test_remove_activity_from_user_preferences(self):

        user = actions.get_user(self.new_user_email)
        activity = actions.add_or_return_activity(self.activity)

        assert len(user.preferences.activities) == 2

        user.preferences.activities.pop(user.preferences.activities.index(activity))

        assert len(user.preferences.activities) == 1

        db.session.add(user)
        db.session.commit()

        user = actions.get_user(self.new_user_email)

        assert len(user.preferences.activities) is 1
