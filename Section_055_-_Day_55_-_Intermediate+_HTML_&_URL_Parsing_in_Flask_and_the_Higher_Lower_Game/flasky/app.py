# -----------------------------
# Standard Library Imports
# -----------------------------

import os                 # Used to access environment variables
import time               # Used for performance timing
import random             # Used to generate random numbers
import functools          # Used to preserve metadata in decorators

# -----------------------------
# Third-Party Imports
# -----------------------------

from dotenv import load_dotenv                     # Loads variables from .env file
from flask import Flask, render_template, request, redirect, url_for, session
# Flask        -> Main web framework
# render_template -> Renders HTML templates
# request      -> Access incoming HTTP request data
# redirect     -> Redirect user to another route
# url_for      -> Dynamically build route URLs
# session      -> Store user-specific session data

from rich.console import Console  # Rich styled console output
from rich.table import Table      # Rich formatted tables
from rich.panel import Panel      # Rich bordered message panels
from rich import box              # Table border styles

# -----------------------------
# Environment Configuration
# -----------------------------

load_dotenv()  # Load environment variables from .env file if present

console = Console()  # Initialize Rich console instance

# -----------------------------
# Flask App Initialization
# -----------------------------

app = Flask(__name__)  # Create Flask application instance

# Secret key is required to sign session cookies securely
# It is loaded from environment variable or fallback value
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key")


# ============================================================
# Logging Decorator
# ============================================================

def log_access(func):
    """
    Logs route access details to console using Rich table.
    """
    @functools.wraps(func)  # Preserves original function metadata
    def wrapper(*args, **kwargs):

        # Create styled table for logging
        table = Table(title="Route Access Log", box=box.SIMPLE)

        # Add table columns
        table.add_column("Field", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")

        # Log useful request metadata
        table.add_row("Route", func.__name__)                     # Function name
        table.add_row("Method", request.method)                   # HTTP method
        table.add_row("Path", request.path)                       # URL path
        table.add_row("Session Auth", str(session.get("is_authenticated")))  # Auth status

        console.print(table)  # Print table to console

        return func(*args, **kwargs)  # Execute original route function

    return wrapper


# ============================================================
# Execution Time Decorator
# ============================================================

def measure_execution_time(func):
    """
    Measures and prints execution time of route function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        start = time.perf_counter()  # High precision start time
        result = func(*args, **kwargs)  # Execute original function
        end = time.perf_counter()  # End time after execution

        # Print execution time using Rich panel
        console.print(
            Panel(
                f"[bold green]{func.__name__}[/bold green] executed in "
                f"[yellow]{end - start:.5f} seconds[/yellow]",
                title="Performance",
                border_style="blue"
            )
        )

        return result  # Return original function response

    return wrapper


# ============================================================
# Authentication Decorator
# ============================================================

def require_auth(func):
    """
    Restricts access to authenticated users only.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        # Check session authentication flag
        if not session.get("is_authenticated"):

            # Log unauthorized attempt
            console.print(
                Panel(
                    "[bold red]Unauthorized access attempt[/bold red]",
                    title="Security Alert",
                    border_style="red"
                )
            )

            # Redirect user to login page
            return redirect(url_for("login"))

        # If authenticated, continue normally
        return func(*args, **kwargs)

    return wrapper


# ============================================================
# Routes
# ============================================================

@app.route("/")
@log_access
@measure_execution_time
def homepage():
    """
    Public homepage route.
    Renders index.html template.
    """
    return render_template("index.html")


@app.route("/about")
@log_access
@measure_execution_time
@require_auth  # Requires authentication before access
def about_page():
    """
    Protected route.
    Only accessible if user is authenticated.
    """
    return render_template("about.html")


@app.route("/login", methods=["GET", "POST"])
@log_access
@measure_execution_time
def login():
    """
    Handles user login.
    GET  -> Show login form.
    POST -> Validate credentials.
    """

    if request.method == "POST":

        # Extract form data safely
        username = request.form.get("username")
        password = request.form.get("password")

        # Simple hardcoded authentication check
        if username == "admin" and password == "1234":

            # Store authentication flag in session
            session["is_authenticated"] = True

            # Store random number for guessing game
            session["secret_number"] = random.randint(1, 10)

            # Log successful login
            console.print(
                Panel(
                    "[bold green]User authenticated successfully[/bold green]",
                    title="Login Success",
                    border_style="green"
                )
            )

            # Redirect to guessing game page
            return redirect(url_for("guess_number"))

        # If credentials invalid
        console.print(
            Panel(
                "[bold red]Invalid credentials[/bold red]",
                title="Login Failed",
                border_style="red"
            )
        )

        return "Invalid credentials"

    # If GET request, render login page
    return render_template("login.html")


@app.route("/logout")
@log_access
@measure_execution_time
def logout():
    """
    Clears user session and logs user out.
    """

    session.clear()  # Remove all session data

    console.print(
        Panel(
            "[bold yellow]User logged out[/bold yellow]",
            title="Session Cleared",
            border_style="yellow"
        )
    )

    return redirect(url_for("homepage"))


@app.route("/guess_number", methods=["GET", "POST"])
@log_access
@measure_execution_time
@require_auth  # Only accessible when logged in
def guess_number():
    """
    Simple number guessing game.
    Compares user guess with secret number stored in session.
    """

    message = None  # Message to display on page

    if request.method == "POST":
        try:
            # Convert input to integer
            user_guess = int(request.form.get("guess"))

            # Retrieve secret number from session
            secret_number = session.get("secret_number")

            # Compare guess with secret number
            if user_guess == secret_number:
                message = "Correct! You guessed the number."
            elif user_guess > secret_number:
                message = "Too high!"
            else:
                message = "Too low!"

        # Handle invalid input cases
        except (TypeError, ValueError):
            message = "Invalid input."

    # Render template with dynamic message
    return render_template("guess_number.html", message=message)


# ============================================================
# Application Entry Point
# ============================================================

if __name__ == "__main__":

    # Log application startup
    console.print(
        Panel(
            "[bold cyan]Starting Flask Application[/bold cyan]",
            border_style="cyan"
        )
    )
    
    # Run development server
    # debug=True enables auto-reload and detailed error pages
    app.run(debug=True)
