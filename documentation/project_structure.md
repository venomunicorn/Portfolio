# Portfolio Project Structure

This document describes the file and directory organization of the portfolio website.

## Directory Tree

```
portfolio/
├── css/
│   └── styles.css       # Main stylesheet for the portfolio. Contains all styling for layout, cards, modal, and animations.
├── documentation/       # (This Directory) Contains documentation/guides.
│   ├── features.md      # Detailed list of portfolio features.
│   ├── project_structure.md # This file.
│   └── setup_guide.md   # Instructions for running and updating the portfolio.
├── js/
│   └── main.js          # Core JavaScript logic. Handles rendering, filtering, search, and modal interactions.
├── data.js              # The centralized database of projects. Contains a JSON array of project objects.
└── index.html           # The main entry point. Defines the semantic HTML structure of the portfolio.
```

## Key File Descriptions

### `index.html`
The skeleton of the website. It includes:
- **Header**: Logo and tagline.
- **Controls**: Search bar and category filter buttons.
- **Stats Container**: Placeholders for dynamic project counts.
- **Projects Grid**: An empty container (`#projectsGrid`) where `main.js` injects project cards.
- **Modal**: Hidden implementation of the demo viewer.

### `data.js`
Stores the project data in a global `const projects` array. Each object follows this schema:
```javascript
{
  "name": "Project Name",
  "category": "C++ Systems",     // Used for filtering logical matching
  "category_short": "C++",       // Displayed on the card tag
  "path": "../C++/ProjectFolder", // Relative path to the source code
  "description": "Short description...",
  "features": ["Feature 1", "Feature 2"], // Array of strings (render as bullet points)
  "demo_url": "../C++/ProjectFolder/demo.html", // Path to the web demo (iframe compatible)
  "run_command": "python app.py", // (Optional) for Python projects
  "has_gui": true                 // (Optional) boolean to show GUI badge
}
```

### `js/main.js`
The engine of the portfolio:
1.  **Reads `data.js`**: Accesses the global `projects` variable.
2.  **Initializes UI**: Calculates stats and renders the initial list of all projects.
3.  **Event Listeners**: Sets up click/input handlers for search, filters, and modal opening/closing.
4.  **DOM Manipulation**: Dynamically constructs HTML strings for project cards and injects them into the grid.

### `css/styles.css`
Handles visual presentation:
- **Resets & Variables**: Defines colors, fonts, and base styles.
- **Grid Layout**: Uses CSS Grid for the responsive project cards layout.
- **Animations**: Keyframes for fade-in effects.
- **Modal Styling**: Position and z-index management for the overlay.
