#!/usr/local/bin/python
# coding: utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from .momentjs import momentjs



app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.login_message = 'Ве молиме прво најавете се!'
lm.session_protection = 'strong'
mail = Mail(app)
app.jinja_env.globals['momentjs'] = momentjs


if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/najdistanmk.log', 'a', 2 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s \n\n [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)


from app import views, models
