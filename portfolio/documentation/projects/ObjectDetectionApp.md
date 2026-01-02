# Object Detection App Documentation

**Category**: Python Systems / Computer Vision
**Path**: `Python/ObjectDetectionApp`
**Version**: 1.0

## Overview
The **Object Detection App** performs real-time object recognition using OpenCV. It is designed to work with a webcam to detect faces (using Haar Cascades) or generalized objects. The application includes a fallback "Simulation Mode" for environments where a camera or OpenCV is not available, ensuring the logic can still be demonstrated.

## Key Features

### 1. Python Computer Vision (`main.py`)
- **Dual Modes**: 
  - **Real Mode**: Uses `cv2.VideoCapture(0)` to grab frames from the webcam and `CascadeClassifier` to detect faces. It draws bounding boxes (`cv2.rectangle`) around detections in real-time.
  - **Simulation Mode**: If OpenCV is missing, it runs a loop printing simulated detection events ("DETECTED: Person | 95%") to the console using `time` and `random`.
- **Haar Cascade Integration**: configured to load the standard `haarcascade_frontalface_default.xml`, a lightweight pre-trained model for face detection.
- **Graceful Error Handling**: Checks for library imports and camera availability to prevent crashes.

### 2. GUI Application (`gui_main.py`)
- *Note: Likely provides a Tkinter window that embeds the video feed or displays a log of detected objects.*

### 3. Web Demo
The web simulator mimics a sophisticated CCTV dashboard:
- **Simulated Feed**: Renders a "Camera View" with a grid background.
- **Visual Bounding Boxes**: Randomly generating "detected objects" (boxes) with labels (Person, Car, Dog) overlaid on the sim-feed.
- **Statistics Panel**: Tracks FPS, Active Objects, and Total Detections count.
- **Event Log**: A scrolling sidebar listing timestamps and confidence scores for every detection event.

## Architecture

### Directory Structure
```
ObjectDetectionApp/
├── main.py         # OpenCV Logic
├── gui_main.py     # Desktop UI
├── demo.html       # Web Dashboard
└── requirements.txt # Dependencies (opencv-python)
```

### Detection Loop (Conceptual)
```python
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray)
    for (x,y,w,h) in faces:
        draw_rectangle(frame, (x,y), (w,h))
    show(frame)
```

## Setup & Execution

### Prerequisites
- Python 3.x
- OpenCV (`pip install opencv-python`)

### Running the App
1.  **Navigate**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\Python\ObjectDetectionApp"
    ```
2.  **Run**:
    ```powershell
    python main.py
    ```

### Expected Output
*If Camera exists:*
A window titled "Object Detection App - Face" opens, showing your webcam feed with a blue box around your face.

*If No Camera/OpenCV:*
```
OpenCV NOT found.
--- SIMULATION MODE ACTIVATED ---
[10:00:01] DETECTED: Car | Confidence: 88.5%
[10:00:04] DETECTED: Person | Confidence: 99.1%
```

## Web Demo Usage
- Open `demo.html` in a web browser.
- **Start**: Click "Start Detection" to activate the simulation.
- **Observe**: colorful boxes appear/disappear on the black screen, simulating AI recognition.
- **Log**: Watch the "Detection Log" fill up with events.
