# Modern Clock App Documentation

**Category**: Python GUI
**Path**: `Python/Clock`
**Version**: 1.0

## Overview
The **Modern Clock App** is a feature-rich productivity suite built with Python's Tkinter library. It goes beyond a simple digital clock, integrating a Pomodoro timer, Stopwatch with lap functionality, and a dedicated Study Session manager. The UI features a clean, pastel-themed design with custom-drawn components like rounded buttons and gradient backgrounds to overcome standard Tkinter limitations.

## Key Features

### 1. Python Desktop App (`clock.py`)
- **Digital Clock**: Shows real-time system time, date, and timezone.
- **Pomodoro Timer**: Implements the standard 25/5-minute work/break cycle to boost productivity.
- **Stopwatch**: Precise timing with milliseconds and a scrollable lap history.
- **Study Session Timer**: A long-form timer (e.g., 4-hour sessions) with a visual progress bar.
- **Custom UI Components**:
  - `create_gradient_frame`: Dynamically draws gradients on HTML5 Canvas equivalents.
  - `create_rounded_button`: Custom shape rendering for modern button aesthetics.
- **Threading**: Uses non-blocking loops (`mainloop`) and scheduled callbacks (`.after()`) to ensure the UI remains responsive while updating timers 60 times a second.

### 2. Web Demo
The web simulation packs the same core functionality into a tabbed interface:
- **Responsive Tabs**: Switch between Clock, Pomodoro, and Stopwatch views instantly.
- **Live JS Clock**: Updates local time every second.
- **Visual Timers**: Color-coded countdowns (Green for focus, Amber for breaks).
- **Interactive Stopwatch**: Start/Stop/Lap controls with a dynamically updating list of lap times.

## Architecture

### Directory Structure
```
Clock/
├── clock.py        # Full Tkinter Desktop Application
└── demo.html       # Web-based Simulation
```

### UI Class Structure
```python
class ModernClockApp:
    def __init__(self):
        self.pomodoro_running = False
        self.stopwatch_elapsed = 0
        self.colors = {'primary': '#667eea', ...}
        
    def setup_ui(self):
        # Creates Notebook tabs
        
    def update_timers(self):
        # Called every 1 second
        # Updates Pomodoro, Stopwatch, and Study Session states
```

## Setup & Execution

### Prerequisites
- Python 3.x
- Tkinter (Standard with Python)

### Running the App
1.  **Navigate**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\Python\Clock"
    ```
2.  **Run**:
    ```powershell
    python clock.py
    ```

### Expected Output
A new window titled "Modern Desktop Clock" will appear with four tabs:
1.  **Digital Clock**: Current time on a gradient background.
2.  **Pomodoro Timer**: Large 25:00 countdown.
3.  **Stopwatch**: 00:00:00 with Start/Lap buttons.
4.  **Study Session**: Long-duration timer.

## Web Demo Usage
- Open `demo.html` in a web browser.
- **Nav**: Click tabs to switch tools.
- **Pomodoro**: Click Start to begin a 25-minute focus session.
- **Stopwatch**: Use the "Lap" button to record splits without stopping the timer.
