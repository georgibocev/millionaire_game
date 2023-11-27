import tkinter as tk
from tkinter import messagebox
from module.modules.game import Game


class MillionaireGUI:
    """
    Graphical user interface for the "Who Wants to Be a Millionaire" game.

    Attributes:
    - BUTTON_LABELS (list): A list of labels for the answer buttons.
    - UI_FONT (tuple): Font specifications for the main UI text.
    - BUTTON_FONT (tuple): Font specifications for the answer buttons.
    - BUTTON_WIDTH (int): Width of the answer buttons.
    - BUTTON_HEIGHT (int): Height of the answer buttons.
    - SCORE_FONT (tuple): Font specifications for the score label.
    - PLAY_AGAIN_FONT (tuple): Font specifications for the "Play Again" button.

    Methods:
    - __init__: Initializes the MillionaireGUI with the root window.
    - __setup_ui: Sets up the UI components.
    - __setup_question_label: Sets up the question label.
    - __setup_option_buttons: Sets up the answer buttons.
    - __setup_play_again_button: Sets up the "Play Again" button.
    - __setup_joker_buttons: Sets up the joker buttons.
    - __setup_percentages_label: Sets up the percentages label.
    - __setup_score_label: Sets up the score label.
    - __load_question: Loads a new question from the game model.
    - __update_ui: Updates the UI components based on the current state of the game.
    - __display_game_over: Displays the "Game Over" message and enables the "Play Again" button.
    - __disable_buttons: Disables answer buttons and joker buttons.
    - __display_victory: Displays a victory message and automatically restarts the game.
    - __handle_answer_button_click: Handles the click event for answer buttons.
    - __handle_joker_button_click: Handles the click event for joker buttons.
    - __handle_restart_button_click: Handles the click event for the "Play Again" button.
    - __display_call_a_friend_message: Displays the message for the "Call a Friend" joker.
    - __display_ask_the_public_message: Displays the message for the "Ask the Public" joker.
    - __hide_play_again_button: Hides the "Play Again" button.
    - __display_50_50_message: Displays the message for the "50/50" joker.

    """
    BUTTON_LABELS = ["A", "B", "C", "D"]
    UI_FONT = ("Arial", 16)
    BUTTON_FONT = ("Arial", 14)
    BUTTON_WIDTH = 600
    BUTTON_HEIGHT = 5
    SCORE_FONT = ("Arial", 14)
    PLAY_AGAIN_FONT = ("Arial", 12)

    def __init__(self, root):
        """
        Initializes the MillionaireGUI with the root window.

        Args:
        - root: The root window for the GUI.

        """
        self.__root = root
        self.__root.title("Who Wants to Be a Millionaire")
        self.__game_model = Game()
        self.__option_buttons = []
        self.__play_again_button = None
        self.__question_label = None
        self.__percentages_label = None
        self.__score_label = None
        self.__joker_buttons = []
        self.__setup_ui()
        self.__load_question()

    def __setup_ui(self):
        """Sets up the UI components."""
        self.__setup_question_label()
        self.__setup_option_buttons()
        self.__setup_score_label()
        self.__setup_play_again_button()
        self.__setup_joker_buttons()
        self.__setup_percentages_label()

    def __setup_question_label(self):
        """Sets up the question label."""
        self.__question_label = tk.Label(
            self.__root,
            text="",
            wraplength=self.BUTTON_WIDTH,
            justify="center",
            font=self.UI_FONT
        )
        self.__question_label.pack(pady=20)

    def __setup_option_buttons(self):
        """Sets up the answer buttons."""
        for index in range(4):
            button = tk.Button(
                self.__root,
                text="",
                command=lambda idx=index: self.__handle_answer_button_click(idx),
                font=self.BUTTON_FONT
            )
            button.pack(fill=tk.X, padx=20, pady=self.BUTTON_HEIGHT)
            self.__option_buttons.append(button)

    def __setup_play_again_button(self):
        """Sets up the "Play Again" button."""
        self.__play_again_button = tk.Button(
            self.__root,
            text="Play Again",
            command=self.__handle_restart_button_click,
            font=self.PLAY_AGAIN_FONT
        )
        self.__play_again_button.pack(pady=10)
        self.__play_again_button.pack_forget()

    def __setup_joker_buttons(self):
        """Sets up the joker buttons."""
        for joker_name in self.__game_model.jokers:
            button = tk.Button(
                self.__root,
                text=joker_name,
                command=lambda name=joker_name: self.__handle_joker_button_click(name),
                font=self.BUTTON_FONT
            )
            button.pack(pady=5)
            self.__joker_buttons.append(button)

    def __setup_percentages_label(self):
        """Sets up the percentages label."""
        self.__percentages_label = tk.Label(self.__root, text="", font=self.BUTTON_FONT)
        self.__percentages_label.pack(pady=5)

    def __setup_score_label(self):
        """Sets up the score label."""
        self.__score_label = tk.Label(self.__root, text="Score: 0", font=self.SCORE_FONT)
        self.__score_label.pack(pady=10)

    def __load_question(self):
        """Loads a new question from the game model."""
        self.__game_model.load_question()
        self.__update_ui()

    def __update_ui(self):
        """Updates the UI components based on the current state of the game."""
        if self.__game_model.current_question:
            self.__question_label.config(text=self.__game_model.current_question["Question"])
            options = self.__game_model.current_question["Options"]
            for i, button in enumerate(self.__option_buttons):
                label = f"{self.BUTTON_LABELS[i]}. {options[i]}"
                button.config(text=label)
                button.config(state=tk.NORMAL)

        else:
            self.__display_game_over()

        self.__score_label.config(text=f"Score: {self.__game_model.score}")

    def __display_game_over(self):
        """Displays the "Game Over" message and enables the "Play Again" button."""
        self.__disable_buttons()
        self.__question_label.config(text="Game Over")
        self.__play_again_button.pack()

    def __disable_buttons(self):
        """Disables answer buttons and joker buttons."""
        for button in self.__option_buttons:
            button.config(state=tk.DISABLED)
        for button in self.__joker_buttons:
            button.config(state=tk.DISABLED)

    def __display_victory(self):
        """
        Displays a victory message and automatically restarts the game.
        """
        self.__disable_buttons()
        won_game_message = "You've won my game! Thank you for playing. The game will now automatically restart."
        messagebox.showinfo("Congratulations!", won_game_message)
        self.__handle_restart_button_click()

    def __handle_answer_button_click(self, selected_option):
        """
        Handles the click event for answer buttons.
        """
        if self.__game_model.check_answer(selected_option):
            if self.__game_model.game_won:
                self.__display_victory()
            else:
                self.__load_question()
        else:
            self.__display_game_over()

    def __handle_joker_button_click(self, joker_name):
        """
        Handles the click event for joker buttons.
        """
        result = self.__game_model.use_joker(joker_name)
        if result:
            if joker_name == "Call a Friend":
                self.__display_call_a_friend_message(result)
            elif joker_name == "Ask the Public":
                public_answer, poll_results = result
                self.__display_ask_the_public_message(public_answer, poll_results)
            elif joker_name == "50/50":
                self.__display_50_50_message(result)
        joker_button_index = [name for name, button in enumerate(self.__joker_buttons) if
                              button.cget("text") == joker_name]
        if joker_button_index:
            self.__joker_buttons[joker_button_index[0]].config(state=tk.DISABLED)
        self.__update_ui()

    def __handle_restart_button_click(self):
        """
        Handles the click event for the "Play Again" button.
        """
        for button in self.__joker_buttons:
            button.config(state=tk.NORMAL)

        self.__game_model.restart_game()
        self.__load_question()
        self.__hide_play_again_button()

    def __display_call_a_friend_message(self, correct_option):
        """
        Displays the message for the "Call a Friend" joker.
        """
        message = f"Your friend says the answer is {correct_option}."
        messagebox.showinfo("Call a Friend", message)
        self.__update_ui()

    def __display_ask_the_public_message(self, correct_option, poll_results):
        """
        Displays the message for the "Ask the Public" joker.
        """
        message = f"Poll Results:\n"
        for option, percentage in poll_results.items():
            message += f"{option}: {percentage:.1f}%\n"
        message += f"\nThe public says the correct answer is {correct_option}."

        messagebox.showinfo("Ask the Public", message)
        self.__update_ui()

    def __hide_play_again_button(self):
        """Hides the "Play Again" button."""
        self.__play_again_button.pack_forget()

    def __display_50_50_message(self, incorrect_answers):
        """
        Displays the message for the "50/50" joker.
        """
        message = f"The eliminated answers are {', '.join(incorrect_answers)}"
        messagebox.showinfo("50/50", message)
        self.__game_model.current_question["Options"] = [opt if opt not in incorrect_answers else "" for opt in
                                                         self.__game_model.current_question["Options"]]
        self.__update_ui()
