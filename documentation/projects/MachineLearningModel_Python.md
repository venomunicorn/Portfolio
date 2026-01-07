# Machine Learning Model Documentation

**Category**: Python Systems / Data Science
**Path**: `Python/MachineLearningModel`
**Version**: 1.0

## Overview
The **Machine Learning Model** in this Python project builds a **Linear Regression** system from scratch using `scikit-learn`. Unlike the C++ Perceptron implementation (which focuses on classification), this project tackles regression: predicting continuous values (House Prices) based on input features (Square Footage). It covers the full ML pipeline: Data Generation, Splitting, Training, Evaluation, and Visualization.

## Key Features

### 1. Python ML Pipeline (`main.py`)
- **Synthetic Data Generation**: Creates a realistic dataset where $Price \approx 300 \times Size + 50000 + Noise$.
- **Model Training**: Uses `LinearRegression` to learn the coefficients ($m$) and intercept ($c$) of the best-fit line.
- **Evaluation Metrics**:
  - **MSE (Mean Squared Error)**: Measures the average squared difference between estimated values and actual value.
  - **$R^2$ Score**: Indicates the proportion of the variance in the dependent variable that is predictable from the independent variable.
- **Visualization**: Uses `matplotlib` to plot the training data points against the regression line, saving the result as `ml_result.png`.

### 2. GUI Application (`gui_main.py`)
- *Note: Likely provides a dashboard to input house parameters and see the predicted price, possibly displaying the regression graph embedded in the window.*

### 3. Web Demo
The web simulation offers an interactive "House Price Predictor":
- **Training Simulation**: Clicking "Train Model" generates random data points and animates the drawing of the regression line (Best Fit) on an SVG chart.
- **Real-Time Prediction**: As users adjust sliders for "Square Feet", "Bedrooms", and "Bathrooms", the predicted price updates instantly based on the learned coefficients.
- **Interactive Visuals**: Data points fade in, and the regression line draws itself across the chart to visualize the learning process.

## Architecture

### Directory Structure
```
MachineLearningModel/
├── main.py         # ML Training Script
├── gui_main.py     # Desktop Predictor
├── demo.html       # Interactive Web Demo
└── requirements.txt # Dependencies (scikit-learn, numpy)
```

### Regression Model
The model predicts price $y$ based on input $x$:
$$ y = w_1 x_1 + w_2 x_2 + ... + b $$
In the demo, the weights correspond to:
- $w_{sqft} \approx 150$/sqft
- $w_{bed} \approx 25000$/room
- $w_{bath} \approx 15000$/bath

## Setup & Execution

### Prerequisites
- Python 3.x
- Libraries: `numpy`, `scikit-learn`, `matplotlib`

### Running the Training Script
1.  **Navigate**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\Python\MachineLearningModel"
    ```
2.  **Run**:
    ```powershell
    python main.py
    ```

### Expected Output
```
--- Simple Machine Learning Model (Linear Regression) ---
Generating synthetic data...
Training Linear Regression model...
Model Coefficient: $305.21
Model Intercept: $51234.50

[Evaluation]
Mean Squared Error: 2450122.99
R2 Score: 0.92

Graph saved to ml_result.png
--- Try it out ---
Enter house size (sq ft): 
```

## Web Demo Usage
- Open `demo.html` in a web browser.
- **Train**: Click **Train Model** to populate the graph.
- **Experiment**: Drag the "Square Feet" slider to 2500.
- **Result**: Watch the price update (e.g., "$450,000").
