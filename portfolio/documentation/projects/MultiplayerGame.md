# Neon Hockey - Multiplayer Game Documentation

**Category**: Web Development
**Path**: `Web/MultiplayerGame`
**Version**: 1.0

## Overview
**Neon Hockey** is a local multiplayer arcade game inspired by Pong. Two players share the same keyboard to compete in a fast-paced game of digital air hockey/table tennis. It runs entirely in the browser using the HTML5 `<canvas>` API for high-performance 2D rendering.

## Key Features

### 1. Local Multiplayer
- **Split Controls**:
  - **Player 1 (Left)**: Controls the Cyan paddle using `W` (Up) and `S` (Down).
  - **Player 2 (Right)**: Controls the Magenta paddle using `Arrow Up` and `Arrow Down`.
- **Simultaneous Input**: Uses an object-based key tracking system (`keys['w'] = true`) to ensure both players can move smoothly at the same time without ghosting or locking.

### 2. Physics & Gameplay
- **Collision Detection**: Checks for intersections between the ball coordinate and the paddle rectangles.
- **Dynamic Difficulty**: The ball speeds up slightly (`dx += 0.5`) every time it hits a paddle, making rallies increasingly intense.
- **Scoring**: Points are awarded when the ball passes the opponent's paddle (crosses `x < 0` or `x > width`). The ball resets to the center with a random serving direction.

### 3. Visuals
- **Retro Aesthetic**: Features a high-contrast black background with neon Cyan and Magenta paddles.
- **Center Court**: A dashed line divides the play area, mimicking a real sports court.
- **Glow Effects**: CSS `box-shadow` gives the game board a glowing arcade cabinet look.

## Architecture

### File Structure
```
MultiplayerGame/
└── index.html      # Single-file game (HTML + CSS + JS)
```
*Note: This project is self-contained in a single HTML file for portability.*

### Game Loop (`index.html`)
The game uses the standard `requestAnimationFrame` pattern:
1.  **Update()**: Calculates new positions for paddles and ball based on input and velocity. Handles collisions and scoring.
2.  **Draw()**: Clears the canvas and repaints the game state (Paddles, Ball, Net).
3.  **Repeat**: Runs at the browser's native refresh rate (usually 60fps).

## Usage Guide

### How to Play
1.  Open `index.html` in a web browser.
2.  **Player 1** places left hand on `W/S`.
3.  **Player 2** places right hand on Arrow Keys.
4.  The game starts immediately.
5.  Defend your side! First player to reach a high score (unlimited in this demo) wins bragging rights. Refresh to restart.
