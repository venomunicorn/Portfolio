# 2D Arcade Game

An endless survival top-down shooter built with C++ and SFML.

## Quick Start

### Prerequisites
1. **Visual Studio 2022** (or 2019) with C++ Desktop Development workload
2. **vcpkg** package manager
3. **CMake** 3.16+

### Setup (One-Time)

```powershell
# 1. Install vcpkg (if not installed)
cd C:\
git clone https://github.com/microsoft/vcpkg.git
cd vcpkg
.\bootstrap-vcpkg.bat

# 2. Install SFML
.\vcpkg install sfml:x64-windows

# 3. Set environment variable (or use -DCMAKE_TOOLCHAIN_FILE each time)
setx VCPKG_ROOT "C:\vcpkg"
```

### Build

```powershell
cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\C++\2DArcadeGame"
mkdir build
cd build

# Configure with vcpkg toolchain
cmake .. -DCMAKE_TOOLCHAIN_FILE="C:\vcpkg\scripts\buildsystems\vcpkg.cmake"

# Build
cmake --build . --config Release

# Run
.\Release\2DArcadeGame.exe
```

## Features

| Category | Details |
|----------|---------|
| **Enemies** | Chaser, Shooter, Bomber (explodes), Tank |
| **Power-ups** | Health, Speed, RapidFire, Shield, ScoreBonus |
| **Boss** | Every 5 waves, 3 phases, 5 attack patterns |
| **Audio** | SFX + music with volume controls |
| **Persistence** | High scores, settings saved to AppData |

## Controls

| Key | Action |
|-----|--------|
| WASD / Arrows | Move |
| Space | Shoot |
| ESC | Pause |
| H | High Scores (menu) |
| S | Settings (menu) |

## Project Structure

```
src/
├── core/       # Game loop, camera, config
├── states/     # Title, Playing, GameOver, HighScore, Settings
├── entities/   # Player, Enemy, Projectile, PowerUp, Boss
├── systems/    # Collision, Input, Spawn
├── effects/    # ParticleSystem
├── audio/      # AudioManager
├── save/       # SaveManager (high scores, settings)
└── ui/         # HUD
```

## Audio Assets (Optional)

Place audio files in `assets/audio/`:
- `menu_music.ogg` - Title screen music
- `game_music.ogg` - Gameplay music  
- `boss_music.ogg` - Boss fight music
- `shoot.wav`, `hit.wav`, `explosion.wav`, `pickup.wav`, `powerup.wav`, `damage.wav`, `death.wav`, `select.wav`, `pause.wav`

The game handles missing audio files gracefully.

## 38 Source Files

Fully implemented with proper C++ architecture using state pattern, object pooling, and component-based design.
