# Payment Data Analysis Tool Documentation

**Category**: Python Systems / Data Analysis
**Path**: `Python/payment`
**Version**: 1.0

## Overview
The **Payment Data Analysis Tool** (implemented as `Payments.py`) is a comprehensive desktop application for analyzing bank transaction histories. It allows users to gain insights into their financial behavior through automated categorization, interactive charts, and detailed statistics. The tool is built using `tkinter` for the GUI and standard data science libraries (`pandas`, `matplotlib`) for processing and visualization.

## Key Features

### 1. Data Processing Engine
- **Flexible Import**: Loads transaction data from `.xlsx`, `.xls`, or `.csv` files.
- **Smart Categorization**: Automatically tags transactions based on keywords in the description.
  - *Example*: "Swiggy" → "🥘 Food & Dining", "Uber" → "🚖 Transport & Travel".
  - **Customizable Rules**: Users can edit the keyword dictionary directly in the settings tab.
- **Robust Cleaning**: Handles mixed date formats, cleans currency symbols (₹, $), and unifies amounts into numeric values.

### 2. Interactive Dashboard (GUI)
- **Summary Statistics**: Cards displaying Total Spent, Income, Net Balance, and Top Spending Categories.
- **Filtering System**:
  - Filter by **Amount Range** (Min/Max).
  - Filter by **Category** or **Keywords**.
- **Visual Analytics**:
  - **Spending Pie Chart**: Breakdown of expenses by category.
  - **Trend Lines**: Daily spending turnover.
  - **Heatmaps**: Spending intensity by Day of Week or Month.

### 3. Reporting & Export
- **CSV Export**: Save filtered datasets or categorized reports.
- **Sample Generator**: Includes a built-in generator that creates realistic mock transaction data (Swiggy, Amazon, Salary credits) for testing the tool without uploading personal files.

## Architecture

### Directory Structure
```
payment/
├── Payments.py     # Monolithic Application (GUI + Logic)
└── data.xlsx       # Sample/Input Data File
```

### Dependencies
- **UI**: `tkinter` (Native Python)
- **Data**: `pandas`, `openpyxl`
- **Plotting**: `matplotlib`, `numpy`

### Class Structure
The `TransactionAnalyzer` class manages the entire lifecycle:
1.  `__init__`: Sets up the UI tabs and loads category rules.
2.  `load_file()`: Reads external data.
3.  `process_data()`: Normalizes columns (DateTime, Amount) and applies tags.
4.  `update_all_displays()`: Refreshes charts and tables based on current filters.

## Setup & Execution

### Prerequisites
- Python 3.x
- Libraries: `pandas`, `matplotlib`, `openpyxl`, `numpy`
  ```powershell
  pip install pandas matplotlib openpyxl numpy
  ```

### Running the Analyzer
1.  **Navigate**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\Python\payment"
    ```
2.  **Run**:
    ```powershell
    python Payments.py
    ```

### Usage Guide
1.  **Load Data**: Click **"📂 Load Excel File"** to open your bank statement.
    - *Alternatively, click **"📋 Use Sample Data"** to see a demo.*
2.  **Analyze**: Switch to the **"Charts"** tab to visualize your spending.
3.  **Filter**: Use the sidebar to focus on specific categories (e.g., "Food & Dining").
4.  **Settings**: Go to the **"Settings"** tab to add new keywords (e.g., add "Starbucks" to "Food").
