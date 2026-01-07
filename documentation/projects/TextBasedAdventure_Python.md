# TextBasedAdventure Documentation

**Category**: Python Games / Interactive Fiction
**Path**: `Python/TextBasedAdventure`
**Version**: 1.0

## Overview
**The Cave Adventure** is a classic text-based interactive fiction game. It harkens back to the days of Zork, where players navigate a world described purely through text, making choices by typing commands like "north", "take key", or "open gate". The project implements a state-machine architecture to manage rooms, inventory, and conditional events.

## Key Features

### 1. Python Game Engine (`main.py`)
- **State Management**: A `GameState` class tracks the player's status:
  - **Location**: Which "scene" (function) is currently active.
  - **Inventory**: A list of acquired items (Rusty Key, Golden Gear, Diamond).
  - **Flags**: Tracks logic updates (e.g., `has_item` checks).
- **Scene System**: Each room (`scene_start`, `scene_forest_clearing`) is a standalone function that:
  1.  Clears the screen.
  2.  Prints the room description using a "typewriter effect" (`print_slow`).
  3.  Enters a `while` loop to handle user input specific to that room.
  4.  Returns the string name of the next room to transition to.
- **Puzzle Logic**:
  - You cannot open the Castle Gate without the *Rusty Key*.
  - You typically cannot use the Machine without the *Golden Gear*.
  - Finding the *Diamond* is a "secret ending" condition.

### 2. GUI Application (`gui_main.py`)
- *Note: Provides a graphical interface wrapper for the text game, likely responding to button clicks instead of typing.*

### 3. Web Demo
The web version modernizes the experience with a "Choose Your Own Adventure" UI:
- **Visual Stats**: Displays Health ❤️, Gold 💰, and Moves ⚡ counters.
- **Action Buttons**: Instead of typing, users click context-sensitive buttons (e.g., "🔦 Enter Cave", "⚔️ Fight Dragon").
- **Inventory System**: Items like "Ancient Sword" appear as badges in a dedicated panel.
- **Adventure Log**: A scrolling text history of actions ("You defeated the dragon!").

## Architecture

### Directory Structure
```
TextBasedAdventure/
├── main.py         # Console Engine
├── gui_main.py     # Desktop UI
└── demo.html       # Web Game
```

### Game Loop Pattern
```python
scenes = { 'start': scene_start, 'cave': scene_cave, ... }
while state.alive:
    # Execute current scene function & update location with its return value
    state.location = scenes[state.location](state)
```

## Setup & Execution

### Prerequisites
- Python 3.x

### Running the Game
1.  **Navigate**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\Python\TextBasedAdventure"
    ```
2.  **Run**:
    ```powershell
    python main.py
    ```

### Expected Output
```
You wake up in a cold, damp cave. It's dark.
To your NORTH is a faint light. To your EAST is a strange humming sound.

What do you do? (north/east/check inventory): 
```

### Walkthrough (Spoiler)
1.  Go **North** to Forest Clearing.
2.  **Take Key** to get the Rusty Key.
3.  Go **North** to Castle Gate.
4.  **Open Gate** using the key.
5.  Enter `castle_hall`.
