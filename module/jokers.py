import random
from abc import ABC, abstractmethod


class Joker(ABC):
    def __init__(self):
        self.used = False

    @abstractmethod
    def use(self, game):
        pass


class Joker50_50(Joker):
    def use(self, question):
        options = question["Options"]
        correct_option_index = question["Correct"]
        correct_option = question["Options"][int(correct_option_index)]

        incorrect_options = [opt for opt in options if opt != correct_option]

        self.used = True
        return random.sample(incorrect_options, min(2, len(incorrect_options)))


class JokerCallAFriend(Joker):
    VALUE_TO_LETTER = {"0": "A",
                       "1": "B",
                       "2": "C",
                       "3": "D"}

    def use(self, question):
        correct_option = question["Correct"]
        self.used = True
        return JokerCallAFriend.VALUE_TO_LETTER.get(correct_option)


class JokerAskThePublic(Joker):
    OPTIONS = ["A", "B", "C", "D"]

    def use(self, question):
        correct_option = question["Correct"]
        percentages = [random.uniform(0.1, 0.9) for _ in JokerAskThePublic.OPTIONS]
        percentages[int(correct_option)] = max(percentages) * 1.5

        total_percentage = sum(percentages)
        normalized_percentages = [p / total_percentage * 100 for p in percentages]

        poll_results = dict(zip(JokerAskThePublic.OPTIONS, normalized_percentages))
        public_answer = max(poll_results, key=poll_results.get)

        self.used = True
        return public_answer, poll_results
