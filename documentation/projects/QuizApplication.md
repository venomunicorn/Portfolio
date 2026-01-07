# Quiz Application - Documentation

**Category**: Web Development
**Path**: `Web/QuizApplication`
**Version**: 1.0

## Overview
The **Quiz Application** is an interactive, multiple-choice quiz engine built with vanilla JavaScript. It is designed to test users' knowledge on web development topics (HTML, CSS, JS) with immediate visual feedback, score tracking, and a results summary.

## Key Features

### 1. Interactive Gameplay
- **Question Engine**: Loads questions dynamically from a structured JavaScript array.
- **Immediate Feedback**: When a user selects an answer:
  - **Correct Choice**: Turns green (`.correct`).
  - **Wrong Choice**: Turns red (`.wrong`), and the correct answer is simultaneously highlighted in green to educate the user.
- **Auto-Advance**: Automatically moves to the next question after a 1.5-second delay, creating a smooth flow without manual "Next" clicks.

### 2. Progress Tracking
- **Header Stats**: Displays the "Current Question / Total" count.
- **Score Counter**: Updates the score in real-time (e.g., "Score: 3") as correct answers are chosen.
- **Progress Bar**: A visual bar fills up as the user progresses through the quiz.

### 3. Results Screen
- **Completion View**: At the end of the quiz, the Question Card is hidden and a Result Card is shown.
- **Dynamic Feedback**: Displays a custom message based on performance:
  - 5/5: "Perfect Score! 🏆"
  - >50%: "Great Job! Keep it up! 👍"
  - <50%: "Keep practicing! 💪"

## Architecture

### File Structure
```
QuizApplication/
├── index.html      # UI Containers (Quiz Card, Result Card)
├── style.css       # Layout, Button styles, Feedback colors (Red/Green)
└── script.js       # Question data, Game logic
```

### Data Structure (`script.js`)
Questions are stored as objects:
```javascript
{
    question: "What does CSS stand for?",
    options: ["Central Style Sheets", "Cascading Style Sheets", ...],
    correct: 1 // Index of the correct answer in the options array
}
```

## Usage Guide

### Playing the Quiz
1.  Open `index.html`.
2.  Read the question card.
3.  Click on one of the 4 option buttons.
4.  Wait for the feedback color (Green/Red) and the automatic transition.
5.  View your final score at the end.

### Customizing Questions
To add your own questions, simply edit the `questions` array in `script.js`. The app automatically adjusts the total count and progress bar calculations.
