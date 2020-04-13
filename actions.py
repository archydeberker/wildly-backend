import requests

import models
import geo


def retrieve_location_for_user(user: dict):
    user_row = models.User.query.filter_by(email=user["email"]).first()

    return models.Location.query.filter_by(id=user_row.location.id).first()


def add_home_location(user, location):
    """Create the `location` in the location table and associate it with a `user` """
    user_row = add_or_return_user(user)
    home_location = add_or_return_location(location)
    models.db.session.add(home_location)
    models.db.session.commit()
    user_row.location = home_location.id

    models.db.session.add(user_row)
    models.db.session.commit()


def add_or_return_location(location: dict):

    location_row = get_location(location)
    if location_row is None:
        location['latitude'], location['longitude'] = geo.get_lat_lon_for_postcode(location['postcode'])
        location_row = models.Location(**location)
        models.db.session.add(location_row)

    return location_row


def get_location(location):
    return models.Location.query.filter_by(postcode=location['postcode']).first()


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


def get_locations_for_user(user):
    user_row = add_or_return_user(user)

    return user_row.locations


def add_location_for_user(user, location):
    """ Add an existing location to an existing user"""
    user_row = add_or_return_user(user)
    user_row.locations += [get_location(location)]
    models.db.session.add(user_row)
    models.db.session.commit()


def set_email_verified(user_row: models.User):
    user_row.email_verified = True
    models.db.session.add(user_row)
    models.db.session.commit()
