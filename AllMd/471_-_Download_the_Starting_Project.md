### Overview

This section details the initial setup required to begin building the RESTful blog application. The starting project provides a foundation that includes a pre-configured SQLite database (`posts.db`) containing three sample blog posts, along with the necessary HTML templates and a basic Flask application structure. Completing these steps ensures the development environment is correctly configured and that the application runs without errors before any modifications are made.

### Contents of the Starting Project

The starting project is distributed as a `.zip` archive. After extraction, the project directory contains the following files and folders:

- `main.py` – The main Flask application file with some boilerplate code and placeholders for routes.
- `posts.db` – An SQLite database file containing a `posts` table with three pre-populated blog post records.
- `templates/` – A directory containing HTML templates:
  - `index.html` – Home page template that lists all blog posts.
  - `post.html` – Template for displaying a single blog post.
  - `make-post.html` – Template that contains a form for creating/editing posts (currently empty).
  - `header.html`, `footer.html` – Partial templates for consistent layout.
- `static/` – A directory for static assets such as CSS, images, and JavaScript (may be empty or contain a basic CSS file).
- `requirements.txt` – A list of Python packages required for the project.

The `main.py` file at this stage includes:

- Imports for Flask, SQLAlchemy, Bootstrap, CKEditor, etc.
- Configuration for the Flask app (secret key, database URI, CKEditor settings).
- Initialization of extensions (db, bootstrap, ckeditor).
- Definition of the `BlogPost` database model matching the `posts` table.
- A placeholder home route (`/`) that currently does not fetch data from the database.
- Placeholder routes for other functionalities (to be implemented later).

### Step 1: Download and Extract the Project

1. Obtain the starting project `.zip` file from the course resources.
2. Extract the contents to a convenient location on your file system (e.g., `Documents/Projects/blog-day-67`).

### Step 2: Open the Project in PyCharm

1. Launch PyCharm (Community or Professional edition).
2. From the welcome screen, select **Open** and navigate to the extracted project folder.
3. Click **OK** to open the project.

PyCharm will detect the presence of a `requirements.txt` file and may automatically prompt you to create a virtual environment and install the dependencies. If prompted, agree to the action and click **OK**. This is the recommended approach and will streamline the setup.

### Step 3: Virtual Environment and Dependency Installation

#### Automatic Setup (Recommended)

If PyCharm displays a notification at the top of the editor window saying "No Python interpreter configured for the project" or "Install requirements from requirements.txt", follow these steps:

- Click the notification and select **Create Virtual Environment**.
- In the dialog, ensure the base interpreter points to a valid Python installation (Python 3.7+).
- Check the option **Install requirements from requirements.txt**.
- Click **OK**.

PyCharm will create a new virtual environment (a `venv` folder inside your project) and install all packages listed in `requirements.txt`. This process may take a minute or two.

#### Manual Setup (If Not Prompted)

If PyCharm does not prompt you automatically, you can set up the virtual environment manually:

1. Go to **File → Settings** (or **PyCharm → Preferences** on macOS).
2. Navigate to **Project: <project-name> → Python Interpreter**.
3. Click the gear icon ⚙️ and select **Add Interpreter → Add Local Interpreter**.
4. Leave the default settings (virtual environment, new environment) and click **OK**.
5. Once the interpreter is created, open the terminal in PyCharm (bottom left corner).
6. In the terminal, ensure the virtual environment is activated (the prompt should show `(venv)`). If not, activate it manually:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
7. Install the required packages by running:
   - On Windows: `python -m pip install -r requirements.txt`
   - On macOS/Linux: `pip3 install -r requirements.txt`

### Step 4: Verify Installation

After the dependencies are installed, check that there are no import errors in `main.py`. If any lines are underlined in red, it indicates that a package is missing or the interpreter is not correctly set.

To refresh PyCharm's indexing and resolve any lingering red underlines:

- Go to **File → Reload All from Disk**.

If red underlines persist, repeat the manual installation steps or verify that the virtual environment is selected as the project interpreter.

### Step 5: Explore the Project Structure

Take a moment to familiarize yourself with the project's components:

#### Database: `posts.db`

The SQLite database file contains a single table `posts` with the following schema (as defined in the `BlogPost` model):

- `id` (INTEGER, PRIMARY KEY)
- `title` (TEXT)
- `subtitle` (TEXT)
- `date` (TEXT)
- `body` (TEXT)
- `author` (TEXT)
- `img_url` (TEXT)

Three sample posts are already inserted. To view the database contents, you can use a tool like **DB Browser for SQLite** (downloadable from sqlitebrowser.org) or any SQLite viewer.

#### Templates

- **`index.html`**: This template currently loops over a list of posts (passed from the view) and displays their titles, subtitles, authors, and dates. It also contains a "Create New Post" button that links to the `/new-post` route (to be implemented). Additionally, there is a placeholder for delete icons (✘) next to each post.
- **`post.html`**: Displays the full content of a single post. At the bottom, there is an "Edit Post" button whose href needs to be dynamically set to `/edit-post/<post_id>`.
- **`make-post.html`**: Contains a form with placeholders for the fields defined in `CreatePostForm`. The form uses Bootstrap for styling and will later be enhanced with CKEditor for the body field.

### Step 6: Run the Initial Application (Optional)

To confirm that the environment is set up correctly, you can run the Flask development server:

1. In PyCharm, open `main.py`.
2. Click the green play button in the top-right corner, or right-click inside the file and select **Run 'main'**.
3. The terminal will show output indicating the server is running, typically at `http://127.0.0.1:5000/`.
4. Open a browser and navigate to that address. You should see a basic home page with no posts (because the database query is not yet implemented) and a "Create New Post" button. Clicking it will likely result in a 404 error because the route is not defined. This is expected at this stage.

### Troubleshooting Common Issues

| Issue | Possible Cause | Solution |
|-------|----------------|----------|
| Import errors in `main.py` (red underlines) | Virtual environment not activated or packages not installed. | Ensure the correct interpreter is selected in PyCharm and that `pip install -r requirements.txt` has been run successfully. |
| `ModuleNotFoundError: No module named 'flask'` when running | The Flask package is not installed in the current environment. | Reinstall dependencies: `pip install -r requirements.txt` while the virtual environment is active. |
| Database file not found | The path in `app.config['SQLALCHEMY_DATABASE_URI']` is incorrect relative to the working directory. | The default URI `sqlite:///posts.db` assumes `posts.db` is in the same directory as `main.py`. Verify that the file exists there. |
| Changes to HTML not reflected after refresh | Flask may cache templates. | Stop the server (Ctrl+C) and restart it. Alternatively, enable debug mode by setting `app.config['DEBUG'] = True` to auto-reload on changes. |
| Port 5000 already in use | Another process is using the default port. | Stop the other process, or run the app on a different port by modifying `app.run(port=5001)`. |

### Next Steps

With the project successfully set up, you are ready to proceed with implementing the required functionality as outlined in the subsequent lectures. The immediate tasks are:

1. Modify the home route to retrieve and display posts from the `posts.db` database.
2. Create a route for individual posts that fetches a post by its ID.
3. Implement the new post form and the POST route to save new entries.
4. Add editing and deletion capabilities.

Each of these steps will be covered in detail in the following documentation files.

### Conclusion

The starting project provides a solid foundation for building a RESTful blog with Flask. By following the setup instructions, you have established a consistent development environment with all necessary dependencies installed. You have also familiarized yourself with the project's structure and the sample data contained in the SQLite database. This preparation ensures that you can focus on the logic and functionality without environmental distractions.