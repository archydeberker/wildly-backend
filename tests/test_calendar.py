import datetime

import pytest

from cal import Calendar, Event
from constants import TEST_EMAIL_ACCOUNT


@pytest.fixture(scope='module')
def calendar_client():
    calendar = Calendar()
    yield calendar


@pytest.fixture(scope='module')
def test_event():
    e = Event(description='test event',
              start=datetime.datetime.now(),
              end=datetime.datetime.now() + datetime.timedelta(hours=1),
              attendees=[TEST_EMAIL_ACCOUNT],
              summary='this is a test event',
              location='H2R 3C2')

    yield e


class TestCalendar:

    @pytest.mark.run_first
    def test_authentication(self, calendar_client):
        assert calendar_client.authenticated is True

    def test_creation_of_event_dictionary(self, calendar_client, test_event):
        created_event = calendar_client.create_event(test_event)
        assert created_event['status'] == 'confirmed'

        # And teardown: delete the event again
        deleted_event = calendar_client.delete_event(created_event['id'])


