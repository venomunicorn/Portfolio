# Data Analysis Tools Documentation

**Category**: C++ Systems
**Path**: `C++/DataAnalysisTools`
**Version**: 1.0

## Overview
The **Data Analysis Tools** project is a statistical computing application implemented in C++. It processes numeric datasets to calculate fundamental statistical properties such as mean, median, standard deviation, and variance. It serves as a practical example of the STL `<numeric>` and `<algorithm>` libraries.

## Key Features

### 1. Statistical Core (C++)
- **Mean Calculation**: Arithmetic average of the dataset using `std::accumulate`.
- **Median Calculation**: Middle value of a sorted dataset. Handles both even and odd dataset sizes correctly.
- **Standard Deviation**: Measure of the amount of variation using `std::sqrt` and custom accumulation logic.
- **Input Handling**: Reads a dynamic stream of numbers from the console until a termination signal is received.

### 2. Supported Statistics
- **Count**: Total number of samples.
- **Mean**: $\bar{x} = \frac{\sum x}{n}$
- **Median**: Middle value (data sorted).
- **Standard Deviation**: $\sigma = \sqrt{\frac{\sum(x - \bar{x})^2}{n}}$
- **Min/Max**: Smallest and largest values in the set.
- **Range**: Difference between Max and Min.

### 3. Web Demo
- **Interactive Dashboard**: A web-based implementation (`demo.html`) replicating the C++ logic in JavaScript.
- **Visualizations**:
  - **Bar Chart**: Visual representation of the first 10 data points using CSS-based bars.
  - **Real-time Metrics**: Displays calculated statistics in a grid card layout.
- **Sample Data**: "One-click" button to populate the input field with random test datasets for quick demonstration.

## Architecture

### Directory Structure
```
DataAnalysisTools/
├── main.cpp    # C++ Implementation
└── demo.html   # Web-based visualization
```

### Critical Functions (`main.cpp`)
- `calculateMean(vector<double>)`: Returns the average.
- `calculateMedian(vector<double>)`: Sorts a copy of the data to find the median.
- `calculateStdDev(vector<double>)`: Calculates the standard deviation based on the mean.

## Setup & Compilation

### Prerequisites
- C++ Compiler (supporting C++11 or later)

### Build Instructions
1.  **Navigate directly**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\C++\DataAnalysisTools"
    ```
2.  **Compile**:
    ```powershell
    g++ main.cpp -o data_analysis
    ```
3.  **Run**:
    ```powershell
    .\data_analysis
    ```

## Web Demo Usage
- Open `demo.html` in a versatile web browser.
- **Input**: Paste comma-separated numbers (e.g., `10, 20, 30, 40`).
- **Analyze**: Click "Analyze Data" to compute statistics and render the chart.
- **Sample**: Use "Sample Data" to try pre-configured sets.
