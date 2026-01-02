import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import string
import csv
import os
import base64
import hashlib
from datetime import datetime
import pyperclip

class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("SecurePass Manager")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(True, True)
        
        # File to store passwords
        self.password_file = "passwords.csv"
        
        # Encryption key (in a real app, this should be user-provided)
        self.encryption_key = "SecurePass2024"
        
        # Create GUI
        self.create_widgets()
        self.load_passwords()
        
    def create_widgets(self):
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50', background='#f0f0f0')
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'), foreground='#34495e', background='#f0f0f0')
        style.configure('Custom.TButton', font=('Arial', 10), padding=10)
        style.configure('Custom.TEntry', fieldbackground='#ffffff', borderwidth=2, relief='flat')
        
        # Main container with padding
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="🔐 SecurePass Manager", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True, pady=10)
        
        # Tab 1: Password Generator
        self.create_generator_tab(notebook)
        
        # Tab 2: Password Storage & Retrieval
        self.create_storage_tab(notebook)
        
    def create_generator_tab(self, notebook):
        # Generator tab
        gen_frame = tk.Frame(notebook, bg='#ecf0f1', padx=20, pady=20)
        notebook.add(gen_frame, text="Password Generator")
        
        # Generator section
        gen_section = tk.LabelFrame(gen_frame, text="Generate New Password", 
                                   font=('Arial', 12, 'bold'), fg='#2c3e50', 
                                   bg='#ecf0f1', padx=15, pady=15)
        gen_section.pack(fill='x', pady=(0, 20))
        
        # Username input
        tk.Label(gen_section, text="Username:", font=('Arial', 10), 
                bg='#ecf0f1', fg='#2c3e50').grid(row=0, column=0, sticky='w', pady=5)
        self.username_entry = tk.Entry(gen_section, font=('Arial', 10), width=30, 
                                      relief='flat', bd=5, bg='white')
        self.username_entry.grid(row=0, column=1, columnspan=2, sticky='ew', pady=5, padx=(10, 0))
        
        # Password length
        tk.Label(gen_section, text="Password Length:", font=('Arial', 10), 
                bg='#ecf0f1', fg='#2c3e50').grid(row=1, column=0, sticky='w', pady=5)
        self.length_var = tk.StringVar(value="12")
        length_spinbox = tk.Spinbox(gen_section, from_=4, to=50, textvariable=self.length_var,
                                   font=('Arial', 10), width=10, relief='flat', bd=2)
        length_spinbox.grid(row=1, column=1, sticky='w', pady=5, padx=(10, 0))
        
        # Generate button
        gen_button = tk.Button(gen_section, text="🔑 Generate Password", 
                              command=self.generate_password,
                              font=('Arial', 10, 'bold'), bg='#3498db', fg='white',
                              relief='flat', padx=20, pady=8, cursor='hand2')
        gen_button.grid(row=2, column=0, columnspan=3, pady=15)
        
        # Generated password display
        tk.Label(gen_section, text="Generated Password:", font=('Arial', 10), 
                bg='#ecf0f1', fg='#2c3e50').grid(row=3, column=0, sticky='w', pady=5)
        self.generated_password = tk.StringVar()
        password_entry = tk.Entry(gen_section, textvariable=self.generated_password,
                                 font=('Arial', 10), width=30, relief='flat', bd=5, bg='#f8f9fa')
        password_entry.grid(row=3, column=1, sticky='ew', pady=5, padx=(10, 5))
        
        # Copy button
        copy_button = tk.Button(gen_section, text="📋 Copy", command=self.copy_password,
                               font=('Arial', 9), bg='#27ae60', fg='white',
                               relief='flat', padx=10, pady=5, cursor='hand2')
        copy_button.grid(row=3, column=2, pady=5, padx=(5, 0))
        
        # Save button
        save_button = tk.Button(gen_section, text="💾 Save Password", 
                               command=self.save_password,
                               font=('Arial', 10, 'bold'), bg='#e74c3c', fg='white',
                               relief='flat', padx=20, pady=8, cursor='hand2')
        save_button.grid(row=4, column=0, columnspan=3, pady=15)
        
        gen_section.columnconfigure(1, weight=1)
        
    def create_storage_tab(self, notebook):
        # Storage tab
        storage_frame = tk.Frame(notebook, bg='#ecf0f1', padx=20, pady=20)
        notebook.add(storage_frame, text="Stored Passwords")
        
        # Stored passwords section
        stored_section = tk.LabelFrame(storage_frame, text="Retrieve Stored Passwords", 
                                      font=('Arial', 12, 'bold'), fg='#2c3e50', 
                                      bg='#ecf0f1', padx=15, pady=15)
        stored_section.pack(fill='both', expand=True)
        
        # Username list
        tk.Label(stored_section, text="Select Username:", font=('Arial', 10), 
                bg='#ecf0f1', fg='#2c3e50').pack(anchor='w', pady=(0, 5))
        
        # Listbox with scrollbar
        listbox_frame = tk.Frame(stored_section, bg='#ecf0f1')
        listbox_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        self.username_listbox = tk.Listbox(listbox_frame, font=('Arial', 10), 
                                          selectmode=tk.SINGLE, relief='flat', bd=2,
                                          bg='white', selectbackground='#3498db')
        scrollbar = tk.Scrollbar(listbox_frame, orient='vertical', command=self.username_listbox.yview)
        self.username_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.username_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.username_listbox.bind('<<ListboxSelect>>', self.on_username_select)
        
        # Retrieve button
        retrieve_button = tk.Button(stored_section, text="🔓 Retrieve Password", 
                                   command=self.retrieve_password,
                                   font=('Arial', 10, 'bold'), bg='#9b59b6', fg='white',
                                   relief='flat', padx=20, pady=8, cursor='hand2')
        retrieve_button.pack(pady=10)
        
        # Retrieved password display
        result_frame = tk.Frame(stored_section, bg='#ecf0f1')
        result_frame.pack(fill='x', pady=10)
        
        tk.Label(result_frame, text="Retrieved Password:", font=('Arial', 10), 
                bg='#ecf0f1', fg='#2c3e50').pack(anchor='w')
        
        password_frame = tk.Frame(result_frame, bg='#ecf0f1')
        password_frame.pack(fill='x', pady=(5, 0))
        
        self.retrieved_password = tk.StringVar()
        retrieved_entry = tk.Entry(password_frame, textvariable=self.retrieved_password,
                                  font=('Arial', 10), relief='flat', bd=5, bg='#f8f9fa')
        retrieved_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        # Copy retrieved password button
        copy_retrieved_button = tk.Button(password_frame, text="📋 Copy", 
                                         command=self.copy_retrieved_password,
                                         font=('Arial', 9), bg='#27ae60', fg='white',
                                         relief='flat', padx=10, pady=5, cursor='hand2')
        copy_retrieved_button.pack(side='right')
        
        # Delete button
        delete_button = tk.Button(stored_section, text="🗑️ Delete Selected", 
                                 command=self.delete_password,
                                 font=('Arial', 10), bg='#e74c3c', fg='white',
                                 relief='flat', padx=15, pady=5, cursor='hand2')
        delete_button.pack(pady=10)
        
        # Refresh button
        refresh_button = tk.Button(stored_section, text="🔄 Refresh List", 
                                  command=self.load_passwords,
                                  font=('Arial', 10), bg='#f39c12', fg='white',
                                  relief='flat', padx=15, pady=5, cursor='hand2')
        refresh_button.pack(pady=5)
        
    def generate_password(self):
        """Generate a secure random password"""
        try:
            length = int(self.length_var.get())
            if length < 4:
                messagebox.showerror("Error", "Password length must be at least 4 characters")
                return
                
            # Character sets
            lowercase = string.ascii_lowercase
            uppercase = string.ascii_uppercase
            digits = string.digits
            symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
            
            # Ensure at least one character from each set
            password = [
                random.choice(lowercase),
                random.choice(uppercase),
                random.choice(digits),
                random.choice(symbols)
            ]
            
            # Fill the rest randomly
            all_chars = lowercase + uppercase + digits + symbols
            for _ in range(length - 4):
                password.append(random.choice(all_chars))
            
            # Shuffle the password
            random.shuffle(password)
            
            generated_pass = ''.join(password)
            self.generated_password.set(generated_pass)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid password length")
    
    def copy_password(self):
        """Copy generated password to clipboard"""
        password = self.generated_password.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No password to copy")
    
    def copy_retrieved_password(self):
        """Copy retrieved password to clipboard"""
        password = self.retrieved_password.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No password to copy")
    
    def encrypt_password(self, password):
        """Multi-layer encryption of password"""
        # Layer 1: Caesar cipher
        caesar_shift = 7
        caesar_encrypted = ""
        for char in password:
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                caesar_encrypted += chr((ord(char) - ascii_offset + caesar_shift) % 26 + ascii_offset)
            else:
                caesar_encrypted += char
        
        # Layer 2: Base64 encoding
        base64_encoded = base64.b64encode(caesar_encrypted.encode()).decode()
        
        # Layer 3: Simple XOR with key
        key_hash = hashlib.md5(self.encryption_key.encode()).hexdigest()
        xor_encrypted = ""
        for i, char in enumerate(base64_encoded):
            xor_encrypted += chr(ord(char) ^ ord(key_hash[i % len(key_hash)]))
        
        # Layer 4: Final Base64 encoding
        final_encrypted = base64.b64encode(xor_encrypted.encode()).decode()
        
        return final_encrypted
    
    def decrypt_password(self, encrypted_password):
        """Multi-layer decryption of password"""
        try:
            # Layer 4: Base64 decoding
            xor_encrypted = base64.b64decode(encrypted_password.encode()).decode()
            
            # Layer 3: XOR decryption
            key_hash = hashlib.md5(self.encryption_key.encode()).hexdigest()
            base64_encoded = ""
            for i, char in enumerate(xor_encrypted):
                base64_encoded += chr(ord(char) ^ ord(key_hash[i % len(key_hash)]))
            
            # Layer 2: Base64 decoding
            caesar_encrypted = base64.b64decode(base64_encoded.encode()).decode()
            
            # Layer 1: Caesar cipher decryption
            caesar_shift = 7
            original_password = ""
            for char in caesar_encrypted:
                if char.isalpha():
                    ascii_offset = 65 if char.isupper() else 97
                    original_password += chr((ord(char) - ascii_offset - caesar_shift) % 26 + ascii_offset)
                else:
                    original_password += char
            
            return original_password
        except Exception as e:
            return None
    
    def save_password(self):
        """Save password to CSV file"""
        username = self.username_entry.get().strip()
        password = self.generated_password.get()
        
        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return
        
        if not password:
            messagebox.showerror("Error", "Please generate a password first")
            return
        
        # Check if username already exists
        if os.path.exists(self.password_file):
            with open(self.password_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 2 and row[0] == username:
                        if not messagebox.askyesno("Confirm", 
                            f"Username '{username}' already exists. Do you want to update the password?"):
                            return
                        break
        
        # Encrypt password
        encrypted_password = self.encrypt_password(password)
        
        # Save to CSV
        try:
            # Read existing data
            existing_data = []
            updated = False
            
            if os.path.exists(self.password_file):
                with open(self.password_file, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if len(row) >= 3 and row[0] == username:
                            # Update existing entry
                            existing_data.append([username, encrypted_password, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
                            updated = True
                        else:
                            existing_data.append(row)
            
            # Add new entry if not updated
            if not updated:
                existing_data.append([username, encrypted_password, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            
            # Write back to file
            with open(self.password_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(existing_data)
            
            messagebox.showinfo("Success", f"Password saved successfully for '{username}'!")
            self.load_passwords()  # Refresh the list
            
            # Clear fields
            self.username_entry.delete(0, tk.END)
            self.generated_password.set("")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save password: {str(e)}")
    
    def load_passwords(self):
        """Load usernames from CSV file"""
        self.username_listbox.delete(0, tk.END)
        
        if not os.path.exists(self.password_file):
            return
        
        try:
            with open(self.password_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 2:
                        self.username_listbox.insert(tk.END, row[0])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load passwords: {str(e)}")
    
    def on_username_select(self, event):
        """Handle username selection"""
        selection = self.username_listbox.curselection()
        if selection:
            # Clear previous password
            self.retrieved_password.set("")
    
    def retrieve_password(self):
        """Retrieve and decrypt password for selected username"""
        selection = self.username_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a username")
            return
        
        selected_username = self.username_listbox.get(selection[0])
        
        try:
            with open(self.password_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 2 and row[0] == selected_username:
                        encrypted_password = row[1]
                        decrypted_password = self.decrypt_password(encrypted_password)
                        
                        if decrypted_password:
                            self.retrieved_password.set(decrypted_password)
                            messagebox.showinfo("Success", f"Password retrieved for '{selected_username}'!")
                        else:
                            messagebox.showerror("Error", "Failed to decrypt password")
                        return
                
                messagebox.showerror("Error", f"Password not found for '{selected_username}'")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve password: {str(e)}")
    
    def delete_password(self):
        """Delete selected password entry"""
        selection = self.username_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a username to delete")
            return
        
        selected_username = self.username_listbox.get(selection[0])
        
        if not messagebox.askyesno("Confirm Delete", 
            f"Are you sure you want to delete the password for '{selected_username}'?"):
            return
        
        try:
            # Read existing data
            remaining_data = []
            deleted = False
            
            with open(self.password_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 2 and row[0] == selected_username:
                        deleted = True
                        continue
                    remaining_data.append(row)
            
            if deleted:
                # Write back remaining data
                with open(self.password_file, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(remaining_data)
                
                messagebox.showinfo("Success", f"Password deleted for '{selected_username}'!")
                self.load_passwords()  # Refresh the list
                self.retrieved_password.set("")  # Clear displayed password
            else:
                messagebox.showerror("Error", f"Password not found for '{selected_username}'")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete password: {str(e)}")

def main():
    # Create the main window
    root = tk.Tk()
    
    # Set window icon (optional)
    try:
        # You can add an icon file here if you have one
        # root.iconbitmap('icon.ico')
        pass
    except:
        pass
    
    # Create the password manager application
    app = PasswordManager(root)
    
    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()
