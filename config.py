"""
We have created a configuration class that sets up a
number of settings we need to get the application running
such as connecting to the database,
setting up the email, creating a secret key
get the absolute path for the directory containing
this file: basedir
"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "you cannot guess my key yoh"
    FLASKY_ADMIN = "awanzihassan@outlook.com"
    FLASKY_MODERATOR = "sultanhamud081@outlook.com"
    MAIL_SERVER = "smtp.office356.com"
    MAIL_PORT = 587
    MAIL_SENDER = "devtools14347@outlook.com"
    MAIL_SUBJECT_PREFIX = "[Flasky]"
    MAIL_USERNAME = "devtools14347@outlook.com"
    MAIL_PASSWORD = "Munene14347"
    MAIL_USE_TLS = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.join(basedir, 'dev_data.sqlite')
    FLASK_DEBUG = True

    @static
    def init_app(app):
        pass

