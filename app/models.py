from itsdangerous import URLSafeTimedSerializer as Serializer
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager
from flask import current_app, request
import hashlib
from datetime import datetime

class Role(db.Model):
    """
    class model for roles table
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0
    """
    ----------------------------------------------------------------------------------------------------
    The function will be used to manipulate the permissions field of the role
    ----------------------------------------------------------------------------------------------------
    """
    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permission(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm
    """
    ---------------------------------------------------------------------------------------------------
    ---------------------------------------------------------------------------------------------------
    """


    """
    ------------------------------------------------------------------------------------------------
    This is a class method that will be used to add the permission to the different users in the database
    so instead of adding the users manually ou do them automatically
    """
    @staticmethod
    def insert_roles():
        roles = {
                'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
                'Moderator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE],
                'Administrator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE, Permission.ADMIN]
                }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()
    """
    -----------------------------------------------------------------------------------------------------------
    ----------------------------------------------------------------------------------------------------------
    """

    def __repr__(self):
        """
        returns string rep of the object
        mainly for debugging and testing
        """
        return '<Role %r>' % self.name


class Permission:
    """
    A mapping of specific tasks with
    their permission values
    """
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16

class User(UserMixin, db.Model):
    """
    class model for the users table
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            elif self.email == current_app.config['FLASKY_MODERATOR']:
                self.role = Role.query.filter_by(name='Moderator').first()
            else:
                self.role = Role.query.filter_by(name='User').first()

    """
    -------------------------------------------------------------------------------------------------
    set the password hash and store it in the password_hash field
    confirm the password hash against the password provided by user
    define a getter method that denies access
    ------------------------------------------------------------------------------------------------
    """
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    """
    -----------------------------------------------------------------------------------------------
    -----------------------------------------------------------------------------------------------
    """

    def ping(self):
        """
        refresh user's last time visit
        everytime the user visits the app
        """
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    """
    ------------------------------------------------------------------------------------------
    generate token to confirm the user's account by sending an email to the user's email
    ------------------------------------------------------------------------------------------
    """
    def generate_confirmation_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True
    """
    -------------------------------------------------------------------------------------------
    -------------------------------------------------------------------------------------------
    """

    def generate_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'reset': self.email})

    def confirm_reset_token(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        return data


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def __repr__(self):
        """
        returns the string rep of the object
        """
        return '<User %r>' % self.username
    
    def change_email(self, token):
        self.email = new_email
        self.avatar_hash = self.garavat_hash()
        db.session.add(self)
        return True

class AnonymousUser(AnonymousUserMixin):
    """
    this custome class is added so as to implement the can() and is_administrator()
    methods. It will enable the application to to freely call current_user.can()
    or current_user.is_administrator() without checking if user is logged in or not
    """
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

class Post(db.Model):
    """
    The blueprint of what a post instance
    will entail
    """
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
