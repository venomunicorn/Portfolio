# GitHub Profile Picture Downloader Documentation

**Category**: Python Systems / API Tools
**Path**: `Python/githbProfile` (Script: `github_avatar_downloader.py`)
**Version**: 1.0

## Overview
The **GitHub Profile Picture Downloader** is a command-line utility for quickly retrieving high-resolution user avatars from GitHub. It simplifies the process of saving a user's `avatar_url` by interacting with the GitHub User API. It supports inputting either a raw username (e.g., `octocat`) or a full profile URL (e.g., `https://github.com/octocat`).

## Key Features

### 1. Python API Client (`github_avatar_downloader.py`)
- **API Integration**: Sends a GET request to `https://api.github.com/users/{username}` to fetch user metadata in JSON format.
- **Smart Parsing**: Includes a regex helper `extract_username()` that can parse:
  - `octocat` → `octocat`
  - `https://github.com/octocat/repositories` → `octocat`
- **Streamed Downloading**: Uses `requests.get(..., stream=True)` to handle image downloads efficiently, writing to disk in 8KB chunks. This is best practice for handling potentially large binary files.
- **Error Handling**: Catches network errors, 404s (User Not Found), and invalid input formats.

### 2. GUI Application (`gui_main.py`)
- *Note: Provides a desktop form where users can type a name and see the image before saving.*

### 3. Web Demo
The web simulator offers a "Profile Preview" card:
- **Instant Search**: Fetches (simulated) data for users like `torvalds` or `gvanrossum` to display their bio, repo count, and follower count.
- **Visual Feedback**: Shows a loading spinner while "fetching" data.
- **Download Action**: A button that links directly to the `github.com/{user}.png` URL, which is the public shortcut for avatars.

## Architecture

### Directory Structure
```
githbProfile/
├── github_avatar_downloader.py # CLI Script
├── gui_main.py                 # Desktop UI
└── demo.html                   # Web Interface
```

### API Response Structure
The script looks for the `avatar_url` key:
```json
{
  "login": "octocat",
  "id": 1,
  "avatar_url": "https://avatars.githubusercontent.com/u/583231?v=4",
  ...
}
```

## Setup & Execution

### Prerequisites
- Python 3.x
- Libraries: `requests` (`pip install requests`)

### Running the Tool
1.  **Navigate**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\Python\githbProfile"
    ```
2.  **Run**:
    ```powershell
    python github_avatar_downloader.py <username>
    ```

### Examples
- **By Username**:
  ```powershell
  python github_avatar_downloader.py octocat
  # Output: Downloading to: octocat_avatar.png
  ```
- **By URL**:
  ```powershell
  python github_avatar_downloader.py https://github.com/torvalds
  # Output: Downloading to: torvalds_avatar.jpeg
  ```

## Web Demo Usage
- Open `demo.html` in a web browser.
- **Search**: Type "torvalds" and press Enter.
- **View**: See the profile stats (Repos: 6, Followers: 185k).
- **Action**: Click "Download Avatar" to open the image.
