# Sudoku Game

A Sudoku puzzle game written in Python using the Tkinter library

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Running the Game](#running-the-game)
- [Game Controls](#game-controls)
- [Additional Information](#additional-information)


## Overview

This project implements a Sudoku game with a graphical user interface using Python and Tkinter, players can interactively solve the Sudoku puzzle and check their solutions.

## Getting Started

The main motivation behind this project was to see if I can come up to the challenge of trying to randomize the board for each game and have a backtraking solver for the program,
as well as seeing if I can make the program run more efficatently

### Prerequisites

Make sure you have the following installed:

- Python (version 3.6 or higher)
- Tkinter (newest version)

### Installation

1.  pip install tk

# Running the Game

- Download attached file that was submitted for this assignmtnt Sudoku-Puzzle-3680.py and run in Visual Studio Code

- or you can use github

1. Clone the repository:

    ```bash
    git clone https://github.com/ethansled/Sudoku-Puzzle-3680.git
    ```

2. Navigate to the project directory:

    ```bash
    cd Final_Project-3680
    ```

3. Run the game:

    ```bash
    python Sudoku-Puzzle-3680.py
    ```

# Game Controls

- The Sudoku puzzle is displayed in a 9x9 grid.
- Click on a cell to select it.
- Use the keyboard to enter numbers into the selected cell.
- Press the "Check" button to verify if the answer was correct.
- Press the "Solve Board" button to automatically solve the entire puzzle.
- Press the "End Game" button to exit the application.


# Additional Information

- **Move Counter:** The number of moves made is displayed on the GUI.
- **Timer:** The elapsed time is shown on the GUI.
- **Results Logging:** The correct moves and game results are logged in the `game_results.txt` file.
