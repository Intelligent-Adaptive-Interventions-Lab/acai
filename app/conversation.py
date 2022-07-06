from dotenv import load_dotenv
from random import choice
import os
import openai

from typing import Dict, overload

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
completion = openai.Completion()

MESSAGE_START = "\n\nPerson: Hello, who are you?\nAI: I am an AI created by OpenAI. How are you doing today?"

def init_prompt(arm_no: int=0, random: bool=False) -> Dict:
    arm_default = {
        "prompt": "The following is a conversation with a counselor. The counselor helps the Human by asking lots of reflection prompts. The counselor is empathetic, trustworthy, and is an active listener.",
        "message_start": MESSAGE_START,
        "chatbot": "AI"
    }
    arm_1 = {
        "prompt": "The following is a conversation with a counselor. The counselor has strong interpersonal skills.",
        "message_start": MESSAGE_START,
        "chatbot": "AI"
    }
    arm_2 = {
        "prompt": "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.",
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


class Conversation:
    CONVO_START = MESSAGE_START
    BOT_START = "Hello. I am an AI agent designed to help you manage your mood and mental health. How can I help you?"
    USER = "Person"
    CHATBOT = "AI"
    WARNING = "Warning"
    END = "End"
    NOTI = "Notification"
    
    def __init__(self, user: str, chatbot: str, chat_log: str) -> None:
        self.user_name = user
        self.chatbot_name = chatbot
        self.chat_log = chat_log
        self.prompt = chat_log.split(self.CONVO_START)[0]
    
    def get_user(self) -> str:
        return self.user_name
    
    def get_chatbot(self) -> str:
        return self.chatbot_name
    
    def get_conversation(self, end: bool=False, test: bool=False) -> Dict:
        chat_log_clean = self.chat_log.split("".join([self.prompt, self.CONVO_START]))[1]
        dialogs = chat_log_clean.split("\n\n")
        
        converation = []
        converation.append({
            "from": self.chatbot_name,
            "to": self.user_name,
            "message": self.BOT_START,
            "send_time": None
        })

        for i in range(1, len(dialogs)):
            messages = dialogs[i].split("\n")
            
            for message in messages:
                identifier_message = message.split(":")
                from_identity = identifier_message[0].strip()
                convo_message = identifier_message[1].strip()
                
                if from_identity == self.USER:
                    convo = {
                        "from": self.user_name,
                        "to": self.chatbot_name,
                        "message": convo_message,
                        "send_time": None
                    }
                else:
                    convo = {
                        "from": self.chatbot_name,
                        "to": self.user_name,
                        "message": convo_message,
                        "send_time": None
                    }

                converation.append(convo)
        
        return converation


class GPTConversation(Conversation):
    CONFIGS = {
        "engine": "text-davinci-002",
        "temperature": 0.9,
        "max_tokens": 150,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0.6,
    }
    
    def __init__(self, user: str, chatbot: str, chat_log: str) -> None:
        super().__init__(user, chatbot, chat_log)
        
        self.start_sequence = f"\n{self.CHATBOT}:"
        self.restart_sequence = f"\n\n{self.USER}: "
    
    def ask(self, question: str) -> str:
        prompt_text = f"{self.chat_log}{self.restart_sequence}{question}{self.start_sequence}"
        response = openai.Completion.create(
            prompt=prompt_text,
            stop=[" {}:".format(self.USER), " {}:".format(self.CHATBOT)],
            **self.CONFIGS
        )
        
        story = response['choices'][0]['text']
        
        answer = str(story).strip().split(self.restart_sequence)[0]
        
        return answer
    
    def append_interaction_to_chat_log(self, question: str, answer: str) -> str:
            return f"{self.chat_log}{self.restart_sequence}{question}{self.start_sequence} {answer}".strip()
    
    def get_conversation(self, end: bool=False, test: bool=False) -> Dict:
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
            
            for msg_idx in range(len(messages)):
                if msg_idx == 0:
                    from_idt = self.user_name
                    to_idt = self.chatbot_name
                else:
                    to_idt = self.user_name
                    from_idt = self.chatbot_name
                
                convo = []
                for text in messages[msg_idx].split("\n"):
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
        
