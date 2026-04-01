## Using Git to Add Version Control to Your Project (PyCharm Integration)

This document provides a comprehensive, step‑by‑step guide to putting your project under version control using Git, with a focus on performing these actions within the PyCharm integrated development environment (IDE). It covers everything from initializing a local Git repository to making your first commit, along with explanations of the underlying concepts and alternative command‑line approaches. By the end, you will have a fully version‑controlled project, ready to be pushed to a remote repository like GitHub.

### Overview

Version control is an essential practice in software development. It allows you to track changes to your code over time, revert to previous states, collaborate with others, and maintain a history of your project. Git is the most widely used version control system. PyCharm provides a rich graphical interface for Git operations, making it accessible without memorizing command‑line syntax.

In this guide, you will:

- Ensure your project is ready for version control (including a `.gitignore` file).
- Enable Git version control integration in PyCharm.
- Add all relevant files to the staging area.
- Commit them with a meaningful message.
- Verify the commit using PyCharm’s Git log.

### Prerequisites

Before starting, make sure you have the following:

- **PyCharm** installed (Community or Professional edition).
- **Git** installed on your system and accessible from the command line. PyCharm relies on the system Git installation.
- A project to put under version control. This can be your own blog project from the previous days, or you can download a completed copy from the lesson resources.
- A `.gitignore` file placed in the project root (as covered in the previous lesson). This file ensures that temporary files, virtual environments, and local configuration are not accidentally tracked.

If you are using the downloaded completed project, you will need to install its required packages and have an admin user pre‑registered. The provided credentials are:

- **Admin email:** `admin@email.com`
- **Admin password:** `asdf`

### Step 1: Verify Your Project Runs Correctly

Before placing the project under version control, it is good practice to run it locally and confirm that everything works as expected. This ensures you are committing a functional state.

1. Open the project in PyCharm.
2. If you are using a fresh download, install the required packages. You can do this via the terminal inside PyCharm:
   ```bash
   pip install -r requirements.txt
   ```
   Alternatively, PyCharm may detect the `requirements.txt` file and offer to install the packages.
3. Run the application (e.g., by executing the main Flask file). The exact run configuration depends on your project structure. Typically, you can right‑click the main Python file and select **Run**.
4. Verify that the application starts without errors and that you can access it in your browser. If you are using the provided admin account, test logging in to ensure the authentication works.

### Step 2: Enable Version Control Integration in PyCharm

Enabling version control integration is equivalent to running `git init` in the terminal. It creates a new Git repository in your project’s root directory.

1. In PyCharm, go to the main menu and select **VCS** → **Enable Version Control Integration**.
   - If you do not see this option, you may already have version control enabled. Check the bottom‑right corner of the IDE; if you see a Git branch indicator (e.g., `master` or `main`), integration is already active.
2. A dialog box will appear asking you to choose the version control system. Select **Git** from the dropdown and click **OK**.

After this step, PyCharm initializes a Git repository in your project folder. You will notice several changes in the IDE:

- A new **Git** tool window becomes available (usually at the bottom or as a tab). It contains two sub‑tabs: **Console** (shows Git command output) and **Log** (displays the commit history).
- File colors in the Project view change. Files that are not yet under version control appear **red**. Files that are tracked and have been modified will appear **green** or **blue**, depending on their status. This color coding helps you quickly see which files are staged, modified, or ignored.

### Step 3: Understand What Will Be Committed (and What Won’t)

Before committing, it is crucial to review which files Git will include. The `.gitignore` file you added earlier tells Git to exclude certain files and directories. For a typical Python project, ignored items include:

- The virtual environment folder (`venv/`)
- Bytecode cache (`__pycache__/`, `*.pyc`)
- Database files (`*.db`, `posts.db`)
- IDE configuration (`.idea/`)
- Environment variable files (`.env`)
- OS metadata (`.DS_Store`)

All other files (your source code, templates, static assets, configuration files like `requirements.txt`, and `.gitignore` itself) are candidates for version control. In the Project view, you will see these files in **red**, indicating they are untracked.

### Step 4: Add Files to the Staging Area and Commit

The commit operation in Git consists of two steps: staging (selecting which changes to include) and committing (recording a snapshot). PyCharm combines these into a convenient commit tool window.

1. Open the commit tool window by:
   - Clicking the **Commit** button on the left toolbar (a checkmark icon), or
   - Using the keyboard shortcut `Ctrl + K` (Windows/Linux) or `Cmd + K` (macOS), or
   - Going to **VCS** → **Commit**.

   The commit tool window opens, typically on the side of the IDE. It displays a list of all files that have changes, grouped by status (e.g., **Unversioned Files**, **Modified**).

2. In the commit tool, you will see a section titled **Unversioned Files**. By default, all unversioned files are checked (selected) for inclusion in the commit. Review the list carefully. Ensure that:
   - Files you want to track are checked.
   - Files listed in your `.gitignore` are **not** shown here (they should be completely absent from the list). If you see files that should be ignored (like `.idea/` or `venv/`), your `.gitignore` may not be correctly placed or formatted. In that case, stop and fix the `.gitignore` file before proceeding.
   - Any sensitive files (like `.env`) are not accidentally checked.

   You can uncheck any file you do not wish to include. However, for a first commit, it is typical to include all source files and configuration.

3. At the bottom of the commit tool window, there is a text field for the **commit message**. Write a clear, concise message describing the initial state of your project. For example:
   ```
   Initial commit: Add blog project with Flask and SQLAlchemy
   ```

   Good commit messages follow the imperative mood (e.g., "Add", "Fix", "Update") and explain the purpose of the change.

4. Before committing, you may also see a **Commit** button with options. If you want to review the changes in each file, you can double‑click a file to see a diff view. This is useful to ensure no unintended changes are included.

5. Click the **Commit** button (or **Commit and Push…** if you want to immediately push to a remote repository – but for now, just commit locally). PyCharm will execute the Git commit command. You may see a dialog asking if you want to enable some pre‑commit checks (like code analysis). For now, you can proceed without them.

After a successful commit, the file colors in the Project view will change. Tracked files that are unchanged appear in **white** (or normal text color). The commit tool window will close, and a confirmation message may appear.

### Step 5: Verify the Commit in the Git Log

To confirm that your commit was recorded, examine the Git log.

1. Open the **Git** tool window (usually at the bottom of the IDE). If it is not visible, go to **View** → **Tool Windows** → **Git**.
2. Switch to the **Log** tab. You will see a graphical representation of your commit history. There should be at least one entry – your initial commit.
3. Click on the commit to see details: the commit hash, author, date, and the list of files included.

The log is a powerful tool for navigating your project’s history. You can compare versions, revert changes, and create branches from here.

### Alternative: Using the Terminal

While PyCharm’s GUI is convenient, it is also helpful to understand the underlying Git commands. The steps above correspond to the following terminal commands:

```bash
# Navigate to your project directory
cd /path/to/your/project

# Initialize a Git repository
git init

# Check the status of files (shows untracked files)
git status

# Add all files (respecting .gitignore) to the staging area
git add .

# Commit with a message
git commit -m "Initial commit: Add blog project with Flask and SQLAlchemy"
```

You can run these commands in PyCharm’s built‑in terminal (**View** → **Tool Windows** → **Terminal**). The GUI and terminal approaches are complementary; knowing both gives you flexibility.

### What to Do Next

With your project now under local version control, you are ready to connect it to a remote repository (e.g., on GitHub) and push your code. This will enable collaboration, backup, and deployment. Typical next steps include:

- Creating a repository on GitHub (without initializing it with a README, to avoid merge conflicts).
- Adding the remote URL to your local repository:
  ```bash
  git remote add origin https://github.com/yourusername/your-repo.git
  ```
- Pushing your local commits to the remote:
  ```bash
  git push -u origin main
  ```
  (If your default branch is named `master`, adjust accordingly.)

These steps will be covered in subsequent lessons. For now, you have successfully established a version‑controlled foundation for your project.

### Troubleshooting Common Issues

- **Git not found**: If PyCharm reports that Git is not installed, you need to install Git from [git-scm.com](https://git-scm.com/) and ensure it is in your system PATH. After installation, restart PyCharm and go to **Settings** → **Version Control** → **Git** to set the path to the Git executable.
- **Files not being ignored**: Double‑check your `.gitignore` file. It must be in the root directory of your project. Use `git status` to see which files are still untracked. If a file is being tracked but should be ignored, you need to stop tracking it first (`git rm --cached <file>`) and then add it to `.gitignore`.
- **Commit fails with "nothing to commit"**: This usually means no files were staged. In the commit tool, ensure that files are checked. Alternatively, you may have already committed all changes; run `git status` to see if there are any uncommitted changes.

### Conclusion

By following this guide, you have transformed your project into a Git‑tracked repository. You can now enjoy the benefits of version control: the ability to revert mistakes, experiment with branches, and collaborate with confidence. The next logical step is to connect your local repository to a remote hosting service like GitHub, which will be the focus of the following lesson.