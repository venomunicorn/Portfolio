# Build File Renamer Documentation

**Category**: Python Systems / DevOps
**Path**: `Python/Renamer`
**Version**: 1.0

## Overview
The **Build File Renamer** is a command-line script designed for CI/CD pipelines and DevOps workflows. Its purpose is to standardize build artifact names by appending project metadata (Version, Date) to the filename. This ensures that every release (e.g., `app-release.apk`) becomes uniquely identifiable (e.g., `MyApp_v1.0.0_2023-12-01.apk`) before being archived or deployed.

## Key Features

### 1. Python Automation (`build_renamer.py`)
- **Smart Filtering**: Automatically identifies relevant build files by extension (e.g., `.apk`, `.exe`, `.tar.gz`) while ignoring source code or text files.
- **Sanitization**: Removes unsafe characters from project names to prevent filesystem errors.
- **Collision Handling**: If a file with the target name already exists, it intelligently appends a counter (`_01`, `_02`) instead of overwriting valid data.
- **Dry-Run Mode**: Allows users to preview rename operations without making physical changes (`--dry-run`).
- **Config Support**: Can read project details from a JSON file, enabling version control of the renaming configuration.

### 2. Configuration (`build_renamer_config.json`)
- Stores persistent settings to avoid re-typing flags:
  - `project_name`: The canonical name of the software (e.g., "MyAwesomeApp").
  - `version`: The current semantic version (e.g., "1.2.3").
  - `directory`: The relative path to the build folder (e.g., `./build`).

## Architecture

### Directory Structure
```
Renamer/
├── build_renamer.py        # Core Logic
├── build_renamer_config.json # Config presets
└── testsub/                # Test directory
```

### Renaming Logic
Pattern: `ProjectName_vVersion_YYYY-MM-DD.ext`
Example Transformation:
`app-release-unsigned.apk` → `MyAwesomeApp_v1.2.3_2024-05-20.apk`

## Setup & Execution

### Prerequisites
- Python 3.x

### Running the Tool
1.  **Navigate**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\Python\Renamer"
    ```
2.  **Run (Interactive)**:
    ```powershell
    python build_renamer.py
    ```
    *Prompts: Enter project name / version.*

3.  **Run (CLI)**:
    ```powershell
    python build_renamer.py -p "MyGame" -v "2.0.0" -d "./outputs"
    ```

### Expected Output
```
Scanning directory: ...\Renamer
Project: MyGame
Version: 2.0.0
Build Date: 2024-05-20
--------------------------------------------------
RENAMED: game_build.exe -> MyGame_v2.0.0_2024-05-20.exe
--------------------------------------------------
Files processed: 1
Successfully renamed: 1
```
