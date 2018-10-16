# -*- coding: utf-8 -*-

import functools
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from werkzeug import exceptions


def not_found(error):
    return jsonify(message=error.name), 404


def bad_request(error):
    return jsonify(message=error.name), 422


def missing_token(error):
    return jsonify(message=error.name), 422


def invalid_token(error):
    pass


def unauthorized_request(error):
    return jsonify(message=error.name)


def sqlalchemy_error_handler(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError as e:
            # db.session.rollback()
            raise exceptions.UnprocessableEntity(e)
    return decorator
