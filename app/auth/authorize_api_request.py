# -*- coding: utf-8 -*-

from app.lib import Message
from app.lib import JsonWebToken
from app.models import User
from app.exceptions import exceptions


class AuthorizeApiRequest:
    def __init__(self, headers):
        self.__headers = headers

    @property
    def user(self):
        decoded_auth_token = self.__decode_auth_token()
        user_id = decoded_auth_token['user_id']
        user = User.query.get(user_id)
        if user is None:
            raise exceptions.InvalidToken(Message.invalid_token)
        return user

    def __decode_auth_token(self):
        if 'Authorization' not in self.__headers:
            raise exceptions.MissingToken(Message.missing_token)
        http_auth_header = self.__headers['Authorization'].split(' ')[-1]
        return JsonWebToken.decode(http_auth_header)
