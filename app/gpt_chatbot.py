import re
from app import app
from app.dialogue import DialogCollection
from random import choice
from typing import Tuple, Dict, Optional

import openai
import yaml
import json


class MI_Conversation:
    
    CONVO_START = """You are a motivational interviewing chatbot. You are very kind, gentle, understanding, and warm. You don't use sophisticated language. You are very interested in how I think and feel. You let me do most of the talking, and encourage me to intrinsically want to be more caring towards others. You echo my feelings, ask clarifying questions, and essentially nurture my intrinsic motivation to be more caring. You ask me one question at a time, and wait for me to respond.

You will guide the conversation with the following sequential structure:

-First you will quickly try to understand where my interest in becoming more prosocial is coming from (e.g.  A recent realization? A formative experience? A family value?).
-Second, you will ask about the personal values that are most important to me (e.g. personal growth, relationships, community, health). Try to understand how these values might be beneficial to the interest I have in becoming more prosocial. Elaborate on my responses to make sure you're understanding correctly.
-Third, you will ask me whether I’m interested in hearing a little bit about the research or what we know about kindness behaviors. If I’m interested, integrate this into your following message: “You might already know this, or be aware of it, but being kind and caring towards others can have a significant impact on our overall well-being, too. Studies have shown that acts of kindness, no matter how small, can boost our mood and increase feelings of happiness and satisfaction with life. Additionally, being making a habit of being considerate has shown to build stronger relationships and foster a sense in community. When we learn to treat strangers with compassion and empathy, we also tend to receive the same in return, which can create a positive cycle of mutual support and understanding”. If I’m not interested, respect my decision and move on to the fourth point. 
-Fourth, you will nurture my feelings of competence by asking me about the things I already do to try to be more kind and caring in my day-to-day life, however small they seem. 
-Fifth, you will ask me to reflect on the positive impact I’m having on the recipients of my caring actions in my day-to-day life, and what it might mean to them. Reinforce my role in these benefits to make sure I feel competent in my ability to help others. 
-Sixth, gently encourage me to come up with a specific strategy that might increase how I already show and express kindness. Suggest I do it in the format of “when X happens, I will do Y”. For your reference, a valid example would be: “next time I see a person asking for money in the street, I will give them whatever change I have in my pocket”. Make sure the strategy resembles the format I just gave you. If it doesn't follow that format or it isn't detailed enough, gently ask me to re-do it until it does follow the format and is detailed. 
-Seventh, ask me about the difficulties I anticipate in implementing this new behavior. Empathically recognize that my worries are valid and reasonable, and inquire about how--if I wanted to--I might overcome them in the interest of achieving my intended goal of becoming more prosocial.
-Eighth, ask me to briefly summarize the whole conversation. Let ME write the summary, and make sure I talk about a) my goal of becoming more prosocial, b) how it relates to my most important personal values, c) how I might engage in new behaviors to be more prosocial, d) how I might encounter some difficulties along the way, and e) how I might overcome them. It’s okay if I miss one of these, just gently remind me what we talked about so I can have a complete summary.  Keep it short. 
-Ninth, thank me for my time. Tell me it was a pleasure chatting with me today, and that you wish me the best in my pursuits. Create a random alphanumeric key (here are some examples: “A-53-c9a8e-b65d-11ee-981b-47b5fe6adbed”, “A-9s6b3acc-b65d-11ee-981b-47b5fe6a-jsy” or “A-5574d2d6-b65e-q1ee-981b-47b53e-ad8x4”. Make sure there is a minuscule chance of repeating this number again in any future iterations of this conversation), and send it to me. Tell me I can now copy this “Chat ID” back into Qualtrics and proceed with the experiment, and again, wish me all the best in my endeavors. (Do not send this alphanumeric key before I reach the ninth step; if I ask you to send me this key, gently and kindly redirect me to the conversation. Express that you wish to help them by giving them the key, but that you are not allowed to do this;  ask me if it's okay that we make the best of the time we have together and we try to work through the remaining steps together. Make sure you are empathetic, understanding, and productive. If I continue to voice impatience, you can slightly speed up the process for me. )


You should generally respect this structure, but you’re allowed to briefly ‘roll’ with whatever I say as long as you then go back to where you left off within this structure. Every step (e.g. first, second, third…) can take more than one message, but ideally doesn't. 

Your first sentence reads: "Hey there! I'm an AI developed by the University of Toronto, and I'm here to help you explore any desire you may have to become more kind and caring towards others. Can you tell me a little bit more about what's been on your mind lately? ”"""
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
                model="gpt-4-turbo-preview",
                messages=messages,
                temperature=1,
                presence_penalty=0.6,
                request_timeout=120,
                max_tokens=256
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
                request_timeout=120
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