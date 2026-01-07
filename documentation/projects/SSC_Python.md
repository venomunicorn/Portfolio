# SSC Math Prep (System Status Monitor?) Documentation

*Note: The project folder is named `SSC`, but the content is clearly a Math Preparation Tool (Multiplication Tables, Squares, Cubes). This documentation reflects the codebase functionality.*

**Category**: Python Systems / Education
**Path**: `Python/SSC` (referenced as sscperp.py)
**Version**: 1.0

## Overview
The **SSC Math Prep** tool is an educational utility designed to generate reference materials for competitive exams (like SSC CGL). It automates the creation of mathematical charts—Multiplication Tables (1-50), Squares (1-100), Cubes (1-100), and Roots—and compiles them into a structured CSV file for printing or analysis.

## Key Features

### 1. Python Data Generation (`sscperp.py`)
- **Pandas Integration**: Utilizes `pandas` DataFrames to structure mathematical data efficiently before exporting.
- **Comprehensive Datasets**:
  - **Multiplication Tables**: Generates tables for numbers 1 to 50, up to $x12$.
  - **Power Functions**: Calculates Squares ($x^2$) and Cubes ($x^3$) up to 100.
  - **Roots**: Calculates Square Roots ($\sqrt{x}$) and Cube Roots ($\sqrt[3]{x}$) for perfect powers.
- **Formatted Export**: Creates a single `mathematical_data.csv` file with clear "Section Headers" (e.g., `=== SQUARES OF NUMBERS ===`) separating the datasets, making the raw text file readable even in basic editors.

### 2. GUI Application (`gui_main.py`)
- *Note: Likely provides a interface to view these tables or select specific ranges to export.*

### 3. Web Demo
The web simulator acts as a digital flashcard system:
- **Interactive Tables**: Select a number (e.g., "Table of 17") from a dropdown to instantly see its 1-12 multiplication list.
- **Reference Grids**: Displays Squares ($1^2$ to $30^2$) and Cubes ($1^3$ to $20^3$) in a responsive grid layout for quick memorization.
- **Roots Tab**: Shows the inverse relationship (e.g., $\sqrt{289} = 17$).
- **Export Simulation**: A demo button that mimics the CSV download functionality.

## Architecture

### Directory Structure
```
SSC/
├── sscperp.py      # Data Generator Script
├── gui_main.py     # Desktop UI
└── demo.html       # Web Reference Tool
```

### Data Logic
The script uses list comprehensions for speed:
```python
# Generating Row for N
row = [num] + [num * i for i in range(1, 13)] 
```

## Setup & Execution

### Prerequisites
- Python 3.x
- Libraries: `pandas`, `numpy` (`pip install pandas numpy`)

### Running the Generator
1.  **Navigate**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\Python\SSC"
    ```
2.  **Run**:
    ```powershell
    python sscperp.py
    ```

### Expected Output
```
Generating mathematical data...
- Generating multiplication tables (1 to 50)...
- Calculating squares (1 to 100)...
...
DATA GENERATION COMPLETE!
File saved as: mathematical_data.csv
Total sections: 5
```

## Web Demo Usage
- Open `demo.html` in a web browser.
- **Tables**: Switch to "Tables" tab, select "19".
- **Memorize**: Switch to "Squares" to revise perfect squares up to 30.
