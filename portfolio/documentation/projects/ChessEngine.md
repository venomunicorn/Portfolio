# Chess Engine Documentation

**Category**: C++ Systems
**Path**: `C++/ChessEngine`
**Version**: 1.0 Lite

## Overview
The **Chess Engine** is a lightweight, console-based C++ application that simulates a standard game of chess. It implements board representation, piece logic, and basic movement validation. It serves as a foundational project for understanding 2D grid management, game state persistence, and turn-based logic.

## Key Features

### 1. Board Representation
- **8x8 Grid**: The board is represented as an 8x8 array of strings.
- **Piece Encoding**: Pieces are encoded with 2-character strings (e.g., `WP` for White Pawn, `BK` for Black King) or ` . ` for empty squares.
- **Console Visualization**: A text-based render of the board with row numbers (1-8) and column labels (a-h).

### 2. Game Mechanics
- **Turn-Based System**: Simulates alternating turns (White -> Black).
- **Move Logic**: Accepts algebraic notation (e.g., "e2" to "e4") to move pieces.
- **Core Rules**:
  - Initializes standard chess layout (Rooks, Knights, Bishops, Queen, King, Pawns).
  - Handles basic piece movement (updating `from` and `to` coordinates in the array).

### 3. Web Demo
- **Interactive GUI**: A web-based counterpart (`demo.html`) provides a visual, clickable interface.
- **Move Validation**: The web demo includes JavaScript logic to validate moves for all piece types (Pawn, Rook, Knight, Bishop, Queen, King).
- **Visual Feedback**: visual highlighting for selected pieces and valid move destinations.

## Architecture

### Directory Structure
```
ChessEngine/
├── main.cpp    # Core C++ implementation (Console)
└── demo.html   # Interactive Web Demo (GUI)
```

### Class Design (`main.cpp`)
- **`ChessBoard` Class**: Encapsulates the game state.
  - `board[8][8]`: Stores piece positions.
  - `setupBoard()`: Populates the initial state.
  - `printBoard()`: Renders the ASCII board to stdout.
  - `makeMove()`: Executes a move from one coordinate to another.

## Setup & Compilation

### Prerequisites
- C++ Compiler (g++, clang++, or MSVC)

### Build Instructions
1.  **Navigate to directory**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\C++\ChessEngine"
    ```
2.  **Compile**:
    ```powershell
    g++ main.cpp -o chess_engine
    ```
3.  **Run**:
    ```powershell
    .\chess_engine
    ```

## Web Demo Usage
- Open `demo.html` in any web browser.
- **Play**: Click a piece to select it (highlighted green), then click a valid destination square (highlighted semi-transparent green) to move.
- **Reset**: Use the "New Game" button to reset the board.
