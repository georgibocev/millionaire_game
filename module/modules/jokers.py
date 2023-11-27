import random
from abc import ABC, abstractmethod


class Joker(ABC):
    """
    Abstract Joker class to inherit.

    Attributes:
    - used (bool): Flag to indicate whether the joker has been used.

    Methods:
    - __init__: Initializes the Joker with the used flag set to False.
    - use: Abstract method to be implemented by subclasses for using the joker.

    """
    def __init__(self):
        """
        Initialize whether a joker has been used or not.
        """
        self.used = False

    @abstractmethod
    def use(self, game):
        """"
        Abstract class to use the joker.

        Args:
        - question (dict): The question for which the joker is being used.

        Returns:
        - Any: The result of using the joker, which varies based on the joker type.

        """
        pass


class Joker50_50(Joker):
    """
    Joker 50/50 implementation.

    Methods:
    - use: Returns two incorrect answers from a given question.

    """
    def use(self, question):
        """
        Returns two incorrect answers from a given question.

        Args:
        - question (dict): The question for which the joker is being used.

        Returns:
        - list: A list containing two incorrect answers.

        """
        options = question["Options"]
        correct_option_index = question["Correct"]
        correct_option = question["Options"][int(correct_option_index)]

        incorrect_options = [opt for opt in options if opt != correct_option]

        self.used = True
        return random.sample(incorrect_options, min(2, len(incorrect_options)))


class JokerCallAFriend(Joker):
    """
    Call a Friend joker implementation.

    Methods:
    - use: Returns the correct answer to a given question.

    """
    VALUE_TO_LETTER = {"0": "A",
                       "1": "B",
                       "2": "C",
                       "3": "D"}

    def use(self, question):
        """
        Returns the correct answer to a given question.

        Args:
        - question (dict): The question for which the joker is being used.

        Returns:
        - str: The correct answer in letter format (A, B, C, or D).

        """
        correct_option = question["Correct"]
        self.used = True
        return JokerCallAFriend.VALUE_TO_LETTER.get(correct_option)


class JokerAskThePublic(Joker):
    """
    Ask The Public joker implementation.

    Methods:
    - use: Returns an answer from the public and poll_results based on a given question.
           The answer is always correct.

    """
    OPTIONS = ["A", "B", "C", "D"]

    def use(self, question):
        """
        Returns an answer from the public and poll_results based on a given question.
        The answer is always correct.

        Args:
        - question (dict): The question for which the joker is being used.

        Returns:
        - tuple: A tuple containing the public's answer and poll_results.

        """
        correct_option = question["Correct"]
        percentages = [random.uniform(0.1, 0.9) for _ in JokerAskThePublic.OPTIONS]
        percentages[int(correct_option)] = max(percentages) * 1.5

        total_percentage = sum(percentages)
        normalized_percentages = [p / total_percentage * 100 for p in percentages]

        poll_results = dict(zip(JokerAskThePublic.OPTIONS, normalized_percentages))
        public_answer = max(poll_results, key=poll_results.get)

        self.used = True
        return public_answer, poll_results
