from __future__ import annotations
from typing import List, Dict

class NextIDCriteria:
    """Conditions for answer to lead to question with certain id

    === Attributes ===
    compared_method: Method in which to compare
        - "eqs": answer == compared value
        - "less" answer < compared value
        - "greater" answer > compared value
        - "contains" answer contains compared value
        - "any" any answer
    compared_value: Value to compare userinput to (using the given method)
    nextid: The id it would go to if this is true
    """

    def __init__(self, compared_method: str, compared_value: list, nextid: str) -> None:
        self.compared_method = compared_method
        self.compared_value = compared_value
        self.nextid = nextid


class ChatbotQuestion:
    """ A question the chatbot asks the user

    === Attributes ===
    id: This question's ID number.
    criteria: List of criteria to compare answer with and to determine nextID
    question: The question that the chatbot asks
    has_ans: If this chatbot waits for answer

    """

    def __init__(self, id: str, criteria: Dict[ChatbotQuestion, NextIDCriteria], question: str, has_ans: bool) -> None:
        self.id = id
        self.criteria = criteria
        self.question = question
        self.has_ans = has_ans

    def get_nextid(self, user_answer: str) -> str:
        """
        Returns nextID by checking which criteria it matches for the question's list of NextIDCriteria
        If the user answer matches a criteria, it returns the next id associated with that criteria
        """

        for c in self.criteria:
            # if user answer equals this value, go to this id
            if (c.compared_method == "eqs"):
                if (user_answer == c.compared_value):
                    return c.nextid
            # if user answer is smaller than the value, go to this id
            elif (c.compared_method == "less"):
                if (user_answer < c.compared_value):
                    return c.nextid
            elif (c.compared_method == "containslist"):
                clist = c.compared_value.split(",")
                containsall = True
                for i in clist:
                    if (i not in user_answer):
                        containsall = False
                if containsall:
                    return c.nextid
            # go to the same id no matter what the answer is
            elif (c.compared_method == "any"):
                return c.nextid
        return "invalid answer"
