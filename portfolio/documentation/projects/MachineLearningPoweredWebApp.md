# Neuro Vision - ML Web App Documentation

**Category**: Web Development
**Path**: `Web/MachineLearningPoweredWebApp`
**Version**: 1.0

## Overview
**Neuro Vision** is a client-side Machine Learning application that runs a pre-trained image classification model (MobileNet) directly in the browser using TensorFlow.js. It allows users to upload images or capture photos via webcam to instantly identify objects with confidence scores.

## Key Features

### 1. In-Browser Computer Vision
- **TensorFlow.js**: Loads the MobileNet v2 model remotely. No backend server is required for inference; all processing happens on the user's device.
- **Real-time Visualization**: Displays a "scanning" animation while the tensors are being processed, breaking down the analysis stages (Initializing → Extracting Features → Computing Probabilities).

### 2. Multi-Source Input
- **Drag & Drop**: Users can drop image files directly onto the analyzer zone.
- **File Upload**: Supports standard image formats (JPG, PNG).
- **Camera Integration**: Accesses the device's webcam (`navigator.mediaDevices.getUserMedia`) to capture live snapshots for analysis.

### 3. Analysis Results
- **Top 5 Predictions**: Returns the 5 most likely classes for the image, displayed with probability bars (e.g., "Golden Retriever: 98.5%").
- **History Tracking**: Automatically saves the last 10 scans to `localStorage`, including a thumbnail and timestamp, allowing users to revisit previous results.

### 4. Export Data
- **JSON Download**: Users can export the classification results for further analysis or record-keeping.

## Architecture

### File Structure
```
MachineLearningPoweredWebApp/
├── index.html      # UI Layout: Drop zone, Camera modal, Results card
├── style.css       # Technology-inspired futuristic styling
└── script.js       # TensorFlow.js integration, Camera logic, History
```

### Dependencies
- **TensorFlow.js** (`@tensorflow/tfjs`): The core ML library.
- **MobileNet** (`@tensorflow-models/mobilenet`): The pre-trained classification model.
*Both are loaded via CDN in `index.html`.*

### Logic Flow
1.  **Init**: Load MobileNet model (displayed via status indicator).
2.  **Input**: User provides image (File or Camera).
3.  **Preprocessing**: Image is read into an HTMLImageElement.
4.  **Inference**: `model.classify(img, 5)` returns an array of predictions.
5.  **Render**: Results are formatted into HTML bars.

## Usage Guide

### First Run
1.  Open `index.html`.
2.  Wait for the "Model Status" indicator in the top right to turn **Green (Ready)**. This may take a few seconds depending on internet speed.

### Analyzing an Image
1.  **Click to Upload** or Drag an image into the center box.
2.  The "Scanning" overlay will appear.
3.  View the results card below.

### Using the Camera
1.  Click the **Camera Icon** button.
2.  Allow browser permission for the camera.
3.  Frame your subject and click **"Capture"**.
