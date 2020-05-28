import time

import actions
import models
import weather
import cal
import geo
import constants
from actions import filter_users_who_already_have_invites_for_today
from app_factory import create_app
from cal import get_calendar_event
from scripts import get_credentials_from_s3

DELAY_IN_S = 1


def main(dry_run=False):
    if dry_run:
        print('DRY RUN MODE')
    calendar = cal.Calendar()
    finder = weather.WeatherWindowFinder(preferences=weather.Preferences(temperature_weighting=constants.TEMPERATURE_WEIGHTINGS,
                                                                         weightings=constants.DEFAULT_WEIGHTINGS))
    eligible_users = []
    # Get all the locations in the database
    for location in reversed(models.Location.query.all()):
        print(f'Getting users for {location}')

        # Users who we will alert
        users = [u for u in location.users if u.email_verified]

        users = filter_users_who_already_have_invites_for_today(users)

        print(f'Eligible users for {location} are {users}')
        if len(users) == 0:
            print(f"All users for this location already have a weather window, aborting")
            continue

        # Get weather forecast from DB for each of them, format as a dataframe
        forecasts_df = actions.get_forecast_for_tomorrow_from_db(location, to_pandas=True)

        # Get the best weather for each of them
        window = finder.get_weather_window_for_forecast(forecasts_df)

        # Generate the calendar invite
        timezone = geo.get_timezone_for_lat_lon(location.latitude, location.longitude)

        if dry_run:
            for u in users:
                eligible_users.append(f"Would send forecast for {window.weather_timestamp} to {u}")
        else:
            event = get_calendar_event(location, window, attendees=[user.email for user in users], timezone=timezone)
            calendar.create_event(event)
            actions.update_most_recent_invite(users)
            eligible_users.append(f"Sent forecast for {window.weather_timestamp} to {users}")
            time.sleep(DELAY_IN_S)

    print('\n'.join(eligible_users))
    if dry_run:
        print(f'{len(eligible_users)} need invites')
    else:
        print(f'{len(eligible_users)} received invites')


if __name__ == '__main__':
    get_credentials_from_s3.main()
    app = create_app()
    app.app_context().push()
    main(dry_run=True)
