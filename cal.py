from __future__ import print_function
import datetime
import pickle
from dataclasses import dataclass

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import constants

credentials_path = constants.GOOGLE_CREDENTIALS_PATH
token_path = constants.GOOGLE_TOKEN_PATH


@dataclass
class Event:
    location: str
    description: str
    start: datetime.datetime
    end: datetime.datetime
    attendees: list
    summary: str = "Your Weather Window"
    timezone: str = 'America/Los_Angeles'

    @staticmethod
    def _format_datetime(timestamp: datetime.datetime):
        return str(timestamp).replace(' ', 'T')

    def to_dict(self):
        return {
            'summary': self.summary,
            'location': self.location,
            'description': self.description,
            'start': {
                'dateTime': self._format_datetime(self.start),
                'timeZone': self.timezone,
            },
            'end': {
                'dateTime': self._format_datetime(self.end),
                'timeZone': self.timezone,
            },
            'attendees': [{'email': e} for e in self.attendees],
            'guestsCanSeeOtherGuests': False,
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }


class Calendar:
    def __init__(self, scopes=None, host=None, token_path=token_path):

        if scopes is None:
            scopes = ['https://www.googleapis.com/auth/calendar.events']

        self.host = host
        self.scopes = scopes
        self.token_path = token_path
        self.service = self._authenticate(self.scopes, self.host)

    def _authenticate(self, scopes, host):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if self.token_path.exists():
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, scopes)
                creds = flow.run_local_server(host=host or 'localhost',
                                              port=0)
            # Save the credentials for the next run
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)
        self.authenticated = True
        return service

    def create_event(self, event: Event):
        event = self.service.events().insert(calendarId='primary', body=event.to_dict()).execute()
        print('Event Inserted')
        return event

    def delete_event(self, event_id):
        self.service.events().delete(calendarId='primary', eventId=event_id).execute()


def get_calendar_event(location, window, attendees, timezone):
    return Event(location=location.postcode,
                 summary=f" 🌞 Your weather window in {location.postcode}",
                 description=f"It's going to be {window.summary}, "
                             f"with a probability of rain of "
                             f"{window.precip_probability} and feeling like "
                             f"{window.apparent_temperature}°C."
                             f"<br> <br>"
                             f"Jealous of your colleague's weather window?"
                             f" Get your own at https://weather-window-app.herokuapp.com",
                 start=window.weather_timestamp,
                 end=window.weather_timestamp + datetime.timedelta(hours=1),
                 attendees=attendees,
                 timezone=timezone)
