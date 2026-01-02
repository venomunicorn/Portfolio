"""
Chatbot GUI Application
Built with Tkinter - Part of 21APEX Challenge
"""

import tkinter as tk
from tkinter import ttk
import re
import random
from datetime import datetime

class ChatbotGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PyBot - AI Chatbot")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        self.root.configure(bg='#1a1a2e')
        
        # Colors - Modern chat theme
        self.colors = {
            'bg': '#1a1a2e',
            'card': '#16213e',
            'primary': '#0f3460',
            'user_bubble': '#4361ee',
            'bot_bubble': '#2d3e50',
            'success': '#00b894',
            'warning': '#fdcb6e',
            'text': '#ffffff',
            'text_dim': '#b0b0b0',
            'input_bg': '#0d1b2a'
        }
        
        # Bot responses
        self.mode = "standard"
        self.responses = {
            r'hello|hi|hey|greetings': [
                "Hello there! 👋",
                "Hi! How can I help you today?",
                "Hey! Nice to chat with you!"
            ],
            r'how are you|how\'s it going': [
                "I'm running great, thanks for asking! 🤖",
                "All systems operational! How about you?",
                "Doing well! Ready to help with anything."
            ],
            r'your name|who are you': [
                "I'm PyBot, your friendly AI assistant! 🤖",
                "Call me PyBot - I'm here to help!",
                "I'm PyBot v1.0, built with Python!"
            ],
            r'what can you do|help|features': [
                "I can chat about various topics! Try asking:\n• About me\n• For tech support (type 'support')\n• Tell me a joke\n• What's the time?",
                "I'm a conversational bot! I can chat, help with tech issues, and more."
            ],
            r'joke|funny|laugh': [
                "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
                "Why did the developer go broke? Because he used up all his cache! 💰",
                "There are only 10 types of people: those who understand binary and those who don't! 🔢"
            ],
            r'time|clock|what time': [
                f"It's currently {datetime.now().strftime('%H:%M:%S')} ⏰"
            ],
            r'thanks|thank you|appreciate': [
                "You're welcome! 😊",
                "Happy to help!",
                "Anytime! Feel free to ask more."
            ],
            r'bye|goodbye|exit|quit': [
                "Goodbye! Have a great day! 👋",
                "See you later! Take care!",
                "Bye! Come back anytime!"
            ]
        }
        
        self.support_responses = {
            r'slow|lag|performance': [
                "Performance issues? Try these:\n• Restart your device\n• Close unused apps\n• Check for updates",
                "Lag can be caused by many things. Have you tried restarting?"
            ],
            r'crash|error|bug': [
                "Crashes can be frustrating! Try:\n• Reinstall the app\n• Clear cache\n• Check for updates",
                "What error message are you seeing? That can help diagnose the issue."
            ],
            r'password|login|access': [
                "Password issues?\n• Use 'Forgot Password'\n• Check Caps Lock\n• Try a different browser",
                "Make sure Caps Lock is off and try again. If still stuck, reset your password."
            ],
            r'internet|connection|wifi': [
                "Connection troubles?\n• Restart your router\n• Check if other devices work\n• Run network diagnostics",
                "Try restarting your router. If the issue persists, contact your ISP."
            ]
        }
        
        self.setup_ui()
        self.add_bot_message("Hello! I'm PyBot 🤖\n\nAsk me anything, or type 'support' for tech help!")
        
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=70)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Bot avatar and name
        avatar_frame = tk.Frame(header_frame, bg=self.colors['primary'])
        avatar_frame.pack(side='left', padx=20, pady=10)
        
        tk.Label(
            avatar_frame,
            text="🤖",
            font=('Segoe UI', 28),
            bg=self.colors['primary']
        ).pack(side='left')
        
        info_frame = tk.Frame(avatar_frame, bg=self.colors['primary'])
        info_frame.pack(side='left', padx=10)
        
        tk.Label(
            info_frame,
            text="PyBot",
            font=('Segoe UI', 16, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['primary']
        ).pack(anchor='w')
        
        self.status_label = tk.Label(
            info_frame,
            text="● Online",
            font=('Segoe UI', 10),
            fg=self.colors['success'],
            bg=self.colors['primary']
        )
        self.status_label.pack(anchor='w')
        
        # Mode indicator
        self.mode_label = tk.Label(
            header_frame,
            text="Standard Mode",
            font=('Segoe UI', 10),
            fg=self.colors['text_dim'],
            bg=self.colors['primary']
        )
        self.mode_label.pack(side='right', padx=20)
        
        # Chat display area
        chat_container = tk.Frame(self.root, bg=self.colors['bg'])
        chat_container.pack(fill='both', expand=True)
        
        # Scrollable chat
        self.chat_canvas = tk.Canvas(
            chat_container,
            bg=self.colors['bg'],
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(chat_container, orient='vertical', command=self.chat_canvas.yview)
        
        self.chat_frame = tk.Frame(self.chat_canvas, bg=self.colors['bg'])
        
        self.chat_canvas.create_window((0, 0), window=self.chat_frame, anchor='nw', width=480)
        
        self.chat_frame.bind('<Configure>', lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox('all')))
        self.chat_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.chat_canvas.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y')
        
        # Input area
        input_frame = tk.Frame(self.root, bg=self.colors['card'], height=80)
        input_frame.pack(fill='x', side='bottom')
        input_frame.pack_propagate(False)
        
        input_container = tk.Frame(input_frame, bg=self.colors['card'])
        input_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        self.message_entry = tk.Entry(
            input_container,
            font=('Segoe UI', 13),
            bg=self.colors['input_bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            relief='flat'
        )
        self.message_entry.pack(side='left', fill='both', expand=True, ipady=12, padx=(0, 10))
        self.message_entry.bind('<Return>', lambda e: self.send_message())
        self.message_entry.focus()
        
        send_btn = tk.Button(
            input_container,
            text="Send ➤",
            font=('Segoe UI', 11, 'bold'),
            fg='white',
            bg=self.colors['user_bubble'],
            activebackground=self.colors['success'],
            relief='flat',
            padx=20,
            pady=10,
            command=self.send_message
        )
        send_btn.pack(side='right')
        
    def add_message_bubble(self, message, is_user=False):
        """Add a message bubble to the chat"""
        bubble_frame = tk.Frame(self.chat_frame, bg=self.colors['bg'])
        bubble_frame.pack(fill='x', padx=10, pady=5)
        
        # Determine bubble color and alignment
        if is_user:
            bg_color = self.colors['user_bubble']
            anchor = 'e'
        else:
            bg_color = self.colors['bot_bubble']
            anchor = 'w'
        
        # Message bubble
        bubble = tk.Label(
            bubble_frame,
            text=message,
            font=('Segoe UI', 11),
            fg=self.colors['text'],
            bg=bg_color,
            wraplength=300,
            justify='left' if not is_user else 'right',
            padx=15,
            pady=10
        )
        bubble.pack(anchor=anchor)
        
        # Timestamp
        time_label = tk.Label(
            bubble_frame,
            text=datetime.now().strftime('%H:%M'),
            font=('Segoe UI', 8),
            fg=self.colors['text_dim'],
            bg=self.colors['bg']
        )
        time_label.pack(anchor=anchor)
        
        # Scroll to bottom
        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)
    
    def add_bot_message(self, message):
        self.add_message_bubble(message, is_user=False)
    
    def add_user_message(self, message):
        self.add_message_bubble(message, is_user=True)
    
    def send_message(self):
        message = self.message_entry.get().strip()
        if not message:
            return
        
        # Add user message
        self.add_user_message(message)
        self.message_entry.delete(0, tk.END)
        
        # Get bot response after a short delay
        self.root.after(500, lambda: self.get_response(message))
    
    def get_response(self, user_input):
        user_input_lower = user_input.lower()
        
        # Mode switching
        if 'support' in user_input_lower and self.mode == 'standard':
            self.mode = 'support'
            self.mode_label.config(text="Support Mode", fg=self.colors['warning'])
            self.add_bot_message("🛠️ Switched to Tech Support Mode!\n\nWhat seems to be the problem?\n(Type 'back' to return to normal chat)")
            return
        
        if ('back' in user_input_lower or 'exit' in user_input_lower) and self.mode == 'support':
            self.mode = 'standard'
            self.mode_label.config(text="Standard Mode", fg=self.colors['text_dim'])
            self.add_bot_message("Returning to Standard Mode. How can I help? 😊")
            return
        
        # Get appropriate response set
        responses = self.support_responses if self.mode == 'support' else self.responses
        
        # Find matching response
        for pattern, replies in responses.items():
            if re.search(pattern, user_input_lower):
                response = random.choice(replies)
                # Update time dynamically
                if 'time' in pattern:
                    response = f"It's currently {datetime.now().strftime('%H:%M:%S')} ⏰"
                self.add_bot_message(response)
                return
        
        # Default response
        if self.mode == 'support':
            self.add_bot_message("I'm not sure about that specific issue. Try describing your problem differently, or type 'back' to return to chat.")
        else:
            self.add_bot_message("I'm not sure I understand. Could you rephrase that? 🤔\n\nOr try asking for 'help' to see what I can do!")
    
    def run(self):
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        
        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.root.mainloop()

if __name__ == "__main__":
    app = ChatbotGUI()
    app.run()
