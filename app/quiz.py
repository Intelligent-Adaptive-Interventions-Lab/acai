import itertools
import random

random.seed(random.randint(0,300))
class Quiz:
    def __init__(self):
        self.index = 0
        self.receiver = ["charity", "self"]
        self.reward = [2,3,4,5]
        self.difficulty = [3,4,6,7]
        self.score = {"charity": 0, "self": 0}
        self.questions = []
        self.log = []
        self.__init_quiz()

    def get_score(self):
        return self.score

    def __correct(self):
        receiver = self.__get_receiver_type()
        self.score[receiver] += self.__get_reward()

    def __generate_answers(self, diff):
        index = random.randint(0, 1)
        answers = [random.sample(range(0, 9), 3), random.sample(range(0, 9), 3)]
        if answers[0] == answers[1]:
            answers[0] = random.sample(range(0, 9), 3)
        org = list(answers[index])
        for i in range(0,3):
            org[i] += diff
            if org[i] >= 10:
                org[i] -= 10
        org.reverse()
        return answers, index, org

    def send_message(self):
        if self.index >= len(self.questions):
            return None
        message = self.questions[self.index]
        return message

    def __init_quiz(self):
        combination = list(itertools.product(self.receiver, self.reward, self.difficulty))
        random.shuffle(combination)
        for receiver, reward, difficulty in combination:
            choice, index, original = self.__generate_answers(difficulty)
            self.questions.append({"receiver": receiver,
                        "reward": reward,
                        "difficulty": difficulty,
                        "choices": choice,
                        "correct_idx": index,
                        "number": original
            })

    def get_message(self, correct):
        question = self.questions[self.index]
        recevier, reward, difficulty, right_idx = question["receiver"], question["reward"], \
                                       question["difficulty"], question["correct_idx"]
        if correct:
            answer = question["choices"][right_idx]
            self.__correct()
        else:
            i = abs(question["correct_idx"] - 1)
            answer = question["choices"][i]
        self.index += 1
        return recevier, reward, difficulty, answer

    def __get_receiver_type(self):
        return self.questions[self.index]["receiver"]

    def __get_reward(self):
        return self.questions[self.index]["reward"]
