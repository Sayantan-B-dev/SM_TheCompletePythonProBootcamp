# Virtual Bookshelf: Project Setup and Initial Configuration

## 1. Overview of the Starting Project

The starting project is a skeleton Flask application that implements a basic virtual bookshelf using an in‑memory list. It contains:

- A `main.py` file with the Flask routes for the home page (`/`) and the add‑book page (`/add`).
- HTML templates (`index.html` and `add.html`) located in a `templates` folder.
- A `requirements.txt` file listing all Python packages needed to run the project.

Currently, the application stores book data in a Python list named `all_books`. This list is re‑created every time the server starts, so any books added are lost on restart. Your task over the coming lessons will be to replace this ephemeral storage with a persistent SQLite database using SQLAlchemy.

Before you can begin coding, you must set up the project on your local machine. This involves downloading the project files, creating an isolated Python environment (a **virtual environment**), and installing the required dependencies.

## 2. Downloading the Project Files

The starting project is provided as a ZIP archive in the course resources. Follow these steps to obtain it:

1. Navigate to the lesson’s **Resources** section (usually below the video).
2. Click the link to download the ZIP file (e.g., `virtual_bookshelf_starting_files.zip`).
3. Save the ZIP file to a convenient location on your computer, such as your `Downloads` folder or a dedicated `PyCharmProjects` directory.

## 3. Unzipping and Opening in PyCharm

### 3.1 Extract the ZIP Archive
- **On Windows:** Right‑click the ZIP file and select **Extract All…**. Choose a destination folder and click **Extract**.
- **On macOS:** Double‑click the ZIP file to automatically extract its contents into a new folder with the same name.

After extraction, you should see a folder containing at least the following items:
- `main.py`
- `templates/` (with `index.html` and `add.html`)
- `requirements.txt`

### 3.2 Open the Project in PyCharm
1. Launch PyCharm.
2. On the welcome screen, click **Open** (or go to **File → Open** from an existing project window).
3. Navigate to the extracted folder, select it, and click **OK** (or **Open**).

PyCharm will load the project and display its contents in the **Project** tool window.

## 4. Setting Up a Virtual Environment

A **virtual environment** is an isolated Python environment that allows you to install project‑specific packages without affecting your system‑wide Python installation. It is considered a best practice for all Python projects because it prevents version conflicts and makes your project reproducible.

### 4.1 Automatic Virtual Environment Creation in PyCharm
When you open a project that contains a `requirements.txt` file, PyCharm often detects this and prompts you to create a virtual environment and install the dependencies automatically.

- If you see a yellow bar at the top of the editor with a message like **"Requirements.txt found. Create virtual environment?"**, click **Create Virtual Environment** (or **Install requirements**) and follow the prompts.
- PyCharm will create a new folder named `venv` (or `.venv`) inside your project directory and install all packages listed in `requirements.txt` into that isolated environment.

### 4.2 Manual Virtual Environment Creation
If PyCharm does not prompt you automatically, or if you prefer to set up the environment manually, follow these steps:

1. **Open the terminal** in PyCharm (bottom‑left corner, tab named **Terminal**).
2. Ensure your current working directory is the project root (where `main.py` and `requirements.txt` reside).
3. Run the appropriate command to create a virtual environment:
   - **Windows:**
     ```bash
     python -m venv venv
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv venv
     ```
   This creates a folder named `venv` containing a fresh Python interpreter and a `pip` executable.

4. **Activate the virtual environment**:
   - **Windows (Command Prompt):**
     ```bash
     venv\Scripts\activate
     ```
   - **Windows (PowerShell):**
     ```bash
     venv\Scripts\Activate.ps1
     ```
   - **macOS / Linux:**
     ```bash
     source venv/bin/activate
     ```
   After activation, your terminal prompt should show `(venv)` at the beginning, indicating that the virtual environment is active.

5. **Install the required packages** using the `requirements.txt` file:
   - **Windows:**
     ```bash
     python -m pip install -r requirements.txt
     ```
   - **macOS / Linux:**
     ```bash
     pip3 install -r requirements.txt
     ```
   This will install Flask, Jinja2, and any other dependencies exactly as specified.

6. **Verify installation**: Check that no red underlines appear in `main.py`. If you still see import errors (e.g., `flask` underlined in red), the packages may not have been installed correctly, or PyCharm may not be using the correct interpreter.

## 5. Configuring PyCharm to Use the Virtual Environment

Even after creating the virtual environment, PyCharm might still be using the global Python interpreter, leading to unresolved references. To fix this:

1. Go to **File → Settings** (or **PyCharm → Preferences** on macOS).
2. Navigate to **Project: <project name> → Python Interpreter**.
3. Click the gear icon ⚙️ and select **Add…**.
4. Choose **Existing environment** and browse to the `python.exe` (Windows) or `python` (macOS/Linux) inside your `venv` folder.
   - On Windows: `venv\Scripts\python.exe`
   - On macOS/Linux: `venv/bin/python`
5. Click **OK**. PyCharm will now use the virtual environment’s interpreter, and any red underlines should disappear.

If red underlines persist, try **File → Reload All from Disk** to refresh the project.

## 6. Understanding the Project Structure

Let’s take a moment to understand what each file does:

- **`main.py`** – The core Flask application. It defines two routes:
  - `@app.route('/')` – Renders the home page (`index.html`) and passes the `all_books` list to the template.
  - `@app.route('/add', methods=['GET', 'POST'])` – Handles both displaying the add‑book form (`add.html`) and processing the form submission. When a book is added, it appends a dictionary to `all_books` and redirects back to the home page.
- **`templates/index.html`** – Displays the list of books. It uses Jinja2 syntax to loop through the `books` variable and show each title, author, and rating. If the list is empty, it shows a “Library is empty” message.
- **`templates/add.html`** – Contains a simple HTML form with fields for title, author, and rating. The form submits a POST request to the same `/add` URL.
- **`requirements.txt`** – Lists all external packages required. For this project, it includes:
  - `Flask` – The web framework.
  - `Flask-SQLAlchemy` – The database extension we will add later.
  - `SQLAlchemy` – The underlying ORM.
  - `Werkzeug`, `Jinja2`, `click`, etc. – Flask dependencies.

## 7. Running the Initial Application

To see the current (non‑persistent) version in action:

1. Ensure your virtual environment is active and dependencies are installed.
2. Run `main.py` by right‑clicking the file in PyCharm and selecting **Run 'main'**, or by executing:
   ```bash
   python main.py
   ```
   (or `python3 main.py` on macOS/Linux).
3. Open a browser and go to `http://127.0.0.1:5000` (the URL shown in the terminal).
4. You should see the home page with a heading “My Library” and a link to “Add New Book”.
5. Click the link, fill out the form, and submit. The book appears on the home page.
6. **Stop the server** (click the red square in PyCharm) and **run it again**. Reload the home page – the book is gone.

This demonstrates exactly why we need a database. The next lessons will guide you through integrating SQLite and SQLAlchemy to make the data persistent.

## 8. Troubleshooting Common Issues

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| **Red underlines in `main.py`** (e.g., `from flask import Flask` is marked as an error). | PyCharm is not using the virtual environment where Flask is installed. | Configure the Python interpreter as described in Section 5. |
| **`ModuleNotFoundError: No module named 'flask'`** when running the script. | The virtual environment is not activated, or packages were not installed. | Activate the virtual environment and run `pip install -r requirements.txt`. |
| **`pip` is not recognized** (Windows). | Python is not in your system PATH, or you are using the wrong command. | Use `python -m pip` instead of `pip`. If that fails, reinstall Python and check “Add Python to PATH”. |
| **Permission denied** when creating virtual environment (macOS/Linux). | You may not have write permissions in the current directory. | Try a different directory (e.g., your home folder). |
| **Database file not appearing** after running later code. | The code that creates the database hasn’t been executed yet, or the path is incorrect. | We will cover database creation in the next lessons. |

## 9. Next Steps

Now that your development environment is correctly set up, you are ready to start building the persistent bookshelf. In the following lessons, you will:

- Learn about SQLite databases and how to interact with them using raw SQL.
- Install and configure Flask‑SQLAlchemy.
- Define a `Book` model that maps to a database table.
- Replace the in‑memory `all_books` list with database queries.
- Implement full CRUD functionality: editing ratings and deleting books.

Make sure you have the starting project open in PyCharm and that no errors are present before moving on. If you encounter any issues during setup, revisit the steps above or consult the course Q&A section.

---
