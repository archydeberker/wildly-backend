import models
import requests


def commit_new_location(location, user_row):
    """
    Handles the adding of new locations to the database, and the association of the relevant
    user and activity details.

    location_request: json object from POST reqeust
    user_row: database row corresponding to that user

    """

    activities = location.pop('activities')
    activities = [act['value'] for act in activities]

    # Retrieve an Unsplash photo associated with that activity and add that field. We don't want to actually have to
    # store the photo ourselves, so we will just save the unsplash URL and then use that to populate the frontend live

    r = requests.get(f"https://source.unsplash.com/800x600/?{','.join([a+'ing' for a in activities])}")

    location['img'] = r.url
    print(location['img'])
    new_location = models.Location(**location)

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


def get_location(location):
    return models.Location.query.filter_by(latitude=location['latitude'],
                                           longitude=location['longitude'],
                                           ).first()


def add_or_return_user(user):
    user_row = models.User.query.filter_by(email=user['email']).first()
    if user_row is None:
        user_row = models.User(email=user["email"],
                               name=user["name"])
        models.db.session.add(user_row)
        models.db.session.commit()

    return user_row


def get_locations_for_user(user):
    # token_row = add_or_return_token_for_user(token)
    user_row = models.User.query.filter_by(email=user["email"]).first()

    return user_row.locations
