import tkinter as tk
from tkinter import messagebox
import config
from game import Game


class MillionaireGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Who Wants to Be a Millionaire")
        self.game_model = Game()
        self.setup_ui()
        self.load_question()

    def setup_ui(self):
        self.question_label = tk.Label(self.root, text="", wraplength=config.BUTTON_WIDTH, justify="center", font=config.UI_FONT)
        self.question_label.pack(pady=20)

        self.option_buttons = []
        for i in range(4):
            button = tk.Button(self.root, text="", command=lambda i=i: self.handle_answer_button_click(i), font=config.BUTTON_FONT)
            button.pack(fill=tk.X, padx=20, pady=config.BUTTON_HEIGHT)
            self.option_buttons.append(button)

        self.score_label = tk.Label(self.root, text="Score: 0", font=config.SCORE_FONT)
        self.score_label.pack(pady=10)

        self.play_again_button = tk.Button(self.root, text="Play Again", command=self.handle_restart_button_click, font=config.PLAY_AGAIN_FONT)
        self.play_again_button.pack(pady=10)
        self.play_again_button.pack_forget()

        self.joker_buttons = []
        for joker_name in self.game_model.jokers:
            button = tk.Button(self.root, text=joker_name, command=lambda name=joker_name: self.handle_joker_button_click(name), font=config.BUTTON_FONT)
            button.pack(pady=5)
            self.joker_buttons.append(button)

        self.percentages_label = tk.Label(self.root, text="", font=config.BUTTON_FONT)
        self.percentages_label.pack(pady=5)

    def load_question(self):
        self.game_model.load_question()
        self.update_ui()

    def update_ui(self):
        if self.game_model.current_question:
            self.question_label.config(text=self.game_model.current_question["Question"])
            options = self.game_model.current_question["Options"]
            for i, button in enumerate(self.option_buttons):
                label = f"{config.BUTTON_LABELS[i]}. {options[i]}"
                button.config(text=label)
                button.config(state=tk.NORMAL)
        else:
            self.display_game_over()

        self.score_label.config(text=f"Score: {self.game_model.score}")

    def display_game_over(self):
        self.disable_buttons()
        self.question_label.config(text="Game Over")
        self.play_again_button.pack()

    def disable_buttons(self):
        for button in self.option_buttons:
            button.config(state=tk.DISABLED)
        for button in self.joker_buttons:
            button.config(state=tk.DISABLED)
    def display_victory(self):
        self.disable_buttons()
        won_game_message = "You've won my game! Thank you for playing. The game will now automatically restart."
        messagebox.showinfo("Congratulations!", won_game_message)
        self.handle_restart_button_click()

    def handle_answer_button_click(self, selected_option):
        if self.game_model.check_answer(selected_option):
            if self.game_model.game_won:
                self.display_victory()
            else:
                self.load_question()
        else:
            self.display_game_over()

    def handle_joker_button_click(self, joker_name):
        result = self.game_model.use_joker(joker_name)
        if result:
            if joker_name == "Call a Friend":
                self.display_call_a_friend_message(result)
            elif joker_name == "Ask the Public":
                public_answer, poll_results = result
                self.display_ask_the_public_message(public_answer, poll_results)
        joker_button_index = [name for name, button in enumerate(self.joker_buttons) if
                                  button.cget("text") == joker_name]
        if joker_button_index:
            self.joker_buttons[joker_button_index[0]].config(state=tk.DISABLED)
        self.update_ui()

    def handle_restart_button_click(self):
        for button in self.joker_buttons:
            button.config(state=tk.NORMAL)

        self.game_model.restart_game()
        self.load_question()
        self.hide_play_again_button()

    def display_call_a_friend_message(self, correct_option):
        message = f"Your friend says the answer is {correct_option}."
        messagebox.showinfo("Call a Friend", message)
        self.update_ui()

    def display_ask_the_public_message(self, correct_option, poll_results):
        message = f"Poll Results:\n"
        for option, percentage in poll_results.items():
            message += f"{option}: {percentage:.1f}%\n"
        message += f"\nThe public says the correct answer is {correct_option}."

        messagebox.showinfo("Ask the Public", message)
        self.update_ui()

    def hide_play_again_button(self):
        self.play_again_button.pack_forget()