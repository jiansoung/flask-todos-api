# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
from app.models import User
from app.lib import Message
from app.auth import AuthenticateUser
from .concerns import only_allow, dict_copy

__all__ = []
blueprint = Blueprint('users_controller', __name__)


@blueprint.route("/users")
def index():
    users = [user.to_dict() for user in User.query.all()]
    return jsonify(users)


@blueprint.route("/signup", methods=["POST"])
@blueprint.route("/users", methods=["POST"])
def create():
    user_params = request.user_params
    _ = User.create(user_params)  # Exception
    email, password = user_params['email'], user_params['password']
    auth_token = AuthenticateUser(email, password).auth_token
    response = { 'message': Message.account_created, 'auth_token': auth_token }
    return jsonify(response), 201


@blueprint.route("/users/<int:user_id>")
def show(user_id):
    user = request.user
    return jsonify(user.to_dict())


@blueprint.route("/users/<int:user_id>", methods=["PUT"])
def update(user_id):
    user = request.user
    user_params = request.user_params
    user.update(user_params)
    return jsonify(), 204


@blueprint.route("/users/<int:user_id>", methods=['DELETE'])
def destroy(user_id):
    user = request.user
    user.destroy()
    return jsonify(), 204


@blueprint.before_request
@only_allow([show, update, destroy], blueprint)
def set_user():
    view_args = request.view_args
    if 'user_id' in view_args:
        request.user = User.query.get_or_404(view_args['user_id'])


@blueprint.before_request
@only_allow([create, update], blueprint)
def set_user_params():
    params = request.json
    keys = ['name', 'email', 'password']
    request.user_params = dict_copy(params, keys)
