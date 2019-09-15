import datetime
from sqlalchemy.exc import IntegrityError

from app import db, app
import os
import models
import pytest


@pytest.fixture(scope="session")
def test_db():
    test_db = 'sqlite:///tests/test_db.sqlite'
    app.config['SQLALCHEMY_DATABASE_URI'] = test_db
    db.init_app(app)
    db.create_all(app=app)

    yield db  # provide the fixture value
    os.remove('test_db.sqlite') # this is teardown


def test_db_creation(test_db):
    assert test_db


class TestUser:

    db = test_db()

    @pytest.mark.runfirst
    def test_add_new_user(self):
        new_user = models.User(email='tmp@gmail.com', name='My Name')

        db.session.add(new_user)
        db.session.commit()

    def test_list_users(self):
        all_users = models.User.query.all()
        assert len(all_users) == 1

    def test_reject_new_user_with_duplicate_email(self):
        with pytest.raises(IntegrityError):
            self.test_add_new_user()

        db.session.rollback()


class TestActivities:
    db = test_db()

    @pytest.mark.runfirst
    def test_add_new_activity(self):
        new_activity = models.Activity(name='skiing')

        db.session.add(new_activity)
        db.session.commit()

    def test_list_activities(self):
        all_activities = models.Activity.query.all()
        assert len(all_activities) == 1
        assert all_activities[0].name == 'skiing'


class TestLocation:
    db = test_db()

    @pytest.mark.runfirst
    def test_add_new_location(self):
        new_location = models.Location(name='Rumney, NH',
                                       latitude=43.8054,
                                       longitude=-71.8126,
                                       img='https://picsum.photos/id/5/300/300')

        db.session.add(new_location)
        db.session.commit()

    def test_list_locations(self):
        all_locations = models.Location.query.all()
        assert len(all_locations) == 1
        assert all_locations[0].name == 'Rumney, NH'


class TestTrip:
    db = test_db()

    @pytest.mark.runfirst
    def test_add_new_trip(self):
        new_trip = models.Trip(activity=1,
                               location=1,
                               timestamp=datetime.datetime.now())

        db.session.add(new_trip)
        db.session.commit()

    def test_add_users_to_trip(self):

        # Get the user we added in the TestUser class
        u = models.User.query.filter_by(id=1).first()

        # Add the trip we created in the test above
        u.trips.append(models.Trip.query.filter_by(id=1).first())

        db.session.add(u)
        db.session.commit()

    def test_retrieve_users_on_trip(self):
        trip = models.Trip.query.filter_by(id=1).first()
        assert trip.users[0].email == 'tmp@gmail.com'


class TestWeather:
    pass
    # TODO: write tests for weather
