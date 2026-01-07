# Nexus - Real-Time Data Dashboard Documentation

**Category**: Web Development
**Path**: `Web/RealTimeDataDashboard`
**Version**: 1.0

## Overview
**Nexus** is a futuristic, sci-fi inspired dashboard interface designed to simulate real-time server monitoring. It visualizes critical system metrics (CPU, Memory, Bandwidth) and network traffic using high-speed animated charts. The purpose is to demonstrate how to build complex, live-updating UIs using JavaScript and Chart.js.

## Key Features

### 1. Live Performance Monitoring
- **Updates Every Second**: The dashboard runs a constant loop `setInterval(..., 1000)` to fetch and update data.
- **Metrics**:
  - **Bandwidth**: Real-time throughput (GB/s).
  - **CPU/Memory**: Live usage percentages with color-coded bars (Green -> Cyan -> Red).
  - **Disk I/O**: Read/Write speeds.

### 2. Interactive Charts
- **Traffic Monitor**: A `Chart.js` Line Chart that updates dynamically (`chart.push()`, `chart.shift()`) to create a scrolling "oscilloscope" effect of Inbound vs. Outbound traffic.
- **System Health**: A Doughnut gauge that calculates an overall health score (0-100%) based on active alerts and load averages.

### 3. Server Grid & Logs
- **Server Status**: A grid of cards (`US-East-1`, `EU-Central`, etc.) showing individual load and online/offline status.
- **Console Logs**: A scrolling activity feed that simulates system events ("Database query completed", "SSL renewed") with timestamps and severity levels (Info, Warning, Error).

### 4. Alert System
- **Popups**: Randomly triggers critical system alerts (e.g., "CPU usage spike detected") that slide into view and auto-dismiss.
- **Controls**: A global "Pause" button freezes the update loop, allowing administrators to inspect the current state.

## Architecture

### File Structure
```
RealTimeDataDashboard/
├── index.html      # Layout: Sidebar, Grid Area, Overlay
├── style.css       # Neon theme, Grid layout, Animations
└── script.js       # Simulation logic, Chart.js updates
```

### Simulation Logic (`script.js`)
Since there is no real backend, the `script.js` file simulates a live server environment:
- **Random Walk**: Metrics update by adding a small random delta to the previous value (e.g., `cpu += Math.random() * 8 - 4`).
- **Bounds Checking**: Ensures values stay within realistic ranges (0-100% for CPU, >0 for users).

## Usage Guide

### Simulation Controls
1.  **Launch**: Open `index.html`. The simulation starts automatically.
2.  **Pause**: Click the "Pause" button in the top right to freeze the data stream.
3.  **Dismiss Alerts**: If a red alert banner appears, click the "X" to acknowledge it.

### Customization
- **Theme**: Modify the `:root` variables in `style.css` to change the neon accent colors (currently Cyan `#00f3ff` and Pink `#ff0055`).
- **Data Speed**: Change the `setInterval` delay in `script.js` (line 196) to make updates faster or slower.
