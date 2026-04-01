## Environment Variables In Python Applications — Structured Reference

---

## Core Definition And Purpose

* Environment variables are external configuration values supplied to a process.
* They exist outside the Python runtime and source code.
* They are injected by the operating system or execution environment.
* They are primarily used for configuration and secret management.

---

## Why Environment Variables Are Used In Practice

* They prevent hardcoding sensitive values inside source files.
* They allow identical codebases across development and production.
* They simplify deployment across machines and cloud platforms.
* They reduce security risks from accidental repository exposure.

---

## Common Data Stored Inside Environment Variables

* API keys and authentication tokens for external services.
* Database connection strings and credentials.
* Feature flags and runtime mode selectors.
* Application behavior switches such as debug or production.

---

## How Environment Variables Exist At System Level

* Environment variables belong to a running process context.
* Each process receives environment variables at startup time.
* Child processes inherit environment variables from parent processes.
* Runtime changes do not affect already running processes.

---

## Reading Environment Variables In Python

* Python accesses environment variables through the `os` module.
* All retrieved values are returned as strings.
* Missing variables return `None` by default.

```python
import os

api_key = os.getenv("API_KEY")
```

* The application must handle missing values explicitly.

---

## Using Default Values With Environment Variables

* Default values prevent runtime crashes when variables are missing.
* They are useful for local development environments.

```python
mode = os.getenv("APP_MODE", "cli")
```

* Defaults should never be used for secrets.

---

## Accessing Environment Variables Using os.environ Mapping

* `os.environ` behaves like a dictionary interface.
* Accessing missing keys raises a KeyError exception.

```python
import os

api_key = os.environ["API_KEY"]
```

* This approach enforces strict configuration requirements.

---

## Writing Environment Variables At Runtime

* Python can set environment variables dynamically.
* These changes affect only the current process and children.

```python
import os

os.environ["APP_MODE"] = "sms"
```

* This does not modify system-wide configuration permanently.

---

## Using python-dotenv For Local Development

* `python-dotenv` loads variables from a `.env` file.
* This file simulates production environment configuration locally.
* The `.env` file must never be committed to repositories.

```python
from dotenv import load_dotenv
load_dotenv()
```

* Variables become accessible through `os.getenv` afterward.

---

## Example .env File Structure

* Each line defines a single key–value pair.
* Quotes are optional unless special characters exist.

```env
API_KEY=your_api_key_here
API_ENDPOINT=https://api.weatherapi.com/v1/forecast.json
APP_MODE=sms
SMS_MODE=whatsapp
```

* Whitespace around keys or values is not permitted.

---

## Environment Variables In Cloud Deployments

* Cloud platforms inject environment variables at runtime.
* Secrets are managed through platform-specific secret managers.
* Code remains unchanged across environments.

Examples include:

* GitHub Actions secrets configuration
* AWS Lambda environment variable settings
* Docker container environment injection

---

## Environment Variables In Docker Containers

* Variables are passed during container startup.
* They remain immutable during container execution.

```bash
docker run -e APP_MODE=sms -e SMS_MODE=whatsapp weather-app
```

* Dockerfiles should not contain secret values.

---

## Environment Variables In Scheduled Jobs And Cron

* Cron jobs require explicit variable definition.
* The execution environment is minimal by default.

```bash
APP_MODE=sms SMS_MODE=whatsapp python main.py
```

* Missing variables cause runtime failures silently.

---

## Security Best Practices For Environment Variables

* Never commit `.env` files to version control.
* Rotate secrets periodically to reduce exposure risk.
* Restrict access permissions to deployment environments.
* Avoid logging environment variable values.

---

## Common Pitfalls And Mistakes

* Assuming environment variables exist without validation.
* Forgetting to load dotenv in local development.
* Mixing configuration logic inside application logic.
* Using environment variables for large structured data.

---

## Recommended Validation Pattern

* Validate required variables at application startup.
* Fail fast with descriptive error messages.

```python
required_vars = ["API_KEY", "API_ENDPOINT"]

for var in required_vars:
    if not os.getenv(var):
        raise RuntimeError(f"Missing required environment variable: {var}")
```

* This prevents silent misconfiguration issues.

---

## Architectural Role Of Environment Variables

* They act as the boundary between code and infrastructure.
* They enable twelve-factor application principles.
* They support scalable, portable, and secure deployments.

