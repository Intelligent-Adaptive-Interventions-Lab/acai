from app import app
import openai
import yaml

with open('./app/static/secret.yaml') as file:
    secret_keys = yaml.load(file, Loader=yaml.FullLoader)
openai.api_key = secret_keys["openai"]
openai.organization = "org-FYH4qiS0WzXH7l0pCbezhmat"


if __name__ == "__main__":
    app.run()
