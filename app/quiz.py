import itertools
import random

random.seed(random.randint(0, 300))
class Quiz:
    def __init__(self):
        self.index = 0
        self.receiver = ["charity", "self"]
        self.reward = [2, 3, 4, 5]
        self.difficulty = [3, 4, 6, 7]
        self.score = {"charity": 0, "self": 0}
        self.questions = []
        self.log = []
        self.__init_quiz()
    def get_questions(self):
        return self.questions

    def __init_quiz(self):
        combination = list(
            itertools.product(self.receiver, self.reward, self.difficulty))
        random.shuffle(combination)
        for receiver, reward, difficulty in combination:
            choice, index, original = self.__generate_answers(difficulty)
            self.questions.append({"receiver": receiver,
                                   "reward": reward,
                                   "difficulty": difficulty,
                                   "choices": choice,
                                   "correct_idx": str(index),
                                   "number": original
                                   })
    def __generate_answers(self, diff):
        index = random.randint(0, 1)
        answers = [random.sample(range(0, 9), 3), random.sample(range(0, 9), 3)]
        if answers[0] == answers[1]:
            answers[0] = random.sample(range(0, 9), 3)
        org = list(answers[index])
        for i in range(0, 3):
            org[i] -= diff
            if org[i] < 0:
                org[i] += 10
        # org.reverse()
        return answers, index, org


class QuizUtility:
    def __init__(self, idx, questions, score):
        self.current_idx = idx
        self.questions = questions
        self.score = score

    def get_score(self):
        return self.score

    def correct(self, amount):
        receiver = self.__get_receiver_type()
        self.score[receiver] += amount

    def send_message(self):
        if self.current_idx >= len(self.questions):
            return None
        message = self.questions[self.current_idx]
        return message

    def get_message(self, correct, amount=0):
        question = self.questions[self.current_idx]
        recevier, reward, difficulty, right_idx = question["receiver"], \
                                                  question["reward"], \
                                                  question["difficulty"], int(
            question["correct_idx"])
        if correct:
            answer = question["choices"][right_idx]
            self.correct(amount)
        else:
            i = abs(int(question["correct_idx"]) - 1)
            answer = question["choices"][i]
        return self.current_idx, recevier, difficulty, reward, answer, amount

    def __get_receiver_type(self):
        return self.questions[self.current_idx]["receiver"]

