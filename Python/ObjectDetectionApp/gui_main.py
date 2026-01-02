"""
Object Detection App GUI
Built with Tkinter - Part of 21APEX Challenge
Supports real OpenCV detection or simulation mode
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import threading

# Try to import OpenCV
try:
    import cv2
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False

class ObjectDetectionGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Object Detection App")
        self.root.geometry("550x650")
        self.root.resizable(False, False)
        self.root.configure(bg='#0f0f0f')
        
        # Colors
        self.colors = {
            'bg': '#0f0f0f',
            'card': '#1a1a1a',
            'primary': '#00ff88',
            'secondary': '#00b4ff',
            'danger': '#ff4444',
            'text': '#ffffff',
            'text_dim': '#888888'
        }
        
        # State
        self.is_detecting = False
        self.detection_thread = None
        self.detections = []
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(
            main_frame,
            text="🎯 Object Detection",
            font=('Segoe UI', 26, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['bg']
        ).pack(pady=(0, 5))
        
        # Status
        status_text = "OpenCV Ready" if HAS_OPENCV else "Simulation Mode (pip install opencv-python)"
        status_color = self.colors['primary'] if HAS_OPENCV else self.colors['secondary']
        
        self.opencv_status = tk.Label(
            main_frame,
            text=f"● {status_text}",
            font=('Segoe UI', 10),
            fg=status_color,
            bg=self.colors['bg']
        )
        self.opencv_status.pack(pady=(0, 15))
        
        # Camera preview placeholder
        preview_frame = tk.Frame(main_frame, bg=self.colors['card'])
        preview_frame.pack(fill='x', pady=10)
        
        self.preview_canvas = tk.Canvas(
            preview_frame,
            width=500,
            height=280,
            bg='#000000',
            highlightthickness=2,
            highlightbackground=self.colors['primary']
        )
        self.preview_canvas.pack(pady=10)
        
        # Draw placeholder
        self.preview_canvas.create_text(
            250, 140,
            text="📷 Camera Preview\n(Click Start to begin detection)",
            font=('Segoe UI', 14),
            fill='#444444',
            justify='center'
        )
        
        # Detection info
        info_frame = tk.Frame(main_frame, bg=self.colors['card'])
        info_frame.pack(fill='x', pady=10, ipady=15)
        
        # Stats row
        stats_frame = tk.Frame(info_frame, bg=self.colors['card'])
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        # Detection count
        stat1 = tk.Frame(stats_frame, bg=self.colors['card'])
        stat1.pack(side='left', expand=True)
        tk.Label(stat1, text="Detections", font=('Segoe UI', 10),
                fg=self.colors['text_dim'], bg=self.colors['card']).pack()
        self.count_label = tk.Label(stat1, text="0", font=('Segoe UI', 24, 'bold'),
                fg=self.colors['primary'], bg=self.colors['card'])
        self.count_label.pack()
        
        # Status
        stat2 = tk.Frame(stats_frame, bg=self.colors['card'])
        stat2.pack(side='left', expand=True)
        tk.Label(stat2, text="Status", font=('Segoe UI', 10),
                fg=self.colors['text_dim'], bg=self.colors['card']).pack()
        self.status_label = tk.Label(stat2, text="Idle", font=('Segoe UI', 16, 'bold'),
                fg=self.colors['danger'], bg=self.colors['card'])
        self.status_label.pack()
        
        # FPS
        stat3 = tk.Frame(stats_frame, bg=self.colors['card'])
        stat3.pack(side='left', expand=True)
        tk.Label(stat3, text="FPS", font=('Segoe UI', 10),
                fg=self.colors['text_dim'], bg=self.colors['card']).pack()
        self.fps_label = tk.Label(stat3, text="--", font=('Segoe UI', 24, 'bold'),
                fg=self.colors['secondary'], bg=self.colors['card'])
        self.fps_label.pack()
        
        # Detection log
        log_frame = tk.Frame(main_frame, bg=self.colors['card'])
        log_frame.pack(fill='both', expand=True, pady=10)
        
        tk.Label(
            log_frame,
            text="📋 Detection Log:",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['card']
        ).pack(anchor='w', padx=15, pady=(10, 5))
        
        # Log listbox
        log_container = tk.Frame(log_frame, bg=self.colors['card'])
        log_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        scrollbar = ttk.Scrollbar(log_container)
        scrollbar.pack(side='right', fill='y')
        
        self.log_listbox = tk.Listbox(
            log_container,
            font=('Consolas', 10),
            bg='#000000',
            fg=self.colors['primary'],
            selectbackground=self.colors['secondary'],
            relief='flat',
            yscrollcommand=scrollbar.set
        )
        self.log_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.log_listbox.yview)
        
        # Control buttons
        control_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        control_frame.pack(fill='x', pady=10)
        
        self.start_btn = tk.Button(
            control_frame,
            text="▶ Start Detection",
            font=('Segoe UI', 12, 'bold'),
            fg='white',
            bg=self.colors['primary'],
            activebackground=self.colors['secondary'],
            relief='flat',
            padx=25,
            pady=12,
            command=self.toggle_detection
        )
        self.start_btn.pack(side='left', padx=5)
        
        tk.Button(
            control_frame,
            text="🗑️ Clear Log",
            font=('Segoe UI', 12, 'bold'),
            fg='white',
            bg='#555555',
            relief='flat',
            padx=25,
            pady=12,
            command=self.clear_log
        ).pack(side='left', padx=5)
        
        if HAS_OPENCV:
            tk.Button(
                control_frame,
                text="🎥 Open Camera Window",
                font=('Segoe UI', 10, 'bold'),
                fg='white',
                bg=self.colors['secondary'],
                relief='flat',
                padx=15,
                pady=10,
                command=self.open_camera_window
            ).pack(side='right', padx=5)
        
    def toggle_detection(self):
        if not self.is_detecting:
            self.start_detection()
        else:
            self.stop_detection()
    
    def start_detection(self):
        self.is_detecting = True
        self.start_btn.config(text="⏹ Stop Detection", bg=self.colors['danger'])
        self.status_label.config(text="Active", fg=self.colors['primary'])
        
        # Update canvas
        self.preview_canvas.delete('all')
        self.preview_canvas.create_text(
            250, 140,
            text="🔍 Scanning for objects...",
            font=('Segoe UI', 16),
            fill=self.colors['primary'],
            tags='scanning'
        )
        
        # Start detection in thread
        self.detection_thread = threading.Thread(target=self.run_simulation, daemon=True)
        self.detection_thread.start()
    
    def stop_detection(self):
        self.is_detecting = False
        self.start_btn.config(text="▶ Start Detection", bg=self.colors['primary'])
        self.status_label.config(text="Stopped", fg=self.colors['danger'])
        self.fps_label.config(text="--")
        
        # Update canvas
        self.preview_canvas.delete('all')
        self.preview_canvas.create_text(
            250, 140,
            text="📷 Detection stopped",
            font=('Segoe UI', 14),
            fill='#444444'
        )
    
    def run_simulation(self):
        """Simulation mode for demo"""
        objects = [
            ("Person", "👤"),
            ("Cat", "🐱"),
            ("Dog", "🐕"),
            ("Car", "🚗"),
            ("Chair", "🪑"),
            ("Laptop", "💻"),
            ("Phone", "📱"),
            ("Book", "📚"),
            ("Cup", "☕"),
            ("Bottle", "🍶")
        ]
        
        detection_count = 0
        start_time = time.time()
        
        while self.is_detecting:
            # Simulate detection
            obj_name, emoji = random.choice(objects)
            confidence = random.uniform(75.0, 99.9)
            x = random.randint(50, 400)
            y = random.randint(50, 230)
            
            detection_count += 1
            elapsed = time.time() - start_time
            fps = detection_count / elapsed if elapsed > 0 else 0
            
            # Update UI in main thread
            self.root.after(0, self.add_detection, obj_name, emoji, confidence, x, y)
            self.root.after(0, self.update_stats, detection_count, fps)
            
            time.sleep(random.uniform(0.5, 1.5))
    
    def add_detection(self, obj_name, emoji, confidence, x, y):
        timestamp = time.strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {emoji} {obj_name}: {confidence:.1f}%"
        
        self.log_listbox.insert(tk.END, log_entry)
        self.log_listbox.see(tk.END)
        
        # Draw detection box on canvas
        self.preview_canvas.delete('box')
        box_color = self.colors['primary'] if confidence > 90 else self.colors['secondary']
        
        # Draw rectangle
        self.preview_canvas.create_rectangle(
            x, y, x + 80, y + 60,
            outline=box_color,
            width=2,
            tags='box'
        )
        
        # Draw label
        self.preview_canvas.create_text(
            x + 40, y - 10,
            text=f"{emoji} {obj_name}",
            font=('Segoe UI', 10, 'bold'),
            fill=box_color,
            tags='box'
        )
        
        self.preview_canvas.create_text(
            x + 40, y + 75,
            text=f"{confidence:.1f}%",
            font=('Segoe UI', 9),
            fill=box_color,
            tags='box'
        )
    
    def update_stats(self, count, fps):
        self.count_label.config(text=str(count))
        self.fps_label.config(text=f"{fps:.1f}")
    
    def clear_log(self):
        self.log_listbox.delete(0, tk.END)
        self.count_label.config(text="0")
    
    def open_camera_window(self):
        """Open real OpenCV camera window for face detection"""
        if not HAS_OPENCV:
            messagebox.showwarning("Warning", "OpenCV is not installed!")
            return
        
        messagebox.showinfo("Camera", "Opening camera window...\nPress 'q' to close the camera window.")
        
        # Run in thread to not block
        threading.Thread(target=self._run_opencv_detection, daemon=True).start()
    
    def _run_opencv_detection(self):
        """Run real OpenCV face detection"""
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(0)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, "Face", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            cv2.imshow('Object Detection - Face (Press Q to close)', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
    
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
    app = ObjectDetectionGUI()
    app.run()
