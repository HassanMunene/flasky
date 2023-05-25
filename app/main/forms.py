from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class NameForm(FlaskForm):
    """
    form class definition
    """
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
    """
    a form that regular user will use
    to fill in his/her information to be
    displayed on the profile page
    """
    name = StringField('Real Name', validators=[Length(1, 64)])
    location = StringField('Location', validators=[Length(1, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')
