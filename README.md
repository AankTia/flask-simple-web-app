# Building a CRUD Web Application with Python (Flask): Step-by-Step Guide

Comprehensive step-by-step guide for building a CRUD web application with Python (Flask). This tutorial uses:

- Flask as the web framework
- SQLAlchemy for database operations
- SQLite as the database system
- HTML templates for the frontend

The guide takes you through:

1. Setting up your project environment
2. Creating the database connection
3. Building your data models
4. Implementing CRUD routes
5. Creating HTML templates
6. Testing your application

The tutorial creates a simple task management application that demonstrates all four CRUD operations:
- Create: Add new tasks
- Read: View task list and individual tasks
- Update: Edit task details and toggle completion status
- Delete: Remove tasks

# Building a CRUD Web Application with Python (Flusk)

This tutorial will guide you through building a complete CRUD (Create, Read, Update, Delete) web application using Python, Flask, and SQLite. By the end, you'll have a working task management application.

## Prerequisites
- Python 3.6+ installed
- Basic understanding of Python
- Basic understanding of HTML/CSS
- Basic knowledge of SQL

## Table of Contents
1. [Project Setup](#1-project-setup)
2. [Database Setup](#2-database-setup)
3. [Creating the Flask Application](#3-creating-the-flask-application)
4. [Building the Models](#4-building-the-models)
5. [Creating Routes and Views](#5-creating-routes-and-views)
6. [Building Templates](#6-building-templates)
7. [Testing Your Application](#7-testing-your-application)
8. [Additional Enhancements](#8-additional-enhancements)

## 1. Project Setup

First, let's set up our project environment:

```bash
# Create a project directory
mkdir flask_crud_app
cd flask_crud_app

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install flask flask-sqlalchemy
```

## 2. Database Setup

We'll use SQLite with Flask-SQLAlchemy for our database management:

```python
# Create a file named database.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

## 3. Creating the Flask Application

Now let's create our main application file:

```python
# Create a file named app.py
from flask import Flask
from database import db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    # Register blueprints (we'll create these later)
    from routes import main
    app.register_blueprint(main)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
```

## 4. Building the Models

Create a models file for our database schema:

```python
# Create a file named models.py
from database import db
from datetime import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Task('{self.title}', '{self.completed}')"
```

## 5. Creating Routes and Views

Let's create our routes for the CRUD operations:

```python
# Create a file named routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import db
from models import Task

main = Blueprint('main', __name__)

@main.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@main.route('/task/new', methods=['GET', 'POST'])
def new_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        if not title:
            flash('Title is required!')
            return redirect(url_for('main.new_task'))
        
        task = Task(title=title, description=description)
        db.session.add(task)
        db.session.commit()
        
        return redirect(url_for('main.index'))
    
    return render_template('create_task.html')

@main.route('/task/<int:task_id>', methods=['GET'])
def view_task(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('view_task.html', task=task)

@main.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        task.completed = 'completed' in request.form
        
        db.session.commit()
        return redirect(url_for('main.index'))
    
    return render_template('edit_task.html', task=task)

@main.route('/task/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/task/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('main.index'))
```

## 6. Building Templates

Now, let's create our HTML templates:

First, create a templates directory:
```bash
mkdir templates
```

### Base template (templates/base.html)
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Task Manager</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .task {
            border: 1px solid #ddd;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
        }
        .task.completed {
            background-color: #f8f8f8;
            text-decoration: line-through;
        }
        .actions {
            margin-top: 10px;
        }
        .actions a, .actions button {
            margin-right: 10px;
        }
        form {
            margin-bottom: 20px;
        }
        label, input, textarea {
            display: block;
            margin-bottom: 10px;
        }
        input[type="text"], textarea {
            width: 100%;
            padding: 8px;
        }
        input[type="submit"], button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        input[type="submit"]:hover, button:hover {
            background-color: #45a049;
        }
        .btn-danger {
            background-color: #f44336;
        }
        .btn-danger:hover {
            background-color: #d32f2f;
        }
        .flash {
            padding: 10px;
            margin-bottom: 10px;
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <h1>Task Manager</h1>
    <nav>
        <a href="{{ url_for('main.index') }}">Home</a> |
        <a href="{{ url_for('main.new_task') }}">New Task</a>
    </nav>
    <hr>
    
    {% with messages = get_flashed_messages() %}
        {% if messages %}
            {% for message in messages %}
                <div class="flash">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}
    
    {% block content %}{% endblock %}
</body>
</html>
```

### Index page (templates/index.html)
```html
{% extends 'base.html' %}

{% block content %}
    <h2>All Tasks</h2>
    
    {% if tasks %}
        {% for task in tasks %}
            <div class="task {% if task.completed %}completed{% endif %}">
                <h3>{{ task.title }}</h3>
                <p>{{ task.description }}</p>
                <p>Created: {{ task.created_at.strftime('%Y-%m-%d %H:%M') }}</p>
                <p>Status: {% if task.completed %}Completed{% else %}Pending{% endif %}</p>
                
                <div class="actions">
                    <a href="{{ url_for('main.view_task', task_id=task.id) }}">View</a>
                    <a href="{{ url_for('main.edit_task', task_id=task.id) }}">Edit</a>
                    <form action="{{ url_for('main.toggle_task', task_id=task.id) }}" method="POST" style="display: inline;">
                        <button type="submit">
                            {% if task.completed %}Mark as Pending{% else %}Mark as Completed{% endif %}
                        </button>
                    </form>
                    <form action="{{ url_for('main.delete_task', task_id=task.id) }}" method="POST" style="display: inline;">
                        <button type="submit" class="btn-danger">Delete</button>
                    </form>
                </div>
            </div>
        {% endfor %}
    {% else %}
        <p>No tasks yet. <a href="{{ url_for('main.new_task') }}">Create one</a>!</p>
    {% endif %}
{% endblock %}
```

### Create Task page (templates/create_task.html)
```html
{% extends 'base.html' %}

{% block content %}
    <h2>Create New Task</h2>
    
    <form method="POST">
        <div>
            <label for="title">Title</label>
            <input type="text" id="title" name="title" required>
        </div>
        
        <div>
            <label for="description">Description</label>
            <textarea id="description" name="description" rows="4"></textarea>
        </div>
        
        <div>
            <input type="submit" value="Create Task">
        </div>
    </form>
{% endblock %}
```

### View Task page (templates/view_task.html)
```html
{% extends 'base.html' %}

{% block content %}
    <h2>Task Details</h2>
    
    <div class="task {% if task.completed %}completed{% endif %}">
        <h3>{{ task.title }}</h3>
        <p>{{ task.description }}</p>
        <p>Created: {{ task.created_at.strftime('%Y-%m-%d %H:%M') }}</p>
        <p>Status: {% if task.completed %}Completed{% else %}Pending{% endif %}</p>
        
        <div class="actions">
            <a href="{{ url_for('main.edit_task', task_id=task.id) }}">Edit</a>
            <form action="{{ url_for('main.toggle_task', task_id=task.id) }}" method="POST" style="display: inline;">
                <button type="submit">
                    {% if task.completed %}Mark as Pending{% else %}Mark as Completed{% endif %}
                </button>
            </form>
            <form action="{{ url_for('main.delete_task', task_id=task.id) }}" method="POST" style="display: inline;">
                <button type="submit" class="btn-danger">Delete</button>
            </form>
        </div>
    </div>
    
    <a href="{{ url_for('main.index') }}">Back to Tasks</a>
{% endblock %}
```

### Edit Task page (templates/edit_task.html)
```html
{% extends 'base.html' %}

{% block content %}
    <h2>Edit Task</h2>
    
    <form method="POST">
        <div>
            <label for="title">Title</label>
            <input type="text" id="title" name="title" value="{{ task.title }}" required>
        </div>
        
        <div>
            <label for="description">Description</label>
            <textarea id="description" name="description" rows="4">{{ task.description }}</textarea>
        </div>
        
        <div>
            <label>
                <input type="checkbox" name="completed" {% if task.completed %}checked{% endif %}>
                Completed
            </label>
        </div>
        
        <div>
            <input type="submit" value="Update Task">
        </div>
    </form>
    
    <a href="{{ url_for('main.index') }}">Cancel</a>
{% endblock %}
```

## 7. Testing Your Application

Now, run your application:

```bash
python app.py
```

Open your web browser and navigate to `http://localhost:5000/`. You should see your task manager application up and running!

## 8. Additional Enhancements

Here are some ideas to enhance your CRUD application:

1. **User Authentication**:
   - Add user registration and login functionality
   - Associate tasks with specific users

2. **Categories or Tags**:
   - Allow categorizing tasks
   - Add filtering by categories

3. **Due Dates**:
   - Add due dates to tasks
   - Implement sorting and filtering by due dates

4. **Search Functionality**:
   - Add a search bar to find specific tasks

5. **API Endpoints**:
   - Create API endpoints for your CRUD operations
   - Implement token-based authentication

6. **Improved UI**:
   - Use a CSS framework like Bootstrap or Tailwind CSS
   - Add JavaScript for dynamic interactions

## Project Structure

Your final project structure should look like this:

```
flask_crud_app/
│
├── venv/
├── app.py
├── database.py
├── models.py
├── routes.py
│
└── templates/
    ├── base.html
    ├── index.html
    ├── create_task.html
    ├── view_task.html
    └── edit_task.html
```

This completes your basic CRUD web application using Python and Flask. You now have a foundation that you can extend and customize based on your specific requirements.
