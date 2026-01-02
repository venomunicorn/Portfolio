# Machine Learning Model Documentation

**Category**: C++ Systems
**Path**: `C++/MachineLearningModel`
**Version**: 1.0 Perceptron

## Overview
The **Machine Learning Model** project demonstrates the implementation of a basic **Perceptron** (a fundamental building block of neural networks) in C++. It is designed to solve the classic **OR Gate** classification problem, showcasing how weights and biases are iteratively adjusted during training to minimize error.

## Key Features

### 1. Mathematical Core (C++)
- **Perceptron Class**: Encapsulates the network logic.
  - `weights`: Vector of floating-point weights connecting inputs to the neuron.
  - `bias`: A scalar value acting as the activation threshold offset.
  - `learningRate`: Controls the magnitude of weight updates during backpropagation.
- **Activation Function**: Uses a simple **Step Function**: returns `1` if weighted sum > 0, else `0`.
- **Training Loop**: Implements the Delta Rule (Gradient Descent approximation) to update weights:
  $w_{new} = w_{old} + \eta \cdot (target - output) \cdot input$

### 2. XOR Simulation (Web Demo)
While the C++ version implements a single-layer perceptron (capable of solving linear problems like OR), the **Web Demo** upgrades this to a **Multi-Layer Perceptron (MLP)** with a hidden layer to solve the non-linear **XOR problem**.
- **Visualizer**: Real-time HTML5 Canvas animation showing neurons (nodes) and synaptic weights (lines). Line opacity/color indicates weight strength and sign.
- **Interactive Training**: Watch the "Loss" decrease and "Accuracy" increase as the network trains over 1000 epochs.
- **Testing**: Manual verification button to run the trained model against the 4 XOR truth table cases.

## Architecture

### Directory Structure
```
MachineLearningModel/
├── main.cpp    # C++ Perceptron (Linear Classifier)
└── demo.html   # Web-based MLP (Non-linear Classifier)
```

### Constraints & Limitations
- **C++ Version**: Can only solve linearly separable problems (AND, OR). It cannot solve XOR without adding hidden layers.
- **Web Demo**: Adds a hidden layer (2-4-1 architecture) to demonstrate solving non-linear problems.

## Setup & Compilation

### Prerequisites
- Standard C++ Compiler

### Build Instructions
1.  **Navigate directly**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\C++\MachineLearningModel"
    ```
2.  **Compile**:
    ```powershell
    g++ main.cpp -o perceptron
    ```
3.  **Run**:
    ```powershell
    .\perceptron
    ```

### Expected Output (Console)
```
Training...
Epoch 0 Errors: 2
Epoch 10 Errors: 0
...
Testing:
0 OR 0 = 0
0 OR 1 = 1
1 OR 0 = 1
1 OR 1 = 1
```

## Web Demo Usage
- Open `demo.html` in a versatile web browser.
- **Visualization**: Observe the 2 Input nodes, 4 Hidden nodes, and 1 Output node.
- **Train**: Click "Train Network" to start the backpropagation process.
- **Reset**: Re-randomize weights to start over.
