from module.jokers import Joker50_50, JokerCallAFriend, JokerAskThePublic
from module.questions import QuestionGenerator


class Game:
    DIFFICULTY_SCORES = {
        "easy": 500,
        "medium": 2000,
        "hard": 10000,
        "very_hard": 20000
    }

    THRESHOLDS = {
        "easy": 1000,
        "medium": 10000,
        "hard": 50000,
        "very_hard": 100000
    }

    def __init__(self):
        self.question_generator = QuestionGenerator()
        self.current_question = None
        self.score = 0
        self.difficulty = "easy"
        self.game_won = False
        self.jokers = {
            "50/50": Joker50_50(),
            "Call a Friend": JokerCallAFriend(),
            "Ask the Public": JokerAskThePublic()
        }

    def load_question(self):
        self.current_question = self.question_generator.load_question(self.difficulty)

    def check_answer(self, selected_option):
        correct_option = str(self.current_question["Correct"])
        if str(selected_option) == correct_option:
            self.score += self.DIFFICULTY_SCORES.get(self.difficulty, 0)
            if self.score >= self.THRESHOLDS["very_hard"]:
                self.score = self.THRESHOLDS["very_hard"]
                self.game_won = True
            else:
                self.increase_difficulty()
            return True
        else:
            return False

    def increase_difficulty(self):
        for difficulty, threshold in self.THRESHOLDS.items():
            if self.score < threshold:
                self.difficulty = difficulty
                break

    def use_joker(self, joker_name):
        if joker_name in self.jokers:
            joker = self.jokers[joker_name]
            if not joker.used:
                result = joker.use(self.current_question)
                return result
        return None

    def restart_game(self):
        self.__init__()
