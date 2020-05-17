from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired

HOURS = []
[[HOURS.append(str(hour) + period) for hour in range(1, 13)] for period in ['AM', 'PM']]

DURATIONS = ['0.5h', '1h', '1.5h']


class RegisterForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired()])
    postcode = StringField('Your Postcode', validators=[DataRequired()])
    submit = SubmitField('Register')


class UnsubscribeForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired()])
    submit = SubmitField('Unsubscribe')


class PreferencesForm(FlaskForm):
    day_start = SelectField('Between', HOURS)
    day_end = SelectField('and', HOURS)
    duration = SelectField('Duration', DURATIONS)
    temperature = DecimalField('Temperature', places=5)
