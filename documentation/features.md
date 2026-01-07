# Features of the 21APEXchallenge Portfolio Website

This document outlines the key features and functionalities of the main portfolio website found in the `portfolio/` directory.

## 1. Dynamic Project Rendering
- **Data-Driven**: All projects are loaded dynamically from a single JavaScript file (`data.js`). This makes adding or updating projects easy without modifying the HTML structure.
- **Project Cards**: Each project is displayed as a card containing:
  - Project Title
  - Description
  - Category Badge (Web, Python, C++)
  - Key Features List (Top 3 features)
  - "GUI App" Badge (for relevant Python projects)
  - Run Command (for Python scripts)
  - "Live Demo" button (if available)
  - "View Code" link

## 2. Interactive Filtering & Search
- **Category Filters**: Users can filter projects by domain with a single click:
  - **All**: Show all 57+ projects.
  - **Web**: HTML/CSS/JS and Web Apps.
  - **Python**: Automation scripts, ML models, and GUIs.
  - **C++**: System tools, games, and engines.
- **Real-Time Search**: A search bar allows users to filter projects instantly by name or description keywords.

## 3. Project Dashboard Statistics
- **Live Counts**: The top of the page displays real-time statistics based on the currently loaded data:
  - Total Projects
  - Web Projects count
  - Python Projects count
  - C++ Projects count

## 4. Integrated Demo Viewer
- **Modal Logic**: Projects with a `demo_url` can be previewed directly within the portfolio using a modal overlay.
- **IFrame Integration**: The modal uses an `<iframe>` to load the project's demo file (e.g., `demo.html`) without navigating away from the main list.
- **External Link**: Options to open the demo in a new tab are provided for a full-screen experience.

## 5. User Interface (UI) & User Experience (UX)
- **Responsive Design**: The layout adapts seamlessly to different screen sizes (desktop, tablet, mobile).
- **Theming**:
  - Uses the **Outfit** Google Font for modern typography.
  - Dynamic background gradients for a premium look.
  - Smooth animations for card appearance (staggered fade-in).
  - Distinct color-coding for different project categories (e.g., specific colors for Web, Python, C++ tags).

## 6. Development & Maintenance
- **Scalable Architecture**: The separation of data (`data.js`) from logic (`main.js`) and presentation (`index.html`) ensures the codebase is easy to maintain.
- **Automated Statistics**: The stats card automatically updates based on the content of the `projects` array, eliminating manual counting.
