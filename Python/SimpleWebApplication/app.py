from flask import Flask, render_template_string

app = Flask(__name__)

# Basic HTML Template using Jinja2
TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body { font-family: sans-serif; text-align: center; padding: 50px; background: #f0f2f5; }
        .container { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); max-width: 600px; margin: 0 auto; }
        h1 { color: #333; }
        p { color: #666; }
        a { color: #3498db; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ title }}</h1>
        <p>Welcome to this simple Flask Web Application.</p>
        <p>This page is served dynamically by Python.</p>
        <hr>
        <a href="/about">Go to About Page</a>
    </div>
</body>
</html>
"""

ABOUT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About</title>
    <style>
        body { font-family: sans-serif; text-align: center; padding: 50px; background: #e8f5e9; }
        .container { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); max-width: 600px; margin: 0 auto; }
        h1 { color: #2e7d32; }
    </style>
</head>
<body>
    <div class="container">
        <h1>About Us</h1>
        <p>This application demonstrates routing in Flask.</p>
        <p>Created as part of the 21APEXchallenge.</p>
        <hr>
        <a href="/">Back Home</a>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(TEMPLATE, title="Home Page")

@app.route('/about')
def about():
    return render_template_string(ABOUT_TEMPLATE)

if __name__ == '__main__':
    print("Starting Flask App...")
    print("Go to http://127.0.0.1:5000")
    app.run(debug=True)
