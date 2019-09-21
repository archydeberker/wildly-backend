import models


def add_new_location(location):
    activities = location.pop('activities')
    new_location = models.Location(**location)

    new_location.activities = [add_or_return_activity(act['value']) for act in activities]

    models.db.session.add(new_location)

    # Associate the new location to the currently logged in user

    models.db.session.commit()


def add_or_return_activity(activity):
    activity_row = models.Activity.query.filter_by(name=activity).first()
    if activity_row is None:
        activity_row = models.Activity(name=activity)

        models.db.session.add(activity_row)
        models.db.session.commit()

    return activity_row


def add_or_return_user(user):
    user_row = models.User.query.filter_by(email=user['email']).first()
    if user_row is None:
        user_row = models.User(email=user["email"],
                               name=user["name"])

        models.db.session.add(user_row)
        models.db.session.commit()

    return user_row
