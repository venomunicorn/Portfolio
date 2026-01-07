# Web Scraper Documentation

**Category**: Python Systems / Data Mining
**Path**: `Python/WebScrraper`
**Version**: 1.0

## Overview
The **Web Scraper** is a lightweight extraction tool designed to parse HTML content from URLs. It gathers essential metadata (Page Title) and a list of all hyperlinks (`href` attributes) found on the page, exporting them to a CSV file. This project demonstrates the usage of Python's standard `urllib` and `re` modules for web crawling without relying on heavy external dependencies like Scrapy or Selenium.

## Key Features

### 1. Python Scraper Logic (`main.py`)
- **HTTP Requests**: Uses `urllib.request` to fetch raw HTML. It includes a custom `User-Agent` header ("Mozilla/5.0") to bypass basic anti-bot simple checks that block default Python requests.
- **Regex Parsing**: Instead of an HTML parser, it utilizes Regular Expressions (`re`) to:
  - Extract the page title: `<title>(.*?)</title>`
  - Find all links: `href=["'](http...)["']`
- **CSV Export**: Automatically saves unique links to `scraped_links.csv`, categorizing them by Source URL and Target Link.
- **Demo Mode**: If no URL is provided, it falls back to parsing an internal "Mock HTML" string to demonstrate functionality offline.

### 2. GUI Application (`gui_main.py`)
- *Note: Provides a desktop form where users paste a URL and click a button to start the scrape, with a text area showing the log.*

### 3. Web Demo
The web simulation visualizes the data extraction process:
- **Mock Scraper**: Simulates the delay of network requests with a progress bar.
- **Data Classification**: Distinguishes between **Internal Links** (relative paths like `/about`) and **External Links** (full URLs like `https://google.com`).
- **Live Info**: Shows a dashboard with "Links Found", "Internal", and "External" counts.
- **CSV Download**: Generates a browser-side `.csv` file of the "scraped" results.

## Architecture

### Directory Structure
```
WebScrraper/
├── main.py         # Regex-based Scraper
├── gui_main.py     # Desktop UI
└── demo.html       # Web Simulation
```

### Extraction Workflow
1.  **Input**: `https://example.com`
2.  **Fetch**: Retrive string `<html>...<a href="...">...</html>`
3.  **Regex**: `re.findall` → `['https://google.com', '...']`
4.  **Save**: Write rows to `scraped_links.csv`.

## Setup & Execution

### Prerequisites
- Python 3.x (Built-in libraries only)

### Running the Scraper
1.  **Navigate**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\Python\WebScrraper"
    ```
2.  **Run**:
    ```powershell
    python main.py
    ```

### Expected Output
```
Enter URL to scrape (or press Enter for demo): https://python.org
Fetching https://python.org...

Page Title: Welcome to Python.org
Found 150 unique links.
saved 150 links to scraped_links.csv
```

## Web Demo Usage
- Open `demo.html` in a web browser.
- **Preset**: Click "Wikipedia" to simulate a scrape of that site.
- **Analyze**: See the Internal/External counts update.
- **Export**: Click "Export CSV" to download the results.
