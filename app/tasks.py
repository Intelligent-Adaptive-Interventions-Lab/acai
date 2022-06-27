from flask import Flask, request, session, jsonify, render_template
from flask.sessions import SecureCookieSession

from typing import Dict

USER = "User"
CHATBOT = "Chatbot"
WARNING = "warning"
END = "end"
NOTI = "notification"


def get_conversation(session: SecureCookieSession) -> Dict:
    return 
