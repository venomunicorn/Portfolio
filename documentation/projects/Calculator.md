# Scientific Calculator Documentation

**Category**: Python Systems / GUI
**Path**: `Python/Calculator`
**Version**: 1.0

## Overview
The **Scientific Calculator** project is a comprehensive mathematical tool implemented in Python. It supports not just basic arithmetic but also advanced scientific functions like trigonometry, logarithms, and exponentiation. The project includes a history feature to track recent calculations, making it suitable for complex workflows.

## Key Features

### 1. Python Logic (`main.py`)
- **Arithmetic**: Addition, subtraction, multiplication, division (with zero-check).
- **Scientific Functions**:
  - **Trigonometry**: `sin`, `cos`, `tan` (Inputs in degrees).
  - **Exponents & Roots**: `power` ($x^y$), `sqrt` ($\sqrt{x}$).
  - **Logarithms**: Base-10 log validation.
- **History Tracking**: Stores the last 5 operations in a list and allows the user to recall them via the menu.
- **Input Handling**: Robust error catching for non-numeric inputs and mathematical errors (like division by zero).

### 2. GUI Application (`gui_main.py`)
- *Note: Provides a desktop graphical interface using Tkinter or PyQt, offering a standard grid layout for buttons.*

### 3. Web Demo
The web-based calculator mimics a physical scientific calculator:
- **Glassmorphism UI**: Semi-transparent design with a glowing backdrop.
- **Scientific Keypad**: dedicated row for `sin`, `cos`, `tan`, `log`, `ln`, `√`, `x²`, and `π`.
- **Live Display**: Shows the current input and the operation history above it (e.g., "50 * 2 =").
- **Smart Formatting**: Automatically handles decimal precision to avoid floating-point artifacts (e.g., displaying `0.3000000004` as `0.3`).

## Architecture

### Directory Structure
```
Calculator/
├── main.py         # CLI Calculator Logic
├── gui_main.py     # Desktop GUI Calculator
└── demo.html       # Web-based Scientific Calculator
```

### Class Design (`Calculator` in `main.py`)
Encapsulates logic to prevent global state pollution:
```python
class Calculator:
    def __init__(self):
        self.history = []
    def add(self, a, b): ...
    def sin(self, a): ...
```
This makes the code reusable in other projects (like a finance app).

## Setup & Execution

### Prerequisites
- Python 3.x

### Running the Console App
1.  **Navigate**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\Python\Calculator"
    ```
2.  **Run**:
    ```powershell
    python main.py
    ```

### Expected Output
```
Welcome to the Advanced Python Calculator!
Options:
1. Add
...
7. Sin
10. Log
Entered choice: 1
Enter first number: 10
Enter second number: 5
Result: 15.0
```

## Web Demo Usage
- Open `demo.html` in a web browser.
- **Basic Math**: Use the number pad and operators (+, -, ×, ÷).
- **Scientific**: Click `sin` then enter `90` to calculate $\sin(90^\circ)$.
- **Constants**: Use `π` for high-precision Pi calculations.
