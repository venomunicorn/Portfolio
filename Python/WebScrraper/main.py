import urllib.request
import urllib.error
import re
import csv
import sys

def fetch_html(url):
    try:
        # Mocking headers to avoid basic anti-bot simple checks
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_links(html):
    # Radius-regex to find href="..."
    # Note: This is a simple regex parser, not a full HTML parser like BeautifulSoup
    link_pattern = r'href=["\'](http[s]?://[^"\']+)["\']'
    links = re.findall(link_pattern, html)
    return list(set(links)) # Deduplicate

def extract_title(html):
    title_pattern = r'<title>(.*?)</title>'
    match = re.search(title_pattern, html, re.IGNORECASE)
    return match.group(1) if match else "No Title Found"

def save_to_csv(data, filename="scraped_links.csv"):
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Source', 'Link'])
            writer.writerows(data)
        print(f"saved {len(data)} links to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def run_demo():
    # Use a safe, simple URL or a local string for demo purposes
    url = input("Enter URL to scrape (or press Enter for demo): ").strip()
    
    if not url:
        print("Running Demo Mode (Simulating HTML content)...")
        html_content = """
        <html>
            <head><title>Demo Page</title></head>
            <body>
                <h1>Welcome</h1>
                <a href="https://www.google.com">Google</a>
                <a href="https://www.python.org">Python</a>
                <a href="https://example.com">Example</a>
            </body>
        </html>
        """
        source = "Demo String"
    else:
        print(f"Fetching {url}...")
        html_content = fetch_html(url)
        source = url

    if html_content:
        title = extract_title(html_content)
        print(f"\nPage Title: {title}")
        
        links = extract_links(html_content)
        print(f"Found {len(links)} unique links.")
        
        csv_data = [[source, link] for link in links]
        save_to_csv(csv_data)
    else:
        print("Failed to retrieve content.")

if __name__ == "__main__":
    run_demo()
