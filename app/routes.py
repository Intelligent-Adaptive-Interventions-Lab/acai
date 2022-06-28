from app import app
from app.chatbot import ask, append_interaction_to_chat_log
from app.tasks import get_conversation
from app.forms import ChatForm

from flask import Flask, request, session, jsonify, render_template, redirect, url_for
from twilio.twiml.messaging_response import MessagingResponse
# import run_with_ngrok from flask_ngrok to run the app using ngrok
# from flask_ngrok import run_with_ngrok

from datetime import datetime, timezone

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

SESSION_PROMPT = "The following is a conversation with a friend. The friend is funny, shy, empathetic, and introverted."

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    chat_log = session.get('chat_log')
    print(f"chat_log: {chat_log}")
    
    if chat_log is None:
        chat_log = SESSION_PROMPT + "\n\nPerson: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?"
    
    print(f"FORM: {request.form}")
    
    form = ChatForm()
    if form.validate_on_submit():
        user_message = form.message.data
        chat_log = session.get('chat_log')
        answer = ask(user_message, chat_log)
        session['chat_log'] = append_interaction_to_chat_log(user_message, answer, chat_log)
        
        print(f"click successful!!! {user_message}")
        print(f"session: {session}")
        print(f"chat_log: {chat_log}")
        return redirect(url_for('index'))
    
    return render_template(
        '/dialogue/conversation_card.html', 
        user=USER, 
        bot=CHATBOT, 
        warning=WARNING, 
        end=END,
        notification=NOTI,
        conversation=get_conversation(SESSION_PROMPT, chat_log),
        form=form
    )

@app.route('/qualtrics', methods=['GET', 'POST'])
def qualtrics():
    
    # TODO: First checking if user existed in database
    # TODO: [In Qualtrics] Second, check contextual variables in MOOClet Engine
    # TODO: [In Qualtrics] check if this user has an arm
    # TODO: [In Qualtrics] If user doesn't have an arm, run MOOClet Engine -> get one arm
    # TODO: arm -> get chat log : The following is a conversation with a friend. The friend is funny, shy, empathetic, and introverted.\n\nPerson: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?
    # TODO: chat log -> OpenAI API -> get the generated responses for the bot
    # TODO: chat log + genrated responses -> conversation
    # TODO: otherwise, get all conversation from the database
    # TODO: [NOT in this API] user can give us responses <- not from this API
    # TODO: [NOT in this API] storing/updating this conversation to database
    
    return render_template(
        '/dialogue/qualtrics_card.html', 
        user=USER, 
        bot=CHATBOT, 
        warning=WARNING, 
        end=END,
        notification=NOTI,
        conversation=conversation
    )

# @app.route('/send_response/?user_id=XXX/')
# def updating_conversation(request):
#     # TODO: user can give us responses <- not from this API
#     # TODO: storing/updating this conversation to database
#     pass


@app.route('/chatsms', methods=['POST'])
def chatsms():
    incoming_msg = request.values['Body']
    print("request: ")
    print(request)
    print()

    print("incoming_msg: {}".format(incoming_msg))
    print()
    chat_log = session.get('chat_log')
    print("chat_log: {}".format(chat_log))
    print()

    answer = ask(incoming_msg, chat_log)
    print("answer: {}".format(answer))
    print()

    session['chat_log'] = append_interaction_to_chat_log(incoming_msg, answer,chat_log)
    
    msg = MessagingResponse()
    msg.message(answer)

    print("message: {}".format(msg))
    print()
    return str(msg)


@app.route('/chatweb', methods=['POST'])
def chatweb():
    input_json = request.get_json(force=True) 
    incoming_msg = str(input_json['response'])
    user_id = str(input_json['response'])
    print("session: ")
    print(session)
    print()
    chat_log = session.get('chat_log')
    answer = ask(incoming_msg, chat_log)
    session['chat_log'] = append_interaction_to_chat_log(incoming_msg, answer, chat_log)
    session['user_id'] = request.remote_addr

    dictToReturn = {
        "answer": answer,
        "chat_log": session['chat_log']
    }
    return jsonify(dictToReturn)

@app.route('/clear', methods=['GET'])
def clear_session():
    
    session['chat_log'] = None
    return "cleared!"