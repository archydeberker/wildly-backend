import json

from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

import actions
import models
from auth import (AuthError, get_token_auth_header, requires_auth,
                  requires_scope, retrieve_user_info)

api = Blueprint("api", __name__)


@api.route("/api/public")
@cross_origin(headers=["Content-Type", "Authorization"])
def public():
    response = (
        "Hello from a public endpoint! You don't need to be authenticated to see this."
    )
    return jsonify(message=response)


@api.route("/api/private")
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def private():
    token = get_token_auth_header()
    user = retrieve_user_info(token)
    response = f"Hello {user['given_name']}, this is a private endpoint! You need to be authenticated to see this."

    return jsonify(message=response)


@api.route("/api/add-location", methods=["POST"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def add_location():
    location_request = request.json.pop("location")
    user_info = request.json.pop("user")
    user = actions.add_or_return_user(user_info)

    actions.commit_new_location(location_request, user)

    return jsonify(location_request)


@api.route("/api/add-existing-location", methods=["POST"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def add_existing_location():
    print(request.json)
    location_request = request.json.pop("location")
    user_info = request.json.pop("user")
    actions.add_location_for_user(user_info, location_request)

    return jsonify(location_request)


@api.route("/api/add-user-home", methods=["POST"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def add_user_home():

    home_location = request.json.pop("home_location")
    locations = request.json.pop("locations", [])
    activities = request.json.pop("activities", [])
    user = request.json.pop("user")

    actions.add_home_location(user, home_location)
    actions.add_locations_and_activities_for_user(user, locations, activities)

    return jsonify(home_location)


@api.route("/api/add-user", methods=["POST"])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def add_user():
    """
    This initializes the user in the backend. However, we have to be a bit careful
    because calling this route too many times can cause timeouts from Auth0.

    The riddle is, we have no way of telling whether this user is in the database or not
    based upon the token, *without* hitting the API. I'm not sure how to deal with this.
    """
    print(request.json)
    user = request.json
    # token = get_token_auth_header()
    # user = retrieve_user_info(token)
    actions.add_or_return_user(user)

    return jsonify(user)


@api.route("/api/locations")
@cross_origin(headers=["Content-Type", "Authorization"])
def list_locations():
    locations = models.Location.query.all()

    return jsonify(
        [
            {
                "name": l.name,
                "lat": l.latitude,
                "long": l.longitude,
                "img": l.img,
                "activities": [a.name for a in l.activities],
            }
            for l in locations
        ]
    )


@api.route("/api/user-locations", methods=["POST"])
@cross_origin(headers=["Content-Type", "Authorization"])
# @requires_auth
def list_locations_for_current_user():
    user = request.json
    locations = actions.get_locations_for_user(user)
    return jsonify(
        [
            {
                "name": l.name,
                "lat": l.latitude,
                "long": l.longitude,
                "img": l.img,
                "activities": [a.name for a in l.activities],
            }
            for l in locations
        ]
    )


@api.route("/api/user-onboarded", methods=["POST"])
@cross_origin(headers=["Content-Type", "Authorization"])
# @requires_auth
def check_onboarding():
    user_info = request.json
    print(user_info)
    user = actions.add_or_return_user(user_info)
    home = user.home_location
    print(home)
    return jsonify(home is not None)


@api.route("/api/user-home", methods=["POST"])
@cross_origin(headers=["Content-Type", "Authorization"])
# @requires_auth
def user_home():
    user_info = request.json
    home = actions.retrieve_home_location(user_info)
    print(home.latitude)
    return jsonify(
        {"name": home.name, "latitude": home.latitude, "longitude": home.longitude}
    )


@api.route("/api/user-toured", methods=["POST"])
@cross_origin(headers=["Content-Type", "Authorization"])
def check_touring():
    user_info = request.json.pop("user")
    user = actions.add_or_return_user(user_info)

    return jsonify(user.has_toured)


@api.route("/api/set-user-toured", methods=["POST"])
@cross_origin(headers=["Content-Type", "Authorization"])
def set_user_touring():
    user_info = request.json.pop("user")
    user = actions.add_or_return_user(user_info)
    actions.set_email_verified(user)
    return jsonify(user.has_toured)


@api.route("/api/users")
@cross_origin(headers=["Content-Type", "Authorization"])
# @requires_auth
def list_users():
    users = models.User.query.all()

    return "\n".join([f"{u.name}: {u.email}" for u in users])


@api.route("/api/activities")
@cross_origin(headers=["Content-Type", "Authorization"])
# @requires_auth
def list_activities():
    locations = models.Activity.query.all()

    return jsonify([f"{l.name}" for l in locations])


@api.route("/api/private-scoped")
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def private_scoped():
    if requires_scope("read:messages"):
        response = "Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this."
        return jsonify(message=response)
    raise AuthError(
        {
            "code": "Unauthorized",
            "description": "You don't have access to this resource",
        },
        403,
    )


@api.route("/ping")
def ping():
    return json.dumps({"result": "pong"})


@api.after_request
def after_request(response):
    header = response.headers
    header["Access-Control-Allow-Origin"] = "*"
    return response


@api.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
