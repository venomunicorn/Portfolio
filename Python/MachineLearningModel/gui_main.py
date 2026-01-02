"""
Machine Learning Demo GUI
Built with Tkinter - Part of 21APEX Challenge
Linear Regression for House Price Prediction
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import math

# Try to import ML libraries
try:
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error, r2_score
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

class MachineLearningGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ML Demo - House Price Prediction")
        self.root.geometry("700x700")
        self.root.resizable(False, False)
        self.root.configure(bg='#1a1a2e')
        
        # Colors
        self.colors = {
            'bg': '#1a1a2e',
            'card': '#16213e',
            'primary': '#e94560',
            'secondary': '#0f3460',
            'success': '#00d9a5',
            'text': '#ffffff',
            'text_dim': '#7f8c8d',
            'data': '#4cc9f0'
        }
        
        # Model state
        self.model = None
        self.coefficient = None
        self.intercept = None
        self.r2_score = None
        self.trained = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(
            main_frame,
            text="🤖 Machine Learning Demo",
            font=('Segoe UI', 26, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['bg']
        ).pack(pady=(0, 5))
        
        tk.Label(
            main_frame,
            text="House Price Prediction using Linear Regression",
            font=('Segoe UI', 11),
            fg=self.colors['text_dim'],
            bg=self.colors['bg']
        ).pack(pady=(0, 10))
        
        # Status
        status_text = "sklearn Ready" if HAS_SKLEARN else "Simulation Mode (pip install scikit-learn)"
        status_color = self.colors['success'] if HAS_SKLEARN else self.colors['data']
        
        tk.Label(
            main_frame,
            text=f"● {status_text}",
            font=('Segoe UI', 10),
            fg=status_color,
            bg=self.colors['bg']
        ).pack(pady=(0, 15))
        
        # Model info card
        model_card = tk.Frame(main_frame, bg=self.colors['card'])
        model_card.pack(fill='x', pady=10, ipady=15)
        
        tk.Label(
            model_card,
            text="📊 Model: Price = (Coefficient × Size) + Base Price",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(pady=(10, 15))
        
        # Stats
        stats_frame = tk.Frame(model_card, bg=self.colors['card'])
        stats_frame.pack(fill='x', padx=20)
        
        # Coefficient
        stat1 = tk.Frame(stats_frame, bg=self.colors['card'])
        stat1.pack(side='left', expand=True)
        tk.Label(stat1, text="Coefficient", font=('Segoe UI', 10),
                fg=self.colors['text_dim'], bg=self.colors['card']).pack()
        self.coef_label = tk.Label(stat1, text="--", font=('Segoe UI', 18, 'bold'),
                fg=self.colors['primary'], bg=self.colors['card'])
        self.coef_label.pack()
        tk.Label(stat1, text="$/sqft", font=('Segoe UI', 9),
                fg=self.colors['text_dim'], bg=self.colors['card']).pack()
        
        # Intercept
        stat2 = tk.Frame(stats_frame, bg=self.colors['card'])
        stat2.pack(side='left', expand=True)
        tk.Label(stat2, text="Base Price", font=('Segoe UI', 10),
                fg=self.colors['text_dim'], bg=self.colors['card']).pack()
        self.intercept_label = tk.Label(stat2, text="--", font=('Segoe UI', 18, 'bold'),
                fg=self.colors['success'], bg=self.colors['card'])
        self.intercept_label.pack()
        tk.Label(stat2, text="$", font=('Segoe UI', 9),
                fg=self.colors['text_dim'], bg=self.colors['card']).pack()
        
        # R2 Score
        stat3 = tk.Frame(stats_frame, bg=self.colors['card'])
        stat3.pack(side='left', expand=True)
        tk.Label(stat3, text="R² Score", font=('Segoe UI', 10),
                fg=self.colors['text_dim'], bg=self.colors['card']).pack()
        self.r2_label = tk.Label(stat3, text="--", font=('Segoe UI', 18, 'bold'),
                fg=self.colors['data'], bg=self.colors['card'])
        self.r2_label.pack()
        tk.Label(stat3, text="accuracy", font=('Segoe UI', 9),
                fg=self.colors['text_dim'], bg=self.colors['card']).pack()
        
        # Train button
        tk.Button(
            model_card,
            text="🚀 Train Model",
            font=('Segoe UI', 12, 'bold'),
            fg='white',
            bg=self.colors['primary'],
            relief='flat',
            padx=30,
            pady=10,
            command=self.train_model
        ).pack(pady=15)
        
        # Training log
        self.log_label = tk.Label(
            model_card,
            text="Click 'Train Model' to start",
            font=('Segoe UI', 10),
            fg=self.colors['text_dim'],
            bg=self.colors['card']
        )
        self.log_label.pack(pady=(0, 10))
        
        # Prediction card
        pred_card = tk.Frame(main_frame, bg=self.colors['card'])
        pred_card.pack(fill='x', pady=10, ipady=15)
        
        tk.Label(
            pred_card,
            text="🏠 Predict House Price",
            font=('Segoe UI', 14, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(pady=(10, 15))
        
        # Input
        input_frame = tk.Frame(pred_card, bg=self.colors['card'])
        input_frame.pack()
        
        tk.Label(
            input_frame,
            text="House Size (sq ft):",
            font=('Segoe UI', 11),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(side='left', padx=5)
        
        self.size_entry = tk.Entry(
            input_frame,
            font=('Segoe UI', 14),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            relief='flat',
            width=10,
            justify='center'
        )
        self.size_entry.pack(side='left', padx=10, ipady=8)
        self.size_entry.insert(0, "1500")
        self.size_entry.bind('<Return>', lambda e: self.predict_price())
        
        tk.Button(
            input_frame,
            text="Predict",
            font=('Segoe UI', 11, 'bold'),
            fg='white',
            bg=self.colors['success'],
            relief='flat',
            padx=20,
            pady=8,
            command=self.predict_price
        ).pack(side='left', padx=10)
        
        # Prediction result
        self.result_label = tk.Label(
            pred_card,
            text="",
            font=('Segoe UI', 24, 'bold'),
            fg=self.colors['success'],
            bg=self.colors['card']
        )
        self.result_label.pack(pady=15)
        
        # Sample predictions
        sample_frame = tk.Frame(main_frame, bg=self.colors['card'])
        sample_frame.pack(fill='both', expand=True, pady=10)
        
        tk.Label(
            sample_frame,
            text="📋 Quick Predictions",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(pady=(10, 10))
        
        # Quick prediction buttons
        sizes_frame = tk.Frame(sample_frame, bg=self.colors['card'])
        sizes_frame.pack(pady=5)
        
        sizes = [500, 1000, 1500, 2000, 2500, 3000]
        for size in sizes:
            btn = tk.Button(
                sizes_frame,
                text=f"{size} sqft",
                font=('Segoe UI', 9),
                fg='white',
                bg=self.colors['secondary'],
                relief='flat',
                padx=10,
                pady=5,
                command=lambda s=size: self.quick_predict(s)
            )
            btn.pack(side='left', padx=3)
        
        # Results display
        self.quick_result = tk.Label(
            sample_frame,
            text="Train model first, then click a size to predict",
            font=('Segoe UI', 11),
            fg=self.colors['text_dim'],
            bg=self.colors['card']
        )
        self.quick_result.pack(pady=10)
    
    def train_model(self):
        self.log_label.config(text="Generating synthetic data...")
        self.root.update()
        
        if HAS_SKLEARN:
            # Use real sklearn
            np.random.seed(42)
            X = 2000 * np.random.rand(100, 1)
            y = 300 * X + 50000 + np.random.randn(100, 1) * 50000
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            self.log_label.config(text="Training Linear Regression model...")
            self.root.update()
            
            self.model = LinearRegression()
            self.model.fit(X_train, y_train)
            
            y_pred = self.model.predict(X_test)
            self.r2_score = r2_score(y_test, y_pred)
            
            self.coefficient = self.model.coef_[0][0]
            self.intercept = self.model.intercept_[0]
        else:
            # Simulation mode
            self.coefficient = 300 + random.uniform(-20, 20)
            self.intercept = 50000 + random.uniform(-5000, 5000)
            self.r2_score = 0.85 + random.uniform(0, 0.1)
        
        self.trained = True
        
        # Update display
        self.coef_label.config(text=f"${self.coefficient:.2f}")
        self.intercept_label.config(text=f"${self.intercept:,.0f}")
        self.r2_label.config(text=f"{self.r2_score:.2f}")
        
        self.log_label.config(text="✓ Model trained successfully!", fg=self.colors['success'])
    
    def predict_price(self):
        if not self.trained:
            messagebox.showwarning("Warning", "Please train the model first!")
            return
        
        try:
            size = float(self.size_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
            return
        
        # Calculate prediction
        if HAS_SKLEARN and self.model:
            import numpy as np
            predicted = self.model.predict([[size]])[0][0]
        else:
            predicted = self.coefficient * size + self.intercept
        
        self.result_label.config(text=f"Predicted Price: ${predicted:,.2f}")
    
    def quick_predict(self, size):
        if not self.trained:
            self.quick_result.config(text="⚠️ Train the model first!", fg=self.colors['primary'])
            return
        
        if HAS_SKLEARN and self.model:
            import numpy as np
            predicted = self.model.predict([[size]])[0][0]
        else:
            predicted = self.coefficient * size + self.intercept
        
        self.quick_result.config(
            text=f"🏠 {size} sq ft → ${predicted:,.2f}",
            fg=self.colors['success']
        )
    
    def run(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.root.mainloop()

if __name__ == "__main__":
    app = MachineLearningGUI()
    app.run()
