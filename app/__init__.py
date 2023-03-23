from flask import Flask

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY = 'this-is-a-secret-key'
)

with open('./app/static/secret.yaml') as file:
    secret_keys = yaml.load(file, Loader=yaml.FullLoader)
    openai.api_key = secret_keys['openai']
    openai.organization = "org-FYH4qiS0WzXH7l0pCbezhmat"


from app import routes
