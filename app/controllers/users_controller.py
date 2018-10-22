# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
from app.models import User
from app.lib import Message
from app.auth import AuthenticateUser
from .concerns import only_allow, dict_copy

__all__ = []
blueprint = Blueprint('users_controller', __name__)


@blueprint.route("/signup", methods=["POST"])
def signup():
    user_params = request.user_params
    User.create(user_params)
    email, password = user_params['email'], user_params['password']
    auth_token = AuthenticateUser(email, password).auth_token
    response = { 'message': Message.account_created, 'auth_token': auth_token }
    return jsonify(response), 201


@blueprint.route("/signin", methods=["POST"])
def signin():
    user_params = request.user_params
    email, password = user_params['email'], user_params['password']
    auth_token = AuthenticateUser(email, password).auth_token
    return jsonify(auth_token=auth_token), 200


@blueprint.before_request
@only_allow([signup, signin], blueprint)
def set_user_params():
    params = request.json
    keys = ['name', 'email', 'password']
    request.user_params = dict_copy(params, keys)
