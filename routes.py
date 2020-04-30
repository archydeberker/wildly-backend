from smtplib import SMTPRecipientsRefused
from sqlite3 import IntegrityError

import flask
from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for
from itsdangerous import BadSignature

from forms import RegisterForm
import actions
import constants
import auth

api = Blueprint("api", __name__)


@api.route("/", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            _, duplicate_user = actions.register_new_user(form.email.data, form.postcode.data)
            if duplicate_user:
                flash(f" We seem to have you registered already, but we've resent your confirmation email!")
            else:
                flash(f"We've sent a confirmation email to {form.email.data}, please check your inbox!")
        except SMTPRecipientsRefused:
            flash(f"We couldn't send an email to {form.email.data}, please check and try again!", category="warning")
        except IndexError:
            flash(f" We couldn't find a location for {form.postcode.data}, please check and try again!")

    return render_template('register.html', title='Weather Window', form=form, GOOGLE_API_KEY=constants.GOOGLE_API_KEY)


@api.route("/")
def index():
    return render_template('base.html')


@api.route("/flash")
def test_flash():
    flash('This is a test flash')
    return render_template('base.html')


@api.route("/ping")
def ping():
    return 'pong'


@api.route("/confirm/<token>", methods=["GET", "POST"])
def confirm_email(token):
    email = auth.decode_token_to_email(token)
    if email is None:
        flash('This confirmation link is invalid or has expired', 'danger')
    else:
        print(f"Email confirmed for user {email}")
        user = actions.get_user(email)
        if user is None:
            flash('Uho, you were already unsubscribed! Please subscribe again')
        actions.set_email_verified(user_row=user)
        # TODO: we can do this async, move it to a cron job

        actions.send_tomorrow_window_to_user(user=user)
        flash('Email confirmed, thanks! Check your calendar, you should have an invite for tomorrow!', 'success')

    return redirect(url_for('api.index'))


@api.route("/unsubscribe/<token>", methods=["GET", "POST"])
def unsubscribe(token):
    try:
        email = auth.decode_token_to_email(token)
        if email is None:
            flash('This unsubscribe link is invalid! Please try again', 'danger')
        else:
            print(f"Unsubscribe confirmed for user {email}")
            actions.delete_user(email)

            flash("You've been unsubscribed. Starting tomorrow, you won't receive new invites.", 'success')

    except BadSignature:
        print('Bad signature error')

    return redirect(url_for('api.index'))


@api.route('/google79a68bb5bf16f86a.html')
def google_verification():
    return render_template('google.html')
