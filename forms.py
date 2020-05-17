from dataclasses import dataclass

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired

HOURS = []
[[HOURS.append(str(hour) + period) for hour in range(1, 13)] for period in ['AM', 'PM']]



@dataclass
class Option:
    label: str
    selected: bool



start_times = {h: Option(label=h, selected=False) for h in HOURS}
end_times = {h: Option(label=h, selected=False) for h in HOURS}
start_times['7AM'] = Option(label='7AM', selected=True)
end_times['6PM'] = Option(label='6PM', selected=True)


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
    temperature = SelectField('Temperature', choices=[Option(label='I like it cool', selected=False),
                                                      Option(label="I don't really mind ", selected=True),
                                                      Option(label='I like it hot', selected=False)
                                                      ])
    activities = SelectMultipleField('Activities', choices=[Option(label='Walking', selected=False),
                                                           Option(label='Running', selected=False),
                                                           Option(label='Cycling', selected=False),
                                                           Option(label='Yoga', selected=False),
                                                           Option(label='Meditating', selected=False),
                                                           Option(label='Other', selected=False)
                                                           ])
