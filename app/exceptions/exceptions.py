# -*- coding: utf-8 -*-

from werkzeug import exceptions


class RecordNotFound(exceptions.NotFound):
    pass


class RecordInvalid(exceptions.UnprocessableEntity):
    pass


class MissingToken(exceptions.UnprocessableEntity):
    pass


class InvalidToken(Exception):
    pass


class AuthenticationError(Exception):
    pass
