# Interactive Product Page Documentation

**Category**: Web Development
**Path**: `Web/InteractiveProductPage`
**Version**: 1.0

## Overview
The **Interactive Product Page** is a high-fidelity e-commerce detail view designed for showcasing a premium tech product (e.g., high-end headphones). It emphasizes visual feedback and micro-interactions to create a compelling "Add to Cart" experience without a full backend.

## Key Features

### 1. Dynamic Customization
- **Color Selector**: Changing the color (Midnight Black, Silver, Ocean Blue, Rose Gold) updates:
  - The UI accent color (buttons, highlights) via CSS variables.
  - The text label describing the selected color.
  - A subtle background glow effect (`radial-gradient`) to match the product's aesthetic.
- **Variant Switcher**: Toggling between Standard/Pro/Max models instantly updates the displayed price (`$299`, `$399`, etc.).

### 2. Gallery & Media
- **Thumbnail Switcher**: Clicking secondary thumbnails fades the main product image out and in, swapping the source URL for a smooth transition.
- **Micro-Animations**: All interactive elements (buttons, quantity toggles, tabs) feature hover states and active transforms.

### 3. Shopping Interactions
- **Quantity Logic**: +/- buttons adjust the count (capped between 1 and 10), dynamically recalculating the total price shown.
- **Add to Cart**:
  - Triggers a "Success" notification toast.
  - Updates the cart icon counter in the header with a pulse animation.
  - Changes the button text temporarily to "Added!".
- **Wishlist**: A toggleable heart icon tracks "favorite" status.

## Architecture

### File Structure
```
InteractiveProductPage/
├── index.html      # Structure: Hero, Details, Tabs
├── style.css       # CSS Grid, Variables, Animations
└── script.js       # Logic for state (color, price, cart)
```

### State Management (`script.js`)
The page maintains a simple state object to track user choices:
```javascript
let state = {
    cart: { items: 0, total: 0 },
    currentColor: 'black',
    currentVariant: 'standard',
    currentPrice: 299,
    quantity: 1
};
```

## Usage Guide

### Viewing the Product
1.  Open `index.html`.
2.  **Customize**: Click the circular color swatches to see the theme change. Scroll down to select a "Pro" variant.
3.  **Inspect**: Click the "Specs" tab to read technical details.
4.  **Buy**: Increase quantity to 2, then click **"Add to Cart"**. Watch the header icon update.
