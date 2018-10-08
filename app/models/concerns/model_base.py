# -*- coding: utf-8 -*-

from app import db
from sqlalchemy.ext.declarative import declared_attr


class ModelBase(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
