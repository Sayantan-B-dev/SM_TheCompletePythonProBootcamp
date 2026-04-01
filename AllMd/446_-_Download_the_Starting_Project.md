# Day 64: Download the Starting Project – Setup Instructions

## 1. Overview

Before you begin coding the Top 10 Movies website, you need to obtain the starter project files and set up your development environment correctly. This file guides you through downloading the project, opening it in PyCharm, creating a virtual environment, and installing all necessary dependencies. Proper setup ensures that your code runs consistently and avoids conflicts with other Python projects on your system.

The starting project includes:

- A basic Flask application structure.
- Pre‑written HTML templates (using Jinja2) that you will later connect to your Flask routes.
- A `requirements.txt` file listing all Python packages needed for the project.

---

## 2. Step 1: Download the Starting Project

### 2.1. Locate the Resources
In the course platform, navigate to the lesson titled **“446_-_Download_the_Starting_Project”**. Under the “Resources” section, you will find a ZIP file containing the starter code.

### 2.2. Download and Extract
- Click the link to download the ZIP file (e.g., `starting_project.zip`).
- Save the file to a convenient location on your computer, such as your `Documents` or `Projects` folder.
- Right‑click the ZIP file and select **Extract All** (Windows) or double‑click to unzip (macOS). Extract the contents to a new folder. You can rename the folder to something like `top10movies` if you wish.

After extraction, you should see a folder containing at least the following files and directories:

```
top10movies/
├── main.py
├── requirements.txt
└── templates/
    ├── index.html
    ├── edit.html
    ├── add.html
    └── select.html
```

*Note: The exact filenames may vary slightly, but the structure is similar.*

---

## 3. Step 2: Open the Project in PyCharm

### 3.1. Launch PyCharm
Open PyCharm (Community or Professional edition). If you have a project already open, close it via **File → Close Project**.

### 3.2. Open the Extracted Folder
- On the Welcome screen, click **Open**.
- Navigate to the folder you extracted (e.g., `top10movies`), select it, and click **OK**.

PyCharm will now load the project. You will see the project files listed in the left sidebar (Project tool window).

---

## 4. Step 3: Set Up a Virtual Environment (Automatic)

When you open a project containing a `requirements.txt` file, PyCharm often detects it and prompts you to create a virtual environment and install the dependencies.

### 4.1. Respond to the Prompt
- A yellow bar may appear at the top of the editor with a message like: *“Requirements.txt found. Create virtual environment?”*.
- Click **Create Virtual Environment** or **OK** (depending on the PyCharm version).
- PyCharm will create a new virtual environment in a folder named `venv` inside your project directory and install all packages listed in `requirements.txt` into that environment.

If you see this prompt and agree, the setup is complete – you can skip to **Step 5**.

### 4.2. If No Prompt Appears
If PyCharm does not automatically offer to set up the virtual environment, you can trigger it manually:

- Right‑click the `requirements.txt` file in the Project tool window.
- Choose **Install all packages** or **Create Virtual Environment** (the exact wording may vary).
- Follow the on‑screen instructions to create a new virtual environment.

---

## 5. Step 4: Manual Virtual Environment Setup (Troubleshooting)

If you prefer to set up the virtual environment manually, or if the automatic methods fail, follow these steps.

### 5.1. Open Project Settings
- Go to **File → Settings** (Windows/Linux) or **PyCharm → Preferences** (macOS).
- In the left panel, select **Project: top10movies → Python Interpreter**.

### 5.2. Add a Local Interpreter
- Click the gear icon ⚙️ and choose **Add…**.
- In the dialog, select **New environment**.
- Leave the default location (it should be inside your project folder, e.g., `.\venv`).
- **Important:** Do **not** check the box “Inherit global site‑packages”. Keeping the environment isolated is crucial.
- Click **OK**.

PyCharm will create a new `venv` folder and set it as the project interpreter. This folder will contain a fresh Python installation (or link to your system Python) and a `site-packages` directory for project‑specific packages.

### 5.3. Install Packages from requirements.txt
Now you need to install the required packages into this new environment.

- Open the **Terminal** tab at the bottom of PyCharm. (If you don’t see it, go to **View → Tool Windows → Terminal**.)
- The terminal should already be activated in the project’s root directory and using the new virtual environment (you should see `(venv)` at the beginning of the prompt).

Run the appropriate command to install the dependencies:

**Windows:**
```bash
python -m pip install -r requirements.txt
```

**macOS/Linux:**
```bash
pip3 install -r requirements.txt
```

Wait for the installation to complete. You will see output listing each package being downloaded and installed.

---

## 6. Step 5: Verify the Setup

### 6.1. Check for Red Underlines
Open `main.py` in the editor. If you still see red underlines under any import statements (e.g., `from flask import Flask`), it means the virtual environment is not correctly recognised or the packages are missing.

### 6.2. Reload the Project from Disk
- Go to **File → Reload All from Disk**. This forces PyCharm to re‑evaluate the project structure and interpreter settings.
- After reload, the red underlines should disappear.

If they persist, double‑check that the virtual environment is selected as the Python interpreter (see **Step 4**) and that the installation command completed without errors.

### 6.3. Inspect the Installed Packages
- Go to **File → Settings → Project → Python Interpreter**.
- You should see a list of packages including `Flask`, `Flask-SQLAlchemy`, `Werkzeug`, etc. This confirms that the installation succeeded.

---

## 7. Understanding the Project Structure

Now that your environment is ready, take a moment to familiarise yourself with the provided files.

### 7.1. `main.py`
This is the entry point of the Flask application. Currently, it contains a minimal skeleton with a few routes and comments indicating where you will add your code. It imports necessary modules and sets up the Flask app.

### 7.2. `requirements.txt`
Lists all external Python packages required for the project. Using this file ensures that anyone working on the project can replicate the exact environment by running `pip install -r requirements.txt`.

### 7.3. `templates/` Directory
Contains HTML files that use the Jinja2 templating language. These files define the layout of the web pages:
- `index.html` – The home page displaying all movies.
- `edit.html` – The page for editing a movie’s rating and review.
- `add.html` – The page with a form to add a new movie by title.
- `select.html` – The page that shows search results from the TMDB API.

These templates are already styled with Bootstrap classes, so they will look presentable once you connect them to your Flask routes.

---

## 8. What’s Next?

With the project successfully opened and dependencies installed, you are ready to start implementing the first requirement: **Be able to view movie list items**. In the next lesson, you will:

- Create a SQLite database using Flask‑SQLAlchemy.
- Define a `Movie` model.
- Add sample movie entries.
- Modify the home route to query and display these movies using the provided `index.html` template.

Proceed to **447_-_Requirement_1_-_Be_Able_to_View_Movie_List_Items.md** to begin coding.

---

## 9. Additional Troubleshooting Tips

- **Virtual environment not activated in terminal:** If you don’t see `(venv)` in the terminal prompt, manually activate it:
  - Windows: `.\venv\Scripts\activate`
  - macOS/Linux: `source venv/bin/activate`
- **Permission errors during package installation:** On macOS/Linux, you might need to use `pip3` and ensure you are not using system Python. The virtual environment should handle this.
- **PyCharm still shows unresolved references:** Try invalidating caches: **File → Invalidate Caches / Restart…**.
- **Conflicting packages:** If you accidentally installed packages globally, the virtual environment isolates your project, so it’s safe to delete the `venv` folder and start over.

---