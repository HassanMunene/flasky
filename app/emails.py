from flask_mail import Message
from . import mail

def send_email(to, subject, template):
