# -*- coding: utf-8 -*-

import functools
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
#from werkzeug import exceptions
from app.exceptions import exceptions
from app.lib import Message


def not_found(error):
    return jsonify(message=error.description), error.code


def bad_request(error):
    return jsonify(message=error.description), error.code


def missing_token(error):
    return jsonify(message=error.description), error.code


def invalid_token(error):
    return jsonify(message=error.description), error.code


def unauthorized_request(error):
    return jsonify(message=error.description), error.code


def sqlalchemy_error_handler(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError as e:
            # db.session.rollback()
            raise exceptions.RecordInvalid(Message.account_not_created)
    return decorator
