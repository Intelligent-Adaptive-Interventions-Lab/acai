from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ChatForm(FlaskForm):
    message = StringField('Write a message...', validators=[DataRequired()])
    submit = SubmitField('Send Message')
