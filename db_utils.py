from app import create_app
import models


def add_or_return_activity(activity):
    activity_row = models.Activity.query.filter_by(name=activity['name']).first()
    if activity_row is None:
        activity_row = models.Activity(**activity)

        models.db.session.add(activity_row)
        models.db.session.commit()

    return activity_row


if __name__ == '__main__':
    app = create_app()
    app.app_context().push()
    add_or_return_activity({'name': 'dogging'})
