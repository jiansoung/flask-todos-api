# -*- coding: utf-8 -*-

from flask import g, Blueprint, request, jsonify
from app.models import Todo, Item
from .concerns import only_allow, dict_copy, authorize_request
from app.exceptions import exceptions
from app.lib import Message

__all__ = []
blueprint = Blueprint('items_controller', __name__)


@blueprint.route("/todos/<int:todo_id>/items")
def index(todo_id):
    todo = request.todo
    items = [item.to_dict() for item in todo.items]
    return jsonify(items)


@blueprint.route("/todos/<int:todo_id>/items", methods=["POST"])
def create(todo_id):
    todo = request.todo
    item_params = request.item_params
    item = todo.create_item(item_params)
    return jsonify(item.to_dict()), 201


@blueprint.route("/todos/<int:todo_id>/items/<int:item_id>")
def show(todo_id, item_id):
    item = request.item
    return jsonify(item.to_dict())


@blueprint.route("/todos/<int:todo_id>/items/<int:item_id>", methods=["PUT"])
def update(todo_id, item_id):
    item = request.item
    item_params = request.item_params
    item.update(item_params)
    return jsonify(), 204


@blueprint.route("/todos/<int:todo_id>/items/<int:item_id>", methods=['DELETE'])
def destroy(todo_id, item_id):
    item = request.item
    item.destroy()
    return jsonify(), 204


@blueprint.before_request
def need_authorize_request():
    authorize_request()


@blueprint.before_request
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
@only_allow([show, update, destroy], blueprint)
def set_item():
    if not hasattr(request, 'todo'):
        set_todo()
    view_args = request.view_args
    if 'item_id' in view_args:
        todo = request.todo
        item_id = view_args['item_id']
        item = Item.query.filter_by(id=item_id, todo=todo).first()
        if item is None:
            raise exceptions.RecordNotFound(Message.not_found())
        request.item = item


@blueprint.before_request
@only_allow([create, update], blueprint)
def set_item_params():
    keys = ['name', 'done', 'todo_id']
    params = { **request.view_args, **request.json }
    request.item_params = dict_copy(params, keys)
