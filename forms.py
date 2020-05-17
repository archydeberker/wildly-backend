from dataclasses import dataclass

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired

HOURS = []
[[HOURS.append(str(hour) + period) for hour in range(1, 13)] for period in ['AM', 'PM']]



@dataclass
class Time:
    label: str
    selected: bool



start_times = {h: Time(label=h, selected=False) for h in HOURS}
end_times = {h: Time(label=h, selected=False) for h in HOURS}
start_times['7AM'] = Time(label='7AM', selected=True)
end_times['6PM'] = Time(label='6PM', selected=True)


class RegisterForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired()])
    postcode = StringField('Your Postcode', validators=[DataRequired()])
    submit = SubmitField('Register')


class UnsubscribeForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired()])
    submit = SubmitField('Unsubscribe')


class PreferencesForm(FlaskForm):
    day_start = SelectField('Between', choices=list(start_times.values()))
    day_end = SelectField('and', choices=list(end_times.values()))
    temperature = DecimalField('Temperature', places=5)
