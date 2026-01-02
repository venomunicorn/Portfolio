#!/usr/bin/env python3
"""
GitHub Profile Picture Downloader
Downloads a user's profile picture from GitHub given their username or profile URL.
"""

import requests
import re
import os
import sys
from urllib.parse import urlparse
from pathlib import Path

def extract_username(input_str):
    """Extract GitHub username from either a username string or GitHub URL."""
    input_str = input_str.strip()
    
    # Check if it's a URL
    if input_str.startswith(('http://', 'https://')):
        parsed_url = urlparse(input_str)
        if 'github.com' in parsed_url.netloc:
            # Extract username from path (remove leading slash)
            username = parsed_url.path.strip('/').split('/')[0]
            return username
        else:
            raise ValueError("Invalid GitHub URL")
    else:
        # Assume it's a username, validate format
        if re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-])*[a-zA-Z0-9]$|^[a-zA-Z0-9]$', input_str):
            return input_str
        else:
            raise ValueError("Invalid GitHub username format")

def get_avatar_url(username):
    """Get the avatar URL for a GitHub user using the GitHub API."""
    api_url = f"https://api.github.com/users/{username}"
    
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        
        user_data = response.json()
        return user_data.get('avatar_url')
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch user data: {e}")
    except KeyError:
        raise Exception("Avatar URL not found in response")

def download_image(url, filename):
    """Download an image from URL and save it to a file."""
    try:
        response = requests.get(url, timeout=30, stream=True)
        response.raise_for_status()
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        return True
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to download image: {e}")

def main():
    """Main function to handle user input and orchestrate the download."""
    if len(sys.argv) != 2:
        print("Usage: python github_avatar_downloader.py <username_or_url>")
        print("Examples:")
        print("  python github_avatar_downloader.py octocat")
        print("  python github_avatar_downloader.py https://github.com/octocat")
        sys.exit(1)
    
    user_input = sys.argv[1]
    
    try:
        # Extract username from input
        username = extract_username(user_input)
        print(f"Extracting profile picture for user: {username}")
        
        # Get avatar URL from GitHub API
        avatar_url = get_avatar_url(username)
        if not avatar_url:
            print("Error: No avatar found for this user")
            sys.exit(1)
        
        print(f"Avatar URL: {avatar_url}")
        
        # Determine file extension from URL
        parsed_avatar_url = urlparse(avatar_url)
        file_extension = Path(parsed_avatar_url.path).suffix or '.png'
        
        # Create filename
        filename = f"{username}_avatar{file_extension}"
        
        # Download the image
        print(f"Downloading to: {filename}")
        download_image(avatar_url, filename)
        
        print(f"✅ Successfully downloaded profile picture: {filename}")
        
    except ValueError as e:
        print(f"❌ Input Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
