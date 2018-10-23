# -*- coding: utf-8 -*-

from app.exceptions import exceptions
from app.exceptions import exception_handler
from app.controllers import todos_controller
from app.controllers import items_controller
from app.controllers import users_controller


def init_app(app):
    app.register_blueprint(todos_controller.blueprint)
    app.register_blueprint(items_controller.blueprint)
    app.register_blueprint(users_controller.blueprint)

    #app.register_error_handler(404, exception_handler.not_found)
    #app.register_error_handler(422, exception_handler.bad_request)
    app.register_error_handler(
        exceptions.RecordNotFound, exception_handler.not_found
    )
    app.register_error_handler(
        exceptions.RecordInvalid, exception_handler.bad_request
    )
    app.register_error_handler(
        exceptions.MissingToken, exception_handler.missing_token
    )
    app.register_error_handler(
        exceptions.InvalidToken, exception_handler.invalid_token
    )
    app.register_error_handler(
        exceptions.AuthenticationError, exception_handler.unauthorized_request
    )
