# -*- coding: utf-8 -*-

from app import db
from .concerns import ModelBase


class Todo(ModelBase):
    title = db.Column(db.String(255), nullable=False)
    created_by = db.Column(db.String(255), nullable=False)

    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #user = db.relationship('User', backref=db.backref('todos', lazy=True))

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            created_by=self.created_by,
            created_at=self.created_at,
            updated_at=self.updated_at,
            items=[item.to_dict() for item in self.items],
            #user_id=self.user_id,
        )

    @staticmethod
    def create(params):
        todo = Todo(**params)
        db.session.add(todo)
        db.session.commit()
        return todo

    def destroy(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, params):
        if 'title' in params:
            self.title = params['title']
        if 'created_by' in params:
            self.created_by = params['created_by']
        db.session.commit()

    def __repr__(self):
        return '<Todo %r>' % self.title
