# Command Line Fundamentals and Backend Development Usage

Command line proficiency is foundational for backend development because servers, deployment environments, virtual environments, containers, and CI pipelines operate primarily through terminal interfaces. The sections below systematically cover essential commands, their behavior, and their backend relevance.

---

# 1. Core Navigation and File System Commands

These commands are universally required for backend work across Linux, macOS, and Git Bash environments.

## Directory Navigation

| Command          | Purpose                     | Backend Relevance                             |
| ---------------- | --------------------------- | --------------------------------------------- |
| `pwd`            | Print working directory     | Confirms project root before executing server |
| `ls`             | List directory contents     | Inspect project structure                     |
| `ls -la`         | List including hidden files | Verify `.env`, `.git`, config files           |
| `cd folder_name` | Change directory            | Navigate into project                         |
| `cd ..`          | Move one directory up       | Return to root folder                         |
| `cd ~`           | Go to home directory        | Access global configs                         |

Example:

```bash
pwd
```

Expected Output:

```
/home/user/backend_project
```

---

## File and Directory Creation

| Command                 | Purpose                   | Backend Usage                     |
| ----------------------- | ------------------------- | --------------------------------- |
| `mkdir project_name`    | Create directory          | Initialize new backend project    |
| `mkdir -p parent/child` | Create nested directories | Create structured project folders |
| `touch app.py`          | Create empty file         | Initialize Flask entry file       |
| `cp file1 file2`        | Copy file                 | Duplicate config or template      |
| `mv old new`            | Rename or move file       | Refactor project structure        |

Example:

```bash
mkdir flask_app
cd flask_app
touch app.py
```

Expected Result:
Directory and file created successfully.

---

## Deletion Commands

| Command         | Purpose                      | Warning               |
| --------------- | ---------------------------- | --------------------- |
| `rm file.py`    | Remove file                  | Permanent deletion    |
| `rm -r folder`  | Remove directory recursively | Deletes entire folder |
| `rm -rf folder` | Force recursive removal      | Extremely destructive |

Example:

```bash
rm -rf __pycache__
```

Backend relevance: Cleaning compiled Python cache files.

---

# 2. Viewing and Inspecting Files

| Command            | Purpose               | Backend Use             |
| ------------------ | --------------------- | ----------------------- |
| `cat file.py`      | Display file contents | Quick script inspection |
| `less file.py`     | Paginated view        | Read long logs          |
| `head file.log`    | First 10 lines        | Debug server logs       |
| `tail file.log`    | Last 10 lines         | Monitor server output   |
| `tail -f file.log` | Live log monitoring   | Observe production logs |

Example:

```bash
tail -f server.log
```

Expected Behavior:
Displays real-time server logs.

---

# 3. Python-Specific Command Line Operations

## Running Python Scripts

```bash
python app.py
```

Expected Output:
Flask development server running.

---

## Python Version Check

```bash
python --version
```

Backend relevance: Ensures compatibility with frameworks.

---

## Virtual Environment Management

Create environment:

```bash
python -m venv venv
```

Activate:

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

Deactivate:

```bash
deactivate
```

Backend relevance: Dependency isolation.

---

## Package Management (pip)

Install package:

```bash
pip install flask
```

Install from requirements file:

```bash
pip install -r requirements.txt
```

Generate requirements file:

```bash
pip freeze > requirements.txt
```

Expected Output:
All installed packages listed with versions.

Backend relevance: Reproducible deployments.

---

# 4. Environment Variables for Backend

Set environment variable:

Linux/Mac:

```bash
export FLASK_ENV=development
```

Windows:

```bash
set FLASK_ENV=development
```

Backend relevance:
Controls configuration modes, database URLs, API keys.

---

# 5. Flask-Specific CLI Commands

Set Flask app:

Linux/Mac:

```bash
export FLASK_APP=app.py
```

Run Flask:

```bash
flask run
```

Run on specific port:

```bash
flask run --port=8000
```

Run on public host:

```bash
flask run --host=0.0.0.0
```

Backend relevance:
Used in development environments.

---

# 6. Process and Port Management

Check running processes:

```bash
ps aux
```

Find process using port:

```bash
lsof -i :5000
```

Kill process:

```bash
kill -9 process_id
```

Backend relevance:
Terminate stuck server instances.

---

# 7. Git Commands for Backend Developers

| Command                    | Purpose               |
| -------------------------- | --------------------- |
| `git init`                 | Initialize repository |
| `git status`               | Check file state      |
| `git add .`                | Stage changes         |
| `git commit -m "message"`  | Save snapshot         |
| `git branch`               | List branches         |
| `git checkout branch_name` | Switch branch         |
| `git pull`                 | Fetch updates         |
| `git push`                 | Upload changes        |

Backend relevance:
Version control and collaboration.

---

# 8. Database Related Commands

SQLite CLI:

```bash
sqlite3 database.db
```

PostgreSQL CLI:

```bash
psql -U username -d database_name
```

Backend relevance:
Direct database inspection and debugging.

---

# 9. Deployment Related Commands

Install Gunicorn:

```bash
pip install gunicorn
```

Run production server:

```bash
gunicorn app:application
```

Docker build:

```bash
docker build -t backend_app .
```

Docker run:

```bash
docker run -p 8000:8000 backend_app
```

Backend relevance:
Production deployment and containerization.

---

# 10. Useful Debugging Commands

Check open ports:

```bash
netstat -tuln
```

Check disk usage:

```bash
df -h
```

Check directory size:

```bash
du -sh folder_name
```

Backend relevance:
Server health monitoring.

---

# Backend Developer Command Line Mastery

A backend developer must comfortably:

* Navigate file systems rapidly
* Manage virtual environments
* Install and lock dependencies
* Run development servers
* Inspect logs in real time
* Manage ports and processes
* Interact with databases
* Use Git fluently
* Deploy using WSGI servers
* Work with containers

Command line literacy directly correlates with backend efficiency and debugging capability.
