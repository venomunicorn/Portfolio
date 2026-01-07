# File Encryption Documentation

**Category**: C++ Systems
**Path**: `C++/FileEncryption`
**Version**: 1.0

## Overview
The **File Encryption** suite is a security-focused project that implements symmetric encryption algorithms to protect file contents. The core C++ application demonstrates file I/O operations with binary stream manipulation using a simple XOR cipher.

## Key Features

### 1. C++ Implementation
- **XOR Cipher**: Implements a lightweight symmetric encryption algorithm. The same key is used for both encryption and decryption.
- **Binary Stream Processing**: Reads input files byte-by-byte using `std::ifstream` in binary mode to ensure non-text files (images, binaries) can also be processed without corruption.
- **Key Management**: Accepts a single-character key for simplicity in the console version.
- **Self-Test Utility**: Automatically generates a `secret.txt` file for immediate testing if one doesn't exist.

### 2. Supported Algorithms (Web Demo)
The web-based demo expands on the C++ concepts by implementing three distinct methods:
1.  **Caesar Cipher**: Shifts characters by a numeric 'n' positions (Classic substitution).
2.  **XOR Cipher**: Bitwise XOR operation with a multi-character key string. Output is hex-encoded for copy-paste safety.
3.  **Base64**: Standard encoding scheme (technically encoding, not encryption, but useful for obfuscation).

### 3. Web Demo Interface
- **Dual Mode**: Toggle between "Encrypt" and "Decrypt" modes.
- **Algorithm Selector**: Dropdown to switch between the three supported methods.
- **Dynamic Key Input**: The input field adapts based on the selected algorithm (e.g., Numeric shift for Caesar, Text key for XOR, Disabled for Base64).
- **Result Display**: Clear visual output box for the processed text.

## Architecture

### Directory Structure
```
FileEncryption/
├── main.cpp    # C++ File Encryption Tool
└── demo.html   # Multi-algorithm Web Demo
```

### Encryption Logic (`main.cpp`)
```cpp
// The core logic loops through every byte
char ch;
while (fin.get(ch)) {
    fout.put(ch ^ key); // XOR operation
}
```
This simplicity allows the encryption of any file type, not just text.

## Setup & Compilation

### Prerequisites
- Standard C++ Compiler

### Build Instructions
1.  **Navigate directly**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\C++\FileEncryption"
    ```
2.  **Compile**:
    ```powershell
    g++ main.cpp -o encryptor
    ```
3.  **Run**:
    ```powershell
    .\encryptor
    ```

### Usage (Console)
1.  Run the program.
2.  Enter input filename (e.g., `secret.txt`).
3.  Enter output filename (e.g., `encrypted.dat`).
4.  Enter a single character key (e.g., `K`).
5.  To decrypt, run again, select `encrypted.dat` as input, and use the same key.

## Web Demo Usage
- Open `demo.html` in a versatile web browser.
- Select "Encrypt" or "Decrypt".
- Choose your algorithm.
- Enter text and a key (if required).
- Click the action button to see the results.
