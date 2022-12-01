from .models import ChatbotQuestion, NextIDCriteria

questions_motivational = [

    
    ChatbotQuestion(question='Hello [Name]! My name is Alex Miller, I am a local counselor collaborating with the University of Toronto',
    
                    id='BAP20001', criteria=[NextIDCriteria('any', '', 'BAP20002')], has_ans=False),
    
    ChatbotQuestion(question='I understand that the researchers are recruiting people who have expressed some degree of interest in becoming more kind and caring towards others. I was hoping to spend some time with you today and chat about the reasons you are here as well as the kinds of things that you might want to do in the future around becoming more kind and caring.',
    
                    id='BAP20002', criteria=[NextIDCriteria('any', '', 'BAP20003')], has_ans=False),
    
    ChatbotQuestion(question='To start off, could you briefly tell me what led you to participate in this study and elaborate on how important becoming more kind and caring is for you?',
    
                    id='BAP20003', criteria=[NextIDCriteria('any', '', 'BAP20004')], has_ans=True),
    
    ChatbotQuestion(question='I would also like to learn a little bit about your personal values. Just so I understand you a bit better, could you order the following least of values from 1 (most important) to 4 (least importan) and explain why (1) and (2) are the most important? Here are the values: relationships, personal growth, community, health',
    
                    id='BAP20004', criteria=[NextIDCriteria('any', '', 'BAP20005')], has_ans=True),
    
    ChatbotQuestion(question='Tell me a little about the ways in which you see being more kind and caring as beneficial towards [TopValue]?', id='BAP20005', criteria=[
    
                    NextIDCriteria('any', '', 'BAP20006')], has_ans=True),
    
    ChatbotQuestion(question='Thank you for sharing that, [Name]. Would you be interested in hearing a little bit about the research or what we know about kindness behaviors?', id='BAP20006', criteria=[
    
                    NextIDCriteria('eqs', 'yes', 'BAP20007'), NextIDCriteria('eqs', 'no', 'BAP20008b')], has_ans=True),  # TODO: right now, needs to be exactly "yes". can't be "y", "Yes", etc.
    
    ChatbotQuestion(question='You might already know this, or be aware of it, but… [info goes here]', id='BAP20007', criteria=[
                    NextIDCriteria('any', '', 'BAP20008a')], has_ans=False),
    
    ChatbotQuestion(question='With this information in mind, I was wondering if it would be ok to switch gears a little bit and focus on what you already do regarding being kind and caring as well as other things you might want to try in the future.. What do you already do regarding being kind and caring? How (if at all) do you think doing these things impacts others?',
                    id='BAP20008a', criteria=[NextIDCriteria('any', '', 'BAP20009')], has_ans=True),
    
    ChatbotQuestion(question='In this case, I wonder if it would be ok to switch gears a little bit and focus on what you already do regarding being kind and caring as well as other things you might want to try in the future.. What do you already do regarding being kind and caring? How (if at all) do you think doing these things impacts others?',
                    id='BAP20008b', criteria=[NextIDCriteria('any', '', 'BAP20009')], has_ans=True),
    
    ChatbotQuestion(question='What might you do to increase how you already show kindness and caring? In your current day-to-day life, what are one or two things you could do to help others?',
                    id='BAP20009', criteria=[NextIDCriteria('any', '', 'BAP20010a')], has_ans=True),
    
    ChatbotQuestion(question='Some ideas might involve being friendly to strangers, donating something you don\'t use, or buying food for a homeless person. Are any of these things you would be willing to try in your dat-to-day life?',
                    id='BAP2009b', criteria=[NextIDCriteria('eqs', 'yes', 'BAP20010a'), NextIDCriteria('eqs', 'no', 'BAP20009c')], has_ans=True),
    
    ChatbotQuestion(question='Other options involve being patient with strangers, and expressing love or appreciation to friends and family.',
                    id='BAP20009c', criteria=[NextIDCriteria('any', '', 'BAP20010b')], has_ans=False),  # TODO: go to next option randomly
    
    ChatbotQuestion(question='That’s great! Perhaps you might already know this, but behavior is more likely to stick when we come up with concrete, if-then plans to make it happen. An example would be, “If I see a person in need, then I will give them whatever change I have in my pocket up to 1$”. Out of the things you just said that you could do to help others, which one suits you the best? What might be your if-then plan?',
                    id='BAP20010a', criteria=[NextIDCriteria('containslist', 'if,then', 'BAP20011a'), NextIDCriteria('any', '', 'BAP20011b')], has_ans=True),
    
    ChatbotQuestion(question='Perhaps you might already know this, but behavior is more likely to stick when we come up with concrete, if-then plans to make it happen. An example would be, “If I see a person in need, then I will give them whatever change I have in my pocket up to 1$”. Out of the things one could do to help others we just discussed, which one suits you the best? What might be your if-then plan?',
                    id='BAP20010b', criteria=[NextIDCriteria('containslist', 'if,then', 'BAP20011a'),NextIDCriteria('any', '', 'BAP20011b')], has_ans=True),
    
    ChatbotQuestion(question='That sounds great! What might be some obstacles when implementing this plan, if any? What might be a way that you could deal with them?',
                    id='BAP20011a', criteria=[NextIDCriteria('any', '', 'BAP20012')], has_ans=True),
    
    ChatbotQuestion(question='It is important to create a plan that reminds you what to do when something specific happens. For example, if I wanted to be more friendly to strangers, I\'d say something like "*if* I make eye contact with a stranger, *then* I will smile at them". What might be your if-then plan?',
                    id='BAP20011b', criteria=[NextIDCriteria('containslist', 'if,then', 'BAP20011a'), NextIDCriteria('any', '', 'BAP20011b')], has_ans=True),
    
    ChatbotQuestion(question='Thinking of obstacles can be a little intimidating, but those feelings are completely normal. Remember that being more kind and caring can help you with [MaxValue]!', id='BAP20012', criteria=[
                    NextIDCriteria('any', '', 'BAP20013')], has_ans=False),
    
    ChatbotQuestion(question='To close off, I was wondering if you could summarize what we’ve talked about? What stands out to you regarding your values, the behaviors you plan to implement to act with kindness and caring, and the way you plan to overcome any potential obstacles?',
                    id='BAP20013', criteria=[NextIDCriteria('any', '', 'BAP20014')], has_ans=True),
    
    # TODO: What to do after last question
    ChatbotQuestion(question='Thank you very much, [Name]! It’s been a pleasure chatting with you today. I hope you found this conversation useful, and I wish you all the best with your plan to achieve your goals!', id='BAP20014', criteria=[
                    NextIDCriteria('any', '', 'BAP20014')], has_ans=False),


]


# questions_mindfulness = [
#     ChatbotQuestion(question='Good morning, [Name]!', id='BAP20001', criteria=[
#                     NextIDCriteria('any', '', 'BAP20002')]),
#     ChatbotQuestion(question='For the next 15 minutes, I\'ll talk to you and get to know you better. Let\'s get started!',
#                     id='BAP20002', criteria=[NextIDCriteria('any', '', 'BAP20003')]),
#     ChatbotQuestion(question='How happy did you feel today?', id='BAP20003', criteria=[
#                     NextIDCriteria('any', '', 'BAP20004')]),
#     ChatbotQuestion(question='How stressed did you feel today?',
#                     id='BAP20004', criteria=[NextIDCriteria('any', '', 'BAP20005')]),
#     ChatbotQuestion(question='How satisfied or content did your life feel today?',
#                     id='BAP20005', criteria=[NextIDCriteria('any', '', 'BAP20006')]),
#     ChatbotQuestion(question='Right now, to what extent are you aware of your thoughts and emotions?',
#                     id='BAP20006', criteria=[NextIDCriteria('any', '', 'BAP20007')]),
#     ChatbotQuestion(question='Right now, to what extent do you wish you could change how you feel?',
#                     id='BAP20007', criteria=[NextIDCriteria('less', '', 'BAP20002')]),
#     ChatbotQuestion(question='I\'m sorry to hear that you felt stressed out today. For the next 10 minutes, let\'s practice mindful breathing together to help you calm down, focusing more on your breath and relaxation. ',
#                     id='BAP20008', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
#     ChatbotQuestion(question='Mindful Breathing video ', id='BAP20010', criteria=[
#                     NextIDCriteria('any', '', 'BAP20002')]),
#     ChatbotQuestion(question='Based on your score, it seems that our awareness activities might be helpful. Which activity sounds more interesting to you? Mindful Breathing, Body Scan, or Mindful Eating?',
#                     id='BAP20011', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
#     ChatbotQuestion(question='Ok! Let\'s practice Mindful Breathing together. [Mindful breathing video]', id='BAP20012a', criteria=[
#                     NextIDCriteria('any', '', 'BAP20002')]),
#     ChatbotQuestion(question='Ok! Let\'s practice Body Scan together. [Body Scan video]', id='BAP20012b', criteria=[
#                     NextIDCriteria('any', '', 'BAP20002')]),
#     ChatbotQuestion(question='Ok! Let\'s practice Mindful Eating together. [Mindful Eating video]', id='BAP20012c', criteria=[
#                     NextIDCriteria('any', '', 'BAP20002')]),
#     ChatbotQuestion(question='Based o\n your score, it seems that our reappraisal activities might be helpful. Which activity sounds more interesting to you? Yes to Life, Gratitude, or Loving and Kindness?',
#                     id='BAP20013', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
#     ChatbotQuestion(question='Ok! Let\'s practice Yes to Life together. [Yes to Life video]', id='BAP20014a', criteria=[
#                     NextIDCriteria('any', '', 'BAP20002')]),
#     ChatbotQuestion(question='Ok! Let\'s practice Gratitude together. [Gratitude video]', id='BAP20014b', criteria=[
#                     NextIDCriteria('any', '', 'BAP20002')]),
#     ChatbotQuestion(question='Ok! Let\'s practice Loving and Kindness together. [Loving and Kindness video]', id='BAP20014c', criteria=[
#                     NextIDCriteria('any', '', 'BAP20002')]),
#     ChatbotQuestion(question='Based o\n your score, it seems that our acceptance activities might be helpful. Which activity sounds more interesting to you? Sensory Awareness, Leaves on the Stream, or Ball in a Pool?',
#                     id='BAP20015', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
#     ChatbotQuestion(question='Ok! Let\'s practice Leaves on the Stream together. [Leaves on the Stream video]', id='BAP20016a', criteria=[
#                     NextIDCriteria('any', '', 'BAP20002')]),
#     ChatbotQuestion(question='Ok! Let\'s practice Ball in the Pool together. [Ball in the Pool video]', id='BAP20016b', criteria=[
#                     NextIDCriteria('any', '', 'BAP20002')]),
#     ChatbotQuestion(question='Ok! Let\'s practice Sensory Awareness together. [Sensory Awareness video]', id='BAP20016c', criteria=[
#                     NextIDCriteria('any', '', 'BAP20002')]),
#     ChatbotQuestion(question='How much did you like today\'s video?',
#                     id='BAP20017', criteria=[NextIDCriteria('any', '', 'BAP20002')]),
#     ChatbotQuestion(question='Thank you for chatting with me today!',
#                     id='BAP20018', criteria=[NextIDCriteria('any', '', 'BAP20002')]),


# ]

def get_chatbot_question_by_id(id: str) -> ChatbotQuestion:
    for q in questions_motivational:
        if q.id == id:
            return q
        
def get_chatbot_question_by_msg(msg: str) -> ChatbotQuestion:
    for q in questions_motivational:
        if q.question == msg:
            return q