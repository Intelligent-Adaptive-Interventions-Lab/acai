from app import app
import openai
import yaml


# def start():
    with open('./app/static/secret.yaml') as file:
        secret_keys = yaml.load(file, Loader=yaml.FullLoader)
        openai.api_key = secret_keys["openai"]
        print(f"{openai.api_key} {secret_keys["openai"]} $$$$$$$$$$$$$$$$$$ {secret_keys}")
        openai.organization = "org-FYH4qiS0WzXH7l0pCbezhmat"

#     return app



if __name__ == "__main__":
    app.run()
