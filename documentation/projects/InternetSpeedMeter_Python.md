# Internet Speed Meter Documentation

**Category**: Python Scripting
**Path**: `InternetSpeedMeter`
**Version**: 1.0

## Overview
**Internet Speed Meter** is a sleek, Windows 11-styled desktop widget that monitors your real-time network upload and download speeds. Built with **PySide6**, it offers a modern aesthetic with transparency, gradients, and a "floating widget" experience.

## Key Features

### 1. Real-Time Monitoring
- **Live Updates**: Uses `psutil` to fetch network byte counters every second (configurable interval).
- **Dual Gauge**: Displays both Upload (Green) and Download (Blue) speeds simultaneously.

### 2. Modern UI/UX
- **Glassmorphism**: Features a semi-transparent, blur-backed window that integrates seamlessly with the Windows desktop.
- **Customizable**:
  - **Modes**: Compact (Mini widget) vs. Expanded (Detailed view).
  - **Styles**: Adjustable opacity, accent colors, and "Always on Top" behavior.

### 3. Usage History
- **Data Logging**: Records speed metrics over time.
- **Visual Charts**: Integrated `matplotlib` graphs show usage trends (e.g., peak usage hours).
- **Export**: Ability to save history logs to CSV for external analysis.

## Architecture

### File Structure
```
InternetSpeedMeter/
├── main.py              # Application Entry Point
├── network_monitor.py   # Background Thread for psutil polling
├── speed_widget.py      # Main UI Widget (PySide6)
├── settings_dialog.py   # Configuration Window
├── history_dialog.py    # Matplotlib Charts Window
└── styles.py            # QSS Stylesheets and Theme Constants
```

### Dependencies
- `PySide6`: Qt for Python framework for the GUI.
- `psutil`: For cross-platform system monitoring.
- `matplotlib`: For rendering history graphs.

## Usage Guide

### Running the App
1.  Navigate to the project directory.
2.  Install dependencies: `pip install -r requirements.txt`.
3.  Run the main script:
    ```bash
    python main.py
    ```

### Controls
- **Move**: Click and drag anywhere on the widget to reposition it.
- **Context Menu**: Right-click the system tray icon to access:
  - **Settings**: Configure network adapter and colors.
  - **History**: View usage graphs.
  - **Quit**: Exit the application.
- **Shortcut**: `Ctrl+Shift+S` to toggle visibility.
