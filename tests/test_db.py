import datetime

import pytest
from sqlalchemy.exc import IntegrityError

import actions
import models
from models import db
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

        assert user.reg_date.date == datetime.date.today()
        


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


class TestForecasst:
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
