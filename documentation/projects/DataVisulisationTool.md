# Data Visualization Tool Documentation

**Category**: Python Systems / Data Science
**Path**: `Python/DataVisulisationTool`
**Version**: 1.0

## Overview
The **Data Visualization Tool** is a Python utility that automates the generation of charts from CSV data. It abstracts the complexity of `matplotlib` into a simple command-line interface, allowing users quickly visualize datasets (like Sales vs. Months) without writing plotting code manually.

## Key Features

### 1. Python Automation (`main.py`)
- **CSV Parsing**: Uses the built-in `csv` library to robustly read headers and column data.
- **Dynamic Headers**: Automatically detects column names for labeling axes (`x_label`, `y_label`).
- **Sample Generation**: If no data exists, it creates a `data.csv` template with dummy financial data to help the user get started.
- **Matplotlib Integration**: Generates professional-grade bar charts:
  - Sets custom colors (`skyblue`).
  - Labels axes and titles dynamically based on input columns.
  - Svaes the result as a high-quality image (`plot_output.png`).
- **Graceful Fallback**: If `matplotlib` is not installed, it prints a text-based summary of the data instead of crashing.

### 2. GUI Application (`gui_main.py`)
- *Note: Provides a desktop graphical interface for selecting files and viewing plots directly in a window.*

### 3. Web Demo
The web dashboard provides an interactive, client-side version of the plotting tool:
- **Live Rendering**: Switch between Bar, Line, and Pie charts instantly using SVG graphics.
- **Randomizer**: "New Data" button simulates changing datasets to test the visualization logic.
- **Integrated Table**: Displays the raw data alongside the chart, updated in real-time.
- **Animations**: CSS transitions make bar height changes and color shifts smooth.

## Architecture

### Directory Structure
```
DataVisulisationTool/
├── main.py         # CLI Plotter
├── gui_main.py     # Desktop GUI
├── demo.html       # Web Dashboard
└── requirements.txt # Dependencies (matplotlib)
```

### Workflow
1.  **Input**: User provides a CSV file (e.g., `Month, Sales`).
2.  **Processing**: Script extracts two specific columns (X-axis, Y-axis).
3.  **Output**: Script generates `plot_output.png`.

## Setup & Execution

### Prerequisites
- Python 3.x
- Matplotlib (`pip install matplotlib`)

### Running the Console App
1.  **Navigate**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\Python\DataVisulisationTool"
    ```
2.  **Run**:
    ```powershell
    python main.py
    ```
    *If prompted for a filename, press Enter to use the default `data.csv`.*

### Expected Output
```
--- Simple Data Viz Tool ---
Created 'data.csv' sample file.
Enter CSV filename: 
Columns: ['Month', 'Sales', 'Expenses']

--- Generating Plot ---
Plot saved to 'plot_output.png'
```

## Web Demo Usage
- Open `demo.html` in a web browser.
- **Views**: Click "Line" to see trends or "Pie" to see distribution.
- **Analyze**: Hover over bars (desktop) to see specific values.
- **Data Source**: The table at the bottom reflects the data currently being visualized.
