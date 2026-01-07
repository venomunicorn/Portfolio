# Chatbot Documentation

**Category**: Python Systems / AI
**Path**: `Python/Chatbot`
**Version**: 1.0

## Overview
The **Chatbot** project is an intelligent conversational agent implemented in Python. It uses Regular Expressions (Regex) to map user inputs to predefined responses, simulating a natural conversation. The chatbot features context switching, allowing it to toggle between a "Standard" chitchat mode and a "Tech Support" mode.

## Key Features

### 1. Python Logic (`main.py`)
- **Regex Pattern Matching**: Uses `re.search` to find keywords in user input (e.g., matching `hello|hi|hey` to detect greetings).
- **Mode Switching**: Maintains a state variable (`self.mode`) to handle different contexts.
  - **Standard Mode**: Generic conversation (Greetings, name inquiries).
  - **Support Mode**: Specialized technical assistance (Password reset, lag fixes).
- **Randomized Responses**: Selects from a list of potential answers for each trigger to keep conversations feeling fresh.
- **Graceful Failure**: Provides fallback responses ("Could you rephrase that?") when input doesn't match known patterns.

### 2. GUI Application (`gui_main.py`)
- *Note: Provides a desktop graphical interface where users can chat in a windowed environment, likely using Tkinter.*

### 3. Web Demo
The web-based interface mimics a modern mobile messaging app:
- **Typing Indicators**: Displays a "..." animation before the bot responds to simulate processing time.
- **Message Bubbles**: Distinct styles for User (Green/Right) and Bot (Grey/Left) messages.
- **Mode Toggles**: Dedicated buttons in the header to switch between "General" and "Tech Support" modes instantly.
- **Timestamping**: Adds real-time clock stamps to every message.

## Architecture

### Directory Structure
```
Chatbot/
├── main.py         # core Regex Chatbot
├── gui_main.py     # Desktop UI Wrapper
└── demo.html       # Web Simulation
```

### Pattern Matching Logic
The core logic iterates through a dictionary of patterns:
```python
responses = {
    r'slow|lag': ["Have you tried restarting?", ...],
    r'error': ["Check the logs.", ...]
}
for pattern, replies in current_responses.items():
    if re.search(pattern, user_input):
        return random.choice(replies)
```

## Setup & Execution

### Prerequisites
- Python 3.x

### Running the Console App
1.  **Navigate**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\Python\Chatbot"
    ```
2.  **Run**:
    ```powershell
    python main.py
    ```

### Expected Output
```
🤖 PyBot Online. Type 'bye' to exit.
You: Hello
Bot: Hi! How can I help?
You: support
Bot: Switching to Tech Support Mode...
You: my computer is slow
Bot: Have you tried restarting your device?
```

## Web Demo Usage
- Open `demo.html` in a web browser.
- **General Chat**: Ask "Who are you?" or say "Hello".
- **Tech Support**: Click the "Tech Support" button, then ask about "Python" or "Errors".
