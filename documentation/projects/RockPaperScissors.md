# Rock Paper Scissors Documentation

**Category**: C++ Systems
**Path**: `C++/RockPaperScissors`
**Version**: 1.0

## Overview
The **Rock Paper Scissors** project is a classic console-based game implemented in C++. It demonstrates the use of random number generation for simple AI logic, conditional statements for determining game outcomes, and loops for continuous play.

## Key Features

### 1. C++ Console Game
- **Random AI**: The computer randomly selects Rock, Paper, or Scissors using `std::rand()` seeded with the current time.
- **Game Logic**: Implements standard rules:
  - Rock beats Scissors
  - Paper beats Rock
  - Scissors beats Paper
- **Interactive Menu**: Users select their move via a numbered menu (1-3) or choose to quit (4).
- **Infinite Play**: The game runs in a `while(true)` loop until the user explicitly decides to exit.

### 2. Web Demo
The web version provides a modern, graphical interface for the same game logic:
- **Visual Feedback**: Uses emoji icons (🪨, 📄, ✂️) to represent moves.
- **Battle Arena**: Highlights the player's choice versus the computer's choice side-by-side.
- **Scoreboard**: Tracks Wins, Losses, and Ties in real-time without refreshing the page.
- **Animations**: Hover effects and result styling (Green for Win, Red for Loss) enhance the user experience.

## Architecture

### Directory Structure
```
RockPaperScissors/
├── main.cpp    # C++ Implementation
└── demo.html   # Graphical Web Demo
```

### Code Logic (`main.cpp`)
- **Input Handling**: Reads an integer (1-4). Includes basic validation to catch numbers outside this range.
- **Outcome Determination**: A series of `if-else if` blocks compare the user's choice against the computer's generated choice.
  ```cpp
  if (user == computer) tie;
  else if (user wins condition) win;
  else lose;
  ```

## Setup & Compilation

### Prerequisites
- Standard C++ Compiler

### Build Instructions
1.  **Navigate directly**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\C++\RockPaperScissors"
    ```
2.  **Compile**:
    ```powershell
    g++ main.cpp -o rps
    ```
3.  **Run**:
    ```powershell
    .\rps
    ```

## Web Demo Usage
- Open `demo.html` in a versatile web browser.
- **Play**: Click one of the three large icons (Rock, Paper, or Scissors).
- **Result**: Instantly see the outcome and updated score.
- **Reset**: Use the "Reset Stats" button to clear the scoreboard.
