HOURS = []
[[HOURS.append(str(hour) + period) for hour in range(1, 13)] for period in ['AM', 'PM']]


class DefaultPreferences:

    hours = HOURS
    day_start = 7
    day_end = 19

    temperature_options = [(0, 'I like it cool'),
                           (1, "I don't really mind"),
                           (2, "I like it hot")
                           ]
    temperature = 1

    activity_options = ['Walking',
                        'Running',
                        'Cycling',
                        'Yoga',
                        'Meditating',
                        'Other',
                        ]
    activities = []
