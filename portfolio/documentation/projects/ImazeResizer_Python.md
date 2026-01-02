# Image Resizer Documentation

**Category**: Python Systems / GUI
**Path**: `Python/ImazeResizer`
**Version**: 1.0

## Overview
The **Image Resizer** is a powerful desktop application built with `Tkinter` and `Pillow` (PIL) that simplifies the process of resizing images. Unlike basic resizers, it offers three advanced modes: scaling by **percentage**, setting exact **pixel dimensions**, or targeting a specific **file size in KB/MB**. It features a modern, clean UI with real-time previews and aspect ratio locking.

## Key Features

### 1. Python Desktop App (`ImageResizer.py`)
- **Three Resize Modes**:
  1.  **Dimensions**: Enter exact Width/Height (supports Aspect Ratio locking).
  2.  **Percentage**: Scale up or down by a % factor.
  3.  **Target File Size**: *Novel Feature* - Iteratively estimates the resolution needed to hit a target filesize (e.g., "Resize this to exactly 500KB").
- **High-Quality Resampling**: Uses `LANCZOS` filtering to ensure images remain sharp after resizing.
- **Format Support**: Handles `.jpg`, `.png`, `.bmp`, `.tiff`, and `.webp`.
- **Quality Control**: Allows users to set JPEG compression quality (1-100) when saving.
- **Preview System**: Shows a thumbnail of the image and updates the "Output Dimensions" label before processing to prevent errors.

### 2. Web Demo
The web simulation replicates the desktop experience:
- **Interactive Controls**: Sliders for "Scale" and "Quality" replace static text inputs for a smoother demo experience.
- **Dynamic Calculation**: Instantly calculates and displays the new `Width x Height` as you drag sliders.
- **Visual Feedback**: Clicking "Resize" triggers a success animation and summary card.

## Architecture

### Directory Structure
```
ImazeResizer/
├── ImageResizer.py # Full Desktop Application
└── demo.html       # Web Simulation
```

### Core Logic (Target Size)
How do we resize to a specific file size (e.g., 500KB)?
Since file size depends on compression, it’s impossible to predict exactly. The app uses a heuristic:
$$ ScaleFactor = \sqrt{\frac{TargetSize}{CurrentSize}} $$
This provides a close approximation for the initial resize operation.

## Setup & Execution

### Prerequisites
- Python 3.x
- Pillow (`pip install Pillow`)
- Tkinter (Standard)

### Running the App
1.  **Navigate**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\Python\ImazeResizer"
    ```
2.  **Run**:
    ```powershell
    python ImageResizer.py
    ```

### Expected Output
A GUI window will open.
1.  Click **Select Image** to load a file.
2.  Choose **Resize Mode** (e.g., "File Size" -> "500 KB").
3.  Click **Resize Image**.
4.  Preview updates. Click **Save As...** to export.

## Web Demo Usage
- Open `demo.html` in a web browser.
- **Load**: Click the placeholder box to load a "Demo Image".
- **Adjust**: Switch to "Percent" tab and drag the slider to 50%.
- **Verify**: Observe the "Output: 960 x 540" label change instantly.
