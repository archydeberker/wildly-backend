import os
import sys

import actions
import constants
import models
from app import app

sys.path.insert(1, os.path.join(sys.path[0], ".."))



if __name__ == "__main__":
    """ Add default data into the database"""
    app.app_context().push()
    [actions.add_or_return_activity(activity) for activity in constants.activities]
    models.db.session.commit()
