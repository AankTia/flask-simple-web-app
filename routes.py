from flask import Blueprint, render_template, request, redirect, url_for,  flash
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
            flash('Title is required')
            return redirect(url_for('main.new_task'))
        
        task = Task(title=title, description=description)
        db.session.add(task)
        db.session.commit()

        return redirect(url_for('main.index'))
    
    return render_template('create_task.html')

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

@main.route('/task/<int:task_id>/toogle', methods=['POST'])
def toogle_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()

    return redirect(url_for('main.index'))