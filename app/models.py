from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class Role(db.Model):
    """
    class model for roles table
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        """
        returns string rep of the object
        mainly for debugging and testing
        """
        return '<Role %r>' % self.name

class User(db.Model):
    """
    class model for the users table
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """
        returns the string rep of the object
        """
        return '<User %r>' % self.username
