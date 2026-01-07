# Transaction Analyzer Dashboard Documentation

**Category**: Web Development
**Path**: `Web/PaymentDataAnalysis`
**Version**: 1.0

## Overview
**Transaction Analyzer Dashboard** is a comprehensive financial analytics tool that visualizes bank transaction data. It allows users to upload Excel/CSV bank statements and instantly receive a detailed breakdown of income, expenses, and spending habits through interactive charts and statistical cards.

## Key Features

### 1. Data Processing
- **File Upload**: Supports drag-and-drop upload for `.xlsx` and `.xls` files.
- **Parsing**: Automatically detects standard transaction columns (Date, Details, Amount, Type).
- **Auto-Categorization**: (Simulated) Assigns categories like "Food", "Transport", "Shopping" based on keyword analysis of transaction descriptions.

### 2. Financial Analytics
- **Summary Cards**: Displays Total Spent, Total Received, Net Balance, Average Transaction Value, and the Largest Single Transaction.
- **Charts**:
  - **Category Spending**: Doughnut chart showing the percentage distribution of expenses across categories.
  - **Spending Trends**: Line chart visualizing spending patterns over Daily, Weekly, or Monthly periods.

### 3. Filtering & Search
- **Advanced Filters**: Users can drill down into data by:
  - Date Range (Start/End)
  - Amount Range (Min/Max)
  - Category (Dropdown)
  - Keyword Search (e.g., "Amazon", "Uber")
- **Live Updates**: All charts and stats refresh instantly when filters are applied.

### 4. Reporting
- **Export CSV**: Downloads the currently filtered dataset as a standardized CSV file.
- **Print Report**: Generates a clean, printer-friendly summary page with key stats and a transaction table.
- **Dark Mode**: Toggleable theme for comfortable viewing in low-light environments.

## Architecture

### File Structure
```
PaymentDataAnalysis/
├── index.html      # Dashboard layout, Chart containers, Modals
├── styles.css      # Grid layout, Theme variables, Component styles
├── script.js       # File handling, Data visualization logic, State management
├── analyze.py      # (Optional) Python backend for advanced file parsing
└── data.xlsx       # Sample dataset for testing
```

### Dependencies
- **Chart.js**: Used for rendering the interactive Doughnut and Line charts.
- **Fetch API**: Handles file uploads to the backend (if running with Python) or processes data locally (if running in demo mode).

## Usage Guide

### Getting Started
1.  Open `index.html`.
2.  **Upload**: Drag the provided `data.xlsx` into the upload zone.
3.  **Analyze**: Click "Upload & Analyze". The dashboard will populate with parsed data.

### Exploring Data
- **View Trends**: Click "Weekly" on the Trend Chart to see spending habits by week.
- **Filter**: Enter "Swiggy" in the Search Keyword box and click "Apply" to see only food delivery expenses.
- **Export**: Click "Export CSV" to save your filtered report.
- **Theme**: Click the Moon icon to switch to Dark Mode.
