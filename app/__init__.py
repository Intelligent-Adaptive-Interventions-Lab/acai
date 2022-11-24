from flask import Flask


app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY = 'this-is-a-secret-key'
)


from app import routes
