import os
import json
import re

ROOT_DIR = "."
OUTPUT_FILE = os.path.join("portfolio", "data.js")
CATEGORIES = {
    "Web": "Web Development",
    "Python": "Python Scripting",
    "C++": "C++ Systems",
}

def get_project_details(project_path):
    """
    Attempts to read a description and features from a README.md file.
    Also checks for index.html to see if a demo is available.
    """
    readme_path = os.path.join(project_path, "README.md")
    description = "A project built as part of the 21APEXchallenge."
    features = []
    
    if os.path.exists(readme_path):
        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()
                
                # 1. Extract Description (Paragraphs after the first header)
                # Look for the first Header, then grab text until the next Header
                match = re.search(r'^#\s+.*?\n+(.+?)(?=\n#|$)', content, re.MULTILINE | re.DOTALL)
                if match:
                    raw_desc = match.group(1).strip()
                    # Clean up markdown links/images if simple text is preferred, 
                    # but for now we'll just take the first non-empty paragraph.
                    paragraphs = [p.strip() for p in raw_desc.split('\n\n') if p.strip()]
                    if paragraphs:
                        description = paragraphs[0] 
                        if len(description) > 200:
                            description = description[:197] + "..."

                # 2. Extract Features (Bullet points under a "Features" section)
                # This is a heuristic: look for "## Features" or similar
                features_match = re.search(r'(?i)#+\s*Features.*?\n((?:\s*[-*]\s+.+\n?)+)', content)
                if features_match:
                    raw_features = features_match.group(1).strip()
                    # Parse bullet points
                    features = [line.strip().lstrip('-*').strip() for line in raw_features.split('\n') if line.strip()]
                    features = features[:5] # Limit to top 5 features
        except Exception as e:
            print(f"Error reading README for {project_path}: {e}")

    # Check for Demo
    demo_url = None
    if os.path.exists(os.path.join(project_path, "index.html")):
        # Path relative to portfolio/index.html
        # project_path is e.g. "./Web/Scanner"
        # we need "../Web/Scanner/index.html"
        # But wait, logic below calculates relative path for the folder.
        # So we just set a flag or local path.
        demo_url = "index.html"

    return description, features, demo_url

def scan_projects():
    projects = []
    
    for folder, category_name in CATEGORIES.items():
        folder_path = os.path.join(ROOT_DIR, folder)
        if not os.path.exists(folder_path):
            print(f"Warning: {folder_path} does not exist.")
            continue
            
        for project_name in os.listdir(folder_path):
            project_path = os.path.join(folder_path, project_name)
            
            # Skip files, only look at directories
            if not os.path.isdir(project_path):
                continue
                
            print(f"Processing: {project_name}...")
            
            description, features, demo_file = get_project_details(project_path)
            
            # Create a relative link from portfolio/ directory
            relative_path = os.path.join("..", folder, project_name).replace("\\", "/") 
            
            final_demo_url = None
            if demo_file:
                final_demo_url = f"{relative_path}/{demo_file}"

            projects.append({
                "name": project_name.replace("-", " ").replace("_", " "), 
                "original_name": project_name,
                "category": category_name,
                "category_short": folder,
                "path": relative_path,
                "description": description,
                "features": features,
                "demo_url": final_demo_url
            })
            
    return projects

def main():
    # Ensure portfolio dir exists
    os.makedirs("portfolio", exist_ok=True)
    
    projects = scan_projects()
    
    # Sort by category then name
    projects.sort(key=lambda x: (x['category'], x['name']))
    
    # Write to a JS file that sets a global variable
    js_content = f"const projects = {json.dumps(projects, indent=2)};"
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(js_content)
    
    print(f"Successfully generated {OUTPUT_FILE} with {len(projects)} projects.")

if __name__ == "__main__":
    main()
