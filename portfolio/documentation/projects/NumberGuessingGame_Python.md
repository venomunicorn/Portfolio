# Number Guessing Game Documentation

**Category**: Python Games / Logic
**Path**: `Python/NumberGuessingGame`
**Version**: 1.0

## Overview
The **Number Guessing Game** is an enhanced version of the classic console game. It pits the play against the computer to guess a secret random number within limited attempts. Notably, this project includes an **AI Solver Demo** that visually demonstrates the **Binary Search** algorithm, explaining how computers can solve this problem efficiently ($O(\log n)$) compared to human guessing.

## Key Features

### 1. Python Game Logic (`main.py`)
- **Difficulty Levels**:
  - **Easy**: 1-10 (5 attempts)
  - **Medium**: 1-50 (7 attempts)
  - **Hard**: 1-100 (10 attempts)
- **Input Validation**: Ensures users enter valid integers and handles crashes gracefully.
- **AI Solver**: An automated mode where the script "plays itself" using Binary Search logic (`(low + high) // 2`) to find the number, printing its reasoning step-by-step.
- **Feedback Loop**: Provides "Too High" or "Too Low" hints after every guess.

### 2. GUI Application (`gui_main.py`)
- *Note: Provides a windowed version where users type guesses into a box and see a progress bar for remaining attempts.*

### 3. Web Demo
The web simulation allows users to play or watch the AI:
- **Visual Progress Bar**: A green bar shrinks as attempts run out, adding tension.
- **Best Score Tracker**: Remembers the fewest attempts used to win in the current session.
- **AI Visualizer**: Clicking "Watch AI Solve" opens a log window that shows the Binary Search algorithm in real-time (e.g., "Trying 25 -> Too High -> Searching 1-24").

## Architecture

### Directory Structure
```
NumberGuessingGame/
├── main.py         # Console Game + AI Logic
├── gui_main.py     # Desktop UI
└── demo.html       # Web Game + AI Visualizer
```

### Algorithmic Concept (Binary Search)
The AI solver demonstrates why Binary Search is optimal for sorted ranges.
```python
while low <= high:
    guess = (low + high) // 2
    if guess < secret:
        low = guess + 1  # Eliminate lower half
    elif guess > secret:
        high = guess - 1 # Eliminate upper half
```
This guarantees finding a number in range 1-100 in just $\approx 7$ guesses ($\log_2 100$).

## Setup & Execution

### Prerequisites
- Python 3.x

### Running the Console App
1.  **Navigate**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\Python\NumberGuessingGame"
    ```
2.  **Run**:
    ```powershell
    python main.py
    ```

### Expected Output
```
Welcome to the Enhanced Number Guessing Game!
1. Play Game
2. Watch AI Solve
Choice: 1

Select Difficulty:
1. Easy
2. Medium
...
Attempt 1/7: Enter guess: 25
Too High!
Attempt 2/7: Enter guess: 12
Too Low!
```

## Web Demo Usage
- Open `demo.html` in a web browser.
- **Play**: Select "Medium" and try to guess the number.
- **Learn**: Click "Watch AI Solve" to see the computer find the number 42 in milliseconds.
