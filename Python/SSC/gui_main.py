"""
SSC Math Preparation Tool GUI
Built with Tkinter - Part of 21APEX Challenge
Generates multiplication tables, squares, cubes, and roots
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math

class SSCPrepGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SSC Math Preparation Tool")
        self.root.geometry("800x650")
        self.root.resizable(True, True)
        self.root.configure(bg='#f5f5f5')
        
        # Colors - Academic theme
        self.colors = {
            'bg': '#f5f5f5',
            'card': '#ffffff',
            'primary': '#3498db',
            'secondary': '#2ecc71',
            'accent': '#9b59b6',
            'text': '#2c3e50',
            'text_dim': '#7f8c8d'
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(
            main_frame,
            text="📚 SSC Math Preparation",
            font=('Segoe UI', 24, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['bg']
        ).pack(pady=(0, 5))
        
        tk.Label(
            main_frame,
            text="Tables, Squares, Cubes & Roots",
            font=('Segoe UI', 11),
            fg=self.colors['text_dim'],
            bg=self.colors['bg']
        ).pack(pady=(0, 15))
        
        # Tabs
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook.Tab', padding=[20, 10], font=('Segoe UI', 10, 'bold'))
        
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)
        
        # Tab 1: Multiplication Tables
        self.create_tables_tab(notebook)
        
        # Tab 2: Squares & Cubes
        self.create_squares_tab(notebook)
        
        # Tab 3: Quick Reference
        self.create_reference_tab(notebook)
        
    def create_tables_tab(self, notebook):
        tab = tk.Frame(notebook, bg=self.colors['card'])
        notebook.add(tab, text="📊 Multiplication Tables")
        
        # Controls
        control_frame = tk.Frame(tab, bg=self.colors['card'])
        control_frame.pack(fill='x', padx=20, pady=15)
        
        tk.Label(
            control_frame,
            text="Generate table for number:",
            font=('Segoe UI', 11),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(side='left')
        
        self.table_num_var = tk.StringVar(value="5")
        num_entry = tk.Entry(
            control_frame,
            textvariable=self.table_num_var,
            font=('Segoe UI', 12),
            width=8,
            relief='flat',
            bg='#ecf0f1'
        )
        num_entry.pack(side='left', padx=10, ipady=5)
        
        tk.Label(
            control_frame,
            text="up to:",
            font=('Segoe UI', 11),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(side='left')
        
        self.table_range_var = tk.StringVar(value="20")
        range_entry = tk.Entry(
            control_frame,
            textvariable=self.table_range_var,
            font=('Segoe UI', 12),
            width=8,
            relief='flat',
            bg='#ecf0f1'
        )
        range_entry.pack(side='left', padx=10, ipady=5)
        
        tk.Button(
            control_frame,
            text="Generate",
            font=('Segoe UI', 10, 'bold'),
            fg='white',
            bg=self.colors['primary'],
            relief='flat',
            padx=15,
            pady=5,
            command=self.generate_table
        ).pack(side='left', padx=10)
        
        # Table display
        display_frame = tk.Frame(tab, bg=self.colors['card'])
        display_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Create text widget with scrollbar
        scroll = ttk.Scrollbar(display_frame)
        scroll.pack(side='right', fill='y')
        
        self.table_text = tk.Text(
            display_frame,
            font=('Consolas', 14),
            bg='#fafafa',
            fg=self.colors['text'],
            relief='flat',
            wrap='none',
            yscrollcommand=scroll.set
        )
        self.table_text.pack(fill='both', expand=True)
        scroll.config(command=self.table_text.yview)
        
        # Generate initial table
        self.generate_table()
        
    def create_squares_tab(self, notebook):
        tab = tk.Frame(notebook, bg=self.colors['card'])
        notebook.add(tab, text="🔢 Squares & Cubes")
        
        # Controls
        control_frame = tk.Frame(tab, bg=self.colors['card'])
        control_frame.pack(fill='x', padx=20, pady=15)
        
        tk.Label(
            control_frame,
            text="Generate from 1 to:",
            font=('Segoe UI', 11),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(side='left')
        
        self.sq_range_var = tk.StringVar(value="50")
        range_entry = tk.Entry(
            control_frame,
            textvariable=self.sq_range_var,
            font=('Segoe UI', 12),
            width=8,
            relief='flat',
            bg='#ecf0f1'
        )
        range_entry.pack(side='left', padx=10, ipady=5)
        
        tk.Button(
            control_frame,
            text="Generate Squares",
            font=('Segoe UI', 10, 'bold'),
            fg='white',
            bg=self.colors['secondary'],
            relief='flat',
            padx=15,
            pady=5,
            command=lambda: self.generate_powers('squares')
        ).pack(side='left', padx=5)
        
        tk.Button(
            control_frame,
            text="Generate Cubes",
            font=('Segoe UI', 10, 'bold'),
            fg='white',
            bg=self.colors['accent'],
            relief='flat',
            padx=15,
            pady=5,
            command=lambda: self.generate_powers('cubes')
        ).pack(side='left', padx=5)
        
        tk.Button(
            control_frame,
            text="📄 Export All",
            font=('Segoe UI', 10, 'bold'),
            fg='white',
            bg='#e74c3c',
            relief='flat',
            padx=15,
            pady=5,
            command=self.export_all
        ).pack(side='right', padx=5)
        
        # Display
        display_frame = tk.Frame(tab, bg=self.colors['card'])
        display_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        scroll = ttk.Scrollbar(display_frame)
        scroll.pack(side='right', fill='y')
        
        self.powers_text = tk.Text(
            display_frame,
            font=('Consolas', 12),
            bg='#fafafa',
            fg=self.colors['text'],
            relief='flat',
            yscrollcommand=scroll.set
        )
        self.powers_text.pack(fill='both', expand=True)
        scroll.config(command=self.powers_text.yview)
        
        self.generate_powers('squares')
        
    def create_reference_tab(self, notebook):
        tab = tk.Frame(notebook, bg=self.colors['card'])
        notebook.add(tab, text="⚡ Quick Reference")
        
        # Common values
        tk.Label(
            tab,
            text="Quick Reference - Common Values",
            font=('Segoe UI', 14, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(pady=(20, 10))
        
        ref_frame = tk.Frame(tab, bg=self.colors['card'])
        ref_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create columns
        col1 = tk.Frame(ref_frame, bg=self.colors['card'])
        col1.pack(side='left', fill='both', expand=True, padx=10)
        
        col2 = tk.Frame(ref_frame, bg=self.colors['card'])
        col2.pack(side='left', fill='both', expand=True, padx=10)
        
        col3 = tk.Frame(ref_frame, bg=self.colors['card'])
        col3.pack(side='left', fill='both', expand=True, padx=10)
        
        # Perfect squares (1-25)
        tk.Label(col1, text="Perfect Squares", font=('Segoe UI', 12, 'bold'),
                fg=self.colors['primary'], bg=self.colors['card']).pack(anchor='w')
        
        sq_text = tk.Text(col1, font=('Consolas', 10), height=18, width=15,
                         bg='#ecf0f1', relief='flat')
        sq_text.pack(fill='x', pady=5)
        for i in range(1, 26):
            sq_text.insert(tk.END, f"{i}² = {i**2}\n")
        sq_text.config(state='disabled')
        
        # Perfect cubes (1-15)
        tk.Label(col2, text="Perfect Cubes", font=('Segoe UI', 12, 'bold'),
                fg=self.colors['secondary'], bg=self.colors['card']).pack(anchor='w')
        
        cb_text = tk.Text(col2, font=('Consolas', 10), height=18, width=18,
                         bg='#ecf0f1', relief='flat')
        cb_text.pack(fill='x', pady=5)
        for i in range(1, 16):
            cb_text.insert(tk.END, f"{i}³ = {i**3}\n")
        cb_text.config(state='disabled')
        
        # Square roots
        tk.Label(col3, text="Square Roots", font=('Segoe UI', 12, 'bold'),
                fg=self.colors['accent'], bg=self.colors['card']).pack(anchor='w')
        
        rt_text = tk.Text(col3, font=('Consolas', 10), height=18, width=18,
                         bg='#ecf0f1', relief='flat')
        rt_text.pack(fill='x', pady=5)
        perfect_squares = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225]
        for sq in perfect_squares:
            rt_text.insert(tk.END, f"√{sq} = {int(math.sqrt(sq))}\n")
        rt_text.config(state='disabled')
        
    def generate_table(self):
        try:
            num = int(self.table_num_var.get())
            max_range = int(self.table_range_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")
            return
        
        self.table_text.delete('1.0', tk.END)
        self.table_text.insert(tk.END, f"╔══════════════════════════════╗\n")
        self.table_text.insert(tk.END, f"║   MULTIPLICATION TABLE OF {num:3d}  ║\n")
        self.table_text.insert(tk.END, f"╠══════════════════════════════╣\n")
        
        for i in range(1, max_range + 1):
            result = num * i
            self.table_text.insert(tk.END, f"║   {num:3d} × {i:3d} = {result:6d}        ║\n")
        
        self.table_text.insert(tk.END, f"╚══════════════════════════════╝\n")
        
    def generate_powers(self, power_type):
        try:
            max_range = int(self.sq_range_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
            return
        
        self.powers_text.delete('1.0', tk.END)
        
        if power_type == 'squares':
            self.powers_text.insert(tk.END, "═" * 50 + "\n")
            self.powers_text.insert(tk.END, f"  SQUARES (1 to {max_range})\n")
            self.powers_text.insert(tk.END, "═" * 50 + "\n\n")
            
            self.powers_text.insert(tk.END, f"{'Number':<10} {'Square':<15} {'Square Root':<15}\n")
            self.powers_text.insert(tk.END, "-" * 40 + "\n")
            
            for i in range(1, max_range + 1):
                sq = i ** 2
                sqrt = math.sqrt(sq)
                self.powers_text.insert(tk.END, f"{i:<10} {sq:<15} {sqrt:<15.0f}\n")
        
        else:  # cubes
            self.powers_text.insert(tk.END, "═" * 50 + "\n")
            self.powers_text.insert(tk.END, f"  CUBES (1 to {max_range})\n")
            self.powers_text.insert(tk.END, "═" * 50 + "\n\n")
            
            self.powers_text.insert(tk.END, f"{'Number':<10} {'Cube':<18} {'Cube Root':<15}\n")
            self.powers_text.insert(tk.END, "-" * 43 + "\n")
            
            for i in range(1, max_range + 1):
                cube = i ** 3
                cbrt = round(cube ** (1/3), 6)
                self.powers_text.insert(tk.END, f"{i:<10} {cube:<18} {cbrt:<15}\n")
    
    def export_all(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")],
            initialfile="ssc_math_reference.txt"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("SSC MATH PREPARATION - REFERENCE SHEET\n")
                    f.write("=" * 60 + "\n\n")
                    
                    # Squares
                    f.write("SQUARES (1-100)\n")
                    f.write("-" * 40 + "\n")
                    for i in range(1, 101):
                        f.write(f"{i}² = {i**2}\n")
                    
                    f.write("\n\nCUBES (1-50)\n")
                    f.write("-" * 40 + "\n")
                    for i in range(1, 51):
                        f.write(f"{i}³ = {i**3}\n")
                    
                    f.write("\n\nMULTIPLICATION TABLES (1-20)\n")
                    f.write("-" * 40 + "\n")
                    for num in range(1, 21):
                        f.write(f"\nTable of {num}:\n")
                        for i in range(1, 13):
                            f.write(f"{num} × {i} = {num*i}\n")
                
                messagebox.showinfo("Success", f"Data exported to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {e}")
    
    def run(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.root.mainloop()

if __name__ == "__main__":
    app = SSCPrepGUI()
    app.run()
