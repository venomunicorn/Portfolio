"""
Modern Calculator GUI Application
Built with Tkinter - Part of 21APEX Challenge
"""

import tkinter as tk
from tkinter import ttk
import math

class CalculatorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Modern Calculator")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.root.configure(bg='#1a1a2e')
        
        # Colors
        self.colors = {
            'bg': '#1a1a2e',
            'display': '#16213e',
            'button': '#0f3460',
            'button_hover': '#1a4a7a',
            'operator': '#e94560',
            'operator_hover': '#ff6b6b',
            'equals': '#00b894',
            'equals_hover': '#00d9a5',
            'text': '#ffffff',
            'text_dim': '#a0a0a0'
        }
        
        # Calculator state
        self.current_input = "0"
        self.first_operand = None
        self.operator = None
        self.new_input = True
        self.history = []
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Display frame
        display_frame = tk.Frame(main_frame, bg=self.colors['display'], height=120)
        display_frame.pack(fill='x', pady=(0, 15))
        display_frame.pack_propagate(False)
        
        # History label (small)
        self.history_label = tk.Label(
            display_frame,
            text="",
            font=('Segoe UI', 12),
            fg=self.colors['text_dim'],
            bg=self.colors['display'],
            anchor='e'
        )
        self.history_label.pack(fill='x', padx=15, pady=(10, 0))
        
        # Main display
        self.display = tk.Label(
            display_frame,
            text="0",
            font=('Segoe UI', 42, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['display'],
            anchor='e'
        )
        self.display.pack(fill='x', padx=15, pady=(5, 15))
        
        # Button grid
        buttons_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        buttons_frame.pack(fill='both', expand=True)
        
        # Button layout
        buttons = [
            ['C', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['√', '0', '.', '=']
        ]
        
        # Configure grid
        for i in range(5):
            buttons_frame.rowconfigure(i, weight=1)
        for j in range(4):
            buttons_frame.columnconfigure(j, weight=1)
        
        # Create buttons
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                self.create_button(buttons_frame, text, i, j)
        
        # Scientific functions frame
        sci_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        sci_frame.pack(fill='x', pady=(10, 0))
        
        sci_buttons = ['sin', 'cos', 'tan', 'log', 'x²', 'xʸ']
        for i, text in enumerate(sci_buttons):
            btn = tk.Button(
                sci_frame,
                text=text,
                font=('Segoe UI', 10, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['button'],
                activebackground=self.colors['button_hover'],
                activeforeground=self.colors['text'],
                relief='flat',
                bd=0,
                command=lambda t=text: self.scientific_operation(t)
            )
            btn.pack(side='left', expand=True, fill='both', padx=2, pady=2, ipady=8)
            btn.bind('<Enter>', lambda e, b=btn: b.configure(bg=self.colors['button_hover']))
            btn.bind('<Leave>', lambda e, b=btn: b.configure(bg=self.colors['button']))
    
    def create_button(self, parent, text, row, col):
        # Determine button color
        if text in ['÷', '×', '-', '+']:
            bg = self.colors['operator']
            hover_bg = self.colors['operator_hover']
        elif text == '=':
            bg = self.colors['equals']
            hover_bg = self.colors['equals_hover']
        elif text in ['C', '±', '%', '√']:
            bg = '#2d3436'
            hover_bg = '#636e72'
        else:
            bg = self.colors['button']
            hover_bg = self.colors['button_hover']
        
        btn = tk.Button(
            parent,
            text=text,
            font=('Segoe UI', 20, 'bold'),
            fg=self.colors['text'],
            bg=bg,
            activebackground=hover_bg,
            activeforeground=self.colors['text'],
            relief='flat',
            bd=0,
            command=lambda: self.button_click(text)
        )
        btn.grid(row=row, column=col, padx=3, pady=3, sticky='nsew')
        
        # Hover effects
        btn.bind('<Enter>', lambda e, b=btn, c=hover_bg: b.configure(bg=c))
        btn.bind('<Leave>', lambda e, b=btn, c=bg: b.configure(bg=c))
    
    def button_click(self, text):
        if text.isdigit():
            self.digit_input(text)
        elif text == '.':
            self.decimal_input()
        elif text in ['÷', '×', '-', '+']:
            self.operator_input(text)
        elif text == '=':
            self.calculate()
        elif text == 'C':
            self.clear()
        elif text == '±':
            self.negate()
        elif text == '%':
            self.percentage()
        elif text == '√':
            self.square_root()
    
    def digit_input(self, digit):
        if self.new_input:
            self.current_input = digit
            self.new_input = False
        else:
            if len(self.current_input) < 12:  # Limit display length
                self.current_input += digit
        self.update_display()
    
    def decimal_input(self):
        if self.new_input:
            self.current_input = "0."
            self.new_input = False
        elif '.' not in self.current_input:
            self.current_input += '.'
        self.update_display()
    
    def operator_input(self, op):
        if self.first_operand is not None and not self.new_input:
            self.calculate()
        self.first_operand = float(self.current_input)
        self.operator = op
        self.new_input = True
        self.history_label.config(text=f"{self.format_number(self.first_operand)} {op}")
    
    def calculate(self):
        if self.first_operand is None or self.operator is None:
            return
        
        second = float(self.current_input)
        result = 0
        
        try:
            if self.operator == '+':
                result = self.first_operand + second
            elif self.operator == '-':
                result = self.first_operand - second
            elif self.operator == '×':
                result = self.first_operand * second
            elif self.operator == '÷':
                if second == 0:
                    self.display.config(text="Error")
                    self.history_label.config(text="Cannot divide by zero")
                    self.clear_state()
                    return
                result = self.first_operand / second
            elif self.operator == '^':
                result = math.pow(self.first_operand, second)
            
            # Format result
            if result == int(result):
                result = int(result)
            
            # Add to history
            history_text = f"{self.format_number(self.first_operand)} {self.operator} {self.format_number(second)} ="
            self.history_label.config(text=history_text)
            
            self.current_input = str(result)
            self.update_display()
            self.clear_state()
            
        except Exception as e:
            self.display.config(text="Error")
            self.clear_state()
    
    def clear_state(self):
        self.first_operand = None
        self.operator = None
        self.new_input = True
    
    def clear(self):
        self.current_input = "0"
        self.first_operand = None
        self.operator = None
        self.new_input = True
        self.history_label.config(text="")
        self.update_display()
    
    def negate(self):
        if self.current_input != "0":
            if self.current_input.startswith('-'):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.update_display()
    
    def percentage(self):
        try:
            value = float(self.current_input) / 100
            self.current_input = str(value)
            self.update_display()
        except:
            pass
    
    def square_root(self):
        try:
            value = float(self.current_input)
            if value < 0:
                self.display.config(text="Error")
                self.history_label.config(text="Invalid input")
                return
            result = math.sqrt(value)
            self.history_label.config(text=f"√{self.format_number(value)} =")
            if result == int(result):
                result = int(result)
            self.current_input = str(result)
            self.new_input = True
            self.update_display()
        except:
            self.display.config(text="Error")
    
    def scientific_operation(self, op):
        try:
            value = float(self.current_input)
            result = 0
            
            if op == 'sin':
                result = math.sin(math.radians(value))
                self.history_label.config(text=f"sin({value}°) =")
            elif op == 'cos':
                result = math.cos(math.radians(value))
                self.history_label.config(text=f"cos({value}°) =")
            elif op == 'tan':
                result = math.tan(math.radians(value))
                self.history_label.config(text=f"tan({value}°) =")
            elif op == 'log':
                if value <= 0:
                    self.display.config(text="Error")
                    return
                result = math.log10(value)
                self.history_label.config(text=f"log({value}) =")
            elif op == 'x²':
                result = value ** 2
                self.history_label.config(text=f"{value}² =")
            elif op == 'xʸ':
                self.first_operand = value
                self.operator = '^'
                self.new_input = True
                self.history_label.config(text=f"{self.format_number(value)} ^")
                return
            
            # Round small values to avoid floating point display issues
            if abs(result) < 1e-10:
                result = 0
            elif result == int(result):
                result = int(result)
            else:
                result = round(result, 10)
            
            self.current_input = str(result)
            self.new_input = True
            self.update_display()
            
        except Exception as e:
            self.display.config(text="Error")
    
    def format_number(self, num):
        """Format numbers for display"""
        if isinstance(num, float) and num == int(num):
            return str(int(num))
        return str(num)
    
    def update_display(self):
        # Truncate if too long
        display_text = self.current_input
        if len(display_text) > 12:
            try:
                num = float(display_text)
                display_text = f"{num:.6e}"
            except:
                display_text = display_text[:12]
        self.display.config(text=display_text)
    
    def run(self):
        # Center window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.root.mainloop()

if __name__ == "__main__":
    app = CalculatorGUI()
    app.run()
