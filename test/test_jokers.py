import unittest
from unittest.mock import patch
from module.modules.jokers import Joker50_50, JokerCallAFriend, JokerAskThePublic


class TestJokers(unittest.TestCase):
    """
    Test Joker classes functionality
    """

    def setUp(self):
        """ Create instances of Joker classes to be used for testing purposes"""
        self.joker_50_50 = Joker50_50()
        self.joker_call_a_friend = JokerCallAFriend()
        self.joker_ask_the_public = JokerAskThePublic()

    @patch('module.modules.jokers.random.sample', return_value=["B", "C"])
    def test_joker_50_50_use(self, mock_random_sample):
        """
        Tests if the Joker50_50 class correctly selects two incorrect options when used.
        """
        question = {"Options": ["A", "B", "C", "D"], "Correct": 0}
        result = self.joker_50_50.use(question)

        self.assertTrue(self.joker_50_50.used)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(option in question["Options"] for option in result))

    @patch('module.modules.jokers.random.choice', return_value="C")
    def test_joker_call_a_friend_use(self, mock_random_choice):
        """
        Tests if the JokerCallAFriend class correctly returns an answer based on the correct option.
        """
        question = {"Correct": "1"}
        result = self.joker_call_a_friend.use(question)

        self.assertTrue(self.joker_call_a_friend.used)
        self.assertEqual(result, "B")

    @patch('module.modules.jokers.random.uniform', side_effect=[0.5, 0.7, 0.9, 0.4])
    def test_joker_ask_the_public_use(self, mock_random_uniform):
        """
        Tests if the JokerAskThePublic class correctly returns a public answer and poll results
        based on the correct option.
        """
        question = {"Correct": "2"}
        result = self.joker_ask_the_public.use(question)

        self.assertTrue(self.joker_ask_the_public.used)
        self.assertEqual(result[0], "C")

        expected_percentages = {'A': 20.0, 'B': 30.0, 'C': 40.0, 'D': 10.0}

        for option, expected_percentage in expected_percentages.items():
            self.assertAlmostEqual(result[1][option], expected_percentage, delta=8.0)
