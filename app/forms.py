from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired


class ChatForm(FlaskForm):
    message = StringField('Write a message...', validators=[DataRequired()])
    submit = SubmitField('Send Message')


class BotToBotChatForm(FlaskForm):
    bot_prompt = TextAreaField(
        'Prompt', 
        default="You are a friend, aiming to promote well-being, guided by the Theory of Planned Behavior, which suggests that an individual's behavior is directly influenced by their intention, shaped by their attitudes towards the behavior, the subjective norms surrounding it, and their perceived control over the behavior. Your approach involves providing emotional through a direct, while maintaining a positive tone throughout the interaction.", 
        validators=[DataRequired()]
    )

    user_prompt = TextAreaField(
        'Prompt', 
        default="You are a student who feels generally positive about life. Recently, you've been managing your academic and personal responsibilities well, feeling confident in your ability to handle challenges. You seek to maintain or slightly improve your current state of well-being. During a conversation with a well-being improvement agent, you express interest in strategies that could further enhance your productivity and overall happiness without indicating any significant distress or issues.", 
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

    stress = IntegerField('Stress', default=5)

    positive_mindset = IntegerField('Positive Mindset', default=3)

    decentering = IntegerField('Positive Mindset', default=3)

    submit = SubmitField('Next')


class DiaryForm(FlaskForm):
    diary_1 = StringField('What has changed?')

    diary_2 = StringField('How the mindfulness practices influence you?')

    video_name = StringField('Video Name')

    submit = SubmitField('Next')


class PostSurveyForm(FlaskForm):
    stress = IntegerField('Stress', default=5)

    statement_1 = IntegerField('Statement 1', default=3)

    statement_2 = IntegerField('Statement 2', default=3)

    submit = SubmitField('Finish')
