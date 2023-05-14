"""
This module set the different configurations for the application
we will have the base configuration class that contain the common
configurations
we will have subclass configurations that configure development, production and testing environment
"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    This is the base class
    """
    SECTRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS =os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'devtools14347@gmail.com'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """
    subaclass for development configurations
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATA_URL') or 'sqliter:///' + os.path.join(basedir, 'dev_data.sqlite')

class TestingConfig(Config):
    """
    subclass for testing configurations
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'test_data.sqlite')
