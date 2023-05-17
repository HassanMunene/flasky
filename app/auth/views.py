"""
this module import the auth blueprint and defines
the routes associated with authentication using its
routes decorator
for now /login route is added
"""
from flask import render_template
from . import auth

@auth.route('/login')
def login():
    return render_template('auth/login.html')
