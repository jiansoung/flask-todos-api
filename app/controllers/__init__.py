# -*- coding: utf-8 -*-

from app import app
from .concerns import exception_handler
from app.controllers import todos_controller
from app.controllers import items_controller
from app.controllers import users_controller


app.register_blueprint(todos_controller.blueprint)
app.register_blueprint(items_controller.blueprint)
app.register_blueprint(users_controller.blueprint)
app.register_error_handler(404, exception_handler.not_found)
