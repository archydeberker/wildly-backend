import json

from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

import actions
import models
from auth import (AuthError, get_token_auth_header, requires_auth,
                  requires_scope, retrieve_user_info)

api = Blueprint("api", __name__)


@api.route("/")
def home():
    return 'Hello world'


@api.route("/ping")
def ping():
    return 'pong'


@api.route("/api/add-user", methods=["POST"])
def add_user():
    print(request)
    postcode = request.json.pop("postcode")
    location = actions.add_or_return_location(dict(postcode=postcode))
    email = request.json.pop("email")
    user = actions.add_or_return_user(email, location)
    print(user)
    return jsonify(user.to_dict())
