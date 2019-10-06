import models
from auth import retrieve_user_info


def commit_new_location(location, user_row):
    """
    Handles the adding of new locations to the database, and the association of the relevant
    user and activity details.

    location_request: json object from POST reqeust
    user_row: database row corresponding to that user

    """

    activities = location.pop('activities')
    new_location = models.Location(**location)

    new_location.activities = [add_or_return_activity(act['value']) for act in activities]
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


def add_or_return_token_for_user(token, user_info=None):

    token_row = models.Token.query.filter_by(token=token).first()

    if token_row is None:
        print(f"Unable to retrieve token row for user {token}")

        if user_info is None:
            user_info = retrieve_user_info(token)

        token_row = models.Token(token=token,
                                 email=user_info["email"],
                                 name=user_info["name"])
        models.db.session.add(token_row)
        models.db.session.commit()
        print(f'Added {token} to db')
    return token_row


def get_locations_for_user(user):
    # token_row = add_or_return_token_for_user(token)
    user_row = models.User.query.filter_by(email=user["email"]).first()

    return user_row.locations


