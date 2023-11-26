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
        correct_option = question["Correct"]

        incorrect_options = [opt for opt in options if opt != correct_option]
        options_to_remove = random.sample(incorrect_options, min(2, len(incorrect_options)))

        question["Options"] = [opt if opt not in options_to_remove else "" for opt in options]
        self.used = True
        ###this must return the 2 correct answers

class JokerCallAFriend(Joker):
    def use(self, question):
        correct_option = question["Correct"]
        self.used = True
        return correct_option


class JokerAskThePublic(Joker):
    def use(self, question):
        correct_option = question["Correct"]
        options = ["A", "B", "C", "D"]

        percentages = [random.uniform(0.1, 0.9) for _ in options]
        correct_index = options.index(correct_option)
        percentages[correct_index] = max(percentages) * 1.5

        total_percentage = sum(percentages)
        normalized_percentages = [p / total_percentage * 100 for p in percentages]

        poll_results = dict(zip(options, normalized_percentages))
        public_answer = max(poll_results, key=poll_results.get)

        self.used = True
        return public_answer, poll_results
