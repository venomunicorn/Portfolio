# Weather Application Documentation

**Category**: Python Systems / API Integration
**Path**: `Python/WeatherApplication`
**Version**: 1.0

## Overview
The **Local Weather Application** is a desktop GUI tool that provides real-time weather updates based on the user's geographical location. It demonstrates how to integrate third-party APIs (OpenWeatherMap) into a Python/Tkinter interface, making it a practical example of network programming and UI design.

## Key Features

### 1. Python API Client (`Weatherapp.py`)
- **Auto-Geolocation**: Uses the `ipapi.co` service to automatically detect the user's City, Country, Latitude, and Longitude based on their public IP address.
- **Live Weather Data**: Fetches JSON data from the **OpenWeatherMap API**, including:
  - Temperature (°C)
  - Humidity (%)
  - Atmospheric Pressure (hPa)
  - Text Description (e.g., "Scattered Clouds")
- **Threaded Refresh**: The "Refresh" button runs the format network request in a background thread using `threading.Thread(daemon=True)`. This ensures the UI remains responsive (doesn't freeze) while waiting for the server response.
- **Graceful Error Handling**: Displays user-friendly error messages if the API Key is missing or network connectivity fails.

### 2. GUI Output
- A clean Tkinter window displays the location name, temperature in large text, and detailed metrics (Condition, Humidity, Pressure).
- Status bar at the bottom gives feedback (e.g., "Fetching data...", "Weather updated successfully").

### 3. Web Demo
The web simulator mimics the mobile app experience:
- **Search Bar**: Users can type cities like "London", "Tokyo", or "Mumbai" to see simulated data.
- **Dynamic Dashboard**: Updates the central weather icon (☀️, 🌧️) and background details based on the selected city.
- **Detailed Metrics**: Displays Grid cards for Wind Speed, Feels Like, and Visibility.

## Architecture

### Directory Structure
```
WeatherApplication/
├── Weatherapp.py       # Main Application
├── instructions.txt    # Setup Guide
└── demo.html           # Web Simulation
```

### API Flow
1.  **Locate**: `GET https://ipapi.co/json/` → Returns Lat/Lon.
2.  **Fetch**: `GET api.openweathermap.org/data/2.5/weather?lat=...&lon=...`
3.  **Parse**: JSON → Python Dictionary → UI Labels.

## Setup & Execution

### Prerequisites
- Python 3.x
- Libraries: `requests` (`pip install requests`)
- **API Key**: You must obtain a free API Key from [OpenWeatherMap](https://openweathermap.org/api) and paste it into line 10 of `Weatherapp.py`.

### Running the App
1.  **Navigate**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\Python\WeatherApplication"
    ```
2.  **Edit Config**:
    Open `Weatherapp.py` and replace `your_api_key_here` with your actual key.
3.  **Run**:
    ```powershell
    python Weatherapp.py
    ```

### Expected Output
- **Title**: Local Weather
- **Location**: San Francisco, California, US (detected)
- **Temperature**: 18.5°C
- **Condition**: Clear Sky

*Note: Without a valid API key, the app will show a warning popup.*
