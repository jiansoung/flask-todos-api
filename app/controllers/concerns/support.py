# -*- coding: utf-8 -*-

import copy
import functools
from flask import g
from flask import request
from app.auth import AuthorizeApiRequest


def authorize_request():
    print(request.headers)
    current_user = AuthorizeApiRequest(request.headers).user
    g.current_user = current_user


def only_allow(view_functions, blueprint):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if is_request_allowed(view_functions, blueprint):
                return func(*args, **kwargs)
        return wrapper
    return decorator


def endpoint_for(view_function, blueprint):
    return '{}.{}'.format(blueprint.name, view_function.__name__)


def is_request_allowed(view_functions, blueprint):
    endpoint = request.url_rule.endpoint
    allowed_endpoints = [
        endpoint_for(view_func, blueprint) for view_func in view_functions
    ]
    return endpoint in allowed_endpoints


# TODO
def dict_merge(*dicts, **options):
    """ 当 key 相同时，后面的 dict 覆盖前面的 dict
    options: keys & shallow
    """
    keys = options.get('keys')
    shallow = options.get('shallow', True)
    result = {}
    for _dict in dicts:
        d = dict_copy(_dict, keys, shallow)
        result.update(d)
    return result


def dict_copy(d, keys=None, shallow=True):
    if keys is None: # Copy all keys
        return d.copy() if shallow else copy.deepcopy(d)
    return {
        key: (d[key] if shallow else copy.deepcopy(d[key]))
        for key in d if key in keys
    }
