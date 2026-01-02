# Math Practice Pro

A comprehensive desktop application for practicing various math skills with adaptive difficulty and progress tracking.

## Features

- **Multiple Math Topics**: Addition, Subtraction, Multiplication, Division, Percentages, Fractions, Squares, Cubes, Cube Roots, and Multiplication Tables
- **Configurable Difficulty**: Adjust number ranges and complexity for each topic
- **Progress Tracking**: Detailed statistics and performance analytics
- **Achievement System**: Unlock badges and rewards for consistent practice
- **Data Export**: Export your progress to CSV files
- **Sound Effects**: Audio feedback for correct/incorrect answers
- **Adaptive Difficulty**: Optional mode that adjusts based on performance

## Installation

### Option 1: Run from Source
1. Install Python 3.7 or higher
2. Run: `python install_requirements.py`
3. Run: `python main.py`

### Option 2: Standalone Executable
1. Run: `python build_exe.py`
2. Find the executable in the `dist` folder
3. Double-click `MathPracticePro.exe` to run

## Usage

1. **Select Topics**: Choose which math topics to practice
2. **Configure Settings**: Adjust difficulty ranges in the Settings tab
3. **Start Quiz**: Click "Start Quiz" to begin
4. **Answer Questions**: Type your answers and press Enter or click Submit
5. **Track Progress**: View your statistics in the Progress tab
6. **Earn Achievements**: Complete challenges to unlock badges

## Data Storage

All progress and configuration data is stored locally in:
- `math_practice.db` - SQLite database for quiz results
- `config.json` - Configuration settings

## System Requirements

- Windows 7 or higher
- 100MB free disk space
- No internet connection required
