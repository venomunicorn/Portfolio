# Mad Libs Generator Documentation

**Category**: Python Games / Strings
**Path**: `Python/MadLibsGenerator`
**Version**: 1.0

## Overview
The **Mad Libs Generator** is a classic word game implemented in Python. It prompts users to enter various parts of speech (nouns, verbs, adjectives) and inserts them into a pre-written story template. The result is often a humorous or nonsensical narrative. This project demonstrates string manipulation, input handling, and basic function management in Python.

## Key Features

### 1. Python Game Logic (`main.py`)
- **Multiple Stories**: Contains a collection of unique story templates (Magical Forest, Space Mission, Pizza creation).
- **Interactive Prompts**: Asks specific questions like "Enter a noun (plural)" to ensure the grammar of the final story makes sense (mostly).
- **String Formatting**: Uses Python's f-strings (`f"One day, a {adj} wizard..."`) to seamlessly inject user input into the text.
- **Menu System**: A simple `while` loop allows players to replay different stories without restarting the program.

### 2. GUI Application (`gui_main.py`)
- *Note: Likely provides a windowed interface where inputs are text fields and the final story is displayed in a large text box.*

### 3. Web Demo
The web simulation offers a rich, interactive experience:
- **Story Selector**: 5 distinct themes (Vacation, Space, Fantasy, Mystery, Food) switchable via tabs.
- **Dynamic Forms**: The input fields change automatically based on the selected story (e.g., "Alien Name" for Space vs. "Chef" for Food).
- **Randomize Button**: Auto-fills all fields with silly words for instant fun.
- **Highlighting**: The generated story highlights the user-inserted words in green to make them stand out.

## Architecture

### Directory Structure
```
MadLibsGenerator/
├── main.py         # Console Game
├── gui_main.py     # Desktop UI
└── demo.html       # Web Game
```

### Variable Injection
The core logic relies on replacing placeholders.
- **Python**: Function-based approach where each story is a function `story_1()` that collects local variables and prints.
- **Web**: Uses a template string `"The {adjective} astronaut..."` and Javascript's `.replace()` method to swap keys for values.

## Setup & Execution

### Prerequisites
- Python 3.x

### Running the Console App
1.  **Navigate**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\Python\MadLibsGenerator"
    ```
2.  **Run**:
    ```powershell
    python main.py
    ```

### Expected Output
```
Welcome to the Ultimate Mad Libs Generator!
Menu:
1. Play Random Story
2. Choose Story
Enter choice: 1

--- Story: The Magical Forest ---
Enter an adjective: smelly
Enter a noun: toaster
Enter a verb (past tense): exploded

One day, a smelly wizard walked into a toaster. He exploded loudly...
```

## Web Demo Usage
- Open `demo.html` in a web browser.
- **Choose**: Click "Space" to load the sci-fi template.
- **Fill**: Type "Blorp" for Alien Name, "700" for Number.
- **Generate**: Click the button to read your story.
- **Shortcut**: Use "Random Words" if you lack inspiration.
