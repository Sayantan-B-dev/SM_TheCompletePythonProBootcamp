## Using Environment Variables to Store Sensitive Information

This document provides a comprehensive guide on replacing hardcoded secrets and configuration values in a Flask application with environment variables. Environment variables are a fundamental practice for securing sensitive data (like secret keys, database URIs, and API credentials) and for making your application adaptable across different environments (development, testing, production). By externalizing configuration, you avoid accidentally committing secrets to version control and simplify deployment.

### Why Use Environment Variables?

Hardcoding sensitive information directly in your source code presents several risks:

- **Security**: If your code is ever exposed (e.g., on a public repository), anyone can see your secret keys, database passwords, or email credentials.
- **Configuration Management**: Different environments (development, staging, production) often require different settings. Hardcoding forces you to change code before deploying.
- **Collaboration**: Team members may need their own local settings. Hardcoding makes it difficult to share a common codebase without overwriting each other's configurations.

Environment variables solve these problems by keeping configuration outside the code. Your application reads values from the environment at runtime, so the same code can run anywhere with the appropriate environment variables set.

### Step 1: Import the `os` Module

The first step is to import Python's built‑in `os` module, which provides a portable way to interact with the operating system, including reading environment variables.

```python
import os
```

Place this import at the top of your main application file (e.g., `main.py`), alongside other imports.

### Step 2: Replace the Flask Secret Key

The Flask secret key is used to securely sign session cookies and other security‑related tokens. It must be kept secret. In your original code, you might have:

```python
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
```

Replace it with a lookup from an environment variable. Choose a descriptive name for the variable, such as `FLASK_KEY`.

```python
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
```

If the environment variable `FLASK_KEY` is not set, this line will set the secret key to `None`, which will likely cause your application to fail (Flask requires a non‑empty secret key when sessions are used). To provide a fallback for development (but **never** in production), you can supply a default value as the second argument:

```python
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY', 'a-default-dev-key')
```

However, be cautious: using a default means your development environment may work without setting the variable, but you must ensure that in production the variable is always defined. A safer approach is to let the application fail explicitly if the variable is missing, so you are forced to set it.

### Step 3: Replace the Database URI

Your application likely uses a database, and the connection URI is another piece of sensitive information. The original line might be:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
```

For production, you will eventually switch to a more robust database like PostgreSQL, and the URI will include credentials. Therefore, you should retrieve it from an environment variable:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI', 'sqlite:///posts.db')
```

Here, the default value `'sqlite:///posts.db'` allows you to keep using SQLite locally without setting any environment variable. In production, you will set `DB_URI` to the full PostgreSQL connection string (e.g., `postgresql://username:password@host:port/database`). This pattern makes the transition seamless.

### Step 4: Handle Contact Form Credentials

If your application includes a contact form that sends emails (e.g., using Flask‑Mail), you likely have configuration like:

```python
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
```

Replace these with environment variables:

```python
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
```

You may also want to provide defaults for development, but again, be careful not to accidentally use real credentials. If you use a service like Gmail, you might generate an app‑specific password and store it in an environment variable.

### Step 5: Disable Debug Mode in Production

Flask’s built‑in server can run in debug mode, which provides an interactive debugger and automatically reloads on code changes. This is extremely useful during development but must never be enabled in a production environment, as it can expose sensitive information and allow arbitrary code execution.

Your original `app.run()` call might have looked like:

```python
if __name__ == "__main__":
    app.run(debug=True)
```

Change it to:

```python
if __name__ == "__main__":
    app.run(debug=False)
```

But even better, you can also control debug mode via an environment variable, so you can enable it in development without modifying code. For example:

```python
if __name__ == "__main__":
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode)
```

Then, in your development environment, set `FLASK_DEBUG=True`; in production, leave it unset or set to `False`.

### Putting It All Together: Example of Updated Code

Here is a condensed example showing how your configuration section might look after the changes:

```python
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Secret key
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')  # No default; must be set in production

# Database URI (SQLite by default for development)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI', 'sqlite:///posts.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email configuration (if using Flask-Mail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

# ... rest of your app

if __name__ == "__main__":
    # Debug mode controlled by environment variable, defaulting to False
    debug_enabled = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_enabled)
```

### Setting Environment Variables Locally

There are several ways to set environment variables on your development machine:

#### 1. Terminal / Command Line

On macOS/Linux, you can set a variable for the current shell session:

```bash
export FLASK_KEY='your-secret-key'
export DB_URI='sqlite:///posts.db'
export MAIL_USERNAME='your-email@gmail.com'
export MAIL_PASSWORD='your-app-password'
export FLASK_DEBUG='True'
```

Then run your application from the same terminal.

On Windows (Command Prompt):

```cmd
set FLASK_KEY=your-secret-key
set DB_URI=sqlite:///posts.db
```

On Windows (PowerShell):

```powershell
$env:FLASK_KEY='your-secret-key'
$env:DB_URI='sqlite:///posts.db'
```

However, these settings are temporary and will be lost when you close the terminal.

#### 2. IDE Configuration (PyCharm)

PyCharm allows you to set environment variables per run configuration:

- Go to **Run** → **Edit Configurations**.
- Select your Flask run configuration (or create one).
- In the **Environment variables** field, add variables in the format `FLASK_KEY=your-key;DB_URI=sqlite:///posts.db` (semicolon‑separated on Windows, colon on macOS/Linux? Actually PyCharm uses semicolon on Windows, but the field usually accepts a list with semicolons).
- Click **OK** and run the configuration.

This method persists the settings within the IDE.

#### 3. Using a `.env` File with `python-dotenv`

A `.env` file is a simple text file that contains key‑value pairs, one per line. For example:

```env
FLASK_KEY=8BYkEfBA6O6donzWlSihBXox7C0sKR6b
DB_URI=sqlite:///posts.db
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
FLASK_DEBUG=True
```

**Important:** Add `.env` to your `.gitignore` to ensure it is never committed to version control.

To load these variables automatically, install the `python-dotenv` package:

```bash
pip install python-dotenv
```

Then, at the beginning of your application (after importing `os`), add:

```python
from dotenv import load_dotenv

load_dotenv()  # This loads variables from a .env file into the environment
```

Now, when you run your application, the variables from `.env` will be available via `os.environ.get()`. This method is convenient for development because you don't have to set variables manually each time. However, in production, you will rely on the platform’s native environment variable settings, not a `.env` file.

### Setting Environment Variables on Cloud Platforms

When you deploy your application, each platform provides a way to set environment variables securely. Below are examples for common Python‑friendly platforms.

#### Render

- In your web service dashboard, go to **Environment**.
- Click **Add Environment Variable**.
- Enter the variable name and value (e.g., `FLASK_KEY`, `DB_URI`, `MAIL_USERNAME`, `MAIL_PASSWORD`).
- Save and redeploy if necessary.

Render also allows you to set environment variables via a `render.yaml` file if you use Infrastructure as Code.

#### Heroku

- Using the Heroku CLI:
  ```bash
  heroku config:set FLASK_KEY='your-secret-key'
  heroku config:set DB_URI='postgresql://...'
  ```
- Or via the Heroku Dashboard: open your app, go to **Settings** → **Config Vars** and add them.

#### PythonAnywhere

- Go to the **Web** tab.
- In the **Code** section, there is a link to the WSGI configuration file. You can set environment variables there by adding lines like:
  ```python
  import os
  os.environ['FLASK_KEY'] = 'your-secret-key'
  ```
  However, this hardcodes them in the WSGI file. A better approach is to use a `.env` file and load it within your application, but PythonAnywhere does not support system‑wide environment variables on the free plan. Many users opt for the WSGI file method for simplicity, but be aware that the WSGI file is not public.

#### Railway

- In the Railway dashboard, select your project, then go to **Variables**.
- Add key‑value pairs; they become environment variables for your service.

### Best Practices

- **Never hardcode secrets**: Always use environment variables or a secure secrets manager.
- **Use different values per environment**: Your development, staging, and production environments should have their own separate secrets and databases.
- **Keep a `.env.example` file**: In your repository, include a sample file (e.g., `.env.example`) with dummy values and comments explaining each variable. This helps other developers know what variables need to be set.
- **Validate required variables**: In your application, you may want to check that essential environment variables are set at startup and exit with a meaningful error if they are missing. This prevents runtime failures due to misconfiguration.
- **Never commit `.env`**: Double‑check your `.gitignore` to ensure `.env` is listed.
- **Use strong, random secret keys**: Generate a long, random string for `FLASK_KEY` (e.g., using `secrets.token_urlsafe(32)`). Do not use easy‑to‑guess values.

### Testing Locally with Environment Variables

After making the changes, test your application thoroughly in your local development environment. If you are using a `.env` file and `python-dotenv`, ensure that the file is correctly formatted and that `load_dotenv()` is called before any code that accesses the variables.

If you set variables via the terminal or IDE, verify they are being picked up. You can temporarily add print statements to debug:

```python
print("FLASK_KEY:", os.environ.get('FLASK_KEY'))
print("DB_URI:", os.environ.get('DB_URI'))
```

But remove or comment these out once you confirm everything works.

### Additional Considerations

- **Contact form email**: If you use Gmail’s SMTP, you may need to enable "Less secure app access" or use an App Password if you have two‑factor authentication enabled. Store the App Password in an environment variable.
- **API keys**: Any external service API keys (e.g., for Gravatar, CKEditor cloud services) should also be moved to environment variables.
- **Configuration for different modes**: You might have settings like `DEBUG`, `TESTING`, etc. Control them via environment variables as well.

### Conclusion

By refactoring your Flask application to use environment variables, you have significantly improved its security and portability. The same codebase can now be deployed to any environment simply by setting the appropriate variables. This practice is standard in professional software development and is a critical step toward a production‑ready application.

In the next steps, you will commit these changes to your Git repository and prepare to deploy your application to a cloud platform, where you will set the environment variables directly in the platform’s dashboard.