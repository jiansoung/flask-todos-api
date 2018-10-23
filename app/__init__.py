# -*- coding: utf-8 -*-

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from app import models
    from app import controllers
    controllers.init_app(app)

    return app
