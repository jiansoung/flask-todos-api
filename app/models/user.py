# -*- coding: utf-8 -*-

from app import db, bcrypt
from .concerns import ModelBase


class User(ModelBase):
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_digest = db.Column(db.String(255), nullable=False)

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
    def create(params):
        password = params['password']
        password_digest = bcrypt.generate_password_hash(password).decode()
        user = User(
            name=params['name'], 
            email=params['email'], 
            password_digest=password_digest
        )
        db.session.add(user)
        db.session.commit()
        return user

    def destroy(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, params):
        if 'name' in params:
            self.name = params['name']
        if 'email' in params:
            self.email = params['email']
        if 'password' in params:
            password = params['password']
            password_digest = bcrypt.generate_password_hash(password).decode()
            self.password_digest = password_digest
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.name