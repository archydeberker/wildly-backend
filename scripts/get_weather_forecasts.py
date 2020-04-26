import actions
import models
from app_factory import create_app


def main():

    # Get all the locations in the database
    for location in models.Location.query.all():
        print(f'Getting forecast for {location}')
        actions.add_tomorrows_forecast_to_db(location)


if __name__ == '__main__':

    app = create_app()
    app.app_context().push()

    main()