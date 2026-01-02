"""
Currency Converter GUI Application
Built with Tkinter - Part of 21APEX Challenge
"""

import tkinter as tk
from tkinter import ttk

class CurrencyConverterGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Currency Converter")
        self.root.geometry("450x550")
        self.root.resizable(False, False)
        self.root.configure(bg='#0a192f')
        
        # Colors
        self.colors = {
            'bg': '#0a192f',
            'card': '#112240',
            'primary': '#64ffda',
            'accent': '#f0a500',
            'text': '#ccd6f6',
            'text_dim': '#8892b0'
        }
        
        # Exchange rates (base: USD)
        self.rates = {
            'USD': {'name': 'US Dollar', 'symbol': '$', 'rate': 1.0},
            'EUR': {'name': 'Euro', 'symbol': '€', 'rate': 0.92},
            'GBP': {'name': 'British Pound', 'symbol': '£', 'rate': 0.79},
            'INR': {'name': 'Indian Rupee', 'symbol': '₹', 'rate': 83.50},
            'JPY': {'name': 'Japanese Yen', 'symbol': '¥', 'rate': 150.25},
            'AUD': {'name': 'Australian Dollar', 'symbol': 'A$', 'rate': 1.52},
            'CAD': {'name': 'Canadian Dollar', 'symbol': 'C$', 'rate': 1.36},
            'CHF': {'name': 'Swiss Franc', 'symbol': 'Fr', 'rate': 0.88},
            'CNY': {'name': 'Chinese Yuan', 'symbol': '¥', 'rate': 7.24},
            'AED': {'name': 'UAE Dirham', 'symbol': 'د.إ', 'rate': 3.67}
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=25, pady=25)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="💱 Currency Converter",
            font=('Segoe UI', 24, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=(0, 25))
        
        # Converter card
        converter_card = tk.Frame(main_frame, bg=self.colors['card'])
        converter_card.pack(fill='x', pady=10, ipady=20)
        
        # Amount input
        amount_frame = tk.Frame(converter_card, bg=self.colors['card'])
        amount_frame.pack(fill='x', padx=25, pady=15)
        
        tk.Label(
            amount_frame,
            text="Amount",
            font=('Segoe UI', 11),
            fg=self.colors['text_dim'],
            bg=self.colors['card']
        ).pack(anchor='w')
        
        self.amount_entry = tk.Entry(
            amount_frame,
            font=('Segoe UI', 20, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['primary'],
            relief='flat',
            justify='right'
        )
        self.amount_entry.pack(fill='x', ipady=10)
        self.amount_entry.insert(0, "1.00")
        self.amount_entry.bind('<KeyRelease>', lambda e: self.convert())
        
        # From currency
        from_frame = tk.Frame(converter_card, bg=self.colors['card'])
        from_frame.pack(fill='x', padx=25, pady=10)
        
        tk.Label(
            from_frame,
            text="From",
            font=('Segoe UI', 11),
            fg=self.colors['text_dim'],
            bg=self.colors['card']
        ).pack(anchor='w')
        
        self.from_var = tk.StringVar(value='USD')
        from_dropdown = ttk.Combobox(
            from_frame,
            textvariable=self.from_var,
            values=list(self.rates.keys()),
            state='readonly',
            font=('Segoe UI', 14)
        )
        from_dropdown.pack(fill='x', ipady=8)
        from_dropdown.bind('<<ComboboxSelected>>', lambda e: self.convert())
        
        # Swap button
        swap_btn = tk.Button(
            converter_card,
            text="⇅ Swap",
            font=('Segoe UI', 11, 'bold'),
            fg=self.colors['bg'],
            bg=self.colors['primary'],
            activebackground=self.colors['accent'],
            relief='flat',
            padx=20,
            pady=5,
            command=self.swap_currencies
        )
        swap_btn.pack(pady=10)
        
        # To currency
        to_frame = tk.Frame(converter_card, bg=self.colors['card'])
        to_frame.pack(fill='x', padx=25, pady=10)
        
        tk.Label(
            to_frame,
            text="To",
            font=('Segoe UI', 11),
            fg=self.colors['text_dim'],
            bg=self.colors['card']
        ).pack(anchor='w')
        
        self.to_var = tk.StringVar(value='INR')
        to_dropdown = ttk.Combobox(
            to_frame,
            textvariable=self.to_var,
            values=list(self.rates.keys()),
            state='readonly',
            font=('Segoe UI', 14)
        )
        to_dropdown.pack(fill='x', ipady=8)
        to_dropdown.bind('<<ComboboxSelected>>', lambda e: self.convert())
        
        # Result display
        result_frame = tk.Frame(converter_card, bg=self.colors['bg'])
        result_frame.pack(fill='x', padx=25, pady=20)
        
        self.result_label = tk.Label(
            result_frame,
            text="83.50",
            font=('Segoe UI', 36, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['bg']
        )
        self.result_label.pack(pady=10)
        
        self.rate_label = tk.Label(
            result_frame,
            text="1 USD = 83.50 INR",
            font=('Segoe UI', 12),
            fg=self.colors['text_dim'],
            bg=self.colors['bg']
        )
        self.rate_label.pack()
        
        # Exchange rates card
        rates_card = tk.Frame(main_frame, bg=self.colors['card'])
        rates_card.pack(fill='both', expand=True, pady=15)
        
        rates_title = tk.Label(
            rates_card,
            text="📊 Exchange Rates (Base: USD)",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['card']
        )
        rates_title.pack(pady=(15, 10))
        
        # Scrollable rates list
        rates_container = tk.Frame(rates_card, bg=self.colors['card'])
        rates_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        canvas = tk.Canvas(rates_container, bg=self.colors['card'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(rates_container, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['card'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add all rates
        for code, info in self.rates.items():
            rate_row = tk.Frame(scrollable_frame, bg=self.colors['card'])
            rate_row.pack(fill='x', pady=3)
            
            tk.Label(
                rate_row,
                text=f"{info['symbol']} {code}",
                font=('Segoe UI', 10, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['card'],
                width=10,
                anchor='w'
            ).pack(side='left')
            
            tk.Label(
                rate_row,
                text=info['name'],
                font=('Segoe UI', 10),
                fg=self.colors['text_dim'],
                bg=self.colors['card'],
                width=18,
                anchor='w'
            ).pack(side='left')
            
            tk.Label(
                rate_row,
                text=f"{info['rate']:.2f}",
                font=('Segoe UI', 10, 'bold'),
                fg=self.colors['primary'],
                bg=self.colors['card'],
                width=10,
                anchor='e'
            ).pack(side='right')
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Initial conversion
        self.convert()
    
    def convert(self):
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            self.result_label.config(text="Invalid")
            return
        
        from_rate = self.rates[self.from_var.get()]['rate']
        to_rate = self.rates[self.to_var.get()]['rate']
        
        # Convert through USD (base currency)
        usd_amount = amount / from_rate
        result = usd_amount * to_rate
        
        # Format result
        if result >= 1000:
            result_text = f"{result:,.2f}"
        else:
            result_text = f"{result:.4f}".rstrip('0').rstrip('.')
        
        to_symbol = self.rates[self.to_var.get()]['symbol']
        self.result_label.config(text=f"{to_symbol} {result_text}")
        
        # Update rate info
        rate = to_rate / from_rate
        from_code = self.from_var.get()
        to_code = self.to_var.get()
        self.rate_label.config(text=f"1 {from_code} = {rate:.4f} {to_code}")
    
    def swap_currencies(self):
        from_curr = self.from_var.get()
        to_curr = self.to_var.get()
        self.from_var.set(to_curr)
        self.to_var.set(from_curr)
        self.convert()
    
    def run(self):
        # Style configuration for combobox
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TCombobox',
                       fieldbackground=self.colors['bg'],
                       background=self.colors['card'],
                       foreground=self.colors['text'])
        
        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.root.mainloop()

if __name__ == "__main__":
    app = CurrencyConverterGUI()
    app.run()
