from app import app
from app.forms import (
    ChatForm, 
    BotToBotChatForm, 
    SurveyForm,
    DiaryForm,
    PostSurveyForm
)
from app.conversation import (
    AutoScriptConversation,
    CustomGPTConversation,
    GPTConversation,
    init_prompt,
    init_reflection_bot,
    init_information_bot,
    init_mindy
)
from app.utils import print_first_50_words
from app.video import init_video_for_mindfulness
from app.database import (
    add_new_chat_log,
    track_link_click,
    add_new_user_to_diary_study,
    update_pre_survey,
    udpate_diary,
    update_reflect_chat,
    update_reflect,
    update_post_survey,
    get_diary_answers_from_latest_user_id
)
from flask import (
    Flask,
    request,
    session,
    jsonify,
    render_template, 
    redirect,
    url_for,
    abort,
    Response
)

from datetime import datetime, timezone

# run_with_ngrok(app)

def _delete_session_variable(variable: str) -> None:
    try:
        del session[variable]
    except KeyError:
        pass


@app.route('/index')
def index():
    return render_template("/quiz/main.html")


@app.route('/quiz_content')
def quiz_content():
    return render_template("/quiz/content.html")


@app.route('/')
def main():
    return render_template("/pages/main.html")


@app.route('/motivational_interview', methods=['GET', 'POST'])
def motivational_interview_conversation():
    chat_log = session.get('motivational_interview_chat_log', None)
    dialogue_id = session.get('motivational_interview_dialogue_id', None)
    dialogue_answers = session.get('motivational_interview_dialogue_answers',
                                   {})

    convo = AutoScriptConversation(
        user="Human",
        chatbot="Alex",
        dialogue_path="motivational_interview",
        dialogue_answers=dialogue_answers
    )

    dialogue_id, chat_log = convo.sync_chat_log(chat_log=chat_log,
                                                dialogue_id=dialogue_id)
    session["motivational_interview_chat_log"] = chat_log
    session["motivational_interview_dialogue_id"] = dialogue_id

    form = ChatForm()
    if form.validate_on_submit():
        message = form.message.data
        dialogue_answers[dialogue_id] = message
        session["motivational_interview_dialogue_answers"] = dialogue_answers

        dialogue_id, chat_log = convo.give_answer(answer=message)
        session["motivational_interview_chat_log"] = chat_log
        session["motivational_interview_dialogue_id"] = dialogue_id

        return render_template(
            '/pages/convo_motivational_interview.html',
            user=convo.get_user(),
            bot=convo.get_chatbot(),
            warning=convo.WARNING,
            end=convo.END,
            notification=convo.NOTI,
            conversation=convo.get_conversation(),
            form=form
         )

    return render_template(
        '/pages/convo_motivational_interview.html',
        user=convo.get_user(),
        bot=convo.get_chatbot(),
        warning=convo.WARNING,
        end=convo.END,
        notification=convo.NOTI,
        conversation=convo.get_conversation(),
        form=form
    )


@app.route('/mindfulness_conversation', methods=['GET', 'POST'])
def mindfulness_conversation():
    chat_log = session.get('mindfulness_chat_log', None)
    dialogue_id = session.get('mindfulness_dialogue_id', None)
    dialogue_answers = session.get('mindfulness_dialogue_answers', {})

    convo = AutoScriptConversation(
        user="HUMAN",
        chatbot="AI",
        dialogue_path="mindfulness",
        dialogue_answers=dialogue_answers
    )

    dialogue_id, chat_log = convo.sync_chat_log(chat_log=chat_log,
                                                dialogue_id=dialogue_id)
    session["mindfulness_chat_log"] = chat_log
    session["mindfulness_dialogue_id"] = dialogue_id

    form = ChatForm()
    if form.validate_on_submit():
        message = form.message.data
        dialogue_answers[dialogue_id] = message
        session["mindfulness_dialogue_answers"] = dialogue_answers

        dialogue_id, chat_log = convo.give_answer(answer=message)
        session["mindfulness_chat_log"] = chat_log
        session["mindfulness_dialogue_id"] = dialogue_id

        return render_template(
            '/pages/combined.html',
            user=convo.get_user(),
            bot=convo.get_chatbot(),
            warning=convo.WARNING,
            end=convo.END,
            notification=convo.NOTI,
            conversation=convo.get_conversation(),
            form=form
        )

    return render_template(
        '/pages/combined.html',
        user=convo.get_user(),
        bot=convo.get_chatbot(),
        warning=convo.WARNING,
        end=convo.END,
        notification=convo.NOTI,
        conversation=convo.get_conversation(),
        form=form
    )

@app.route('/bot_to_bot/download/bot')
def download_bot_chat_log():
    form = BotToBotChatForm(turn="User")
    
    # Extract data from form
    chat_log = session.get('bot_chat_log', form.bot_prompt.data)
    
    return Response(
        chat_log,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment;filename=bot_a_chat_log.txt"}
    )

@app.route('/bot_to_bot/download/user')
def download_user_chat_log():
    form = BotToBotChatForm(turn="Bot")
    
    # Extract data from form
    chat_log = session.get('user_chat_log', form.user_prompt.data)
    
    return Response(
        chat_log,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment;filename=bot_b_chat_log.txt"}
    )

@app.route('/bot_to_bot/clear')
def bot_to_bot_refresh():
    delete_variables = [
        'bot_chat_log',
        'user_chat_log'
    ]
    for variable in delete_variables:
        _delete_session_variable(variable)
    
    return redirect(url_for('bot_to_bot'))


@app.route('/bot_to_bot', methods=['GET', 'POST'])
def bot_to_bot():
    form = BotToBotChatForm(turn="User")

    bot = CustomGPTConversation(
        user="HUMAN",
        chatbot="AI",
        chat_log=session.get('bot_chat_log', form.bot_prompt.data),
        prompt=form.bot_prompt.data,
        default_start="I am an AI agent designed to improve your well-being. How are you doing today?"
    )
    bot.prompt = bot.get_prompt()

    user = CustomGPTConversation(
        user="HUMAN",
        chatbot="AI",
        chat_log=session.get('user_chat_log', form.user_prompt.data),
        prompt=form.user_prompt.data,
        default_start="Hello, who are you?"
    )
    user.prompt = user.get_prompt()

    if form.validate_on_submit():
        print("============== START ==============")
        message = form.message.data
        turn = form.turn.data

        print(f'turn: {turn}')

        if message == '':
            last_question = bot.get_last_message() if turn == 'User' else user.get_last_message()

            if last_question == '':
                answer = user.default_start if turn == 'User' else bot.default_start
            else:
                answer = user.ask() if turn == 'User' else bot.ask()

            bot_chat_log = bot.append_interaction_to_chat_log(answer=answer) if turn == 'User' else bot.append_interaction_to_chat_log(question=answer)
            user_chat_log = user.append_interaction_to_chat_log(question=answer) if turn == 'User' else user.append_interaction_to_chat_log(answer=answer)
            form.turn.default = 'Bot' if turn == 'User' else 'User'
        else:
            answer = user.ask(question=message) if turn == 'User' else bot.ask(question=message)
            
            if turn == 'User':
                user.append_interaction_to_chat_log(answer=message)
                user_chat_log = user.append_interaction_to_chat_log(question=answer)
                bot_chat_log = bot.append_interaction_to_chat_log(question=message, answer=answer)
            else:
                bot.append_interaction_to_chat_log(answer=message)
                bot_chat_log = bot.append_interaction_to_chat_log(question=answer)
                user_chat_log = user.append_interaction_to_chat_log(question=message, answer=answer)

        # # Check current turn of the conversation
        # if turn == 'User':
        #     # USER turn
        #     # Check if providing message manually
        #     if message != '':
        #         # [USER] Add answer (self) message to chat log
        #         user.append_interaction_to_chat_log(answer=message)

        #         # [BOT] Generate message to chat log
        #         answer = bot.ask(question=message)

        #         # [BOT] Add message back to chat log
        #         bot_chat_log = bot.append_interaction_to_chat_log(
        #             question=message, answer=answer)

        #         # [USER] Add question (opposite) message to chat log
        #         user_chat_log = user.append_interaction_to_chat_log(
        #             question=answer)

        #         # print(f'user_chat_log: {user_chat_log}')
        #         # print(f'bot_chat_log: {bot_chat_log}')

        #         form.turn.default = 'User'
        #     else:
        #         # [USER] Get last message for question
        #         question = user.get_last_message()

        #         print('[USER] Get last message for question')
        #         print_first_50_words(question)

        #         if question == '':
        #             # [USER] If no starting message is given, use the default start
        #             answer = user.default_start
        #         else:
        #             # [USER] Ask to get answer
        #             answer = user.ask()

        #         # [BOT] Add question (opposite) message to chat log
        #         bot_chat_log = bot.append_interaction_to_chat_log(
        #             question=answer)

        #         # [USER] Add answer (self) message to chat log
        #         user_chat_log = user.append_interaction_to_chat_log(
        #             answer=answer)

        #         # print(f'user_chat_log: {user_chat_log}')
        #         # print(f'bot_chat_log: {bot_chat_log}')

        #         form.turn.default = 'Bot'
        # else:
        #     # BOT turn
        #     # Check if providing message manually
        #     if message != '':
        #         # [BOT] Add answer (self) message to chat log
        #         bot.append_interaction_to_chat_log(answer=message)

        #         # [USER] Generate message to chat log
        #         answer = user.ask(question=message)

        #         # [USER] Add message back to chat log
        #         user_chat_log = user.append_interaction_to_chat_log(
        #             question=message, answer=answer)

        #         # [BOT] Add question (opposite) message to chat log
        #         bot_chat_log = bot.append_interaction_to_chat_log(
        #             question=answer)

        #         # print(f'user_chat_log: {user_chat_log}')
        #         # print(f'bot_chat_log: {bot_chat_log}')

        #         form.turn.default = 'Bot'
        #     else:
        #         # [BOT] Get last message for question
        #         question = bot.get_last_message()

        #         print('[BOT] Get last message for question')
        #         print_first_50_words(question)

        #         if question == '':
        #             # [BOT] If no starting message is given, use the default start
        #             answer = bot.default_start
        #         else:
        #             # [BOT] Ask to get answer
        #             answer = bot.ask()

        #         # [USER] Add question (opposite) message to chat log
        #         user_chat_log = user.append_interaction_to_chat_log(
        #             question=answer)

        #         # [BOT] Add answer (self) message to chat log
        #         bot_chat_log = bot.append_interaction_to_chat_log(answer=answer)

        #         # print(f'user_chat_log: {user_chat_log}')
        #         # print(f'bot_chat_log: {bot_chat_log}')

        #         form.turn.default = 'User'

        # Sync both USER and BOT chat logs
        user.sync_chat_log(user_chat_log)
        bot.sync_chat_log(bot_chat_log)

        # Update Session
        session['user_chat_log'] = user_chat_log
        session['bot_chat_log'] = bot_chat_log
        form.process()

        add_new_chat_log("BTB - {}".format(user.get_user()), user_chat_log)

        print("============== END ==============")
        # Render conversation from BOT
        return render_template(
            "/pages/bot_to_bot.html",
            user=user.get_user(),
            bot=user.get_chatbot(),
            warning=user.WARNING,
            end=user.END,
            notification=user.NOTI,
            conversation=user.get_conversation(test=False),
            form=form
        )
    else:
        form.bot_prompt.default = bot.get_prompt()
        form.user_prompt.default = user.get_prompt()
        form.turn.default = 'User'
        form.process()

    return render_template(
        "/pages/bot_to_bot.html",
        user=user.get_user(),
        bot=user.get_chatbot(),
        warning=user.WARNING,
        end=user.END,
        notification=user.NOTI,
        conversation=user.get_conversation(test=False),
        form=form
    )


@app.route('/conversation', methods=['GET', 'POST'])
def start_conversation():
    chat_log = session.get('chat_log')

    if chat_log is None:
        arm_no = session.get("arm_no")
        if arm_no is None:
            select_prompt = init_prompt(random=True)
        else:
            select_prompt = init_prompt(arm_no=arm_no)
        session["chat_log"] = select_prompt["prompt"] + select_prompt[
            "message_start"]
        session["chatbot"] = select_prompt["chatbot"]
        session["user"] = request.remote_addr
        session["start"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    convo = GPTConversation(
        session.get("user"), 
        session.get("chatbot"),
        session.get("chat_log"),
        bot_start="Hello. I am an AI agent designed to help you solve math questions. How can I help you?"
    )

    form = ChatForm()
    if form.validate_on_submit():
        user_message = form.message.data
        answer = convo.ask(user_message)
        chat_log = convo.append_interaction_to_chat_log(user_message, answer)
        session["chat_log"] = chat_log
        
        add_new_chat_log(session["user"], session["chat_log"])

        return redirect(url_for('start_conversation'))

    return render_template(
        '/pages/convo.html',
        user=convo.get_user(),
        bot=convo.get_chatbot(),
        warning=convo.WARNING,
        end=convo.END,
        notification=convo.NOTI,
        conversation=convo.get_conversation(test=True),
        form=form
    )
    


@app.route('/qualtrics', methods=['GET', 'POST'])
def start_qualtrics_conversation():
    chat_log = session.get('chat_log')
    if chat_log is None:
        arm_no = session.get("arm_no")
        if arm_no is None:
            select_prompt = init_prompt(random=True)
        else:
            select_prompt = init_prompt(arm_no=arm_no)
        session["chat_log"] = select_prompt["prompt"] + select_prompt[
            "message_start"]
        session["chatbot"] = select_prompt["chatbot"]
        session["user"] = request.remote_addr
        session["start"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    convo = GPTConversation(
        session.get("user"), 
        session.get("chatbot"),
        session.get("chat_log"),
        bot_start="Hello. I am an AI agent designed to help you solve math questions. How can I help you?"
    )

    start = session.get('start')
    if start is None:
        session["start"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    stop = session.get('stop')
    if stop is None:
        session["stop"] = 5 * 60

    now = datetime.now()
    difference = now - datetime.strptime(session.get('start'),
                                         "%m/%d/%Y, %H:%M:%S")
    difference_seconds = difference.total_seconds()

    end = session.get('end')
    if end is None or not end:
        session["end"] = (difference_seconds >= session.get('stop'))

    session["end"] = False
    form = ChatForm()
    if form.validate_on_submit() and not session.get('end'):
        user_message = form.message.data
        answer = convo.ask(user_message)
        chat_log = convo.append_interaction_to_chat_log(user_message, answer)

        session['chat_log'] = chat_log

        add_new_chat_log(session["user"], session["chat_log"])

        return redirect(url_for('start_qualtrics_conversation'))

    return render_template(
        '/dialogue/qualtrics_card.html',
        user=convo.get_user(),
        bot=convo.get_chatbot(),
        warning=convo.WARNING,
        end=convo.END,
        notification=convo.NOTI,
        conversation=convo.get_conversation(end=session.get('end')),
        form=form
    )


@app.route('/clear', methods=['GET'])
def clear_session():
    delete_variables = [
        'chat_log',
        'start',
        'end',
        'arm_no',
        'bot_chat_log',
        'user_chat_log',
        'mindfulness_chat_log',
        'mindfulness_dialogue_id',
        'mindfulness_dialogue_answers',
        'motivational_interview_chat_log',
        'motivational_interview_id',
        'motivational_interview_answers',
        'info_bot',
        'reflection_bot',
        'mindy',
        'reflect_diary',
        'user'
    ]
    for variable in delete_variables:
        _delete_session_variable(variable)

    return "cleared!"


@app.route('/end', methods=['GET'])
def end():
    session['end'] = True
    return "ended!"


@app.route('/arm', methods=['GET'])
def select_arm():
    args = request.args
    location = int(args['location'])
    if location == 12345:
        arm_no = 0
    elif location == 23456:
        arm_no = 1
    elif location == 34567:
        arm_no = 2
    elif location == 45678:
        arm_no = 3
    elif location == 56789:
        arm_no = 4
    elif location == 67891:
        arm_no = 5
    elif location == 78910:
        arm_no = 6
    elif location == 89101:
        arm_no = 7
    elif location == 91011:
        arm_no = 8
    elif location == 10111:
        arm_no = 9
    elif location == 11121:
        arm_no = 10
    elif location == 12131:
        arm_no = 11
    elif location == 13141:
        arm_no = 12
    elif location == 14151:
        arm_no = 13
    elif location == 15161:
        arm_no = 14
    elif location == 16171:
        arm_no = 15
    elif location == 17181:
        arm_no = 16
    elif location == 18192:
        arm_no = 16
    session['arm_no'] = arm_no
    return redirect(url_for('start_qualtrics_conversation'))


@app.route('/qualtrics_specific', methods=['GET'])
def start_coversation_without_arm():
    pass


@app.route('/info_bot', methods=['GET', 'POST'])
def info_bot():
    info_bot = session.get("info_bot", None)
    if not info_bot:
        select_prompt = init_information_bot()
        info_bot = {
            "chat_log": select_prompt["prompt"] + select_prompt[
                "message_start"],
            "convo_start": select_prompt["message_start"],
            "bot_start": "Hello. I am an AI agent designed to act as your Mindfulness instructor. I can answer any questions you might have related to Mindfulness. How can I help you?",
            "chatbot": select_prompt["chatbot"],
            "user": request.remote_addr,
            "start": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        }

    convo = GPTConversation(
        user=info_bot.get("user"),
        chatbot=info_bot.get("chatbot"),
        chat_log=info_bot.get("chat_log"),
        bot_start=info_bot.get("bot_start"),
        convo_start=info_bot.get("convo_start")
    )

    start = info_bot.get('start')
    if start is None:
        info_bot["start"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    stop = info_bot.get('stop')
    if stop is None:
        info_bot["stop"] = 5 * 60

    now = datetime.now()
    difference = now - datetime.strptime(info_bot.get('start'),
                                         "%m/%d/%Y, %H:%M:%S")
    difference_seconds = difference.total_seconds()

    end = info_bot.get('end')
    if end is None or not end:
        info_bot["end"] = (difference_seconds >= info_bot.get('stop'))

    form = ChatForm()
    if form.validate_on_submit() and not info_bot.get('end'):
        user_message = form.message.data
        answer = convo.ask(user_message)
        chat_log = convo.append_interaction_to_chat_log(user_message, answer)

        info_bot['chat_log'] = chat_log

        add_new_chat_log(info_bot["user"], info_bot["chat_log"])

        session["info_bot"] = info_bot
        return redirect(url_for('info_bot'))

    session["info_bot"] = info_bot
    return render_template(
        '/dialogue/qualtrics_card.html',
        user=convo.get_user(),
        bot=convo.get_chatbot(),
        warning=convo.WARNING,
        end=convo.END,
        notification=convo.NOTI,
        conversation=convo.get_conversation(end=info_bot.get('end')),
        form=form
    )

@app.route('/full_chat/<user_id>', defaults={'show_bot_avatar': None}, methods=['GET', 'POST'])
@app.route('/full_chat/<user_id>/<show_bot_avatar>', methods=['GET', 'POST'])
def full_chat_window(user_id, show_bot_avatar):
    session["user"] = user_id
    chat_log = session.get('chat_log')
    if chat_log is None:
        arm_no = session.get("arm_no")
        if arm_no is None:
            select_prompt = init_prompt(random=True)
        else:
            select_prompt = init_prompt(arm_no=arm_no)
        session["chat_log"] = select_prompt["prompt"] + select_prompt[
            "message_start"]
        session["chatbot"] = select_prompt["chatbot"]

    convo = GPTConversation(
        session.get("user"), 
        session.get("chatbot"),
        session.get("chat_log"),
        bot_start="Hello. I am an AI agent designed to help you solve math questions. How can I help you?"
    )

    form = ChatForm()
    if form.validate_on_submit() and not session.get('end'):
        user_message = form.message.data
        answer = convo.ask(user_message)
        chat_log = convo.append_interaction_to_chat_log(user_message, answer)

        session['chat_log'] = chat_log

        add_new_chat_log(session["user"], session["chat_log"])

        return redirect(url_for('full_chat_window', user_id=user_id, show_bot_avatar=show_bot_avatar))

    return render_template(
        '/dialogue/qualtrics_card.html',
        user=convo.get_user(),
        bot=convo.get_chatbot(),
        show_bot_avatar=show_bot_avatar is not None,
        warning=convo.WARNING,
        end=convo.END,
        notification=convo.NOTI,
        conversation=convo.get_conversation(end=session.get('end')),
        form=form
    )


@app.route('/survey/<user_id>', methods=['GET', 'POST'])
def survey(user_id):
    
    session["user"] = user_id

    form = SurveyForm()
    if form.validate_on_submit():
        presurvey_1 = form.mindful_today.data
        presurvey_2 = form.stress.data
        presurvey_3 = form.positive_mindset.data
        presurvey_4 = form.decentering.data
        print("SURVEY FORM IS SUBMITTED!!!")
        print(f"presurvey 1: {presurvey_1}\npresurvey 2: {presurvey_2}\npresurvey 3: {presurvey_3}\npresurvey 4: {presurvey_4}")

        update_pre_survey(
            user_id=user_id, 
            pre_mindful=presurvey_1, 
            pre_stress=presurvey_2,
            pre_aware=presurvey_3,
            pre_perspective=presurvey_4,
            pre_survey_click_ts=datetime.now()
        )

        return redirect(url_for('video_diary', user_id=user_id))
    
    track_link_click(user_id=user_id, timestamp=datetime.now())
    add_new_user_to_diary_study(user_id=user_id, session_start_ts=datetime.now())
    
    delete_variables = [
        'reflect_diary'
    ]
    for variable in delete_variables:
        _delete_session_variable(variable)

    return render_template(
        "/pages/survey.html",
        form=form
    )


@app.route('/video_diary/<user_id>', methods=['GET', 'POST'])
def video_diary(user_id):
    
    session["user"] = user_id
    video_url = init_video_for_mindfulness()

    form = DiaryForm()
    if form.validate_on_submit():
        diary_1 = form.diary_1.data
        diary_2 = form.diary_2.data
        video_name = form.video_name.data
        print("VIDEO DIARY FORM IS SUBMITTED!!!")
        print(f"diary 1: {diary_1}\ndiary 2: {diary_2}")
        print(f"video_name: {video_name}")

        udpate_diary(
            user_id=user_id, 
            diary_1=str(diary_1), 
            diary_2=str(diary_2), 
            video_name=str(video_name), 
            main_interface_click_ts_1=datetime.now()
        )

        if int(user_id) % 2 == 0:
            return redirect(url_for('reflect_diary', user_id=user_id))
        else:
            return redirect(url_for('post_survey', user_id=user_id))

    return render_template(
        "/pages/video_diary.html", 
        video_url=video_url, 
        form=form
    )


@app.route('/post_survey/<user_id>', methods=['GET', 'POST'])
def post_survey(user_id):
    
    session["user"] = user_id
    form = PostSurveyForm()
    if form.validate_on_submit():
        stress = form.stress.data
        statement_1 = form.statement_1.data
        statement_2 = form.statement_2.data
        print("POST SURVEY FORM IS SUBMITTED!!!")
        print(f"stress: {stress}\nstatement 1: {statement_1}\nstatement 2: {statement_2}")

        update_post_survey(
            user_id=user_id, 
            post_stress=stress, 
            post_aware=statement_1, 
            post_mindful=statement_2, 
            post_survey_click_ts=datetime.now()
        )

        return redirect(url_for('end_survey', user_id=user_id))

    return render_template(
        "/pages/post_survey.html", 
        form=form
    )


@app.route('/reflect_diary/<user_id>', methods=['GET', 'POST'])
def reflect_diary(user_id):
    
    session["user"] = user_id
    reflect_diary = session.get("reflect_diary", None)
    start_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    if not reflect_diary:
        reflect_diary = {
            "start": start_time
        }
        session['reflect_diary'] = reflect_diary

    start = session['reflect_diary'].get('start')
    if start is None:
        session['reflect_diary']["start"] = start_time

    print(f"start time: {session['reflect_diary'].get('start')}")

    form = DiaryForm()
    if form.validate_on_submit():
        diary_1 = form.diary_1.data
        diary_2 = form.diary_2.data
        print("VIDEO DIARY FORM IS SUBMITTED!!!")
        print(f"diary 1: {diary_1}\ndiary 2: {diary_2}")

        update_reflect(
            user_id=user_id, 
            diary_1=diary_1, 
            diary_2=diary_2, 
            main_interface_click_ts_2=datetime.now()
        )

        return redirect(url_for('post_survey', user_id=user_id))
    
    diary_1, diary_2 = get_diary_answers_from_latest_user_id(user_id)
    form.diary_1.default = diary_1 if diary_1 is not None else ''
    form.diary_2.default = diary_2 if diary_2 is not None else ''
    form.process()
    
    return render_template(
        "/pages/reflect_diary.html", 
        convo_start=session['reflect_diary'].get('start'),
        user_id=user_id,
        form=form
    )


@app.route('/reflect_bot/<user_id>/<convo_end>', defaults={'show_bot_avatar': None}, methods=['GET', 'POST'])
@app.route('/reflect_bot/<user_id>/<show_bot_avatar>/<convo_end>', methods=['GET', 'POST'])
def reflect_bot(user_id, convo_end, show_bot_avatar):
    
    end = bool(int(convo_end))
    session["user"] = user_id
    reflection_bot = session.get("reflection_bot", None)
    if not reflection_bot:
        select_prompt = init_reflection_bot()
        reflection_bot = {
            "chat_log": select_prompt["prompt"] + select_prompt[
                "message_start"],
            "convo_start": select_prompt["message_start"],
            "bot_start": 'The following bot is designed to help you reflect on your understanding of the mindfulness video. You can start by prompting "Can you help me reflect on my understanding of mindfulness?"',
            "chatbot": select_prompt["chatbot"],
            "user": user_id,
        }
    else:
        reflection_bot["user"] = user_id

    convo = GPTConversation(
        user=reflection_bot.get("user"),
        chatbot=reflection_bot.get("chatbot"),
        chat_log=reflection_bot.get("chat_log"),
        bot_start=reflection_bot.get("bot_start"),
        convo_start=reflection_bot.get("convo_start")
    )

    form = ChatForm()
    if form.validate_on_submit() and not end:
        user_message = form.message.data
        answer = convo.ask(user_message)
        chat_log = convo.append_interaction_to_chat_log(user_message, answer)

        reflection_bot['chat_log'] = chat_log

        add_new_chat_log(reflection_bot["user"], reflection_bot["chat_log"])
        update_reflect_chat(user_id=user_id, reflect_chatlog=chat_log)

        session["reflection_bot"] = reflection_bot
        return redirect(url_for('reflect_bot', user_id=user_id, convo_end=1 if end else 0))

    session["reflection_bot"] = reflection_bot
    return render_template(
        '/dialogue/qualtrics_card.html',
        user=convo.get_user(),
        bot=convo.get_chatbot(),
        show_bot_avatar=show_bot_avatar is not None,
        warning=convo.WARNING,
        end=convo.END,
        notification=convo.NOTI,
        conversation=convo.get_conversation(end=end),
        form=form
    )


@app.route('/end_survey/<user_id>', methods=['GET', 'POST'])
def end_survey(user_id):
    
    session["user"] = user_id

    delete_variables = [
        'chat_log',
        'start',
        'end',
        'arm_no',
        'bot_chat_log',
        'user_chat_log',
        'info_bot',
        'reflection_bot',
        'reflect_diary',
        'user'
    ]
    for variable in delete_variables:
        _delete_session_variable(variable)

    return render_template("/pages/end.html")


@app.route('/chat_with_mindy/<user_id>', methods=['GET', 'POST'])
def mindy_chat(user_id):
    
    delete_variables = [
        'user',
        'mindy'
    ]
    for variable in delete_variables:
        _delete_session_variable(variable)
    
    return redirect(url_for('mindy', user_id=user_id))


@app.route('/mindy_chat/<user_id>', methods=['GET', 'POST'])
def mindy(user_id):
    
    session["user"] = str(user_id)
    session["mindy"] = session.get("mindy", {})
    chat_log = session["mindy"].get('chat_log')
    if chat_log is None:
        select_prompt = init_mindy()
        session["mindy"]["chat_log"] = select_prompt["prompt"] + select_prompt["message_start"]
        session["mindy"]["chatbot"] = select_prompt["chatbot"]

    convo = GPTConversation(
        user_id, 
        session["mindy"].get("chatbot"),
        session["mindy"].get("chat_log"),
        bot_start="Hi! I am Mindy, your mindfulness buddy! How can I help you today?",
        convo_start="\n\nHuman: Hello, who are you?\nMindy: Hi! I am Mindy, your mindfulness buddy! How can I help you today?"
    )

    form = ChatForm()
    if form.validate_on_submit() and not session.get('end'):
        user_message = form.message.data
        answer = convo.ask(user_message)
        chat_log = convo.append_interaction_to_chat_log(user_message, answer)

        session["mindy"]['chat_log'] = chat_log

        add_new_chat_log(user_id, session["mindy"]['chat_log'])

        return redirect(url_for('mindy', user_id=user_id))

    return render_template(
        '/dialogue/qualtrics_card.html',
        user=convo.get_user(),
        bot=convo.get_chatbot(),
        show_bot_avatar=True,
        warning=convo.WARNING,
        end=convo.END,
        notification=convo.NOTI,
        conversation=convo.get_conversation(end=session.get('end')),
        title="Mindy",
        form=form
    )


@app.route('/bot_video_diary', methods=['GET', 'POST'])
def bot_video_diary():
    
    return render_template("/pages/bot_video_diary.html")


@app.route('/info_diary')
def info_diary():
    
    return render_template("/pages/info_diary.html")
