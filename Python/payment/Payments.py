#!/usr/bin/env python3
"""
Complete Bank Transaction Analyzer
A comprehensive single-file application for analyzing bank transactions
with GUI, charts, filtering, and export capabilities.

Author: AI Assistant
Date: August 28, 2025
Version: 1.0
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime, timedelta
import json
import csv
import os
import sys
from collections import defaultdict
import threading
import queue

# Set matplotlib style
plt.style.use('default')

class TransactionAnalyzer:
    """Main Transaction Analyzer Application"""
    
    def __init__(self):
        # Initialize main window
        self.root = tk.Tk()
        self.root.title("💳 Bank Transaction Analyzer v1.0")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#f0f0f0')
        
        # Data storage
        self.df = None
        self.filtered_df = None
        self.original_df = None
        
        # UI Components
        self.charts = {}
        self.stats_labels = {}
        
        # Category keywords for automatic categorization
        self.category_keywords = {
            "🥘 Food & Dining": [
                "swiggy", "zomato", "restaurant", "hotel", "cafe", "eatery", "food", 
                "dominos", "pizza hut", "kfc", "mcdonald", "burger king", "paid to",
                "dining", "meal", "lunch", "dinner", "breakfast", "canteen", "mess"
            ],
            "🛒 Groceries & Essentials": [
                "blinkit", "bigbasket", "grocery", "kirana", "spencer", "reliance fresh", 
                "dmart", "star bazaar", "meesho", "grofers", "fresh", "market",
                "vegetables", "fruits", "milk", "bread", "rice", "dal", "oil"
            ],
            "🏥 Medical & Healthcare": [
                "pharmacy", "hospital", "medical", "doctor", "clinic", "apollo", 
                "medplus", "1mg", "netmeds", "medicine", "tablet", "syrup",
                "checkup", "consultation", "lab", "test", "health", "care"
            ],
            "🧾 Bills & Utilities": [
                "jio", "airtel", "vodafone", "idea", "bsnl", "mtnl", "recharge", "bill", 
                "electricity", "water", "gas", "dth", "broadband", "wifi", "internet",
                "mobile", "phone", "postpaid", "prepaid", "utility"
            ],
            "🛍 Shopping": [
                "google play", "shopping", "flipkart", "amazon", "snapdeal", "myntra", 
                "nykaa", "ajio", "lifestyle", "max", "h&m", "zara", "shein", 
                "subscription", "netflix", "spotify", "hotstar", "prime video",
                "clothes", "dress", "shirt", "shoes", "electronics", "mobile", "laptop"
            ],
            "💵 Transfers & P2P": [
                "sent to", "money sent", "transfer", "upi to", "money given", 
                "to friend", "to family", "pay to", "transferred", "payment to"
            ],
            "💰 Money Received": [
                "received from", "payment from", "refund", "cashback", "reversal", 
                "credited", "salary", "income", "bonus", "interest", "dividend",
                "freelance", "commission", "reward", "gift"
            ],
            "🚖 Transport & Travel": [
                "uber", "ola", "rapido", "meru", "cab", "taxi", "bus", "train", "irctc", 
                "metro", "flight", "airlines", "indigo", "air india", "vistara", 
                "travel", "ticket", "booking", "petrol", "diesel", "fuel"
            ],
            "🎬 Entertainment": [
                "bookmyshow", "pvr", "inox", "movie", "cinema", "event", "concert", 
                "ticket", "game", "gaming", "entertainment", "fun", "park"
            ],
            "🎓 Education": [
                "byjus", "unacademy", "udemy", "coursera", "edx", "skillshare", 
                "school", "college", "exam fee", "tuition", "fees", "book", "course"
            ],
            "🏦 Banking & Fees": [
                "bank charge", "atm fee", "interest", "emi", "loan repayment", 
                "overdraft", "penalty", "service charge", "processing fee", "charges"
            ],
            "🏠 Rent & Housing": [
                "rent", "maintenance", "society", "housing", "flat", "apartment",
                "property", "deposit", "advance", "brokerage"
            ],
            "⛽ Fuel": [
                "petrol", "diesel", "fuel", "hpcl", "iocl", "bpcl", "shell", 
                "filling station", "pump", "cng", "lpg"
            ],
            "💳 ATM & Cash": [
                "atm", "cash withdrawal", "cash", "withdraw", "withdrawal"
            ]
        }
        
        # Color schemes
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'success': '#F18F01',
            'danger': '#C73E1D',
            'info': '#3F88C5',
            'light': '#F8F9FA',
            'dark': '#343A40'
        }
        
        # Create UI
        self.create_ui()
        self.generate_sample_data()
        
    def create_ui(self):
        """Create the main user interface"""
        # Create main container with notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_main_tab()
        self.create_charts_tab()
        self.create_data_tab()
        self.create_settings_tab()
        
        # Status bar
        self.create_status_bar()
        
    def create_status_bar(self):
        """Create status bar at bottom"""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(fill='x', side='bottom', padx=10, pady=(0, 10))
        
        self.status_label = ttk.Label(self.status_bar, text="Ready")
        self.status_label.pack(side='left')
        
        self.progress = ttk.Progressbar(self.status_bar, length=200, mode='indeterminate')
        self.progress.pack(side='right', padx=(10, 0))
        
    def create_main_tab(self):
        """Create main analysis tab"""
        main_frame = ttk.Frame(self.notebook)
        self.notebook.add(main_frame, text="🏠 Main Dashboard")
        
        # Control panel
        control_frame = ttk.LabelFrame(main_frame, text="📁 File Operations & Filters", padding="10")
        control_frame.pack(fill='x', padx=10, pady=10)
        
        # File operations
        file_frame = ttk.Frame(control_frame)
        file_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Button(file_frame, text="📂 Load Excel File", 
                  command=self.load_file, style='Accent.TButton').pack(side='left', padx=(0, 10))
        ttk.Button(file_frame, text="📋 Use Sample Data", 
                  command=self.load_sample_data, style='Accent.TButton').pack(side='left', padx=(0, 10))
        ttk.Button(file_frame, text="💾 Export CSV", 
                  command=self.export_csv).pack(side='left', padx=(0, 10))
        ttk.Button(file_frame, text="📊 Generate Report", 
                  command=self.generate_report).pack(side='left', padx=(0, 10))
        
        # Filters
        filter_frame = ttk.Frame(control_frame)
        filter_frame.pack(fill='x')
        
        # Amount filters
        ttk.Label(filter_frame, text="Min Amount (₹):").grid(row=0, column=0, sticky='w', padx=(0, 5))
        self.min_amount_var = tk.StringVar()
        self.min_amount_entry = ttk.Entry(filter_frame, textvariable=self.min_amount_var, width=12)
        self.min_amount_entry.grid(row=0, column=1, padx=(0, 15))
        
        ttk.Label(filter_frame, text="Max Amount (₹):").grid(row=0, column=2, sticky='w', padx=(0, 5))
        self.max_amount_var = tk.StringVar()
        self.max_amount_entry = ttk.Entry(filter_frame, textvariable=self.max_amount_var, width=12)
        self.max_amount_entry.grid(row=0, column=3, padx=(0, 15))
        
        # Category filter
        ttk.Label(filter_frame, text="Category:").grid(row=0, column=4, sticky='w', padx=(0, 5))
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(filter_frame, textvariable=self.category_var, 
                                          state='readonly', width=18)
        self.category_combo.grid(row=0, column=5, padx=(0, 15))
        
        # Keyword search
        ttk.Label(filter_frame, text="Search:").grid(row=0, column=6, sticky='w', padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=15)
        self.search_entry.grid(row=0, column=7, padx=(0, 15))
        
        # Filter buttons
        ttk.Button(filter_frame, text="🔍 Apply Filters", 
                  command=self.apply_filters).grid(row=0, column=8, padx=5)
        ttk.Button(filter_frame, text="🔄 Reset", 
                  command=self.reset_filters).grid(row=0, column=9, padx=5)
        
        # Statistics panel
        stats_frame = ttk.LabelFrame(main_frame, text="📊 Summary Statistics", padding="10")
        stats_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        self.create_stats_panel(stats_frame)
        
        # Quick charts
        quick_charts_frame = ttk.LabelFrame(main_frame, text="📈 Quick Analysis", padding="10")
        quick_charts_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        self.create_quick_charts(quick_charts_frame)
        
    def create_stats_panel(self, parent):
        """Create statistics display panel"""
        # Create grid of statistics
        stats_grid = ttk.Frame(parent)
        stats_grid.pack(fill='x')
        
        # Define statistics to display
        stats = [
            ("Total Spent", "total_spent", "💸"),
            ("Total Received", "total_received", "💰"),
            ("Net Amount", "net_amount", "📊"),
            ("Transaction Count", "transaction_count", "🔢"),
            ("Average Transaction", "avg_transaction", "📈"),
            ("Largest Transaction", "largest_transaction", "🏆"),
            ("Most Active Category", "top_category", "🎯"),
            ("Date Range", "date_range", "📅")
        ]
        
        # Create stats cards
        for i, (label, key, icon) in enumerate(stats):
            row, col = divmod(i, 4)
            
            card_frame = ttk.Frame(stats_grid, relief='raised', borderwidth=1)
            card_frame.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            
            ttk.Label(card_frame, text=f"{icon} {label}", font=('Arial', 9, 'bold')).pack(anchor='w')
            
            self.stats_labels[key] = ttk.Label(card_frame, text="₹0", font=('Arial', 11))
            self.stats_labels[key].pack(anchor='w', pady=(5, 10))
        
        # Configure grid weights
        for i in range(4):
            stats_grid.columnconfigure(i, weight=1)
    
    def create_quick_charts(self, parent):
        """Create quick analysis charts"""
        # Create chart container
        chart_container = ttk.Frame(parent)
        chart_container.pack(fill='both', expand=True)
        
        # Category pie chart
        self.fig_quick, ((self.ax_category, self.ax_trends), (self.ax_dow, self.ax_monthly)) = plt.subplots(
            2, 2, figsize=(12, 8))
        self.fig_quick.suptitle('Transaction Analysis Overview', fontsize=14, fontweight='bold')
        
        self.canvas_quick = FigureCanvasTkAgg(self.fig_quick, chart_container)
        self.canvas_quick.get_tk_widget().pack(fill='both', expand=True)
        
        # Initialize empty charts
        self.ax_category.set_title("💸 Spending by Category")
        self.ax_trends.set_title("📈 Daily Spending Trends")
        self.ax_dow.set_title("📅 Spending by Day of Week")
        self.ax_monthly.set_title("📊 Monthly Overview")
        
        plt.tight_layout()
        
    def create_charts_tab(self):
        """Create detailed charts tab"""
        charts_frame = ttk.Frame(self.notebook)
        self.notebook.add(charts_frame, text="📊 Detailed Charts")
        
        # Chart controls
        control_frame = ttk.Frame(charts_frame)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(control_frame, text="Chart Type:").pack(side='left', padx=(0, 10))
        
        self.chart_type_var = tk.StringVar(value="Category Analysis")
        chart_types = ["Category Analysis", "Time Trends", "Amount Distribution", "Merchant Analysis"]
        
        self.chart_type_combo = ttk.Combobox(control_frame, textvariable=self.chart_type_var,
                                           values=chart_types, state='readonly', width=20)
        self.chart_type_combo.pack(side='left', padx=(0, 10))
        self.chart_type_combo.bind('<<ComboboxSelected>>', self.update_detailed_chart)
        
        ttk.Button(control_frame, text="🔄 Update Chart", 
                  command=self.update_detailed_chart).pack(side='left', padx=10)
        
        # Chart area
        self.fig_detailed = Figure(figsize=(14, 10))
        self.canvas_detailed = FigureCanvasTkAgg(self.fig_detailed, charts_frame)
        self.canvas_detailed.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
    def create_data_tab(self):
        """Create data view tab"""
        data_frame = ttk.Frame(self.notebook)
        self.notebook.add(data_frame, text="📋 Transaction Data")
        
        # Data controls
        data_controls = ttk.Frame(data_frame)
        data_controls.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(data_controls, text="Show:").pack(side='left', padx=(0, 5))
        self.show_count_var = tk.StringVar(value="100")
        show_counts = ["50", "100", "200", "500", "All"]
        ttk.Combobox(data_controls, textvariable=self.show_count_var, values=show_counts, 
                    state='readonly', width=8).pack(side='left', padx=(0, 15))
        
        ttk.Label(data_controls, text="Sort by:").pack(side='left', padx=(0, 5))
        self.sort_by_var = tk.StringVar(value="DateTime")
        sort_options = ["DateTime", "Amount", "Category", "Transaction Details"]
        ttk.Combobox(data_controls, textvariable=self.sort_by_var, values=sort_options, 
                    state='readonly', width=15).pack(side='left', padx=(0, 15))
        
        ttk.Button(data_controls, text="🔄 Refresh Table", 
                  command=self.update_data_table).pack(side='left', padx=10)
        
        # Data table
        table_frame = ttk.Frame(data_frame)
        table_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Treeview with scrollbars
        self.tree_frame = ttk.Frame(table_frame)
        self.tree_frame.pack(fill='both', expand=True)
        
        columns = ("DateTime", "Details", "Category", "Amount", "Type")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show='headings', height=20)
        
        # Configure columns
        column_configs = {
            "DateTime": {"width": 150, "anchor": "w"},
            "Details": {"width": 350, "anchor": "w"},
            "Category": {"width": 180, "anchor": "w"},
            "Amount": {"width": 120, "anchor": "e"},
            "Type": {"width": 80, "anchor": "center"}
        }
        
        for col, config in column_configs.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=config["width"], anchor=config["anchor"])
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(self.tree_frame, orient='vertical', command=self.tree.yview)
        h_scroll = ttk.Scrollbar(self.tree_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        # Pack treeview and scrollbars
        self.tree.pack(fill='both', expand=True)
        v_scroll.pack(side='right', fill='y')
        h_scroll.pack(side='bottom', fill='x')
        
    def create_settings_tab(self):
        """Create settings and configuration tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # Category management
        category_frame = ttk.LabelFrame(settings_frame, text="🏷️ Category Management", padding="10")
        category_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Category list
        list_frame = ttk.Frame(category_frame)
        list_frame.pack(fill='both', expand=True)
        
        ttk.Label(list_frame, text="Categories and Keywords:", font=('Arial', 10, 'bold')).pack(anchor='w')
        
        # Text widget to display and edit categories
        self.category_text = tk.Text(list_frame, height=25, width=80)
        self.category_text.pack(fill='both', expand=True, pady=(10, 0))
        
        # Populate with current categories
        self.update_category_text()
        
        # Buttons
        button_frame = ttk.Frame(category_frame)
        button_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(button_frame, text="💾 Save Categories", 
                  command=self.save_categories).pack(side='left', padx=(0, 10))
        ttk.Button(button_frame, text="🔄 Reset to Default", 
                  command=self.reset_categories).pack(side='left', padx=(0, 10))
        ttk.Button(button_frame, text="📥 Import Categories", 
                  command=self.import_categories).pack(side='left', padx=(0, 10))
        ttk.Button(button_frame, text="📤 Export Categories", 
                  command=self.export_categories).pack(side='left')
        
    def update_category_text(self):
        """Update the category text widget"""
        self.category_text.delete(1.0, tk.END)
        for category, keywords in self.category_keywords.items():
            self.category_text.insert(tk.END, f"{category}:\n")
            self.category_text.insert(tk.END, f"  {', '.join(keywords)}\n\n")
    
    def categorize_transaction(self, details):
        """Categorize a transaction based on keywords"""
        if pd.isna(details) or str(details).strip() == '':
            return "🔄 Miscellaneous"
        
        details_lower = str(details).lower().strip()
        
        for category, keywords in self.category_keywords.items():
            for keyword in keywords:
                if keyword.lower() in details_lower:
                    return category
        
        return "🔄 Miscellaneous"
    
    def load_file(self):
        """Load Excel file"""
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[
                ("Excel Files", "*.xlsx *.xls"),
                ("CSV Files", "*.csv"),
                ("All Files", "*.*")
            ]
        )
        
        if not file_path:
            return
        
        try:
            self.update_status("Loading file...")
            self.progress.start(10)
            
            # Load file based on extension
            if file_path.lower().endswith('.csv'):
                self.df = pd.read_csv(file_path)
            else:
                self.df = pd.read_excel(file_path, engine='openpyxl')
            
            # Process the loaded data
            self.process_data()
            
            self.update_status(f"Successfully loaded {len(self.df)} transactions")
            messagebox.showinfo("Success", f"Successfully loaded {len(self.df)} transactions!")
            
            self.reset_filters()
            
        except Exception as e:
            self.update_status("Error loading file")
            messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
        
        finally:
            self.progress.stop()
    
    def process_data(self):
        """Process loaded data"""
        if self.df is None:
            return
        
        # Handle DateTime columns
        if 'Date' in self.df.columns and 'Time' in self.df.columns:
            # Combine Date and Time
            try:
                self.df['DateTime'] = pd.to_datetime(
                    self.df['Date'].astype(str) + ' ' + self.df['Time'].astype(str), 
                    errors='coerce'
                )
            except:
                self.df['DateTime'] = pd.to_datetime(self.df['Date'], errors='coerce')
        elif 'Date' in self.df.columns:
            self.df['DateTime'] = pd.to_datetime(self.df['Date'], errors='coerce')
        elif 'DateTime' in self.df.columns:
            self.df['DateTime'] = pd.to_datetime(self.df['DateTime'], errors='coerce')
        else:
            # Create dummy dates
            base_date = datetime.now() - timedelta(days=len(self.df))
            self.df['DateTime'] = [base_date + timedelta(days=i) for i in range(len(self.df))]
        
        # Handle Amount column
        amount_col = None
        for col in self.df.columns:
            if 'amount' in col.lower():
                amount_col = col
                break
        
        if amount_col:
            # Clean and convert amount
            self.df['Amount'] = pd.to_numeric(
                self.df[amount_col].astype(str).str.replace(r'[₹,$,\s]', '', regex=True),
                errors='coerce'
            ).fillna(0)
        else:
            self.df['Amount'] = 0
        
        # Handle Transaction Details
        details_col = None
        for col in self.df.columns:
            if 'transaction' in col.lower() and 'detail' in col.lower():
                details_col = col
                break
        
        if not details_col:
            # Look for any text column that might contain transaction info
            text_cols = [col for col in self.df.columns if self.df[col].dtype == 'object']
            if text_cols:
                details_col = text_cols[0]
        
        if details_col:
            self.df['Transaction Details'] = self.df[details_col].fillna('Unknown Transaction')
        else:
            self.df['Transaction Details'] = 'Unknown Transaction'
        
        # Add derived columns
        self.df['Category'] = self.df['Transaction Details'].apply(self.categorize_transaction)
        self.df['Type'] = self.df['Amount'].apply(lambda x: 'Credit' if x > 0 else 'Debit')
        self.df['AbsAmount'] = self.df['Amount'].abs()
        
        # Add time-based columns
        self.df['Date'] = self.df['DateTime'].dt.date
        self.df['DayOfWeek'] = self.df['DateTime'].dt.day_name()
        self.df['Month'] = self.df['DateTime'].dt.strftime('%Y-%m')
        self.df['WeekOfYear'] = self.df['DateTime'].dt.isocalendar().week
        
        # Store original for reset
        self.original_df = self.df.copy()
        self.filtered_df = self.df.copy()
    
    def generate_sample_data(self):
        """Generate sample transaction data"""
        np.random.seed(42)  # For reproducible results
        
        transactions = []
        base_date = datetime.now() - timedelta(days=120)
        
        # Transaction templates with realistic amounts and categories
        templates = [
            # Food & Dining
            ("Swiggy Food Delivery", -450, "🥘 Food & Dining"),
            ("Zomato Order", -320, "🥘 Food & Dining"),
            ("McDonald's", -280, "🥘 Food & Dining"),
            ("Cafe Coffee Day", -150, "🥘 Food & Dining"),
            ("Local Restaurant", -650, "🥘 Food & Dining"),
            ("Pizza Hut", -480, "🥘 Food & Dining"),
            ("KFC", -380, "🥘 Food & Dining"),
            
            # Groceries
            ("BigBasket Grocery", -1250, "🛒 Groceries & Essentials"),
            ("DMart Shopping", -890, "🛒 Groceries & Essentials"),
            ("Local Kirana Store", -340, "🛒 Groceries & Essentials"),
            ("Reliance Fresh", -560, "🛒 Groceries & Essentials"),
            ("Blinkit Delivery", -420, "🛒 Groceries & Essentials"),
            
            # Shopping
            ("Amazon Purchase", -2150, "🛍 Shopping"),
            ("Flipkart Order", -1580, "🛍 Shopping"),
            ("Myntra Clothing", -980, "🛍 Shopping"),
            ("Nykaa Beauty Products", -450, "🛍 Shopping"),
            ("Lifestyle Store", -1200, "🛍 Shopping"),
            ("Max Fashion", -800, "🛍 Shopping"),
            
            # Bills & Utilities
            ("Jio Recharge", -399, "🧾 Bills & Utilities"),
            ("Airtel Postpaid", -599, "🧾 Bills & Utilities"),
            ("Electricity Bill", -1200, "🧾 Bills & Utilities"),
            ("Water Bill", -300, "🧾 Bills & Utilities"),
            ("Broadband Bill", -799, "🧾 Bills & Utilities"),
            ("DTH Recharge", -250, "🧾 Bills & Utilities"),
            
            # Medical
            ("Apollo Pharmacy", -850, "🏥 Medical & Healthcare"),
            ("Medical Consultation", -500, "🏥 Medical & Healthcare"),
            ("1mg Medicine", -320, "🏥 Medical & Healthcare"),
            ("Lab Test", -800, "🏥 Medical & Healthcare"),
            
            # Transport
            ("Uber Trip", -275, "🚖 Transport & Travel"),
            ("Ola Cab", -180, "🚖 Transport & Travel"),
            ("Petrol", -3000, "⛽ Fuel"),
            ("Metro Card Recharge", -200, "🚖 Transport & Travel"),
            ("Auto Rickshaw", -120, "🚖 Transport & Travel"),
            
            # Entertainment
            ("Netflix Subscription", -649, "🛍 Shopping"),
            ("BookMyShow Tickets", -400, "🎬 Entertainment"),
            ("Spotify Premium", -119, "🛍 Shopping"),
            ("PVR Cinema", -600, "🎬 Entertainment"),
            
            # Income transactions
            ("Salary Credit", 85000, "💰 Money Received"),
            ("Freelance Payment", 15000, "💰 Money Received"),
            ("Interest Credit", 250, "💰 Money Received"),
            ("Cashback", 50, "💰 Money Received"),
            ("Refund", 299, "💰 Money Received"),
            ("Bonus", 10000, "💰 Money Received"),
            ("Dividend", 500, "💰 Money Received"),
            
            # Transfers
            ("Money sent to friend", -2000, "💵 Transfers & P2P"),
            ("Family transfer", -5000, "💵 Transfers & P2P"),
            ("Split payment", -800, "💵 Transfers & P2P"),
            
            # Banking
            ("ATM Withdrawal", -2000, "💳 ATM & Cash"),
            ("Bank Charges", -150, "🏦 Banking & Fees"),
            ("Annual Fee", -500, "🏦 Banking & Fees"),
            ("Interest Debit", -75, "🏦 Banking & Fees"),
            
            # Housing
            ("Rent Payment", -25000, "🏠 Rent & Housing"),
            ("Maintenance", -2000, "🏠 Rent & Housing"),
            ("Security Deposit", -10000, "🏠 Rent & Housing"),
        ]
        
        # Generate 300 transactions over past 120 days
        for i in range(300):
            template = templates[i % len(templates)]
            
            # Add random variation to amounts (±30%)
            variation = np.random.uniform(0.7, 1.3)
            amount = template[1] * variation
            
            # Random date within the range
            days_ago = np.random.randint(0, 120)
            hours = np.random.randint(6, 22)
            minutes = np.random.randint(0, 59)
            
            transaction_date = base_date + timedelta(days=days_ago, hours=hours, minutes=minutes)
            
            transactions.append({
                'DateTime': transaction_date,
                'Date': transaction_date.date(),
                'Time': transaction_date.strftime('%H:%M'),
                'Transaction Details': template[0],
                'Amount': round(amount, 2),
                'Category': template[2],
                'Other Transaction Details (UPI ID or A/c No)': f"merchant{np.random.randint(1000, 9999)}@paytm" if amount < 0 else "",
                'Your Account': 'XXXX1234',
                'UPI Ref No.': f"UPI{np.random.randint(100000, 999999)}" if amount < 0 else "",
                'Order ID': f"ORD{np.random.randint(10000, 99999)}" if amount < 0 else "",
                'Remarks': template[0],
                'Tags': template[2].split(' ')[-1],
                'Comment': ''
            })
        
        # Create DataFrame
        self.sample_df = pd.DataFrame(transactions)
        
        # Add derived columns
        self.sample_df['Type'] = self.sample_df['Amount'].apply(lambda x: 'Credit' if x > 0 else 'Debit')
        self.sample_df['AbsAmount'] = self.sample_df['Amount'].abs()
        self.sample_df['DayOfWeek'] = self.sample_df['DateTime'].dt.day_name()
        self.sample_df['Month'] = self.sample_df['DateTime'].dt.strftime('%Y-%m')
        self.sample_df['WeekOfYear'] = self.sample_df['DateTime'].dt.isocalendar().week
        
    def load_sample_data(self):
        """Load sample data"""
        if not hasattr(self, 'sample_df'):
            self.generate_sample_data()
        
        self.df = self.sample_df.copy()
        self.original_df = self.df.copy()
        self.filtered_df = self.df.copy()
        
        self.update_status(f"Loaded {len(self.df)} sample transactions")
        messagebox.showinfo("Sample Data", f"Loaded {len(self.df)} sample transactions!")
        
        self.reset_filters()
    
    def apply_filters(self):
        """Apply filters to the data"""
        if self.df is None:
            messagebox.showwarning("Warning", "Please load data first!")
            return
        
        try:
            filtered_df = self.df.copy()
            
            # Amount filters
            if self.min_amount_var.get():
                min_amount = float(self.min_amount_var.get())
                filtered_df = filtered_df[filtered_df['AbsAmount'] >= min_amount]
            
            if self.max_amount_var.get():
                max_amount = float(self.max_amount_var.get())
                filtered_df = filtered_df[filtered_df['AbsAmount'] <= max_amount]
            
            # Category filter
            if self.category_var.get() and self.category_var.get() != "All":
                filtered_df = filtered_df[filtered_df['Category'] == self.category_var.get()]
            
            # Keyword search
            if self.search_var.get():
                keyword = self.search_var.get().lower()
                filtered_df = filtered_df[
                    filtered_df['Transaction Details'].str.lower().str.contains(keyword, na=False)
                ]
            
            self.filtered_df = filtered_df
            
            # Update displays
            self.update_all_displays()
            
            self.update_status(f"Filters applied - showing {len(self.filtered_df)} of {len(self.df)} transactions")
            
        except ValueError as e:
            messagebox.showerror("Filter Error", f"Invalid filter value: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error applying filters: {str(e)}")
    
    def reset_filters(self):
        """Reset all filters"""
        if self.df is None:
            return
        
        # Clear filter inputs
        self.min_amount_var.set("")
        self.max_amount_var.set("")
        self.category_var.set("All")
        self.search_var.set("")
        
        # Update category dropdown
        categories = ['All'] + sorted(self.df['Category'].unique())
        self.category_combo['values'] = categories
        if categories:
            self.category_combo.current(0)
        
        # Reset filtered data
        self.filtered_df = self.df.copy()
        
        # Update all displays
        self.update_all_displays()
        
        self.update_status(f"Filters reset - showing all {len(self.df)} transactions")
    
    def update_all_displays(self):
        """Update all displays with current filtered data"""
        if self.filtered_df is None:
            return
        
        self.update_statistics()
        self.update_quick_charts()
        self.update_data_table()
        self.update_detailed_chart()
    
    def update_statistics(self):
        """Update statistics display"""
        if self.filtered_df is None or len(self.filtered_df) == 0:
            # Set all to zero/empty
            for key in self.stats_labels:
                self.stats_labels[key].config(text="₹0" if "amount" in key or "spent" in key or "received" in key else "0")
            return
        
        df = self.filtered_df
        
        # Calculate statistics
        debit_data = df[df['Amount'] < 0]
        credit_data = df[df['Amount'] > 0]
        
        total_spent = debit_data['Amount'].abs().sum() if len(debit_data) > 0 else 0
        total_received = credit_data['Amount'].sum() if len(credit_data) > 0 else 0
        net_amount = total_received - total_spent
        transaction_count = len(df)
        avg_transaction = df['Amount'].mean()
        
        # Largest transaction
        largest_amount = df.loc[df['AbsAmount'].idxmax(), 'Amount'] if len(df) > 0 else 0
        
        # Most active category
        if len(debit_data) > 0:
            top_category = debit_data['Category'].mode()
            top_category = top_category.iloc[0] if len(top_category) > 0 else "N/A"
        else:
            top_category = "N/A"
        
        # Date range
        if len(df) > 0:
            date_min = df['DateTime'].min().strftime('%Y-%m-%d')
            date_max = df['DateTime'].max().strftime('%Y-%m-%d')
            date_range = f"{date_min} to {date_max}"
        else:
            date_range = "No data"
        
        # Update labels
        self.stats_labels['total_spent'].config(text=f"₹{total_spent:,.2f}")
        self.stats_labels['total_received'].config(text=f"₹{total_received:,.2f}")
        self.stats_labels['net_amount'].config(text=f"₹{net_amount:,.2f}")
        self.stats_labels['transaction_count'].config(text=f"{transaction_count:,}")
        self.stats_labels['avg_transaction'].config(text=f"₹{avg_transaction:,.2f}")
        self.stats_labels['largest_transaction'].config(text=f"₹{abs(largest_amount):,.2f}")
        self.stats_labels['top_category'].config(text=top_category)
        self.stats_labels['date_range'].config(text=date_range)
    
    def update_quick_charts(self):
        """Update quick analysis charts"""
        if self.filtered_df is None or len(self.filtered_df) == 0:
            # Clear all charts
            for ax in [self.ax_category, self.ax_trends, self.ax_dow, self.ax_monthly]:
                ax.clear()
                ax.text(0.5, 0.5, 'No Data', ha='center', va='center', transform=ax.transAxes)
            self.canvas_quick.draw()
            return
        
        df = self.filtered_df
        
        # Clear all axes
        self.ax_category.clear()
        self.ax_trends.clear()
        self.ax_dow.clear()
        self.ax_monthly.clear()
        
        # 1. Category pie chart (spending only)
        debit_data = df[df['Amount'] < 0]
        if len(debit_data) > 0:
            category_data = debit_data.groupby('Category')['AbsAmount'].sum()
            if len(category_data) > 0:
                colors = plt.cm.Set3(np.linspace(0, 1, len(category_data)))
                wedges, texts, autotexts = self.ax_category.pie(
                    category_data.values,
                    labels=category_data.index,
                    autopct='%1.1f%%',
                    colors=colors,
                    startangle=90
                )
                # Make text smaller
                for text in texts:
                    text.set_fontsize(8)
                for autotext in autotexts:
                    autotext.set_fontsize(7)
        
        self.ax_category.set_title("💸 Spending by Category", fontsize=10)
        
        # 2. Daily spending trends
        if len(debit_data) > 0:
            daily_spending = debit_data.groupby('Date')['AbsAmount'].sum().sort_index()
            if len(daily_spending) > 0:
                self.ax_trends.plot(daily_spending.index, daily_spending.values, 
                                   marker='o', linewidth=1, markersize=3, color='#2E86AB')
                self.ax_trends.tick_params(axis='x', rotation=45, labelsize=8)
                self.ax_trends.tick_params(axis='y', labelsize=8)
        
        self.ax_trends.set_title("📈 Daily Spending Trends", fontsize=10)
        self.ax_trends.grid(True, alpha=0.3)
        
        # 3. Day of week spending
        if len(debit_data) > 0:
            dow_data = debit_data.groupby('DayOfWeek')['AbsAmount'].sum()
            # Reorder days
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            dow_data = dow_data.reindex([day for day in day_order if day in dow_data.index])
            
            if len(dow_data) > 0:
                colors = plt.cm.Pastel1(np.linspace(0, 1, len(dow_data)))
                self.ax_dow.bar(range(len(dow_data)), dow_data.values, color=colors)
                self.ax_dow.set_xticks(range(len(dow_data)))
                self.ax_dow.set_xticklabels([day[:3] for day in dow_data.index], fontsize=8)
                self.ax_dow.tick_params(axis='y', labelsize=8)
        
        self.ax_dow.set_title("📅 Spending by Day of Week", fontsize=10)
        self.ax_dow.grid(True, alpha=0.3, axis='y')
        
        # 4. Monthly overview
        if len(df) > 0:
            monthly_data = df.groupby('Month').agg({
                'Amount': lambda x: len(x[x < 0])  # Count of debit transactions
            })
            
            if len(monthly_data) > 0:
                colors = plt.cm.Set2(np.linspace(0, 1, len(monthly_data)))
                self.ax_monthly.bar(range(len(monthly_data)), monthly_data['Amount'].values, color=colors)
                self.ax_monthly.set_xticks(range(len(monthly_data)))
                self.ax_monthly.set_xticklabels(monthly_data.index, rotation=45, fontsize=8)
                self.ax_monthly.tick_params(axis='y', labelsize=8)
        
        self.ax_monthly.set_title("📊 Transaction Count by Month", fontsize=10)
        self.ax_monthly.grid(True, alpha=0.3, axis='y')
        
        # Adjust layout and refresh
        self.fig_quick.suptitle('Transaction Analysis Overview', fontsize=12, fontweight='bold')
        plt.tight_layout()
        self.canvas_quick.draw()
    
    def update_detailed_chart(self, event=None):
        """Update detailed chart based on selected type"""
        if self.filtered_df is None or len(self.filtered_df) == 0:
            self.fig_detailed.clear()
            ax = self.fig_detailed.add_subplot(111)
            ax.text(0.5, 0.5, 'No Data Available', ha='center', va='center', transform=ax.transAxes)
            self.canvas_detailed.draw()
            return
        
        chart_type = self.chart_type_var.get()
        df = self.filtered_df
        
        self.fig_detailed.clear()
        
        if chart_type == "Category Analysis":
            self.create_category_analysis_chart(df)
        elif chart_type == "Time Trends":
            self.create_time_trends_chart(df)
        elif chart_type == "Amount Distribution":
            self.create_amount_distribution_chart(df)
        elif chart_type == "Merchant Analysis":
            self.create_merchant_analysis_chart(df)
        
        self.canvas_detailed.draw()
    
    def create_category_analysis_chart(self, df):
        """Create detailed category analysis"""
        debit_data = df[df['Amount'] < 0]
        
        if len(debit_data) == 0:
            ax = self.fig_detailed.add_subplot(111)
            ax.text(0.5, 0.5, 'No Spending Data Available', ha='center', va='center')
            return
        
        # Create 2x2 subplot
        ax1 = self.fig_detailed.add_subplot(2, 2, 1)
        ax2 = self.fig_detailed.add_subplot(2, 2, 2)
        ax3 = self.fig_detailed.add_subplot(2, 2, 3)
        ax4 = self.fig_detailed.add_subplot(2, 2, 4)
        
        # 1. Category pie chart
        category_totals = debit_data.groupby('Category')['AbsAmount'].sum().sort_values(ascending=False)
        colors = plt.cm.Set3(np.linspace(0, 1, len(category_totals)))
        ax1.pie(category_totals.values, labels=category_totals.index, autopct='%1.1f%%', 
                colors=colors, startangle=90)
        ax1.set_title('Spending Distribution by Category')
        
        # 2. Top categories bar chart
        top_categories = category_totals.head(10)
        ax2.barh(range(len(top_categories)), top_categories.values, 
                color=plt.cm.Pastel1(np.linspace(0, 1, len(top_categories))))
        ax2.set_yticks(range(len(top_categories)))
        ax2.set_yticklabels([cat[:20] + '...' if len(cat) > 20 else cat for cat in top_categories.index])
        ax2.set_title('Top Categories by Amount')
        ax2.set_xlabel('Amount (₹)')
        
        # 3. Category vs count
        category_counts = debit_data.groupby('Category').size().sort_values(ascending=False).head(10)
        ax3.bar(range(len(category_counts)), category_counts.values,
                color=plt.cm.Set2(np.linspace(0, 1, len(category_counts))))
        ax3.set_xticks(range(len(category_counts)))
        ax3.set_xticklabels([cat[:10] + '...' if len(cat) > 10 else cat for cat in category_counts.index], 
                           rotation=45)
        ax3.set_title('Transaction Count by Category')
        ax3.set_ylabel('Number of Transactions')
        
        # 4. Average amount by category
        avg_amounts = debit_data.groupby('Category')['AbsAmount'].mean().sort_values(ascending=False).head(10)
        ax4.bar(range(len(avg_amounts)), avg_amounts.values,
                color=plt.cm.Pastel2(np.linspace(0, 1, len(avg_amounts))))
        ax4.set_xticks(range(len(avg_amounts)))
        ax4.set_xticklabels([cat[:10] + '...' if len(cat) > 10 else cat for cat in avg_amounts.index], 
                           rotation=45)
        ax4.set_title('Average Amount by Category')
        ax4.set_ylabel('Average Amount (₹)')
        
        self.fig_detailed.suptitle('Detailed Category Analysis', fontsize=16, fontweight='bold')
        plt.tight_layout()
    
    def create_time_trends_chart(self, df):
        """Create detailed time trends analysis"""
        if len(df) == 0:
            ax = self.fig_detailed.add_subplot(111)
            ax.text(0.5, 0.5, 'No Data Available', ha='center', va='center')
            return
        
        # Create 2x2 subplot
        ax1 = self.fig_detailed.add_subplot(2, 2, 1)
        ax2 = self.fig_detailed.add_subplot(2, 2, 2)
        ax3 = self.fig_detailed.add_subplot(2, 2, 3)
        ax4 = self.fig_detailed.add_subplot(2, 2, 4)
        
        debit_data = df[df['Amount'] < 0]
        
        # 1. Daily spending trend
        if len(debit_data) > 0:
            daily_spending = debit_data.groupby('Date')['AbsAmount'].sum().sort_index()
            ax1.plot(daily_spending.index, daily_spending.values, marker='o', linewidth=2, markersize=4)
            ax1.set_title('Daily Spending Trend')
            ax1.set_ylabel('Amount (₹)')
            ax1.tick_params(axis='x', rotation=45)
            ax1.grid(True, alpha=0.3)
        
        # 2. Monthly spending
        if len(debit_data) > 0:
            monthly_spending = debit_data.groupby('Month')['AbsAmount'].sum().sort_index()
            ax2.bar(range(len(monthly_spending)), monthly_spending.values,
                   color=plt.cm.Blues(np.linspace(0.3, 1, len(monthly_spending))))
            ax2.set_xticks(range(len(monthly_spending)))
            ax2.set_xticklabels(monthly_spending.index, rotation=45)
            ax2.set_title('Monthly Spending')
            ax2.set_ylabel('Amount (₹)')
        
        # 3. Weekly pattern
        if len(debit_data) > 0:
            weekly_spending = debit_data.groupby('DayOfWeek')['AbsAmount'].sum()
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            weekly_spending = weekly_spending.reindex([day for day in day_order if day in weekly_spending.index])
            
            ax3.bar(range(len(weekly_spending)), weekly_spending.values,
                   color=plt.cm.Greens(np.linspace(0.3, 1, len(weekly_spending))))
            ax3.set_xticks(range(len(weekly_spending)))
            ax3.set_xticklabels([day[:3] for day in weekly_spending.index])
            ax3.set_title('Weekly Spending Pattern')
            ax3.set_ylabel('Amount (₹)')
        
        # 4. Hourly pattern (if time data available)
        if 'DateTime' in df.columns:
            df_with_hour = df.copy()
            df_with_hour['Hour'] = df_with_hour['DateTime'].dt.hour
            debit_hourly = df_with_hour[df_with_hour['Amount'] < 0]
            
            if len(debit_hourly) > 0:
                hourly_spending = debit_hourly.groupby('Hour')['AbsAmount'].sum()
                ax4.plot(hourly_spending.index, hourly_spending.values, marker='o', linewidth=2)
                ax4.set_title('Hourly Spending Pattern')
                ax4.set_xlabel('Hour of Day')
                ax4.set_ylabel('Amount (₹)')
                ax4.grid(True, alpha=0.3)
            else:
                ax4.text(0.5, 0.5, 'No Hourly Data', ha='center', va='center', transform=ax4.transAxes)
        
        self.fig_detailed.suptitle('Detailed Time Trends Analysis', fontsize=16, fontweight='bold')
        plt.tight_layout()
    
    def create_amount_distribution_chart(self, df):
        """Create amount distribution analysis"""
        if len(df) == 0:
            ax = self.fig_detailed.add_subplot(111)
            ax.text(0.5, 0.5, 'No Data Available', ha='center', va='center')
            return
        
        # Create 2x2 subplot
        ax1 = self.fig_detailed.add_subplot(2, 2, 1)
        ax2 = self.fig_detailed.add_subplot(2, 2, 2)
        ax3 = self.fig_detailed.add_subplot(2, 2, 3)
        ax4 = self.fig_detailed.add_subplot(2, 2, 4)
        
        # 1. Amount histogram
        amounts = df['Amount']
        ax1.hist(amounts, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        ax1.set_title('Amount Distribution')
        ax1.set_xlabel('Amount (₹)')
        ax1.set_ylabel('Frequency')
        ax1.grid(True, alpha=0.3)
        
        # 2. Debit vs Credit amounts
        debit_amounts = df[df['Amount'] < 0]['Amount'].abs()
        credit_amounts = df[df['Amount'] > 0]['Amount']
        
        if len(debit_amounts) > 0:
            ax2.hist(debit_amounts, bins=20, alpha=0.7, label='Debits', color='red')
        if len(credit_amounts) > 0:
            ax2.hist(credit_amounts, bins=20, alpha=0.7, label='Credits', color='green')
        
        ax2.set_title('Debit vs Credit Distribution')
        ax2.set_xlabel('Amount (₹)')
        ax2.set_ylabel('Frequency')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Box plot by category (top 8 categories)
        debit_data = df[df['Amount'] < 0]
        if len(debit_data) > 0:
            top_categories = debit_data['Category'].value_counts().head(8).index
            category_amounts = []
            category_labels = []
            
            for cat in top_categories:
                cat_amounts = debit_data[debit_data['Category'] == cat]['AbsAmount']
                if len(cat_amounts) > 0:
                    category_amounts.append(cat_amounts.values)
                    category_labels.append(cat[:15] + '...' if len(cat) > 15 else cat)
            
            if category_amounts:
                ax3.boxplot(category_amounts, labels=category_labels)
                ax3.set_title('Amount Distribution by Category')
                ax3.set_ylabel('Amount (₹)')
                ax3.tick_params(axis='x', rotation=45)
        else:
            ax3.text(0.5, 0.5, 'No Debit Data', ha='center', va='center', transform=ax3.transAxes)
        
        # 4. Cumulative spending over time
        if len(debit_data) > 0:
            daily_spending = debit_data.groupby('Date')['AbsAmount'].sum().sort_index()
            cumulative_spending = daily_spending.cumsum()
            
            ax4.plot(cumulative_spending.index, cumulative_spending.values, linewidth=2, color='red')
            ax4.set_title('Cumulative Spending Over Time')
            ax4.set_xlabel('Date')
            ax4.set_ylabel('Cumulative Amount (₹)')
            ax4.tick_params(axis='x', rotation=45)
            ax4.grid(True, alpha=0.3)
        else:
            ax4.text(0.5, 0.5, 'No Spending Data', ha='center', va='center', transform=ax4.transAxes)
        
        self.fig_detailed.suptitle('Amount Distribution Analysis', fontsize=16, fontweight='bold')
        plt.tight_layout()
    
    def create_merchant_analysis_chart(self, df):
        """Create merchant analysis"""
        debit_data = df[df['Amount'] < 0]
        
        if len(debit_data) == 0:
            ax = self.fig_detailed.add_subplot(111)
            ax.text(0.5, 0.5, 'No Spending Data Available', ha='center', va='center')
            return
        
        # Create 2x2 subplot
        ax1 = self.fig_detailed.add_subplot(2, 2, 1)
        ax2 = self.fig_detailed.add_subplot(2, 2, 2)
        ax3 = self.fig_detailed.add_subplot(2, 2, 3)
        ax4 = self.fig_detailed.add_subplot(2, 2, 4)
        
        # 1. Top merchants by amount
        merchant_amounts = debit_data.groupby('Transaction Details')['AbsAmount'].sum().sort_values(ascending=False).head(10)
        ax1.barh(range(len(merchant_amounts)), merchant_amounts.values,
                color=plt.cm.Set1(np.linspace(0, 1, len(merchant_amounts))))
        ax1.set_yticks(range(len(merchant_amounts)))
        ax1.set_yticklabels([merchant[:25] + '...' if len(merchant) > 25 else merchant 
                           for merchant in merchant_amounts.index])
        ax1.set_title('Top Merchants by Amount')
        ax1.set_xlabel('Amount (₹)')
        
        # 2. Top merchants by frequency
        merchant_counts = debit_data['Transaction Details'].value_counts().head(10)
        ax2.bar(range(len(merchant_counts)), merchant_counts.values,
               color=plt.cm.Set2(np.linspace(0, 1, len(merchant_counts))))
        ax2.set_xticks(range(len(merchant_counts)))
        ax2.set_xticklabels([merchant[:15] + '...' if len(merchant) > 15 else merchant 
                           for merchant in merchant_counts.index], rotation=45)
        ax2.set_title('Most Frequent Merchants')
        ax2.set_ylabel('Transaction Count')
        
        # 3. Average amount by merchant
        merchant_avg = debit_data.groupby('Transaction Details')['AbsAmount'].mean().sort_values(ascending=False).head(10)
        ax3.bar(range(len(merchant_avg)), merchant_avg.values,
               color=plt.cm.Set3(np.linspace(0, 1, len(merchant_avg))))
        ax3.set_xticks(range(len(merchant_avg)))
        ax3.set_xticklabels([merchant[:15] + '...' if len(merchant) > 15 else merchant 
                           for merchant in merchant_avg.index], rotation=45)
        ax3.set_title('Highest Average Amount')
        ax3.set_ylabel('Average Amount (₹)')
        
        # 4. Merchant category distribution
        merchant_categories = debit_data.groupby(['Transaction Details', 'Category']).size().reset_index(name='count')
        top_merchants = merchant_amounts.head(15).index
        
        # Create a stacked bar for top merchants showing their categories
        merchant_cat_data = {}
        for merchant in top_merchants:
            merchant_data = debit_data[debit_data['Transaction Details'] == merchant]
            cat_counts = merchant_data['Category'].value_counts()
            merchant_cat_data[merchant] = cat_counts
        
        if merchant_cat_data:
            # Get all unique categories
            all_cats = set()
            for cats in merchant_cat_data.values():
                all_cats.update(cats.index)
            all_cats = sorted(list(all_cats))
            
            # Create matrix for stacked bar
            merchants = list(merchant_cat_data.keys())[:8]  # Limit to 8 for readability
            bottom = np.zeros(len(merchants))
            
            colors = plt.cm.tab20(np.linspace(0, 1, len(all_cats)))
            
            for i, cat in enumerate(all_cats):
                values = [merchant_cat_data[merchant].get(cat, 0) for merchant in merchants]
                if sum(values) > 0:  # Only plot if there are values
                    ax4.bar(range(len(merchants)), values, bottom=bottom, label=cat[:10], color=colors[i])
                    bottom += values
            
            ax4.set_xticks(range(len(merchants)))
            ax4.set_xticklabels([m[:15] + '...' if len(m) > 15 else m for m in merchants], rotation=45)
            ax4.set_title('Transaction Categories by Merchant')
            ax4.set_ylabel('Transaction Count')
            ax4.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
        
        self.fig_detailed.suptitle('Merchant Analysis', fontsize=16, fontweight='bold')
        plt.tight_layout()
    
    def update_data_table(self):
        """Update the transaction data table"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if self.filtered_df is None or len(self.filtered_df) == 0:
            return
        
        # Get display settings
        try:
            show_count = int(self.show_count_var.get()) if self.show_count_var.get() != "All" else len(self.filtered_df)
        except:
            show_count = 100
        
        sort_by = self.sort_by_var.get()
        
        # Sort data
        display_df = self.filtered_df.copy()
        
        try:
            if sort_by in display_df.columns:
                display_df = display_df.sort_values(sort_by, ascending=False)
        except:
            display_df = display_df.sort_values('DateTime', ascending=False)
        
        # Limit rows
        display_df = display_df.head(show_count)
        
        # Insert data into treeview
        for _, row in display_df.iterrows():
            try:
                date_str = row['DateTime'].strftime('%Y-%m-%d %H:%M') if pd.notna(row['DateTime']) else 'N/A'
                details = str(row['Transaction Details'])[:50] + "..." if len(str(row['Transaction Details'])) > 50 else str(row['Transaction Details'])
                category = row['Category'] if pd.notna(row['Category']) else 'N/A'
                amount = f"₹{row['Amount']:,.2f}"
                trans_type = row['Type'] if pd.notna(row['Type']) else 'N/A'
                
                # Color coding
                tags = ('credit',) if row['Amount'] > 0 else ('debit',)
                
                self.tree.insert('', 'end', values=(date_str, details, category, amount, trans_type), tags=tags)
            except Exception as e:
                continue  # Skip problematic rows
        
        # Configure tag colors
        self.tree.tag_configure('credit', foreground='green')
        self.tree.tag_configure('debit', foreground='red')
    
    def export_csv(self):
        """Export filtered data to CSV"""
        if self.filtered_df is None or len(self.filtered_df) == 0:
            messagebox.showwarning("Warning", "No data to export!")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Export Transactions to CSV"
            )
            
            if filename:
                # Prepare export data
                export_df = self.filtered_df.copy()
                
                # Format DateTime for export
                if 'DateTime' in export_df.columns:
                    export_df['DateTime'] = export_df['DateTime'].dt.strftime('%Y-%m-%d %H:%M:%S')
                
                # Select relevant columns
                export_columns = ['DateTime', 'Transaction Details', 'Category', 'Amount', 'Type']
                export_columns = [col for col in export_columns if col in export_df.columns]
                
                export_df[export_columns].to_csv(filename, index=False)
                
                messagebox.showinfo("Export Successful", f"Data exported to {filename}\n{len(export_df)} transactions exported.")
                self.update_status(f"Exported {len(export_df)} transactions to CSV")
        
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data:\n{str(e)}")
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        if self.filtered_df is None or len(self.filtered_df) == 0:
            messagebox.showwarning("Warning", "No data to generate report!")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Save Analysis Report"
            )
            
            if filename:
                self.update_status("Generating report...")
                self.progress.start(10)
                
                report = self.create_analysis_report()
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(report)
                
                messagebox.showinfo("Report Generated", f"Analysis report saved to {filename}")
                self.update_status("Report generated successfully")
        
        except Exception as e:
            messagebox.showerror("Report Error", f"Failed to generate report:\n{str(e)}")
        
        finally:
            self.progress.stop()
    
    def create_analysis_report(self):
        """Create comprehensive analysis report"""
        df = self.filtered_df
        
        # Calculate statistics
        debit_data = df[df['Amount'] < 0]
        credit_data = df[df['Amount'] > 0]
        
        total_spent = debit_data['Amount'].abs().sum() if len(debit_data) > 0 else 0
        total_received = credit_data['Amount'].sum() if len(credit_data) > 0 else 0
        net_amount = total_received - total_spent
        
        report = f"""
COMPREHENSIVE TRANSACTION ANALYSIS REPORT
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}

OVERVIEW
{'='*60}
Total Transactions Analyzed: {len(df):,}
Date Range: {df['DateTime'].min().strftime('%Y-%m-%d')} to {df['DateTime'].max().strftime('%Y-%m-%d')}
Analysis Period: {(df['DateTime'].max() - df['DateTime'].min()).days} days

FINANCIAL SUMMARY
{'='*60}
Total Money Spent: ₹{total_spent:,.2f}
Total Money Received: ₹{total_received:,.2f}
Net Cash Flow: ₹{net_amount:,.2f}
Average Transaction Amount: ₹{df['Amount'].mean():,.2f}
Median Transaction Amount: ₹{df['Amount'].median():,.2f}

Largest Single Expense: ₹{debit_data['Amount'].abs().max():,.2f} if len(debit_data) > 0 else 0
Largest Single Income: ₹{credit_data['Amount'].max():,.2f} if len(credit_data) > 0 else 0

SPENDING ANALYSIS
{'='*60}
"""
        
        # Top spending categories
        if len(debit_data) > 0:
            top_categories = debit_data.groupby('Category')['AbsAmount'].sum().sort_values(ascending=False).head(10)
            report += "Top Spending Categories:\n"
            for i, (category, amount) in enumerate(top_categories.items(), 1):
                percentage = (amount / total_spent) * 100
                report += f"{i:2d}. {category:<30} ₹{amount:>10,.2f} ({percentage:5.1f}%)\n"
            
            report += f"\n"
        
        # Top merchants
        if len(debit_data) > 0:
            top_merchants = debit_data.groupby('Transaction Details')['AbsAmount'].sum().sort_values(ascending=False).head(10)
            report += "Top Merchants by Spending:\n"
            for i, (merchant, amount) in enumerate(top_merchants.items(), 1):
                report += f"{i:2d}. {merchant:<40} ₹{amount:>10,.2f}\n"
            
            report += f"\n"
        
        # Monthly breakdown
        if len(df) > 0:
            monthly_summary = df.groupby('Month').agg({
                'Amount': ['count', lambda x: abs(x[x < 0].sum()), lambda x: x[x > 0].sum()]
            })
            monthly_summary.columns = ['Count', 'Spent', 'Received']
            
            report += "Monthly Breakdown:\n"
            report += f"{'Month':<10} {'Transactions':<12} {'Spent':<15} {'Received':<15} {'Net':<15}\n"
            report += f"{'-'*67}\n"
            
            for month in monthly_summary.index:
                count = int(monthly_summary.loc[month, 'Count'])
                spent = monthly_summary.loc[month, 'Spent']
                received = monthly_summary.loc[month, 'Received']
                net = received - spent
                
                report += f"{month:<10} {count:<12} ₹{spent:<14,.0f} ₹{received:<14,.0f} ₹{net:<14,.0f}\n"
            
            report += f"\n"
        
        # Day of week analysis
        if len(debit_data) > 0:
            dow_spending = debit_data.groupby('DayOfWeek')['AbsAmount'].sum().sort_values(ascending=False)
            report += "Spending by Day of Week:\n"
            for day, amount in dow_spending.items():
                report += f"{day:<10} ₹{amount:>10,.2f}\n"
            
            report += f"\n"
        
        # Transaction frequency analysis
        report += "TRANSACTION PATTERNS\n"
        report += "=" * 60 + "\n"
        
        report += f"Average transactions per day: {len(df) / max((df['DateTime'].max() - df['DateTime'].min()).days, 1):.1f}\n"
        report += f"Most active day: {df['DayOfWeek'].mode().iloc[0] if len(df['DayOfWeek'].mode()) > 0 else 'N/A'}\n"
        
        if len(debit_data) > 0:
            report += f"Most expensive category: {debit_data.groupby('Category')['AbsAmount'].sum().idxmax()}\n"
            report += f"Most frequent spending category: {debit_data['Category'].mode().iloc[0] if len(debit_data['Category'].mode()) > 0 else 'N/A'}\n"
        
        report += f"\nREPORT END\n"
        report += f"Generated by Bank Transaction Analyzer v1.0\n"
        
        return report
    
    def save_categories(self):
        """Save categories from text widget"""
        try:
            content = self.category_text.get(1.0, tk.END).strip()
            new_categories = {}
            current_category = None
            
            for line in content.split('\n'):
                line = line.strip()
                if line.endswith(':'):
                    current_category = line[:-1]
                    new_categories[current_category] = []
                elif line and current_category:
                    # Parse keywords (comma separated)
                    keywords = [kw.strip() for kw in line.split(',') if kw.strip()]
                    new_categories[current_category].extend(keywords)
            
            if new_categories:
                self.category_keywords = new_categories
                messagebox.showinfo("Success", "Categories saved successfully!")
                
                # Re-categorize existing data if available
                if self.df is not None:
                    self.df['Category'] = self.df['Transaction Details'].apply(self.categorize_transaction)
                    self.filtered_df = self.df.copy()
                    self.update_all_displays()
            else:
                messagebox.showwarning("Warning", "No valid categories found!")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save categories:\n{str(e)}")
    
    def reset_categories(self):
        """Reset categories to default"""
        self.category_keywords = {
            "🥘 Food & Dining": ["swiggy", "zomato", "restaurant", "hotel", "cafe", "food"],
            "🛒 Groceries & Essentials": ["bigbasket", "dmart", "grocery", "kirana"],
            "🏥 Medical & Healthcare": ["pharmacy", "hospital", "medical", "doctor"],
            "🧾 Bills & Utilities": ["jio", "airtel", "electricity", "bill", "recharge"],
            "🛍 Shopping": ["amazon", "flipkart", "shopping", "myntra"],
            "💵 Transfers & P2P": ["sent to", "transfer", "pay to"],
            "💰 Money Received": ["salary", "credited", "refund", "cashback"],
            "🚖 Transport & Travel": ["uber", "ola", "petrol", "taxi"],
            "🎬 Entertainment": ["netflix", "movie", "cinema"],
            "🏦 Banking & Fees": ["atm", "bank charge", "fee"]
        }
        self.update_category_text()
        messagebox.showinfo("Reset", "Categories reset to default values!")
    
    def import_categories(self):
        """Import categories from JSON file"""
        try:
            filename = filedialog.askopenfilename(
                title="Import Categories",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if filename:
                with open(filename, 'r', encoding='utf-8') as f:
                    imported_categories = json.load(f)
                
                self.category_keywords = imported_categories
                self.update_category_text()
                messagebox.showinfo("Import Successful", "Categories imported successfully!")
        
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import categories:\n{str(e)}")
    
    def export_categories(self):
        """Export categories to JSON file"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Export Categories"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.category_keywords, f, indent=2, ensure_ascii=False)
                
                messagebox.showinfo("Export Successful", f"Categories exported to {filename}")
        
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export categories:\n{str(e)}")
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

def main():
    """Main function to run the application"""
    try:
        # Create and run the application
        app = TransactionAnalyzer()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
