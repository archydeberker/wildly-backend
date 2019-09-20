import json

from flask import jsonify, request
from flask import Blueprint
from flask_cors import cross_origin

from auth import requires_auth, requires_scope, AuthError

import models

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
    response = "Hello from a private endpoint! You need to be authenticated to see this."
    return jsonify(message=response)


@api.route("/api/add-location", methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
# @requires_auth
def add_location():
    loc = request.json
    activities = loc.pop('activities')
    new_location = models.Location(**loc)

    models.db.session.add(new_location)
    models.db.session.commit()
    return jsonify(request.json)


@api.route("/api/locations")
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def list_locations():
    locations = models.Location.query.all()

    return '\n'.join([f'{l.id}: {l.name}' for l in locations])


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

