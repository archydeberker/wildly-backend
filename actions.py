import datetime
from typing import List

import pandas as pd
from flask import url_for, render_template

import cal
import models
import weather
import geo
import auth
import preferences

from flask_mail import Mail

from auth import generate_confirmation_token

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


def add_new_user_to_db_with_default_preferences(email, location):
    user = add_or_return_user(email, location)
    prefs = preferences.create_default_preference_row()
    prefs.user_id = user.id

    models.db.session.add(prefs)
    models.db.session.commit()

    return user


def register_new_user(email: str, place: str):
    print(f"Received new user signup for {email} and {place}")
    location = add_or_return_location(place)
    duplicate_user = False
    user = models.User.query.filter_by(email=email).first()
    if user is None:
        user = add_new_user_to_db_with_default_preferences(email, location)
    else:
        duplicate_user = True

    html = compose_verification_email(email)

    auth.send_email(email, 'Please confirm your email for Weather Window', html, mail)
    print(f'Sent a verification email to {email} for {place}')

    return user, duplicate_user


def send_unsubscribe_email(email: str):
    user = get_user(email)
    if user:
        html = compose_unsubscribe_email(email)
        auth.send_email(email, 'Unsubscribe from Weather Window', html, mail)
    else:
        raise ValueError


def retrieve_location_for_user(user: dict):
    user_row = models.User.query.filter_by(email=user["email"]).first()

    return models.Location.query.filter_by(id=user_row.location.id).first()


def add_or_return_user_preferences(user_email: str):
    user_row = get_user(user_email)
    prefs = user_row.preferences
    if prefs is None:
        prefs = preferences.create_default_preference_row()
        prefs.user_id = user_row.id

    models.db.session.add(prefs)
    models.db.session.commit()

    return prefs


def add_or_return_location(place: str):
    location_row = get_location_by_place(place)
    if location_row is None:
        location = dict(place=place)
        location['latitude'], location['longitude'] = geo.get_lat_lon_for_place(location['place'])
        location_row = models.Location(**location)
        models.db.session.add(location_row)

    return location_row


def get_location_by_place(place: str):
    return models.Location.query.filter_by(place=place).first()


def get_user(email: str):
    return models.User.query.filter_by(email=email).first()


def delete_user(email: str):
    user = get_user(email)
    models.db.session.delete(user)
    print(f'Deleting user {email}')
    models.db.session.commit()


def add_user(email: str, location: models.Location):
    user_row = models.User(email=email, location=location, registered=datetime.datetime.now())
    models.db.session.add(user_row)
    models.db.session.commit()
    return user_row


def add_activity(activity_name: str):
    activity_row = models.Activity(name=activity_name)
    models.db.session.add(activity_row)
    models.db.session.commit()

    return activity_row


def add_or_return_activity(activity_name: str):
    activity_row = models.Activity.query.filter_by(name=activity_name).first()
    if activity_row is None:
        activity_row = add_activity(activity_name)

    return activity_row


def add_or_return_user(email: str, location: models.Location = None):
    user_row = models.User.query.filter_by(email=email).first()
    if user_row is None:
        if location is not None:
            user_row = add_user(email, location)
        else:
            raise ValueError('User not found and no location specified')

    return user_row


def set_email_verified(user_row: models.User):
    user_row.email_verified = True
    models.db.session.add(user_row)
    models.db.session.commit()


def update_most_recent_invite(users: List[models.User]):
    now = datetime.datetime.now()
    for u in users:
        u.most_recent_invite = now
        models.db.session.add(u)

    models.db.session.commit()


def send_tomorrow_window_to_user(user: models.User, host: str = 'localhost'):
    calendar = cal.Calendar(host=host)
    finder = weather.WeatherWindowFinder()

    location = user.location

    # In case it's a new location
    add_tomorrows_forecast_to_db(location)

    today = datetime.date.today()
    if not needs_invite_for_tomorrow(user, today):
        print("New user already has an invite, aborting")
        return

    # Get weather forecast from DB for each of them, format as a dataframe
    forecasts_df = get_forecast_for_tomorrow_from_db(location, to_pandas=True)

    # Get the best weather for each of them
    window = finder.get_weather_window_for_forecast(forecasts_df)

    # Generate the calendar invite
    timezone = geo.get_timezone_for_lat_lon(location.latitude, location.longitude)
    event = cal.get_calendar_event(location, window, attendees=[user.email], timezone=timezone)

    calendar.create_event(event)
    update_most_recent_invite([user])


def filter_users_who_already_have_invites_for_today(users):
    today = datetime.date.today()
    users = [u for u in users if needs_invite_for_tomorrow(u, today)]
    return users


def needs_invite_for_tomorrow(user: models.User, today):
    if user.email == 'berkerboy@gmail.com':
        return True
    if user.most_recent_invite is None:
        return True
    if user.most_recent_invite.date() == today:
        return False
    return True


def compose_verification_email(email: str):
    token = generate_confirmation_token(email)
    confirm_url = url_for('api.confirm_email', token=token, _external=True)
    unsubscribe_url = url_for('api.unsubscribe', token=token, _external=True)
    html = render_template('emails/activate.html', confirm_url=confirm_url, unsub_url=unsubscribe_url)
    return html


def compose_unsubscribe_email(email: str):
    token = generate_confirmation_token(email)
    unsubscribe_url = url_for('api.unsubscribe', token=token, _external=True)
    html = render_template('emails/unsubscribe.html', unsub_url=unsubscribe_url)
    return html
