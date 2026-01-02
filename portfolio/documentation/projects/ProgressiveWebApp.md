# MultiConvert - Progressive Web App Documentation

**Category**: Web Development
**Path**: `Web/ProgressiveWebApp`
**Version**: 1.0

## Overview
**MultiConvert** is a versatile Unit Converter built as a **Progressive Web App (PWA)**. It is designed to work seamlessly offline, allowing users to install it on their home screen like a native application. It supports real-time conversion across three major categories: Length, Weight, and Temperature.

## Key Features

### 1. Progressive Web App (PWA) Capabilities
- **Installable**: Meets all PWA criteria (Manifest, HTTPS/Localhost, Service Worker). On supported browsers, an "Install" button appears, allowing the app to be added to the device's home screen.
- **Offline Support**: The Service Worker (`sw.js`) caches the core assets (HTML, CSS, JS), enabling the app to load instantly even without an internet connection.
- **Offline Banner**: Automatically detects network status changes (`window.onoffline`) and displays a notification banner if connectivity is lost.

### 2. Multi-Unit Conversion
- **Categories**:
  - **Length**: Meters, Kilometers, Feet, Inches, Miles, etc.
  - **Weight**: Kilograms, Pounds, Ounces, Grams, etc.
  - **Temperature**: Celsius, Fahrenheit, Kelvin.
- **Real-Time Input**: Conversions happen instantly as the user types (`input` event), eliminating the need for a submit button.
- **Bi-Directional**: A "Swap" button instantly reverses the From/To units and values.

### 3. Utility Features
- **History Log**: The last 10 conversions are saved to `localStorage`, creating a persistent audit trail.
- **Dark Mode**: A toggleable visual theme that respects user preference across sessions.
- **Quick Reference**: A static grid displays common conversion benchmarks (e.g., "1 km → 0.621 mi") for the selected category.

## Architecture

### File Structure
```
ProgressiveWebApp/
├── index.html      # UI Skeleton
├── style.css       # Mobile-first styles, Dark mode variables
├── script.js       # Conversion logic, PWA installation handler
├── manifest.json   # App metadata (Name, Icons, Start URL)
└── sw.js           # Service Worker (Caching strategy)
```

### Data Structure
Conversion factors are stored in a normalized object tree:
```javascript
const units = {
    length: {
        meters: { toBase: 1 },
        feet: { toBase: 0.3048 } // 1 ft = 0.3048 m
    },
    ...
};
```
*Logic*: `Input Value * FromUnit.toBase / ToUnit.toBase = Output Value`.

## Usage Guide

### Installation
1.  Open the web page in Chrome/Edge/Safari.
2.  Click the **"Install App"** button (top right) or use the browser's menu to "Add to Home Screen".
3.  Launch the app from your desktop/home screen to verify it opens in a standalone window without browser chrome.

### Converting
1.  Select a category tab (e.g., **Weight**).
2.  Choose "Kilograms" from the first dropdown and "Pounds" from the second.
3.  Type `10` in the input box.
4.  Result: `22.0462 lb` appears instantly.
