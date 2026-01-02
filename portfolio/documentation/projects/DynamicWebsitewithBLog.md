# Minimalist Blog Documentation

**Category**: Web Development
**Path**: `Web/DynamicWebsitewithBLog`
**Version**: 1.0

## Overview
The **Minimalist Blog** is a dynamic, single-page application (SPA) built with vanilla JavaScript. It demonstrates a complete Content Management System (CMS) loop including creating, reading, updating, and deleting (CRUD) blog posts. The application prioritizes a clean, distraction-free reading experience with a focus on typography and whitespace.

## Key Features

### 1. Single Page Architecture (SPA)
- **Hash-Based Routing**: Uses the URL hash (`#home`, `#post/123`, `#new`, `#edit/123`) to navigate between views without reloading the page.
- **View Management**: Dynamically toggles visibility of sections (`homeView`, `postView`, `formView`) based on the current state.

### 2. Post Management (CRUD)
- **Create**: A dedicated form allows users to title, categorize, and write full-length articles.
- **Read**: The homepage lists all posts with excerpts. Clicking a post opens the full view.
- **Update**: Existing posts can be edited, modifying the title, content, or category (updating the `updatedAt` timestamp).
- **Delete**: Users can remove posts permanently with confirmation.

### 3. Data Persistence
- **Local Storage**: All data is saved to the browser's `localStorage` (key: `minimalist_blog_posts`). This ensures posts persist even after the browser is closed.
- **Default Content**: On the first load, the app initializes with a set of sample posts (e.g., "The Art of Minimalism", "Why Vanilla JS?") to demonstrate the layout.

### 4. Search & Filtering
- **Live Search**: The search bar filters posts in real-time by checking both titles and content bodies.
- **Category Filter**: A dropdown allows users to view posts only from specific categories (Design, Development, Thoughts).

## Architecture

### File Structure
```
DynamicWebsitewithBLog/
├── index.html      # Main markup and view containers
├── style.css       # Typography, layout, and "hidden" classes
└── script.js       # SPA Router, State Management, and Event Listeners
```

### Class Structure (`script.js`)
- `BlogPost`: Data model class for post objects.
- `BlogStorage`: Static helper for reading/writing to `localStorage`.
- `Router`: Handles `hashchange` events and switches views.
- `BlogApp`: The main controller that wires event listeners and renders the UI.

## Usage Guide

### Running the Blog
Since this is a client-side only application, it can be run by simply opening `index.html` in any modern web browser. No server setup is required.

### How to Post
1.  Click **"New Post"** in the navigation bar.
2.  Select a category (e.g., "Development").
3.  Enter a Title and Content.
4.  Click **"Save Post"**. It will appear immediately on the Home feed.
