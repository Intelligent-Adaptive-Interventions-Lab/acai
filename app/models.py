from typing import List

class NextIDCriteria:
    """Conditions for answer to lead to question with certain id
    
    === Attributes ===
    compared_method: Method in which to compare
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
    has_ans: If thi
    
    """
    def __init__(self, id: str, criteria: List[NextIDCriteria], question: str) -> None:
        self.id = id
        self.criteria = criteria
        self.question = question
    
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
            # go to the same id no matter what the answer is
            elif (c.compared_method == "any"):
                    return c.nextid
        return "invalid answer"
        
        
questions_motivational = [
ChatbotQuestion(question='Hello [Name]! My name is Alex Miller, I am a local counselor collaborating with the University of Toronto', id='BAP20001', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='I understand that the researchers are recruiting people who have expressed some degree of interest in becoming more kind and caring towards others. I was hoping to spend some time with you today and chat about the reasons you are here as well as the kinds of things that you might want to do in the future around becoming more kind and caring.', id='BAP20002', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='To start off, could you briefly tell me what led you to participate in this study and elaborate on how important becoming more kind and caring is for you?', id='BAP20003', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='I would also like to learn a little bit about your personal values. Just so I understand you a bit better, could you order the following least of values from 1 (most important) to 4 (least importan) and explain why (1) and (2) are the most important? Here are the values: relationships, personal growth, community, health', id='BAP20004', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='Tell me a little about the ways in which you see being more kind and caring as beneficial towards [TopValue]?', id='BAP20005', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='Thank you for sharing that, [Name]. Would you be interested in hearing a little bit about the research or what we know about kindness behaviors?', id='BAP20006', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='nan', id='nan', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='You might already know this, or be aware of it, but… [info goes here]', id='BAP20007', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='With this information in mind, I was wondering if it would be ok to switch gears a little bit and focus on what you already do regarding being kind and caring as well as other things you might want to try in the future.. What do you already do regarding being kind and caring? How (if at all) do you think doing these things impacts others?', id='BAP20008a', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='In this case, I wonder if it would be ok to switch gears a little bit and focus on what you already do regarding being kind and caring as well as other things you might want to try in the future.. What do you already do regarding being kind and caring? How (if at all) do you think doing these things impacts others?', id='BAP20008b', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='What might you do to increase how you already show kindness and caring? In your current day-to-day life, what are one or two things you could do to help others?', id='BAP20009', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='Some ideas might involve being friendly to strangers, donating something you don\'t use, or buying food for a homeless person. Are any of these things you would be willing to try in your dat-to-day life?', id='BAP2009b', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='nan', id='nan', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='Other options involve being patient with strangers, and expressing love or appreciation to friends and family.', id='BAP20009c', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='That’s great! Perhaps you might already know this, but behavior is more likely to stick when we come up with concrete, if-then plans to make it happen. An example would be, “If I see a person in need, then I will give them whatever change I have in my pocket up to 1$”. Out of the things you just said that you could do to help others, which one suits you the best? What might be your if-then plan?', id='BAP20010a', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='Perhaps you might already know this, but behavior is more likely to stick when we come up with concrete, if-then plans to make it happen. An example would be, “If I see a person in need, then I will give them whatever change I have in my pocket up to 1$”. Out of the things one could do to help others we just discussed, which one suits you the best? What might be your if-then plan?', id='BAP20010b', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='That sounds great! What might be some obstacles when implementing this plan, if any? What might be a way that you could deal with them?', id='BAP20011a', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='It is important to create a plan that reminds you what to do when something specific happens. For example, if I wanted to be more friendly to strangers, I\'d say something like "*if* I make eye contact with a stranger, *then* I will smile at them". What might be your if-then plan?', id='BAP20011b', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='Thinking of obstacles can be a little intimidating, but those feelings are completely normal. Remember that being more kind and caring can help you with [MaxValue]!', id='BAP20012', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='To close off, I was wondering if you could summarize what we’ve talked about? What stands out to you regarding your values, the behaviors you plan to implement to act with kindness and caring, and the way you plan to overcome any potential obstacles?', id='BAP20013', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='Thank you very much, [Name]! It’s been a pleasure chatting with you today. I hope you found this conversation useful, and I wish you all the best with your plan to achieve your goals!', id='BAP20014', criteria=[NextIDCriteria('any', '', 'BAP20002')]),

]


questions_mindfulness = [
ChatbotQuestion(question='nan', id='BAP20000', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='Good morning, [Name]!', id='BAP20001', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='For the next 15 minutes, I\'ll talk to you and get to know you better. Let\'s get started!', id='BAP20002', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='How happy did you feel today?', id='BAP20003', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='How stressed did you feel today?', id='BAP20004', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='How satisfied or content did your life feel today?', id='BAP20005', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='Right now, to what extent are you aware of your thoughts and emotions?', id='BAP20006', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='Right now, to what extent do you wish you could change how you feel?', id='BAP20007', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='I\'m sorry to hear that you felt stressed out today. For the next 10 minutes, let\'s practice mindful breathing together to help you calm down, focusing more on your breath and relaxation. ', id='BAP20008', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='Mindful Breathing video ', id='BAP20010', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='Based on your score, it seems that our awareness activities might be helpful. Which activity sounds more interesting to you? Mindful Breathing, Body Scan, or Mindful Eating?', id='BAP20011', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='Ok! Let\'s practice Mindful Breathing together. [Mindful breathing video]', id='BAP20012a', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='Ok! Let\'s practice Body Scan together. [Body Scan video]', id='BAP20012b', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='Ok! Let\'s practice Mindful Eating together. [Mindful Eating video]', id='BAP20012c', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='Based o\n your score, it seems that our reappraisal activities might be helpful. Which activity sounds more interesting to you? Yes to Life, Gratitude, or Loving and Kindness?', id='BAP20013', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='Ok! Let\'s practice Yes to Life together. [Yes to Life video]', id='BAP20014a', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='Ok! Let\'s practice Gratitude together. [Gratitude video]', id='BAP20014b', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='Ok! Let\'s practice Loving and Kindness together. [Loving and Kindness video]', id='BAP20014c', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='Based o\n your score, it seems that our acceptance activities might be helpful. Which activity sounds more interesting to you? Sensory Awareness, Leaves on the Stream, or Ball in a Pool?', id='BAP20015', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='Ok! Let\'s practice Leaves on the Stream together. [Leaves on the Stream video]', id='BAP20016a', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='Ok! Let\'s practice Ball in the Pool together. [Ball in the Pool video]', id='BAP20016b', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='Ok! Let\'s practice Sensory Awareness together. [Sensory Awareness video]', id='BAP20016c', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='How much did you like today\'s video?', id='BAP20017', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
ChatbotQuestion(question='Thank you for chatting with me today!', id='BAP20018', criteria=[NextIDCriteria('any', '', 'BAP20002')]),

    
]


  
# Example      
# prompt1
# {<=, 3, idA}
# {==, 5, idB}
# ==, "y", idC

# prompt2
# 'any', '', idD
