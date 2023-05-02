from flask import Flask, session
from flask_session import Session
import openai
import yaml
import redis


with open('./app/static/secret.yaml') as file:
    secret_keys = yaml.load(file, Loader=yaml.FullLoader)
    openai.api_key = secret_keys['openai']
    openai.organization = "org-FYH4qiS0WzXH7l0pCbezhmat"

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY = 'this-is-a-secret-key'
)

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
# app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')

server_session = Session(app)


from app import routes
