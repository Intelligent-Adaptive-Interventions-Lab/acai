from flask import Flask, request, session, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from app.chatbot import ask, append_interaction_to_chat_log
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)
# if for some reason your conversation with Jabe gets weird, change the secret key
app.config['SECRET_KEY'] = 'this-is-a-secrete-key'

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
    chat_log = session.get('chat_log')
    answer = ask(incoming_msg, chat_log)
    session['chat_log'] = append_interaction_to_chat_log(incoming_msg, answer,chat_log)

    dictToReturn = {
        "answer": answer,
        "chat_log": session['chat_log']
    }
    return jsonify(dictToReturn)


if __name__ == '__main__':
    app.run()