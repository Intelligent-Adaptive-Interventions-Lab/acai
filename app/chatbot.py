from app import app


import openai
import yaml


with open('./app/static/secret.yaml') as file:
    secret_keys = yaml.load(file, Loader=yaml.FullLoader)
openai.api_key = secret_keys["openai"]
completion = openai.Completion()

start_sequence = "\nAI:"
restart_sequence = "\n\nPerson:"

session_prompt1 = "The following is a conversation with a friend. " + \
    "The friend is funny, shy, empathetic, and introverted." + \
    "\n\nPerson: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?"


session_prompt2 = "The following is a conversation with a therapist. " + \
    "The therapist is helpful, creative, empathetic, and very friendly." + \
    "\n\nPerson: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?"


def ask(question, chat_log=None):
    prompt_text = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt_text,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.3,
        stop=["\n"],
    )

    story = response['choices'][0]['text']

    return str(story)


def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = session_prompt1
    return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'