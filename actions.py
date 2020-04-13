import requests

import models


def retrieve_location(user: dict):
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


def commit_new_location(location, user_row):
    """
    Handles the adding of new locations to the database, and the association of the relevant
    user and activity details.

    location_request: json object from POST reqeust
    user_row: database row corresponding to that user

    """
    if len(location) == 0:
        return

    activities = location.pop("activities", [])
    activities = [act["value"] for act in activities]

    # Retrieve an Unsplash photo associated with that activity and add that field. We don't want to actually have to
    # store the photo ourselves, so we will just save the unsplash URL and then use that to populate the frontend live

    r = requests.get(
        f"https://source.unsplash.com/800x600/?{','.join([a+'ing' for a in activities])}"
    )

    location["img"] = r.url
    new_location = add_or_return_location(location)

    new_location.activities = [add_or_return_activity(a) for a in activities]
    new_location.users.append(user_row)

    models.db.session.add(new_location)
    models.db.session.commit()


def add_or_return_activity(activity):
    activity_row = models.Activity.query.filter_by(name=activity).first()
    if activity_row is None:
        activity_row = models.Activity(name=activity)
        models.db.session.add(activity_row)

    return activity_row


def add_or_return_location(location):

    location_row = get_location(location)
    print(location)
    if location_row is None:
        location_row = models.Location(**location)
        models.db.session.add(location_row)

    return location_row


def get_location(location):
    return models.Location.query.filter_by(
        latitude=location["latitude"], longitude=location["longitude"],
    ).first()


def add_or_return_user(user):
    user_row = models.User.query.filter_by(email=user["email"]).first()
    if user_row is None:
        user_row = models.User(email=user["email"], name=user["name"])
        models.db.session.add(user_row)
        models.db.session.commit()

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


def add_locations_and_activities_for_user(user, locations, activities):
    user_row = add_or_return_user(user)
    print(locations)
    print(activities)
    user_row.locations += [get_location(location) for location in locations]
    user_row.activities += [
        add_or_return_activity(activity["value"]) for activity in activities
    ]

    print(user_row.locations)
    print(user_row.activities)
    models.db.session.add(user_row)
    models.db.session.commit()


def set_email_verified(user_row: models.User):
    user_row.email_verified = True
    models.db.session.add(user_row)
    models.db.session.commit()
