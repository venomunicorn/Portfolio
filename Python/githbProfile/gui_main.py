"""
GitHub Profile Picture Downloader GUI
Built with Tkinter - Part of 21APEX Challenge
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import urllib.request
import urllib.error
import json
import os
import re
import threading
from io import BytesIO

# Try to import PIL for image display
try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

class GitHubProfileGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GitHub Avatar Downloader")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        self.root.configure(bg='#0d1117')
        
        # Colors - GitHub dark theme
        self.colors = {
            'bg': '#0d1117',
            'card': '#161b22',
            'primary': '#238636',
            'secondary': '#21262d',
            'accent': '#58a6ff',
            'text': '#c9d1d9',
            'text_dim': '#8b949e'
        }
        
        # State
        self.avatar_url = None
        self.avatar_image = None
        self.username = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(
            main_frame,
            text="🐙 GitHub Avatar Downloader",
            font=('Segoe UI', 22, 'bold'),
            fg=self.colors['accent'],
            bg=self.colors['bg']
        ).pack(pady=(0, 5))
        
        tk.Label(
            main_frame,
            text="Download profile pictures from GitHub",
            font=('Segoe UI', 10),
            fg=self.colors['text_dim'],
            bg=self.colors['bg']
        ).pack(pady=(0, 20))
        
        # Input card
        input_card = tk.Frame(main_frame, bg=self.colors['card'])
        input_card.pack(fill='x', pady=10, ipady=15)
        
        tk.Label(
            input_card,
            text="Enter GitHub Username or URL:",
            font=('Segoe UI', 11),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(pady=(10, 5))
        
        input_frame = tk.Frame(input_card, bg=self.colors['card'])
        input_frame.pack(pady=5)
        
        self.username_entry = tk.Entry(
            input_frame,
            font=('Segoe UI', 13),
            bg=self.colors['secondary'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            relief='flat',
            width=30
        )
        self.username_entry.pack(side='left', padx=5, ipady=10)
        self.username_entry.insert(0, "octocat")
        self.username_entry.bind('<Return>', lambda e: self.fetch_avatar())
        
        self.fetch_btn = tk.Button(
            input_frame,
            text="🔍 Fetch",
            font=('Segoe UI', 11, 'bold'),
            fg='white',
            bg=self.colors['primary'],
            activebackground=self.colors['accent'],
            relief='flat',
            padx=15,
            pady=8,
            command=self.fetch_avatar
        )
        self.fetch_btn.pack(side='left', padx=5)
        
        # Example usernames
        example_frame = tk.Frame(input_card, bg=self.colors['card'])
        example_frame.pack(pady=10)
        
        tk.Label(
            example_frame,
            text="Try:",
            font=('Segoe UI', 9),
            fg=self.colors['text_dim'],
            bg=self.colors['card']
        ).pack(side='left', padx=5)
        
        examples = ['octocat', 'torvalds', 'gvanrossum', 'defunkt']
        for user in examples:
            btn = tk.Button(
                example_frame,
                text=user,
                font=('Segoe UI', 9),
                fg=self.colors['accent'],
                bg=self.colors['secondary'],
                relief='flat',
                padx=8,
                pady=2,
                command=lambda u=user: self.try_user(u)
            )
            btn.pack(side='left', padx=2)
        
        # Status
        self.status_label = tk.Label(
            input_card,
            text="Enter a username and click Fetch",
            font=('Segoe UI', 10),
            fg=self.colors['text_dim'],
            bg=self.colors['card']
        )
        self.status_label.pack(pady=(5, 10))
        
        # Avatar display card
        avatar_card = tk.Frame(main_frame, bg=self.colors['card'])
        avatar_card.pack(fill='both', expand=True, pady=10)
        
        tk.Label(
            avatar_card,
            text="👤 Profile Picture:",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(pady=(15, 10))
        
        # Avatar canvas
        self.avatar_canvas = tk.Canvas(
            avatar_card,
            width=200,
            height=200,
            bg=self.colors['secondary'],
            highlightthickness=2,
            highlightbackground=self.colors['accent']
        )
        self.avatar_canvas.pack(pady=10)
        
        # Placeholder
        self.avatar_canvas.create_text(
            100, 100,
            text="Avatar will\nappear here",
            font=('Segoe UI', 12),
            fill='#444444',
            justify='center'
        )
        
        # User info
        self.info_label = tk.Label(
            avatar_card,
            text="",
            font=('Segoe UI', 11),
            fg=self.colors['text'],
            bg=self.colors['card']
        )
        self.info_label.pack(pady=5)
        
        # Download button
        self.download_btn = tk.Button(
            avatar_card,
            text="💾 Download Avatar",
            font=('Segoe UI', 11, 'bold'),
            fg='white',
            bg=self.colors['primary'],
            relief='flat',
            padx=20,
            pady=10,
            state='disabled',
            command=self.download_avatar
        )
        self.download_btn.pack(pady=15)
    
    def try_user(self, username):
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, username)
        self.fetch_avatar()
    
    def extract_username(self, input_str):
        input_str = input_str.strip()
        
        if input_str.startswith(('http://', 'https://')):
            if 'github.com' in input_str:
                parts = input_str.split('github.com/')
                if len(parts) > 1:
                    username = parts[1].strip('/').split('/')[0]
                    return username
            raise ValueError("Invalid GitHub URL")
        
        if re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-])*[a-zA-Z0-9]$|^[a-zA-Z0-9]$', input_str):
            return input_str
        raise ValueError("Invalid username format")
    
    def fetch_avatar(self):
        input_str = self.username_entry.get().strip()
        if not input_str:
            messagebox.showwarning("Warning", "Please enter a username!")
            return
        
        try:
            self.username = self.extract_username(input_str)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        
        self.fetch_btn.config(state='disabled', text="Fetching...")
        self.status_label.config(text=f"Fetching data for {self.username}...", fg=self.colors['accent'])
        self.root.update()
        
        # Fetch in thread
        threading.Thread(target=self._fetch_user_data, daemon=True).start()
    
    def _fetch_user_data(self):
        try:
            api_url = f"https://api.github.com/users/{self.username}"
            req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            self.avatar_url = data.get('avatar_url')
            name = data.get('name', self.username)
            bio = data.get('bio', 'No bio')
            followers = data.get('followers', 0)
            
            self.root.after(0, self._display_result, name, bio, followers)
            
            # Download avatar image for display
            if HAS_PIL and self.avatar_url:
                self._download_and_display_avatar()
            
        except Exception as e:
            self.root.after(0, self._show_error, str(e))
    
    def _display_result(self, name, bio, followers):
        self.status_label.config(text=f"✓ Found user: {self.username}", fg=self.colors['primary'])
        self.info_label.config(text=f"{name}\n{followers} followers")
        self.download_btn.config(state='normal')
        self.fetch_btn.config(state='normal', text="🔍 Fetch")
    
    def _download_and_display_avatar(self):
        try:
            req = urllib.request.Request(self.avatar_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                image_data = response.read()
            
            image = Image.open(BytesIO(image_data))
            image = image.resize((196, 196), Image.Resampling.LANCZOS)
            
            self.avatar_image = ImageTk.PhotoImage(image)
            
            self.root.after(0, self._show_avatar)
        except Exception as e:
            print(f"Could not display avatar: {e}")
    
    def _show_avatar(self):
        self.avatar_canvas.delete('all')
        self.avatar_canvas.create_image(100, 100, image=self.avatar_image)
    
    def _show_error(self, error):
        self.status_label.config(text=f"✗ Error: {error[:40]}", fg='#f85149')
        self.fetch_btn.config(state='normal', text="🔍 Fetch")
        messagebox.showerror("Error", f"Failed to fetch user:\n{error}")
    
    def download_avatar(self):
        if not self.avatar_url:
            messagebox.showwarning("Warning", "No avatar to download!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")],
            initialfile=f"{self.username}_avatar.png"
        )
        
        if file_path:
            try:
                req = urllib.request.Request(self.avatar_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=30) as response:
                    with open(file_path, 'wb') as f:
                        f.write(response.read())
                
                messagebox.showinfo("Success", f"Avatar saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Download failed: {e}")
    
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
    app = GitHubProfileGUI()
    app.run()
