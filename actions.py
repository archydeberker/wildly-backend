import datetime

import pandas as pd

import cal
import models
import weather
import geo
import auth
from flask_mail import Mail

from auth import compose_verifiation_email

mail = Mail()


def get_forecast_for_tomorrow_from_db(location: models.Location, to_pandas=True):
    today = datetime.datetime.now()
    forecasts = models.Forecast.query.filter(models.Forecast.weather_timestamp > today,
                                            models.Forecast.location_id == location.id)

    if to_pandas:
        output = pd.read_sql(forecasts.statement, forecasts.session.bind)
    else:
        output = forecasts.all()

    return output


def add_tomorrows_forecast_to_db(location: models.Location):
    forecast = weather.DarkSky()
    hourly_forecast = forecast.get_forecast_tomorrow(location.longitude, location.latitude)

    for row in hourly_forecast.to_dict('records'):
        row['location_id'] = location.id
        forecast = models.Forecast(**row)
        models.db.session.add(forecast)

    models.db.session.commit()


def register_new_user(email: str, postcode: str):
    location = add_or_return_location(postcode)
    user = add_or_return_user(email, location)

    html = compose_verifiation_email(email)

    auth.send_verification_email(email, 'Please confirm your email for Weather Window', html, mail)

    return user


def retrieve_location_for_user(user: dict):
    user_row = models.User.query.filter_by(email=user["email"]).first()

    return models.Location.query.filter_by(id=user_row.location.id).first()


def add_or_return_location(postcode: str):

    location_row = get_location_by_postcode(postcode)
    if location_row is None:
        location = dict(postcode=postcode)
        location['latitude'], location['longitude'] = geo.get_lat_lon_for_postcode(location['postcode'])
        location_row = models.Location(**location)
        models.db.session.add(location_row)

    return location_row


def get_location_by_postcode(postcode: str):
    return models.Location.query.filter_by(postcode=postcode).first()


def get_user(email: str):
    return models.User.query.filter_by(email=email).first()


def add_or_return_user(email: str, location: models.Location = None):

    user_row = models.User.query.filter_by(email=email).first()
    if user_row is None:
        if location is not None:
            user_row = models.User(email=email, location=location)
            models.db.session.add(user_row)
            models.db.session.commit()
        else:
            raise ValueError('User not found and no location specified')

    return user_row


def set_email_verified(user_row: models.User):
    user_row.email_verified = True
    models.db.session.add(user_row)
    models.db.session.commit()


def send_tomorrow_window_to_user(user: models.Location, host: str = 'localhost'):
    calendar = cal.Calendar(host=host)
    finder = weather.WeatherWindowFinder()

    location = user.location

    # In case it's a new location
    add_tomorrows_forecast_to_db(location)

    # Get weather forecast from DB for each of them, format as a dataframe
    forecasts_df = get_forecast_for_tomorrow_from_db(location, to_pandas=True)

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
                      attendees=[user.email],
                      timezone=timezone)

    calendar.create_event(event)