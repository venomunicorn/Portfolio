"""
Number Guessing Game GUI Application
Built with Tkinter - Part of 21APEX Challenge
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import threading

class NumberGuessingGameGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Number Guessing Game")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        self.root.configure(bg='#0d1117')
        
        # Colors
        self.colors = {
            'bg': '#0d1117',
            'card': '#161b22',
            'primary': '#58a6ff',
            'success': '#3fb950',
            'warning': '#d29922',
            'danger': '#f85149',
            'text': '#c9d1d9',
            'text_dim': '#8b949e',
            'accent': '#a371f7'
        }
        
        # Game state
        self.secret_number = None
        self.max_number = 100
        self.max_attempts = 10
        self.attempts_left = 10
        self.game_active = False
        self.guess_history = []
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="🎯 Number Guessing Game",
            font=('Segoe UI', 24, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=(0, 20))
        
        # Difficulty selection card
        diff_card = tk.Frame(main_frame, bg=self.colors['card'], relief='flat')
        diff_card.pack(fill='x', pady=10)
        
        diff_title = tk.Label(
            diff_card,
            text="Select Difficulty",
            font=('Segoe UI', 14, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['card']
        )
        diff_title.pack(pady=(15, 10))
        
        # Difficulty buttons frame
        btn_frame = tk.Frame(diff_card, bg=self.colors['card'])
        btn_frame.pack(pady=(0, 15))
        
        difficulties = [
            ("Easy", 10, 5, self.colors['success']),
            ("Medium", 50, 7, self.colors['warning']),
            ("Hard", 100, 10, self.colors['danger'])
        ]
        
        self.difficulty_var = tk.StringVar(value="Hard")
        
        for text, max_num, attempts, color in difficulties:
            btn = tk.Button(
                btn_frame,
                text=f"{text}\n1-{max_num}",
                font=('Segoe UI', 10, 'bold'),
                fg='white',
                bg=color,
                activebackground=color,
                relief='flat',
                width=10,
                height=2,
                command=lambda m=max_num, a=attempts, t=text: self.set_difficulty(m, a, t)
            )
            btn.pack(side='left', padx=5)
        
        # Game display card
        game_card = tk.Frame(main_frame, bg=self.colors['card'], relief='flat')
        game_card.pack(fill='both', expand=True, pady=10)
        
        # Status display
        self.status_label = tk.Label(
            game_card,
            text="Choose difficulty and press Start!",
            font=('Segoe UI', 14),
            fg=self.colors['text'],
            bg=self.colors['card']
        )
        self.status_label.pack(pady=20)
        
        # Attempts display
        self.attempts_label = tk.Label(
            game_card,
            text=f"Attempts: {self.attempts_left}/{self.max_attempts}",
            font=('Segoe UI', 16, 'bold'),
            fg=self.colors['accent'],
            bg=self.colors['card']
        )
        self.attempts_label.pack()
        
        # Progress bar for attempts
        self.progress = ttk.Progressbar(
            game_card,
            length=300,
            mode='determinate',
            maximum=100
        )
        self.progress.pack(pady=15)
        self.progress['value'] = 100
        
        # Guess input frame
        input_frame = tk.Frame(game_card, bg=self.colors['card'])
        input_frame.pack(pady=15)
        
        self.guess_entry = tk.Entry(
            input_frame,
            font=('Segoe UI', 24, 'bold'),
            width=8,
            justify='center',
            bg=self.colors['bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            relief='flat'
        )
        self.guess_entry.pack(side='left', padx=5, ipady=10)
        self.guess_entry.bind('<Return>', lambda e: self.make_guess())
        
        self.guess_btn = tk.Button(
            input_frame,
            text="Guess",
            font=('Segoe UI', 14, 'bold'),
            fg='white',
            bg=self.colors['primary'],
            activebackground=self.colors['primary'],
            relief='flat',
            padx=20,
            pady=10,
            command=self.make_guess,
            state='disabled'
        )
        self.guess_btn.pack(side='left', padx=5)
        
        # Hint display
        self.hint_label = tk.Label(
            game_card,
            text="",
            font=('Segoe UI', 18, 'bold'),
            fg=self.colors['warning'],
            bg=self.colors['card']
        )
        self.hint_label.pack(pady=10)
        
        # Guess history
        history_frame = tk.Frame(game_card, bg=self.colors['card'])
        history_frame.pack(fill='x', padx=20, pady=10)
        
        history_title = tk.Label(
            history_frame,
            text="Previous Guesses:",
            font=('Segoe UI', 11),
            fg=self.colors['text_dim'],
            bg=self.colors['card']
        )
        history_title.pack(anchor='w')
        
        self.history_label = tk.Label(
            history_frame,
            text="",
            font=('Segoe UI', 12),
            fg=self.colors['text'],
            bg=self.colors['card'],
            wraplength=400
        )
        self.history_label.pack(anchor='w')
        
        # Control buttons
        control_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        control_frame.pack(fill='x', pady=10)
        
        self.start_btn = tk.Button(
            control_frame,
            text="▶ Start Game",
            font=('Segoe UI', 12, 'bold'),
            fg='white',
            bg=self.colors['success'],
            activebackground=self.colors['success'],
            relief='flat',
            padx=30,
            pady=10,
            command=self.start_game
        )
        self.start_btn.pack(side='left', padx=5)
        
        self.reset_btn = tk.Button(
            control_frame,
            text="↻ Reset",
            font=('Segoe UI', 12, 'bold'),
            fg='white',
            bg=self.colors['danger'],
            activebackground=self.colors['danger'],
            relief='flat',
            padx=30,
            pady=10,
            command=self.reset_game
        )
        self.reset_btn.pack(side='left', padx=5)
        
        self.ai_btn = tk.Button(
            control_frame,
            text="🤖 AI Demo",
            font=('Segoe UI', 12, 'bold'),
            fg='white',
            bg=self.colors['accent'],
            activebackground=self.colors['accent'],
            relief='flat',
            padx=30,
            pady=10,
            command=self.ai_demo
        )
        self.ai_btn.pack(side='left', padx=5)
    
    def set_difficulty(self, max_num, attempts, text):
        self.max_number = max_num
        self.max_attempts = attempts
        self.attempts_left = attempts
        self.status_label.config(text=f"Difficulty: {text} (1-{max_num}, {attempts} attempts)")
        self.attempts_label.config(text=f"Attempts: {attempts}/{attempts}")
        self.progress['value'] = 100
    
    def start_game(self):
        self.secret_number = random.randint(1, self.max_number)
        self.attempts_left = self.max_attempts
        self.game_active = True
        self.guess_history = []
        
        self.status_label.config(text=f"Guess a number between 1 and {self.max_number}")
        self.hint_label.config(text="")
        self.history_label.config(text="")
        self.attempts_label.config(text=f"Attempts: {self.attempts_left}/{self.max_attempts}")
        self.progress['value'] = 100
        
        self.guess_entry.config(state='normal')
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()
        self.guess_btn.config(state='normal')
        self.start_btn.config(state='disabled')
    
    def make_guess(self):
        if not self.game_active:
            return
        
        try:
            guess = int(self.guess_entry.get())
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid number!")
            return
        
        if guess < 1 or guess > self.max_number:
            messagebox.showwarning("Out of Range", f"Please guess between 1 and {self.max_number}!")
            return
        
        self.attempts_left -= 1
        self.guess_history.append(guess)
        self.history_label.config(text=" → ".join(map(str, self.guess_history)))
        
        # Update attempts display
        self.attempts_label.config(text=f"Attempts: {self.attempts_left}/{self.max_attempts}")
        self.progress['value'] = (self.attempts_left / self.max_attempts) * 100
        
        if guess == self.secret_number:
            self.game_won()
        elif guess < self.secret_number:
            self.hint_label.config(text="📈 Too LOW! Go higher!", fg=self.colors['primary'])
        else:
            self.hint_label.config(text="📉 Too HIGH! Go lower!", fg=self.colors['danger'])
        
        if self.attempts_left <= 0 and guess != self.secret_number:
            self.game_lost()
        
        self.guess_entry.delete(0, tk.END)
    
    def game_won(self):
        self.game_active = False
        attempts_used = self.max_attempts - self.attempts_left
        self.status_label.config(
            text=f"🎉 CONGRATULATIONS! You got it in {attempts_used} attempts!",
            fg=self.colors['success']
        )
        self.hint_label.config(text=f"The number was {self.secret_number}!", fg=self.colors['success'])
        self.guess_entry.config(state='disabled')
        self.guess_btn.config(state='disabled')
        self.start_btn.config(state='normal')
    
    def game_lost(self):
        self.game_active = False
        self.status_label.config(
            text="😞 Game Over! Better luck next time!",
            fg=self.colors['danger']
        )
        self.hint_label.config(text=f"The number was {self.secret_number}", fg=self.colors['danger'])
        self.guess_entry.config(state='disabled')
        self.guess_btn.config(state='disabled')
        self.start_btn.config(state='normal')
    
    def reset_game(self):
        self.game_active = False
        self.secret_number = None
        self.attempts_left = self.max_attempts
        self.guess_history = []
        
        self.status_label.config(text="Choose difficulty and press Start!", fg=self.colors['text'])
        self.hint_label.config(text="")
        self.history_label.config(text="")
        self.attempts_label.config(text=f"Attempts: {self.max_attempts}/{self.max_attempts}")
        self.progress['value'] = 100
        
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.config(state='disabled')
        self.guess_btn.config(state='disabled')
        self.start_btn.config(state='normal')
    
    def ai_demo(self):
        """AI solving the game using binary search"""
        self.start_game()
        self.game_active = False  # Disable player input during AI demo
        self.guess_entry.config(state='disabled')
        self.guess_btn.config(state='disabled')
        
        self.status_label.config(text="🤖 AI is solving using Binary Search...")
        
        # Run AI demo in a separate thread
        threading.Thread(target=self._ai_solve, daemon=True).start()
    
    def _ai_solve(self):
        low = 1
        high = self.max_number
        
        while low <= high and self.attempts_left > 0:
            time.sleep(0.8)  # Delay for visualization
            
            guess = (low + high) // 2
            self.guess_history.append(guess)
            self.attempts_left -= 1
            
            # Update UI from main thread
            self.root.after(0, self._update_ai_guess, guess, low, high)
            
            if guess == self.secret_number:
                self.root.after(0, self._ai_won, guess)
                return
            elif guess < self.secret_number:
                low = guess + 1
            else:
                high = guess - 1
    
    def _update_ai_guess(self, guess, low, high):
        self.history_label.config(text=" → ".join(map(str, self.guess_history)))
        self.attempts_label.config(text=f"Attempts: {self.attempts_left}/{self.max_attempts}")
        self.progress['value'] = (self.attempts_left / self.max_attempts) * 100
        
        if guess < self.secret_number:
            self.hint_label.config(text=f"AI: {guess} - Too LOW! Range: [{guess+1}-{self.max_number}]", fg=self.colors['primary'])
        else:
            self.hint_label.config(text=f"AI: {guess} - Too HIGH! Range: [1-{guess-1}]", fg=self.colors['danger'])
    
    def _ai_won(self, guess):
        attempts_used = self.max_attempts - self.attempts_left
        self.status_label.config(
            text=f"🤖 AI found {guess} in {attempts_used} attempts!",
            fg=self.colors['success']
        )
        self.hint_label.config(text=f"Binary Search: O(log n) complexity!", fg=self.colors['accent'])
        self.start_btn.config(state='normal')
    
    def run(self):
        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.root.mainloop()

if __name__ == "__main__":
    app = NumberGuessingGameGUI()
    app.run()
