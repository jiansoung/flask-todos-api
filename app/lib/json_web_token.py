# -*- coding: utf-8 -*-

import jwt
import datetime
from app import app
from app.controllers import exceptions


class JsonWebToken:
    SECRET_KEY = app.secret_key

    @staticmethod
    def encode(payload, expiration=None):
        if expiration:
            exp = expiration
        else:
            exp = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        payload['exp'] = exp
        return jwt.encode(payload, JsonWebToken.SECRET_KEY).decode()

    @staticmethod
    def decode(token):
        try:
            return jwt.decode(token, JsonWebToken.SECRET_KEY)
        except Exception as e:
            raise exceptions.InvalidToken(str(e))
