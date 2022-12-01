from typing import List, Dict, Optional


dialogues = [
    {
        "dialogue_id": "BAP20001",
        "bot_message": "Good morning!",
        "answer": None,
        "jump_to": [
            {
                "condition": None,
                "to": "BAP20002"
            }
        ]
    },
    {
        "dialogue_id": "BAP20002",
        "bot_message": "For the next 15 minutes, I'll talk to you and get to know you better. Let's get started!",
        "answer": None,
        "jump_to": [
            {
                "condition": None,
                "to": "BAP20003"
            }
        ]
    },
    {
        "dialogue_id": "BAP20003",
        "bot_message": "How happy did you feel today?",
        "answer": {
            "type": "likert",
            "choices": [1, 2, 3, 4, 5, 6, 7],
            "description": "7-point Likert scale: 1 (very upset), 7 (very happy)"
        },
        "jump_to": [
            {
                "condition": None,
                "to": "BAP20004"
            }
        ]
    },
    {
        "dialogue_id": "BAP20004",
        "bot_message": "How stressed did you feel today?",
        "answer": {
            "type": "likert",
            "choices": [1, 2, 3, 4, 5, 6, 7],
            "description": "7-point Likert scale: 1 (not stressed), 7 (extremely stressed)"
        },
        "jump_to": [
            {
                "condition": {
                    # If BAP20004 > 4 (stress rating)
                    "gt": 4
                },
                "to": "BAP20008"
            }
        ]
    },
    {
        "dialogue_id": "BAP20008",
        "bot_message": "I'm sorry to hear that you felt stressed out today. For the next 10 minutes, let's practice mindful breathing together to help you calm down, focusing more on your breath and relaxation.",
        "answer": None,
        "jump_to": None
    }
]

"""
This is an Answer Class contains awll of the answer choices and data.
"""
class Answer:
    
    TYPE = "type"
    CHOICES = "choices"
    DESC = "description"

    def __init__(self, answer_information: Dict=None) -> None:

        if not answer_information:
            return
        
        self.type = answer_information.get(self.TYPE, None)
        self.choices = answer_information.get(self.CHOICES, None)
        self.description = answer_information.get(self.DESC, None)
    
    def __str__(self) -> str:

        return f"[ANSWER]: type: {self.type}, choices: {self.choices}, description: {self.description}"
    
    def validate_answer(self, answer: str) -> bool:

        if self.type == "likert":
            if not answer.isnumeric():
                return False

            return int(answer) in self.choices

        return False
    
    def get_answer(self, answer: str):

        if self.type == "likert":

            return float(answer)
        
        return answer
    
    def get_choices(self) -> List:

        return self.choices


"""
This is a Dialog Class contains all of the logics including answer choices, 
dialogue redirections, messages, etcs.
"""
class Dialog:

    ID = "dialogue_id"
    MESSAGE = "bot_message"
    ANSWER = "answer"
    JUMPTO = "jump_to"
    
    def __init__(self, dialogue_information: Dict) -> None:

        if not dialogue_information.get(self.ID, None):
            return

        self.id = dialogue_information.get(self.ID, None)
        self.message = dialogue_information.get(self.MESSAGE, None)
        self.jumpto = dialogue_information.get(self.JUMPTO, None)

        if dialogue_information.get(self.ANSWER, None):
            self.answer = Answer(dialogue_information.get(self.ANSWER, None))
        else:
            self.answer = None
    
    def __str__(self) -> str:

        return self.id

    def get_message(self) -> str:

        return self.mesasge
    
    def get_next_dialogue(self, answer: str) -> Optional[str]:

        if not self.answer or not self.answer.validate_answer(answer):
            return None

        for jump in self.jumpto:
            avaliable_choices = self.answer.get_choices()
            condition = jump.get("condition")
            to = jump.get("to")

            if condition is None:
                return to
            
            # conditions: ["gt", "lt", "gte", "lte", "eqt", "any"]
            for k, v in condition.items():
                if condition[k] == "gt":
                    avaliable_choices = list(filter(lambda value: value > v, avaliable_choices))
                elif condition[k] == "lt":
                    avaliable_choices = list(filter(lambda value: value < v, avaliable_choices))
                elif condition[k] == "gte":
                    avaliable_choices = list(filter(lambda value: value >= v, avaliable_choices))
                elif condition[k] == "lte":
                    avaliable_choices = list(filter(lambda value: value <= v, avaliable_choices))
                elif condition[k] == "eqt":
                    avaliable_choices = list(filter(lambda value: value == v, avaliable_choices))
            
            if self.answer.get_answer(answer) in avaliable_choices:
                return to
        
        return None


"""
This is a DialogCollection Class contains all Dialogs.
"""
class DialogCollection:

    def __init__(self, dialogues: List[Dict]) -> None:
        pass


if __name__ == "__main__":

    dialogues = {
        str(Dialog(dialogues[1])): Dialog(dialogues[1]), 
        str(Dialog(dialogues[2])): Dialog(dialogues[2])
    }
    
    print(dialogues["BAP20002"])
