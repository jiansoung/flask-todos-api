# -*- coding: utf-8 -*-

import functools
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from werkzeug import exceptions


def sqlalchemy_error_handler(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError as e:
            # db.session.rollback()
            raise exceptions.UnprocessableEntity(e)
    return decorator
