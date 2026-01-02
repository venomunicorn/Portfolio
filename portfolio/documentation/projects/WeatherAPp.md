# Atmosphere - Weather App Documentation

**Category**: Web Development
**Path**: `Web/WeatherAPp`
**Version**: 1.0

## Overview
**Atmosphere** is a modern, dashboard-style weather application that provides detailed atmospheric data for major cities. It features a rich UI with detailed metrics (humidity, wind, UV, etc.), hourly/daily forecasts, and sun cycle visualization.

## Key Features

### 1. Multi-City Support
- **Dataset**: `weatherDatabase` contains mock data for San Francisco, London, New York, Tokyo, Dubai, Mumbai, and Sydney.
- **Search**: Users can input a city name to load its specific weather data simulating an API call (`fetchWeather`).
- **Geolocation**: The "Use My Location" button (`geoBtn`) simulates a location lookup by picking a random city from the verified list (for demo purposes).

### 2. Comprehensive Metrics
- **Current Conditions**: Temperature, Condition (e.g., "Partly Cloudy"), and a dynamic FontAwesome icon.
- **Atmospheric Details**: "Feels Like" temp, Humidity %, Wind Speed (km/h), Pressure (hPa), Visibility, and Cloud Cover.
- **Sun Cycle**: Displays Sunrise/Sunset times and a visual progress bar indicating the sun's current position in the sky based on the time of day.

### 3. Forecast Visualization
- **Hourly Scroller**: A horizontal list showing temperature trends for the next 12 hours.
- **Daily 5-Day**: A list of upcoming days with High/Low bars visualizing the temperature range.

### 4. User Preferences
- **Unit Toggle**: Users can switch the entire dashboard between Celsius (°C) and Fahrenheit (°F) with a single click. The conversion happens instantly on the client side (`celsius * 9/5 + 32`).
- **Recent Searches**: The app saves valid searches to `localStorage` and displays them as clickable tags for quick access.

## Architecture

### File Structure
```
WeatherAPp/
├── index.html      # Dashboard Layout (Grid/Flex)
├── style.css       # Glassmorphism effects, Responsive Grid
└── script.js       # Data Store, Conversion Logic, UI Updates
```

### Data Handling
The app uses a local "Mock Database" object in `script.js` to simulate a reliable backend without needing an API key:
```javascript
const weatherDatabase = {
    'london': {
        temp: 8,
        condition: 'Rainy',
        hourly: [...],
        daily: [...]
    },
    ...
};
```
*Note: This architecture allows for easy swapping with a real API like OpenWeatherMap in the future.*

## Usage Guide

### Checking Weather
1.  Open `index.html`.
2.  **Type** "Dubai" in the search box and press Enter.
3.  **View** the dashboard update with sunny conditions and high temperatures.

### Changing Units
1.  Click the **°C** button in the top right.
2.  Watch all temperature values (Current, Feels Like, Forecasts) convert to Fahrenheit.

### Mobile Use
- The dashboard collapses into a single-column scrollable view on mobile devices, ensuring all data remains readable.
