from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(1000))
    lastlogin = db.Column(db.DateTime)


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    name = db.Column(db.String(1000))
    img = db.Column(db.String(1000))


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))


class Weather(db.Model):
    """
    This table stores both forecasts and nowcasts.

    The triple primary key (location, recorded timestamp, weather timestamp) defines a row stored at
    `recorded_timestamp` pertaining to `location` at `weather_timestamp`. This allows us to distinguish between
    forecasts of the same timepoint made at different times.

    """
    location = db.Column(db.Integer, db.ForeignKey("location.id"), primary_key=True)
    recorded_timestamp = db.Column(db.DateTime, primary_key=True)
    weather_timestamp = db.Column(db.DateTime, primary_key=True)
    apparent_temperature = db.Column(db.Float)
    cloud_cover = db.Column(db.String(1000))
    dew_point = db.Column(db.Float)
    humidity = db.Column(db.Float)
    icon = db.Column(db.String(1000))
    ozone = db.Column(db.Float)
    precip_accumulation = db.Column(db.Float)
    precip_intensity = db.Column(db.Float)
    precip_probability = db.Column(db.Float)
    precip_type = db.Column(db.Float)
    pressure = db.Column(db.Float)
    summary = db.Column(db.String(1000))
    temperature = db.Column(db.Float)
    uvIndex = db.Column(db.Float)
    visibility = db.Column(db.Float)
    windBearing = db.Column(db.Float)
    windGust = db.Column(db.Float)
    windSpeed = db.Column(db.Float)


trips = db.Table(
    "trips",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column(
        "activity_id", db.Integer, db.ForeignKey("activity.id"), primary_key=True
    ),
    db.Column(
        "location_id", db.Integer, db.ForeignKey("location.id"), primary_key=True
    ),
    db.Column("timestamp", db.DateTime, primary_key=True),
)

tags = db.Table(
    "tags",
    db.Column(
        "activity_id", db.Integer, db.ForeignKey("activity.id"), primary_key=True
    ),
    db.Column(
        "location_id", db.Integer, db.ForeignKey("location.id"), primary_key=True
    ),
)

user_interests = db.Table(
    "user_interests",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column(
        "activity_id", db.Integer, db.ForeignKey("activity.id"), primary_key=True
    ),
)

user_locations = db.Table(
    "user_locations",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column(
        "location_id", db.Integer, db.ForeignKey("location.id"), primary_key=True
    ),
)


