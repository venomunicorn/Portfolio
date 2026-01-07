# Number Guessing Game Documentation

**Category**: C++ Systems
**Path**: `C++/NumberGuessingGame`
**Version**: 1.0

## Overview
The **Number Guessing Game** is a classic beginner-friendly project that introduces the concepts of random number generation, conditional logic (`if-else`), and loops in C++. The program generates a secret number between 1 and 100, and the user must guess it based on "Too High" or "Too Low" hints.

## Key Features

### 1. C++ Logic
- **Random Number Generation**: Uses `std::srand` seeded with `std::time` to ensure a different secret number every run.
- **Input Validation**: Checks if the user's input is a valid integer. If not, it clears the error state and ignores the bad input to prevent infinite loops.
- **Game Loop**: A `while` loop continues until the user's guess matches the secret number.
- **Attempt Counter**: Tracks and displays the number of guesses taken to win.

### 2. Web Demo
The HTML5 demo version provides a polished user interface:
- **Instant Feedback**: Displays styled messages ("Too HIGH", "Too LOW", "Congratulations") immediately after each guess.
- **Stats Tracking**: Shows the current attempt count.
- **Persistence**: Uses `localStorage` to save the player's **Best Score** (fewest attempts) across browser sessions.
- **Keyboard Support**: Players can press "Enter" to submit guesses quickly.

## Architecture

### Directory Structure
```
NumberGuessingGame/
├── main.cpp    # C++ Source Code
└── demo.html   # Interactive Web Demo
```

### Game Flow (`main.cpp`)
1.  **Initialize**: Seed RNG, pick number (1-100), reset attempts.
2.  **Prompt**: Ask user for input.
3.  **Validate**: Check against secret number.
    - If `Guess > Secret`: Print "Too high".
    - If `Guess < Secret`: Print "Too low".
    - If `Guess == Secret`: Print "Success" and break loop.
4.  **Repeat**: Return to step 2.

## Setup & Compilation

### Prerequisites
- Standard C++ Compiler

### Build Instructions
1.  **Navigate directly**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\C++\NumberGuessingGame"
    ```
2.  **Compile**:
    ```powershell
    g++ main.cpp -o guessing_game
    ```
3.  **Run**:
    ```powershell
    .\guessing_game
    ```

## Web Demo Usage
- Open `demo.html` in a versatile web browser.
- **Type**: Enter a number in the input box.
- **Guess**: Click "Guess!" or press Enter.
- **Read Hint**: Adjust your next guess based on the feedback.
- **Reset**: Click "New Game" to play again without losing your high score.
