# Tic-Tac-Toe vs AI Documentation

**Category**: Python Games / Artificial Intelligence
**Path**: `Python/Tic-Tac-Toe`
**Version**: 1.0

## Overview
**Tic-Tac-Toe vs AI** is a classic implementation of the game Noughts and Crosses, featuring an unbeatable computer opponent. This project demonstrates the implementation of the **Minimax Algorithm**, a recursive decision-making strategy used in game theory to minimize the possible loss for a worst-case scenario (hence "Mini-Max").

## Key Features

### 1. Python Game Engine (`main.py`)
- **Minimax AI**: The core feature is the `minimax()` function, which simulates all possible future moves to determine the optimal play. Since the state space of Tic-Tac-Toe is small, it can search to the end of the game depth.
  - **Result**: The AI will *never* lose. It will either win or force a tie.
- **Console Interface**: A text-based grid (0-8) allows the user to play by entering the number of the square they want to mark.
- **Recursion**: Demonstrates a practical application of recursive functions in Python.

### 2. GUI Application (`gui_main.py`)
- *Note: A graphical version where users click cells instead of typing numbers.*

### 3. Web Demo
The web version provides a visual interface for the same algorithm:
- **Interactive Board**: A CSS Grid layout that responds to clicks.
- **JavaScript AI**: Implements the same Minimax logic in client-side JS (`getBestMove` and `minimax` functions) to provide an identical unbeatable opponent in the browser.
- **Scoreboard**: Tracks Wins (unlikely), AI Wins, and Ties across the session.

## Architecture

### Directory Structure
```
Tic-Tac-Toe/
├── main.py         # Console AI (Minimax)
├── gui_main.py     # Desktop UI
└── demo.html       # Web Game + JS Minimax
```

### The Minimax Algorithm
1.  **Check Terminal State**: If Player wins, return -10. If AI wins, return +10. If Tie, return 0.
2.  **Recursive Step**: 
    - Loop through all available empty spots.
    - Play a "mock" move.
    - Call `minimax()` again for the next player.
    - Undo the move.
    - Choose the move that yields the highest score (for AI) or lowest score (for Player).

## Setup & Execution

### Prerequisites
- Python 3.x

### Running the Game
1.  **Navigate**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\Python\Tic-Tac-Toe"
    ```
2.  **Run**:
    ```powershell
    python main.py
    ```

### Expected Output
```
Welcome to Tic Tac Toe vs AI!
Board Positions: 0-8

   |   |   
---+---+---
   |   |   
---+---+---
   |   |   

X's turn. Input move (0-8): 4

 X |   |   
---+---+---
   | O |   
...
```
