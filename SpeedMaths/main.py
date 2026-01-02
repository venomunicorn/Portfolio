import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import random
import time
import csv
import json
from datetime import datetime, timedelta
import threading
import pygame
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Set up customtkinter appearance
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class MathEngine:
    """Core logic for Math Practice Pro"""
    def __init__(self):
        self.difficulty_configs = {
            'addition': {'min_digits': 1, 'max_digits': 3, 'enabled': True, 'level': 1},
            'subtraction': {'min_digits': 1, 'max_digits': 3, 'enabled': True, 'level': 1},
            'multiplication': {'min_digits': 1, 'max_digits': 2, 'enabled': True, 'level': 1},
            'division': {'min_digits': 1, 'max_digits': 2, 'enabled': True, 'level': 1},
            'percentages': {'min_value': 1, 'max_value': 100, 'enabled': True, 'level': 1},
            'fractions': {'min_value': 1, 'max_value': 100, 'enabled': True, 'level': 1},
            'squares': {'min_value': 1, 'max_value': 20, 'enabled': True, 'level': 1},
            'cubes': {'min_value': 1, 'max_value': 10, 'enabled': True, 'level': 1},
            'cube_roots': {'min_value': 1, 'max_value': 1000, 'enabled': True, 'level': 1},
            'mult_tables': {'min_table': 1, 'max_table': 12, 'enabled': True, 'level': 1}
        }
    
    def load_config(self, filepath='config.json'):
        try:
            with open(filepath, 'r') as f:
                saved = json.load(f)
                for k, v in saved.items():
                    if k in self.difficulty_configs:
                        self.difficulty_configs[k].update(v)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save_config(self, filepath='config.json'):
        try:
            with open(filepath, 'w') as f:
                json.dump(self.difficulty_configs, f)
            return True
        except Exception:
            return False

    def generate_question(self, topic, adaptive=False):
        config = self.difficulty_configs[topic]
        level = config.get('level', 1)
        scale = 1.0 + (level * 0.1) if adaptive else 1.0
        
        question, answer, hint = "", "", ""

        if topic == 'addition':
            d_min = config['min_digits']
            d_max = config['max_digits'] + (1 if level > 5 and adaptive else 0)
            min_val = 10**(d_min-1) if d_min > 1 else 1
            max_val = (10**d_max) - 1
            a = random.randint(min_val, max_val)
            b = random.randint(min_val, max_val)
            question = f"{a} + {b}"
            answer = str(a + b)
            hint = f"Sum of {a} and {b}"
            
        elif topic == 'subtraction':
            d_min = config['min_digits']
            d_max = config['max_digits']
            min_val = 10**(d_min-1) if d_min > 1 else 1
            max_val = (10**d_max) - 1
            a = random.randint(min_val, max_val)
            b = random.randint(min_val, a)
            question = f"{a} - {b}"
            answer = str(a - b)
            hint = f"Difference between {a} and {b}"
            
        elif topic == 'multiplication':
            d_min = config['min_digits']
            d_max = config['max_digits']
            min_val = 10**(d_min-1) if d_min > 1 else 1
            max_val = (10**d_max) - 1
            a = random.randint(min_val, max_val)
            b = random.randint(min_val, max_val)
            question = f"{a} × {b}"
            answer = str(a * b)
            hint = f"Product of {a} and {b}"
            
        elif topic == 'division':
            d_min = config['min_digits']
            d_max = config['max_digits']
            result_max = 10**d_max - 1
            b = random.randint(2, 12 + level)
            result = random.randint(2, result_max)
            a = b * result
            question = f"{a} ÷ {b}"
            answer = str(result)
            hint = f"How many times does {b} go into {a}?"
            
        elif topic == 'percentages':
            val = random.randint(config['min_value'], config['max_value'] + (level*5))
            if random.choice([True, False]):
                question = f"{val}% as fraction"
                from fractions import Fraction
                f = Fraction(val, 100)
                answer = f"{f.numerator}/{f.denominator}"
                hint = "Simplify the fraction over 100"
            else:
                question = f"50% of {val*2}" # Placeholder
                answer = str(val)
                hint = "Half of the number"
                
        elif topic == 'squares':
            n = random.randint(config['min_value'], config['max_value'] + level)
            question = f"{n}²"
            answer = str(n**2)
            hint = f"{n} times {n}"
            
        elif topic == 'cubes':
            n = random.randint(config['min_value'], config['max_value'])
            question = f"{n}³"
            answer = str(n**3)
            hint = f"{n} * {n} * {n}"
            
        elif topic == 'cube_roots':
             n = random.randint(config['min_value'], config['max_value'])
             cube = n**3
             question = f"∛{cube}"
             answer = str(n)
             hint = "Number multiplied by itself 3 times"
             
        elif topic == 'fractions':
            den = random.randint(2, 10 + level)
            num = random.randint(1, den-1)
            question = f"Decimal of {num}/{den}"
            answer = f"{num/den:.2f}"
            hint = "Divide numerator by denominator"
        
        elif topic == 'mult_tables':
            t_min, t_max = config['min_table'], config['max_table']
            t = random.randint(t_min, t_max + (level // 2))
            m = random.randint(1, 12)
            question = f"{t} × {m}"
            answer = str(t * m)
            hint = "Multiplication table"

        if not question: # Fallback
            a, b = random.randint(1, 10), random.randint(1, 10)
            question = f"{a} + {b}"
            answer = str(a+b)
            hint = "Sum"

        return {
            'topic': topic,
            'question': question,
            'answer': answer,
            'hint': hint
        }

    def update_difficulty(self, topic, is_correct):
        if is_correct:
            self.difficulty_configs[topic]['level'] = min(self.difficulty_configs[topic].get('level', 1) + 1, 10)
        else:
            self.difficulty_configs[topic]['level'] = max(self.difficulty_configs[topic].get('level', 1) - 1, 1)


class MathPracticeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.engine = MathEngine()
        self.engine.load_config()
        
        self.title("Math Practice Pro 2025")
        self.geometry("1100x800")
        
        pygame.mixer.init()
        self.init_database()
        
        self.current_question = None
        self.start_timer_time = None
        self.session_questions = []
        self.current_question_index = 0
        self.session_correct = 0
        self.session_total = 0
        self.quiz_mode = "Standard"
        self.blitz_time_remaining = 60
        self.is_quiz_active = False
        
        self.create_widgets()
        self.load_achievements()
        self.update_history() # Load initial history
        
    def init_database(self):
        self.conn = sqlite3.connect('math_practice.db', check_same_thread=False)
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS quiz_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT, topic TEXT, question TEXT, correct_answer TEXT,
                user_answer TEXT, is_correct BOOLEAN, time_taken REAL, difficulty TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, description TEXT, unlocked BOOLEAN DEFAULT FALSE, unlock_date DATETIME)''')
        achievements = [("First Steps", "Complete first quiz"), ("Perfect Score", "100% score"), ("Blitz Master", "Score > 15 in Blitz")]
        for name, desc in achievements:
            cursor.execute('INSERT OR IGNORE INTO achievements (name, description) VALUES (?, ?)', (name, desc))
        self.conn.commit()
    
    def create_widgets(self):
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill='both', expand=True, padx=20, pady=20)
        self.tabview.add("Practice")
        self.tabview.add("History") # Changed order for visibility
        self.tabview.add("Progress")
        self.tabview.add("Settings")
        self.tabview.add("Achievements")
        
        self.create_practice_tab_ctk()
        self.create_history_tab_ctk()
        self.create_config_tab_ctk()
        self.create_progress_tab_ctk()
        self.create_achievements_tab_ctk()

        # Keyboard Bindings
        self.bind('<Return>', lambda e: self.on_enter_key())
        self.bind('<Right>', lambda e: self.next_button.invoke() if self.next_button and str(self.next_button._state) == 'normal' else None)
        self.bind('<Escape>', lambda e: self.end_button.invoke() if self.end_button and str(self.end_button._state) == 'normal' else None)
        self.bind('<Control-h>', lambda e: self.hint_button.invoke() if self.hint_button and str(self.hint_button._state) == 'normal' else None)

    def on_enter_key(self):
        if str(self.start_button._state) == 'normal':
            self.start_button.invoke()
        elif str(self.submit_button._state) == 'normal':
            self.submit_button.invoke()
        elif str(self.next_button._state) == 'normal':
            self.next_button.invoke()
        
    def create_practice_tab_ctk(self):
        main = self.tabview.tab("Practice")
        left = ctk.CTkFrame(main, corner_radius=10)
        left.pack(side='left', fill='y', padx=10, pady=10)
        
        ctk.CTkLabel(left, text="Game Mode", font=("Roboto", 16, "bold")).pack(pady=5)
        self.mode_var = ctk.StringVar(value="Standard")
        self.mode_switch = ctk.CTkSegmentedButton(left, values=["Standard", "Blitz Mode"], variable=self.mode_var, command=self.toggle_mode_ui)
        self.mode_switch.pack(pady=5)
        
        self.adaptive_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(left, text="Adaptive Difficulty", variable=self.adaptive_var).pack(pady=10)
        
        self.num_questions_var = ctk.StringVar(value="10")
        ctk.CTkComboBox(left, values=["5", "10", "20", "50"], variable=self.num_questions_var).pack(pady=5)
        
        scroll = ctk.CTkScrollableFrame(left, label_text="Topics")
        scroll.pack(fill='both', expand=True, padx=5, pady=5)
        self.topic_vars = {}
        for key in self.engine.difficulty_configs.keys():
             self.topic_vars[key] = ctk.BooleanVar(value=True)
             ctk.CTkCheckBox(scroll, text=key.title(), variable=self.topic_vars[key]).pack(anchor='w')

        right = ctk.CTkFrame(main)
        right.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        top = ctk.CTkFrame(right, fg_color="transparent")
        top.pack(fill='x', padx=20, pady=20)
        self.timer_label = ctk.CTkLabel(top, text="Time: 0s", font=("Roboto", 18))
        self.timer_label.pack(side='left')
        self.score_label = ctk.CTkLabel(top, text="Score: 0/0", font=("Roboto", 18))
        self.score_label.pack(side='right')
        
        self.question_label = ctk.CTkLabel(right, text="Ready?", font=("Roboto", 40, "bold"))
        self.question_label.pack(expand=True)
        self.feedback_label = ctk.CTkLabel(right, text="", font=("Roboto", 18))
        self.feedback_label.pack(pady=10)
        
        input_frame = ctk.CTkFrame(right, fg_color="transparent")
        input_frame.pack(pady=30)
        self.answer_var = ctk.StringVar()
        self.answer_entry = ctk.CTkEntry(input_frame, textvariable=self.answer_var, font=("Roboto", 24), width=200, justify='center')
        self.answer_entry.pack(side='left', padx=10)
        
        self.submit_button = ctk.CTkButton(input_frame, text="Submit", command=self.submit_answer)
        self.submit_button.pack(side='left', padx=10)
        
        controls = ctk.CTkFrame(right, fg_color="transparent")
        controls.pack(pady=20, side='bottom')
        self.start_button = ctk.CTkButton(controls, text="Start", command=self.start_quiz, fg_color="green")
        self.start_button.pack(side='left', padx=5)
        self.next_button = ctk.CTkButton(controls, text="Next", command=self.next_question, state='disabled')
        self.next_button.pack(side='left', padx=5)
        self.hint_button = ctk.CTkButton(controls, text="Hint (Ctrl+H)", command=self.show_hint, state='disabled', fg_color="orange")
        self.hint_button.pack(side='left', padx=5)
        self.end_button = ctk.CTkButton(controls, text="End (Esc)", command=self.end_quiz, state='disabled', fg_color="red")
        self.end_button.pack(side='left', padx=5)

    def create_history_tab_ctk(self):
        """Create History Tab to view database records"""
        frame = self.tabview.tab("History")
        
        # Simple style for treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", rowheight=25)
        style.map('Treeview', background=[('selected', '#1f538d')])
        
        columns = ('Time', 'Topic', 'Question', 'Result', 'User')
        self.history_tree = ttk.Treeview(frame, columns=columns, show='headings')
        
        self.history_tree.heading('Time', text='Time')
        self.history_tree.heading('Topic', text='Topic')
        self.history_tree.heading('Question', text='Question')
        self.history_tree.heading('Result', text='Result')
        self.history_tree.heading('User', text='Your Answer')
        
        self.history_tree.column('Time', width=150)
        self.history_tree.column('Topic', width=100)
        self.history_tree.column('Question', width=150)
        self.history_tree.column('Result', width=80)
        self.history_tree.column('User', width=100)
        
        scrollbar = ctk.CTkScrollbar(frame, command=self.history_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        self.history_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        ctk.CTkButton(frame, text="Refresh History", command=self.update_history).pack(pady=5)

    def update_history(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
            
        cursor = self.conn.cursor()
        cursor.execute('SELECT timestamp, topic, question, is_correct, user_answer FROM quiz_results ORDER BY timestamp DESC LIMIT 50')
        for row in cursor.fetchall():
            ts, topic, q, corr, ans = row
            res = "✅" if corr else "❌"
            self.history_tree.insert('', 'end', values=(ts, topic, q, res, ans))

    def toggle_mode_ui(self, mode):
        self.answer_entry.configure(placeholder_text="Blitz!" if mode != "Standard" else "")

    def create_config_tab_ctk(self):
        frame = self.tabview.tab("Settings")
        canvas = ctk.CTkScrollableFrame(frame)
        canvas.pack(fill='both', expand=True)
        self.config_widgets = {}
        for topic, config in self.engine.difficulty_configs.items():
            row = ctk.CTkFrame(canvas)
            row.pack(fill='x', padx=5, pady=5)
            ctk.CTkLabel(row, text=topic.title(), width=100).pack(side='left')
            self.config_widgets[topic] = {}
            for k in ['min_digits', 'max_digits', 'min_value', 'max_value']:
                if k in config:
                    ctk.CTkLabel(row, text=k).pack(side='left', padx=5)
                    v = ctk.StringVar(value=str(config[k]))
                    self.config_widgets[topic][k] = v
                    ctk.CTkEntry(row, textvariable=v, width=50).pack(side='left')
        ctk.CTkButton(frame, text="Save", command=self.save_UI_config).pack(pady=10)
        
    def save_UI_config(self):
        for t, widgets in self.config_widgets.items():
            for k, v in widgets.items():
                try:
                    self.engine.difficulty_configs[t][k] = int(v.get())
                except: pass
        self.engine.save_config()
        messagebox.showinfo("Saved", "Config saved")

    def create_progress_tab_ctk(self):
        frame = self.tabview.tab("Progress")
        self.stats_text = ctk.CTkTextbox(frame, height=80)
        self.stats_text.pack(fill='x', padx=10)
        self.graph_frame = ctk.CTkFrame(frame)
        self.graph_frame.pack(fill='both', expand=True, padx=10, pady=10)
        ctk.CTkButton(frame, text="Refresh", command=self.update_progress).pack(pady=5)

    def create_achievements_tab_ctk(self):
        frame = self.tabview.tab("Achievements")
        self.ach_list = ctk.CTkTextbox(frame)
        self.ach_list.pack(fill='both', expand=True)

    def start_quiz(self):
        selected = [t for t, v in self.topic_vars.items() if v.get()]
        if not selected: return
        self.quiz_mode = self.mode_var.get()
        self.is_quiz_active = True
        self.session_questions = []
        self.current_question_index = 0
        self.session_correct = 0
        self.start_timer_time = time.time()
        
        if self.quiz_mode == "Standard":
            num = int(self.num_questions_var.get())
            self.session_total = num
            for _ in range(num):
                self.session_questions.append(self.engine.generate_question(random.choice(selected), self.adaptive_var.get()))
        else:
            self.session_total = 0
            self.blitz_time_remaining = 60
            
        self.start_button.configure(state='disabled')
        self.submit_button.configure(state='normal')
        self.next_button.configure(state='disabled')
        self.end_button.configure(state='normal')
        self.hint_button.configure(state='normal')
        
        self.load_next_question()
        self.start_timer()
        self.answer_entry.focus()
        
    def load_next_question(self):
        selected = [t for t, v in self.topic_vars.items() if v.get()]
        if self.quiz_mode == "Standard":
            if self.current_question_index >= len(self.session_questions):
                self.end_quiz()
                return
            self.current_question = self.session_questions[self.current_question_index]
        else:
            self.current_question = self.engine.generate_question(random.choice(selected), self.adaptive_var.get())
            
        self.question_label.configure(text=self.current_question['question'])
        self.answer_var.set("")
        self.feedback_label.configure(text="")
        if self.quiz_mode=="Standard":
            self.score_label.configure(text=f"Score: {self.session_correct}/{self.current_question_index} | {self.current_question_index+1}/{self.session_total}")
        else:
            self.score_label.configure(text=f"Score: {self.session_correct}")

    def flash_feedback(self, correct):
        try:
            # Simple color flash
            orig = self.answer_entry.cget('fg_color')
            flash = "#2ecc71" if correct else "#e74c3c"
            self.answer_entry.configure(fg_color=flash)
            self.after(300, lambda: self.answer_entry.configure(fg_color=orig))
        except: pass

    def submit_answer(self):
        if not self.is_quiz_active or not self.current_question: return
        user_ans = self.answer_var.get().strip()
        corr_ans = self.current_question['answer']
        
        try: is_correct = float(user_ans) == float(corr_ans)
        except: is_correct = user_ans.lower() == corr_ans.lower()
        
        self.flash_feedback(is_correct)
        
        if self.adaptive_var.get():
            self.engine.update_difficulty(self.current_question['topic'], is_correct)
            
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO quiz_results (topic, question, correct_answer, user_answer, is_correct, time_taken, difficulty) VALUES (?,?,?,?,?,?,?)',
                      (self.current_question['topic'], self.current_question['question'], corr_ans, user_ans, is_correct, 0, 'adaptive' if self.adaptive_var.get() else 'normal'))
        self.conn.commit()
        self.update_history() # Update history in real-time
        
        if is_correct:
            self.session_correct += 1
            self.feedback_label.configure(text="Correct!", text_color="green")
            self.play_sound('correct')
            # AUTO ADVANCE LOGIC
            self.after(1000, self.auto_advance)
            self.submit_button.configure(state='disabled') # Prevent double submit during wait
        else:
            self.feedback_label.configure(text=f"Wrong. {corr_ans}", text_color="red")
            self.play_sound('wrong')
            self.current_question_index += 1
            if self.quiz_mode == "Standard":
                self.submit_button.configure(state='disabled')
                self.next_button.configure(state='normal')
                self.next_button.focus()
            else:
                self.load_next_question()
                self.answer_entry.focus()
    
    def auto_advance(self):
        # Move forward automatically called by after() if correct
        if not self.is_quiz_active: return
        self.current_question_index += 1
        
        if self.quiz_mode == "Standard":
            self.submit_button.configure(state='normal') # Re-enable for next q
            self.load_next_question()
            self.answer_entry.focus()
        else:
            self.submit_button.configure(state='normal')
            self.load_next_question()
            self.answer_entry.focus()

    def next_question(self):
        self.submit_button.configure(state='normal')
        self.next_button.configure(state='disabled')
        self.load_next_question()
        self.answer_entry.focus()
        
    def end_quiz(self):
        self.is_quiz_active = False
        messagebox.showinfo("Done", f"Score: {self.session_correct}")
        self.start_button.configure(state='normal')
        self.submit_button.configure(state='disabled')
        self.update_progress()
        self.load_achievements()

    def start_timer(self):
        def _t():
            while self.is_quiz_active:
                if self.quiz_mode == "Standard":
                    self.timer_label.configure(text=f"Time: {int(time.time()-self.start_timer_time)}s")
                else:
                    self.blitz_time_remaining -= 1
                    self.timer_label.configure(text=f"Time: {self.blitz_time_remaining}s")
                    if self.blitz_time_remaining <= 0:
                        self.after(0, self.end_quiz)
                        break
                time.sleep(1)
        threading.Thread(target=_t, daemon=True).start()

    def play_sound(self, t):
        try:
            import numpy as np
            freq = 800 if t=='correct' else 300
            arr = (np.sin(2*np.pi*np.arange(4410)*freq/44100)*32767).astype(np.int16)
            pygame.sndarray.make_sound(arr).play()
        except: pass

    def show_hint(self):
        if self.current_question: messagebox.showinfo("Hint", self.current_question['hint'])

    def update_progress(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT topic, AVG(is_correct) FROM quiz_results GROUP BY topic")
        data = cursor.fetchall()
        for w in self.graph_frame.winfo_children(): w.destroy()
        if data:
            fig = Figure(figsize=(5,3), dpi=100)
            ax = fig.add_subplot(111)
            # Dynamic coloring for graph
            bg = '#2b2b2b' if ctk.get_appearance_mode()=="Dark" else "#ffffff"
            fg = '#ffffff' if ctk.get_appearance_mode()=="Dark" else "#000000"
            fig.patch.set_facecolor(bg)
            ax.set_facecolor(bg)
            ax.tick_params(axis='x', colors=fg)
            ax.tick_params(axis='y', colors=fg)
            ax.spines['bottom'].set_color(fg)
            ax.spines['left'].set_color(fg)
            ax.bar([x[0] for x in data], [x[1]*100 for x in data])
            FigureCanvasTkAgg(fig, self.graph_frame).get_tk_widget().pack(fill='both', expand=True)

    def load_achievements(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, unlocked FROM achievements")
        txt = "\n".join([f"{'🏆' if u else '🔒'} {n}" for n, u in cursor.fetchall()])
        self.ach_list.delete("0.0", "end")
        self.ach_list.insert("0.0", txt)

if __name__ == "__main__":
    app = MathPracticeApp()
    app.mainloop()
