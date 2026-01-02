#!/usr/bin/env python3
"""
Build File Renamer Script
Automatically renames build files with version, date, and project name.
"""

import os
import sys
import argparse
import shutil
from datetime import datetime
from pathlib import Path
import json
import re

class BuildFileRenamer:
    def __init__(self, project_name, version, directory="."):
        self.project_name = project_name
        self.version = version
        self.directory = Path(directory)
        self.build_date = datetime.now().strftime("%Y-%m-%d")
        
        # Define build file extensions
        self.build_extensions = {
            '.apk',   # Android Package
            '.exe',   # Windows Executable
            '.zip',   # Archive
            '.jar',   # Java Archive
            '.war',   # Web Archive
            '.ear',   # Enterprise Archive
            '.msi',   # Windows Installer
            '.dmg',   # macOS Disk Image
            '.deb',   # Debian Package
            '.rpm',   # Red Hat Package
            '.tar.gz', # Compressed Archive
            '.ipa',   # iOS App
            '.appx',  # Windows App Package
        }
    
    def is_build_file(self, file_path):
        """Check if file is a build file based on extension."""
        file_path = Path(file_path)
        
        # Check for .tar.gz specifically
        if file_path.name.endswith('.tar.gz'):
            return True
        
        # Check other extensions
        return file_path.suffix.lower() in self.build_extensions
    
    def sanitize_filename(self, name):
        """Remove invalid characters from filename."""
        # Replace invalid characters with underscore
        invalid_chars = r'[<>:"/\\|?*]'
        return re.sub(invalid_chars, '_', name)
    
    def generate_new_filename(self, original_file):
        """Generate new filename with project name, version, and date."""
        file_path = Path(original_file)
        
        # Handle .tar.gz extension specially
        if file_path.name.endswith('.tar.gz'):
            extension = '.tar.gz'
        else:
            extension = file_path.suffix
        
        # Sanitize project name for filename
        clean_project_name = self.sanitize_filename(self.project_name)
        
        # Generate new filename
        new_name = f"{clean_project_name}_v{self.version}_{self.build_date}{extension}"
        
        return file_path.parent / new_name
    
    def rename_file_safely(self, old_path, new_path):
        """Safely rename file, handling conflicts."""
        old_path = Path(old_path)
        new_path = Path(new_path)
        
        if new_path.exists():
            # If target exists, add counter
            counter = 1
            stem = new_path.stem
            suffix = new_path.suffix
            parent = new_path.parent
            
            while new_path.exists():
                new_name = f"{stem}_{counter:02d}{suffix}"
                new_path = parent / new_name
                counter += 1
        
        try:
            # Rename the file
            old_path.rename(new_path)
            return new_path, True
        except Exception as e:
            print(f"Error renaming {old_path}: {e}")
            return old_path, False
    
    def scan_and_rename(self, dry_run=False):
        """Scan directory and rename build files."""
        if not self.directory.exists():
            print(f"Directory {self.directory} does not exist!")
            return
        
        print(f"Scanning directory: {self.directory.absolute()}")
        print(f"Project: {self.project_name}")
        print(f"Version: {self.version}")
        print(f"Build Date: {self.build_date}")
        print("-" * 50)
        
        renamed_files = []
        skipped_files = []
        
        # Scan for build files
        for file_path in self.directory.iterdir():
            if file_path.is_file() and self.is_build_file(file_path):
                new_path = self.generate_new_filename(file_path)
                
                if dry_run:
                    print(f"WOULD RENAME: {file_path.name} -> {new_path.name}")
                    renamed_files.append((file_path, new_path))
                else:
                    final_path, success = self.rename_file_safely(file_path, new_path)
                    if success:
                        print(f"RENAMED: {file_path.name} -> {final_path.name}")
                        renamed_files.append((file_path, final_path))
                    else:
                        print(f"FAILED: {file_path.name}")
                        skipped_files.append(file_path)
        
        # Summary
        print("-" * 50)
        print(f"Files processed: {len(renamed_files) + len(skipped_files)}")
        print(f"Successfully renamed: {len(renamed_files)}")
        print(f"Failed/Skipped: {len(skipped_files)}")
        
        return renamed_files, skipped_files

def load_config_file(config_path):
    """Load configuration from JSON file."""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"Error loading config file: {e}")
        return {}

def create_sample_config():
    """Create a sample configuration file."""
    config = {
        "project_name": "MyApp",
        "version": "1.0.0",
        "directory": ".",
        "custom_extensions": [".custom", ".special"]
    }
    
    with open("build_renamer_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("Sample configuration file 'build_renamer_config.json' created!")
    print("Edit this file with your project details.")

def main():
    parser = argparse.ArgumentParser(
        description="Rename build files with version, date, and project name",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python build_renamer.py -p "MyApp" -v "1.2.3"
  python build_renamer.py -p "MyApp" -v "1.2.3" -d "./dist" --dry-run
  python build_renamer.py --config config.json
  python build_renamer.py --create-config
        """
    )
    
    parser.add_argument("-p", "--project", help="Project name")
    parser.add_argument("-v", "--version", help="Version number (e.g., 1.2.3)")
    parser.add_argument("-d", "--directory", default=".", help="Directory to scan (default: current)")
    parser.add_argument("--config", help="Path to JSON configuration file")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be renamed without actually renaming")
    parser.add_argument("--create-config", action="store_true", help="Create a sample configuration file")
    
    args = parser.parse_args()
    
    # Create sample config
    if args.create_config:
        create_sample_config()
        return
    
    # Load from config file if specified
    if args.config:
        config = load_config_file(args.config)
        project_name = config.get("project_name")
        version = config.get("version")
        directory = config.get("directory", ".")
    else:
        project_name = args.project
        version = args.version
        directory = args.directory
    
    # Interactive input if not provided
    if not project_name:
        project_name = input("Enter project name: ").strip()
    
    if not version:
        version = input("Enter version (e.g., 1.2.3): ").strip()
    
    if not project_name or not version:
        print("Error: Project name and version are required!")
        sys.exit(1)
    
    # Validate version format
    if not re.match(r'^\d+\.\d+\.\d+', version):
        print("Warning: Version format should be X.Y.Z (e.g., 1.2.3)")
    
    # Create renamer and process files
    renamer = BuildFileRenamer(project_name, version, directory)
    
    try:
        renamed_files, skipped_files = renamer.scan_and_rename(dry_run=args.dry_run)
        
        if args.dry_run:
            print("\nThis was a dry run. Use without --dry-run to actually rename files.")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
