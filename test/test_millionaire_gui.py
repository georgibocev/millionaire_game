import unittest
from unittest.mock import patch, Mock
import tkinter as tk
from tkinter import messagebox
from module.modules.game import Game
from module.modules.millionaire_gui import MillionaireGUI
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(PROJECT_ROOT)

class TestMillionaireGUI(unittest.TestCase):
    """
    Test MillionaireGUI class functionality
    """

    def setUp(self):
        """ Create an instance of the MillionaireGUI to be used for testing purposes"""
        self.root = tk.Tk()
        self.gui = MillionaireGUI(self.root)

    @patch.object(MillionaireGUI, 'load_question')
    def test_setup_play_again_button(self, mock_load_question):
        """
        Tests if the setup_play_again_button method correctly sets up the Play Again button and invokes the load_question method.
        """
        self.gui.setup_play_again_button()
        self.gui.play_again_button.invoke()
        mock_load_question.assert_called_once()

    @patch.object(MillionaireGUI, 'update_ui')
    def test_display_victory(self, mock_update_ui):
        """
        Tests if the display_victory method correctly shows the victory message and invokes update_ui.
        """
        with patch.object(messagebox, 'showinfo') as mock_showinfo:
            self.gui.display_victory()
            mock_showinfo.assert_called_once_with('Congratulations!', "You've won my game! Thank you for playing."
                                                                      " The game will now automatically restart.")
            mock_update_ui.assert_called_once()

    @patch.object(messagebox, 'showinfo')
    def test_display_call_a_friend_message(self, mock_showinfo):
        """
        Tests if the display_call_a_friend_message method correctly shows the Call a Friend message and invokes update_ui.
        """
        self.gui.display_call_a_friend_message('A')
        mock_showinfo.assert_called_once_with("Call a Friend", 'Your friend says the answer is A.')
        self.gui.update_ui()

    @patch.object(messagebox, 'showinfo')
    def test_display_ask_the_public_message(self, mock_showinfo):
        """
        Tests if the display_ask_the_public_message method correctly shows the Ask the Public message and invokes update_ui.
        """
        poll_results = {'A': 25.0, 'B': 30.0, 'C': 40.0, 'D': 5.0}
        self.gui.display_ask_the_public_message('B', poll_results)
        mock_showinfo.assert_called_once_with("Ask the Public", 'Poll Results:\nA: 25.0%\nB: 30.0%\nC: 40.0%\nD: '
                                                                '5.0%\n\nThe public says the correct answer is B.')
        self.gui.update_ui()

    @patch.object(messagebox, 'showinfo')
    def test_display_50_50_message(self, mock_showinfo):
        """
        Tests if the display_50_50_message method correctly shows the 50/50 message, updates the options, and invokes update_ui.
        """
        initial_options = ['Berlin', 'Rome', 'Paris', 'Madrid']
        self.gui.game_model.current_question["Options"] = initial_options
        incorrect_answers = ['Rome', 'Paris']
        self.gui.display_50_50_message(incorrect_answers)
        mock_showinfo.assert_called_once_with("50/50", "The eliminated answers are Rome, Paris")
        expected_options = [option if option not in incorrect_answers else "" for option in initial_options]
        self.assertEqual(self.gui.game_model.current_question["Options"], expected_options)

    @patch.object(messagebox, 'showinfo')
    @patch.object(MillionaireGUI, 'display_game_over')
    def test_handle_answer_button_click_incorrect(self, mock_display_game_over, mock_showinfo):
        """
        Tests if the handle_answer_button_click method correctly handles an incorrect answer, displays the game over message, and invokes display_game_over.
        """
        with patch.object(Game, 'check_answer', return_value=False):
            self.gui.handle_answer_button_click('B')
            mock_display_game_over.assert_called_once()
            mock_showinfo.assert_not_called()

    def tearDown(self):
        """
        Clean up resources after each test.
        """
        self.root.destroy()
