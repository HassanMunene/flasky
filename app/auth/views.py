"""
this module import the auth blueprint and defines
the routes associated with authentication using its
routes decorator
for now /login route is added
"""
from flask import render_template, redirect, url_for, request, flash
from . import auth
from flask_login import login_user
from ..models import User
from .forms import LoginForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    logform = LoginForm()
    if from.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password')
    return render_template('auth/login.html', logform=logform)
