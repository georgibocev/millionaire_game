import os
import random
import json
import sys


class QuestionGenerator:
    def __init__(self):
        self.used_questions = set()

    def load_question(self, difficulty):

        questions_directory = "questions"
        file_name = f"questions_{difficulty.lower()}.json"
        file_path = os.path.join(questions_directory, file_name)

        try:
            with open(file_path, "r") as file:
                question_data = json.load(file)

                available_questions = [q for q in question_data if q["Question"] not in self.used_questions]

                if available_questions:
                    selected_question = random.choice(available_questions)
                    self.used_questions.add(selected_question["Question"])
                    return selected_question
                else:
                    return None  # if no questions found for difficulty
        except FileNotFoundError:
            print(f"Error: File not found - {file_path}")
            sys.exit(1)
