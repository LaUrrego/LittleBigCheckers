# LittleBigCheckers

<a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" alt ="Python banner"></a>
<a href="https://www.jetbrains.com/pycharm/"><img src="https://img.shields.io/badge/PyCharm-000000.svg?&style=for-the-badge&logo=PyCharm&logoColor=white" alt ="PyCharm banner"></a>
<a href="https://www.linkedin.com/in/larryurrego/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt ="LinkedIn banner"></a>
<a href="https://www.geeksforgeeks.org/print-colors-python-terminal/"><img src="https://img.shields.io/badge/GeeksforGeeks-298D46?style=for-the-badge&logo=geeksforgeeks&logoColor=white" alt ="GeeksforGeeks banner"></a>


![Terminal output view](https://github.com/LaUrrego/LittleBigCheckers/blob/main/Images/Checkers_Terminal_Screen.png)

LittleBigCheckers is my attempt at a custom checkers simulating game made entirely in Python. It's turn and prompt based,
determining all possible diagonals for a given token's current position on the board, and utilizing a custom algorithm to 
evaluate possible moves. It prioritizes captures according to official <a href="https://www.wikihow.com/Play-Checkers">rules,</a> but move autonomy lies solely on the user.

The project is organized using object-oriented programming principles into distinct classes for players, checkers, tokens, 
and the checkerboard, and modularized move logic for ease of use throughout the code or for later customization.  

Although I'm proud of the work I've done, this is very much still a work in progress I hope to develop over time to 
become fully executable within terminal to include automated play calls, auto refresh after turns, and segmented move
logic displays to aid players with making their next move. I'm also looking into further development in the form of 
an integrated CPU opponent with difficulty levels to make it easy to play or train.

I hope you enjoy this project as much as I did making it! 

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Code Examples](#code-examples)
- [Contributing](#contributing)
- [References](#license)
- [Contact](#contact)

## Features

- **Custom Game Logic**  
  - The game logic is designed to handle all the nuances of the checkers game, such as regular pieces, kings, and triple kings. It accurately calculates all possible diagonal moves and jumps for each token type and determines the validity of a move based on the game's rules.
- **Colorful Terminal Output** 
  - The print_color_board() method in the Checkers class outputs the current game state as a stacked, numbered list of lists, using ANSI escape sequences to display colors in the terminal. This makes it easy to view the live display of the board during gameplay.
- **Extensible Class Structure** 
  - The project consists of distinct classes for various game elements, such as Player, Checkers, Token, and CheckerBoard, allowing for easy modifications and enhancements to the game's logic and representation.
- **Helpful Debugging Features** 
  - The Checkers class includes a print_moves() method that accepts a (row, column) position and displays the number of possible jumps for the piece at that position. This helps in understanding and debugging the game's logic.

![PyCharm console output view](https://github.com/LaUrrego/LittleBigCheckers/blob/main/Images/Checkers_Console_Screen.png)


# How to Use

Currently for Mac Terminal! Testing others as time allows.

To use LittleBigCheckers, simply create an instance of Checkers, create two players using create_player(), and the call
play_game() method to begin the game and use it to move your token pieces. You can also call the print_color_board() 
method below all play_game() calls to automatically display the game board in the terminal after each move in full color 
and labeled rows/columns to help make move planning easier. 
For more insights into the game's logic, you can uncomment the print statements in the diagonal calculation logic to view 
per-move, per-piece printouts of moves on each diagonal.

When running the project in IDE: 
```Python
# Initiate the game
game = Checkers()
# Create players
game.create_player()
# Print a color representation of the board
game.print_color_board()
# Main function to enter a move
game.play_game()

```

## Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/LaUrrego/LittleBigCheckers.git
```

2. Change to the project directory:

```bash
cd LittleBigCheckers
```

3. Ensure you have Python 3.x installed on your system. You can check your curent version with:

```bash
python --version
```

## Usage

1. Run the game using Python:

```bash
python3 CheckersGame.py
```

2. Follow the on-screen instructions to play the game and have fun!

## Contributing 

Any contributions are greatly appreciated. Please follow these steps to contribute:

1. Fork the repo.
2. Create your feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am ‘Add some feature’`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Create a new Pull Request.

## References

<a href="https://www.geeksforgeeks.org/print-colors-python-terminal/" >GeeksforGeeks article on how to add color to Python projects</a>

## Contact

Feel free to reach out to me here or on LinkedIn!