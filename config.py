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
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_DEFAULT_SENDER = "devtools14347@outlook.com"
    MAIL_SERVER = "smtp.office365.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_DEBUG = False
    MAIL_USERNAME = "devtools14347@outlook.com"
    MAIL_PASSWORD = "Munene14347"
    FLASKY_ADMIN = "devtools14347@outlook.com"
    FLASKY_MODERATOR = "devtools214347@outlook.com"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """
    subaclass for development configurations
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'dev_data.sqlite')

class TestingConfig(Config):
    """
    subclass for testing configurations
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'test_data.sqlite')

class ProductionConfig(Config):
    """
    subclass for production configurations
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
        'default': DevelopmentConfig
        }

