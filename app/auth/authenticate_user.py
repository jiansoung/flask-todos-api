# -*- coding: utf-8 -*-

from app.models import User
from app.lib import Message
from app.lib import JsonWebToken
from app.controllers import exceptions


class AuthenticateUser:
    def __init__(self, email, password):
        self.__email = email.lower()
        self.__password = password

    @property
    def auth_token(self):
        user = self.__user
        return JsonWebToken.encode({'user_id': user.id})

    @property
    def __user(self):
        q = User.query.filter_by(email = self.__email)
        try:
            user = q.first()
            if user.authenticate(self.__password):
                return user
        except Exception as _:
            pass
        raise exceptions.AuthenticationError(Message.invalid_credentials)
