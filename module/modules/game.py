from module.modules.jokers import Joker50_50, JokerCallAFriend, JokerAskThePublic
from module.modules.questions import QuestionGenerator


class Game:
    """
        Represents the game logic for Who Wants to Be a Millionaire.

        Attributes:
        - __question_generator (QuestionGenerator): The question generator for the game.
        - current_question (dict): The current question being presented.
        - score (int): The player's current score.
        - __difficulty (str): The difficulty level of the game.
        - game_won (bool): Indicates whether the player has won the game.
        - jokers (dict): Dictionary of available jokers.

        Constants:
        - DIFFICULTY_SCORES (dict): Mapping of difficulty levels to their corresponding score values.
        - THRESHOLDS (dict): Score thresholds for each difficulty level.
        """
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
        """
        Initializes a new instance of the Game class.
        """
        self.__question_generator = QuestionGenerator()
        self.current_question = None
        self.score = 0
        self.__difficulty = "easy"
        self.game_won = False
        self.jokers = {
            "50/50": Joker50_50(),
            "Call a Friend": JokerCallAFriend(),
            "Ask the Public": JokerAskThePublic()
        }

    def load_question(self):
        """
        Loads a new question for the game.
        """
        self.current_question = self.__question_generator.load_question(self.__difficulty)

    def check_answer(self, selected_option):
        """
        Checks if the selected answer is correct and updates the game state accordingly.

        Args:
         - selected_option (str): The option selected by the player.

        Returns:
        - bool: True if the answer is correct, False otherwise.
        """
        correct_option = str(self.current_question["Correct"])
        if str(selected_option) == correct_option:
            self.score += self.DIFFICULTY_SCORES.get(self.__difficulty, 0)
            if self.score >= self.THRESHOLDS["very_hard"]:
                self.score = self.THRESHOLDS["very_hard"]
                self.game_won = True
            else:
                self.__increase_difficulty()
            return True
        else:
            return False

    def __increase_difficulty(self):
        """
        Increases the game difficulty based on the player's score.
        """
        for difficulty, threshold in self.THRESHOLDS.items():
            if self.score < threshold:
                self.__difficulty = difficulty
                break

    def use_joker(self, joker_name):
        """
        Uses the specified joker and returns the result.

        Args:
        - joker_name (str): The name of the joker to use.

        Returns:
        - The result of using the joker.
        """
        if joker_name in self.jokers:
            joker = self.jokers[joker_name]
            if not joker.used:
                result = joker.use(self.current_question)
                return result
        return None

    def restart_game(self):
        """
        Restarts the game by resetting its state.
        """
        self.__init__()
