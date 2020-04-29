import datetime

import pytest

import geo
from cal import Calendar, get_calendar_event


@pytest.fixture(scope='module')
def calendar_client():
    calendar = Calendar()
    yield calendar


class TestLocation:
    place = "BS2 7EV"


class BritishTestLocation:
    place = "BS6 6BP"


class CanadianTestLocation:
    place = "H2S 3C3"


class TestWindow:
    summary = "Test"
    precip_probability = 0.2
    apparent_temperature = 0.3
    weather_timestamp = datetime.datetime.now()


@pytest.fixture(scope='module')
def test_event():

    e = get_calendar_event(location=TestLocation,
                           window=TestWindow,
                           attendees=['test@test.com'],
                           timezone='UTC')

    yield e


class TestCalendar:

    def test_authentication(self, calendar_client):
        assert calendar_client.authenticated is True

    def test_creation_of_event_dictionary(self, calendar_client, test_event):
        created_event = calendar_client.create_event(test_event)
        assert created_event['status'] == 'confirmed'

        # And teardown: delete the event again
        deleted_event = calendar_client.delete_event(created_event['id'])

    def test_event_creation_has_correct_timezone(self, calendar_client, test_event):

        lat, lon = geo.get_lat_lon_for_place(BritishTestLocation.place)
        timezone = geo.get_timezone_for_lat_lon(lat, lon)

        e = get_calendar_event(location=TestLocation,
                               window=TestWindow,
                               attendees=['berkerboy@gmail.com'],
                               timezone=timezone)

        assert e.timezone == 'Europe/London'

        created_event = calendar_client.create_event(e)
        assert created_event['start']['timeZone'] == 'Europe/London'
