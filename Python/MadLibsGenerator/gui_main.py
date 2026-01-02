"""
Mad Libs Generator GUI Application
Built with Tkinter - Part of 21APEX Challenge
"""

import tkinter as tk
from tkinter import ttk
import random

class MadLibsGeneratorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mad Libs Generator")
        self.root.geometry("550x700")
        self.root.resizable(False, False)
        self.root.configure(bg='#2d1b69')
        
        # Colors
        self.colors = {
            'bg': '#2d1b69',
            'card': '#11063b',
            'primary': '#ff6b6b',
            'secondary': '#4ecdc4',
            'accent': '#ffe66d',
            'text': '#ffffff',
            'text_dim': '#b8b8d1'
        }
        
        # Story templates
        self.stories = {
            'The Magical Forest': {
                'fields': [
                    ('adjective1', 'Enter an adjective:'),
                    ('noun1', 'Enter a noun:'),
                    ('verb_past', 'Enter a verb (past tense):'),
                    ('adjective2', 'Enter another adjective:'),
                    ('noun_plural', 'Enter a noun (plural):')
                ],
                'template': "One day, a {adjective1} wizard walked into a {noun1}. He {verb_past} loudly, causing all the {adjective2} {noun_plural} to scatter in fear!"
            },
            'The Space Mission': {
                'fields': [
                    ('name', 'Enter a name:'),
                    ('noun1', 'Enter a noun:'),
                    ('number', 'Enter a number:'),
                    ('verb', 'Enter a verb:'),
                    ('adjective', 'Enter an adjective:')
                ],
                'template': "Captain {name} looked out the window of the {noun1}. 'We have {number} seconds to {verb}!' she shouted. It was a {adjective} day in space."
            },
            'Creating a Pizza': {
                'fields': [
                    ('adjective', 'Enter an adjective:'),
                    ('food', 'Enter a food item:'),
                    ('noun', 'Enter a noun:'),
                    ('verb', 'Enter a verb:')
                ],
                'template': "To make the most {adjective} pizza, first you need dough made of {food}. Then, add a {noun} on top and {verb} it for 20 minutes."
            },
            'The Monster Party': {
                'fields': [
                    ('creature', 'Enter a creature:'),
                    ('adjective', 'Enter an adjective:'),
                    ('verb_ing', 'Enter a verb ending in -ing:'),
                    ('noun', 'Enter a noun:'),
                    ('emotion', 'Enter an emotion:')
                ],
                'template': "Last night, a {creature} threw the most {adjective} party! Everyone was {verb_ing} around the {noun} feeling totally {emotion}."
            },
            'The Superhero': {
                'fields': [
                    ('superhero_name', 'Enter a superhero name:'),
                    ('power', 'Enter a superpower:'),
                    ('villain', 'Enter a villain name:'),
                    ('city', 'Enter a city:'),
                    ('adjective', 'Enter an adjective:')
                ],
                'template': "{superhero_name}, with the power of {power}, faced {villain} in the heart of {city}. It was the most {adjective} battle ever!"
            }
        }
        
        self.current_story = None
        self.input_entries = {}
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="📖 Mad Libs Generator",
            font=('Comic Sans MS', 28, 'bold'),
            fg=self.colors['accent'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=(0, 5))
        
        subtitle = tk.Label(
            main_frame,
            text="Fill in the blanks to create hilarious stories!",
            font=('Segoe UI', 12),
            fg=self.colors['text_dim'],
            bg=self.colors['bg']
        )
        subtitle.pack(pady=(0, 15))
        
        # Story selector
        selector_frame = tk.Frame(main_frame, bg=self.colors['card'])
        selector_frame.pack(fill='x', pady=10, ipady=10)
        
        tk.Label(
            selector_frame,
            text="Choose a Story:",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(pady=(10, 5))
        
        story_titles = list(self.stories.keys())
        self.story_var = tk.StringVar(value=story_titles[0])
        
        story_dropdown = ttk.Combobox(
            selector_frame,
            textvariable=self.story_var,
            values=story_titles,
            state='readonly',
            font=('Segoe UI', 12),
            width=30
        )
        story_dropdown.pack(pady=(0, 10))
        story_dropdown.bind('<<ComboboxSelected>>', lambda e: self.load_story())
        
        # Random story button
        random_btn = tk.Button(
            selector_frame,
            text="🎲 Random Story",
            font=('Segoe UI', 10, 'bold'),
            fg=self.colors['card'],
            bg=self.colors['secondary'],
            activebackground=self.colors['primary'],
            relief='flat',
            padx=15,
            pady=5,
            command=self.random_story
        )
        random_btn.pack(pady=(0, 10))
        
        # Inputs container
        self.inputs_frame = tk.Frame(main_frame, bg=self.colors['card'])
        self.inputs_frame.pack(fill='x', pady=10, ipady=10)
        
        # Generate button
        generate_btn = tk.Button(
            main_frame,
            text="✨ Generate Story!",
            font=('Segoe UI', 14, 'bold'),
            fg=self.colors['card'],
            bg=self.colors['primary'],
            activebackground=self.colors['accent'],
            relief='flat',
            padx=30,
            pady=10,
            command=self.generate_story
        )
        generate_btn.pack(pady=15)
        
        # Result container
        result_frame = tk.Frame(main_frame, bg=self.colors['card'])
        result_frame.pack(fill='both', expand=True, pady=10)
        
        result_title = tk.Label(
            result_frame,
            text="📜 Your Story:",
            font=('Segoe UI', 14, 'bold'),
            fg=self.colors['accent'],
            bg=self.colors['card']
        )
        result_title.pack(pady=(15, 10))
        
        self.result_text = tk.Text(
            result_frame,
            font=('Georgia', 13),
            fg=self.colors['text'],
            bg=self.colors['bg'],
            wrap='word',
            height=8,
            relief='flat',
            padx=15,
            pady=15
        )
        self.result_text.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        self.result_text.insert('1.0', "Your story will appear here...")
        self.result_text.config(state='disabled')
        
        # Load first story
        self.load_story()
    
    def load_story(self):
        # Clear previous inputs
        for widget in self.inputs_frame.winfo_children():
            widget.destroy()
        self.input_entries.clear()
        
        story_name = self.story_var.get()
        story_data = self.stories[story_name]
        
        tk.Label(
            self.inputs_frame,
            text=f"📝 Fill in for: {story_name}",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['secondary'],
            bg=self.colors['card']
        ).pack(pady=(10, 5))
        
        for field_id, label_text in story_data['fields']:
            field_frame = tk.Frame(self.inputs_frame, bg=self.colors['card'])
            field_frame.pack(fill='x', padx=30, pady=5)
            
            label = tk.Label(
                field_frame,
                text=label_text,
                font=('Segoe UI', 10),
                fg=self.colors['text'],
                bg=self.colors['card'],
                width=25,
                anchor='e'
            )
            label.pack(side='left', padx=(0, 10))
            
            entry = tk.Entry(
                field_frame,
                font=('Segoe UI', 11),
                bg=self.colors['bg'],
                fg=self.colors['accent'],
                insertbackground=self.colors['accent'],
                relief='flat',
                width=20
            )
            entry.pack(side='left', fill='x', expand=True, ipady=5)
            
            self.input_entries[field_id] = entry
    
    def random_story(self):
        story_titles = list(self.stories.keys())
        self.story_var.set(random.choice(story_titles))
        self.load_story()
    
    def generate_story(self):
        story_name = self.story_var.get()
        story_data = self.stories[story_name]
        
        # Collect inputs
        values = {}
        for field_id, _ in story_data['fields']:
            value = self.input_entries[field_id].get().strip()
            if not value:
                value = f"[{field_id}]"  # Placeholder if empty
            values[field_id] = value
        
        # Generate story
        story = story_data['template'].format(**values)
        
        # Display result
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert('1.0', story)
        self.result_text.config(state='disabled')
    
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
    app = MadLibsGeneratorGUI()
    app.run()
