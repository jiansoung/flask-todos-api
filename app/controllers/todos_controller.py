# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
from app.models import Todo
from .concerns import only_allow, dict_copy

__all__ = []
blueprint = Blueprint('todos_controller', __name__)


@blueprint.route("/todos")
def index():
    todos = [todo.to_dict() for todo in Todo.query.all()]
    return jsonify(todos)


@blueprint.route("/todos", methods=["POST"])
def create():
    todo_params = request.todo_params
    todo = Todo.create(todo_params)
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
@only_allow([show, update, destroy], blueprint)
def set_todo():
    view_args = request.view_args
    if 'todo_id' in view_args:
        request.todo = Todo.query.get_or_404(view_args['todo_id'])


@blueprint.before_request
@only_allow([create, update], blueprint)
def set_todo_params():
    params = request.json
    keys = ['title', 'created_by']
    request.todo_params = dict_copy(params, keys)
