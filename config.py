import os
"""
get the absolute path for the directory containing
this file: basedir
"""
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    FLASKY_ADMIN = "awanzihassan@outlook.com"
    FLASKY_MODERATOR = "sultanhamud081@outlook.com"
    MAIL_SERVER = "smtp.office356.com"
    MAIL_PORT = 587
    MAIL_SENDER = "devtools14347@outlook.com"
    MAIL_SUBJECT_PREFIX = "[Flasky]"
    MAIL_USERNAME = "devtools14347@outlook.com"
    MAIL_PASSWORD = "Munene14347"
    MAIL_USE_TLS = True
