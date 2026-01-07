# Vanilla SPA - Single Page Application Documentation

**Category**: Web Development
**Path**: `Web/SinglePageApplication`
**Version**: 1.0

## Overview
**Vanilla SPA** is a lightweight, dependency-free Single Page Application logic demonstration. It proves that complex modern web features—like client-side routing, dynamic view rendering, and state management—can be built entirely with native JavaScript, HTML5, and CSS3, without the overhead of heavy frameworks like React or Angular.

## Key Features

### 1. Custom Router System
- **Hash-Based Routing**: Listens for `hashchange` events (e.g., `#home`, `#about`) to trigger navigation.
- **Dynamic Rendering**: Swaps the inner HTML of a main container matching the current route, ensuring no full page reloads occur.
- **404 Handling**: Gracefully catches undefined routes (e.g., `#unknown`) and renders a custom "Not Found" view.

### 2. Rich Content Management
- **Routes**:
  - **Home**: Feature highlights and CTA.
  - **About**: Company story and tech stack stats.
  - **Projects**: A dynamic portfolio grid populated from a JSON-like array.
  - **Team**: Personnel cards with bios and social links.
  - **Blog**: Article previews with categories and read times.
  - **Contact**: A functional form with simulated submission states.

### 3. Interactive UI Components
- **Modal System**: A reusable overlay (`div.modal`) that displays expanded details for portfolio items when clicked.
- **Sidebar Navigation**: a responsive slide-out menu on mobile devices and a permanent sidebar on desktop.
- **Theme Engine**: Persistence-supported Dark/Light mode toggle that saves user preference to `localStorage`.

## Architecture

### File Structure
```
SinglePageApplication/
├── index.html      # App Shell (Sidebar, Main Container, Modal)
├── style.css       # CSS Variables, Flex/Grid Layouts, Transitions
└── script.js       # Router, Data Store, Event Listeners
```

### Route Defintion (`script.js`)
Routes are defined as a dictionary of objects, separating logic from presentation:
```javascript
const routes = {
    'home': {
        title: 'Home',
        render: () => `<h1>Welcome...</h1>`
    },
    'about': { ... }
};
```

## Usage Guide

### Navigation
1.  **Click Links**: Use the sidebar to switch views instantly.
2.  **Browser History**: The Back/Forward browser buttons work naturally because the hash changes push updates to the browser's history stack.

### Viewing Projects
1.  Navigate to the **Projects** tab.
2.  Click on any Project Card (e.g., "3D Graphics Engine").
3.  A modal appears with a larger image, description, and a "Run/Demo" button.

### Form Simulation
1.  Go to **Contact**.
2.  Fill out the form and submit.
3.  Watch the button change state to "Sending..." -> "Message Sent!" (simulated async delay).
