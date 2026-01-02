import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import math

class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Resizer Pro")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.original_image = None
        self.resized_image = None
        self.preview_image = None
        self.file_path = ""
        
        # StringVars for UI elements
        self.resize_mode = tk.StringVar(value="pixels")
        self.width_var = tk.StringVar(value="800")
        self.height_var = tk.StringVar(value="600")
        self.percentage_var = tk.StringVar(value="100")
        self.file_size_var = tk.StringVar(value="500")
        self.file_size_unit = tk.StringVar(value="KB")
        self.maintain_aspect = tk.BooleanVar(value=True)
        self.quality_var = tk.StringVar(value="85")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Image Resizer Pro", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # File selection frame
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
        file_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Button(file_frame, text="Select Image", 
                  command=self.select_file).grid(row=0, column=0, padx=(0, 10))
        
        self.file_label = ttk.Label(file_frame, text="No file selected", 
                                   foreground="gray")
        self.file_label.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Resize options frame
        resize_frame = ttk.LabelFrame(main_frame, text="Resize Options", padding="10")
        resize_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), 
                         padx=(0, 10), pady=(0, 10))
        
        # Resize mode selection
        ttk.Label(resize_frame, text="Resize Mode:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        mode_frame = ttk.Frame(resize_frame)
        mode_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Radiobutton(mode_frame, text="Pixel Dimensions", 
                       variable=self.resize_mode, value="pixels",
                       command=self.on_mode_change).grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(mode_frame, text="Percentage", 
                       variable=self.resize_mode, value="percentage",
                       command=self.on_mode_change).grid(row=1, column=0, sticky=tk.W)
        ttk.Radiobutton(mode_frame, text="File Size", 
                       variable=self.resize_mode, value="filesize",
                       command=self.on_mode_change).grid(row=2, column=0, sticky=tk.W)
        
        # Pixel dimensions frame
        self.pixel_frame = ttk.Frame(resize_frame)
        self.pixel_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(self.pixel_frame, text="Width:").grid(row=0, column=0, sticky=tk.W)
        self.width_entry = ttk.Entry(self.pixel_frame, textvariable=self.width_var, width=10)
        self.width_entry.grid(row=0, column=1, padx=(5, 10))
        self.width_entry.bind('<KeyRelease>', self.on_width_change)
        
        ttk.Label(self.pixel_frame, text="Height:").grid(row=0, column=2, sticky=tk.W)
        self.height_entry = ttk.Entry(self.pixel_frame, textvariable=self.height_var, width=10)
        self.height_entry.grid(row=0, column=3, padx=(5, 0))
        self.height_entry.bind('<KeyRelease>', self.on_height_change)
        
        # Percentage frame
        self.percentage_frame = ttk.Frame(resize_frame)
        
        ttk.Label(self.percentage_frame, text="Scale:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(self.percentage_frame, textvariable=self.percentage_var, 
                 width=10).grid(row=0, column=1, padx=(5, 5))
        ttk.Label(self.percentage_frame, text="%").grid(row=0, column=2, sticky=tk.W)
        
        # File size frame
        self.filesize_frame = ttk.Frame(resize_frame)
        
        ttk.Label(self.filesize_frame, text="Target Size:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(self.filesize_frame, textvariable=self.file_size_var, 
                 width=10).grid(row=0, column=1, padx=(5, 5))
        ttk.Combobox(self.filesize_frame, textvariable=self.file_size_unit, 
                    values=["KB", "MB"], width=5, state="readonly").grid(row=0, column=2)
        
        # Aspect ratio and quality
        ttk.Checkbutton(resize_frame, text="Maintain Aspect Ratio", 
                       variable=self.maintain_aspect).grid(row=5, column=0, sticky=tk.W, pady=(10, 5))
        
        quality_frame = ttk.Frame(resize_frame)
        quality_frame.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        ttk.Label(quality_frame, text="JPEG Quality:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(quality_frame, textvariable=self.quality_var, 
                 width=10).grid(row=0, column=1, padx=(5, 5))
        ttk.Label(quality_frame, text="(1-100)").grid(row=0, column=2, sticky=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(resize_frame)
        button_frame.grid(row=7, column=0, pady=(10, 0))
        
        self.resize_btn = ttk.Button(button_frame, text="Resize Image", 
                                    command=self.resize_image, state='disabled')
        self.resize_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.save_btn = ttk.Button(button_frame, text="Save As...", 
                                  command=self.save_image, state='disabled')
        self.save_btn.grid(row=0, column=1)
        
        # Preview frame
        preview_frame = ttk.LabelFrame(main_frame, text="Image Preview", padding="10")
        preview_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(1, weight=1)
        
        # Image info label
        self.info_label = ttk.Label(preview_frame, text="No image loaded", 
                                   font=('Arial', 9))
        self.info_label.grid(row=0, column=0, pady=(0, 10))
        
        # Preview canvas
        self.preview_canvas = tk.Canvas(preview_frame, bg='white', 
                                       width=400, height=400, relief='sunken', bd=2)
        self.preview_canvas.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Initially hide unused frames
        self.on_mode_change()
        
    def on_mode_change(self):
        # Hide all frames first
        self.percentage_frame.grid_remove()
        self.filesize_frame.grid_remove()
        
        # Show relevant frame
        if self.resize_mode.get() == "pixels":
            pass  # Pixel frame is always visible
        elif self.resize_mode.get() == "percentage":
            self.percentage_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        elif self.resize_mode.get() == "filesize":
            self.filesize_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
    
    def on_width_change(self, event=None):
        if self.maintain_aspect.get() and self.original_image:
            try:
                width = int(self.width_var.get())
                aspect_ratio = self.original_image.size[0] / self.original_image.size[1]
                height = int(width / aspect_ratio)
                self.height_var.set(str(height))
            except ValueError:
                pass
    
    def on_height_change(self, event=None):
        if self.maintain_aspect.get() and self.original_image:
            try:
                height = int(self.height_var.get())
                aspect_ratio = self.original_image.size[0] / self.original_image.size[1]
                width = int(height * aspect_ratio)
                self.width_var.set(str(width))
            except ValueError:
                pass
    
    def select_file(self):
        file_types = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("PNG files", "*.png"),
            ("All files", "*.*")
        ]
        
        self.file_path = filedialog.askopenfilename(
            title="Select an image file",
            filetypes=file_types
        )
        
        if self.file_path:
            try:
                self.original_image = Image.open(self.file_path)
                filename = os.path.basename(self.file_path)
                self.file_label.config(text=filename, foreground="black")
                
                # Update info
                width, height = self.original_image.size
                self.info_label.config(text=f"Original: {width} x {height} pixels")
                
                # Update default values
                self.width_var.set(str(width))
                self.height_var.set(str(height))
                
                # Enable resize button
                self.resize_btn.config(state='normal')
                
                # Show original image in preview
                self.show_image_preview(self.original_image)
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
                self.file_path = ""
                self.original_image = None
    
    def calculate_target_size(self):
        if not self.original_image:
            return None, None
            
        original_width, original_height = self.original_image.size
        
        try:
            if self.resize_mode.get() == "pixels":
                target_width = int(self.width_var.get())
                target_height = int(self.height_var.get())
                
                if target_width <= 0 or target_height <= 0:
                    raise ValueError("Dimensions must be positive")
                
                return target_width, target_height
                
            elif self.resize_mode.get() == "percentage":
                scale = float(self.percentage_var.get()) / 100
                if scale <= 0:
                    raise ValueError("Percentage must be positive")
                
                target_width = max(1, int(original_width * scale))
                target_height = max(1, int(original_height * scale))
                return target_width, target_height
                
            elif self.resize_mode.get() == "filesize":
                target_size_kb = float(self.file_size_var.get())
                if self.file_size_unit.get() == "MB":
                    target_size_kb *= 1024
                
                if target_size_kb <= 0:
                    raise ValueError("File size must be positive")
                
                # Estimate scale factor based on current image
                # This is an approximation - actual file size depends on compression
                current_pixels = original_width * original_height
                # Rough estimate: 1 pixel ≈ 3 bytes for RGB, plus JPEG compression
                estimated_current_size_kb = (current_pixels * 3) / (1024 * 2)  # Assume 50% compression
                
                if estimated_current_size_kb > 0:
                    scale_factor = math.sqrt(target_size_kb / estimated_current_size_kb)
                else:
                    scale_factor = 0.5  # Default reduction
                
                target_width = max(1, int(original_width * scale_factor))
                target_height = max(1, int(original_height * scale_factor))
                
                return target_width, target_height
                
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
            return None, None
    
    def resize_image(self):
        if not self.original_image:
            messagebox.showwarning("Warning", "Please select an image first")
            return
        
        target_width, target_height = self.calculate_target_size()
        if target_width is None or target_height is None:
            return
        
        try:
            # Resize image using high-quality resampling
            self.resized_image = self.original_image.resize(
                (target_width, target_height), Image.Resampling.LANCZOS)
            
            # Show resized image in preview
            self.show_image_preview(self.resized_image)
            
            # Update info
            original_size = self.original_image.size
            self.info_label.config(
                text=f"Original: {original_size[0]} x {original_size[1]} → "
                     f"Resized: {target_width} x {target_height} pixels"
            )
            
            # Enable save button
            self.save_btn.config(state='normal')
            
            messagebox.showinfo("Success", "Image resized successfully!\nClick 'Save As...' to save the image.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to resize image: {str(e)}")
    
    def show_image_preview(self, image):
        # Calculate preview size (fit within 380x380 to leave some padding)
        img_width, img_height = image.size
        max_preview_size = 380
        
        if img_width > max_preview_size or img_height > max_preview_size:
            ratio = min(max_preview_size / img_width, max_preview_size / img_height)
            preview_width = int(img_width * ratio)
            preview_height = int(img_height * ratio)
            preview_img = image.resize((preview_width, preview_height), Image.Resampling.LANCZOS)
        else:
            preview_img = image.copy()
        
        # Convert to PhotoImage
        self.preview_image = ImageTk.PhotoImage(preview_img)
        
        # Clear canvas and display image
        self.preview_canvas.delete("all")
        
        # Center the image in the canvas
        canvas_width = 400
        canvas_height = 400
        img_x = (canvas_width - preview_img.size[0]) // 2
        img_y = (canvas_height - preview_img.size[1]) // 2
        
        self.preview_canvas.create_image(img_x, img_y, anchor=tk.NW, image=self.preview_image)
    
    def save_image(self):
        if not self.resized_image:
            messagebox.showwarning("Warning", "Please resize an image first")
            return
        
        # Get file extension from original file or default to jpg
        if self.file_path:
            original_ext = os.path.splitext(self.file_path)[1].lower()
            if not original_ext:
                original_ext = '.jpg'
        else:
            original_ext = '.jpg'
        
        # File dialog for saving
        file_types = [
            ("JPEG files", "*.jpg"),
            ("PNG files", "*.png"),
            ("BMP files", "*.bmp"),
            ("TIFF files", "*.tiff"),
            ("All files", "*.*")
        ]
        
        save_path = filedialog.asksaveasfilename(
            title="Save resized image",
            defaultextension=original_ext,
            filetypes=file_types
        )
        
        if save_path:
            try:
                # Get quality setting
                quality = int(self.quality_var.get())
                quality = max(1, min(100, quality))
                
                # Save image based on format
                file_ext = os.path.splitext(save_path)[1].lower()
                
                if file_ext in ['.jpg', '.jpeg']:
                    # Convert to RGB if necessary for JPEG
                    if self.resized_image.mode in ('RGBA', 'LA', 'P'):
                        rgb_image = Image.new('RGB', self.resized_image.size, (255, 255, 255))
                        if self.resized_image.mode == 'RGBA':
                            rgb_image.paste(self.resized_image, mask=self.resized_image.split()[-1])
                        else:
                            rgb_image.paste(self.resized_image)
                        rgb_image.save(save_path, 'JPEG', quality=quality, optimize=True)
                    else:
                        self.resized_image.save(save_path, 'JPEG', quality=quality, optimize=True)
                elif file_ext == '.png':
                    self.resized_image.save(save_path, 'PNG', optimize=True)
                else:
                    self.resized_image.save(save_path, optimize=True)
                
                # Show file size info
                file_size = os.path.getsize(save_path)
                if file_size < 1024:
                    size_str = f"{file_size} bytes"
                elif file_size < 1024 * 1024:
                    size_str = f"{file_size / 1024:.1f} KB"
                else:
                    size_str = f"{file_size / (1024 * 1024):.1f} MB"
                
                messagebox.showinfo("Success", 
                    f"Image saved successfully!\n\nFile: {os.path.basename(save_path)}\nSize: {size_str}\nLocation: {save_path}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")

def main():
    root = tk.Tk()
    
    # Set minimum window size
    root.minsize(800, 600)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_reqwidth()
    height = root.winfo_reqheight()
    pos_x = (root.winfo_screenwidth() // 2) - (width // 2)
    pos_y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
    
    app = ImageResizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
