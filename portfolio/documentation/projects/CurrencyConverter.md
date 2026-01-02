# Currency Converter Documentation

**Category**: C++ Systems
**Path**: `C++/CurrencyConverter`
**Version**: 1.0

## Overview
The **Currency Converter** is a simple C++ utility designed to demonstrate fundamental programming concepts such as switch-case control structures, arithmetic operations, and console I/O formatting. It provides a text-based interface for converting between major global currencies.

## Key Features

### 1. Core Logic
- **Fixed Exchange Rates**: Uses constant `double` values to define conversion rates (e.g., USD to EUR, EUR to USD, USD to INR).
- **Arithmetic Precision**: Utilizes `std::fixed` and `std::setprecision(2)` to ensure monetary values are displayed with two decimal places.
- **Menu System**: A persistent `while` loop displays a navigation menu, allowing multiple conversions until the user chooses to exit.

### 2. Supported Conversions (Console App)
1. **USD to EUR**
2. **EUR to USD**
3. **USD to INR**
4. **INR to USD**

### 3. Web Demo
- **Enhanced UI**: The `demo.html` file provides a modern, responsive interface for the same logic.
- **Bi-Directional**: Supports 5 currencies (USD, EUR, GBP, INR, JPY) with any-to-any conversion (unlike the limited pairs in the C++ version).
- **Features**:
  - Live conversion as you type.
  - "Swap" button to instantly reverse the `From` and `To` currencies.
  - Visual display of the current exchange rate (e.g., "1 USD = 0.92 EUR").

## Architecture

### Directory Structure
```
CurrencyConverter/
├── main.cpp    # C++ Source Code
└── demo.html   # Web-based interactive demo
```

### Code Structure (`main.cpp`)
- **`displayMenu()`**: Prints the available options to the console.
- **`main()`**:
  - Defines constants for exchange rates.
  - Enters an infinite loop handling user input.
  - Uses a `switch` statement to execute the selected conversion formula.
  - Validates input to ensure menu choices are within range (1-5).

## Setup & Compilation

### Prerequisites
- Standard C++ Compiler (GCC, Clang, or MSVC)

### Build Instructions
1.  **Navigate**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\C++\CurrencyConverter"
    ```
2.  **Compile**:
    ```powershell
    g++ main.cpp -o currency_converter
    ```
3.  **Run**:
    ```powershell
    .\currency_converter
    ```

## Web Demo Usage
- Open `demo.html` in a browser.
- Enter an amount in the left box.
- Select source and target currencies from the dropdowns.
- The result updates instantly in the right box.
