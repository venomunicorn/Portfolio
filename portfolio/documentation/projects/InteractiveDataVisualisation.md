# Interactive Data Visualization Dashboard Documentation

**Category**: Web Development
**Path**: `Web/InteractiveDataVisualisation`
**Version**: 1.0

## Overview
The **Interactive Data Visualization Dashboard** is a data analytics interface powered by Chart.js. It visualizes global trends such as Population, GDP, CO₂ Emissions, and Internet Usage over time. The dashboard allows users to switch between different visualization types (Bar, Line, Pie, Radar) and different datasets, updating specific cards with relevant statistics dynamically.

## Key Features

### 1. Dynamic Charting
- **Engine**: Built on `Chart.js` for high-performance, responsive HTML5 canvas rendering.
- **Multiple Views**: Users can toggle between **Line**, **Bar**, **Pie**, and **Radar** charts to see the data from different perspectives.
- **Interactive Tooltips**: Hovering over data points shows precise values and units.

### 2. Multi-Dataset Support
The dashboard includes four pre-loaded Global Datasets:
- **World Population** (Billions)
- **World GDP** (Trillions USD)
- **CO₂ Emissions** (Billion Tonnes)
- **Internet Usage** (% of Population)

### 3. Statistical Analysis Cards
Upon selecting a dataset, the sidebar automatically updates to show:
- **Current Value**: The latest data point.
- **Change**: Percentage growth or decline.
- **Min/Max/Avg**: Calculated statistics based on the full historical range of the dataset.

### 4. Export Capability
- **Download PNG**: Users can save a high-resolution snapshot of the currently rendered chart by clicking the "Download Chart" button.

## Architecture

### File Structure
```
InteractiveDataVisualisation/
├── index.html      # Dashboard layout (Sidebar, Main Chart Area)
├── style.css       # Dark mode theme, glassmorphism effects
└── script.js       # Dataset definitions, Chart.js configuration, Event handling
```

### Data Structure (`script.js`)
Datasets are stored as a configuration object:
```javascript
const datasets = {
    population: {
        name: 'World Population',
        unit: 'billion',
        labels: ['1950', '1960', ...],
        data: [2.5, 3.0, ...],
        colors: [...],
        stats: { ... }
    },
    ...
};
```

## Usage Guide

### Launching
Open `index.html` in a browser. Ensure you have an internet connection to load the Chart.js library from the CDN (included in the HTML head).

### Exploring Data
1.  **Select Metric**: Use the dropdown menu in the top right to choose a topic (e.g., "World GDP").
2.  **Choose Visualization**: Click the icons (Line, Bar, Pie, Radar) above the chart to change the rendering mode.
3.  **Analyze**: Review the stats cards on the right sidebar for a quick summary.
4.  **Save**: Click the download icon to save the graph for a report.
