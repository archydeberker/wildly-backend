import actions
import models
import weather


def main():



    # Get all the locations in the database
    for location in models.Location.Query.all():
        actions.add_tomorrows_forecast_to_db(location)


if __name__ == '__main__':

    main()