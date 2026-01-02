# Nexus Creative - Static Website Documentation

**Category**: Web Development
**Path**: `Web/StaticWebsite`
**Version**: 1.0

## Overview
**Nexus Creative** is a professional, multi-section static agency portfolio. It serves as a classic example of a "Brochure Website," designed to showcase services, past work (portfolio), team members, and client testimonials. It emphasizes clean layout, responsive design, and smooth user interactions.

## Key Features

### 1. Robust Theming System
- **Dark/Light Mode**: Full CSS variable-based theme engine. The state is persisted in `localStorage` (`theme: 'dark'|'light'`), checking the preference on load to prevent flash-of-unstyled-content (FOUC).
- **CSS Variables**: Uses `--bg-color`, `--text-primary`, `--accent-color` etc. to instantly swap color palettes across the entire site.

### 2. Interactive Components
- **Counter Animation**: "Stat numbers" in the hero section (e.g., "500+ Clients") animate from 0 up to their target value when the page loads.
- **Scroll Spy**: The navigation bar becomes translucent and adds a shadow (`.scrolled`) when the user scrolls down, ensuring menu visibility without blocking content.
- **Scroll Reveal**: Elements like service cards and portfolio items fade in and slide up (`.animate-in`) as they enter the viewport using `IntersectionObserver`.

### 3. Contact Functionality
- **Form Simulation**: The contact form captures Name, Email, and Message inputs.
- **Validation**: Basic Javascript validation ensures fields are not empty.
- **Feedback**: Displays a success notification ("Message Sent!") and disables the button temporarily to prevent double submissions.

## Architecture

### File Structure
```
StaticWebsite/
├── index.html      # semantic HTML5 Structure (Header, Sections, Footer)
├── style.css       # CSS Grid/Flexbox, Media Queries, Theme Variables
└── script.js       # Navigation logic, Scroll observers, Form handling
```

### Sections
1.  **Hero**: Large headline, CTA buttons, and animated success stats.
2.  **About**: Agency introduction with visual feature list.
3.  **Services**: Grid of offering cards (Design, Dev, Marketing).
4.  **Portfolio**: Gallery of project thumbnails with hover effects.
5.  **Testimonials**: Sliding cards with client reviews.
6.  **Team**: Profiles of key team members.
7.  **Contact**: Layout with contact info (Phone/Email) side-by-side with the inquiry form.

## Usage Guide

### Navigation
- **Desktop**: Use the top navigation bar to smooth-scroll to specific sections.
- **Mobile**: Use the "Hamburger" menu icon to toggle the slide-down mobile navigation.

### Theming
- Click the **Moon/Sun icon** in the navbar to toggle between the dark and light themes.

### Responsiveness
- Resize the browser window to see the grid layouts adjust from 3 columns (Desktop) to 2 (Tablet) to 1 (Mobile).
