from flask_sqlalchemy import SQLAlchemy

from preferences import DefaultPreferences

db = SQLAlchemy()

# For an explanation of the models and relationships defined here, see
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/

# To keep things really simple, the weather windows are not (for now) stored anywhere, but dynamically computed.
# In the future it might make sense to add a Windows class which simply links together location_ids with specific
# forecast IDs.

user_interests = db.Table(
    "user_interests",
    db.Column(
        "activity_name",
        db.String(1000),
        db.ForeignKey("activity.name"),
        primary_key=True,
    ),
    db.Column(
        "preferences_id", db.Integer, db.ForeignKey("preferences.id"), primary_key=True
    ),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    email_verified = db.Column(db.Boolean, default=False)
    most_recent_invite = db.Column(db.DateTime, nullable=True)
    registered = db.Column(db.DateTime, nullable=True)

    # 1 to 1 relationship (each user has exactly one location & preferences)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), nullable=False)
    preferences = db.relationship('Preferences', backref='user', lazy=True, uselist=False)

    def __repr__(self):
        return f"<User {self.email}>"

    def to_dict(self):

        return {'email': self.email,
                'id': self.id,
                'verified': self.email_verified,
                'registered': self.reg_date,
                'place': self.location.place}


class Preferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day_start = db.Column(db.Integer, default=DefaultPreferences.day_start)
    day_end = db.Column(db.Integer, default=DefaultPreferences.day_end)
    temperature = db.Column(db.String(50), default=DefaultPreferences.temperature)

    # 1 to 1 relationship (each user has exactly one preference row)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # Many (preferences) to many (activities) relationships
    activities = db.relationship(
        "Activity", secondary=user_interests, backref="activities", lazy=True,
    )


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.String(100), nullable=False, unique=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    google_ref = db.Column(db.String(1000))

    # Many (forecasts, users) to 1 (location) relationship
    forecasts = db.relationship('Forecast', backref='location', lazy=True)
    users = db.relationship('User', backref='location', lazy=True)

    def __repr__(self):
        return f"<Location {self.place}>"


class Activity(db.Model):
    name = db.Column(db.String(1000), nullable=False, primary_key=True, unique=True)

    def __repr__(self):
        return f"<Activity {self.name}>"


class Forecast(db.Model):
    """
    This table stores both forecasts and nowcasts.

    The triple primary key (location, recorded timestamp, weather timestamp) defines a row stored at
    `recorded_timestamp` pertaining to `location` at `weather_timestamp`. This allows us to distinguish between
    forecasts of the same timepoint made at different times.

    It is setup to function with the darsky API, and based off
    https://github.com/archydeberker/ski-monitor/blob/master/db_utils.py

    """

    # Many to 1 relationship: each Forecast has 1 location, but each location has many forecasts
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), primary_key=True)

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
    precip_type = db.Column(db.String(10))
    pressure = db.Column(db.Float)
    summary = db.Column(db.String(1000))
    temperature = db.Column(db.Float)
    uv_index = db.Column(db.Float)
    visibility = db.Column(db.String(20))
    wind_bearing = db.Column(db.String(10))
    wind_gust = db.Column(db.Float)
    wind_speed = db.Column(db.Float)
