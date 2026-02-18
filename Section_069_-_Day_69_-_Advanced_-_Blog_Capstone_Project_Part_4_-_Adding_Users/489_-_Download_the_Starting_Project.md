## 489 - Download the Starting Project

This document provides a comprehensive guide to obtaining, setting up, and exploring the initial codebase for the Blog Capstone Project with user authentication. The starting project contains a partially built blog application with an SQLite database, pre-existing sample blog posts, and placeholder pages for login and registration. The goal of this setup phase is to establish a working development environment, verify that the existing functionality operates correctly, and become familiar with the project's structure before implementing the new user authentication features.

### Prerequisites

Before beginning, ensure your development machine meets the following requirements:

- **Python 3.8 or higher** installed and accessible from the command line.
- **PyCharm Community or Professional Edition** installed. The instructions are tailored for PyCharm, but you may use another IDE or text editor with appropriate Python support.
- **Git** (optional) if you plan to version control your changes.
- **DB Browser for SQLite** or a similar tool to inspect the `blog.db` file. This helps in understanding the existing data schema and verifying database modifications later.

### Step 1: Download the Starting Project Archive

Obtain the project ZIP file from the lesson resources. This archive contains all the necessary files to begin.

- **Source**: The download link is provided in the lecture materials (usually under "Resources" or "Attachments").
- **Action**: Click the link to download the ZIP file to your local machine, typically into your `Downloads` folder.

### Step 2: Extract the Archive and Open in PyCharm

1. **Extract the ZIP**: Navigate to the downloaded file, right‑click, and select "Extract All" (Windows) or double‑click (macOS) to unzip. Choose a location for your project, such as `C:\Users\<YourName>\PycharmProjects\` or `~/PycharmProjects/`. Ensure the folder name does not contain spaces to avoid path issues.

2. **Open in PyCharm**:
   - Launch PyCharm.
   - On the Welcome screen, click **Open** and navigate to the extracted folder.
   - Select the folder (the one containing `main.py`, `requirements.txt`, etc.) and click **OK**.

3. **Virtual Environment Prompt**: PyCharm automatically detects the presence of a `requirements.txt` file. A notification may appear in the bottom‑right corner asking if you want to create a virtual environment and install the dependencies. If you see this prompt:
   - Click **Create Virtual Environment** or **OK**.
   - Accept the default settings (the environment will be created in a `venv` folder inside your project).
   - PyCharm will then run `pip install -r requirements.txt` in the background. This may take a few moments.

4. **If No Prompt Appears**:
   - You can manually trigger the virtual environment creation using the steps in **Step 3** below.

### Step 3: Manual Virtual Environment Setup (Troubleshooting)

If PyCharm does not prompt you, or you prefer to create the environment manually, follow these steps:

1. Open **File** > **Settings** (Windows/Linux) or **PyCharm** > **Preferences** (macOS).
2. Navigate to **Project: <project_name>** > **Python Interpreter**.
3. Click the gear icon ⚙️ and select **Add Interpreter** > **Add Local Interpreter**.
4. In the dialog, leave the default settings (Virtualenv Environment, New environment) and ensure the base interpreter points to your system Python.
5. **Important**: Do **not** check the box that says "Inherit global site-packages". This ensures the virtual environment remains isolated.
6. Click **OK**. PyCharm will create a new `venv` folder and configure the interpreter for the project.

After the virtual environment is created, you need to install the required packages. Open the **Terminal** in PyCharm (bottom‑left toolbar, or use `Alt+F12`).

- **On Windows**:
  ```bash
  python -m pip install -r requirements.txt
  ```
- **On macOS/Linux**:
  ```bash
  pip3 install -r requirements.txt
  ```

The `requirements.txt` file lists all external libraries the project depends on. A typical content for this project might include:
```
Flask==2.3.3
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.2
Flask-WTF==1.1.1
Werkzeug==2.3.7
WTForms==3.0.1
```
These packages provide the web framework, database ORM, authentication, form handling, and security utilities.

Once the installation completes, any red underlines in `main.py` should disappear. If they persist, proceed to the troubleshooting steps below.

### Step 4: Verify No Red Underlines in main.py

After installing dependencies, open `main.py` (the main application file). If you still see red underlines beneath import statements:

1. **Ensure the correct interpreter is selected**: Look at the bottom‑right corner of PyCharm. It should show the name of your virtual environment (e.g., `Python 3.x (venv)`). If it shows a different interpreter, click it and choose the one from your `venv` folder.
2. **Reload the project from disk**: Go to **File** > **Reload All from Disk**. This forces PyCharm to re‑index the project and re‑evaluate the interpreter paths.
3. **Restart PyCharm**: Sometimes a full restart is necessary to clear cached errors.

### Step 5: Explore the Project Structure and Database

Take time to understand what the starting project contains. The key files and folders are:

- **main.py**: The main Flask application. It contains route definitions, database setup, and existing logic for displaying blog posts and handling comments (if implemented). Placeholder routes for login and registration are present but not yet functional.
- **database.py** (if present): May contain database initialization and model definitions. If not, models are likely defined inside `main.py`.
- **forms.py**: Likely contains Flask-WTF form classes for login and registration (empty or commented out initially).
- **templates/**: Contains HTML files rendered by the application. Look for `base.html`, `index.html` (home page), `post.html` (individual post page), `login.html`, `register.html`, etc. The login and register templates are incomplete placeholders.
- **static/**: Holds CSS, JavaScript, and image files. The styling is already applied, so pages should look reasonably styled.
- **blog.db**: SQLite database file containing sample blog posts. Use DB Browser for SQLite to open this file and inspect the tables and their fields.

**Database Inspection with DB Browser for SQLite**:

1. Download and install DB Browser for SQLite from [sqlitebrowser.org](https://sqlitebrowser.org/).
2. Open the application, click **Open Database**, and navigate to the `blog.db` file inside your project folder.
3. Examine the tables. You will likely see:
   - **posts**: Contains columns such as `id`, `title`, `subtitle`, `body`, `author`, `date`. This table stores the blog posts.
   - **comments** (if implemented): May contain `id`, `text`, `post_id`, `author_name`, `author_email`, etc. Note that currently comments are not linked to registered users.
   - **users**: This table may not exist yet; it will be added during the authentication implementation.
4. Understanding the existing schema is crucial because you will later modify it to integrate user accounts (e.g., adding a `users` table, altering `comments` to link to users).

### Step 6: Run the Application

1. In PyCharm, locate the `main.py` file in the Project tool window.
2. Right‑click on `main.py` and select **Run 'main'**. Alternatively, click the green triangle ▶️ in the top‑right corner if the file is already open.
3. The console will show output similar to:
   ```
   * Serving Flask app 'main'
   * Debug mode: on
   * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
   ```
4. Open your web browser and go to `http://127.0.0.1:5000`. You should see the blog homepage displaying the sample posts.
5. Navigate through the pages using the provided links. Click on a post to view its details. Test any existing comment form (if present) – it may work but comments will be stored without user association.
6. Attempt to access the login and register pages via the navigation bar. They will load basic forms but likely will not function correctly because the backend logic is not yet implemented. This is expected.

### Step 7: Code Familiarization

Before adding new features, review the existing code thoroughly. Pay attention to:

- How the Flask app is configured (secret key, database URI).
- How database models are defined (look for classes inheriting from `db.Model`).
- The routes: `/`, `/post/<int:post_id>`, `/login`, `/register`, `/logout` (if present).
- How templates are rendered and which variables are passed.
- Any existing authentication‑related code (e.g., use of `flask_login` might be partially imported but not fully integrated).

Understanding the current codebase ensures that when you begin adding user authentication, you can seamlessly integrate it without breaking existing functionality.

### Troubleshooting Common Issues

- **Red underlines persist after installation**: Double‑check that the virtual environment is activated. In the PyCharm terminal, the prompt should show `(venv)` at the beginning. If not, manually activate it:
  - Windows: `venv\Scripts\activate`
  - macOS/Linux: `source venv/bin/activate`
  Then reinstall requirements.

- **ModuleNotFoundError when running the app**: This indicates that the required package is not installed in the current environment. Activate the virtual environment and run `pip install -r requirements.txt` again.

- **Database errors (e.g., "no such table")**: The SQLite database might be missing or corrupted. Ensure `blog.db` is present in the project root. If the application creates tables automatically, you might need to delete the existing `blog.db` and let the app recreate it (but this would lose sample posts). Check the code to see if the database is initialised with sample data.

- **Port already in use**: If another application is using port 5000, you can change the port by modifying the `app.run()` call in `main.py` to `app.run(port=5001)`.

### Next Steps

After successfully setting up and exploring the project, you are ready to proceed with implementing user authentication. The subsequent lessons will guide you through:

- Creating a `User` model and updating the `Comment` model to link to users.
- Building registration and login forms.
- Integrating Flask-Login for session management.
- Protecting routes (e.g., requiring login to comment).
- Updating templates to show user‑specific information and conditional UI elements.

Ensure you have a solid grasp of the starting project before moving forward. This foundation is critical for a smooth implementation of the remaining features.

**Resources**:
- DB Browser for SQLite: [https://sqlitebrowser.org/](https://sqlitebrowser.org/)
- Flask documentation: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
- Flask-Login documentation: [https://flask-login.readthedocs.io/](https://flask-login.readthedocs.io/)
- Flask-SQLAlchemy documentation: [https://flask-sqlalchemy.palletsprojects.com/](https://flask-sqlalchemy.palletsprojects.com/)
- Flask-WTF documentation: [https://flask-wtf.readthedocs.io/](https://flask-wtf.readthedocs.io/)

By the end of this setup, your development environment is correctly configured, the application runs without errors, and you have a clear mental map of the existing codebase. You are now prepared to add the user authentication layer.