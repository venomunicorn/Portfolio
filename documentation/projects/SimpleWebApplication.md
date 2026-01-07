# Simple Web Application Documentation

**Category**: Python Systems / Web
**Path**: `Python/SimpleWebApplication`
**Version**: 1.0

## Overview
The **Simple Web Application** is a minimalistic example of a web server built with **Flask**, Python's lightweight web framework. It demonstrates the fundamental concepts of web development: Routing, Templates, and serving HTML. Instead of separate HTML files, it uses `render_template_string` to serve dynamic content directly from the Python script, making it a self-contained "Micro-App".

## Key Features

### 1. Flask Application (`app.py`)
- **Routing**: Maps URLs to Python functions:
  - `/` -> `home()`: Renders the blue-themed Home page.
  - `/about` -> `about()`: Renders the green-themed About page.
- **Jinja2 Templating**: Uses `{{ title }}` syntax to dynamically inject variables (like page titles) into the HTML structure.
- **CSS Styling**: Includes embedded CSS within the headers to create a card-based, responsive layout without external stylesheets.
- **Debug Mode**: Configured to run with `debug=True`, which provides live reloading and detailed error messages during development.

## Architecture

### Directory Structure
```
SimpleWebApplication/
├── app.py          # Main Flask Application
└── requirements.txt # Dependencies (flask)
```

### Routing Logic
```python
@app.route('/')
def home():
    # Looks for {{ title }} in TEMPLATE and replaces it
    return render_template_string(TEMPLATE, title="Home Page")
```

## Setup & Execution

### Prerequisites
- Python 3.x
- Flask (`pip install flask`)

### Running the App
1.  **Navigate**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\Python\SimpleWebApplication"
    ```
2.  **Run**:
    ```powershell
    python app.py
    ```

### Expected Output
```
Starting Flask App...
Go to http://127.0.0.1:5000
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

### Usage
- Open your web browser to `http://127.0.0.1:5000`.
- **Home**: View the welcome card.
- **Navigate**: Click "Go to About Page" to see the routing in action.
- **Return**: Click "Back Home".
