import models


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
