import os
import random


class QuestionGenerator:
    def __init__(self):
        self.questions = []
        self.used_questions = set()

    def load_question(self, difficulty):

        questions_directory = "questions"
        file_name = f"questions_{difficulty.lower()}.txt"
        file_path = os.path.join(questions_directory, file_name)

        try:
            with open(file_path, "r") as file:
                questions = []
                current_question = None
                options = []

                for line in file:
                    line = line.strip()

                    if line.startswith("Category:"):
                        current_question = {"Category": line.split(":")[1].strip()}
                    elif line.startswith("Difficulty:"):
                        current_question["Difficulty"] = line.split(":")[1].strip()
                    elif line.startswith("Question:"):
                        current_question["Question"] = line.split(":")[1].strip()
                    elif line.startswith("A:"):
                        options.append(line.split(":")[1].strip())
                    elif line.startswith("B:"):
                        options.append(line.split(":")[1].strip())
                    elif line.startswith("C:"):
                        options.append(line.split(":")[1].strip())
                    elif line.startswith("D:"):
                        options.append(line.split(":")[1].strip())
                    elif line.startswith("Correct:"):
                        current_question["Correct"] = line.split(":")[1].strip()
                        current_question["Options"] = options
                        questions.append(current_question)
                        options = []

                available_questions = [q for q in questions if q["Question"] not in self.used_questions]

                if available_questions:
                    selected_question = random.choice(available_questions)
                    self.used_questions.add(selected_question["Question"])
                    return selected_question
                else:
                    return None  # if no questions found for difficulty
        except FileNotFoundError:
            return None