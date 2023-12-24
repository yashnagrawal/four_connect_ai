# FourConnect Game Playing Script

## Overview

This script (`main.py`) is designed to play the FourConnect game, a variation of Connect Four, using a Game Tree Player with the Minimax algorithm and Alpha-Beta pruning. The game is played on a 6x7 grid, and the objective is to connect four of your own discs in a row, either horizontally, vertically, or diagonally.

## Instructions

1. Run the script using Python 3: `python3 main.py`
2. The game will start, and each player will take turns making moves. The Game Tree Player uses the Minimax algorithm with Alpha-Beta pruning to make optimal moves.
3. The game continues until a player wins or the board is full (a draw). The winner and number of moves will be displayed at the end.

## File Structure

- `main.py`: The main script containing the game logic and the Game Tree Player implementation.
- `FourConnect.py`: The FourConnect class with methods for managing the game state, checking for a winner, and making moves.
- `report.pdf`: A report describing the Game Tree Player implementation and the results of the tests.
- `testcases/`: A directory containing test cases for the Game Tree Player. Each test case is a text file containing the game state and the expected move.

## Game Tree Player Implementation

The `GameTreePlayer` class implements the Minimax algorithm with Alpha-Beta pruning. It uses various heuristics to prioritize moves and evaluate the game state. The `FindBestAction` method is responsible for finding the optimal move.

## Test Cases

You can run the test case using the `RunTestCase` function in the script. It checks if the Game Tree Player can win in 5 moves.

## Random Games

The `PlayGameRandom` function allows you to simulate multiple random games and gather statistics on wins, losses, draws, and the average number of moves.

## Random Games

The `PlayGameRandom` function allows you to simulate multiple random games and gather statistics on wins, losses, draws, and the average number of moves.

## Note

This script uses a simple Move Ordering Heuristic and three different heuristic functions for evaluating the game state. You can modify these functions or add additional heuristics based on your understanding of the game.
