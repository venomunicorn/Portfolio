"""
Web Scraper GUI Application
Built with Tkinter - Part of 21APEX Challenge
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import urllib.request
import urllib.error
import re
import csv
import threading

class WebScraperGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Web Scraper")
        self.root.geometry("650x700")
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
            'text_dim': '#8892b0',
            'link': '#64ffda'
        }
        
        self.scraped_links = []
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(
            main_frame,
            text="🕷️ Web Scraper",
            font=('Segoe UI', 26, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['bg']
        ).pack(pady=(0, 5))
        
        tk.Label(
            main_frame,
            text="Extract links and data from web pages",
            font=('Segoe UI', 11),
            fg=self.colors['text_dim'],
            bg=self.colors['bg']
        ).pack(pady=(0, 15))
        
        # URL Input card
        input_card = tk.Frame(main_frame, bg=self.colors['card'])
        input_card.pack(fill='x', pady=10, ipady=15)
        
        tk.Label(
            input_card,
            text="Enter URL to Scrape:",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(pady=(15, 5))
        
        input_frame = tk.Frame(input_card, bg=self.colors['card'])
        input_frame.pack(pady=5)
        
        self.url_entry = tk.Entry(
            input_frame,
            font=('Segoe UI', 12),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            relief='flat',
            width=45
        )
        self.url_entry.pack(side='left', padx=5, ipady=10)
        self.url_entry.insert(0, "https://example.com")
        self.url_entry.bind('<Return>', lambda e: self.start_scrape())
        
        self.scrape_btn = tk.Button(
            input_frame,
            text="🔍 Scrape",
            font=('Segoe UI', 11, 'bold'),
            fg='white',
            bg=self.colors['primary'],
            activebackground=self.colors['success'],
            relief='flat',
            padx=15,
            pady=8,
            command=self.start_scrape
        )
        self.scrape_btn.pack(side='left', padx=5)
        
        # Demo button
        tk.Button(
            input_card,
            text="🧪 Run Demo Mode",
            font=('Segoe UI', 10),
            fg=self.colors['bg'],
            bg=self.colors['success'],
            activebackground=self.colors['primary'],
            relief='flat',
            padx=15,
            pady=5,
            command=self.run_demo
        ).pack(pady=10)
        
        # Status
        self.status_label = tk.Label(
            input_card,
            text="Ready to scrape",
            font=('Segoe UI', 10),
            fg=self.colors['text_dim'],
            bg=self.colors['card']
        )
        self.status_label.pack(pady=(0, 10))
        
        # Results card
        results_card = tk.Frame(main_frame, bg=self.colors['card'])
        results_card.pack(fill='both', expand=True, pady=10)
        
        # Page info
        info_frame = tk.Frame(results_card, bg=self.colors['card'])
        info_frame.pack(fill='x', padx=15, pady=(15, 5))
        
        tk.Label(
            info_frame,
            text="Page Title:",
            font=('Segoe UI', 10),
            fg=self.colors['text_dim'],
            bg=self.colors['card']
        ).pack(side='left')
        
        self.title_label = tk.Label(
            info_frame,
            text="--",
            font=('Segoe UI', 10, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['card']
        )
        self.title_label.pack(side='left', padx=5)
        
        # Links count
        count_frame = tk.Frame(results_card, bg=self.colors['card'])
        count_frame.pack(fill='x', padx=15, pady=5)
        
        tk.Label(
            count_frame,
            text="Links Found:",
            font=('Segoe UI', 10),
            fg=self.colors['text_dim'],
            bg=self.colors['card']
        ).pack(side='left')
        
        self.count_label = tk.Label(
            count_frame,
            text="0",
            font=('Segoe UI', 10, 'bold'),
            fg=self.colors['success'],
            bg=self.colors['card']
        )
        self.count_label.pack(side='left', padx=5)
        
        # Results list
        tk.Label(
            results_card,
            text="📋 Extracted Links:",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(anchor='w', padx=15, pady=(10, 5))
        
        # Listbox with scrollbar
        list_frame = tk.Frame(results_card, bg=self.colors['card'])
        list_frame.pack(fill='both', expand=True, padx=15, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.links_listbox = tk.Listbox(
            list_frame,
            font=('Consolas', 10),
            bg=self.colors['bg'],
            fg=self.colors['link'],
            selectbackground=self.colors['primary'],
            relief='flat',
            yscrollcommand=scrollbar.set
        )
        self.links_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.links_listbox.yview)
        
        # Action buttons
        action_frame = tk.Frame(results_card, bg=self.colors['card'])
        action_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Button(
            action_frame,
            text="💾 Export to CSV",
            font=('Segoe UI', 10, 'bold'),
            fg='white',
            bg=self.colors['secondary'],
            relief='flat',
            padx=15,
            pady=8,
            command=self.export_csv
        ).pack(side='left', padx=5)
        
        tk.Button(
            action_frame,
            text="📋 Copy Selected",
            font=('Segoe UI', 10, 'bold'),
            fg='white',
            bg=self.colors['secondary'],
            relief='flat',
            padx=15,
            pady=8,
            command=self.copy_selected
        ).pack(side='left', padx=5)
        
        tk.Button(
            action_frame,
            text="🗑️ Clear",
            font=('Segoe UI', 10, 'bold'),
            fg='white',
            bg='#f38ba8',
            relief='flat',
            padx=15,
            pady=8,
            command=self.clear_results
        ).pack(side='left', padx=5)
    
    def start_scrape(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a URL!")
            return
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, url)
        
        self.scrape_btn.config(state='disabled', text="Scraping...")
        self.status_label.config(text=f"Fetching {url}...", fg=self.colors['primary'])
        self.root.update()
        
        # Run in thread
        thread = threading.Thread(target=self.scrape_url, args=(url,))
        thread.daemon = True
        thread.start()
    
    def scrape_url(self, url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8', errors='ignore')
            
            # Extract title
            title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
            title = title_match.group(1).strip() if title_match else "No Title"
            
            # Extract links
            link_pattern = r'href=["\']([^"\']+)["\']'
            all_links = re.findall(link_pattern, html)
            
            # Filter to http/https links
            links = list(set([l for l in all_links if l.startswith(('http://', 'https://'))]))
            
            self.root.after(0, self.display_results, title, links, url)
            
        except Exception as e:
            self.root.after(0, self.show_error, str(e))
    
    def display_results(self, title, links, source):
        self.scraped_links = [(source, link) for link in links]
        
        self.title_label.config(text=title[:50] + "..." if len(title) > 50 else title)
        self.count_label.config(text=str(len(links)))
        
        self.links_listbox.delete(0, tk.END)
        for link in links:
            self.links_listbox.insert(tk.END, link)
        
        self.status_label.config(text=f"✓ Successfully scraped {len(links)} links", fg=self.colors['success'])
        self.scrape_btn.config(state='normal', text="🔍 Scrape")
    
    def show_error(self, error):
        self.status_label.config(text=f"✗ Error: {error[:50]}", fg=self.colors['primary'])
        self.scrape_btn.config(state='normal', text="🔍 Scrape")
        messagebox.showerror("Error", f"Failed to scrape:\n{error}")
    
    def run_demo(self):
        """Run with simulated HTML content"""
        demo_html = """
        <html>
            <head><title>Demo Page - Web Scraper Test</title></head>
            <body>
                <a href="https://www.google.com">Google</a>
                <a href="https://www.python.org">Python</a>
                <a href="https://github.com">GitHub</a>
                <a href="https://stackoverflow.com">Stack Overflow</a>
                <a href="https://www.wikipedia.org">Wikipedia</a>
                <a href="https://www.reddit.com">Reddit</a>
                <a href="https://www.youtube.com">YouTube</a>
                <a href="https://example.com/page1">Example Page 1</a>
            </body>
        </html>
        """
        
        # Extract from demo
        title_match = re.search(r'<title>(.*?)</title>', demo_html)
        title = title_match.group(1) if title_match else "Demo"
        
        link_pattern = r'href=["\']([^"\']+)["\']'
        links = re.findall(link_pattern, demo_html)
        links = [l for l in links if l.startswith('http')]
        
        self.display_results(title, links, "Demo Mode")
        self.status_label.config(text="✓ Demo mode - showing sample links", fg=self.colors['success'])
    
    def export_csv(self):
        if not self.scraped_links:
            messagebox.showwarning("Warning", "No links to export!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="scraped_links.csv"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Source', 'Link'])
                    writer.writerows(self.scraped_links)
                messagebox.showinfo("Success", f"Exported {len(self.scraped_links)} links to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")
    
    def copy_selected(self):
        selection = self.links_listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Please select a link to copy")
            return
        
        link = self.links_listbox.get(selection[0])
        self.root.clipboard_clear()
        self.root.clipboard_append(link)
        self.status_label.config(text="✓ Link copied to clipboard!", fg=self.colors['success'])
    
    def clear_results(self):
        self.links_listbox.delete(0, tk.END)
        self.scraped_links = []
        self.title_label.config(text="--")
        self.count_label.config(text="0")
        self.status_label.config(text="Results cleared", fg=self.colors['text_dim'])
    
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
    app = WebScraperGUI()
    app.run()
