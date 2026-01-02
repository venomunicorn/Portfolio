# WhatsApp Chatbot Documentation

**Category**: Python Automation
**Path**: `Python/ChatbotWhatsapp`
**Version**: 1.0

## Overview
The **WhatsApp Chatbot** is a console-based automation simulator. While full WhatsApp automation typically requires libraries like `pywhatkit` or `selenium` to control a browser, this project demonstrates the *logic* flow of such an application without requiring complex driver setups or active WhatsApp accounts. It simulates the process of opening WhatsApp Web, finding a contact, and sending a scheduled message.

## Key Features

### 1. Automation Logic Simulation
- **Input Handling**: Accepts target phone number and message content from the user.
- **Workflow Simulation**: Mimics the steps a real bot would take:
  1.  Validate inputs.
  2.  Wait for the target time (Simulated).
  3.  Launch Browser / Find Contact.
  4.  Type Message.
  5.  Send.
- **Console Feedback**: Provides step-by-step logs (`* Opening WhatsApp Web *`, `* Typing... *`) to visualize the automation process.

## Architecture

### Directory Structure
```
ChatbotWhatsapp/
└── main.py         # Automation Simulator
```

### Automation Concept
Real automation scripts often fail due to timing issues (e.g., browser taking too long to load). This script creates a blueprint for handling such delays using `time.sleep()`.

A real implementation would look like this (conceptual):
```python
# import pywhatkit
# pywhatkit.sendwhatmsg(phone, message, hours, minutes)
```
This project replaces the external dependency calls with print statements to ensure the code is runnable and educational in any environment.

## Setup & Execution

### Prerequisites
- Python 3.x

### Running the App
1.  **Navigate**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\Python\ChatbotWhatsapp"
    ```
2.  **Run**:
    ```powershell
    python main.py
    ```

### Expected Output
```
--- WhatsApp Automation Bot ---
Enter Phone Number: +15550199
Enter Message: Hello World
Sending now...

[SIMULATION] Scheduling message for +15550199...
* Opening WhatsApp Web *
* Searching for +15550199 *
* Typing: 'Hello World' *
* Pressed Send *
```

## Future Enhancements
To turn this into a live bot, one would:
1.  Install `pip install pywhatkit`.
2.  Replace `send_message_simulated` with `pywhatkit.sendwhatmsg`.
3.  Ensure a web browser (Chrome) is installed and logged into WhatsApp Web.
