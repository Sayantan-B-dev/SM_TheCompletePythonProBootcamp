## Setting Up a WSGI Server with Gunicorn

This document provides a comprehensive guide to configuring your Flask application to use a production‑ready WSGI server – specifically, **Gunicorn**. You will learn why a WSGI server is necessary, how to add Gunicorn to your project dependencies, and how to create a `Procfile` that tells your hosting platform how to run your application. By the end, you will have a project that is correctly set up to be served by Gunicorn in a production environment, and you will have committed these changes to your Git repository.

### Introduction

When you develop a Flask application locally, you typically start it with `app.run()` or the `flask run` command. This uses Flask’s built‑in development server, which is convenient for development because it automatically reloads on code changes and provides detailed error pages. However, this server is **not designed to handle production traffic**. It is single‑threaded, can become a security risk if exposed to the internet, and does not scale well. To run your application reliably and securely in a production environment, you need a dedicated **WSGI server**.

### What is WSGI?

WSGI stands for **Web Server Gateway Interface**. It is a specification (described in [PEP 3333](https://www.python.org/dev/peps/pep-3333/)) that defines a simple and universal interface between web servers and Python web applications or frameworks.

In simple terms:

- A traditional web server (like Nginx or Apache) is excellent at serving static files and handling HTTP requests, but it cannot directly execute Python code.
- A WSGI server acts as a bridge: it communicates with the web server (or directly with the client) on one side, and calls your Python application on the other side, passing the request data and receiving the response.

By standardising this interface, any WSGI server can work with any WSGI‑compliant framework (Flask, Django, etc.), and your application becomes deployable on a wide range of hosting platforms without modification.

### Why Gunicorn?

**Gunicorn** (Green Unicorn) is one of the most popular WSGI servers for Python applications. It is simple to configure, performs well, and is widely supported by hosting providers like Heroku, Render, and PythonAnywhere. Gunicorn uses a pre‑fork worker model, meaning it starts multiple operating system processes to handle requests concurrently, which improves throughput and reliability.

By using Gunicorn, you ensure that your application can handle multiple simultaneous requests, recover from crashes, and run efficiently in a production environment.

---

### Step 1: Add Gunicorn to `requirements.txt`

The first step is to include Gunicorn in your project’s list of dependencies. This ensures that when you deploy your application, the hosting platform installs Gunicorn along with your other packages.

1. Open your `requirements.txt` file.
2. If Gunicorn is not already listed, add the following line:
   ```
   gunicorn==21.2.0
   ```
   The exact version number (`21.2.0`) is the version that has been tested with the deployment process in this course. Using a specific version avoids unexpected changes caused by newer releases.

   If you are using the starting code provided for this section, Gunicorn should already be present. Nevertheless, verify that the line exists.

3. Save the file.

**Why pin the version?**  
Specifying an exact version guarantees that the same version of Gunicorn will be installed in every environment (development, staging, production). This prevents situations where a newer version introduces a breaking change and causes your deployment to fail.

**Example of a complete `requirements.txt` after adding Gunicorn:**

```
Bootstrap_Flask==2.3.3
Flask_CKEditor==0.5.1
Flask_Login==0.6.3
Flask-Gravatar==0.5.0
Flask_WTF==1.2.1
WTForms==3.0.1
Werkzeug==3.0.0
Flask==2.3.2
flask_sqlalchemy==3.1.1
SQLAlchemy==2.0.25
gunicorn==21.2.0
psycopg2-binary==2.9.9
```

---

### Step 2: Create a `Procfile`

The `Procfile` is a configuration file used by many cloud platforms (Heroku, Render, etc.) to declare how your application should be started. It specifies the **process types** and the commands to run them. For a web application, you define a `web` process that runs your WSGI server.

#### What is a Procfile?

A `Procfile` is a simple text file named exactly `Procfile` (with a capital P and no file extension) placed in the root directory of your project. Each line follows the format:

```
<process type>: <command>
```

For a typical Flask application, you will have a single line:

```
web: gunicorn main:app
```

Let’s break down this command:

- `web:` – This tells the platform that this process will handle HTTP traffic. It is the standard name for a web server process.
- `gunicorn` – The command to start the Gunicorn server.
- `main:app` – This argument tells Gunicorn where to find your WSGI application. It consists of two parts:
  - `main` – The name of the Python module (without the `.py` extension) that contains your Flask application object. In this example, the module is `main.py`.
  - `app` – The name of the Flask application instance inside that module. By convention, many Flask apps are instantiated as `app = Flask(__name__)`. If your application object has a different name (e.g., `application`), you would adjust this part accordingly (e.g., `main:application`).

If your main application file is named something else, replace `main` with the correct module name. For instance, if your file is `blog.py` and it contains `app = Flask(__name__)`, the line would be:

```
web: gunicorn blog:app
```

#### Creating the Procfile

1. In PyCharm (or your text editor/IDE), create a new file in the **top‑level folder** of your project (the same directory that contains `requirements.txt` and your main application file).
2. Name the file exactly **`Procfile`** – note the capital P and no extension. PyCharm will likely show a dialog asking if you want to add this file to Git. Click **Add** (or confirm) to track it under version control.
3. Open the file and type the following line (adjusting the module name if necessary):
   ```
   web: gunicorn main:app
   ```
4. Save the file.

#### Why the Procfile is Essential

When you deploy your application to a platform like Render or Heroku, the platform reads the `Procfile` to determine how to run your app. Without it, the platform would not know which command to execute. The `Procfile` standardises the deployment process and ensures that your application starts correctly every time.

**Important:** Make sure the file name is spelled exactly as `Procfile`. Common mistakes include `procfile` (lowercase), `Procfile.txt`, or `Procfile.py`. These will not be recognised, and your deployment will fail.

---

### Step 3: Commit Your Changes

Now that you have modified `requirements.txt` and created the `Procfile`, it is time to save these changes in your Git repository. Committing at this point creates a snapshot of a deployment‑ready configuration.

1. Open the **Commit tool** in PyCharm (use `Ctrl+K` on Windows/Linux or `Cmd+K` on macOS, or go to **VCS → Commit**).
2. In the commit window, you will see the changed files:
   - `requirements.txt` (modified)
   - `Procfile` (new, untracked)
3. Ensure both files are checked (selected) for inclusion in the commit.
4. Write a descriptive commit message, for example:
   ```
   Add gunicorn to requirements and create Procfile for WSGI server
   ```
5. Click **Commit** (or **Commit and Push** if you want to push to a remote repository immediately).

After committing, your local Git repository now contains the configuration needed for Gunicorn. The next step in the deployment process will be to push these changes to your remote repository (e.g., GitHub) and then connect to a hosting platform, which will automatically detect the `Procfile` and use Gunicorn to serve your application.

---

### Additional Considerations

#### Testing Gunicorn Locally

While not strictly necessary for deployment, you can test that Gunicorn works correctly on your local machine. This helps catch any issues before deploying.

1. Ensure Gunicorn is installed (it should be if you ran `pip install -r requirements.txt` after adding it).
2. In the terminal, navigate to your project directory.
3. Run the following command:
   ```bash
   gunicorn main:app
   ```
   (Replace `main:app` with your module and app name.)
4. By default, Gunicorn will start listening on `127.0.0.1:8000`. Open your browser and go to `http://127.0.0.1:8000` to see your application.
5. Press `Ctrl+C` to stop the server.

If you encounter any errors, check that your application is structured correctly and that all environment variables are set (if you are using a `.env` file, you may need to load it explicitly because Gunicorn does not automatically load it; for testing, you can set variables in the terminal).

#### Alternative WSGI Servers

While Gunicorn is the focus here, other WSGI servers exist, such as **Waitress**, **uWSGI**, and **mod_wsgi**. Each has its own strengths. Gunicorn is chosen for its simplicity and widespread adoption. If you later need a server that runs on Windows without a Unix‑like environment, Waitress is a good alternative.

#### Procfile for Multiple Processes

The `Procfile` can define multiple process types. For example, you might have a separate worker process for background tasks. In that case, you would add another line:

```
worker: python worker.py
```

However, for a basic Flask application, the `web` process is sufficient.

#### Environment Variables and the Procfile

The `Procfile` itself does not handle environment variables. Those are set separately in the hosting platform’s dashboard or via configuration files. The Gunicorn command will inherit those environment variables automatically.

---

### Summary

You have now completed the essential steps to prepare your Flask application for production using Gunicorn:

- Added `gunicorn` to `requirements.txt` with a pinned version.
- Created a `Procfile` that instructs the hosting platform to run `gunicorn main:app`.
- Committed these changes to version control.

Your project is now one step closer to being deployable. In the next lessons, you will learn how to set up a remote Git repository (if you haven’t already) and deploy your application to a cloud platform like Render, where the `Procfile` will be automatically recognised and used to start your app with Gunicorn.

Remember: using a proper WSGI server is a critical part of making your web application robust, secure, and scalable. By following this guide, you have adopted an industry‑best practice that will serve you well in all future Python web projects.