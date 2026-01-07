# Luxe E-commerce Platform Documentation

**Category**: Web Development
**Path**: `Web/E-commercePlatform`
**Version**: 1.0

## Overview
The **Luxe E-commerce Platform** is a fully functional, front-end demo of a luxury online store. It features a curated product catalog, a slide-out shopping cart, real-time total calculation, and a multi-step checkout modal. The design emphasizes high-quality visuals and a smooth user experience (UX) typical of high-end bag and clothing retailers.

## Key Features

### 1. Product Catalog & Filtering
- **Dynamic Rendering**: Products are loaded via JavaScript from a structured array, making the catalog easy to update.
- **Category Filtering**: Users can filter items by Bags, Clothing, Accessories, or Footwear using the sticky navigation menu.
- **Quick View**: Clicking a product card opens a modal overlay (`quickViewModal`) with larger imagery, detailed descriptions, and a direct "Add to Bag" button.

### 2. Shopping Cart System
- **Slide-Out Drawer**: The cart (`cartSidebar`) slides in from the right, preventing navigation away from the current page.
- **State Management**: Cart state (items, quantities) is persisted in `localStorage` (`luxe_cart`), ensuring items remain after a refresh.
- **Quantity Controls**: Users can increment, decrement, or remove items directly from the cart drawer.
- **Live Totals**: Subtotals and the grand total are recalculated instantly upon any change.

### 3. Checkout Flow
- **Order Summary**: Displays a line-item breakdown of the purchase before payment.
- **Simulated Payment**: Includes a mock credit card form (validation placeholders included).
- **Success State**: Upon "placing order," the user receives a confirmation message, and the cart is programmatically cleared.

## Architecture

### File Structure
```
E-commercePlatform/
├── index.html      # Structure: Header, Hero, Grid, Modals
├── style.css       # Grid layout, animations (slide-in), responsive design
└── script.js       # Product data, Cart logic, Modal handling
```

### Data Model (`script.js`)
Products are defined as constant objects:
```javascript
{
    id: 1,
    name: "Canvas Tote Bag",
    price: 45.00,
    category: "Bags",
    img: "https://..."
}
```

### Layout Responsiveness
- **Desktop**: 3-column grid layout for products.
- **Mobile**: Single-column layout with a hamburger menu (if implemented) or simplified navigation.
- **Modals**: Full-screen overlays on mobile, centered dialogs on desktop.

## Usage Guide

### Browsing & Buying
1.  Open `index.html`.
2.  Click **"Shop Now"** to scroll to the collection.
3.  Hover over an item and click **"Add to Bag"**.
4.  Open the Cart (top right icon).
5.  Click **"Checkout"**.
6.  Fill in dummy details and click **"Place Order"** to see the success screen.

### Customization
- **Add Products**: Edit the `products` array in `script.js` to add new inventory.
- **Change Images**: Update the `img` URLs to point to your own product photography.
