from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# For an explanation of the models and relationships defined here, see
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/


trips = db.Table("trips",
                 db.Column("trip_id", db.Integer, db.ForeignKey("trip.id"), primary_key=True),
                 db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True))

activities = db.Table(
    "tags",
    db.Column(
        "activity_name", db.String(1000), db.ForeignKey("activity.name"), primary_key=True
    ),
    db.Column(
        "location_id", db.Integer, db.ForeignKey("location.id"), primary_key=True
    ),
)

user_interests = db.Table(
    "user_interests",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column(
        "activity_name", db.String(1000), db.ForeignKey("activity.name"), primary_key=True
    ),
)

user_locations = db.Table(
    "user_locations",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column(
        "location_id", db.Integer, db.ForeignKey("location.id"), primary_key=True
    ),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(1000), nullable=False)
    last_login = db.Column(db.DateTime)

    # Many to many relationships
    locations = db.relationship('Location', secondary=user_locations,
                                backref='users', lazy=True)
    activities = db.relationship('Activity', secondary=user_interests,
                                 backref='users', lazy=True)
    trips = db.relationship('Trip', secondary=trips,
                                 backref='users ', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'


class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column("activity_name", db.String(1000), db.ForeignKey("activity.name"))
    location = db.Column("location_id", db.Integer, db.ForeignKey("location.id"))
    timestamp = db.Column("timestamp", db.DateTime)

    def __repr__(self):
        return f'<{self.location}, {self.activity}, {self.timestamp}>'


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    img = db.Column(db.String(1000))

    # Many to many relationships
    activities = db.relationship('Activity', secondary=activities, lazy='subquery',
                                 backref=db.backref('locations', lazy=True))

    def __repr__(self):
        return f'<Location {self.name}>'


class Activity(db.Model):
    name = db.Column(db.String(1000), nullable=False, primary_key=True)

    def __repr__(self):
        return f'<Activity {self.name}>'


class Weather(db.Model):
    """
    This table stores both forecasts and nowcasts.

    The triple primary key (location, recorded timestamp, weather timestamp) defines a row stored at
    `recorded_timestamp` pertaining to `location` at `weather_timestamp`. This allows us to distinguish between
    forecasts of the same timepoint made at different times.

    It is setup to function with the darsky API, and based off
    https://github.com/archydeberker/ski-monitor/blob/master/db_utils.py

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


