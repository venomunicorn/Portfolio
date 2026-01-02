# Project Tracker Pro Documentation

**Category**: Python Scripting
**Path**: `ProjectTracker`
**Version**: 3.0 (Production)

## Overview
**Project Tracker Pro** is a comprehensive, production-grade desktop application for task and project management. Built with **PySide6**, it rivals commercial tools with its modern "glassmorphic" UI, advanced analytics, and productivity features like a command palette and focus mode. It is designed for power users who want local, privacy-focused project tracking.

## Key Features

### 1. Productivity Suite
- **Command Palette (`Ctrl+K`)**: A Spotlight-like launcher to execute commands (e.g., "New Project", "Toggle Theme") instantly.
- **Focus Mode**: Hides all distractions, showing only the active task and a timer.
- **Pomodoro Timer**: Integrated 25-minute timer with break notifications and time logging directly against projects.

### 2. Advanced Project Management
- **Dashboard**: "GitHub-style" contribution heatmap and progress statistics.
- **Sub-Tasks**: Nested task lists that automatically calculate the parent project's completion percentage.
- **Templates**: Save project structures (tags, sub-tasks) as reusable templates.
- **Rich Text**: Markdown editor for project descriptions with live preview.

### 3. Professional UI/UX
- **HUD Overlay (`Ctrl+H`)**: An "Always-on-Top" floating mini-window to keep track of active tasks without opening the full app.
- **System Tray**: Minimizes to tray with quick actions context menu.
- **Themes**: Full Dark/Light mode support with acrylic/glass visual effects.

## Architecture

### File Structure
The project is structured as a modular application:
```
ProjectTracker/
├── project_tracker_enhanced.py  # Main Entry Point (Production)
├── Data/                        # Local Storage (JSON)
├── Feature Modules/             # Logic Separation
│   ├── command_palette.py       # Fuzzy search & execution
│   ├── statistics_dashboard.py  # Matplotlib/PySide charts
│   ├── hud_overlay.py           # Floating window logic
│   └── ... (70+ files)
└── tests/                       # Comprehensive pytest suite
```

### Data Storage
- **Local JSON**: All data is stored in `~/.project_tracker/projects_data.json` for privacy and portability.
- **Automatic Backups**: Creates timestamped snapshots in `history/` every 30 seconds.

## Usage Guide

### Getting Started
1. Install dependencies: `pip install -r requirements-prod.txt`.
2. Launch the app: `python project_tracker_enhanced.py`.
3. Follow the interactive **Onboarding Tutorial** on first launch.

### Performance
- Optimized for handling 100+ concurrent projects.
- Uses lazy loading and skeleton screens for instant startup feel.

### Building for Distribution
The project includes fully configured build scripts for creating standalone executables:
- **Windows**: Run `build.bat` to generate `ProjectTracker.exe`.
- **macOS/Linux**: Run `./build.sh` to create binaries or AppImages.
