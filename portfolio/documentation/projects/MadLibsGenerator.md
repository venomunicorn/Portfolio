# Mad Libs Generator Documentation

**Category**: C++ Systems
**Path**: `C++/MadLibsGenerator`
**Version**: 1.0

## Overview
The **Mad Libs Generator** is an interactive word game that prompts the user for various words (nouns, adjectives, verbs, etc.) to substitute into a pre-written story template. The C++ version runs in the console, demonstrating basic string input/output and user interaction logic.

## Key Features

### 1. C++ Console Application
- **Sequential Prompts**: Guides the user step-by-step through the required inputs (e.g., "Enter a noun", "Enter a verb").
- **String Manipulation**: Captures full lines of text using `std::getline` to allow for multi-word inputs (like "Giant Squid").
- **Template System**: The story structure is hardcoded but flexible enough to create humorous or nonsensical results based on user input.

### 2. Web Demo
The web version expands the concept significantly:
- **Multiple Stories**: Users can choose from 3 different templates ("A Day at School", "Space Adventure", "Dragon's Quest").
- **Dynamic Inputs**: The input form automatically regenerates based on the selected story's requirements.
- **Randomizer**: A "Random Words" button that fills the fields with pre-defined funny options for instant gratification.

## Architecture

### Directory Structure
```
MadLibsGenerator/
├── main.cpp    # C++ Implementation
└── demo.html   # Advanced Web Demo
```

### Code Logic (`main.cpp`)
- **Input Phase**:
  - Uses `std::getline(std::cin, variable)` to read inputs. This is preferred over `std::cin >> variable` because it captures spaces.
- **Output Phase**:
  - Concatenates the string literals (the story parts) with the user variables to print the final narrative.

## Setup & Compilation

### Prerequisites
- Standard C++ Compiler

### Build Instructions
1.  **Navigate directly**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\C++\MadLibsGenerator"
    ```
2.  **Compile**:
    ```powershell
    g++ main.cpp -o madlibs
    ```
3.  **Run**:
    ```powershell
    .\madlibs
    ```

## Web Demo Usage
- Open `demo.html` in a versatile web browser.
- **Select Story**: Choose a theme from the dropdown menu.
- **Fill Inputs**: Type words into the labeled boxes manually.
- **Auto-Fill**: Click "Random Words" to let the computer decide.
- **Generate**: Click "Generate Story" to read the created masterpiece.
