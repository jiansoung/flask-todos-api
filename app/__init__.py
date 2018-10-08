# -*- coding: utf-8 -*-

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile("config.py")
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from app import models
from app import controllers
