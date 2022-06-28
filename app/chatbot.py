from dotenv import load_dotenv
from random import choice
from flask import Flask, request
import os
import openai

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
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
    # response = openai.Completion.create(
    #     engine="davinci",
    #     temperature=0.8,
    #     max_tokens=150,
    #     top_p=1,
    #     frequency_penalty=0,
    #     presence_penalty=0.3,
    #     stop=["\n"],
    # )

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
        # session_prompts = [session_prompt1, session_prompt2]
        # chat_log = choice(session_prompts) 
        chat_log = session_prompt1
    return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'