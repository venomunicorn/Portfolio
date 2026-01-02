"""
QR Code Generator GUI Application
Built with Tkinter - Part of 21APEX Challenge
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import io
import os

# Try to import qrcode, use simulation if not available
try:
    import qrcode
    HAS_QRCODE = True
except ImportError:
    HAS_QRCODE = False

class QRCodeGeneratorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("QR Code Generator")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        self.root.configure(bg='#1e1e2e')
        
        # Colors
        self.colors = {
            'bg': '#1e1e2e',
            'card': '#313244',
            'primary': '#cba6f7',
            'secondary': '#89b4fa',
            'success': '#a6e3a1',
            'text': '#cdd6f4',
            'text_dim': '#6c7086'
        }
        
        self.qr_image = None
        self.qr_photo = None
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=25, pady=25)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="📱 QR Code Generator",
            font=('Segoe UI', 24, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=(0, 5))
        
        # Status label
        status_text = "Ready" if HAS_QRCODE else "⚠️ Simulation Mode (pip install qrcode[pil])"
        status_color = self.colors['success'] if HAS_QRCODE else self.colors['secondary']
        
        status_label = tk.Label(
            main_frame,
            text=status_text,
            font=('Segoe UI', 10),
            fg=status_color,
            bg=self.colors['bg']
        )
        status_label.pack(pady=(0, 15))
        
        # Input card
        input_card = tk.Frame(main_frame, bg=self.colors['card'])
        input_card.pack(fill='x', pady=10, ipady=15)
        
        tk.Label(
            input_card,
            text="Enter text or URL:",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(pady=(15, 5))
        
        self.text_entry = tk.Entry(
            input_card,
            font=('Segoe UI', 14),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['primary'],
            relief='flat',
            width=35,
            justify='center'
        )
        self.text_entry.pack(padx=20, ipady=10)
        self.text_entry.insert(0, "https://example.com")
        self.text_entry.bind('<Return>', lambda e: self.generate_qr())
        
        # Options frame
        options_frame = tk.Frame(input_card, bg=self.colors['card'])
        options_frame.pack(pady=15)
        
        # Color picker for QR
        tk.Label(
            options_frame,
            text="QR Color:",
            font=('Segoe UI', 10),
            fg=self.colors['text_dim'],
            bg=self.colors['card']
        ).pack(side='left', padx=(0, 5))
        
        self.qr_color_var = tk.StringVar(value='black')
        colors_dropdown = ttk.Combobox(
            options_frame,
            textvariable=self.qr_color_var,
            values=['black', 'darkblue', 'darkgreen', 'purple', 'darkred'],
            state='readonly',
            font=('Segoe UI', 10),
            width=10
        )
        colors_dropdown.pack(side='left', padx=10)
        
        # Generate button
        generate_btn = tk.Button(
            input_card,
            text="✨ Generate QR Code",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['bg'],
            bg=self.colors['primary'],
            activebackground=self.colors['secondary'],
            relief='flat',
            padx=25,
            pady=10,
            command=self.generate_qr
        )
        generate_btn.pack(pady=(10, 15))
        
        # QR Code display card
        display_card = tk.Frame(main_frame, bg=self.colors['card'])
        display_card.pack(fill='both', expand=True, pady=10)
        
        tk.Label(
            display_card,
            text="Generated QR Code:",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(pady=(15, 10))
        
        # QR Code canvas
        self.qr_canvas = tk.Canvas(
            display_card,
            width=250,
            height=250,
            bg='white',
            highlightthickness=2,
            highlightbackground=self.colors['primary']
        )
        self.qr_canvas.pack(pady=10)
        
        # Placeholder text
        self.qr_canvas.create_text(
            125, 125,
            text="QR Code will\nappear here",
            font=('Segoe UI', 14),
            fill='#888888',
            tags='placeholder'
        )
        
        # Action buttons
        action_frame = tk.Frame(display_card, bg=self.colors['card'])
        action_frame.pack(pady=15)
        
        save_btn = tk.Button(
            action_frame,
            text="💾 Save PNG",
            font=('Segoe UI', 10, 'bold'),
            fg='white',
            bg=self.colors['success'],
            activebackground=self.colors['primary'],
            relief='flat',
            padx=20,
            pady=8,
            command=self.save_qr
        )
        save_btn.pack(side='left', padx=5)
        
        clear_btn = tk.Button(
            action_frame,
            text="🗑️ Clear",
            font=('Segoe UI', 10, 'bold'),
            fg='white',
            bg='#f38ba8',
            activebackground=self.colors['primary'],
            relief='flat',
            padx=20,
            pady=8,
            command=self.clear_qr
        )
        clear_btn.pack(side='left', padx=5)
    
    def generate_qr(self):
        text = self.text_entry.get().strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter text or URL to encode!")
            return
        
        if not HAS_QRCODE:
            # Simulation mode - draw placeholder pattern
            self.draw_simulated_qr()
            return
        
        try:
            # Generate QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=2
            )
            qr.add_data(text)
            qr.make(fit=True)
            
            # Create image with selected color
            qr_color = self.qr_color_var.get()
            self.qr_image = qr.make_image(fill_color=qr_color, back_color='white')
            
            # Resize for display
            display_size = (240, 240)
            display_image = self.qr_image.copy()
            display_image = display_image.resize(display_size, Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            self.qr_photo = ImageTk.PhotoImage(display_image)
            
            # Clear canvas and display
            self.qr_canvas.delete('all')
            self.qr_canvas.create_image(125, 125, image=self.qr_photo)
            
            messagebox.showinfo("Success", "QR Code generated successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR Code: {str(e)}")
    
    def draw_simulated_qr(self):
        """Draw a simulated QR code pattern for demo mode"""
        self.qr_canvas.delete('all')
        
        # Draw a simple QR-like pattern
        size = 240
        cell_size = size // 25
        offset = 5
        
        # Position detection patterns (corners)
        def draw_finder(x, y):
            # Outer black square
            self.qr_canvas.create_rectangle(
                x, y, x + 7*cell_size, y + 7*cell_size,
                fill='black', outline='black'
            )
            # Inner white square
            self.qr_canvas.create_rectangle(
                x + cell_size, y + cell_size,
                x + 6*cell_size, y + 6*cell_size,
                fill='white', outline='white'
            )
            # Center black square
            self.qr_canvas.create_rectangle(
                x + 2*cell_size, y + 2*cell_size,
                x + 5*cell_size, y + 5*cell_size,
                fill='black', outline='black'
            )
        
        # Draw finder patterns
        draw_finder(offset, offset)
        draw_finder(size - 7*cell_size - offset, offset)
        draw_finder(offset, size - 7*cell_size - offset)
        
        # Draw some random data pattern
        import random
        for i in range(8, 17):
            for j in range(8, 17):
                if random.random() > 0.5:
                    x = offset + i * cell_size
                    y = offset + j * cell_size
                    self.qr_canvas.create_rectangle(
                        x, y, x + cell_size, y + cell_size,
                        fill='black', outline='black'
                    )
        
        self.qr_image = None
        messagebox.showinfo("Simulation Mode", 
            "This is a simulated QR code.\nInstall 'qrcode' library for real QR codes:\npip install qrcode[pil]")
    
    def save_qr(self):
        if self.qr_image is None:
            messagebox.showwarning("Warning", "No QR Code to save! Generate one first.")
            return
        
        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            initialfile="qrcode.png"
        )
        
        if file_path:
            try:
                self.qr_image.save(file_path)
                messagebox.showinfo("Success", f"QR Code saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def clear_qr(self):
        self.qr_canvas.delete('all')
        self.qr_canvas.create_text(
            125, 125,
            text="QR Code will\nappear here",
            font=('Segoe UI', 14),
            fill='#888888',
            tags='placeholder'
        )
        self.qr_image = None
        self.qr_photo = None
        self.text_entry.delete(0, tk.END)
        self.text_entry.insert(0, "https://example.com")
    
    def run(self):
        # Style configuration
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
    app = QRCodeGeneratorGUI()
    app.run()
