import requests

import models
import geo
import auth


def register_new_user(email: str, postcode: str):
    location = add_or_return_location(dict(postcode=postcode))
    user = add_or_return_user(email, location)
    auth.send_verification_email(user)

    return user


def retrieve_location_for_user(user: dict):
    user_row = models.User.query.filter_by(email=user["email"]).first()

    return models.Location.query.filter_by(id=user_row.location.id).first()


def add_or_return_location(location: dict):

    location_row = get_location(location)
    if location_row is None:
        location['latitude'], location['longitude'] = geo.get_lat_lon_for_postcode(location['postcode'])
        location_row = models.Location(**location)
        models.db.session.add(location_row)

    return location_row


def get_location(location):
    return models.Location.query.filter_by(postcode=location['postcode']).first()


def get_user(email:str):
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
