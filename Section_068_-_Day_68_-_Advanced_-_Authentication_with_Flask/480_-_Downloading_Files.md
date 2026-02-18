## Downloading Files

### 1. Introduction

After a user successfully registers and is redirected to the secret page, we want to offer them a downloadable resource – a secret Flask programming cheat sheet in PDF format. The file is already placed in the project at `static/files/cheat_sheet.pdf`. In this lesson, you will create a route `/download` that serves this file to the user when they click a button on the secrets page.

Serving files in Flask can be done in several ways. The simplest is to place the file in the `static` folder and let users access it directly via a URL like `/static/files/cheat_sheet.pdf`. However, that would allow anyone who knows the URL to download the file, even without being logged in. To control access, we will create a dedicated route that checks authentication (later) and then uses Flask's `send_from_directory` function to securely deliver the file.

### 2. The `send_from_directory` Function

Flask provides a helper function called `send_from_directory` that safely sends a file from a given directory. It is designed to prevent directory traversal attacks by ensuring that the requested file is indeed within the specified directory.

**Syntax:**

```python
from flask import send_from_directory

send_from_directory(directory, filename, **options)
```

- `directory` – the absolute or relative path to the directory containing the file.
- `filename` – the name of the file to send (must be within the directory).
- `**options` – additional keyword arguments passed to the underlying WSGI server (e.g., `as_attachment=True` to force download, `attachment_filename` to set a different download name).

**Why use `send_from_directory`?**

- It validates that the requested file path is inside the given directory, mitigating path traversal attacks.
- It automatically handles range requests, caching headers, and other HTTP details.
- It works well with Flask’s development server and production WSGI servers.

### 3. Modifying the Secrets Template

First, update the `secrets.html` template to include a link that points to the `/download` route. The existing template already has a placeholder anchor tag:

```html
<a href="{{ url_for('download') }}">Download Your File</a>
```

The `url_for('download')` function generates the URL for the route named `download`. We will soon define that route. If the route is not yet defined, Flask will raise an error when rendering the template, so we must create the route before testing the link.

### 4. Creating the Download Route

Add a new route to `main.py`:

```python
from flask import send_from_directory

@app.route('/download')
def download():
    # For now, no authentication check; we will add it later with Flask-Login
    return send_from_directory('static', path='files/cheat_sheet.pdf')
```

**Explanation:**

- The route is bound to `/download` and accepts GET requests (the default).
- Inside the function, we call `send_from_directory` with:
  - `directory='static'` – the name of the directory (relative to the application root).
  - `path='files/cheat_sheet.pdf'` – the path to the file within that directory. The parameter is named `path` (or `filename` depending on Flask version; both work). We explicitly use `path` to avoid ambiguity.

When a user navigates to `/download`, Flask will locate the file `static/files/cheat_sheet.pdf` and send it to the client. The browser will typically prompt to download the file, displaying the filename `cheat_sheet.pdf`.

### 5. Testing the Download

1. Ensure your Flask application is running.
2. Register a new user or simply navigate to the secrets page by manually appending `?name=Test` to the URL (e.g., `http://127.0.0.1:5000/secrets?name=Test`). The secrets page should render with the download link.
3. Click the **Download Your File** link. The browser should either download `cheat_sheet.pdf` or open it in a new tab (depending on browser settings). You should see the PDF content.

If you encounter a 404 error, double-check the file path. The file must exist at `static/files/cheat_sheet.pdf` relative to where `main.py` is running. The `static` folder should be in the same directory as `main.py`.

### 6. Important Considerations

#### 6.1 Security – No Authentication Yet

At this point, the `/download` route is publicly accessible. Anyone who knows the URL `http://127.0.0.1:5000/download` can download the file without logging in. This is **not** secure. In a later lesson, when we integrate Flask-Login, we will protect this route by requiring authentication. For now, we are just implementing the file serving mechanism.

#### 6.2 Alternative: Using `send_file`

Flask also has a `send_file` function that can send a file given its full path. However, `send_from_directory` is preferred when serving files from a known directory because it adds an extra layer of path validation.

#### 6.3 Absolute vs Relative Paths

The `directory` argument can be an absolute path or a relative path. A relative path is resolved relative to the current working directory (usually where the Flask app is run). To make it robust, you can construct an absolute path using `os.path`:

```python
import os
from flask import send_from_directory

@app.route('/download')
def download():
    static_dir = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_dir, 'files/cheat_sheet.pdf')
```

But for simplicity, the relative path `'static'` works as long as the application is started from the project root.

#### 6.4 Forcing Download vs Inline Display

By default, `send_from_directory` lets the browser decide how to handle the file based on its MIME type. PDFs are often displayed inline (in the browser). If you want to force a download dialog, add the `as_attachment` parameter:

```python
return send_from_directory('static', path='files/cheat_sheet.pdf', as_attachment=True)
```

You can also specify a different filename for the download using `download_name` (Flask 2.0+) or `attachment_filename` (older versions):

```python
return send_from_directory('static', path='files/cheat_sheet.pdf', as_attachment=True, download_name='secret_cheat_sheet.pdf')
```

### 7. Code Summary

After adding the download route, your `main.py` now includes:

```python
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('secrets', name=name))
    return render_template('register.html')

@app.route('/secrets')
def secrets():
    name = request.args.get('name')
    return render_template('secrets.html', name=name)

@app.route('/download')
def download():
    return send_from_directory('static', path='files/cheat_sheet.pdf')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    pass

if __name__ == '__main__':
    app.run(debug=True)
```

### 8. Next Steps

You have successfully implemented file downloading. In the next lessons, you will learn about encryption and hashing, which are essential for storing passwords securely. After that, you will integrate Flask-Login to add authentication and protect the secrets page and download route.