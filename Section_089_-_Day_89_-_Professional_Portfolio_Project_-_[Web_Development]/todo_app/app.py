import os
from flask import Flask, render_template, redirect, url_for, flash, request
from models import db, Project, Task
from forms import ProjectForm, TaskForm
from config import Config
from datetime import datetime, timedelta, timezone
from sqlalchemy import func

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def index():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('index.html', projects=projects)

@app.route('/project/new', methods=['GET', 'POST'])
def new_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(name=form.name.data, description=form.description.data)
        db.session.add(project)
        db.session.commit()
        flash('Project created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('project_form.html', form=form, title='New Project')

@app.route('/project/<int:project_id>')
def view_project(project_id):
    project = Project.query.get_or_404(project_id)
    tasks = project.tasks
    todo_tasks = [t for t in tasks if t.status == 'todo']
    doing_tasks = [t for t in tasks if t.status == 'doing']
    done_tasks = [t for t in tasks if t.status == 'done']
    return render_template('project.html', project=project,
                           todo_tasks=todo_tasks, doing_tasks=doing_tasks, done_tasks=done_tasks)

@app.route('/project/<int:project_id>/task/new', methods=['GET', 'POST'])
def new_task(project_id):
    project = Project.query.get_or_404(project_id)
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            status=form.status.data,
            priority=form.priority.data,
            due_date=form.due_date.data if form.due_date.data else None,
            project_id=project.id
        )
        db.session.add(task)
        db.session.commit()
        flash('Task created successfully!', 'success')
        return redirect(url_for('view_project', project_id=project.id))
    return render_template('task_form.html', form=form, project=project, title='New Task')

@app.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.status = form.status.data
        task.priority = form.priority.data
        task.due_date = form.due_date.data if form.due_date.data else None
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('view_project', project_id=task.project_id))
    if task.due_date:
        form.due_date.data = task.due_date.date()
    return render_template('task_form.html', form=form, project=task.project, title='Edit Task')

@app.route('/task/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    project_id = task.project_id
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted!', 'success')
    return redirect(url_for('view_project', project_id=project_id))

@app.route('/task/<int:task_id>/move/<string:status>', methods=['POST'])
def move_task(task_id, status):
    task = Task.query.get_or_404(task_id)
    if status in ['todo', 'doing', 'done']:
        task.status = status
        db.session.commit()
    return redirect(url_for('view_project', project_id=task.project_id))

@app.route('/project/<int:project_id>/delete', methods=['POST'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
