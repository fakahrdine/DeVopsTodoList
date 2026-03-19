import json
import os
# We import Flask and some helpful tools from it
from flask import Flask, render_template, request, redirect, url_for

# Initialize the Flask application
app = Flask(__name__)

# Same exact file used by our CLI and GUI versions!
TODO_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

def save_tasks(tasks):
    with open(TODO_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# @app.route defines the URL for this function. '/' is the homepage.
@app.route('/')
def index():
    # 1. Load the tasks from JSON
    tasks = load_tasks()
    
    # 2. Render the HTML file, passing the tasks list into the template!
    return render_template('index.html', tasks=tasks)

# This route only accepts POST requests (form submissions)
@app.route('/add', methods=['POST'])
def add():
    # request.form grabs inputs from HTML forms using the 'name' attribute
    title = request.form.get('title')
    
    if title:
        tasks = load_tasks()
        tasks.append({"title": title, "completed": False})
        save_tasks(tasks)
        
    # Redirect the user back to the homepage
    return redirect(url_for('index'))

# URL variables! <int:task_id> captures the number passed in the URL (e.g. /complete/0)
@app.route('/complete/<int:task_id>', methods=['POST'])
def complete(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]['completed'] = True
        save_tasks(tasks)
        
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        del tasks[task_id]
        save_tasks(tasks)
        
    return redirect(url_for('index'))

if __name__ == "__main__":
    # Start the web server! debug=True allows it to auto-reload if we change the code.
    app.run(debug=True)
