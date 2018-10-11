# -*- coding: utf-8 -*-

from app import db
from .concerns import ModelBase


class Item(ModelBase):
    name = db.Column(db.String(255), nullable=False)
    done = db.Column(db.Boolean, nullable=False, default=False)
    todo_id = db.Column(db.Integer, db.ForeignKey('todo.id'), nullable=False)
    todo = db.relationship('Todo', backref=db.backref('items', cascade='all,delete', lazy=True))

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            done=self.done,
            created_at=self.created_at,
            updated_at=self.updated_at,
            todo_id=self.todo_id,
        )

    @staticmethod
    def create(params):
        item = Item(**params)
        db.session.add(item)
        db.session.commit()
        return item

    def destroy(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, params):
        if 'title' in params:
            self.title = params['title']
        if 'done' in params:
            self.done = params['done']
        if 'todo_id' in params:
            self.todo_id = params['todo_id']
        db.session.commit()

    def __repr__(self):
        return '<Item %r>' % self.name
