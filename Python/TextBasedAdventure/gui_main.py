"""
Text-Based Adventure Game GUI Application
Built with Tkinter - Part of 21APEX Challenge
"""

import tkinter as tk
from tkinter import ttk
import time

class TextAdventureGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("The Cave Adventure")
        self.root.geometry("650x700")
        self.root.resizable(False, False)
        self.root.configure(bg='#0d0d0d')
        
        # Colors - Dark fantasy theme
        self.colors = {
            'bg': '#0d0d0d',
            'card': '#1a1a1a',
            'primary': '#d4af37',  # Gold
            'secondary': '#8b4513',  # Brown
            'success': '#228B22',
            'danger': '#8B0000',
            'text': '#f0e6d3',
            'text_dim': '#8b8b7a',
            'action': '#4a6fa5'
        }
        
        # Game state
        self.inventory = []
        self.location = 'start'
        self.game_log = []
        
        # Scene definitions
        self.scenes = {
            'start': {
                'description': "You wake up in a cold, damp cave. It's dark, but you can make out your surroundings.\n\nTo your NORTH, you see a faint light filtering through an opening.\nTo your EAST, you hear a strange humming sound echoing from deeper in the cave.",
                'actions': [
                    ('Go North', 'forest_clearing'),
                    ('Go East', 'machine_room'),
                    ('Check Inventory', 'inventory')
                ]
            },
            'forest_clearing': {
                'description': "You emerge into a moonlit forest clearing. The air is fresh and cool.\n\nA rusty KEY lies on a moss-covered tree stump, glinting in the moonlight.\n\nA path leads back to the CAVE (south) or towards a creepy CASTLE (north) looming in the distance.",
                'actions': [
                    ('Take the Key', 'take_key'),
                    ('Go to Castle', 'castle_gate'),
                    ('Return to Cave', 'start'),
                    ('Check Inventory', 'inventory')
                ]
            },
            'machine_room': {
                'description': "You find a mysterious room carved into the rock. In the center sits a strange, humming metal box covered in gears and switches.\n\nThere's a large red BUTTON on its surface.\n\nThe path back WEST leads to where you woke up.",
                'actions': [
                    ('Push the Button', 'push_button'),
                    ('Go West', 'start'),
                    ('Check Inventory', 'inventory')
                ]
            },
            'castle_gate': {
                'description': "You stand before a massive iron gate, rusted with age but still imposing. Beyond it, the dark castle towers against the night sky.\n\nThe gate is LOCKED with an ancient mechanism.",
                'actions': [
                    ('Try to Open Gate', 'try_gate'),
                    ('Return to Forest', 'forest_clearing'),
                    ('Check Inventory', 'inventory')
                ]
            },
            'castle_hall': {
                'description': "You are in the Castle Hall. Despite the decay, you can see it was once magnificent.\n\nOn a dusty pedestal in the center, a shiny GOLDEN GEAR catches your eye, perfectly preserved.\n\nThe exit leads back SOUTH to the gate.",
                'actions': [
                    ('Take the Golden Gear', 'take_gear'),
                    ('Leave the Hall', 'castle_gate'),
                    ('Check Inventory', 'inventory')
                ]
            }
        }
        
        self.setup_ui()
        self.show_scene('start')
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title with decorative elements
        title_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        title_frame.pack(fill='x')
        
        tk.Label(
            title_frame,
            text="⚔️ THE CAVE ADVENTURE ⚔️",
            font=('Times New Roman', 28, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['bg']
        ).pack()
        
        tk.Label(
            title_frame,
            text="A Text-Based RPG",
            font=('Times New Roman', 12, 'italic'),
            fg=self.colors['text_dim'],
            bg=self.colors['bg']
        ).pack()
        
        # Stats bar
        stats_frame = tk.Frame(main_frame, bg=self.colors['card'])
        stats_frame.pack(fill='x', pady=15, ipady=8)
        
        tk.Label(
            stats_frame,
            text="🎒 Inventory:",
            font=('Segoe UI', 11, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['card']
        ).pack(side='left', padx=15)
        
        self.inventory_label = tk.Label(
            stats_frame,
            text="Empty",
            font=('Segoe UI', 11),
            fg=self.colors['text'],
            bg=self.colors['card']
        )
        self.inventory_label.pack(side='left')
        
        # Location indicator
        tk.Label(
            stats_frame,
            text="📍 Location:",
            font=('Segoe UI', 11, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['card']
        ).pack(side='right', padx=(10, 5))
        
        self.location_label = tk.Label(
            stats_frame,
            text="Cave",
            font=('Segoe UI', 11),
            fg=self.colors['text'],
            bg=self.colors['card']
        )
        self.location_label.pack(side='right', padx=(0, 15))
        
        # Story display
        story_frame = tk.Frame(main_frame, bg=self.colors['card'], relief='flat')
        story_frame.pack(fill='both', expand=True, pady=10)
        
        self.story_text = tk.Text(
            story_frame,
            font=('Georgia', 13),
            fg=self.colors['text'],
            bg=self.colors['card'],
            wrap='word',
            relief='flat',
            padx=20,
            pady=20,
            height=12
        )
        self.story_text.pack(fill='both', expand=True)
        self.story_text.config(state='disabled')
        
        # Event log
        log_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        log_frame.pack(fill='x', pady=5)
        
        tk.Label(
            log_frame,
            text="📜 Event Log:",
            font=('Segoe UI', 10, 'bold'),
            fg=self.colors['text_dim'],
            bg=self.colors['bg']
        ).pack(anchor='w')
        
        self.log_label = tk.Label(
            log_frame,
            text="Your adventure begins...",
            font=('Segoe UI', 10, 'italic'),
            fg=self.colors['success'],
            bg=self.colors['bg']
        )
        self.log_label.pack(anchor='w')
        
        # Action buttons container
        self.actions_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        self.actions_frame.pack(fill='x', pady=15)
        
        # Win message (hidden initially)
        self.win_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        
    def show_scene(self, scene_id):
        if scene_id == 'inventory':
            self.show_inventory()
            return
        elif scene_id == 'take_key':
            self.take_item('Rusty Key')
            return
        elif scene_id == 'take_gear':
            self.take_item('Golden Gear')
            return
        elif scene_id == 'try_gate':
            self.try_open_gate()
            return
        elif scene_id == 'push_button':
            self.push_button()
            return
        
        self.location = scene_id
        scene = self.scenes[scene_id]
        
        # Update location label
        location_names = {
            'start': 'Cave',
            'forest_clearing': 'Forest Clearing',
            'machine_room': 'Machine Room',
            'castle_gate': 'Castle Gate',
            'castle_hall': 'Castle Hall'
        }
        self.location_label.config(text=location_names.get(scene_id, scene_id.title()))
        
        # Update story text
        self.story_text.config(state='normal')
        self.story_text.delete('1.0', tk.END)
        self.story_text.insert('1.0', scene['description'])
        self.story_text.config(state='disabled')
        
        # Clear and create action buttons
        for widget in self.actions_frame.winfo_children():
            widget.destroy()
        
        for action_text, action_target in scene['actions']:
            btn = tk.Button(
                self.actions_frame,
                text=action_text,
                font=('Segoe UI', 11, 'bold'),
                fg='white',
                bg=self.colors['action'],
                activebackground=self.colors['primary'],
                relief='flat',
                padx=20,
                pady=10,
                command=lambda t=action_target: self.show_scene(t)
            )
            btn.pack(side='left', padx=5, expand=True, fill='x')
    
    def show_inventory(self):
        if self.inventory:
            items = ", ".join(self.inventory)
            self.add_log(f"Inventory: {items}")
        else:
            self.add_log("Your inventory is empty.")
    
    def take_item(self, item):
        if item not in self.inventory:
            self.inventory.append(item)
            self.inventory_label.config(text=", ".join(self.inventory))
            self.add_log(f"🌟 Acquired: {item}!")
        else:
            self.add_log(f"You already have the {item}.")
    
    def try_open_gate(self):
        if 'Rusty Key' in self.inventory:
            self.add_log("🔓 The key turns! The gate creaks open...")
            self.show_scene('castle_hall')
        else:
            self.add_log("❌ The gate is locked tight. You need a key.")
    
    def push_button(self):
        if 'Golden Gear' in self.inventory:
            self.add_log("⚙️ You insert the Golden Gear...")
            self.root.after(1000, self.win_game)
        else:
            self.add_log("The machine sputters. It seems to be missing a part...")
    
    def win_game(self):
        self.story_text.config(state='normal')
        self.story_text.delete('1.0', tk.END)
        self.story_text.insert('1.0', 
            "🎉 VICTORY! 🎉\n\n"
            "The machine whirs to life! Gears turn, lights flash, and a secret compartment opens.\n\n"
            "Inside, you find a magnificent DIAMOND, glowing with an inner light.\n\n"
            "You have completed the Cave Adventure!\n\n"
            "Congratulations, brave adventurer!"
        )
        self.story_text.config(state='disabled')
        
        # Clear action buttons and add restart
        for widget in self.actions_frame.winfo_children():
            widget.destroy()
        
        if 'Diamond' not in self.inventory:
            self.inventory.append('Diamond')
            self.inventory_label.config(text=", ".join(self.inventory))
        
        restart_btn = tk.Button(
            self.actions_frame,
            text="🔄 Play Again",
            font=('Segoe UI', 14, 'bold'),
            fg='white',
            bg=self.colors['success'],
            activebackground=self.colors['primary'],
            relief='flat',
            padx=30,
            pady=15,
            command=self.restart_game
        )
        restart_btn.pack(pady=20)
    
    def restart_game(self):
        self.inventory = []
        self.inventory_label.config(text="Empty")
        self.log_label.config(text="Your adventure begins anew...")
        self.show_scene('start')
    
    def add_log(self, message):
        self.log_label.config(text=message)
    
    def run(self):
        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.root.mainloop()

if __name__ == "__main__":
    app = TextAdventureGUI()
    app.run()
