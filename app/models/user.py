# -*- coding: utf-8 -*-

import base64

from app import db, bcrypt
from sqlalchemy.orm import validates
from .concerns import ModelBase
from .concerns import CaseInsensitiveString
from .concerns import exception_handler


class User(ModelBase):
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(CaseInsensitiveString(255), unique=True, nullable=False)
    password_digest = db.Column(db.String(255), nullable=False)

    @validates('email')
    def convert_to_lower(self, key, value):
        return value.lower()

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
        password = params['password']
        password_digest = User.generate_password_digest(password)
        user = User(
            name=params['name'],
            email=params['email'],
            password_digest=password_digest,
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
            password = params['password']
            password_digest = User.generate_password_digest(password)
            self.password_digest = password_digest
        db.session.commit()

    def authenticate(self, password):
        password_hash = base64.b64decode(self.password_digest)
        return bcrypt.check_password_hash(password_hash, password)

    @staticmethod
    def generate_password_digest(password):
        password_hash = bcrypt.generate_password_hash(password)
        return base64.b64encode(password_hash).decode()

    def __repr__(self):
        return '<User %r>' % self.name
