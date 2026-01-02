"""
Blockchain Application GUI
Built with Tkinter - Part of 21APEX Challenge
"""

import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import time
import json
from datetime import datetime

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'data': self.data,
            'nonce': self.nonce
        }, sort_keys=True, default=str)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data, callback=None):
        new_block = Block(
            index=len(self.chain),
            previous_hash=self.get_latest_block().hash,
            timestamp=time.time(),
            data=data
        )
        new_block.hash = self.proof_of_work(new_block, callback)
        self.chain.append(new_block)
        return new_block

    def proof_of_work(self, block, callback=None):
        block.nonce = 0
        computed_hash = block.calculate_hash()
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.calculate_hash()
            if callback and block.nonce % 1000 == 0:
                callback(block.nonce)
        return computed_hash

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True


class BlockchainGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PyChain - Blockchain Demo")
        self.root.geometry("700x750")
        self.root.resizable(False, False)
        self.root.configure(bg='#0f0f1a')
        
        # Colors - Crypto/blockchain theme
        self.colors = {
            'bg': '#0f0f1a',
            'card': '#1a1a2e',
            'primary': '#f7931a',  # Bitcoin orange
            'secondary': '#627eea',  # Ethereum blue
            'success': '#00d395',
            'text': '#ffffff',
            'text_dim': '#8b8b9a',
            'hash': '#4ade80'
        }
        
        self.blockchain = Blockchain(difficulty=2)
        self.setup_ui()
        self.update_chain_display()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        title_frame.pack(fill='x')
        
        tk.Label(
            title_frame,
            text="⛓️ PyChain Blockchain",
            font=('Segoe UI', 26, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['bg']
        ).pack(side='left')
        
        # Validation badge
        self.valid_label = tk.Label(
            title_frame,
            text="✓ Valid Chain",
            font=('Segoe UI', 11, 'bold'),
            fg=self.colors['success'],
            bg=self.colors['bg']
        )
        self.valid_label.pack(side='right')
        
        # Stats bar
        stats_frame = tk.Frame(main_frame, bg=self.colors['card'])
        stats_frame.pack(fill='x', pady=15, ipady=12)
        
        # Chain length
        stat1 = tk.Frame(stats_frame, bg=self.colors['card'])
        stat1.pack(side='left', expand=True)
        tk.Label(stat1, text="Blocks", font=('Segoe UI', 10),
                fg=self.colors['text_dim'], bg=self.colors['card']).pack()
        self.blocks_label = tk.Label(stat1, text="1", font=('Segoe UI', 20, 'bold'),
                fg=self.colors['primary'], bg=self.colors['card'])
        self.blocks_label.pack()
        
        # Difficulty
        stat2 = tk.Frame(stats_frame, bg=self.colors['card'])
        stat2.pack(side='left', expand=True)
        tk.Label(stat2, text="Difficulty", font=('Segoe UI', 10),
                fg=self.colors['text_dim'], bg=self.colors['card']).pack()
        self.diff_label = tk.Label(stat2, text="2", font=('Segoe UI', 20, 'bold'),
                fg=self.colors['secondary'], bg=self.colors['card'])
        self.diff_label.pack()
        
        # Create block section
        create_frame = tk.Frame(main_frame, bg=self.colors['card'])
        create_frame.pack(fill='x', pady=10, ipady=15)
        
        tk.Label(
            create_frame,
            text="⚒️ Mine New Block",
            font=('Segoe UI', 14, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(pady=(10, 5))
        
        # Data input
        input_frame = tk.Frame(create_frame, bg=self.colors['card'])
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Transaction Data:", font=('Segoe UI', 10),
                fg=self.colors['text_dim'], bg=self.colors['card']).pack(side='left', padx=5)
        
        self.data_entry = tk.Entry(
            input_frame,
            font=('Segoe UI', 12),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            relief='flat',
            width=30
        )
        self.data_entry.pack(side='left', padx=5, ipady=8)
        self.data_entry.insert(0, '{"amount": 100}')
        
        # Mine button
        self.mine_btn = tk.Button(
            create_frame,
            text="⛏️ Mine Block",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['bg'],
            bg=self.colors['primary'],
            activebackground=self.colors['secondary'],
            relief='flat',
            padx=25,
            pady=10,
            command=self.mine_block
        )
        self.mine_btn.pack(pady=10)
        
        # Mining status
        self.mining_label = tk.Label(
            create_frame,
            text="",
            font=('Segoe UI', 10),
            fg=self.colors['success'],
            bg=self.colors['card']
        )
        self.mining_label.pack()
        
        # Chain display
        chain_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        chain_frame.pack(fill='both', expand=True, pady=10)
        
        tk.Label(
            chain_frame,
            text="📋 Blockchain Explorer",
            font=('Segoe UI', 14, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['bg']
        ).pack(anchor='w')
        
        # Scrollable chain display
        canvas_frame = tk.Frame(chain_frame, bg=self.colors['bg'])
        canvas_frame.pack(fill='both', expand=True, pady=5)
        
        self.chain_canvas = tk.Canvas(
            canvas_frame,
            bg=self.colors['bg'],
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(canvas_frame, orient='vertical', command=self.chain_canvas.yview)
        
        self.chain_display = tk.Frame(self.chain_canvas, bg=self.colors['bg'])
        
        self.chain_canvas.create_window((0, 0), window=self.chain_display, anchor='nw', width=640)
        self.chain_display.bind('<Configure>', lambda e: self.chain_canvas.configure(scrollregion=self.chain_canvas.bbox('all')))
        self.chain_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.chain_canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Controls
        control_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        control_frame.pack(fill='x', pady=10)
        
        tk.Button(
            control_frame,
            text="✓ Validate Chain",
            font=('Segoe UI', 10, 'bold'),
            fg='white',
            bg=self.colors['success'],
            relief='flat',
            padx=15,
            pady=8,
            command=self.validate_chain
        ).pack(side='left', padx=5)
        
        tk.Button(
            control_frame,
            text="🔄 Reset Chain",
            font=('Segoe UI', 10, 'bold'),
            fg='white',
            bg='#ef4444',
            relief='flat',
            padx=15,
            pady=8,
            command=self.reset_chain
        ).pack(side='left', padx=5)
    
    def mine_block(self):
        data = self.data_entry.get().strip()
        if not data:
            messagebox.showwarning("Warning", "Please enter transaction data!")
            return
        
        self.mine_btn.config(state='disabled', text="Mining...")
        self.mining_label.config(text="Finding valid hash...")
        self.root.update()
        
        start_time = time.time()
        
        new_block = self.blockchain.add_block(data)
        
        elapsed = time.time() - start_time
        self.mining_label.config(
            text=f"✓ Block #{new_block.index} mined! Nonce: {new_block.nonce:,} | Time: {elapsed:.2f}s"
        )
        
        self.mine_btn.config(state='normal', text="⛏️ Mine Block")
        self.update_chain_display()
    
    def update_chain_display(self):
        # Clear existing display
        for widget in self.chain_display.winfo_children():
            widget.destroy()
        
        # Update stats
        self.blocks_label.config(text=str(len(self.blockchain.chain)))
        self.diff_label.config(text=str(self.blockchain.difficulty))
        
        # Display blocks (newest first)
        for block in reversed(self.blockchain.chain):
            block_frame = tk.Frame(self.chain_display, bg=self.colors['card'], relief='flat')
            block_frame.pack(fill='x', pady=5, ipady=10, padx=5)
            
            # Block header
            header_frame = tk.Frame(block_frame, bg=self.colors['card'])
            header_frame.pack(fill='x', padx=15, pady=(10, 5))
            
            tk.Label(
                header_frame,
                text=f"Block #{block.index}",
                font=('Segoe UI', 12, 'bold'),
                fg=self.colors['primary'],
                bg=self.colors['card']
            ).pack(side='left')
            
            timestamp = datetime.fromtimestamp(block.timestamp).strftime('%Y-%m-%d %H:%M:%S')
            tk.Label(
                header_frame,
                text=timestamp,
                font=('Segoe UI', 9),
                fg=self.colors['text_dim'],
                bg=self.colors['card']
            ).pack(side='right')
            
            # Block details
            details_frame = tk.Frame(block_frame, bg=self.colors['card'])
            details_frame.pack(fill='x', padx=15, pady=5)
            
            # Hash
            tk.Label(
                details_frame,
                text=f"Hash: {block.hash[:32]}...",
                font=('Consolas', 9),
                fg=self.colors['hash'],
                bg=self.colors['card']
            ).pack(anchor='w')
            
            # Previous hash
            tk.Label(
                details_frame,
                text=f"Prev: {block.previous_hash[:32]}..." if len(block.previous_hash) > 32 else f"Prev: {block.previous_hash}",
                font=('Consolas', 9),
                fg=self.colors['text_dim'],
                bg=self.colors['card']
            ).pack(anchor='w')
            
            # Data and nonce
            tk.Label(
                details_frame,
                text=f"Data: {block.data} | Nonce: {block.nonce:,}",
                font=('Segoe UI', 9),
                fg=self.colors['text'],
                bg=self.colors['card']
            ).pack(anchor='w')
        
        # Scroll to top
        self.chain_canvas.yview_moveto(0)
    
    def validate_chain(self):
        if self.blockchain.is_chain_valid():
            self.valid_label.config(text="✓ Valid Chain", fg=self.colors['success'])
            messagebox.showinfo("Validation", "✓ Blockchain is valid!\n\nAll blocks are properly linked and hashes are correct.")
        else:
            self.valid_label.config(text="✗ Invalid Chain", fg='#ef4444')
            messagebox.showerror("Validation", "✗ Blockchain is INVALID!\n\nChain has been tampered with.")
    
    def reset_chain(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to reset the blockchain?"):
            self.blockchain = Blockchain(difficulty=2)
            self.mining_label.config(text="")
            self.valid_label.config(text="✓ Valid Chain", fg=self.colors['success'])
            self.update_chain_display()
    
    def run(self):
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.root.mainloop()

if __name__ == "__main__":
    app = BlockchainGUI()
    app.run()
