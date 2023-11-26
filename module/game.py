import module.config as config
from module.jokers import Joker50_50, JokerCallAFriend, JokerAskThePublic
from module.questions import QuestionGenerator


class Game:
    def __init__(self):
        self.question_generator = QuestionGenerator()
        self.current_question = None
        self.score = 0
        self.difficulty = "easy"
        self.jokers = {
            "50/50": Joker50_50(),
            "Call a Friend": JokerCallAFriend(),
            "Ask the Public": JokerAskThePublic()
        }
        self.game_won = False

    def load_question(self):
        self.current_question = self.question_generator.load_question(self.difficulty)

    def check_answer(self, selected_option):
        if self.current_question:
            correct_option = config.ANSWER_MAPPING.get(self.current_question["Correct"])
            if selected_option == correct_option:
                self.score += config.DIFFICULTY_SCORES.get(self.difficulty, 0)
                if self.score >= config.THRESHOLDS["very_hard"]:
                    self.score = config.THRESHOLDS["very_hard"]
                    self.game_won = True
                else:
                    self.increase_difficulty()
                return True
        return False

    def increase_difficulty(self):
        if self.score < config.THRESHOLDS["easy"]:
            self.difficulty = "easy"
        elif self.score < config.THRESHOLDS["medium"]:
            self.difficulty = "medium"
        elif self.score < config.THRESHOLDS["hard"]:
            self.difficulty = "hard"
        elif self.score < config.THRESHOLDS["very_hard"]:
            self.difficulty = "very_hard"

    def use_joker(self, joker_name):
        if joker_name in self.jokers:
            joker = self.jokers[joker_name]
            if not joker.used:
                result = joker.use(self)
                joker.used = True
                return result
        return None

    def restart_game(self):
        self.__init__()

    def use_50_50_joker(self):
        return self.use_joker("50/50")

    def use_call_a_friend_joker(self):
        if "Call a Friend" in self.jokers:
            joker = self.jokers["Call a Friend"]
            if not joker.used:
                result = joker.use(self)
                joker.used = True
                return result

    def use_ask_the_public_joker(self):
        if "Ask the Public" in self.jokers:
            joker = self.jokers["Ask the Public"]
            if not joker.used:
                result = joker.use(self)
                joker.used = True
                return result
