# -*- coding: utf-8 -*-

from flask import jsonify


def not_found(error):
    return jsonify(message=error.name), 404


def bad_request(error):
    return jsonify(message=error.name), 422


def invalid_token(error):
    pass
