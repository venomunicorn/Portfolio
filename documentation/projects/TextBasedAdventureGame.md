# Text-Based Adventure Game Documentation

**Category**: C++ Systems
**Path**: `C++/TextBasedAdventureGame`
**Version**: 1.0

## Overview
The **Text-Based Adventure Game** is an immersive interactive fiction engine implemented in C++. It demonstrates advanced control flow using state machines (via `switch-case`), object-oriented concepts (`Player` class), and inventory management to create a dungeon crawler experience entirely in the console.

## Key Features

### 1. C++ Logic
- **Object-Oriented Design**: Uses a `Player` class to encapsulate attributes like `name`, `health`, and state flags (`hasKey`).
- **State Machine**: The game loop uses a `switch` statement on `currentRoom` variables to manage navigation between different "rooms" (e.g., Entrance Hall, Armory, Dragon Chamber).
- **Conditional Progression**: Certain paths are locked behind conditions (e.g., unlocking a door requires finding a "Rusty Key" first).
- **Infinite Loop**: The game runs continuously until a win or loss condition breaks the `while` loop.

### 2. Web Demo
The web version transforms the linear console text into a rich graphical interface:
- **Rich Narrative**: Expanded storylines (lit tunnels vs. dark trap-filled tunnels) and branching paths.
- **Visual Stats**: Real-time dashboard showing Health bar, Gold count, and Inventory icons.
- **Dynamic Content**: Uses JavaScript objects to define "Scenes", where each scene contains title, description, and choices logic. 
- **Inventory System**: Players can find items (Swords, Potions) that unlock new choices later in the game (e.g., "Attack Dragon" is only successful if you have the Sword).

## Architecture

### Directory Structure
```
TextBasedAdventureGame/
├── main.cpp    # C++ Console Engine
└── demo.html   # Graphical Web RPG
```

### Game State Logic (`main.cpp`)
```cpp
switch(currentRoom) {
    case 1: // Start Room
        // Print description
        // Get input -> Change currentRoom to 2 or 3
        break;
    case 4: // Locked Room
        if (player.hasKey) {
             // Unlock and enter
        } else {
             // Deny entry
        }
        break;
}
```

## Setup & Compilation

### Prerequisites
- Standard C++ Compiler

### Build Instructions
1.  **Navigate directly**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\C++\TextBasedAdventureGame"
    ```
2.  **Compile**:
    ```powershell
    g++ main.cpp -o adventure
    ```
3.  **Run**:
    ```powershell
    .\adventure
    ```

## Web Demo Usage
- Open `demo.html` in a versatile web browser.
- **Read**: Follow the narrative in the central panel.
- **Choose**: Click buttons to make decisions (e.g., "Take the Lit Tunnel").
- **Manage**: Watch your Health and Inventory. If health drops to 0, it's Game Over.
- **Replay**: Restart to try different paths and find all secrets.
