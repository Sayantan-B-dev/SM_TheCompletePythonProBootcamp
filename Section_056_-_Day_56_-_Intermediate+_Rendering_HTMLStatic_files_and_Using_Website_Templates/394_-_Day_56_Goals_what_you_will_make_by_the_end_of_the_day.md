## Flask Environment Variables — Complete Reference

Flask configuration through environment variables allows runtime control without modifying source code. Below is a structured breakdown of all relevant variables, including core Flask variables and related Python environment settings.

---

# 1. Core Flask CLI Variables

These are used by the `flask` command-line interface.

### `FLASK_APP`

Specifies the application entry module.

```bash
FLASK_APP=server
```

Meaning: Flask will look for `app = Flask(__name__)` inside `server.py`.

---

### `FLASK_ENV`  (Deprecated in Flask 2.3+)

Previously used to toggle development mode.

```bash
FLASK_ENV=development
```

Now replaced by `FLASK_DEBUG`.

---

### `FLASK_DEBUG`

Enables debug mode.

```bash
FLASK_DEBUG=1
```

Equivalent to:

```python
app.run(debug=True)
```

---

### `FLASK_RUN_HOST`

Specifies host binding address.

```bash
FLASK_RUN_HOST=0.0.0.0
```

Common values:

| Value     | Meaning                 |
| --------- | ----------------------- |
| 127.0.0.1 | Localhost only          |
| 0.0.0.0   | Accessible from network |

---

### `FLASK_RUN_PORT`

Sets port number.

```bash
FLASK_RUN_PORT=5001
```

Default is `5000`.

---

### `FLASK_RUN_CERT`

Specifies SSL certificate file.

```bash
FLASK_RUN_CERT=cert.pem
```

---

### `FLASK_RUN_KEY`

Specifies SSL private key.

```bash
FLASK_RUN_KEY=key.pem
```

Used together with `FLASK_RUN_CERT` for HTTPS development.

---

### `FLASK_RUN_EXTRA_FILES`

Comma-separated list of extra files to watch for reload.

```bash
FLASK_RUN_EXTRA_FILES=config.yaml,settings.json
```

---

# 2. Application-Specific Environment Variables

These are accessed via:

```python
os.getenv("VARIABLE_NAME")
```

Example in your code:

```python
SECRET_KEY = os.getenv("SECRET_KEY")
```

Common application-level variables:

| Variable         | Purpose                      |
| ---------------- | ---------------------------- |
| `SECRET_KEY`     | Session signing security     |
| `DATABASE_URL`   | Database connection string   |
| `API_KEY`        | External service credentials |
| `MAIL_SERVER`    | Email service configuration  |
| `MAIL_PORT`      | SMTP port                    |
| `JWT_SECRET_KEY` | Token signing key            |

---

# 3. Python Runtime Environment Variables

These influence Python execution itself.

### `PYTHONPATH`

Adds custom module search paths.

```bash
PYTHONPATH=.
```

---

### `PYTHONUNBUFFERED`

Disables output buffering.

```bash
PYTHONUNBUFFERED=1
```

Useful for logging in production containers.

---

### `PYTHONDONTWRITEBYTECODE`

Prevents `.pyc` file creation.

```bash
PYTHONDONTWRITEBYTECODE=1
```

---

# 4. Werkzeug / Development Server Variables

Werkzeug powers Flask's development server.

### `WERKZEUG_RUN_MAIN`

Internal variable used during reloader execution.

Automatically managed. Do not set manually.

---

# 5. Production Deployment Variables

When deploying with production servers:

### `GUNICORN_CMD_ARGS`

Example:

```bash
GUNICORN_CMD_ARGS="--bind=0.0.0.0:8000 --workers=4"
```

---

### `PORT`

Common in cloud platforms like Heroku.

```bash
PORT=8000
```

Then inside Flask:

```python
port = int(os.environ.get("PORT", 5000))
app.run(port=port)
```

---

# 6. Using `.env` File

With `python-dotenv`, create:

```
.env
```

Example content:

```
FLASK_APP=server
FLASK_DEBUG=1
SECRET_KEY=super_secret_value
FLASK_RUN_PORT=5001
```

Flask automatically loads `.env` if `python-dotenv` is installed.

---

# 7. Full Example Setup (Development)

### `.env`

```
FLASK_APP=server
FLASK_DEBUG=1
FLASK_RUN_HOST=127.0.0.1
FLASK_RUN_PORT=5000
SECRET_KEY=my_secret_key
```

Then run:

```bash
flask run
```

---

# 8. Environment Variable Scope

Environment variables can be set:

| Scope           | Persistence     |
| --------------- | --------------- |
| Command line    | Temporary       |
| `.env` file     | Project-level   |
| System settings | Global          |
| Dockerfile      | Container-level |

---

# 9. How Flask CLI Resolves Application

Flask looks in this order:

1. `--app` argument
2. `FLASK_APP` variable
3. `app.py` file
4. `wsgi.py` file

If none found → error: *Could not locate a Flask application.*

---

# 10. Recommended Development Setup

For `server.py`:

```
FLASK_APP=server
FLASK_DEBUG=1
SECRET_KEY=strong_random_string
```

Then:

```bash
flask run
```

Or bypass CLI entirely:

```bash
python server.py
```

---

This covers the complete environment variable ecosystem relevant to Flask applications, development server behavior, Python runtime configuration, and production deployment settings.
