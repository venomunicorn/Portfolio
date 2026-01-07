# Connect 2025 - Social Media Landing Page Documentation

**Category**: Web Development
**Path**: `Web/SocialMediaLandingPage`
**Version**: 1.0

## Overview
**Connect 2025** is a high-conversion landing page for a fictional next-generation social network. It is designed to capture user interest and drive waitlist sign-ups for an upcoming product launch. The page features modern aesthetics (glassmorphism, gradients), scroll animations, and interactive elements.

## Key Features

### 1. Waitlist Engine
- **Email Capture**: Two strategically placed forms (Hero section and Footer CTA) collect user emails.
- **Validation**: Checks for valid email formats before submission.
- **Feedback Loop**:
  - The submit button shows a loading spinner.
  - On success, it transforms to "You're In!" with a green checkmark.
  - A contextual note updates to welcome the user.

### 2. Animated UI
- **Count Up Stats**: The "Waitlist" number (e.g., 15,847) animates from 0 to the target value when scrolled into view using `IntersectionObserver`.
- **Scroll Reveal**: Sections like Features, Steps, and Testimonials fade in and slide up as the user scrolls down the page.
- **Live Phone Mockup**: (CSS-based) A stylized representation of the mobile app interface in the hero section.

### 3. Informational Sections
- **Features Grid**: Highlights key selling points (Chronological Feed, Privacy First, Zero Ads).
- **How It Works**: A 3-step timeline (Sign Up -> Connect -> Share) explaining the onboarding process.
- **Testimonials**: Social proof cards with star ratings and user avatars.
- **Pricing**: A comparative table (Free vs Pro vs Team) with a "Most Popular" highlight.
- **FAQ**: An interactive accordion section for common questions.

## Architecture

### File Structure
```
SocialMediaLandingPage/
├── index.html      # Structure: Hero, Features, Pricing, Waitlist
├── style.css       # Visuals: Gradients, Animations, Responsive layouts
└── script.js       # Logic: Scroll observers, Form handling, Mobile menu
```

### Design System
- **Typography**: Uses `Space Grotesk` for a modern, tech-forward feel.
- **Color Palette**: Dark mode base (`#0f172a`) with vibrant gradients (Violet/Pink/Cyan) to create a "Web3/Future" vibe.
- **Effects**: Background "blobs" with blur filters create a dynamic, moving backdrop.

## Usage Guide

### Simulation
1.  Open `index.html`.
2.  Scroll down to see elements animate in.
3.  Click "Get Early Access" to smooth-scroll back to the hero form.
4.  Enter a dummy email (e.g., `test@example.com`) and click "Join Waitlist" to see the success state.
5.  Click on FAQ questions to toggle the answers.

### Customization
- **Waitlist Target**: Change `data-target="15847"` in `index.html` line 53 to adjust the counter end value.
- **Pricing**: Edit the `pricing-grid` section in `index.html` to modify plans.
