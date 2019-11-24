import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import models
import actions
from app import app

if __name__ == '__main__':
    """ Un-onboard a test user to allow us to test the onboarding again."""
    app.app_context().push()
    user = actions.add_or_return_user(dict(email='berkerboy@googlemail.com'))
    user.has_toured = False
    user.home_location = None

    models.db.session.add(user)
    models.db.session.commit()
