from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
    """
    form class definition
    """
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')
