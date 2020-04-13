


# Get all the locations in the database
for locations in db:

    # Users who we will alert
    users = locations.users

    # Get weather forecast from DB for each of them, format as a dataframe
    df = dataframe_from_db

    # Get the best weather for each of them
    window = get_weather_window(df)

    # Generate the calendar invite

    event = Event(yadyayaya, users)

    # Invite them all to the event
    calendar.invite()
