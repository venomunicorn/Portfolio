# 2D Arcade Game Documentation

**Category**: C++ Systems
**Path**: `C++/2DArcadeGame`

## Overview
The **2D Arcade Game** is a feature-rich, endless survival top-down shooter built using **C++** and the **SFML** (Simple and Fast Multimedia Library). It demonstrates advanced game development concepts such as state management, entity-component design, particle systems, and persistent data storage.

## Key Features

### 1. Game Mechanics
- **Player Control**: Smooth WASD movement and mouse-aiming mechanics.
- **Combat System**: Projectile-based shooting with collision detection.
- **Enemy Variety**:
  - **Chaser**: Follows the player directly.
  - **Shooter**: Fires projectiles at the player.
  - **Bomber**: Explodes on proximity or death.
  - **Tank**: High health, slow moving.
- **Boss Battles**: Occur every 5 waves. The boss has 3 distinct phases and 5 complex attack patterns.

### 2. Power-Up System
collectible items that drop during gameplay:
- **Health**: Restores HP.
- **Speed**: temporarily boosts movement speed.
- **RapidFire**: Increases shooting rate.
- **Shield**: Provides temporary invulnerability.
- **ScoreBonus**: Grants extra points.

### 3. Technical Systems
- **State Machine**: Clean transition between Title, Playing, GameOver, HighScore, and Settings states.
- **Particle System**: Visual effects for explosions, hits, and thrusters.
- **Audio Manager**: Handles background music (Menu, Game, Boss) and sound effects (Shoot, Hit, Explosion).
- **Save System**: Persists high scores and user settings to the local AppData folder using JSON or binary serialization.

## Architecture

### Directory Structure
```
src/
├── core/       # Core engine components (Game loop, Window, Camera)
├── states/     # Game State implementations (MainMenu, GameState, etc.)
├── entities/   # Game objects (Player, Enemy, Boss)
├── systems/    # Logic systems (Collision, Input, Spawning)
├── effects/    # Visual effects (Particles)
├── audio/      # Sound and Music management
├── save/       # Data persistence
└── ui/         # Heads-Up Display (HUD) and Menus
```

### Dependencies
- **SFML**: Graphics, Windowing, Audio, System.
- **CMake**: Build automation.
- **Vcpkg**: Dependency management.

## Setup & Compilation

### Prerequisites
- Visual Studio 2019/2022 (C++ workload)
- CMake 3.16+
- Vcpkg (for SFML)

### Build Instructions
1.  **Install SFML via vcpkg**:
    ```powershell
    .\vcpkg install sfml:x64-windows
    ```
2.  **Generate Project**:
    ```powershell
    mkdir build && cd build
    cmake .. -DCMAKE_TOOLCHAIN_FILE="<path_to_vcpkg>/scripts/buildsystems/vcpkg.cmake"
    ```
3.  **Compile**:
    ```powershell
    cmake --build . --config Release
    ```
4.  **Run**:
    Launch `2DArcadeGame.exe` from the `Release` folder.

## Controls
- **WASD / Arrows**: Move Player
- **Space / Left Click**: Shoot
- **ESC**: Pause Game
- **H**: View High Scores (from Menu)
- **S**: Open Settings (from Menu)
