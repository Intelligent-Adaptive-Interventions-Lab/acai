from typing import List, Dict, Optional, Tuple

import json

class Answer:
    """
    This is an Answer Class contains awll of the answer choices and data.
    """
    
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

    def validate_answer(self, answer: str=None) -> bool:

        if self.type == "likert":
            if not answer or not answer.isnumeric():
                return False

            return int(answer) in self.choices

        return True

    def get_answer(self, answer: str=None):

        if self.type == "likert":

            return float(answer)

        return answer

    def get_choices(self) -> List:

        return self.choices

    def get_description(self) -> str:

        return self.description


class Dialog:
    """
    This is a Dialog Class contains all of the logics including answer choices, 
    dialogue redirections, messages, etcs.
    """

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

    def get_message(self) -> List[str]:

        messages = [self.message]
        if self.answer:
            messages.append(self.answer.get_description())

        return messages

    def get_answer(self) -> Optional[Answer]:

        return self.answer

    def get_next_dialogue(self, answer: str=None) -> Optional[str]:

        if self.answer and not self.answer.validate_answer(answer):
            return None

        if not self.jumpto:
            return None

        for jump in self.jumpto:
            condition = jump.get("condition")
            next_id = jump.get("to")

            if not condition or not self.answer:
                return next_id

            avaliable_choices = self.answer.get_choices()
            # conditions: ["gt", "lt", "gte", "lte", "eqt", "any"]
            for k, v in condition.items():
                if k == "gt":
                    avaliable_choices = list(filter(lambda value: value > v, avaliable_choices))
                elif k == "lt":
                    avaliable_choices = list(filter(lambda value: value < v, avaliable_choices))
                elif k == "gte":
                    avaliable_choices = list(filter(lambda value: value >= v, avaliable_choices))
                elif k == "lte":
                    avaliable_choices = list(filter(lambda value: value <= v, avaliable_choices))
                elif k == "eqt":
                    avaliable_choices = list(filter(lambda value: value == v, avaliable_choices))
            
            print(f"AVALIABLE CHOICES: {avaliable_choices}")

            if self.answer.get_answer(answer) in avaliable_choices:
                return next_id

        return None


class DialogCollection:
    """
    This is a DialogCollection Class contains all Dialogs.
    """

    def __init__(self, dialogues: List[Dict]) -> None:
        self.dialogues = {}

        for d in dialogues:
            self.dialogues[d.get("dialogue_id")] = Dialog(d)

        self.curr_id = dialogues[0].get("dialogue_id")
    
    def start(self) -> Tuple[str, List[str]]:
        messages = self.get_curr_messages()
        while self.dialogues[self.curr_id].get_answer() is None:
            next_id = self.dialogues[self.curr_id].get_next_dialogue()
            if not next_id or next_id not in list(self.dialogues.keys()):
                return self.curr_id, messages

            self.curr_id = next_id
            messages += self.get_curr_messages()

        return self.curr_id, messages

    def move_to_next_question(self, answer: str=None) -> Tuple[str, List[str]]:
        answer_validation = self.dialogues[self.curr_id].get_answer()
        if answer_validation and not answer_validation.validate_answer(answer):
            return self.curr_id, ["I don't understand your answer.", answer_validation.get_description()]

        next_id = self.dialogues[self.curr_id].get_next_dialogue(answer)

        print(f"NEXT ID: {next_id}")
        if not next_id or next_id not in list(self.dialogues.keys()):
            return self.curr_id, []

        self.curr_id = next_id
        messages = self.get_curr_messages()
        while self.dialogues[self.curr_id].get_answer() is None:
            next_id = self.dialogues[self.curr_id].get_next_dialogue()
            if not next_id or next_id not in list(self.dialogues.keys()):
                return self.curr_id, messages

            self.curr_id = next_id
            messages += self.get_curr_messages()

        return self.curr_id, messages

    def get_num_dialogues(self) -> int:

        return len(self.dialogues.items())

    def get_curr_id(self) -> str:

        return self.curr_id

    def get_curr_messages(self) -> List[str]:

        return self.dialogues[self.curr_id].get_message()

    def set_curr_id(self, id: str) -> None:

        self.curr_id = id


if __name__ == "__main__":

    with open('./static/dialogues/mindfulness.json') as file:
        curr_dialogues = json.load(file)

    dialog_collection = DialogCollection(curr_dialogues)

    print(dialog_collection.start())
    # print(dialog_collection.move_to_next_question())
    # print(dialog_collection.move_to_next_question())
    # print(dialog_collection.move_to_next_question(answer="7"))
    # print(dialog_collection.move_to_next_question(answer="8"))
    # print(dialog_collection.move_to_next_question(answer="1"))
