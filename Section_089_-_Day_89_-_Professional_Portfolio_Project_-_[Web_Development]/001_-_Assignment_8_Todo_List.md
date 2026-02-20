# TaskFlow – Complete Project Documentation

## 1. Introduction

**TaskFlow** (also referred to as TaskMaster in some files) is a modern, Kanban‑style task management web application built with Flask. It allows users to create projects, add tasks to them, and organise tasks by status (`todo`, `doing`, `done`) – similar to a Trello board. The application features a clean, responsive user interface styled with Tailwind CSS and FontAwesome icons.

This documentation provides a comprehensive overview of the project’s architecture, data models, routes, templates, forms, and every relationship that makes the application work.

## 2. Project Structure

The project is organised as follows:

```
todo_app/
├── app.py                 # Main Flask application (routes and app factory)
├── config.py              # Configuration class (secret key, database URI)
├── models.py              # SQLAlchemy models (Project, Task)
├── forms.py               # WTForms classes (ProjectForm, TaskForm)
├── init_db.py             # Script to create database tables
├── add_dummy_data.py      # Script to populate the database with random projects/tasks
├── requirements.txt       # Python dependencies
├── README.md              # Basic project overview
├── static/
│   ├── css/
│   │   └── style.css      # Empty (Tailwind is used via CDN)
│   └── js/
│       └── script.js      # Empty (no custom JavaScript yet)
└── templates/
    ├── base.html          # Base template with navigation and footer
    ├── index.html         # Home page listing all projects
    ├── project.html       # Kanban board for a single project
    ├── project_form.html  # Form to create/edit a project
    ├── task_form.html     # Form to create/edit a task
    └── task_card.html     # Reusable card component for a task
```

## 3. Configuration (`config.py`)

The configuration is stored in a class `Config`:

- `SECRET_KEY`: Used for CSRF protection in forms. Falls back to a hard‑coded string if the environment variable is not set.
- `SQLALCHEMY_DATABASE_URI`: Defines the SQLite database location (`app.db` in the project root).
- `SQLALCHEMY_TRACK_MODIFICATIONS`: Disabled to save resources.

```python
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

## 4. Database Models (`models.py`)

SQLAlchemy is used as the ORM. The database contains two tables: `project` and `task`.

### 4.1. Helper function `_get_utc_now()`

Returns a naive UTC datetime (without timezone) for compatibility with SQLite, which does not store timezone information.

```python
def _get_utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)
```

### 4.2. Project Model

| Column       | Type          | Description                                  |
|--------------|---------------|----------------------------------------------|
| `id`         | Integer (PK)  | Unique identifier                            |
| `name`       | String(100)   | Project name (required)                      |
| `description`| String(200)   | Optional description                          |
| `created_at` | DateTime      | Automatically set on creation                 |
| `tasks`      | Relationship  | One-to-many with `Task` (cascade delete)     |

The `tasks` relationship is defined with `lazy=True` (default select) and `cascade='all, delete-orphan'`. This means:
- When a project is deleted, all its tasks are also deleted.
- If a task is removed from the relationship (orphaned), it is deleted automatically.

```python
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=_get_utc_now)
    tasks = db.relationship('Task', backref='project', lazy=True, cascade='all, delete-orphan')
```

### 4.3. Task Model

| Column       | Type          | Description                                      |
|--------------|---------------|--------------------------------------------------|
| `id`         | Integer (PK)  | Unique identifier                                |
| `title`      | String(100)   | Task title (required)                            |
| `description`| Text          | Optional detailed description                    |
| `status`     | String(20)    | One of `todo`, `doing`, `done` (default `todo`)  |
| `priority`   | String(20)    | One of `low`, `medium`, `high` (default `medium`)|
| `due_date`   | DateTime      | Optional due date                                |
| `created_at` | DateTime      | Automatically set on creation                    |
| `updated_at` | DateTime      | Automatically updated on modification            |
| `project_id` | Integer (FK)  | Foreign key to `project.id` (required)           |

The `updated_at` column uses `onupdate=_get_utc_now` so it changes every time the record is updated.

The `project_id` foreign key establishes the many-to-one relationship: each task belongs to exactly one project.

```python
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='todo')
    priority = db.Column(db.String(20), default='medium')
    due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=_get_utc_now)
    updated_at = db.Column(db.DateTime, default=_get_utc_now, onupdate=_get_utc_now)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
```

**Relationships summary:**
- **Project 1 : N Task** – A project can have many tasks; each task belongs to exactly one project.
- **Cascade delete** – Deleting a project deletes all its tasks automatically.

## 5. Forms (`forms.py`)

Flask-WTF is used to handle form rendering and validation. Both forms inherit from `FlaskForm`.

### 5.1. ProjectForm

- `name`: Required string field.
- `description`: Optional text area.

```python
class ProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
```

### 5.2. TaskForm

- `title`: Required string.
- `description`: Optional text area.
- `status`: Select field with choices `('todo','To Do')`, `('doing','In Progress')`, `('done','Done')`. Default `todo`.
- `priority`: Select field with choices `('low','Low')`, `('medium','Medium')`, `('high','High')`. Default `medium`.
- `due_date`: Optional date field, formatted as `YYYY-MM-DD`.

```python
class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    status = SelectField('Status', choices=[('todo', 'To Do'), ('doing', 'In Progress'), ('done', 'Done')], default='todo')
    priority = SelectField('Priority', choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium')
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[Optional()])
```

## 6. Application Routes (`app.py`)

The main Flask application defines the following routes. Each route is explained with its purpose, HTTP methods, parameters, and interactions.

### 6.1. `@app.route('/')` – Index

- **Methods:** `GET`
- **Description:** Displays the home page with a list of all projects, ordered by creation date (newest first).
- **Logic:** `Project.query.order_by(Project.created_at.desc()).all()`
- **Template:** `index.html` – receives the list of projects.

### 6.2. `@app.route('/project/new', methods=['GET', 'POST'])` – New Project

- **Methods:** `GET`, `POST`
- **Description:** Creates a new project.
- **Form:** `ProjectForm`
- **Process:**
  - On `GET`: Renders an empty form.
  - On `POST` (validated): Creates a `Project` instance, adds it to the session, commits, flashes a success message, and redirects to the index.
- **Template:** `project_form.html` – with `title='New Project'`.

### 6.3. `@app.route('/project/<int:project_id>')` – View Project

- **Methods:** `GET`
- **Description:** Displays the Kanban board for a specific project.
- **Parameters:** `project_id` – the ID of the project.
- **Logic:**
  - Fetches the project or returns 404.
  - Retrieves all tasks belonging to that project (via `project.tasks`).
  - Splits tasks into three lists based on status: `todo_tasks`, `doing_tasks`, `done_tasks`.
- **Template:** `project.html` – receives `project`, `todo_tasks`, `doing_tasks`, `done_tasks`.

### 6.4. `@app.route('/project/<int:project_id>/task/new', methods=['GET', 'POST'])` – New Task

- **Methods:** `GET`, `POST`
- **Description:** Adds a new task to the specified project.
- **Parameters:** `project_id`
- **Form:** `TaskForm`
- **Process:**
  - On `GET`: Renders an empty form, passing the project for the cancel link.
  - On `POST` (validated): Creates a `Task` instance with the form data, sets `project_id`, adds to session, commits, flashes success, and redirects to the project view.
- **Template:** `task_form.html` – with `title='New Task'` and `project`.

### 6.5. `@app.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])` – Edit Task

- **Methods:** `GET`, `POST`
- **Description:** Edits an existing task.
- **Parameters:** `task_id`
- **Form:** `TaskForm` pre-populated with the task’s current values.
- **Process:**
  - On `GET`: Fetches the task, sets the form’s `due_date` to the task’s date (converted to `date()` if present).
  - On `POST` (validated): Updates the task’s attributes with form data, commits, flashes success, and redirects to the project view.
- **Template:** `task_form.html` – with `title='Edit Task'` and the parent project.

### 6.6. `@app.route('/task/<int:task_id>/delete', methods=['POST'])` – Delete Task

- **Methods:** `POST`
- **Description:** Deletes a task.
- **Parameters:** `task_id`
- **Process:**
  - Fetches the task.
  - Stores `project_id` before deletion (needed for redirect).
  - Deletes the task from the session and commits.
  - Flashes success and redirects to the project view.
- **Note:** Only `POST` is allowed, so deletion cannot be triggered by a simple link (prevents CSRF).

### 6.7. `@app.route('/task/<int:task_id>/move/<string:status>', methods=['POST'])` – Move Task

- **Methods:** `POST`
- **Description:** Changes the status of a task (used by the arrow buttons on task cards).
- **Parameters:** `task_id`, `status` (must be one of `todo`, `doing`, `done`).
- **Process:**
  - Fetches the task.
  - If the provided status is valid, updates `task.status` and commits.
  - Redirects back to the project view.
- **Security:** Only `POST` is allowed to prevent accidental GET requests from changing state.

### 6.8. `@app.route('/project/<int:project_id>/delete', methods=['POST'])` – Delete Project

- **Methods:** `POST`
- **Description:** Deletes a project and all its tasks (due to cascade).
- **Parameters:** `project_id`
- **Process:**
  - Fetches the project.
  - Deletes it (SQLAlchemy automatically deletes related tasks).
  - Commits, flashes success, and redirects to index.

## 7. Templates and UI

All templates extend `base.html` and use Tailwind CSS (via CDN) for styling. FontAwesome icons are used throughout.

### 7.1. `base.html`

- Provides the common layout: a navigation bar, a main content block, and a footer.
- Displays flashed messages with appropriate styling (green for success, red for error).
- Includes Tailwind and FontAwesome.

### 7.2. `index.html` (Projects list)

- Displays a grid of project cards.
- Each card shows the project name, description (or placeholder), creation date, task count, and buttons to view or delete.
- If no projects exist, a friendly message is shown with a call-to-action to create one.

### 7.3. `project.html` (Kanban board)

- Shows the project name and description, with a breadcrumb link back to projects.
- Three columns: **To Do**, **In Progress**, **Done**.
- Each column lists tasks using the `task_card.html` partial.
- The column headers show the count of tasks in that status.
- A green “Add Task” button at the top.

### 7.4. `task_card.html` (Partial for a single task)

This is the most interactive component. It displays:

- Task title and edit/delete icons.
- Optional description.
- Priority badge (colored: red for high, yellow for medium, green for low).
- Due date (if present) with a calendar icon.
- Creation date.
- **Movement buttons**:
  - Left arrow to move to “To Do” (hidden if already `todo`).
  - Right arrow to move to “In Progress” (hidden if already `doing`).
  - Check icon to move to “Done” (hidden if already `done`).
- Each movement button is a form that `POST`s to `move_task`.

The card is reused in all three columns, and the movement buttons are conditionally rendered based on the task’s current status.

### 7.5. `project_form.html` and `task_form.html`

Both are similar: they render a form inside a centered card. They use `form.hidden_tag()` for CSRF protection. Error messages are displayed below each field if validation fails. The cancel button returns to the appropriate page (index for project form, project view for task form).

## 8. Dummy Data Script (`add_dummy_data.py`)

This standalone script populates the database with random projects and tasks for testing or demonstration purposes.

### How it works:

- Uses the same `app` and `models` from the application.
- Contains pools of project names, task titles, statuses, and priorities.
- Defines a helper `random_date(start, end)` to generate random datetimes.
- Inside `create_dummy_data()`:
  - Optionally clears existing data (commented out by default).
  - Creates 3–6 random projects.
  - For each project, creates 5–12 tasks.
  - For each task:
    - Chooses a random title (sometimes appends a random number).
    - Generates a random creation date within the last 6 months.
    - Generates a random due date between 15 days before and 30 days after creation.
    - Assigns random status and priority.
    - Explicitly sets `created_at` to the generated date (overriding the default).
  - Commits after each project to ensure IDs are available.
- The script is meant to be run manually: `python add_dummy_data.py`.

## 9. How to Run the Application

1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/Scripts/activate   # on Windows Git Bash
   # or source venv/bin/activate (Mac/Linux)
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database**:
   ```bash
   python init_db.py
   ```

4. **(Optional) Add dummy data**:
   ```bash
   python add_dummy_data.py
   ```

5. **Run the Flask development server**:
   ```bash
   flask run
   # or python app.py
   ```

6. Open http://127.0.0.1:5000 in your browser.

## 10. Conclusion

TaskFlow is a well-structured Flask application that demonstrates fundamental web development concepts:

- **ORM relationships** – one-to-many with cascade delete.
- **Form handling** – using Flask-WTF with CSRF protection.
- **CRUD operations** – create, read, update, delete for projects and tasks.
- **Template inheritance and partials** – reusing the task card.
- **User feedback** – flash messages for success/deletion.
- **RESTful design** – using appropriate HTTP methods (POST for state changes).

Every relationship (Project–Task, the status categories, the movement logic) has been explained in detail. The application is ready for further enhancements, such as user authentication, drag‑and‑drop, or due date reminders.

