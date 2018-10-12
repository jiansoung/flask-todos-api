# -*- coding: utf-8 -*-

from app.models import User
from app.lib import Message
from app.lib import JsonWebToken
from app.controllers import exceptions


class AuthenticateUser:
    def __init__(self, email, password):
        self.__email = email
        self.__password = password

    @property
    def auth_token(self):
        user = self.__user
        return JsonWebToken.encode({'user_id': user.id})

    @property
    def __user(self):
        user = User.query.filter_by(email=self.__email).first()
        if user and user.authenticate(self.__password):
            return user
        raise exceptions.AuthenticationError(Message.invalid_credentials)
