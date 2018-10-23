# -*- coding: utf-8 -*-

import base64

from sqlalchemy.orm import validates

from app.extensions import db, bcrypt
from .concerns import ModelBase
from .concerns import CaseInsensitiveString
from app.models import Todo
from app.exceptions import exception_handler


class User(ModelBase):
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(CaseInsensitiveString(255), unique=True, nullable=False)
    password_digest = db.Column(db.String(255), nullable=False)

    @validates('email')
    def convert_to_lower(self, key, value):
        return value.lower()

    @validates('password_digest')
    def convert_to_password_digest(self, key, value):
        password_hash = bcrypt.generate_password_hash(value)
        return base64.b64encode(password_hash).decode()

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            email=self.email,
            password_digest=self.password_digest,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @staticmethod
    @exception_handler.sqlalchemy_error_handler
    def create(params):
        user = User(
            name=params['name'],
            email=params['email'],
            password_digest=params['password'],
        )
        db.session.add(user)
        db.session.commit()
        return user

    def destroy(self):
        db.session.delete(self)
        db.session.commit()

    @exception_handler.sqlalchemy_error_handler
    def update(self, params):
        if 'name' in params:
            self.name = params['name']
        if 'email' in params:
            self.email = params['email']
        if 'password' in params:
            self.password_digest = params['password']
        db.session.commit()

    def authenticate(self, password):
        password_hash = base64.b64decode(self.password_digest)
        return bcrypt.check_password_hash(password_hash, password)

    def create_todo(self, todo_params):
        todo = Todo(**todo_params)
        self.todos.append(todo)
        db.session.commit()
        return todo

    def __repr__(self):
        return '<User %r>' % self.name
