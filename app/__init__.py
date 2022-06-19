from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this-is-a-secrete-key'

from app import routes