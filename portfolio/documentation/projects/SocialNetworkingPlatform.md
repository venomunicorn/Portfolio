# Social Networking Platform Documentation

**Category**: Web Development
**Path**: `Web/SocialNetworkingPlatform`
**Version**: 1.0

## Overview
**Social Networking Platform** is a functional mockup of a Facebook/Instagram-style social media feed. It simulates the core user loop: scrolling through a feed, liking posts, and creating new content. It demonstrates how to manage a dynamic list of objects (posts) and update the DOM efficiently using JavaScript.

## Key Features

### 1. Dynamic Feed
- **Post Rendering**: Automatically generates HTML for each post in the `posts` array.
- **Content Types**: Supports displaying user avatars, names, timestamps, post images (via Lorem Picsum), and captions.
- **Initial Data**: Pre-loaded with sample posts from "Lana Rose" and "John Doe" to demonstrate the layout.

### 2. User Interaction
- **Create Post**: A functional input bar allows users to type a caption and hit Enter/Submit. This adds a new post to the top of the feed (`unshift`) with the user's name ("You") and a random image.
- **Like System**: Toggling the heart icon updates the `liked` state in the data model and re-renders the icon (Solid vs. Outline) to reflect the change.

## Architecture

### File Structure
```
SocialNetworkingPlatform/
├── index.html      # Feed Layout, Sidebar, Create Post Area
├── style.css       # Grid layout, Card styling, Button effects
└── script.js       # Feed rendering, Event listeners
```

### Data Model (`script.js`)
The application state is held in a simple array:
```javascript
const posts = [
    {
        name: 'Lana Rose',
        time: '15 mins ago',
        image: '...',
        caption: 'Enjoying the sunset...',
        liked: false
    }
];
```

## Usage Guide

### Viewing the Feed
1.  Open `index.html`.
2.  Scroll down to see the pre-loaded posts.

### Interacting
1.  **Like**: Click the Heart icon on any post. It will turn solid red (state change).
2.  **Post**: Go to the top text box ("What's on your mind?"). Type "Hello World!" and click "Post".
3.  **Result**: A new card appears instantly at the top with your caption and a randomly generated image.
