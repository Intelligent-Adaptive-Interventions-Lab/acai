from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField
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


class SurveyForm(FlaskForm):
    mindful_today = SelectField(
        'Select mindful today', 
        choices=[
            ('none', 'none'), 
            ('once', 'once'), 
            ('a_few_times', 'a_few_times')
        ], 
        validators=[DataRequired()]
    )

    stress = IntegerField('Stress', default=0)

    positive_mindset = IntegerField('Positive Mindset', default=3)

    decentering = IntegerField('Positive Mindset', default=3)

    submit = SubmitField('Next')


class DiaryForm(FlaskForm):
    diary_1 = StringField('What has changed?')

    diary_2 = StringField('How the mindfulness practices influence you?')

    video_name = StringField('Video Name')

    submit = SubmitField('Next')


class PostSurveyForm(FlaskForm):
    stress = IntegerField('Stress', default=0)

    statement_1 = IntegerField('Statement 1', default=3)

    statement_2 = IntegerField('Statement 2', default=3)

    submit = SubmitField('Finish')
