from flask import render_template, redirect, url_for, request, flash
from . import auth
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User, Role, Permission, Post
from .forms import LoginForm, RegistrationForm, ChangePassword, ResetPassword, EmailReset
from .. import db
from ..emails import send_email

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePassword()
    if form.validate_on_submit():
        user = current_user
        if user.verify_password(form.oldpassword.data):
            user.password = form.newpassword.data
            db.session.add(user)
            db.session.commit()
            flash('Password has been changed successfully')
            return redirect(url_for('main.index'))
    if request.form.get('Click here to reset password'):
        email = form.data.email
        if email is None:
            flash('You need to enter you email to proceed')
    return render_template('auth/change_password.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm your Account', 'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/resend_confirmation')
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your account', 'auth/email/confirm', user=current_user, token=token)
    flash("Confirmation email has been sent.")
    return redirect(url_for('main.index'))


@auth.route('/emailReset', methods=['GET', 'POST'])
def emailReset():
    """
    This is the route that will render
    a form that requires you to enter your
    email or username in case you requested
    a password reset after forgetting your password
    """
    form = EmailReset()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Password', 'auth/email/reset', user=user, token=token)
            flash("Email successfully confirmed check your inbox for the link")
            return redirect(url_for('auth.emailReset'))
        else:
            flash("This email is not recognised")
    return render_template('auth/emailReset.html', form=form)

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPassword()
    form2 = EmailReset()
    user = User()
    dict_data = user.confirm_reset_token(token)
    email1 = dict_data['reset']
    user1 = User.query.filter_by(email=email1).first()
    if user1.email == email1:
        render_template('auth/reset_password.html', form=form)

        if form.validate_on_submit():
            user1.password = form.password.data
            db.session.add(user1)
            db.session.commit()
            flash("Password successfully updated!")
            return redirect(url_for('auth.login'))
    else:
        return render_template('auth/emailReset.html', form=form2)
    return render_template('auth/reset_password.html', form=form)
