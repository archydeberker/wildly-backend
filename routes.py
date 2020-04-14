import flask
from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for
from forms import RegisterForm
import actions
import auth
from flask_mail import Mail
from flask import current_app as app

api = Blueprint("api", __name__)


@api.route("/", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash(f"We've sent a confirmation email to {form.email.data}, please check your inbox!")
        actions.register_new_user(form.email.data, form.postcode.data)

    return render_template('register.html', title='Register', form=form)


@api.route("/")
def index():
    return render_template('base.html')


@api.route("/ping")
def ping():
    host = flask.request.host_url
    print(host)
    return 'pong'


@api.route("/confirm/<token>", methods=["GET", "POST"])
def confirm_email(token):
    host = flask.request.host_url
    print(host)
    email = auth.decode_token_to_email(token)
    if email is None:
        flash('This confirmation link is invalid or has expired', 'danger')
    else:
        print(f"Email confirmed for user {email}")
        user = actions.get_user(email)
        actions.set_email_verified(user_row=user)
        actions.send_tomorrow_window_to_user(user=user, host='weather-window-app.herokuapp.com')
        flash('Email confirmed, thanks!', 'success')

    return redirect(url_for('api.index'))


@api.route('/google79a68bb5bf16f86a.html')
def google_verification():
    return render_template('google.html')
