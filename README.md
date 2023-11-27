# Project Summary
This program provides a Python GUI implementation of the famous "Who Wants To Become A Millionaire" Game. The user can choose an answer between four options, only one of which is correct. 
There are 3 available jokers:
- 50/50, which removes two incorrect answers
- Ask A Friend (which for simplicity for the time being just gives the correct answer)
- Ask The Public (which for simplicity also gives the correct answer, but creates a poll to simulate a voting public)
If the user chooses a wrong answer the game ends and an option to play again will appear.
There is a scoring system for every answer given by the player (more difficult answers give more points) and once the score reaches 100.000 the user has won the game.

# Requirements
This programm is run using [python3](https://www.python.org/).  
The following modules are used as dependencies: tkinter.

# Usage
To play "Who Wants To Become A Millionaire" navigate to the project directory (ensure you have Python installed) and run the following command:
```
python main.py 
```

# Technical Details
The program uses Python and leverages object-oriented principles. The programm relies on the Tkinter library for enhancing user experience by providing an interactive and visually appealing interface, allowing players to navigate the game more intuitively.

#Workflow
1. Game Initialization
At the start of the game, the program initializes the game state, including the player's score, current question, difficulty level, and lifelines. This sets the foundation for the gameplay.

2. Loading Questions and Presenting to the Player
The program loads questions based on the current difficulty level. These questions are presented to the player, typically in a formatted manner through the GUI, ensuring clarity and readability.

3. Answer Validation and Scoring
After the player selects an answer, the program validates the response against the correct answer. If the answer is correct, the player's score is updated based on the difficulty level. Incorrect answers result in the end of the game.

4. Lifeline Usage
Players can use lifelines such as "50/50," "Call a Friend," or "Ask the Public" for assistance. Lifelines introduce strategic elements to the game, adding complexity and decision-making for the player.

5. Difficulty Progression
As the player successfully answers questions, the difficulty level increases. This progression adds a challenging aspect to the game, requiring the player to demonstrate a deeper knowledge of the subject matter.

6. Game Restart or Exit
The game continues until the player either reaches the maximum score, exhausts all questions, or decides to exit. In the case of game over, the player may choose to restart the game, initiating a new round with the initial settings.

#Testing
All modules are tested with a comprehensive test suite to achieve high code coverage.
