from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class ChatForm(FlaskForm):
    message = StringField('Write a message...', validators=[DataRequired()])
    submit = SubmitField('Send Message')


class BotToBotChatForm(FlaskForm):
    bot_prompt = TextAreaField(
        'Prompt', 
        default="The following is a conversation with a Psychoanalytic Coach. The Psychoanalytic Coach facilitates awareness of unconscious motivations, thereby increasing choice. The Psychoanalytic Coach explores the ways in which the human avoids painful or threatening feelings, fantasies, and thoughts. The assistant is helpful, creative, clever, and very friendly. The Psychoanalytic Coach makes empathic reflections and interpretations to make the human more aware of unconscious experiences and relational patterns. The Psychoanalytic Coach pays attention to the therapeutic relationship, including transference and countertransference.", 
        validators=[DataRequired()]
    )

    user_prompt = TextAreaField(
        'Prompt', 
        default="The following is a conversation with a person suffering from anxiety. The person is seeking help to manage their thoughts and emotions.", 
        validators=[DataRequired()]
    )

    turn = SelectField(
        'Select conversation turn', 
        choices=[
            ('Bot', 'Bot'), 
            ('User', 'User')
        ], 
        validators=[DataRequired()]
    )

    message = StringField('Write a message...')

    submit = SubmitField('Send Message')