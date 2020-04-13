from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired()])
    postcode = StringField('Your Postcode', validators=[DataRequired()])
    submit = SubmitField('Register')