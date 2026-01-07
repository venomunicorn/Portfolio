# Sudoku Solver Documentation

**Category**: C++ Systems
**Path**: `C++/SudokuSolver`
**Version**: 1.0

## Overview
The **Sudoku Solver** is an algorithmic project implemented in C++ that demonstrates the power of the **Backtracking** technique. It takes a partially filled 9x9 Sudoku grid as input and recursively attempts to fill empty cells with numbers 1-9, backtracking whenever a rule violation is detected, until a valid solution is found.

## Key Features

### 1. Backtracking Algorithm (C++)
- **Recursive Logic**: The core function `solveSudoku` calls itself to fill the grid cell by cell.
- **Validation**: The `isSafe` function ensures every number placement adheres to Sudoku rules:
  - Unique in its row.
  - Unique in its column.
  - Unique in its 3x3 subgrid.
- **Efficiency**: Finds a solution for standard puzzles almost instantly by pruning invalid branches of the search tree early.

### 2. Web Demo
The web-based version implements the same logic in JavaScript to provide a visual, interactive experience:
- **Interactive Grid**: A 9x9 HTML input grid that accepts user input.
- **Input Validation**: Restricts input to single digits (1-9) to prevent errors.
- **Visual Feedback**:
  - **Preset Numbers**: Dark gray background (locked).
  - **Solved Numbers**: Green text (computed).
  - **Status Messages**: Displays "Solved successfully" or "No solution exists" clearly.
- **Example Loader**: A "Load Example" button to pre-fill the grid with a known solvable puzzle for quick testing.

## Architecture

### Directory Structure
```
SudokuSolver/
├── main.cpp    # C++ Optimization Algorithm
└── demo.html   # Web-based Interactive Solver
```

### Algorithm Flow (`main.cpp`)
1.  **Find Empty**: Locate the first cell with a `0`.
2.  **Try Numbers**: Iterate `num` from 1 to 9.
3.  **Check Safety**: If `isSafe(grid, row, col, num)` is true:
    - Place `num`.
    - Recurse: `solveSudoku(next_cell)`.
    - If recursion returns `true`, return `true` (Success).
4.  **Backtrack**: If recursion fails, reset cell to `0` and try next `num`.
5.  **Failure**: If no numbers work, return `false`.

## Setup & Compilation

### Prerequisites
- Standard C++ Compiler

### Build Instructions
1.  **Navigate directly**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\C++\SudokuSolver"
    ```
2.  **Compile**:
    ```powershell
    g++ main.cpp -o sudoku
    ```
3.  **Run**:
    ```powershell
    .\sudoku
    ```

## Web Demo Usage
- Open `demo.html` in a versatile web browser.
- **Enter Puzzle**: Type your Sudoku numbers into the grid.
- **Solve**: Click "Solve" to see the computer fill in the blanks.
- **Clear**: Reset the board to try a new puzzle.
