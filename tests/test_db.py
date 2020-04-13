import datetime

import pytest
from sqlalchemy.exc import IntegrityError

import actions
import models
from app import db
from tests.fixtures import test_db, setup_test_app


def test_db_creation(test_db):
    assert test_db


class TestUser:

    location = dict(postcode="BS6 7EQ", longitude=123, latitude=456)

    @pytest.mark.runfirst
    def test_add_new_user(self, test_db):

        user = dict(email="tmp@gmail.com", location=actions.add_or_return_location(self.location))

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
        location = actions.retrieve_location(dict(email='tmp@gmail.com'))
        assert location.postcode == self.location['postcode']

    def test_setting_of_verified(self, test_db):
        user = actions.add_or_return_user(dict(email='tmp@gmail.com'))
        assert user.email_verified is False
        actions.set_email_verified(user)
        assert user.email_verified is True


class TestActivities:
    @pytest.mark.runfirst
    def test_add_new_activity(self, test_db):
        new_activity = models.Activity(name="skiing")

        db.session.add(new_activity)
        db.session.commit()

    def test_list_activities(self, test_db):
        all_activities = models.Activity.query.all()
        assert len(all_activities) == 1
        assert all_activities[0].name == "skiing"


class TestLocation:
    @pytest.mark.runfirst
    def test_add_new_location(self, test_db):
        new_location = models.Location(
            name="Rumney, NH",
            latitude=43.8054,
            longitude=-71.8126,
            img="https://picsum.photos/id/5/300/300",
        )

        db.session.add(new_location)
        db.session.commit()

    def test_list_locations(self, test_db):
        all_locations = models.Location.query.all()
        assert len(all_locations) == 2  # We add one in the User class above
        assert all_locations[-1].name == "Rumney, NH"


class TestTrip:
    @pytest.mark.runfirst
    def test_add_new_trip(self, test_db):
        new_trip = models.Trip(
            activity=1, location=1, timestamp=datetime.datetime.now()
        )

        db.session.add(new_trip)
        db.session.commit()

    def test_add_users_to_trip(self, test_db):

        # Get the user we added in the TestUser class
        u = models.User.query.filter_by(id=1).first()

        # Add the trip we created in the test above
        u.trips.append(models.Trip.query.filter_by(id=1).first())

        db.session.add(u)
        db.session.commit()

    def test_retrieve_users_on_trip(self, test_db):
        trip = models.Trip.query.filter_by(id=1).first()
        assert trip.users[0].email == "tmp@gmail.com"


class TestWeather:
    pass
    # TODO: write tests for weather
