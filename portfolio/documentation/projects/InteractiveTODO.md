# Task Master Documentation

**Category**: Web Development
**Path**: `Web/InteractiveTODO`
**Version**: 1.0

## Overview
**Task Master** is a feature-rich "Todo" application that goes beyond simple list-making. It includes priority tagging, due dates, progress tracking, and persisted local storage. The application features a clean, responsive UI with dark mode support.

## Key Features

### 1. Advanced Task Management
- **Priorities**: Users can assign High (Red), Medium (Yellow), or Low (Green) priority to tasks.
- **Due Dates**: Tasks can have optional deadlines. If a task isn't completed by the due date, it is visually flagged as "Overdue".
- **Inline Editing**: Double-clicking or clicking the edit icon allows users to modify the task text directly within the list.

### 2. Filtering & Searching
- **Facet Filters**: Filter tasks by status (All, Pending, Completed).
- **Priority Filter**: View only "High Priority" items to focus on what's urgent.
- **Live Search**: A search bar filters the list in real-time based on task content.

### 3. Productivity Stats
- **Dashboard**: A header section displays the total count, completed count, and pending count.
- **Progress Bar**: A visual progress bar moves from 0% to 100% as tasks are checked off, gamifying productivity.

### 4. Persistence & Theme
- **Local Storage**: Tasks (`taskmaster_todos`) and theme preferences (`taskmaster_theme`) are saved to the browser, restoring the exact state upon return.
- **Dark Mode**: A toggle switches the entire UI between a light theme and a high-contrast dark theme.

## Architecture

### File Structure
```
InteractiveTODO/
├── index.html      # Layout: Controls, Stats, Lists using Semantic HTML
├── style.css       # CSS Variables for theming, Flexbox for layout
└── script.js       # CRUD logic, Filters, DOM manipulation
```

### Data Model (`script.js`)
Tasks are objects stored in an array:
```javascript
{
    id: 17163829102,
    text: "Finish documentation",
    completed: false,
    priority: "high",
    dueDate: "2025-01-30",
    createdAt: "..."
}
```

## Usage Guide

### Managing Tasks
1.  **Add**: Type a task in the input field, select a priority, optionally pick a date, and press Enter (or click "+").
2.  **Complete**: Click the circle icon to mark a task as done. It will fade out and strike through.
3.  **Edit**: Click the Pencil icon to change the text.
4.  **Delete**: Click the Trash icon to remove it.

### Organizing
- Use the **"High"** filter dropdown to see urgent items.
- Use the **Search** bar to find specific keywords.
- Click the **Moon/Sun** icon to toggle the visual theme.
