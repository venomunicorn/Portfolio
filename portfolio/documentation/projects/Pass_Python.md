# SecurePass Manager Documentation

**Category**: Python Systems / Crypto
**Path**: `Python/Pass`
**Version**: 1.0

## Overview
**SecurePass Manager** is a comprehensive password management solution that combines a strong password generator with an encrypted vault system. Unlike simple text storage, this application uses a multi-layered encryption approach (Caesar Cipher + XOR + Base64) to safely store credentials in a CSV file. It features a Tkinter GUI for easy management and a web demo for visualizing the generation process.

## Key Features

### 1. Python Security Core (`main.py`)
- **Advanced Encryption Layer**:
  1.  **Caesar Cipher**: Shifts characters to obfuscate the text ($+7$ shift).
  2.  **Base64 Encoding**: Converts binary data to text.
  3.  **XOR Cipher**: Encrypts the Base64 string against a hidden key ("SecurePass2024").
  4.  **Final Base64**: Ensures the saved string is alphanumeric and safe for CSV storage.
- **CSV Database**: Stores `[Username, EncryptedPassword, Date]` in `passwords.csv`, ensuring data persistence between sessions.
- **Generator**: Creates 4-50 character passwords using `random.SystemRandom` (cryptographically strong) with selectable character sets (Upper, Lower, Digits, Symbols).
- **Clipboard Integration**: Uses `pyperclip` to copy passwords immediately after generation or retrieval.

### 2. GUI Application (`main.py` - Tkinter)
- **Tabbed Interface**:
  - **Generator Tab**: Sliders for length, toggles for complexity, and "One-Click Copy".
  - **Storage Tab**: A list of saved accounts. Clicking a user allows you to "Retrieve" (decrypt) the password or "Delete" the entry.
- **Safety Checks**: Warns before overwriting existing usernames or deleting entries.

### 3. Web Demo
The web simulator focuses on the UX of password generation:
- **Strength Meter**: A dynamic bar that changes color (Red/Yellow/Green) and label (Weak/Strong) based on entropy criteria (Length > 12, Mix of chars).
- **Interactive Vault**: A mock "Saved Passwords" list lets users practice copying credentials or "peeking" at them (simulated via Alerts).
- **Toast Notifications**: "Copied to clipboard" popups confirm actions.

## Architecture

### Directory Structure
```
Pass/
├── main.py         # Full App (GUI + Crypto + Logic)
└── demo.html       # Web Simulation
```

### Encryption Flow
$$ Plain \xrightarrow{Shift+7} Caesar \xrightarrow{Base64} B64_1 \xrightarrow{XOR(Key)} XORed \xrightarrow{Base64} Stored $$

## Setup & Execution

### Prerequisites
- Python 3.x
- Libraries: `pyperclip` (`pip install pyperclip`)

### Running the App
1.  **Navigate**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\Python\Pass"
    ```
2.  **Run**:
    ```powershell
    python main.py
    ```

### Expected Output
A "SecurePass Manager" window appears.
- **Generate**: Go to "Password Generator", set length to 16, click "Generate".
- **Save**: Enter "MyGoogleAccount" as username, click "Save Password".
- **Retrieve**: Go to "Stored Passwords", click "Refresh", select "MyGoogleAccount", click "Retrieve". The decrypted password appears.

## Web Demo Usage
- Open `demo.html` in a web browser.
- **Test**: Drag the length slider to 24.
- **Observe**: The strength bar turns fully green.
- **Mock Store**: Click the "Copy" icon next to "GitHub" in the list below to simulate retrieving a saved password.
