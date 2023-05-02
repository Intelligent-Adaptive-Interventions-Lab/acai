import flask

from app import app
from app.chatbot import ask, append_interaction_to_chat_log
from app.forms import ChatForm, BotToBotChatForm, EvaluationForm
from app.conversation import (
    AutoScriptConversation,
    CustomGPTConversation,
    GPTConversation,
    init_prompt,
    init_reflection_bot,
    init_information_bot
)
from app.gpt_chatbot import MI_Conversation, MI_GPTConversation

from flask import Flask, request, session, jsonify, render_template, redirect, url_for, Response, json
from flask_session import Session
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime, timedelta, timezone
import sqlite3

import os, os.path
import errno
import uuid
import time

from app.quiz import Quiz, QuizUtility
from datetime import datetime
# run_with_ngrok(app)



USER = "Person"
CHATBOT = "AI"
WARNING = "warning"
END = "end"
NOTI = "notification"

conversation = [
    {
        "from": CHATBOT,
        "to": WARNING,
        "message": "The following is a conversation with a therapist. The therapist is helpful, creative, empathetic, and very friendly.",
        "send_time": datetime(2022, 6, 20, 0, 0, 0, tzinfo=timezone.utc)
    },
    {
        "from": CHATBOT,
        "to": NOTI,
        "message": "Yesterday",
        "send_time": datetime(2022, 6, 20, 0, 0, 0, tzinfo=timezone.utc)
    },
    {
        "from": USER,
        "to": CHATBOT,
        "message": "Hello, who are you?",
        "send_time": datetime(2022, 6, 20, 0, 0, 1, tzinfo=timezone.utc)
    },
    {
        "from": CHATBOT,
        "to": USER,
        "message": "I am an AI created by OpenAI. How can I help you today?",
        "send_time": datetime(2022, 6, 20, 0, 1, 0, tzinfo=timezone.utc)
    },
    {
        "from": USER,
        "to": CHATBOT,
        "message": "I need help.",
        "send_time": datetime(2022, 6, 20, 0, 2, 0, tzinfo=timezone.utc)
    },
    {
        "from": CHATBOT,
        "to": USER,
        "message": "I'm sorry to hear that. What's going on?",
        "send_time": datetime(2022, 6, 20, 0, 3, 0, tzinfo=timezone.utc)
    },
    {
        "from": CHATBOT,
        "to": NOTI,
        "message": "Today",
        "send_time": datetime(2022, 6, 20, 0, 4, 0, tzinfo=timezone.utc)
    },
    {
        "from": USER,
        "to": CHATBOT,
        "message": "I had an argument with my family today.",
        "send_time": datetime(2022, 6, 20, 0, 4, 0, tzinfo=timezone.utc)
    },
    {
        "from": CHATBOT,
        "to": USER,
        "message": "I'm sorry to hear that. Can you tell me more about what happened?",
        "send_time": datetime(2022, 6, 20, 0, 5, 0, tzinfo=timezone.utc)
    },
    {
        "from": USER,
        "to": CHATBOT,
        "message": "I told my mom that I want to buy a computer but she was very upset about that.",
        "send_time": datetime(2022, 6, 20, 0, 6, 0, tzinfo=timezone.utc)
    },
    {
        "from": CHATBOT,
        "to": USER,
        "message": "I'm sorry to hear that she was upset. Can you tell me more about why you want to buy a computer?",
        "send_time": datetime(2022, 6, 20, 0, 7, 0, tzinfo=timezone.utc)
    },
    {
        "from": USER,
        "to": CHATBOT,
        "message": "I told her that I need a computer to complete my assignment.",
        "send_time": datetime(2022, 6, 20, 0, 8, 0, tzinfo=timezone.utc)
    },
    {
        "from": CHATBOT,
        "to": USER,
        "message": "I see. And she was upset because she doesn't think you need a computer for that?",
        "send_time": datetime(2022, 6, 20, 0, 9, 0, tzinfo=timezone.utc)
    },
    {
        "from": USER,
        "to": CHATBOT,
        "message": "No, she doesn't 😥.",
        "send_time": datetime(2022, 6, 20, 0, 10, 0, tzinfo=timezone.utc)
    },
    {
        "from": CHATBOT,
        "to": USER,
        "message": "I'm sorry to hear that. Can you tell me more about your assignment? Maybe there's a way to do it without a computer.",
        "send_time": datetime(2022, 6, 20, 0, 11, 0, tzinfo=timezone.utc)
    },
    {
        "from": USER,
        "to": CHATBOT,
        "message": "There is NO WAY to finish that assignment without a computer. Why didn't she understand that??? 😡",
        "send_time": datetime(2022, 6, 20, 0, 12, 0, tzinfo=timezone.utc)
    },
    {
        "from": CHATBOT,
        "to": USER,
        "message": "It sounds like you're feeling frustrated because you feel like your mom doesn't understand your needs. Can you tell me more about that?",
        "send_time": datetime(2022, 6, 20, 0, 13, 0, tzinfo=timezone.utc)
    },
    {
        "from": CHATBOT,
        "to": END,
        "message": "This conversation ended by the system.",
        "send_time": datetime(2022, 6, 20, 0, 14, 0, tzinfo=timezone.utc)
    }
]

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    mkdir_p(os.path.dirname(path))
    return open(path, 'w')


def _delete_session_variable(variable: str) -> None:
    try:
        del session[variable]
    except KeyError:
        pass


@app.route('/index')
def index():

    return render_template("/quiz/main.html", date=datetime.today().strftime('%Y-%m-%d'))


@app.route('/quiz_content', methods=['GET', 'POST'])
def quiz_content():

    qid = session.setdefault("qid", f"QUIZ-{uuid.uuid1()}")
    questions = session.setdefault("quiz_questions", Quiz().get_questions())
    curr_idx = session.setdefault("index", 0)
    
    if curr_idx >= 32:
            return render_template("/quiz/ending_page.html", 
                user_id = qid,
                date = datetime.now(timezone.utc).strftime('%m/%d/%Y')
                )

    total_rewards = session.setdefault("total_rewards", {"charity": 0, "self": 0})
    question_start_time = session.setdefault("question_start_time", time.time())
    difficulty_selection_time = session.setdefault("difficulty_selection_time", datetime.min)
    selected_choice = session.setdefault("selected_choice", 0)

    active_questions = questions[curr_idx]
    curr_question = active_questions[selected_choice]


    form = EvaluationForm()
    form.selection.choices = [("0", "".join(map(str, curr_question["choices"][0]))),
                              ("1", "".join(map(str, curr_question["choices"][1])))]
    
    print(f"selection: {selected_choice}    \nactive_questions:{active_questions}\ncurr_questions:{curr_question}")


    if form.validate_on_submit() and difficulty_selection_time > question_start_time:
        submit_time = time.time()
        result = int(form.selection.data)

        print(f"choice {result}")

        # set reward if correctly answered
        if result == curr_question["correct_idx"]:
            print("Correct choice")
            actual_reward = curr_question["reward"]
            total_rewards[curr_question["receiver"]] += actual_reward
        else:
            print("Incorrect choice")
            actual_reward = 0

        sqliteConnection = None
        try:
            sqliteConnection = sqlite3.connect(app.root_path+'/database.db')
            cursor = sqliteConnection.cursor()
            print("Successfully Connected to SQLite")
            time1 = difficulty_selection_time - question_start_time
            print(f"time {difficulty_selection_time} {question_start_time} {submit_time} {difficulty_selection_time}")
            time2 = submit_time - difficulty_selection_time
            sqlite_insert_query = """INSERT INTO quiz
                                  (quiz_id, receiver, difficulty, reward, answer, actual_reward, time1, time2) 
                                   VALUES 
                                  (?,?,?,?,?,?,?,?);"""

            param_tuple = (qid, 
                curr_question["receiver"], 
                curr_question["difficulty"], 
                curr_question["reward"], 
                "".join(map(str, curr_question["choices"][result])), 
                actual_reward, 
                '%.2f'%time1, 
                '%.2f'%time2)

            count = cursor.execute(sqlite_insert_query, param_tuple)
            sqliteConnection.commit()
            print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
            cursor.close()

        except Exception as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("The SQLite connection is closed")


        # update variables
        curr_idx += 1

        active_questions = questions[curr_idx]
        question_start_time = time.time()


        # update session variables
        session["qid"] = qid
        session["quiz_questions"] = questions
        session["index"] = curr_idx
        session["total_rewards"] = total_rewards
        session["question_start_time"] = question_start_time
        session["difficulty_selection_time"] = difficulty_selection_time

        if curr_idx >= 32:
            return render_template("/quiz/ending_page.html", 
                user_id = qid,
                date = datetime.now(timezone.utc).strftime('%m/%d/%Y')
                )

        return redirect(url_for('quiz_content'))

    return render_template("/quiz/content.html",
                                question1=active_questions[0],
                                question2=active_questions[1],
                                score1=total_rewards["charity"],
                                score2=total_rewards["self"],
                                form=form,
                                page_num=curr_idx
                           )




@app.route("/getchoice", methods=["POST"])
def get_user_choice():
    difficulty_choice = request.json.get("difficulty_choice")

    if difficulty_choice != None:
        if difficulty_choice == 0:
            print("diff choice 0")
            session["selected_choice"] = 0
        elif difficulty_choice == 1:
            session["selected_choice"] = 1
            print("diff choice 1")

        questions = session.setdefault("quiz_questions", Quiz().get_questions())
        curr_idx = session.setdefault("index", 0)
        selected_choice = session.setdefault("selected_choice", 0)

        active_questions = questions[curr_idx]
        curr_question = active_questions[selected_choice]

        response = app.response_class(
            response=json.dumps({"choice0": "".join(map(str, curr_question["choices"][0])),
                "choice1": "".join(map(str, curr_question["choices"][1]))}),
            status=200,
            mimetype='application/json'
        )
        session["difficulty_selection_time"] = time.time()
        print(f"selection: {selected_choice}    \nactive_questions:{active_questions}\ncurr_questions:{curr_question}")
    else:
        response = app.response_class(
            response=json.dumps({"diff": 0}),
            status=400,
            mimetype='application/json'
        )

    return response

@app.route('/')
def main():
    return render_template("/pages/main.html")

@app.route('/mi_conversation', methods=['GET', 'POST'])
def mi_conversation():
    INITIAL_TIMER = 300

    chat_log = session.get('mi_chat_log', f"{MI_Conversation.CONVO_START}\n\n{MI_Conversation.CHATBOT}: {MI_Conversation.BOT_START}")
    chatbot = session.get('mi_chatbot', "Alex")
    user = session.get('mi_user', "A-"+str(uuid.uuid1()))
    start = session.get('mi_start', int(time.time()))

    timer_remaining = INITIAL_TIMER - (int(time.time()) - start)

    convo = MI_GPTConversation(user, chatbot, chat_log)

    session['mi_user'] = user
    session["mi_chatbot"] = chatbot
    session["mi_start"] = start

    form = ChatForm()
    if form.validate_on_submit():
        user_message = form.message.data
        answer = convo.ask(user_message)
        chat_log = convo.append_interaction_to_chat_log(user_message, answer)
        session["mi_chat_log"] = chat_log

        f = None
        try:
            path = f"{app.root_path}/adaptive_mi_chatlogs/{user}.txt"
            f = safe_open_w(path)
            f.write(chat_log)
            print(f"Saved chatlogs to {path}")
        except Exception as e:
            print(f"Failed to save chatlogs. {e}")
        finally:
            if f:
                f.close()

        return redirect(url_for('mi_conversation'))

    return render_template(
        '/pages/adaptive_convo_motivational_interview.html',
        user=convo.get_user(),
        bot=convo.get_chatbot(),
        # warning=convo.WARNING,
        end=convo.END,
        notification=convo.NOTI,
        conversation=convo.get_conversation(test=True),
        form=form,
        enable_typing_animation=1,
        timer=timer_remaining
    )

@app.route('/motivational_interview', methods=['GET', 'POST'])
def motivational_interview_conversation():
    INITIAL_TIMER = 300

    chat_log = session.get('motivational_interview_chat_log', None)
    dialogue_id = session.get('motivational_interview_dialogue_id', None)
    dialogue_answers = session.get('motivational_interview_dialogue_answers', {})
    auxillary_data = session.get('motivational_interview_auxillary_data', {})
    user = session.get('motivational_interview_user', "D-"+str(uuid.uuid1()))
    start = session.get('motivational_interview_start', int(time.time()))

    timer_remaining = INITIAL_TIMER - (int(time.time()) - start)

    convo = AutoScriptConversation(
        user=user,
        chatbot="Alex",
        dialogue_path="motivational_interview",
        dialogue_answers=dialogue_answers,
        auxillary_data=auxillary_data
    )

    dialogue_id, chat_log = convo.sync_chat_log(chat_log=chat_log,
                                                dialogue_id=dialogue_id)
    session["motivational_interview_chat_log"] = chat_log
    session["motivational_interview_dialogue_id"] = dialogue_id
    session["motivational_interview_user"] = user
    session["motivational_interview_start"] = start

    form = ChatForm()
    if form.validate_on_submit():
        message = form.message.data
        dialogue_answers[dialogue_id] = message
        session["motivational_interview_dialogue_answers"] = dialogue_answers

        dialogue_id, chat_log = convo.give_answer(answer=message)
        session["motivational_interview_chat_log"] = chat_log
        session["motivational_interview_dialogue_id"] = dialogue_id
        session["motivational_interview_auxillary_data"] = auxillary_data


        f = None
        try:
            path = f"{app.root_path}/deterministic_mi_chatlogs/{user}.txt"
            f = safe_open_w(path)
            f.write(chat_log)
            print(f"Saved chatlogs to {path}")
        except Exception as e:
            print(f"Failed to save chatlogs. {e}")
        finally:
            if f:
                f.close()

        return render_template(
            '/pages/deterministic_convo_motivational_interview.html',
            user=convo.get_user(),
            bot=convo.get_chatbot(),
            warning=convo.WARNING,
            end=convo.END,
            notification=convo.NOTI,
            conversation=convo.get_conversation(),
            form=form,
            enable_typing_animation=1,
            timer=timer_remaining
        )

    return render_template(
        '/pages/deterministic_convo_motivational_interview.html',
        user=convo.get_user(),
        bot=convo.get_chatbot(),
        warning=convo.WARNING,
        end=convo.END,
        notification=convo.NOTI,
        conversation=convo.get_conversation(),
        form=form,
        enable_typing_animation=1,
        timer=timer_remaining
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
            '/pages/convo.html',
            user=convo.get_user(),
            bot=convo.get_chatbot(),
            warning=convo.WARNING,
            end=convo.END,
            notification=convo.NOTI,
            conversation=convo.get_conversation(),
            form=form
        )

    return render_template(
        '/pages/convo.html',
        user=convo.get_user(),
        bot=convo.get_chatbot(),
        warning=convo.WARNING,
        end=convo.END,
        notification=convo.NOTI,
        conversation=convo.get_conversation(),
        form=form
    )


@app.route('/bot_to_bot', methods=['GET', 'POST'])
def bot_to_bot():
    form = BotToBotChatForm(turn="Bot")

    bot = CustomGPTConversation(
        user="HUMAN",
        chatbot="AI",
        chat_log=session.get('bot_chat_log', form.bot_prompt.data),
        prompt=form.bot_prompt.data,
        default_start="I am an AI created by OpenAI. How are you doing today?"
    )
    bot.prompt = bot.get_prompt()
    form.bot_prompt.default = bot.get_prompt()

    user = CustomGPTConversation(
        user="HUMAN",
        chatbot="AI",
        chat_log=session.get('user_chat_log', form.user_prompt.data),
        prompt=form.user_prompt.data,
        default_start="Hello, who are you?"
    )
    user.prompt = user.get_prompt()
    form.user_prompt.default = user.get_prompt()

    if form.validate_on_submit():
        # print("============== START ==============")
        message = form.message.data
        turn = form.turn.data

        # Check current turn of the conversation
        if turn == 'User':
            # USER turn
            # Check if providing message manually
            if message != '':
                # [USER] Add answer (self) message to chat log
                user.append_interaction_to_chat_log(answer=message)

                # [BOT] Generate message to chat log
                answer = bot.ask(question=message)

                # [BOT] Add message back to chat log
                bot_chat_log = bot.append_interaction_to_chat_log(
                    question=message, answer=answer)

                # [USER] Add question (opposite) message to chat log
                user_chat_log = user.append_interaction_to_chat_log(
                    question=answer)

                form.turn.default = 'User'
            else:
                # [USER] Get last message for question
                question = user.get_last_message()

                if question == '':
                    # [USER] If no starting message is given, use the default start
                    answer = user.default_start
                else:
                    # [USER] Ask to get answer
                    answer = user.ask()

                # [BOT] Add question (opposite) message to chat log
                bot_chat_log = bot.append_interaction_to_chat_log(
                    question=answer)

                # [USER] Add answer (self) message to chat log
                user_chat_log = user.append_interaction_to_chat_log(
                    answer=answer)

                form.turn.default = 'Bot'
        else:
            # BOT turn
            # Check if providing message manually
            if message != '':
                # [BOT] Add answer (self) message to chat log
                bot.append_interaction_to_chat_log(answer=message)

                # [USER] Generate message to chat log
                answer = user.ask(question=message)

                # [USER] Add message back to chat log
                user_chat_log = user.append_interaction_to_chat_log(
                    question=message, answer=answer)

                # [BOT] Add question (opposite) message to chat log
                bot_chat_log = user.append_interaction_to_chat_log(
                    question=answer)
                bot_chat_log = bot.append_interaction_to_chat_log(
                    question=answer)
                form.turn.default = 'Bot'
            else:
                # [BOT] Get last message for question
                question = bot.get_last_message()

                if question == '':
                    # [BOT] If no starting message is given, use the default start
                    answer = bot.default_start
                else:
                    # [BOT] Ask to get answer
                    answer = bot.ask()

                # [USER] Add question (opposite) message to chat log
                user_chat_log = user.append_interaction_to_chat_log(
                    question=answer)

                # [BOT] Add answer (self) message to chat log
                bot_chat_log = bot.append_interaction_to_chat_log(answer=answer)

                form.turn.default = 'User'

        # Sync both USER and BOT chat logs
        user.sync_chat_log(user_chat_log)
        bot.sync_chat_log(bot_chat_log)

        # Update Session
        session['user_chat_log'] = user_chat_log
        session['bot_chat_log'] = bot_chat_log
        form.process()

        sqliteConnection = None
        try:
            sqliteConnection = sqlite3.connect(
                '/var/www/html/acaidb/database.db')
            cursor = sqliteConnection.cursor()
            print("Successfully Connected to SQLite")

            sqlite_insert_query = """INSERT INTO chats
                                  (user_id, chat_log) 
                                   VALUES 
                                  (?,?);"""
            param_tuple = ("BTB - {}".format(bot.get_user()), bot_chat_log)
            count = cursor.execute(sqlite_insert_query, param_tuple)
            sqliteConnection.commit()
            print(
                "Record inserted successfully into SqliteDb_developers table ",
                cursor.rowcount)
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("The SQLite connection is closed")

        # print("============== END ==============")
        # Render conversation from BOT
        return render_template(
            "/pages/bot_to_bot.html",
            user=bot.get_user(),
            bot=bot.get_chatbot(),
            warning=bot.WARNING,
            end=bot.END,
            notification=bot.NOTI,
            conversation=bot.get_conversation(test=False),
            form=form
        )

    return render_template(
        "/pages/bot_to_bot.html",
        user=bot.get_user(),
        bot=bot.get_chatbot(),
        warning=bot.WARNING,
        end=bot.END,
        notification=bot.NOTI,
        conversation=bot.get_conversation(test=False),
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

    convo = GPTConversation(session.get("user"), session.get("chatbot"),
                            session.get("chat_log"))

    form = ChatForm()
    if form.validate_on_submit():
        user_message = form.message.data
        answer = convo.ask(user_message)
        chat_log = convo.append_interaction_to_chat_log(user_message, answer)
        session["chat_log"] = chat_log
        sqliteConnection = None
        try:
            sqliteConnection = sqlite3.connect(
                '/var/www/html/acaidb/database.db')
            cursor = sqliteConnection.cursor()
            print("Successfully Connected to SQLite")

            sqlite_insert_query = """INSERT INTO chats
                                  (user_id, chat_log) 
                                   VALUES 
                                  (?,?);"""
            param_tuple = (session["user"], session["chat_log"])
            count = cursor.execute(sqlite_insert_query, param_tuple)
            sqliteConnection.commit()
            print(
                "Record inserted successfully into SqliteDb_developers table ",
                cursor.rowcount)
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("The SQLite connection is closed")

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

    convo = GPTConversation(session.get("user"), session.get("chatbot"),
                            session.get("chat_log"))

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

    form = ChatForm()
    if form.validate_on_submit() and not session.get('end'):
        user_message = form.message.data
        answer = convo.ask(user_message)
        chat_log = convo.append_interaction_to_chat_log(user_message, answer)

        session['chat_log'] = chat_log
        sqliteConnection = None
        try:
            sqliteConnection = sqlite3.connect(
                '/var/www/html/acaidb/database.db')
            cursor = sqliteConnection.cursor()
            print("Successfully Connected to SQLite")

            sqlite_insert_query = """INSERT INTO chats
                                  (user_id, chat_log) 
                                   VALUES 
                                  (?,?);"""
            param_tuple = (session["user"], session["chat_log"])
            count = cursor.execute(sqlite_insert_query, param_tuple)
            sqliteConnection.commit()
            print(
                "Record inserted successfully into SqliteDb_developers table ",
                cursor.rowcount)
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("The SQLite connection is closed")

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


@app.route('/chatsms', methods=['POST'])
def chatsms():
    incoming_msg = request.values['Body']
    chat_log = session.get('chat_log')
    answer = ask(incoming_msg, chat_log)

    session['chat_log'] = append_interaction_to_chat_log(incoming_msg, answer,
                                                         chat_log)

    msg = MessagingResponse()
    msg.message(answer)

    return str(msg)


@app.route('/chatweb', methods=['POST'])
def chatweb():
    input_json = request.get_json(force=True)
    incoming_msg = str(input_json['response'])
    chat_log = session.get('chat_log')
    answer = ask(incoming_msg, chat_log)
    session['chat_log'] = append_interaction_to_chat_log(incoming_msg, answer,
                                                         chat_log)

    dictToReturn = {
        "answer": answer,
        "chat_log": session['chat_log']
    }
    return jsonify(dictToReturn)


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
        'reflection_bot'
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
        sqliteConnection = None
        try:
            sqliteConnection = sqlite3.connect(
                '/var/www/html/acaidb/database.db')
            cursor = sqliteConnection.cursor()
            print("Successfully Connected to SQLite")

            sqlite_insert_query = """INSERT INTO chats
                                  (user_id, chat_log) 
                                   VALUES 
                                  (?,?);"""
            param_tuple = (info_bot["user"], info_bot["chat_log"])
            count = cursor.execute(sqlite_insert_query, param_tuple)
            sqliteConnection.commit()
            print(
                "Record inserted successfully into SqliteDb_developers table ",
                cursor.rowcount)
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("The SQLite connection is closed")

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


@app.route('/reflect_bot', methods=['GET', 'POST'])
def reflect_bot():
    reflection_bot = session.get("reflection_bot", None)
    if not reflection_bot:
        select_prompt = init_reflection_bot()
        reflection_bot = {
            "chat_log": select_prompt["prompt"] + select_prompt[
                "message_start"],
            "convo_start": select_prompt["message_start"],
            "bot_start": "Hello. I am an AI agent designed to act as your Mindfulness instructor. I am here to help you reflect on your learnings. How can I help you?",
            "chatbot": select_prompt["chatbot"],
            "user": request.remote_addr,
            "start": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        }

    convo = GPTConversation(
        user=reflection_bot.get("user"),
        chatbot=reflection_bot.get("chatbot"),
        chat_log=reflection_bot.get("chat_log"),
        bot_start=reflection_bot.get("bot_start"),
        convo_start=reflection_bot.get("convo_start")
    )

    start = reflection_bot.get('start')
    if start is None:
        reflection_bot["start"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    stop = reflection_bot.get('stop')
    if stop is None:
        reflection_bot["stop"] = 5 * 60

    now = datetime.now()
    difference = now - datetime.strptime(reflection_bot.get('start'),
                                         "%m/%d/%Y, %H:%M:%S")
    difference_seconds = difference.total_seconds()

    end = reflection_bot.get('end')
    if end is None or not end:
        reflection_bot["end"] = (
                difference_seconds >= reflection_bot.get('stop'))

    form = ChatForm()
    if form.validate_on_submit() and not reflection_bot.get('end'):
        user_message = form.message.data
        answer = convo.ask(user_message)
        chat_log = convo.append_interaction_to_chat_log(user_message, answer)

        reflection_bot['chat_log'] = chat_log
        sqliteConnection = None
        try:
            sqliteConnection = sqlite3.connect(
                '/var/www/html/acaidb/database.db')
            cursor = sqliteConnection.cursor()
            print("Successfully Connected to SQLite")

            sqlite_insert_query = """INSERT INTO chats
                                  (user_id, chat_log) 
                                   VALUES 
                                  (?,?);"""
            param_tuple = (reflection_bot["user"], reflection_bot["chat_log"])
            count = cursor.execute(sqlite_insert_query, param_tuple)
            sqliteConnection.commit()
            print(
                "Record inserted successfully into SqliteDb_developers table ",
                cursor.rowcount)
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("The SQLite connection is closed")

        session["reflection_bot"] = reflection_bot
        return redirect(url_for('reflect_bot'))

    session["reflection_bot"] = reflection_bot
    return render_template(
        '/dialogue/qualtrics_card.html',
        user=convo.get_user(),
        bot=convo.get_chatbot(),
        warning=convo.WARNING,
        end=convo.END,
        notification=convo.NOTI,
        conversation=convo.get_conversation(end=reflection_bot.get('end')),
        form=form
    )
