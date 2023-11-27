import os
import random
import json
import sys


class QuestionGenerator:
    """
    Generates questions from a JSON file.

    Attributes:
    - used_questions (set): A set to keep track of already generated questions to avoid repetition.

    Methods:
    - __init__: Initializes the QuestionGenerator with an empty set for used questions.
    - load_question: Loads a question based on the given difficulty.

    """
    def __init__(self):
        """
        Initialize a set to keep track of the already generated questions in order to avoid repetition.
        """
        self.used_questions = set()

    def load_question(self, difficulty):
        """
        Loads a question based on a given difficulty.

        Args:
        - difficulty (str): The difficulty level for the question.

        Returns:
        - dict: The loaded question data.
        """
        questions_directory = os.path.abspath("questions/")
        file_name = f"questions_{difficulty.lower()}.json"
        file_path = os.path.join(questions_directory, file_name)

        try:
            with open(file_path, "r") as file:
                question_data = json.load(file)

                available_questions = [q for q in question_data if q["Question"] not in self.used_questions]

                if available_questions:
                    random.shuffle(available_questions)
                    selected_question = random.choice(available_questions)
                    self.used_questions.add(selected_question["Question"])
                    return selected_question
                else:
                    print(f"Error: No available questions found.")
                    sys.exit(1)
        except FileNotFoundError:
            print(f"Error: File not found - {file_path}")
            sys.exit(1)
