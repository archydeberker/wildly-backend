import actions
import models
from app import create_app


def main():

    # Get all the locations in the database
    for location in models.Location.query.all():
        print(f'Getting users for {location}')
        # Users who we will alert
        users = location.users
        print(users)

        # # Get weather forecast from DB for each of them, format as a dataframe
        forecasts = actions.get_forecast_for_tomorrow_from_db(location)

        print(forecasts)
        #
        # # Get the best weather for each of them
        # window = get_weather_window(df)
        #
        # # Generate the calendar invite
        #
        # event = Event(yadyayaya, users)
        #
        # # Invite them all to the event
        # calendar.invite()



if __name__ == '__main__':

    app = create_app()
    app.app_context().push()

    main()
