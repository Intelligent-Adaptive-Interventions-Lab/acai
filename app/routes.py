from app import app
from app.chatbot import ask, append_interaction_to_chat_log

from flask import Flask, request, session, jsonify, render_template
from twilio.twiml.messaging_response import MessagingResponse
# import run_with_ngrok from flask_ngrok to run the app using ngrok
from flask_ngrok import run_with_ngrok

run_with_ngrok(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template('/dialogue/index.html')


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
    print("session: ")
    print(session)
    print()
    chat_log = session.get('chat_log')
    answer = ask(incoming_msg, chat_log)
    session['chat_log'] = append_interaction_to_chat_log(incoming_msg, answer,chat_log)

    dictToReturn = {
        "answer": answer,
        "chat_log": session['chat_log']
    }
    return jsonify(dictToReturn)

