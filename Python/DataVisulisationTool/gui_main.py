"""
Data Visualization Tool GUI
Built with Tkinter - Part of 21APEX Challenge
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import os

# Try to import matplotlib for actual plots
try:
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


class DataVisualizationGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Data Visualization Tool")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        self.root.configure(bg='#f8f9fa')
        
        # Colors
        self.colors = {
            'bg': '#f8f9fa',
            'card': '#ffffff',
            'primary': '#4361ee',
            'secondary': '#3f37c9',
            'success': '#4cc9f0',
            'text': '#212529',
            'text_dim': '#6c757d',
            'chart_colors': ['#4361ee', '#7209b7', '#f72585', '#4cc9f0', '#06d6a0']
        }
        
        # Data storage
        self.data = None
        self.headers = None
        self.filename = None
        
        self.setup_ui()
        self.create_sample_data()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(
            main_frame,
            text="📊 Data Visualization Tool",
            font=('Segoe UI', 24, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['bg']
        ).pack(pady=(0, 5))
        
        # Status
        status_text = "Ready" if HAS_MATPLOTLIB else "⚠️ Basic Mode (pip install matplotlib)"
        status_color = self.colors['success'] if HAS_MATPLOTLIB else '#f0ad4e'
        
        tk.Label(
            main_frame,
            text=status_text,
            font=('Segoe UI', 10),
            fg=status_color,
            bg=self.colors['bg']
        ).pack(pady=(0, 15))
        
        # File controls
        file_frame = tk.Frame(main_frame, bg=self.colors['card'])
        file_frame.pack(fill='x', pady=10, ipady=15)
        
        tk.Label(
            file_frame,
            text="📁 Data Source",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(pady=(10, 5))
        
        btn_frame = tk.Frame(file_frame, bg=self.colors['card'])
        btn_frame.pack()
        
        tk.Button(
            btn_frame,
            text="📂 Load CSV",
            font=('Segoe UI', 10, 'bold'),
            fg='white',
            bg=self.colors['primary'],
            relief='flat',
            padx=20,
            pady=8,
            command=self.load_csv
        ).pack(side='left', padx=5)
        
        tk.Button(
            btn_frame,
            text="🔄 Use Sample Data",
            font=('Segoe UI', 10, 'bold'),
            fg='white',
            bg=self.colors['secondary'],
            relief='flat',
            padx=20,
            pady=8,
            command=self.use_sample_data
        ).pack(side='left', padx=5)
        
        self.file_label = tk.Label(
            file_frame,
            text="No file loaded",
            font=('Segoe UI', 10),
            fg=self.colors['text_dim'],
            bg=self.colors['card']
        )
        self.file_label.pack(pady=(10, 5))
        
        # Column selection
        columns_frame = tk.Frame(main_frame, bg=self.colors['card'])
        columns_frame.pack(fill='x', pady=10, ipady=15)
        
        tk.Label(
            columns_frame,
            text="📈 Chart Settings",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(pady=(10, 10))
        
        selection_frame = tk.Frame(columns_frame, bg=self.colors['card'])
        selection_frame.pack()
        
        # X-axis column
        tk.Label(selection_frame, text="X-Axis:", font=('Segoe UI', 10),
                fg=self.colors['text'], bg=self.colors['card']).pack(side='left', padx=5)
        
        self.x_column_var = tk.StringVar()
        self.x_dropdown = ttk.Combobox(
            selection_frame,
            textvariable=self.x_column_var,
            state='readonly',
            width=15
        )
        self.x_dropdown.pack(side='left', padx=5)
        
        # Y-axis column
        tk.Label(selection_frame, text="Y-Axis:", font=('Segoe UI', 10),
                fg=self.colors['text'], bg=self.colors['card']).pack(side='left', padx=(20, 5))
        
        self.y_column_var = tk.StringVar()
        self.y_dropdown = ttk.Combobox(
            selection_frame,
            textvariable=self.y_column_var,
            state='readonly',
            width=15
        )
        self.y_dropdown.pack(side='left', padx=5)
        
        # Chart type
        tk.Label(selection_frame, text="Type:", font=('Segoe UI', 10),
                fg=self.colors['text'], bg=self.colors['card']).pack(side='left', padx=(20, 5))
        
        self.chart_type_var = tk.StringVar(value='Bar Chart')
        chart_dropdown = ttk.Combobox(
            selection_frame,
            textvariable=self.chart_type_var,
            values=['Bar Chart', 'Line Chart', 'Pie Chart'],
            state='readonly',
            width=12
        )
        chart_dropdown.pack(side='left', padx=5)
        
        # Generate button
        tk.Button(
            columns_frame,
            text="✨ Generate Chart",
            font=('Segoe UI', 12, 'bold'),
            fg='white',
            bg=self.colors['success'],
            relief='flat',
            padx=30,
            pady=10,
            command=self.generate_chart
        ).pack(pady=15)
        
        # Chart display area
        self.chart_frame = tk.Frame(main_frame, bg=self.colors['card'])
        self.chart_frame.pack(fill='both', expand=True, pady=10)
        
        tk.Label(
            self.chart_frame,
            text="📊 Chart Display",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(pady=(10, 5))
        
        # Chart canvas container
        self.chart_container = tk.Frame(self.chart_frame, bg=self.colors['card'])
        self.chart_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Placeholder
        self.placeholder_label = tk.Label(
            self.chart_container,
            text="Load data and click 'Generate Chart'\nto visualize your data here",
            font=('Segoe UI', 14),
            fg=self.colors['text_dim'],
            bg=self.colors['card']
        )
        self.placeholder_label.pack(expand=True)
    
    def create_sample_data(self):
        """Create sample CSV data"""
        self.sample_data = {
            'headers': ['Month', 'Sales', 'Expenses', 'Profit'],
            'data': [
                ['Jan', 12000, 8000, 4000],
                ['Feb', 15000, 9000, 6000],
                ['Mar', 18000, 10000, 8000],
                ['Apr', 14000, 8500, 5500],
                ['May', 19000, 11000, 8000],
                ['Jun', 22000, 12000, 10000]
            ]
        }
    
    def load_csv(self):
        """Load data from CSV file"""
        filepath = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not filepath:
            return
        
        try:
            with open(filepath, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                self.headers = next(reader)
                self.data = [row for row in reader]
            
            self.filename = os.path.basename(filepath)
            self.file_label.config(text=f"Loaded: {self.filename} ({len(self.data)} rows)")
            
            # Update dropdowns
            self.x_dropdown['values'] = self.headers
            self.y_dropdown['values'] = self.headers
            
            if len(self.headers) >= 2:
                self.x_column_var.set(self.headers[0])
                self.y_column_var.set(self.headers[1])
            
            messagebox.showinfo("Success", f"Loaded {len(self.data)} rows from {self.filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def use_sample_data(self):
        """Use built-in sample data"""
        self.headers = self.sample_data['headers']
        self.data = self.sample_data['data']
        self.filename = "sample_data.csv"
        
        self.file_label.config(text=f"Using: Sample Data ({len(self.data)} rows)")
        
        # Update dropdowns
        self.x_dropdown['values'] = self.headers
        self.y_dropdown['values'] = self.headers
        
        self.x_column_var.set(self.headers[0])
        self.y_column_var.set(self.headers[1])
    
    def generate_chart(self):
        """Generate the chart based on selected options"""
        if not self.data or not self.headers:
            messagebox.showwarning("Warning", "Please load data first!")
            return
        
        x_col = self.x_column_var.get()
        y_col = self.y_column_var.get()
        
        if not x_col or not y_col:
            messagebox.showwarning("Warning", "Please select X and Y columns!")
            return
        
        x_idx = self.headers.index(x_col)
        y_idx = self.headers.index(y_col)
        
        x_values = [row[x_idx] for row in self.data]
        y_values = []
        
        for row in self.data:
            try:
                y_values.append(float(row[y_idx]))
            except ValueError:
                y_values.append(0)
        
        # Clear previous chart
        for widget in self.chart_container.winfo_children():
            widget.destroy()
        
        if HAS_MATPLOTLIB:
            self.create_matplotlib_chart(x_values, y_values, x_col, y_col)
        else:
            self.create_text_chart(x_values, y_values, x_col, y_col)
    
    def create_matplotlib_chart(self, x_values, y_values, x_label, y_label):
        """Create chart using matplotlib"""
        fig = Figure(figsize=(7, 4), dpi=100, facecolor=self.colors['card'])
        ax = fig.add_subplot(111)
        ax.set_facecolor(self.colors['card'])
        
        chart_type = self.chart_type_var.get()
        
        if chart_type == 'Bar Chart':
            bars = ax.bar(x_values, y_values, color=self.colors['chart_colors'])
        elif chart_type == 'Line Chart':
            ax.plot(x_values, y_values, marker='o', linewidth=2, 
                   color=self.colors['primary'], markersize=8)
            ax.fill_between(range(len(x_values)), y_values, alpha=0.3, color=self.colors['primary'])
        elif chart_type == 'Pie Chart':
            ax.pie(y_values, labels=x_values, autopct='%1.1f%%', 
                  colors=self.colors['chart_colors'])
        
        if chart_type != 'Pie Chart':
            ax.set_xlabel(x_label, fontsize=11)
            ax.set_ylabel(y_label, fontsize=11)
        
        ax.set_title(f"{y_label} by {x_label}", fontsize=14, fontweight='bold')
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def create_text_chart(self, x_values, y_values, x_label, y_label):
        """Create text-based chart when matplotlib is not available"""
        # Find max value for scaling
        max_val = max(y_values) if y_values else 1
        bar_width = 30
        
        chart_text = tk.Text(
            self.chart_container,
            font=('Consolas', 10),
            bg=self.colors['card'],
            fg=self.colors['text'],
            relief='flat',
            height=15
        )
        chart_text.pack(fill='both', expand=True)
        
        chart_text.insert('end', f"  {y_label} by {x_label}\n")
        chart_text.insert('end', "  " + "=" * 40 + "\n\n")
        
        for i, (x, y) in enumerate(zip(x_values, y_values)):
            bar_len = int((y / max_val) * bar_width)
            bar = "█" * bar_len
            chart_text.insert('end', f"  {str(x):<8} | {bar} {y:,.0f}\n")
        
        chart_text.insert('end', "\n  " + "-" * 40 + "\n")
        chart_text.insert('end', f"  Chart Type: {self.chart_type_var.get()}\n")
        chart_text.insert('end', "  (Install matplotlib for graphical charts)")
        
        chart_text.config(state='disabled')
    
    def run(self):
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TCombobox', fieldbackground='white')
        
        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.root.mainloop()


if __name__ == "__main__":
    app = DataVisualizationGUI()
    app.run()
