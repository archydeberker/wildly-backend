from dateutil import parser

import models

HOURS = []
[[HOURS.append(str(hour) + period) for hour in range(1, 13)] for period in ['AM', 'PM']]


class DefaultPreferences:

    hours = HOURS
    day_start = 7
    day_end = 19

    temperature_options = [('cool', 'I like it cool'),
                           ('neutral', "I don't really mind"),
                           ('hot', "I like it hot")
                           ]
    temperature = 'neutral'

    activity_options = ['Walking',
                        'Running',
                        'Cycling',
                        'Yoga',
                        'Meditating',
                        'Other',
                        ]
    activities = []


def parse_time_to_int(time_string):
    return parser.parse(time_string).hour


def create_default_preference_row(preferences=DefaultPreferences):
    return models.Preferences(day_start=preferences.day_start,
                              day_end=preferences.day_end,
                              temperature=preferences.temperature,
                              activities=preferences.activities)


def update_preferences_for_user_from_form(user_email: str, form):
    pass