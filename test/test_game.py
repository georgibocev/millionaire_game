import unittest
from unittest.mock import MagicMock, patch
from module.modules.game import Game


class TestGame(unittest.TestCase):
    """
    Test Game class functionality
    """

    def setUp(self):
        """Create an instance of the Game class to be used for testing purposes"""
        self.game = Game()

    @patch.object(Game, 'increase_difficulty')
    @patch.object(Game, 'load_question')
    def test_check_answer_correct(self, mock_load_question, mock_increase_difficulty):
        """
        Tests if the check_answer method returns True when the selected option is correct.
        """
        self.game.current_question = {"Correct": "A"}
        self.game.__score = 0
        result = self.game.check_answer("A")
        self.assertTrue(result)

    @patch.object(Game, 'increase_difficulty')
    @patch.object(Game, 'load_question')
    def test_check_answer_incorrect(self, mock_load_question, mock_increase_difficulty):
        """
        Tests if the check_answer method returns False when the selected option is incorrect.
        """
        self.game.current_question = {"Correct": "A"}
        self.game.__score = 0
        result = self.game.check_answer("B")
        self.assertFalse(result)

    @patch.object(Game, 'increase_difficulty')
    @patch.object(Game, 'load_question')
    def test_check_answer_game_won(self, mock_load_question, mock_increase_difficulty):
        """
        Tests if the check_answer method sets game_won to True when the score reaches the maximum.
        """
        self.game.current_question = {"Correct": "A"}
        self.game.__score = 99999
        self.game.check_answer("A")
        self.assertTrue(self.game.game_won)

    @patch.object(Game, 'increase_difficulty')
    @patch.object(Game, 'load_question')
    def test_increase_difficulty(self, mock_load_question, mock_increase_difficulty):
        """
        Tests if the increase_difficulty method correctly updates the difficulty based on the score.
        """

        self.game.__score = 600
        self.assertEqual(self.game.__difficulty, "easy")

    @patch.object(Game, 'use_joker')
    def test_use_joker_valid(self, mock_use_joker):
        """
        Tests if the use_joker method correctly uses a valid joker and returns the result.
        """
        mock_joker = MagicMock()
        mock_joker.used = False
        self.game.jokers["mock_joker"] = mock_joker
        result = self.game.use_joker("mock_joker")
        self.assertEqual(result, mock_use_joker.return_value)
        mock_use_joker.assert_called_once_with("mock_joker")

    @patch.object(Game, '__init__')
    def test_restart_game(self, mock_init):
        """
        Tests if the restart_game method correctly resets the game state.
        """
        self.game.restart_game()
        mock_init.assert_called_once()
