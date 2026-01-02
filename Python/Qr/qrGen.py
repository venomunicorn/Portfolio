import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import qrcode
from PIL import Image, ImageTk
import cv2
from pyzbar import pyzbar
import os
import io
import base64
import tempfile
import pyperclip
import mimetypes
import re
from datetime import datetime

class QRCodeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Main window configuration
        self.title('QR Code Generator & Decoder')
        self.geometry('1200x800')  # Wider window for split layout
        self.configure(bg='#f8fafc')
        self.resizable(True, True)
        
        # Configure modern styling
        self.setup_styles()
        
        # Create main notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=25, pady=20)
        
        # Create tabs
        self.generate_tab = ttk.Frame(self.notebook)
        self.decode_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.generate_tab, text='  Generate QR  ')
        self.notebook.add(self.decode_tab, text='  Decode QR  ')
        
        # Initialize tab components
        self.setup_generate_tab()
        self.setup_decode_tab()
        
        # Initialize variables
        self.generated_qr_img = None
        self.generated_qr_display = None
        self.decoded_qr_display = None
        self.last_generated_data = ""
        
    def setup_styles(self):
        """Configure modern pastel styling for the application"""
        style = ttk.Style(self)
        style.theme_use('clam')
        
        # Configure notebook and tabs
        style.configure('TNotebook', background='#f8fafc', borderwidth=0)
        style.configure('TNotebook.Tab', 
                       background='#e2e8f0', 
                       padding=[20, 12], 
                       font=('Segoe UI', 11, 'bold'),
                       borderwidth=0)
        style.map('TNotebook.Tab', 
                 background=[('selected', '#cbd5e1')],
                 foreground=[('selected', '#1e293b')])
        
        # Configure frames and labels
        style.configure('TFrame', background='#f8fafc')
        style.configure('TLabel', background='#f8fafc', 
                       font=('Segoe UI', 11), foreground='#475569')
        style.configure('Header.TLabel', 
                       font=('Segoe UI', 16, 'bold'), 
                       foreground='#1e293b')
        style.configure('Section.TLabel', 
                       font=('Segoe UI', 12, 'bold'), 
                       foreground='#334155')
        
        # Configure buttons with rounded appearance
        style.configure('TButton', 
                       font=('Segoe UI', 10, 'bold'),
                       padding=[12, 8],
                       relief='flat')
        style.map('TButton',
                 background=[('active', '#a5b4fc'), ('!active', '#c7d2fe')],
                 foreground=[('active', '#1e1b4b'), ('!active', '#3730a3')])
        
        # Configure entry fields
        style.configure('TEntry', 
                       font=('Segoe UI', 11),
                       padding=[8, 6])
        
        # Configure radiobuttons
        style.configure('TRadiobutton', 
                       background='#f8fafc',
                       font=('Segoe UI', 10),
                       padding=[5, 3])
    
    def setup_generate_tab(self):
        """Setup the QR code generation tab with split layout"""
        frame = self.generate_tab
        
        # **SPLIT LAYOUT: Create left and right panels**
        main_paned = ttk.PanedWindow(frame, orient='horizontal')
        main_paned.pack(expand=True, fill='both', padx=10, pady=10)
        
        # LEFT PANEL: Input controls
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)
        
        # RIGHT PANEL: QR display and controls
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=1)
        
        # === LEFT PANEL CONTENT ===
        
        # Header
        header_frame = ttk.Frame(left_frame)
        header_frame.pack(fill='x', pady=(10, 15))
        
        ttk.Label(header_frame, text='QR Code Generator', 
                 style='Header.TLabel').pack()
        ttk.Label(header_frame, text='Create QR codes for various types of data', 
                 font=('Segoe UI', 10), foreground='#64748b').pack()
        
        # QR Type Selection
        type_frame = ttk.LabelFrame(left_frame, text='  Input Type  ', padding=15)
        type_frame.pack(fill='x', padx=10, pady=10)
        
        self.qr_type_var = tk.StringVar(value='text')
        
        qr_types = [
            ('📝 Plain Text', 'text'),
            ('🔗 URL', 'url'),
            ('👤 Contact (vCard)', 'vcard'),
            ('📶 WiFi', 'wifi'),
            ('📄 File Info', 'file')
        ]
        
        # Arrange radio buttons in a more compact way
        for i, (text, value) in enumerate(qr_types):
            rb = ttk.Radiobutton(type_frame, text=text, 
                               variable=self.qr_type_var, value=value,
                               command=self.update_input_fields)
            rb.pack(anchor='w', pady=2)
        
        # Dynamic input fields container
        self.input_frame = ttk.LabelFrame(left_frame, text='  Input Data  ', padding=15)
        self.input_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.input_widgets = {}
        self.create_input_fields('text')
        
        # Generate button and auto-save
        control_frame = ttk.Frame(left_frame)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        self.generate_btn = ttk.Button(control_frame, text='🔄 Generate QR Code', 
                                     command=self.generate_qr_code)
        self.generate_btn.pack(pady=(0, 10))
        
        # Auto-save checkbox
        self.auto_save_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(control_frame, text='Auto-save QR code with custom filename', 
                       variable=self.auto_save_var).pack()
        
        # === RIGHT PANEL CONTENT ===
        
        # QR Code display header
        display_header = ttk.Frame(right_frame)
        display_header.pack(fill='x', pady=(10, 10))
        
        ttk.Label(display_header, text='Generated QR Code Preview', 
                 style='Section.TLabel').pack()
        
        # QR Code display
        display_frame = ttk.LabelFrame(right_frame, text='  QR Code Preview  ', padding=15)
        display_frame.pack(fill='both', expand=True, padx=10)
        
        # Create QR canvas
        self.qr_canvas = tk.Canvas(display_frame, 
                                  width=450, height=450,
                                  bg='#ffffff', 
                                  relief='solid', 
                                  bd=2,
                                  highlightthickness=0)
        self.qr_canvas.pack(pady=10)
        
        # Add placeholder text
        self.qr_canvas.create_text(225, 225,
                                  text='QR Code will appear here\nafter generation\n(Large Preview)', 
                                  font=('Segoe UI', 14), 
                                  fill='#94a3b8',
                                  justify='center',
                                  tags='placeholder')
        
        # Save options
        save_frame = ttk.Frame(display_frame)
        save_frame.pack(pady=15)
        
        self.save_btn = ttk.Button(save_frame, text='💾 Save As...', 
                                  command=self.save_qr_image, state='disabled')
        self.save_btn.pack(side='left', padx=5)
        
        self.copy_btn = ttk.Button(save_frame, text='📋 Copy Data', 
                                  command=self.copy_qr_info, state='disabled')
        self.copy_btn.pack(side='left', padx=5)
        
        # Auto-saved file info
        self.auto_save_label = ttk.Label(display_frame, text='', 
                                        font=('Segoe UI', 10), 
                                        foreground='#059669',
                                        wraplength=400)
        self.auto_save_label.pack(pady=5)
        
        # Additional info panel
        info_frame = ttk.LabelFrame(right_frame, text='  Quick Info  ', padding=10)
        info_frame.pack(fill='x', padx=10, pady=(10, 0))
        
        info_text = """• QR codes are saved in high resolution (300 DPI)
• Auto-save creates a 'QR_Codes' folder
• Filenames are generated from your input data
• Large preview shows actual QR code size"""
        
        ttk.Label(info_frame, text=info_text, 
                 font=('Segoe UI', 9), 
                 foreground='#64748b',
                 justify='left').pack(anchor='w')
    
    def setup_decode_tab(self):
        """Setup the QR code decoding tab with split layout"""
        frame = self.decode_tab
        
        # **SPLIT LAYOUT: Create left and right panels**
        main_paned = ttk.PanedWindow(frame, orient='horizontal')
        main_paned.pack(expand=True, fill='both', padx=10, pady=10)
        
        # LEFT PANEL: Upload controls and decoded data
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)
        
        # RIGHT PANEL: Image display
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=1)
        
        # === LEFT PANEL CONTENT ===
        
        # Header
        header_frame = ttk.Frame(left_frame)
        header_frame.pack(fill='x', pady=(10, 15))
        
        ttk.Label(header_frame, text='QR Code Decoder', 
                 style='Header.TLabel').pack()
        ttk.Label(header_frame, text='Upload and decode existing QR codes', 
                 font=('Segoe UI', 10), foreground='#64748b').pack()
        
        # Upload section
        upload_frame = ttk.LabelFrame(left_frame, text='  Upload QR Code  ', padding=15)
        upload_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(upload_frame, text='📁 Select Image File', 
                  command=self.upload_qr_image).pack(pady=10)
        
        # Decoded data display
        result_frame = ttk.LabelFrame(left_frame, text='  Decoded Data  ', padding=15)
        result_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Text display with scrollbar
        text_container = ttk.Frame(result_frame)
        text_container.pack(fill='both', expand=True, pady=10)
        
        self.decoded_text = tk.Text(text_container, height=15, font=('Consolas', 11),
                                   wrap='word', relief='solid', bd=1)
        scrollbar = ttk.Scrollbar(text_container, orient='vertical', 
                                command=self.decoded_text.yview)
        self.decoded_text.configure(yscrollcommand=scrollbar.set)
        
        self.decoded_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Action buttons
        action_frame = ttk.Frame(result_frame)
        action_frame.pack(pady=10)
        
        ttk.Button(action_frame, text='📋 Copy to Clipboard', 
                  command=self.copy_decoded_text).pack(side='left', padx=5)
        ttk.Button(action_frame, text='💾 Save as Text File', 
                  command=self.save_decoded_text).pack(side='left', padx=5)
        
        # === RIGHT PANEL CONTENT ===
        
        # Display header
        display_header = ttk.Frame(right_frame)
        display_header.pack(fill='x', pady=(10, 10))
        
        ttk.Label(display_header, text='Uploaded QR Code Image', 
                 style='Section.TLabel').pack()
        
        # Image display
        image_frame = ttk.LabelFrame(right_frame, text='  Image Preview  ', padding=15)
        image_frame.pack(fill='both', expand=True, padx=10)
        
        self.decode_canvas = tk.Canvas(image_frame, 
                                     width=450, height=450,
                                     bg='#ffffff', 
                                     relief='solid', 
                                     bd=2,
                                     highlightthickness=0)
        self.decode_canvas.pack(pady=10)
        
        # Add placeholder text for decode canvas
        self.decode_canvas.create_text(225, 225,
                                     text='Upload QR code image\nto see it here\n(Large Preview)', 
                                     font=('Segoe UI', 14), 
                                     fill='#94a3b8',
                                     justify='center',
                                     tags='placeholder')
        
        # Decode info panel
        decode_info_frame = ttk.LabelFrame(right_frame, text='  Decode Info  ', padding=10)
        decode_info_frame.pack(fill='x', padx=10, pady=(10, 0))
        
        decode_info_text = """• Supports PNG, JPG, BMP, GIF, TIFF formats
• Automatically detects and decodes QR codes
• Decoded data appears in the left panel
• Copy or save decoded content easily"""
        
        ttk.Label(decode_info_frame, text=decode_info_text, 
                 font=('Segoe UI', 9), 
                 foreground='#64748b',
                 justify='left').pack(anchor='w')
    
    def update_input_fields(self):
        """Update input fields based on selected QR type"""
        qr_type = self.qr_type_var.get()
        
        # Clear existing widgets
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        self.input_widgets.clear()
        
        self.create_input_fields(qr_type)
        self.reset_display()
    
    def create_input_fields(self, qr_type):
        """Create appropriate input fields for the selected QR type"""
        if qr_type in ['text', 'url']:
            label_text = 'Enter your text:' if qr_type == 'text' else 'Enter URL:'
            ttk.Label(self.input_frame, text=label_text).pack(anchor='w', pady=(0, 5))
            
            entry = tk.Text(self.input_frame, height=4, font=('Segoe UI', 11),
                           wrap='word', relief='solid', bd=1)
            entry.pack(fill='both', expand=True, pady=(0, 10))
            self.input_widgets['text'] = entry
            
        elif qr_type == 'vcard':
            # vCard contact fields - more compact layout
            fields = [
                ('First Name *', 'first_name'),
                ('Last Name *', 'last_name'),
                ('Organization', 'organization'),
                ('Job Title', 'title'),
                ('Phone Number', 'phone'),
                ('Email Address', 'email'),
                ('Website', 'url')
            ]
            
            for label, key in fields:
                ttk.Label(self.input_frame, text=label).pack(anchor='w', pady=(5, 2))
                entry = ttk.Entry(self.input_frame, font=('Segoe UI', 11))
                entry.pack(fill='x', pady=(0, 5))
                self.input_widgets[key] = entry
                
        elif qr_type == 'wifi':
            # WiFi credential fields
            ttk.Label(self.input_frame, text='Network Name (SSID) *').pack(anchor='w', pady=(0, 2))
            ssid_entry = ttk.Entry(self.input_frame, font=('Segoe UI', 11))
            ssid_entry.pack(fill='x', pady=(0, 10))
            self.input_widgets['ssid'] = ssid_entry
            
            ttk.Label(self.input_frame, text='Password').pack(anchor='w', pady=(0, 2))
            pwd_entry = ttk.Entry(self.input_frame, font=('Segoe UI', 11), show='*')
            pwd_entry.pack(fill='x', pady=(0, 10))
            self.input_widgets['password'] = pwd_entry
            
            ttk.Label(self.input_frame, text='Security Type').pack(anchor='w', pady=(0, 2))
            self.wifi_security_var = tk.StringVar(value='WPA')
            security_combo = ttk.Combobox(self.input_frame, textvariable=self.wifi_security_var,
                                        values=['WPA', 'WEP', 'nopass'], state='readonly')
            security_combo.pack(fill='x', pady=(0, 10))
            self.input_widgets['security'] = self.wifi_security_var
            
        elif qr_type == 'file':
            # File selection
            ttk.Label(self.input_frame, text='Select File').pack(anchor='w', pady=(0, 5))
            
            file_frame = ttk.Frame(self.input_frame)
            file_frame.pack(fill='x', pady=(0, 10))
            
            file_entry = ttk.Entry(file_frame, font=('Segoe UI', 11))
            file_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
            
            ttk.Button(file_frame, text='Browse...', 
                      command=self.browse_file).pack(side='right')
            
            self.input_widgets['file_path'] = file_entry
    
    def browse_file(self):
        """Open file browser for file selection"""
        file_path = filedialog.askopenfilename(
            title='Select file to encode information about',
            filetypes=[
                ('All Files', '*.*'),
                ('PDF Files', '*.pdf'),
                ('Image Files', '*.png *.jpg *.jpeg *.gif *.bmp'),
                ('Document Files', '*.doc *.docx *.txt *.rtf'),
            ]
        )
        if file_path:
            self.input_widgets['file_path'].delete(0, tk.END)
            self.input_widgets['file_path'].insert(0, file_path)
    
    def sanitize_filename(self, text):
        """Create a safe filename from text"""
        # Remove or replace invalid filename characters
        text = re.sub(r'[<>:"/\\|?*]', '_', text)
        text = re.sub(r'[^\w\s-]', '', text).strip()
        text = re.sub(r'[-\s]+', '_', text)
        # Limit length and ensure it's not empty
        text = text[:50] if text else "qr_code"
        return text
    
    def generate_filename_from_data(self, qr_type, data):
        """Generate filename based on QR type and data"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if qr_type == 'text':
            # Use first 30 characters of text
            clean_text = self.sanitize_filename(data[:30])
            return f"{clean_text}_{timestamp}.png"
            
        elif qr_type == 'url':
            # Extract domain from URL
            try:
                from urllib.parse import urlparse
                domain = urlparse(data).netloc.replace('www.', '')
                clean_domain = self.sanitize_filename(domain)
                return f"url_{clean_domain}_{timestamp}.png"
            except:
                return f"url_{timestamp}.png"
                
        elif qr_type == 'vcard':
            # Use person's name
            first_name = self.input_widgets['first_name'].get().strip()
            last_name = self.input_widgets['last_name'].get().strip()
            clean_name = self.sanitize_filename(f"{first_name}_{last_name}")
            return f"contact_{clean_name}_{timestamp}.png"
            
        elif qr_type == 'wifi':
            # Use WiFi SSID
            ssid = self.input_widgets['ssid'].get().strip()
            clean_ssid = self.sanitize_filename(ssid)
            return f"wifi_{clean_ssid}_{timestamp}.png"
            
        elif qr_type == 'file':
            # Use original filename
            file_path = self.input_widgets['file_path'].get().strip()
            if file_path:
                original_name = os.path.splitext(os.path.basename(file_path))[0]
                clean_name = self.sanitize_filename(original_name)
                return f"file_{clean_name}_{timestamp}.png"
        
        return f"qr_code_{timestamp}.png"
    
    def generate_qr_code(self):
        """Generate QR code based on input data with auto-save"""
        qr_type = self.qr_type_var.get()
        
        try:
            # Get data based on QR type
            if qr_type == 'text':
                data = self.input_widgets['text'].get('1.0', tk.END).strip()
                if not data:
                    raise ValueError('Please enter some text to generate QR code.')
                    
            elif qr_type == 'url':
                data = self.input_widgets['text'].get('1.0', tk.END).strip()
                if not data:
                    raise ValueError('Please enter a URL to generate QR code.')
                if not data.startswith(('http://', 'https://')):
                    data = 'https://' + data
                    
            elif qr_type == 'vcard':
                # Generate vCard format
                first_name = self.input_widgets['first_name'].get().strip()
                last_name = self.input_widgets['last_name'].get().strip()
                
                if not first_name or not last_name:
                    raise ValueError('First name and last name are required.')
                
                vcard_data = [
                    'BEGIN:VCARD',
                    'VERSION:3.0',
                    f'N:{last_name};{first_name};;;',
                    f'FN:{first_name} {last_name}',
                ]
                
                optional_fields = [
                    ('organization', 'ORG'),
                    ('title', 'TITLE'),
                    ('phone', 'TEL;TYPE=CELL'),
                    ('email', 'EMAIL;TYPE=INTERNET'),
                    ('url', 'URL')
                ]
                
                for field, vcard_field in optional_fields:
                    value = self.input_widgets[field].get().strip()
                    if value:
                        vcard_data.append(f'{vcard_field}:{value}')
                
                vcard_data.append('END:VCARD')
                data = '\n'.join(vcard_data)
                
            elif qr_type == 'wifi':
                # Generate WiFi QR format
                ssid = self.input_widgets['ssid'].get().strip()
                password = self.input_widgets['password'].get().strip()
                security = self.input_widgets['security'].get()
                
                if not ssid:
                    raise ValueError('Network name (SSID) is required.')
                
                # Escape special characters
                def escape_wifi_string(s):
                    return s.replace('\\', '\\\\').replace(';', '\\;').replace(',', '\\,').replace('"', '\\"')
                
                data = f'WIFI:T:{security};S:{escape_wifi_string(ssid)};P:{escape_wifi_string(password)};H:false;;'
                
            elif qr_type == 'file':
                # Generate file information QR
                file_path = self.input_widgets['file_path'].get().strip()
                if not file_path or not os.path.isfile(file_path):
                    raise ValueError('Please select a valid file.')
                
                file_size = os.path.getsize(file_path)
                file_name = os.path.basename(file_path)
                mime_type, _ = mimetypes.guess_type(file_path)
                
                if not mime_type:
                    mime_type = 'application/octet-stream'
                
                # Create file info string
                data = f'FILE_INFO\nName: {file_name}\nSize: {file_size} bytes\nType: {mime_type}\nPath: {file_path}'
            
            # Create QR code with higher resolution
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=15,
                border=4,
            )
            
            qr.add_data(data)
            qr.make(fit=True)
            
            # Generate high-resolution image
            self.generated_qr_img = qr.make_image(fill_color='black', back_color='white')
            
            # Display on canvas
            self.qr_canvas.delete('all')
            
            # Resize image to fit canvas
            canvas_size = 430
            display_img = self.generated_qr_img.resize((canvas_size, canvas_size), Image.LANCZOS)
            
            # Convert to PhotoImage and keep reference
            self.generated_qr_display = ImageTk.PhotoImage(display_img)
            
            # Center position for canvas
            canvas_center_x = 225
            canvas_center_y = 225
            
            # Create image on canvas
            self.qr_canvas.create_image(
                canvas_center_x, canvas_center_y, 
                image=self.generated_qr_display, 
                anchor='center'
            )
            
            # Add border
            border_size = canvas_size // 2
            self.qr_canvas.create_rectangle(
                canvas_center_x - border_size - 5, 
                canvas_center_y - border_size - 5,
                canvas_center_x + border_size + 5, 
                canvas_center_y + border_size + 5, 
                outline='#cbd5e1', 
                width=3
            )
            
            # Store the data
            self.last_generated_data = data
            
            # Auto-save functionality
            if self.auto_save_var.get():
                try:
                    save_dir = "QR_Codes"
                    if not os.path.exists(save_dir):
                        os.makedirs(save_dir)
                    
                    filename = self.generate_filename_from_data(qr_type, data)
                    full_path = os.path.join(save_dir, filename)
                    
                    self.generated_qr_img.save(full_path, dpi=(300, 300))
                    self.auto_save_label.config(text=f"✅ Auto-saved: {filename}")
                    
                except Exception as save_error:
                    self.auto_save_label.config(text=f"❌ Auto-save failed: {str(save_error)}")
            else:
                self.auto_save_label.config(text="")
            
            # Enable buttons
            self.save_btn.config(state='normal')
            self.copy_btn.config(state='normal')
            
            messagebox.showinfo('Success', 'QR Code generated successfully!')
            
        except Exception as e:
            messagebox.showerror('Generation Error', str(e))
    
    def save_qr_image(self):
        """Save the generated QR code as an image file"""
        if not self.generated_qr_img:
            messagebox.showerror('Error', 'No QR code to save.')
            return
        
        suggested_filename = self.generate_filename_from_data(
            self.qr_type_var.get(), 
            self.last_generated_data
        )
        
        file_path = filedialog.asksaveasfilename(
            initialfile=suggested_filename,
            defaultextension='.png',
            filetypes=[
                ('PNG files', '*.png'),
                ('JPEG files', '*.jpg'),
                ('All files', '*.*')
            ],
            title='Save QR Code Image'
        )
        
        if file_path:
            try:
                self.generated_qr_img.save(file_path, dpi=(300, 300))
                messagebox.showinfo('Success', f'QR code saved successfully to:\n{file_path}')
            except Exception as e:
                messagebox.showerror('Save Error', f'Failed to save image: {str(e)}')
    
    def copy_qr_info(self):
        """Copy the QR code data to clipboard"""
        if hasattr(self, 'last_generated_data'):
            try:
                pyperclip.copy(self.last_generated_data)
                messagebox.showinfo('Success', 'QR code data copied to clipboard!')
            except Exception as e:
                messagebox.showerror('Error', f'Failed to copy to clipboard: {str(e)}')
        else:
            messagebox.showwarning('Warning', 'No QR code data to copy.')
    
    def upload_qr_image(self):
        """Upload and decode a QR code image"""
        file_path = filedialog.askopenfilename(
            title='Select QR Code Image',
            filetypes=[
                ('Image files', '*.png *.jpg *.jpeg *.bmp *.gif *.tiff'),
                ('All files', '*.*')
            ]
        )
        
        if not file_path:
            return
        
        try:
            # Load and display image
            img = Image.open(file_path)
            
            # Clear canvas
            self.decode_canvas.delete('all')
            
            # Resize and display image
            display_img = img.resize((430, 430), Image.LANCZOS)
            self.decoded_qr_display = ImageTk.PhotoImage(display_img)
            
            # Center the image
            self.decode_canvas.create_image(225, 225, 
                                          image=self.decoded_qr_display, 
                                          anchor='center')
            
            # Add border
            self.decode_canvas.create_rectangle(
                10, 10, 440, 440, 
                outline='#cbd5e1', 
                width=3
            )
            
            # Decode QR code
            img_cv = cv2.imread(file_path)
            if img_cv is None:
                raise ValueError('Could not load image file.')
            
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            decoded_objects = pyzbar.decode(gray)
            
            if not decoded_objects:
                raise ValueError('No QR code found in the image.')
            
            decoded_data = decoded_objects[0].data.decode('utf-8')
            
            # Display decoded data
            self.decoded_text.delete('1.0', tk.END)
            self.decoded_text.insert('1.0', decoded_data)
            
            messagebox.showinfo('Success', 'QR code decoded successfully!')
            
        except Exception as e:
            messagebox.showerror('Decode Error', f'Failed to decode QR code: {str(e)}')
    
    def copy_decoded_text(self):
        """Copy decoded text to clipboard"""
        text = self.decoded_text.get('1.0', tk.END).strip()
        if text:
            try:
                pyperclip.copy(text)
                messagebox.showinfo('Success', 'Decoded text copied to clipboard!')
            except Exception as e:
                messagebox.showerror('Error', f'Failed to copy to clipboard: {str(e)}')
        else:
            messagebox.showwarning('Warning', 'No text to copy.')
    
    def save_decoded_text(self):
        """Save decoded text to a file"""
        text = self.decoded_text.get('1.0', tk.END).strip()
        if not text:
            messagebox.showwarning('Warning', 'No text to save.')
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension='.txt',
            filetypes=[
                ('Text files', '*.txt'),
                ('All files', '*.*')
            ],
            title='Save Decoded Text'
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                messagebox.showinfo('Success', f'Decoded text saved to:\n{file_path}')
            except Exception as e:
                messagebox.showerror('Save Error', f'Failed to save file: {str(e)}')
    
    def reset_display(self):
        """Reset the QR code display areas"""
        self.qr_canvas.delete('all')
        self.qr_canvas.create_text(225, 225,
                                  text='QR Code will appear here\nafter generation\n(Large Preview)', 
                                  font=('Segoe UI', 14), 
                                  fill='#94a3b8',
                                  justify='center',
                                  tags='placeholder')
        self.save_btn.config(state='disabled')
        self.copy_btn.config(state='disabled')
        self.auto_save_label.config(text='')
        self.generated_qr_img = None
        self.generated_qr_display = None

def main():
    """Main function to run the application"""
    app = QRCodeApp()
    app.mainloop()

if __name__ == '__main__':
    main()
