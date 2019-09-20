import models


def add_or_return_activity(activity):
    activity_row = models.Activity.query.filter_by(name=activity).first()
    if activity_row is None:
        activity_row = models.Activity(name=activity)

        models.db.session.add(activity_row)
        models.db.session.commit()

    return activity_row

