import json

from flask import jsonify, request
from flask import Blueprint
from flask_cors import cross_origin

from auth import requires_auth, requires_scope, AuthError, get_token_auth_header, retrieve_user_info

import models
import actions
api = Blueprint('api', __name__)


@api.route("/api/public")
@cross_origin(headers=["Content-Type", "Authorization"])
def public():
    response = "Hello from a public endpoint! You don't need to be authenticated to see this."
    return jsonify(message=response)


@api.route("/api/private")
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def private():
    token = get_token_auth_header()
    user = retrieve_user_info(token)
    response = f"Hello {user['given_name']}, this is a private endpoint! You need to be authenticated to see this."

    return jsonify(message=response)


@api.route("/api/add-location", methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def add_location():
    location_request = request.json

    token = get_token_auth_header()
    user_info = retrieve_user_info(token)

    user = actions.add_or_return_user(user_info)

    actions.commit_new_location(location_request, user)

    return jsonify(location_request)


@api.route("/api/add-user", methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def add_user():
    token = get_token_auth_header()
    user = retrieve_user_info(token)
    actions.add_or_return_user(user)

    print(user)
    return jsonify(user)


@api.route("/api/locations")
@cross_origin(headers=["Content-Type", "Authorization"])
# @requires_auth
def list_locations():
    locations = models.Location.query.all()

    return '\n'.join([f'{l.id}: {l.name}, {l.users}' for l in locations])


@api.route("/api/users")
@cross_origin(headers=["Content-Type", "Authorization"])
# @requires_auth
def list_users():
    users = models.User.query.all()

    return '\n'.join([f'{u.name}: {u.email}' for u in users])


@api.route("/api/activities")
@cross_origin(headers=["Content-Type", "Authorization"])
# @requires_auth
def list_activities():
    locations = models.Activity.query.all()

    return '\n'.join([f'{l.name}' for l in locations])


@api.route("/api/private-scoped")
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def private_scoped():
    if requires_scope("read:messages"):
        response = "Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this."
        return jsonify(message=response)
    raise AuthError({
        "code": "Unauthorized",
        "description": "You don't have access to this resource"
    }, 403)


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

