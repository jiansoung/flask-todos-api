# -*- coding: utf-8 -*-

from flask import Flask

from app import models, controllers
from app.extensions import db, bcrypt, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    controllers.init_app(app)
    return app
