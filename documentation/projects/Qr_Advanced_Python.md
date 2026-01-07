# Advanced QR Code Generator Documentation

**Category**: Python Systems / Utilities
**Path**: `Python/Qr` (Script: `qrGen.py`)
**Version**: 2.0 (Advanced Edition)

## Overview
The **Advanced QR Code Generator** is a robust desktop application built with `tkinter`. Unlike the basic `QR_Codes` project, this version features a modern, split-pane UI, supports multiple data types (vCard, WiFi, Files), and includes **decoding capabilities** (reading QR codes from images). It is designed as a complete "QR Toolkit" for power users.

## Key Features

### 1. Multi-Format Generation
- **Text/URL**: Standard encoding.
- **vCard**: Create digital business cards (Name, Org, Phone, Email) readable by smartphones.
- **WiFi**: Generate "Join Network" codes (SSID, Password, WPA/WEP) for instant connection.
- **File Metadata**: Encode file info (Name, Size, MIME Type) into a QR code.

### 2. Built-in Decoder (Scanner)
- **Image Upload**: Users can select any image (`.png`, `.jpg`, `.bmp`) containing a QR code.
- **Auto-Detection**: Uses `pyzbar` and `cv2` (OpenCV) to locate and decode the QR pattern.
- **Data Viewer**: Displays the extracted text in a scrolling text box with "Copy to Clipboard" and "Save as Text" options.

### 3. Modern GUI (`qrGen.py`)
- **Split Layout**: Left panel for inputs/controls, right panel for large previews.
- **Live Preview**: High-resolution (300 DPI) rendering of the generated QR code on a Tkinter Canvas.
- **Auto-Save**: Automatically archives generated codes to a `QR_Codes/` folder with descriptive filenames (e.g., `wifi_HomeNetwork_20240828.png`).

## Architecture

### Dependencies
- **UI**: `tkinter`, `ttk`
- **QR Core**: `qrcode`, `PIL` (Pillow)
- **Computer Vision**: `cv2` (OpenCV), `pyzbar` (ZBar Barcode Reader)
- **Utilities**: `pyperclip` (Clipboard), `mimetypes`

### Class Structure `QRCodeApp(tk.Tk)`
- `setup_generate_tab()`: Builds the creation interface.
  - `create_input_fields(type)`: Dynamically swaps widgets (e.g., shows Password field only for WiFi).
  - `generate_qr_code()`: Validates input, constructs the payload string (e.g., `WIFI:S:MyNet;P:1234;;`), and renders the image.
- `setup_decode_tab()`: Builds the scanning interface.
  - `upload_qr_image()`: Loads image -> Grayscale -> `pyzbar.decode()` -> Text.

## Setup & Execution

### Prerequisites
- Python 3.x
- **Libraries**:
  ```powershell
  pip install qrcode[pil] opencv-python pyzbar pyperclip
  ```
- **System**: The `pyzbar` library may require the Visual C++ Redistributable on Windows.

### Running the App
1.  **Navigate**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\Python\Qr"
    ```
2.  **Run**:
    ```powershell
    python qrGen.py
    ```

### Usage Guide
1.  **Generate**:
    - Select **"📶 WiFi"**.
    - Enter SSID and Password.
    - Click **"🔄 Generate QR Code"**.
    - The code appears on the right. It is also auto-saved to the local folder.
2.  **Decode**:
    - Switch to **"Decode QR"** tab.
    - Click **"📁 Select Image File"**.
    - Open any QR image.
    - Read the decoded text in the **"Decoded Data"** box.
