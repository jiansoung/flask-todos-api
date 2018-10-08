# -*- coding: utf-8 -*-

from flask import jsonify


def not_found(error):
    return jsonify(message=error.name), 404
