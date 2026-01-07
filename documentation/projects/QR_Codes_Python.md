# QR Code Generator Documentation

**Category**: Python Systems / Tools
**Path**: `Python/QR_Codes`
**Version**: 1.0

## Overview
The **QR Code Generator** is a fast and simple utility for converting text or URLs into Scannable 2D barcodes (Quick Response Codes). It utilizes the `qrcode` library in Python to handle the matrix encoding and generation logic. This tool is essential for sharing links, creating Wi-Fi access codes, or embedding text data into physical media.

## Key Features

### 1. Python QR Logic (`main.py`)
- **Quick Encode**: Takes user input (Text/URL) and uses `qrcode.QRCode()` to create the matrix.
  - *Version 1*: The smallest matrix size (21x21).
  - *ECC Level*: Low error correction (allows for cleaner codes with less redundancy).
- **Image Export**: Saves the generated code as `result_qr.png` using PIL.
- **ASCII Preview**: A unique feature that prints the QR code directly to the console/terminal using text characters, allowing for quick verification without opening the image file.
- **Fallback Mode**: If the `qrcode` library is missing, it runs in a "Simulation Mode" to prevent crashes and guide the user to install dependencies.

### 2. GUI Application (`gui_main.py`)
- *Note: Provides a desktop window allowing users to type text, choose a file save location, and potentially adjust colors before generating.*

### 3. Web Demo
The web simulator focuses on customization and immediate visual feedback:
- **Live Preview**: The QR code pattern updates instantly as you type in the text box.
- **Color Customization**: Users can pick custom Foreground and Background colors (e.g., Green on White) instead of standard Black/White.
- **Smart Presets**: One-click buttons to pre-fill common formats like "GitHub URL", "Phone Number", or "Plain Text".
- **Download**: A dedicated button to save the generated canvas as a PNG file.

## Architecture

### Directory Structure
```
QR_Codes/
├── main.py         # CLI Generator
├── gui_main.py     # Desktop GUI
├── demo.html       # Web Generator
└── requirements.txt # Dependencies (qrcode, pillow)
```

### Canvas Simulation
The web demo simulates QR generation logic using HTML5 Canvas `fillRect()`:
- It draws the three "Position Detection Patterns" (the squares in corners).
- It fills the data area based on a hash of the input text to mimic the appearance of a real QR code (Note: The web demo pattern is non-functional/simulated, whereas the Python script generates real scannable codes).

## Setup & Execution

### Prerequisites
- Python 3.x
- Libraries: `qrcode[pil]` (`pip install qrcode[pil]`)

### Running the App
1.  **Navigate**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\Python\QR_Codes"
    ```
2.  **Run**:
    ```powershell
    python main.py
    ```

### Expected Output
```
--- QR Code Generator ---
Enter text/URL to encode: https://google.com
Success! QR code saved to result_qr.png

Terminal Preview:
##############
#  ##  ##  #
#  ##  ##  #
...
```

## Web Demo Usage
- Open `demo.html` in a web browser.
- **Type**: Enter "Wifi Password: 123" into the text box.
- **Style**: Change Foreground color to Blue.
- **Save**: Click "Save as PNG" to download the image.
