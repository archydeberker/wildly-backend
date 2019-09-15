from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(1000))
    lastlogin = db.Column(db.DateTime)


class Trips(db.Model):
    """ Store association between users, activities, and locations"""
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer)
    location = db.Column(db.Integer)
    activity = db.Column(db.Integer)


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    name = db.Column(db.String(1000))
    img = db.Column(db.String(1000))


class Activity(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))


class TagTable(db.Model):
    """
    Store the association between locations and activities
    """
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.Integer)
    location = db.Column(db.Integer)


class ActivityProfile(db.Model):
    """
    Store the association between users and activities

    """
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer)
    activity = db.Column(db.Integer)


class LocationProfile(db.Model):
    """
    Store the association between users and locations

    """
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer)
    location = db.Column(db.Integer)


class WeatherForecast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.Integer)
    lastupdated = db.Column(db.DateTime)

