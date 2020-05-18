from dataclasses import dataclass

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError

HOURS = []
[[HOURS.append(str(hour) + period) for hour in range(1, 13)] for period in ['AM', 'PM']]


class RegisterForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired()])
    postcode = StringField('Your Postcode', validators=[DataRequired()])
    submit = SubmitField('Register')


class UnsubscribeForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired()])
    submit = SubmitField('Unsubscribe')


class PreferencesForm(FlaskForm):
    day_start = SelectField('day_start', choices=HOURS, default=7)
    day_end = SelectField('day_end', choices=HOURS, default=19)
    temperature = SelectField('Temperature', choices=[("cold", 'I like it cool'),
                                                      ("neutral", "I don't really mind"),
                                                      ("hot", "I like it hot")
                                                      ],
                              default=1)
    activities = SelectMultipleField('Activities', choices=['Walking',
                                                           'Running',
                                                           'Cycling',
                                                           'Yoga',
                                                           'Meditating',
                                                           'Other',
                                                           ])

    def validate(self):
        """
        Custom validation to ensure day start is not after day end
        """
        super().validate()
        if HOURS.index(self.day_start.data) >= HOURS.index(self.day_end.data):
            raise ValidationError('Your day must end after it begins and last an hour or more!')
        return True
