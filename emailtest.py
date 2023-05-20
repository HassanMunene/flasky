from flask import Flask, render_template
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['SECRET_KEY'] = "veryhard"
app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_PASSWORD'] = 'Munene14347'
app.config['MAIL_USERNAME'] = 'devtools14347@outlook.com'

mail = Mail(app)

@app.route("/", methods=['GET'])
def index():
    return "index"


@app.route("/send_email")
def send_email():
    msg = Message('Hello there dude', sender='devtools14347@outlook.com', recipients=['awanzihassan@gmail.com'])
    msg_body = "This is the email body"
    mail.send(msg)
    return 'Email sent'

if __name__ == "__main__":
    app.run(debug=True)
