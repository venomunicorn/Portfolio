# Currency Converter Documentation

**Category**: Python Systems / GUI
**Path**: `Python/CurrencyConverter`
**Version**: 1.0

## Overview
The **Currency Converter** is a financial utility tool built to demonstrate API handling or internal conversion logic in Python. It allows users to convert amounts between major world currencies (USD, EUR, GBP, INR, JPY, etc.) using predefined exchange rates, ensuring valid inputs and formatting the output cleanly.

## Key Features

### 1. Python Logic (`main.py`)
- **Dictionary-Based Rates**: Stores exchange rates relative to a base currency (USD) in a `self.rates` dictionary.
- **Two-Step Conversion**:
  1.  Convert Source Currency -> Base Currency (USD).
  2.  Convert Base Currency -> Target Currency.
  This allows conversion between ANY two supported currencies without needing $N^2$ exchange rate pairs.
- **Error Handling**: Validates that both source and target currency codes exist in the database and ensures the amount is non-negative.
- **Interactive Menu**: A text-based UI loop for continuous use.

### 2. GUI Application (`gui_main.py`)
- *Note: Offers a user-friendly window with Dropdown menus (Comboboxes) for selecting currencies, likely built with Tkinter.*

### 3. Web Demo
The web simulator offers a polished, responsive interface:
- **Live Calculation**: Updates the result instantly as you type numbers or change selections (`oninput` event).
- **Swap Function**: A dedicated button (⇅) to quickly reverse the "From" and "To" fields.
- **Rate Dashboard**: Displays a grid of current exchange rates against USD for quick reference.
- **Symbol Support**: Automatically detects and displays symbols ($, €, £, ₹) for better readability.

## Architecture

### Directory Structure
```
CurrencyConverter/
├── main.py         # CLI Logic
├── gui_main.py     # Desktop GUI
└── demo.html       # Web Simulation
```

### Conversion Algorithm
Formula used for converting Amount $A$ from currency $C_1$ to $C_2$:
$$ Result = \left( \frac{A}{Rate_{C1}} \right) \times Rate_{C2} $$
where $Rate_{CX}$ is the value of 1 USD in currency $X$.

## Setup & Execution

### Prerequisites
- Python 3.x

### Running the Console App
1.  **Navigate**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\Python\CurrencyConverter"
    ```
2.  **Run**:
    ```powershell
    python main.py
    ```

### Expected Output
```
Welcome to the Currency Converter!
Supported Currencies: USD, EUR, GBP, INR, ...

Menu:
1. Convert Currency
2. View Rates
Enter option: 1
Convert FROM: USD
Convert TO: INR
Enter amount in USD: 100

✅ 100.0 USD = 8350.0 INR
```

## Web Demo Usage
- Open `demo.html` in a web browser.
- **Input**: Enter "100" in the first box.
- **Select**: Choose "USD" on the left and "EUR" on the right.
- **Result**: View the calculated Euro amount instantly in the green box.
- **Swap**: Click the arrow circle to calculate how many USD you get for 100 EUR.
