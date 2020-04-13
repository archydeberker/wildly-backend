import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], ".."))
import models
import actions
from app import app

if __name__ == "__main__":
    """ Un-onboard users to allow us to test the onboarding again."""
    app.app_context().push()
    for email in ["stephaniewillis808@gmail.com", "berkerboy@googlemail.com"]:
        user = actions.add_or_return_user(dict(email=email, name=email.split("@")[0]))
        user.has_toured = False
        user.home_location = None
        user.locations = []

    models.db.session.add(user)
    models.db.session.commit()
