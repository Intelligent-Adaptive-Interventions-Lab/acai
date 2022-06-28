from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY = 'this-is-a-secret-key'
)

csrf = CSRFProtect()
csrf.init_app(app)

from app import routes