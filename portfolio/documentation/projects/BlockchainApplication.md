# Blockchain Application Documentation

**Category**: Python Algorithms
**Path**: `Python/BlockchainApplication`
**Version**: 1.0

## Overview
The **Blockchain Application** (PyChain) is an educational Python implementation of a blockchain structure. It demonstrates the core concepts of decentralized ledgers including block creation, hashing, linking via previous hash pointers, and a basic Proof-of-Work (PoW) consensus algorithm.

## Key Features

### 1. Python Implementation (`main.py`)
- **Block Structure**: A `Block` class containing:
  - `index`: Position in the chain.
  - `timestamp`: Creation time.
  - `data`: Payload (e.g., transaction details).
  - `previous_hash`: Link to the preceding block.
  - `hash`: SHA-256 digital signature.
  - `nonce`: Number used once for mining.
- **SHA-256 Hashing**: Uses Python's `hashlib` to generate cryptographic signatures.
- **Proof of Work (Mining)**: Implements a difficulty target (leading zeros) that requires computational effort to solve.
- **Chain Validation**: A method to verify integrity by ensuring:
  - Each block's hash is valid.
  - Each block correctly points to the previous block's hash.

### 2. GUI Application (`gui_main.py`)
- *Note: This project includes a `gui_main.py` which likely provides a Tkinter or similar interface for desktop interaction, building upon the logic in `main.py`.*

### 3. Web Demo
The web demo provides a visual Block Explorer:
- **Interactive Mining**: Users can enter data and "Mine" a new block, watching the nonce increment until a valid hash is found.
- **Chain Visualization**: Renders blocks as connected cards showing Index, Hash, Previous Hash, and Data.
- **Validation Tool**: A button to check the integrity of the chain (simulating how nodes verify ledgers).
- **Genesis Block**: Automatically initializes the chain with block #0.

## Architecture

### Directory Structure
```
BlockchainApplication/
├── main.py         # Core Blockchain Logic
├── gui_main.py     # Desktop GUI Implementation
└── demo.html       # Visual Web Simulator
```

### Mining Logic (Proof of Work)
```python
while not computed_hash.startswith('0' * difficulty):
    block.nonce += 1
    computed_hash = block.calculate_hash()
```
This loop ensures that blocks cannot be spammed, simulating the security mechanism of Bitcoin.

## Setup & Execution

### Prerequisites
- Python 3.x

### Running the Console App
1.  **Navigate**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\Python\BlockchainApplication"
    ```
2.  **Run**:
    ```powershell
    python main.py
    ```

### Expected Output
```
--- PyChain v1.0 ---
Mining block 1...
Mining block 2...

Blockchain Valid? True

[Chain Details]
Index: 0
Hash: ...
Prev: 0
Data: Genesis Block
------------------------------
Index: 1
...
```

## Web Demo Usage
- Open `demo.html` in a web browser.
- **Add Data**: Enter text like "Alice pays Bob $50".
- **Mine**: Click "Mine Block" and wait for the simulated PoW.
- **Verify**: The block appears in the chain view.
