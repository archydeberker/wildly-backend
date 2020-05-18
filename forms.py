from dataclasses import dataclass

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError

import models
from preferences import DefaultPreferences, parse_time_to_int


def parse_temperature(option):
    parsed = option.strip("\\'(),")
    print(parsed)
    return parsed


class RegisterForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired()])
    postcode = StringField('Your Postcode', validators=[DataRequired()])
    submit = SubmitField('Register')


class UnsubscribeForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired()])
    submit = SubmitField('Unsubscribe')


class PreferencesForm(FlaskForm):
    day_start = SelectField('day_start',
                            choices=DefaultPreferences.hours,
                            default=DefaultPreferences.day_start,
                            coerce=parse_time_to_int)
    day_end = SelectField('day_end',
                          choices=DefaultPreferences.hours,
                          default=DefaultPreferences.day_end,
                          coerce=parse_time_to_int)
    temperature = SelectField('Temperature', choices=DefaultPreferences.temperature_options,
                              default=DefaultPreferences.temperature,
                              coerce=parse_temperature)
    activities = SelectMultipleField('Activities', choices=DefaultPreferences.activity_options)

    def validate(self):
        """
        Custom validation to ensure day start is not after day end
        """
        super().validate()
        if self.day_start.data >= self.day_end.data:
            raise ValidationError('Your day must end after it begins and last an hour or more!')
        return True

    def initialize_from_db(self, preferences: models.Preferences):
        """
        Initialize the values of the form from an entry in the `Preferences` table of the database.
        """
        self.day_start.default = preferences.day_start
        self.day_end.default = preferences.day_end
        self.temperature.default = preferences.temperature
        self.activities.default = preferences.activities

        print('Initialized')