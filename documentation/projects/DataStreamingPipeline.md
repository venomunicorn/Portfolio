# Data Streaming Pipeline Documentation

**Category**: Python Systems / Data Engineering
**Path**: `Python/DataStreamingPipeline`
**Version**: 1.0

## Overview
The **Data Streaming Pipeline** demonstrates the concept of a "Producer-Consumer" architecture and Functional Reactive Programming (FRP) principles using Python Generators. It simulates a real-time sensor network where data is generated, filtered, transformed, and consumed in a streaming fashion without loading the entire dataset into memory.

## Key Features

### 1. Generator-Based Pipeline
- **Memory Efficient**: Using Python `yield`, data is processed one item at a time. This allows the pipeline to theoretically handle infinite streams of data without crashing RAM.
- **Decoupled Stages**:
  1.  **Source (Producer)**: Generates synthetic sensor data (Temperature, Timestamp).
  2.  **Filter Stage**: Discards "OK" statuses, passing only "CRITICAL" data downstream.
  3.  **Transform Stage**: Enriches data by converting Celsius to Fahrenheit.
  4.  **Sink (Consumer)**: The final alert system that prints warnings to the console.

### 2. Real-time Simulation
- **Latency Simulation**: The producer intentionally sleeps (`time.sleep(0.1)`) to mimic the network latency of real IoT devices.
- **Randomized Data**: Temperature values are randomized to ensure unpredictable "CRITICAL" events, testing the filter logic.

## Architecture

### Directory Structure
```
DataStreamingPipeline/
└── main.py         # ETL Pipeline Implementation
```

### Pipeline Flow
```mermaid
graph LR
    A[Sensor Gen] -->|Raw Data| B[Filter Critical]
    B -->|Filtered Data| C[Transform F]
    C -->|Enriched Data| D[Alert System]
```

### Code Concept (Generators)
```python
def pipeline_stage(input_stream):
    for item in input_stream:
        # process item
        yield result
```
This pattern allows stages to be chained effortlessly: `stage2(stage1(source()))`.

## Setup & Execution

### Prerequisites
- Python 3.x

### Running the App
1.  **Navigate**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\Python\DataStreamingPipeline"
    ```
2.  **Run**:
    ```powershell
    python main.py
    ```

### Expected Output
The script will run for a few seconds, printing alerts only when the random temperature exceeds 90°C.
```
Initializing Data Pipeline...
--- Starting Monitoring Stream ---
[ALERT] High Temp Detected! ID:3 Temp:92.4C / 198.3F
[ALERT] High Temp Detected! ID:8 Temp:95.1C / 203.2F
...
Stream ended.
```
