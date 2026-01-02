# Simple Music Player Documentation

**Category**: C++ Systems
**Path**: `C++/SimpleMusicPlayer`
**Version**: 1.0

## Overview
The **Simple Music Player** is a unique demonstration of hardware interaction using only standard C++ libraries and the Windows API. It converts arrays of frequency data (Hz) and duration (ms) into audible square waves using the system's buzzer or speaker, effectively playing a monophonic melody directly from the code.

## Key Features

### 1. C++ Hardware Audio (beep.h)
- **Direct Hardware Control**: Utilizes the `Windows.h` library's `Beep(frequency, duration)` function to control the PC speaker.
- **Frequency Mapping**: Defines constant integer values for musical notes (e.g., `NOTE_C4 = 261` Hz).
- **Sequencing**: Stores the song data in two parallel arrays:
  - `melody[]`: The sequence of notes to play.
  - `durations[]`: How long each note lasts in milliseconds.
- **Console Feedback**: Prints the current note being played to the console for visual debugging.

### 2. Web Demo (Mock Interface)
Since browsers cannot access the system BIOS speaker directly, the web demo simulates a modern "Music Player" interface:
- **Rich UI**: Features a glassmorphism-inspired design with album art, progress bar, and volume controls.
- **Playlist Management**: Displays a list of mock tracks ("Synthwave Dreams", "Neon Nights").
- **State Management**: Handles Play/Pause, Next/Previous, and seeking via Javascript logic.
- **Visualizations**: CSS animations rotate the album art when music is "playing".

## Architecture

### Directory Structure
```
SimpleMusicPlayer/
├── main.cpp    # C++ Hardware Player
└── demo.html   # Web-based UI Simulation
```

### Constraints
- **Platform**: The C++ code is specific to Windows (`<windows.h>`) because `Beep` is a Windows API function. It will not compile on Linux/macOS without modification (e.g., using `ncurses` or system calls).
- **Sound Quality**: The C++ version produces simple square wave "beeps", reminiscent of early 1980s computers.

## Setup & Compilation

### Prerequisites
- Windows OS (Required for `Beep`)
- Standard C++ Compiler (MinGW/MSVC)

### Build Instructions
1.  **Navigate directly**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\C++\SimpleMusicPlayer"
    ```
2.  **Compile**:
    ```powershell
    g++ main.cpp -o music_player
    ```
3.  **Run**:
    ```powershell
    .\music_player
    ```
    *Warning: Ensure your system volume is on but not maximum, as system beeps can be loud.*

## Web Demo Usage
- Open `demo.html` in a versatile web browser.
- **Play/Pause**: Click the large Play button.
- **Navigate**: Click Next/Prev or select a track from the playlist.
- **Seek**: Click anywhere on the progress bar to jump to that time.
