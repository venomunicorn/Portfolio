# RestfulAPI Documentation

**Category**: Python Systems / Web
**Path**: `Python/RestfulAPI`
**Version**: 1.0

## Overview
The **RestfulAPI** project demonstrates how to build a fully functional HTTP server from scratch using Python's standard library (`http.server`). It implements a CRUD (Create, Read, Update, Delete) interface without relying on external frameworks like Flask or Django. This makes it an excellent educational resource for understanding the low-level mechanics of HTTP methods, status codes, and JSON parsing.

## Key Features

### 1. Zero-Dependency Server (`main.py`)
- **GET `/items`**: Returns the list of all stored items as a JSON array.
- **POST `/items`**: accepts a JSON body (e.g., `{"name": "New"}`) to create a new resource. Automatically assigns a unique ID.
- **DELETE `/items/<id>`**: Removes the item with the specified integer ID from the database.
- **In-Memory Storage**: Uses a simple Python dictionary `DATA = {1: {...}, 2: {...}}` to simulate a database. Data persists only while the script is running.

## Architecture

### Directory Structure
```
RestfulAPI/
└── main.py         # Single-file Server
```

### HTTP Handling
The class `SimpleAPI` inherits from `BaseHTTPRequestHandler` and overrides standard methods:
- `do_GET()`: Handles read requests.
- `do_POST()`: Reads `Content-Length`, parses the body, and updates store.
- `do_DELETE()`: Parses the URL path to extract the resource ID.

## Setup & Execution

### Prerequisites
- Python 3.x (Built-in libraries only)

### Running the API
1.  **Navigate**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\Python\RestfulAPI"
    ```
2.  **Run**:
    ```powershell
    python main.py
    ```

### Expected Output
```
Starting API server on port 8000...
Endpoints:
  GET    http://localhost:8000/items
  POST   http://localhost:8000/items
  DELETE http://localhost:8000/items/<id>
```

### Testing with CURL
- **List Items**: `curl http://localhost:8000/items`
- **Add Item**: `curl -X POST -d '{"name":"Test"}' http://localhost:8000/items`
