import tkinter as tk
from tkinter import ttk
import time
from datetime import datetime, timedelta
import threading
from tkinter import messagebox
import math

class ModernClockApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Modern Desktop Clock")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f2f5')
        
        # Color scheme - modern pastel colors
        self.colors = {
            'primary': '#667eea',
            'secondary': '#764ba2',
            'success': '#56ab2f',
            'warning': '#f093fb',
            'danger': '#f85032',
            'light': '#f8f9fc',
            'dark': '#2c3e50',
            'background': '#f0f2f5',
            'card': '#ffffff',
            'text_primary': '#2c3e50',
            'text_secondary': '#718096',
            'accent': '#4fd1c7'
        }
        
        # Timer states
        self.pomodoro_running = False
        self.pomodoro_paused = False
        self.pomodoro_time_left = 25 * 60  # 25 minutes
        self.pomodoro_is_break = False
        
        self.stopwatch_running = False
        self.stopwatch_start_time = 0
        self.stopwatch_elapsed = 0
        self.lap_times = []
        
        self.study_session_running = False
        self.study_session_paused = False
        self.study_session_time_left = 4 * 3600  # 4 hours
        self.study_is_break = False
        
        self.setup_ui()
        self.start_clock_update()
        
    def create_gradient_frame(self, parent, color1, color2, width, height):
        """Create a frame with gradient-like effect"""
        frame = tk.Frame(parent, width=width, height=height)
        frame.pack_propagate(False)
        
        canvas = tk.Canvas(frame, width=width, height=height, highlightthickness=0)
        canvas.pack(fill='both', expand=True)
        
        # Create gradient effect by drawing multiple rectangles
        steps = 100
        for i in range(steps):
            # Calculate intermediate color
            ratio = i / steps
            r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
            r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
            
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            
            color = f"#{r:02x}{g:02x}{b:02x}"
            y = int(i * height / steps)
            canvas.create_rectangle(0, y, width, y + height // steps + 1, 
                                  fill=color, outline=color)
        
        return frame, canvas
    
    def create_rounded_button(self, parent, text, command, bg_color, text_color='white', width=120, height=35):
        """Create a modern rounded button"""
        button_frame = tk.Frame(parent, bg=parent['bg'])
        
        canvas = tk.Canvas(button_frame, width=width, height=height, 
                          highlightthickness=0, bg=parent['bg'])
        canvas.pack()
        
        # Draw rounded rectangle
        x1, y1, x2, y2 = 5, 5, width-5, height-5
        canvas.create_oval(x1-10, y1-10, x1+10, y1+10, fill=bg_color, outline=bg_color)
        canvas.create_oval(x2-10, y1-10, x2+10, y1+10, fill=bg_color, outline=bg_color)
        canvas.create_oval(x1-10, y2-10, x1+10, y2+10, fill=bg_color, outline=bg_color)
        canvas.create_oval(x2-10, y2-10, x2+10, y2+10, fill=bg_color, outline=bg_color)
        canvas.create_rectangle(x1, y1-10, x2, y2+10, fill=bg_color, outline=bg_color)
        canvas.create_rectangle(x1-10, y1, x2+10, y2, fill=bg_color, outline=bg_color)
        
        # Add text
        canvas.create_text(width//2, height//2, text=text, fill=text_color, 
                          font=('Arial', 10, 'bold'))
        
        # Bind click event
        canvas.bind("<Button-1>", lambda e: command())
        canvas.bind("<Enter>", lambda e: self.on_button_hover(canvas, bg_color, True))
        canvas.bind("<Leave>", lambda e: self.on_button_hover(canvas, bg_color, False))
        
        return button_frame
    
    def on_button_hover(self, canvas, original_color, is_hover):
        """Handle button hover effects"""
        if is_hover:
            # Slightly lighten the color on hover
            canvas.configure(cursor="hand2")
        else:
            canvas.configure(cursor="")
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Create main container with tabs
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure tab colors
        style.configure('TNotebook.Tab', 
                       background=self.colors['light'],
                       foreground=self.colors['text_primary'],
                       padding=[20, 10])
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['primary'])],
                 foreground=[('selected', 'white')])
        
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create tabs
        self.setup_clock_tab(notebook)
        self.setup_pomodoro_tab(notebook)
        self.setup_stopwatch_tab(notebook)
        self.setup_study_session_tab(notebook)
    
    def setup_clock_tab(self, parent):
        """Setup the digital clock tab"""
        clock_frame = tk.Frame(parent, bg=self.colors['background'])
        parent.add(clock_frame, text='Digital Clock')
        
        # Create gradient background
        gradient_frame, gradient_canvas = self.create_gradient_frame(
            clock_frame, self.colors['primary'], self.colors['secondary'], 760, 500
        )
        gradient_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Time display
        self.time_label = tk.Label(gradient_canvas, text="", 
                                  font=('Arial', 48, 'bold'), 
                                  fg='white', bg=self.colors['primary'])
        gradient_canvas.create_window(380, 200, window=self.time_label)
        
        # Date display
        self.date_label = tk.Label(gradient_canvas, text="", 
                                  font=('Arial', 18), 
                                  fg='white', bg=self.colors['primary'])
        gradient_canvas.create_window(380, 270, window=self.date_label)
        
        # Timezone display
        self.timezone_label = tk.Label(gradient_canvas, text="", 
                                      font=('Arial', 14), 
                                      fg='white', bg=self.colors['primary'])
        gradient_canvas.create_window(380, 310, window=self.timezone_label)
    
    def setup_pomodoro_tab(self, parent):
        """Setup the Pomodoro timer tab"""
        pomodoro_frame = tk.Frame(parent, bg=self.colors['background'])
        parent.add(pomodoro_frame, text='Pomodoro Timer')
        
        # Main container
        main_container = tk.Frame(pomodoro_frame, bg=self.colors['card'], relief='flat')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_container, text="Pomodoro Timer", 
                              font=('Arial', 24, 'bold'), 
                              fg=self.colors['text_primary'], bg=self.colors['card'])
        title_label.pack(pady=20)
        
        # Timer display
        self.pomodoro_display = tk.Label(main_container, text="25:00", 
                                        font=('Arial', 64, 'bold'), 
                                        fg=self.colors['primary'], bg=self.colors['card'])
        self.pomodoro_display.pack(pady=30)
        
        # Status label
        self.pomodoro_status = tk.Label(main_container, text="Work Session", 
                                       font=('Arial', 16), 
                                       fg=self.colors['text_secondary'], bg=self.colors['card'])
        self.pomodoro_status.pack(pady=10)
        
        # Control buttons
        button_frame = tk.Frame(main_container, bg=self.colors['card'])
        button_frame.pack(pady=30)
        
        self.pomodoro_start_btn = self.create_rounded_button(
            button_frame, "Start", self.toggle_pomodoro, self.colors['success']
        )
        self.pomodoro_start_btn.pack(side='left', padx=10)
        
        reset_btn = self.create_rounded_button(
            button_frame, "Reset", self.reset_pomodoro, self.colors['danger']
        )
        reset_btn.pack(side='left', padx=10)
    
    def setup_stopwatch_tab(self, parent):
        """Setup the stopwatch tab"""
        stopwatch_frame = tk.Frame(parent, bg=self.colors['background'])
        parent.add(stopwatch_frame, text='Stopwatch')
        
        # Main container
        main_container = tk.Frame(stopwatch_frame, bg=self.colors['card'], relief='flat')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_container, text="Stopwatch", 
                              font=('Arial', 24, 'bold'), 
                              fg=self.colors['text_primary'], bg=self.colors['card'])
        title_label.pack(pady=20)
        
        # Timer display
        self.stopwatch_display = tk.Label(main_container, text="00:00:00", 
                                         font=('Arial', 48, 'bold'), 
                                         fg=self.colors['accent'], bg=self.colors['card'])
        self.stopwatch_display.pack(pady=30)
        
        # Control buttons
        button_frame = tk.Frame(main_container, bg=self.colors['card'])
        button_frame.pack(pady=20)
        
        self.stopwatch_start_btn = self.create_rounded_button(
            button_frame, "Start", self.toggle_stopwatch, self.colors['success']
        )
        self.stopwatch_start_btn.pack(side='left', padx=10)
        
        lap_btn = self.create_rounded_button(
            button_frame, "Lap", self.add_lap, self.colors['warning']
        )
        lap_btn.pack(side='left', padx=10)
        
        reset_btn = self.create_rounded_button(
            button_frame, "Reset", self.reset_stopwatch, self.colors['danger']
        )
        reset_btn.pack(side='left', padx=10)
        
        # Lap times display
        lap_frame = tk.Frame(main_container, bg=self.colors['card'])
        lap_frame.pack(fill='both', expand=True, pady=20)
        
        lap_title = tk.Label(lap_frame, text="Lap Times", 
                            font=('Arial', 16, 'bold'), 
                            fg=self.colors['text_primary'], bg=self.colors['card'])
        lap_title.pack()
        
        # Scrollable lap times
        lap_scroll_frame = tk.Frame(lap_frame, bg=self.colors['card'])
        lap_scroll_frame.pack(fill='both', expand=True, pady=10)
        
        scrollbar = tk.Scrollbar(lap_scroll_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.lap_listbox = tk.Listbox(lap_scroll_frame, yscrollcommand=scrollbar.set,
                                     bg=self.colors['light'], 
                                     fg=self.colors['text_primary'],
                                     font=('Arial', 12))
        self.lap_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.lap_listbox.yview)
    
    def setup_study_session_tab(self, parent):
        """Setup the study session timer tab"""
        study_frame = tk.Frame(parent, bg=self.colors['background'])
        parent.add(study_frame, text='Study Session')
        
        # Main container
        main_container = tk.Frame(study_frame, bg=self.colors['card'], relief='flat')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_container, text="Study Session Timer", 
                              font=('Arial', 24, 'bold'), 
                              fg=self.colors['text_primary'], bg=self.colors['card'])
        title_label.pack(pady=20)
        
        # Info label
        info_label = tk.Label(main_container, text="4 Hours Study + 1.5 Hours Break", 
                             font=('Arial', 14), 
                             fg=self.colors['text_secondary'], bg=self.colors['card'])
        info_label.pack(pady=5)
        
        # Timer display
        self.study_display = tk.Label(main_container, text="4:00:00", 
                                     font=('Arial', 56, 'bold'), 
                                     fg=self.colors['secondary'], bg=self.colors['card'])
        self.study_display.pack(pady=30)
        
        # Status label
        self.study_status = tk.Label(main_container, text="Study Time", 
                                    font=('Arial', 18, 'bold'), 
                                    fg=self.colors['primary'], bg=self.colors['card'])
        self.study_status.pack(pady=10)
        
        # Progress bar
        self.study_progress = ttk.Progressbar(main_container, length=400, mode='determinate')
        self.study_progress.pack(pady=20)
        
        # Control buttons
        button_frame = tk.Frame(main_container, bg=self.colors['card'])
        button_frame.pack(pady=30)
        
        self.study_start_btn = self.create_rounded_button(
            button_frame, "Start", self.toggle_study_session, self.colors['success']
        )
        self.study_start_btn.pack(side='left', padx=10)
        
        reset_btn = self.create_rounded_button(
            button_frame, "Reset", self.reset_study_session, self.colors['danger']
        )
        reset_btn.pack(side='left', padx=10)
    
    def start_clock_update(self):
        """Start the clock update loop"""
        self.update_clock()
        self.update_timers()
    
    def update_clock(self):
        """Update the digital clock display"""
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%A, %B %d, %Y")
        timezone_str = now.strftime("IST %z")
        
        self.time_label.config(text=time_str)
        self.date_label.config(text=date_str)
        self.timezone_label.config(text=timezone_str)
        
        # Schedule next update
        self.root.after(1000, self.update_clock)
    
    def update_timers(self):
        """Update all timer displays"""
        # Update Pomodoro timer
        if self.pomodoro_running and not self.pomodoro_paused:
            if self.pomodoro_time_left > 0:
                self.pomodoro_time_left -= 1
                minutes = self.pomodoro_time_left // 60
                seconds = self.pomodoro_time_left % 60
                self.pomodoro_display.config(text=f"{minutes:02d}:{seconds:02d}")
            else:
                self.pomodoro_complete()
        
        # Update stopwatch
        if self.stopwatch_running:
            current_time = time.time()
            total_elapsed = self.stopwatch_elapsed + (current_time - self.stopwatch_start_time)
            hours = int(total_elapsed // 3600)
            minutes = int((total_elapsed % 3600) // 60)
            seconds = int(total_elapsed % 60)
            self.stopwatch_display.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        
        # Update study session timer
        if self.study_session_running and not self.study_session_paused:
            if self.study_session_time_left > 0:
                self.study_session_time_left -= 1
                hours = self.study_session_time_left // 3600
                minutes = (self.study_session_time_left % 3600) // 60
                seconds = self.study_session_time_left % 60
                self.study_display.config(text=f"{hours:01d}:{minutes:02d}:{seconds:02d}")
                
                # Update progress bar
                if self.study_is_break:
                    total_time = 90 * 60  # 1.5 hours in seconds
                    progress = ((total_time - self.study_session_time_left) / total_time) * 100
                else:
                    total_time = 4 * 3600  # 4 hours in seconds
                    progress = ((total_time - self.study_session_time_left) / total_time) * 100
                self.study_progress['value'] = progress
            else:
                self.study_session_complete()
        
        # Schedule next update
        self.root.after(1000, self.update_timers)
    
    # Pomodoro Timer Functions
    def toggle_pomodoro(self):
        """Toggle Pomodoro timer start/pause"""
        if not self.pomodoro_running:
            self.pomodoro_running = True
            self.pomodoro_paused = False
            self.pomodoro_start_btn.destroy()
            self.pomodoro_start_btn = self.create_rounded_button(
                self.pomodoro_start_btn.master, "Pause", self.toggle_pomodoro, self.colors['warning']
            )
            self.pomodoro_start_btn.pack(side='left', padx=10)
        elif not self.pomodoro_paused:
            self.pomodoro_paused = True
            self.pomodoro_start_btn.destroy()
            self.pomodoro_start_btn = self.create_rounded_button(
                self.pomodoro_start_btn.master, "Resume", self.toggle_pomodoro, self.colors['success']
            )
            self.pomodoro_start_btn.pack(side='left', padx=10)
        else:
            self.pomodoro_paused = False
            self.pomodoro_start_btn.destroy()
            self.pomodoro_start_btn = self.create_rounded_button(
                self.pomodoro_start_btn.master, "Pause", self.toggle_pomodoro, self.colors['warning']
            )
            self.pomodoro_start_btn.pack(side='left', padx=10)
    
    def reset_pomodoro(self):
        """Reset Pomodoro timer"""
        self.pomodoro_running = False
        self.pomodoro_paused = False
        self.pomodoro_is_break = False
        self.pomodoro_time_left = 25 * 60
        self.pomodoro_display.config(text="25:00")
        self.pomodoro_status.config(text="Work Session")
        
        self.pomodoro_start_btn.destroy()
        self.pomodoro_start_btn = self.create_rounded_button(
            self.pomodoro_start_btn.master, "Start", self.toggle_pomodoro, self.colors['success']
        )
        self.pomodoro_start_btn.pack(side='left', padx=10)
    
    def pomodoro_complete(self):
        """Handle Pomodoro timer completion"""
        if not self.pomodoro_is_break:
            # Work session complete, start break
            self.pomodoro_is_break = True
            self.pomodoro_time_left = 5 * 60  # 5 minute break
            self.pomodoro_status.config(text="Break Time!")
            messagebox.showinfo("Pomodoro", "Work session complete! Time for a 5-minute break.")
        else:
            # Break complete, start new work session
            self.pomodoro_is_break = False
            self.pomodoro_time_left = 25 * 60  # 25 minute work
            self.pomodoro_status.config(text="Work Session")
            messagebox.showinfo("Pomodoro", "Break complete! Time to get back to work.")
    
    # Stopwatch Functions
    def toggle_stopwatch(self):
        """Toggle stopwatch start/stop"""
        if not self.stopwatch_running:
            self.stopwatch_running = True
            self.stopwatch_start_time = time.time()
            self.stopwatch_start_btn.destroy()
            self.stopwatch_start_btn = self.create_rounded_button(
                self.stopwatch_start_btn.master, "Stop", self.toggle_stopwatch, self.colors['danger']
            )
            self.stopwatch_start_btn.pack(side='left', padx=10)
        else:
            self.stopwatch_running = False
            self.stopwatch_elapsed += time.time() - self.stopwatch_start_time
            self.stopwatch_start_btn.destroy()
            self.stopwatch_start_btn = self.create_rounded_button(
                self.stopwatch_start_btn.master, "Start", self.toggle_stopwatch, self.colors['success']
            )
            self.stopwatch_start_btn.pack(side='left', padx=10)
    
    def add_lap(self):
        """Add a lap time"""
        if self.stopwatch_running:
            current_time = time.time()
            total_elapsed = self.stopwatch_elapsed + (current_time - self.stopwatch_start_time)
            hours = int(total_elapsed // 3600)
            minutes = int((total_elapsed % 3600) // 60)
            seconds = int(total_elapsed % 60)
            lap_time = f"Lap {len(self.lap_times) + 1}: {hours:02d}:{minutes:02d}:{seconds:02d}"
            self.lap_times.append(lap_time)
            self.lap_listbox.insert(tk.END, lap_time)
            self.lap_listbox.see(tk.END)
    
    def reset_stopwatch(self):
        """Reset stopwatch"""
        self.stopwatch_running = False
        self.stopwatch_elapsed = 0
        self.stopwatch_display.config(text="00:00:00")
        self.lap_times.clear()
        self.lap_listbox.delete(0, tk.END)
        
        self.stopwatch_start_btn.destroy()
        self.stopwatch_start_btn = self.create_rounded_button(
            self.stopwatch_start_btn.master, "Start", self.toggle_stopwatch, self.colors['success']
        )
        self.stopwatch_start_btn.pack(side='left', padx=10)
    
    # Study Session Functions
    def toggle_study_session(self):
        """Toggle study session timer"""
        if not self.study_session_running:
            self.study_session_running = True
            self.study_session_paused = False
            self.study_start_btn.destroy()
            self.study_start_btn = self.create_rounded_button(
                self.study_start_btn.master, "Pause", self.toggle_study_session, self.colors['warning']
            )
            self.study_start_btn.pack(side='left', padx=10)
        elif not self.study_session_paused:
            self.study_session_paused = True
            self.study_start_btn.destroy()
            self.study_start_btn = self.create_rounded_button(
                self.study_start_btn.master, "Resume", self.toggle_study_session, self.colors['success']
            )
            self.study_start_btn.pack(side='left', padx=10)
        else:
            self.study_session_paused = False
            self.study_start_btn.destroy()
            self.study_start_btn = self.create_rounded_button(
                self.study_start_btn.master, "Pause", self.toggle_study_session, self.colors['warning']
            )
            self.study_start_btn.pack(side='left', padx=10)
    
    def reset_study_session(self):
        """Reset study session timer"""
        self.study_session_running = False
        self.study_session_paused = False
        self.study_is_break = False
        self.study_session_time_left = 4 * 3600
        self.study_display.config(text="4:00:00")
        self.study_status.config(text="Study Time")
        self.study_progress['value'] = 0
        
        self.study_start_btn.destroy()
        self.study_start_btn = self.create_rounded_button(
            self.study_start_btn.master, "Start", self.toggle_study_session, self.colors['success']
        )
        self.study_start_btn.pack(side='left', padx=10)
    
    def study_session_complete(self):
        """Handle study session completion"""
        if not self.study_is_break:
            # Study session complete, start break
            self.study_is_break = True
            self.study_session_time_left = 90 * 60  # 1.5 hour break
            self.study_status.config(text="Break Time!")
            self.study_progress['value'] = 0
            messagebox.showinfo("Study Session", "4-hour study session complete! Time for a 1.5-hour break.")
        else:
            # Break complete
            self.study_session_running = False
            self.study_status.config(text="Session Complete!")
            messagebox.showinfo("Study Session", "Break complete! Great job on completing your study session.")
            self.reset_study_session()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    app = ModernClockApp()
    app.run()
