import re
from app import app
from app.dialogue import DialogCollection
from random import choice
from typing import Tuple, Dict, Optional

import openai
import yaml
import json


class MI_Conversation:
    CONVO_START = "You are a motivational interviewing chatbot. You are very kind, gentle, understanding, and warm. You are very interested in how I think and feel. You  encourage me to intrinsically want to be more caring towards others. You echo my feelings, and nurture my intrinsic motivation to be more caring. You ask me one question at a time, and wait for me to respond."
    BOT_START = "Hey there! I'm an AI developed by the University of Toronto, and I'm here to help you explore your desire to become more kind and caring towards others. Can you tell me a little bit more about what's been on your mind lately? What's been motivating you to want to be more caring?"
    USER = "HUMAN"
    CHATBOT = "AI"
    WARNING = "Warning"
    END = "End"
    NOTI = "Notification"

    def __init__(self, user: str, chatbot: str, chat_log: str=None) -> None:
        self.user_name = user
        self.chatbot_name = chatbot
        self.chat_log = chat_log

    def get_user(self) -> str:
        return self.user_name

    def get_chatbot(self) -> str:
        return self.chatbot_name


class MI_GPTConversation(MI_Conversation):

    
    CONFIGS = {
        "engine": "text-davinci-003",
        "temperature": 0.9,
        "max_tokens": 300,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0.6,
    }

    def __init__(self, user: str, chatbot: str, chat_log: str, bot_start: str=None, convo_start: str=None) -> None:
        super().__init__(user, chatbot, chat_log)

        if bot_start:
            self.BOT_START = bot_start

        if convo_start:
            self.CONVO_START = convo_start

        self.prompt = chat_log.split(self.CONVO_START)[0]
        self.start_sequence = f"{self.CHATBOT}:"
        self.restart_sequence = f"{self.USER}: "

    def ask(self, question: str) -> str:
        try:
            # is_english_query = openai.Completion.create(
            #     model="text-davinci-003",
            #     prompt=f"Is the text english? Yes or No?\n\nText:{question}\n\nAnswer:",
            #     temperature=0,
            #     max_tokens=15,
            #     request_timeout=3
            # )['choices'][0]['text'].lower().strip()

            # if "no" in is_english_query:
            #     print('NOT ENGLISH')
            #     return "Sorry, I don't understand. Could you try saying that in a different way?"

            # prompt_text = f"{self.chat_log}{self.restart_sequence}{question.strip()}{self.start_sequence}"
            # print(prompt_text)

            messages = [
                {
                    "role": "system",
                    "content": self.CONVO_START
                }
            ]

            for s in self.chat_log.split('\n'):
                if s == "":
                    continue
                msg = s.split(' ', 1)

                msg[0] = msg[0].strip()
                msg[1] = msg[1].strip()

                messages.append({
                    "role": "user" if msg[0] == self.restart_sequence else "assistant",
                    "content": msg[1]
                })

            messages.append({
                "role": "user",
                "content": question.strip()
            })

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                temperature=0.9,
                presence_penalty=0.6,
                request_timeout=30
            )

            resp_msg = response['choices'][0]['message']
            return resp_msg['content']
            

            # response = openai.Completion.create(
            #     prompt=prompt_text,
            #     stop=[" {}:".format(self.USER), " {}:".format(self.CHATBOT)],
            #     **self.CONFIGS,
            #     request_timeout=10
            # )

            # story = response['choices'][0]['text']
            # answer = str(story).strip().split(self.restart_sequence.rstrip())[0]
        except Exception as e:
            print(f"ERROR: {e}")
            return "Sorry, something went wrong. Can you please try again?"

    def append_interaction_to_chat_log(self, question: str, answer: str) -> str:
            return f"{self.chat_log}\n{self.restart_sequence} {question}\n{self.start_sequence} {answer}".strip()

    def get_conversation(self, end: bool=False, test: bool=False) -> Dict:
        # print("chat_log: ", self.chat_log)
        # print("split: ", "".join([self.prompt, self.CONVO_START]))
        # print("chat_log_clean: ", self.chat_log.split("".join([self.prompt, self.CONVO_START])))
        chat_log_clean = self.chat_log.split("".join([self.prompt, self.CONVO_START]))[1]
        dialogs = chat_log_clean.split(self.restart_sequence)

        converation = []

        if test:
            converation.append({
                "from": self.chatbot_name,
                "to": self.WARNING,
                "message": self.prompt,
                "send_time": None
            })

        converation.append({
            "from": self.chatbot_name,
            "to": self.user_name,
            "message": self.BOT_START,
            "send_time": None
        })

        for i in range(1, len(dialogs)):
            messages = dialogs[i].split(self.start_sequence)

            for msg_idx, msg in enumerate(messages):
                if msg_idx == 0:
                    from_idt = self.user_name
                    to_idt = self.chatbot_name
                else:
                    to_idt = self.user_name
                    from_idt = self.chatbot_name

                convo = []
                for text in msg.split("\n"):
                    if len(text) != 0:
                        convo.append({
                            "from": from_idt,
                            "to": to_idt,
                            "message": text.strip(),
                            "send_time": None
                        })
                converation.extend(convo)

        return converation
    
class NP_MI_GPTConversation(MI_Conversation):

    
    CONFIGS = {
        "engine": "text-davinci-003",
        "temperature": 0.9,
        "max_tokens": 300,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0.6,
    }

    def __init__(self, user: str, chatbot: str, chat_log: str, bot_start: str=None, convo_start: str=None) -> None:
        super().__init__(user, chatbot, chat_log)

        self.CONVO_START = "\n"
        self.BOT_START = "Hello, how can I help you?"

        self.prompt = ""
        self.start_sequence = f"{self.CHATBOT}:"
        self.restart_sequence = f"{self.USER}: "

    def ask(self, question: str) -> str:
        try:
            # is_english_query = openai.Completion.create(
            #     model="text-davinci-003",
            #     prompt=f"Is the text english? Yes or No?\n\nText:{question}\n\nAnswer:",
            #     temperature=0,
            #     max_tokens=15,
            #     request_timeout=3
            # )['choices'][0]['text'].lower().strip()

            # if "no" in is_english_query:
            #     print('NOT ENGLISH')
            #     return "Sorry, I don't understand. Could you try saying that in a different way?"

            # prompt_text = f"{self.chat_log}{self.restart_sequence}{question.strip()}{self.start_sequence}"
            # print(prompt_text)

            messages = []

            for s in self.chat_log.split('\n'):
                if s == "":
                    continue
                msg = s.split(' ', 1)

                msg[0] = msg[0].strip()
                msg[1] = msg[1].strip()

                messages.append({
                    "role": "user" if msg[0] == self.restart_sequence else "assistant",
                    "content": msg[1]
                })

            messages.append({
                "role": "user",
                "content": question.strip()
            })

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                temperature=0.9,
                presence_penalty=0.6,
                request_timeout=30
            )

            resp_msg = response['choices'][0]['message']
            return resp_msg['content']
            

            # response = openai.Completion.create(
            #     prompt=prompt_text,
            #     stop=[" {}:".format(self.USER), " {}:".format(self.CHATBOT)],
            #     **self.CONFIGS,
            #     request_timeout=10
            # )

            # story = response['choices'][0]['text']
            # answer = str(story).strip().split(self.restart_sequence.rstrip())[0]
        except Exception as e:
            print(f"ERROR: {e}")
            return "Sorry, something went wrong. Can you please try again?"

    def append_interaction_to_chat_log(self, question: str, answer: str) -> str:
            return f"{self.chat_log}\n{self.restart_sequence} {question}\n{self.start_sequence} {answer}".strip()

    def get_conversation(self, end: bool=False, test: bool=False) -> Dict:
        # print("chat_log: ", self.chat_log)
        # print("split: ", "".join([self.prompt, self.CONVO_START]))
        # print("chat_log_clean: ", self.chat_log.split("".join([self.prompt, self.CONVO_START])))
        chat_log_clean = self.chat_log
        dialogs = chat_log_clean.split(self.restart_sequence)

        converation = []

        if test:
            converation.append({
                "from": self.chatbot_name,
                "to": self.WARNING,
                "message": self.prompt,
                "send_time": None
            })

        converation.append({
            "from": self.chatbot_name,
            "to": self.user_name,
            "message": self.BOT_START,
            "send_time": None
        })

        for i in range(1, len(dialogs)):
            messages = dialogs[i].split(self.start_sequence)

            for msg_idx, msg in enumerate(messages):
                if msg_idx == 0:
                    from_idt = self.user_name
                    to_idt = self.chatbot_name
                else:
                    to_idt = self.user_name
                    from_idt = self.chatbot_name

                convo = []
                for text in msg.split("\n"):
                    if len(text) != 0:
                        convo.append({
                            "from": from_idt,
                            "to": to_idt,
                            "message": text.strip(),
                            "send_time": None
                        })
                converation.extend(convo)

        return converation