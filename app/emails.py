from flask_mail import Message
from . import create_app
from flask import render_template
from . import mail

def send_email(to, subject, template, **kwargs):
    msg = Message('[Flasky]' + subject, sender='devtools14347@outlook.com', recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    mail.send(msg)
