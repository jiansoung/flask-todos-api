# -*- coding: utf-8 -*-

from werkzeug import exceptions


class RecordNotFound(exceptions.NotFound):
    pass


class RecordInvalid(exceptions.UnprocessableEntity):
    pass


class MissingToken(exceptions.UnprocessableEntity):
    pass


class InvalidToken(exceptions.UnprocessableEntity):
    pass


class AuthenticationError(exceptions.Unauthorized):
    pass
