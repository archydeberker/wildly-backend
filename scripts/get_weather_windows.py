import datetime

import actions
import models
import weather
import cal
import geo
from app import create_app


def main():
    calendar = cal.Calendar()
    finder = weather.WeatherWindowFinder()

    # Get all the locations in the database
    for location in models.Location.query.all():
        print(f'Getting users for {location}')
        # Users who we will alert
        users = location.users
        print(users)

        # Get weather forecast from DB for each of them, format as a dataframe
        forecasts_df = actions.get_forecast_for_tomorrow_from_db(location, to_pandas=True)

        # Get the best weather for each of them
        window = finder.get_weather_window_for_forecast(forecasts_df)

        # Generate the calendar invite
        timezone = geo.get_timezone_for_lat_lon(location.latitude, location.longitude)
        event = cal.Event(location=location.postcode,
                          summary=f"Your weather window in {location.postcode}",
                          description=f"It's going to be {window.summary}, "
                                      f"with a probability of rain of "
                                      f"{window.precip_probability} and feeling like "
                                      f"{window.apparent_temperature}°C",
                          start=window.weather_timestamp,
                          end=window.weather_timestamp + datetime.timedelta(hours=1),
                          attendees=[u.email for u in users],
                          timezone=timezone)

        calendar.create_event(event)


if __name__ == '__main__':

    app = create_app()
    app.app_context().push()

    main()
