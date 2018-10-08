# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
from app.models import Todo, Item
from .concerns import only_allow, dict_copy

__all__ = []
blueprint = Blueprint('items_controller', __name__)


@blueprint.route("/todos/<int:todo_id>/items")
def index(todo_id):
    todo = request.todo
    items = [item.to_dict() for item in todo.items]
    return jsonify(items)


@blueprint.route("/todos/<int:todo_id>/items", methods=["POST"])
def create(todo_id):
    item_params = request.item_params
    item = Item.create(item_params)
    return jsonify(item.to_dict()), 201


@blueprint.route("/todos/<int:todo_id>/items/<int:item_id>")
def show(todo_id, item_id):
    item = request.todo_item
    return jsonify(item.to_dict())


@blueprint.route("/todos/<int:todo_id>/items/<int:item_id>", methods=["PUT"])
def update(todo_id, item_id):
    item = request.todo_item
    item_params = request.item_params
    item.update(item_params)
    return jsonify(), 204


@blueprint.route("/todos/<int:todo_id>/items/<int:item_id>", methods=['DELETE'])
def destroy(todo_id, item_id):
    item = request.todo_item
    item.destroy()
    return jsonify(), 204


@blueprint.before_request
def set_todo():
    view_args = request.view_args
    if 'todo_id' in view_args:
        request.todo = Todo.query.get_or_404(view_args['todo_id'])


@blueprint.before_request
@only_allow([show, update, destroy], blueprint)
def set_todo_item():
    view_args = request.view_args
    if 'item_id' in view_args:
        request.todo_item = Item.query.get_or_404(view_args['item_id'])


@blueprint.before_request
@only_allow([create, update], blueprint)
def set_item_params():
    keys = ['name', 'done', 'todo_id']
    params = { **request.view_args, **request.json }
    request.item_params = dict_copy(params, keys)
