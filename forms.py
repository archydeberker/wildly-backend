from dataclasses import dataclass

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError
from preferences import DefaultPreferences


class RegisterForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired()])
    postcode = StringField('Your Postcode', validators=[DataRequired()])
    submit = SubmitField('Register')


class UnsubscribeForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired()])
    submit = SubmitField('Unsubscribe')


class PreferencesForm(FlaskForm):
    day_start = SelectField('day_start', choices=DefaultPreferences.hours, default=DefaultPreferences.day_start)
    day_end = SelectField('day_end', choices=DefaultPreferences.hours, default=DefaultPreferences.day_end)
    temperature = SelectField('Temperature', choices=DefaultPreferences.temperature_options,
                              default=DefaultPreferences.temperature)
    activities = SelectMultipleField('Activities', choices=DefaultPreferences.activity_options)

    def validate(self):
        """
        Custom validation to ensure day start is not after day end
        """
        super().validate()
        if DefaultPreferences.hours.index(self.day_start.data) >= DefaultPreferences.hours.index(self.day_end.data):
            raise ValidationError('Your day must end after it begins and last an hour or more!')
        return True
