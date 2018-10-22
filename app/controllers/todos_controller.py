# -*- coding: utf-8 -*-

from flask import g, Blueprint, request, jsonify
from app.models import Todo
from .concerns import only_allow, dict_copy, authorize_request
from app.exceptions import exceptions
from app.lib import Message

__all__ = []
blueprint = Blueprint('todos_controller', __name__)


@blueprint.route("/todos")
def index():
    current_user = g.current_user
    todos = [todo.to_dict() for todo in current_user.todos]
    return jsonify(todos)


@blueprint.route("/todos", methods=["POST"])
def create():
    user = g.current_user
    todo_params = request.todo_params
    todo = user.create_todo(todo_params)
    return jsonify(todo.to_dict()), 201


@blueprint.route("/todos/<int:todo_id>")
def show(todo_id):
    todo = request.todo
    return jsonify(todo.to_dict())


@blueprint.route("/todos/<int:todo_id>", methods=["PUT"])
def update(todo_id):
    todo = request.todo
    todo_params = request.todo_params
    todo.update(todo_params)
    return jsonify(), 204


@blueprint.route("/todos/<int:todo_id>", methods=['DELETE'])
def destroy(todo_id):
    todo = request.todo
    todo.destroy()
    return jsonify(), 204


@blueprint.before_request
def need_authorize_request():
    authorize_request()


@blueprint.before_request
@only_allow([show, update, destroy], blueprint)
def set_todo():
    if 'current_user' not in g:
        authorize_request()
    view_args = request.view_args
    if 'todo_id' in view_args:
        todo_id = view_args['todo_id']
        todo = Todo.query.filter_by(id=todo_id, user=g.current_user).first()
        if todo is None:
            raise exceptions.RecordNotFound(Message.not_found())
        request.todo = todo


@blueprint.before_request
@only_allow([create, update], blueprint)
def set_todo_params():
    params = request.json
    keys = ['title', 'created_by']
    request.todo_params = dict_copy(params, keys)
