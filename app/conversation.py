from app import app
from app.dialogue import DialogCollection
from random import choice
from typing import Tuple, Dict, Optional

import openai
import yaml
import json


MESSAGE_START = "\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How are you doing today?"

def _init_prompt_behavior(arm_no: int=0, random: bool=False) -> Dict:
    arm_default = {
        "prompt": "The following is a conversation with a coach. The coach asks open-ended reflection questions and helps the Human develop coping skills. The coach has strong interpersonal skills.",
        "message_start": MESSAGE_START,
        "chatbot": "AI"
    }
    arm_1 = {
        "prompt": "The following is a conversation with a coach. The coach asks open-ended reflection questions and helps the Human develop coping skills. The coach is optimistic, flexible, and empathetic.",
        "message_start": MESSAGE_START,
        "chatbot": "AI"
    }
    arm_2 = {
        "prompt": "The following is a conversation with a coach. The coach asks open-ended reflection questions and helps the Human develop coping skills. The coach is trustworthy, is an active listener, and is empathetic. The coach offers supportive and helpful attention, with no expectation of reciprocity.",
        "message_start": MESSAGE_START,
        "chatbot": "AI"
    }

    if random:
        return choice([arm_default, arm_1, arm_2])
    if arm_no == 1:
        return arm_1
    if arm_no == 2:
        return arm_2
    return arm_default


def _init_prompt_identity(arm_no: int=0, random: bool=False) -> Dict:
    arm_default = {
        "prompt": "The following is a conversation with a coach. The coach asks open-ended reflection questions and helps the Human develop coping skills. The coach has strong interpersonal skills.",
        "message_start": MESSAGE_START,
        "chatbot": "AI"
    }
    arm_1 = {
        "prompt": "The following is a conversation with a friend. The friend asks open-ended reflection questions and helps the Human develop coping skills. The friend has strong interpersonal skills.",
        "message_start": MESSAGE_START,
        "chatbot": "AI"
    }
    arm_2 = {
        "prompt": "The following is a conversation with a mental health professional. The mental health professional asks open-ended reflection questions and helps the Human develop coping skills. The mental health professional has strong interpersonal skills.",
        "message_start": MESSAGE_START,
        "chatbot": "AI"
    }
    
    if random:
        return choice([arm_default, arm_1, arm_2])
    if arm_no == 1:
        return arm_1
    if arm_no == 2:
        return arm_2
    return arm_default


def _init_prompt_field(arm_no: int=0, random: bool=False) -> Dict:
    arms = [
        # arm 0 
        {
            "prompt": "The following is a conversation with a coach. The coach asks open-ended reflection questions and helps the Human develop coping skills. The coach has strong interpersonal skills.",
            "message_start": MESSAGE_START,
            "chatbot": "AI"
        },
        # arm 1
        {
            "prompt": "The following is a conversation with a friend. The friend asks open-ended reflection questions and helps the Human develop coping skills. The friend has strong interpersonal skills.",
            "message_start": MESSAGE_START,
            "chatbot": "AI"
        },
        # arm 2
        {
            "prompt": "The following is a conversation with a coach. The coach helps the Human understand how their thoughts, feelings, and behaviors influence each other. If the Human demonstrates negative thoughts, the coach helps the Human replace them with more realistic beliefs. The coach has strong interpersonal skills.",
            "message_start": MESSAGE_START,
            "chatbot": "AI"
        },
        # arm 3
        {
            "prompt": "The following is a conversation with a friend. The friend helps the Human understand how their thoughts, feelings, and behaviors influence each other. If the Human demonstrates negative thoughts, the friend helps the Human replace them with more realistic beliefs. The friend has strong interpersonal skills.",
            "message_start": MESSAGE_START,
            "chatbot": "AI"
        },
        # arm 4
        {
            "prompt": "The following is a conversation with a coach. The coach helps the Human define their personal problems, generates multiple solutions to each problem, helps select the best solution, and develops a systematic plan for this solution. The coach has strong interpersonal skills.",
            "message_start": MESSAGE_START,
            "chatbot": "AI"
        },
        # arm 5
        {
            "prompt": "The following is a conversation with a friend. The friend helps the Human define their personal problems, generates multiple solutions to each problem, helps select the best solution, and develops a systematic plan for this solution. The friend has strong interpersonal skills.",
            "message_start": MESSAGE_START,
            "chatbot": "AI"
        },
        # arm 6
        {
            "prompt": "The following is a conversation with a coach. The coach asks open-ended reflection questions and helps the Human develop coping skills. The coach is trustworthy, is an active listener, and is empathetic. The coach offers supportive and helpful attention, with no expectation of reciprocity.",
            "message_start": MESSAGE_START,
            "chatbot": "AI"
        },
        # arm 7
        {
            "prompt": "The following is a conversation with a friend. The friend asks open-ended reflection questions and helps the Human develop coping skills. The friend is trustworthy, is an active listener, and is empathetic. The friend offers supportive and helpful attention, with no expectation of reciprocity.",
            "message_start": MESSAGE_START,
            "chatbot": "AI"
        },
        # arm 8
        {
            "prompt": "The following is a conversation with a coach. The coach helps the Human understand how their thoughts, feelings, and behaviors influence each other. If the Human demonstrates negative thoughts, the coach helps the Human replace them with more realistic beliefs. The coach is trustworthy, is an active listener, and is empathetic. The coach offers supportive and helpful attention, with no expectation of reciprocity.",
            "message_start": MESSAGE_START,
            "chatbot": "AI"
        },
        # arm 9
        {
            "prompt": "The following is a conversation with a friend. The friend helps the Human understand how their thoughts, feelings, and behaviors influence each other. If the Human demonstrates negative thoughts, the friend helps the Human replace them with more realistic beliefs. The friend is trustworthy, is an active listener, and is empathetic. The friend offers supportive and helpful attention, with no expectation of reciprocity.",
            "message_start": MESSAGE_START,
            "chatbot": "AI"
        },
        # arm 10
        {
            "prompt": "The following is a conversation with a coach. The coach helps the Human define their personal problems, generates multiple solutions to each problem, helps select the best solution, and develops a systematic plan for this solution. The coach is trustworthy, is an active listener, and is empathetic. The coach offers supportive and helpful attention, with no expectation of reciprocity.",
            "message_start": MESSAGE_START,
            "chatbot": "AI"
        },
        # arm 11
        {
            "prompt": "The following is a conversation with a friend. The friend helps the Human define their personal problems, generates multiple solutions to each problem, helps select the best solution, and develops a systematic plan for this solution. The friend is trustworthy, is an active listener, and is empathetic. The friend offers supportive and helpful attention, with no expectation of reciprocity.",
            "message_start": MESSAGE_START,
            "chatbot": "AI"
        },
        # arm 12
        {
            "prompt": "The following is a conversation with a coach. The coach asks open-ended reflection questions and helps the Human develop coping skills. The coach is optimistic, flexible, and empathetic.",
            "message_start": MESSAGE_START,
            "chatbot": "AI"
        },
        # arm 13
        {
            "prompt": "The following is a conversation with a friend. The friend asks open-ended reflection questions and helps the Human develop coping skills. The friend is optimistic, flexible, and empathetic.",
            "message_start": MESSAGE_START,
            "chatbot": "AI"
        },
        # arm 14
        {
            "prompt": "The following is a conversation with a coach. The coach helps the Human understand how their thoughts, feelings, and behaviors influence each other. If the Human demonstrates negative thoughts, the coach helps the Human replace them with more realistic beliefs. The coach is optimistic, flexible, and empathetic.",
            "message_start": MESSAGE_START,
            "chatbot": "AI"
        },
        # arm 15
        {
            "prompt": "The following is a conversation with a friend. The friend helps the Human understand how their thoughts, feelings, and behaviors influence each other. If the Human demonstrates negative thoughts, the friend helps the Human replace them with more realistic beliefs. The friend is optimistic, flexible, and empathetic.",
            "message_start": MESSAGE_START,
            "chatbot": "AI"
        },
        # arm 16
        {
            "prompt": "The following is a conversation with a coach. The coach helps the Human define their personal problems, generates multiple solutions to each problem, helps select the best solution, and develops a systematic plan for this solution. The coach is optimistic, flexible, and empathetic.",
            "message_start": MESSAGE_START,
            "chatbot": "AI"
        },
        # arm 17
        {
            "prompt": "The following is a conversation with a friend. The friend helps the Human define their personal problems, generates multiple solutions to each problem, helps select the best solution, and develops a systematic plan for this solution. The friend is optimistic, flexible, and empathetic.",
            "message_start": MESSAGE_START,
            "chatbot": "AI"
        }
    ]

    if random:
        return choice(arms)
    if arm_no < len(arms):
        return arms[arm_no]
    return arms[0]


def _init_prompt_mindfulness(arm_no: int=0, random: bool=False) -> Dict:
    arms = [
        # arm 0 
        {
            "prompt": "The following is a conversation with a mindfulness instructor. The mindfulness instructor facilitates knowledge of mindfulness. The mindfulness instructor is trustworthy, is an active listener, and is empathetic. The mindfulness instructor offers supportive and helpful suggestions, with no expectation of reciprocity.",
            "message_start": MESSAGE_START,
            "chatbot": "AI"
        },
        # arm 1
        {
            "prompt": "The following is a conversation with a friend. The friend asks open-ended reflection questions and helps the Human develop mindfulness skills.",
            "message_start": MESSAGE_START,
            "chatbot": "AI"
        },
        # arm 2
        {
            "prompt": "The following is a conversation with a mindfulness instructor. The mindfulness instructor asks open-ended reflection questions and helps the Human develop mindfulness skills. The mindfulness instructor offers supportive and helpful suggestions, with no expectation of reciprocity.",
            "message_start": MESSAGE_START,
            "chatbot": "AI"
        },
        # arm 3
        {
            "prompt": "The following is a conversation with a mindfulness instructor. The mindfulness instructor asks open-ended reflection questions and helps the Human develop mindfulness skills.",
            "message_start": MESSAGE_START,
            "chatbot": "AI"
        },
        # arm 4
        {
            "prompt": "The following is a conversation with a mindfulness instructor. The mindfulness instructor facilitates knowledge of mindfulness. The mindfulness instructor is trustworthy, is an active listener, and is empathetic.",
            "message_start": MESSAGE_START,
            "chatbot": "AI"
        },
        # arm 5
        {
            "prompt": "The following is a conversation with a friend. The friend facilitates knowledge of mindfulness. The friend is trustworthy, is an active listener, and is empathetic. The friend offers supportive and helpful suggestions, with no expectation of reciprocity.",
            "message_start": MESSAGE_START,
            "chatbot": "AI"
        },
        # arm 6
        {
            "prompt": "The following is a conversation with a friend. The friend facilitates knowledge of mindfulness. The friend is trustworthy, is an active listener, and is empathetic.",
            "message_start": MESSAGE_START,
            "chatbot": "AI"
        },
        # arm 7
        {
            "prompt": "The following is a conversation with a friend. The friend asks open-ended reflection questions and helps the Human develop mindfulness skills. The friend offers supportive and helpful suggestions, with no expectation of reciprocity.",
            "message_start": MESSAGE_START,
            "chatbot": "AI"
        }
    ]
    
    if random:
        return choice(arms)
    if arm_no < len(arms):
        return arms[arm_no]
    return arms[0]


def init_prompt(arm_no: int=0, random: bool=False) -> Dict:
    return _init_prompt_field(arm_no, random)


def init_reflection_bot() -> Dict:
    reflection = {
        "prompt": "The following is a conversation with a Mindfulness instructor. The instructor asks open-ended reflection questions to the Human to solidify the Human's understanding of Mindfulness and helps them plan when they can practice Mindfulness in their daily lives. The instructor has a sense of humour, is fair, and empathetic.",
        "message_start": "\n\nHuman: Hello, who are you?\nAI: Hello. I am an AI agent designed to act as your Mindfulness instructor. I am here to help you reflect on your learnings. How can I help you?",
        "chatbot": "AI"
    }

    return reflection


def init_information_bot() -> Dict:
    information = {
        "prompt": "The following is a conversation with a Mindfulness instructor. The instructor teaches and provides information about different mindfulness activities to the Human. The instructor explains different activities clearly and provides examples wherever possible. The instructor has a sense of humour, is fair, and empathetic. ",
        "message_start": "\n\nHuman: Hello, who are you?\nAI: Hello. I am an AI agent designed to act as your Mindfulness instructor. I can answer any questions you might have related to Mindfulness. How can I help you?",
        "chatbot": "AI"
    }

    return information


class Conversation:
    CONVO_START = MESSAGE_START
    BOT_START = "Hello. I am an AI agent designed to help you manage your mood and mental health. How can I help you?"
    USER = "Human"
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


class GPTConversation(Conversation):
    CONFIGS = {
        "engine": "text-davinci-002",
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
        self.start_sequence = f"\n{self.CHATBOT}:"
        self.restart_sequence = f"\n\n{self.USER}: "

        with open('./app/static/secret.yaml') as file:
            secret_keys = yaml.load(file, Loader=yaml.FullLoader)
        openai.api_key = secret_keys["openai"]

    def ask(self, question: str) -> str:
        prompt_text = f"{self.chat_log}{self.restart_sequence}{question}{self.start_sequence}"
        response = openai.Completion.create(
            prompt=prompt_text,
            stop=[" {}:".format(self.USER), " {}:".format(self.CHATBOT)],
            **self.CONFIGS
        )

        story = response['choices'][0]['text']
        answer = str(story).strip().split(self.restart_sequence.rstrip())[0]

        return answer

    def append_interaction_to_chat_log(self, question: str, answer: str) -> str:
            return f"{self.chat_log}{self.restart_sequence}{question}{self.start_sequence} {answer}".strip()

    def get_conversation(self, end: bool=False, test: bool=False) -> Dict:
        print("chat_log: ", self.chat_log)
        print("split: ", "".join([self.prompt, self.CONVO_START]))
        print("chat_log_clean: ", self.chat_log.split("".join([self.prompt, self.CONVO_START])))
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

        if end:
            converation.append({
                "from": self.chatbot_name,
                "to": self.END,
                "message": "This conversation is ended. Your username is the secret key, which you have to paste in the previous survey window.",
                "send_time": None
            })
            converation.append({
                "from": self.chatbot_name,
                "to": self.END,
                "message": "To copy the secret key (i.e. username), you can click the blue button on the bottom left of your screen.",
                "send_time": None
            })

        return converation


class CustomGPTConversation(GPTConversation):
    def __init__(self, user: str, chatbot: str, chat_log: str, prompt: str, default_start: str) -> None:
        super().__init__(user, chatbot, chat_log)

        self.default_start = default_start
        self.prompt = prompt

    def append_interaction_to_chat_log(self, question: str=None, answer: str=None) -> str:
        # restart_sequence/question: user message (opposite) 
        # start_sequence/answer: bot message (self)

        if not question and not answer:
            return self.chat_log

        if question and answer:
            # Construct single turn conversation after performing asking
            self.chat_log = f"{self.chat_log}{self.restart_sequence}{question}{self.start_sequence} {answer}".strip()
            return self.chat_log

        if question:
            # Construct question before performing asking
            self.chat_log = f"{self.chat_log}{self.restart_sequence}{question}".strip()
            return self.chat_log

        # Construct answer after performing asking
        self.chat_log = f"{self.chat_log}{self.start_sequence} {answer}".strip()
        return self.chat_log

    def sync_chat_log(self, chat_log: str) -> None:
        self.chat_log = chat_log
    
    def get_prompt(self) -> str:
        return self.chat_log.split(self.restart_sequence, 1)[0].split(self.start_sequence, 1)[0]

    def get_last_message(self) -> str:
        # Get last message from the user (opposite) in the chat log
        separate_bot_message = self.chat_log.rsplit(self.restart_sequence, 1)

        if len(separate_bot_message) > 1:
            last_turn_msg = separate_bot_message[-1].rsplit(self.start_sequence, 1)[0]
            return last_turn_msg.strip()

        return ''

    def ask(self, question: str=None) -> str:
        if not question:
            prompt_text = f"{self.chat_log}{self.start_sequence}"
        else:
            prompt_text = f"{self.chat_log}{self.restart_sequence}{question}{self.start_sequence}"

        response = openai.Completion.create(
            prompt=prompt_text,
            stop=[" {}:".format(self.USER), " {}:".format(self.CHATBOT)],
            **self.CONFIGS
        )

        story = response['choices'][0]['text']
        answer = str(story).strip().split(self.restart_sequence.rstrip())[0]

        return answer

    def get_conversation(self, end: bool=False, test: bool=False) -> Dict:
        start_text = self.prompt

        chat_log_clean = self.chat_log.split(start_text)[1]

        dialogs = chat_log_clean.split(self.restart_sequence)

        converation = []

        if test:
            converation.append({
                "from": self.chatbot_name,
                "to": self.WARNING,
                "message": self.prompt,
                "send_time": None
            })

        for dialog_msg in dialogs:
            messages = dialog_msg.split(self.start_sequence)

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

        if end:
            converation.append({
                "from": self.chatbot_name,
                "to": self.END,
                "message": "This conversation is ended. Your username is the secret key, which you have to paste in the previous survey window.",
                "send_time": None
            })
            converation.append({
                "from": self.chatbot_name,
                "to": self.END,
                "message": "To copy the secret key (i.e. username), you can click the blue button on the bottom left of your screen.",
                "send_time": None
            })

        return converation


class AutoScriptConversation(Conversation):
    def __init__(self, user: str, chatbot: str, dialogue_path: str, dialogue_answers: Optional[Dict]) -> None:
        super().__init__(user, chatbot)

        self.start_sequence = f"\n{self.CHATBOT}:"
        self.restart_sequence = f"\n\n{self.USER}: "

        with open(f'./app/static/dialogues/{dialogue_path}.json', encoding="utf-8") as file:
            dialogues = json.load(file)

        self.dialogue = DialogCollection(dialogues, answers=dialogue_answers)

    def sync_chat_log(self, chat_log: str, dialogue_id: str) -> Tuple[str, str]:
        if dialogue_id and chat_log:
            curr_id = dialogue_id
            self.dialogue.set_curr_id(curr_id)
            self.chat_log = chat_log
        else:
            curr_id, messages = self.dialogue.move_to_next(show_current=True)
            self.chat_log = "".join([f"{self.start_sequence} {message}" for message in messages])

        return curr_id, self.chat_log

    def give_answer(self, answer: str=None) -> Tuple[str, str]:

        if answer:
            self.chat_log += f"{self.restart_sequence}{answer}"
            self.dialogue.add_answer(answer)

        curr_id, messages = self.dialogue.move_to_next(show_current=False)

        for message in messages:
            self.chat_log += f"{self.start_sequence} {message}"

        return curr_id, self.chat_log

    def get_conversation(self) -> Dict:
        dialogs = self.chat_log.split(self.restart_sequence)

        converation = []

        for dialog_msg in dialogs:
            messages = dialog_msg.split(self.start_sequence)

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
