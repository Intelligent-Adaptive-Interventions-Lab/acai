from flask import Flask, request, session, jsonify, render_template
from flask.sessions import SecureCookieSession
from datetime import datetime, timezone

from typing import Dict

USER = "Person"
CHATBOT = "AI"
WARNING = "warning"
END = "end"
NOTI = "notification"

CONVO_START = "\n\nPerson: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?"

BOT_START = "I am an AI created by OpenAI. How can I help you today?"

def get_conversation(session_prompt1, chat_log) -> Dict:
    # session_prompt1 = "The following is a conversation with a friend. The friend is funny, shy, empathetic, and introverted."
    # chat_log = "The following is a conversation with a friend. The friend is funny, shy, empathetic, and introverted.\n\nPerson: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\n\nPerson: Hello!\nAI: Hi there!\n\nPerson: Hello!\nAI: Hello, how are you doing today?"
    timestamps = [
        datetime(2022, 6, 20, 0, 0, 0, tzinfo=timezone.utc).strftime("%A, %d. %B %Y %I:%M%p"), 
        datetime(2022, 6, 20, 0, 0, 0, tzinfo=timezone.utc).strftime("%A, %d. %B %Y %I:%M%p"), 
        datetime(2022, 6, 20, 0, 0, 0, tzinfo=timezone.utc).strftime("%A, %d. %B %Y %I:%M%p"),
        
        datetime(2022, 6, 20, 0, 1, 0, tzinfo=timezone.utc).strftime("%A, %d. %B %Y %I:%M%p"),
        datetime(2022, 6, 20, 0, 1, 0, tzinfo=timezone.utc).strftime("%A, %d. %B %Y %I:%M%p"),
        
        datetime(2022, 6, 20, 0, 2, 0, tzinfo=timezone.utc).strftime("%A, %d. %B %Y %I:%M%p"),
        datetime(2022, 6, 20, 0, 2, 0, tzinfo=timezone.utc).strftime("%A, %d. %B %Y %I:%M%p"),
    ]
    
    print("session_prompt1::: {}".format(session_prompt1))
    print("chat_log::: {}".format(chat_log))
    print("merged::: {}".format("".join([session_prompt1, CONVO_START])))
    print("split::: {}".format(chat_log.split("".join([session_prompt1, CONVO_START]))))
    
    chat_log_clean = chat_log.split("".join([session_prompt1, CONVO_START]))[1]
    dialogs = chat_log_clean.split("\n\n")
    
    converation = []
    converation.append({
        "from": CHATBOT,
        "to": USER,
        "message": BOT_START,
        "send_time": None
    })
    
    for i in range(1, len(dialogs)):
        messages = dialogs[i].split("\n")
        print("messages: {}".format(messages))
        
        if len(messages) == 1:
            identifier_message = messages[0].split(":")
            convo = {
                "from": identifier_message[0].strip(),
                "to": CHATBOT,
                "message": identifier_message[1].strip(),
                "send_time": None
            }
            
            converation.append(convo)
        else:
            user_message = messages[0].split(":")
            bot_message = messages[1].split(":")
            
            converation.extend([
                {
                    "from": user_message[0].strip(),
                    "to": bot_message[0].strip(),
                    "message": user_message[1].strip(),
                    "send_time": None
                },
                {
                    "from": bot_message[0].strip(),
                    "to": user_message[0].strip(),
                    "message": bot_message[1].strip(),
                    "send_time": None
                },
            ])
        
    return converation
