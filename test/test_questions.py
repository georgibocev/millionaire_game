import unittest
from unittest.mock import mock_open, patch
from module.modules.questions import QuestionGenerator


class TestQuestionGenerator(unittest.TestCase):
    """
    Test Question Generator class functionality
    """
    def setUp(self):
        """ Create an instance of the QuestionGenerator to be used for testing purposes"""
        self.question_generator = QuestionGenerator()

    @patch('builtins.open', new_callable=mock_open, read_data='[{"Question": "Q1", "Options": ["A", "B", "C", "D"]}]')
    def test_load_question_success(self, mock_file_open):
        """
        Tests if the load_question method returns a question with "Question" and "Options" keys when there are
        available questions
        """
        question = self.question_generator.load_question("easy")

        self.assertIn("Question", question)
        self.assertIn("Options", question)

    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_load_question_no_available_questions(self, mock_file_open):
        """
        Tests if the load_question method raises a SystemExit when there are no available questions.
        """
        with self.assertRaises(SystemExit):
            self.question_generator.load_question("easy")

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_question_file_not_found(self, mock_file_open):
        """
        Tests if the load_question method raises a SystemExit when the file is not found.
        """
        with self.assertRaises(SystemExit):
            self.question_generator.load_question("easy")
