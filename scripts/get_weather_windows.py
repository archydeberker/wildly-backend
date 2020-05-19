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


def main():
    calendar = cal.Calendar()
    finder = weather.WeatherWindowFinder(preferences=weather.Preferences(temperature_weighting=constants.TEMPERATURE_WEIGHTINGS,
                                                                         weightings=constants.DEFAULT_WEIGHTINGS))

    # Get all the locations in the database
    for location in models.Location.query.all():
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

        event = get_calendar_event(location, window, attendees=[u.email for u in users], timezone=timezone)
        calendar.create_event(event)
        actions.update_most_recent_invite(users)


if __name__ == '__main__':
    get_credentials_from_s3.main()
    app = create_app()
    app.app_context().push()

    main()
