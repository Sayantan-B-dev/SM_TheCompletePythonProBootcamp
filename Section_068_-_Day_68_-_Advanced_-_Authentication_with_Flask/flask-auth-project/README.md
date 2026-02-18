# Flask Authentication Project

This project demonstrates a complete user authentication system built with Flask. It includes registration, login, logout, protected routes, file download, flash messages, and conditional template rendering. Passwords are securely hashed using Werkzeug's `pbkdf2:sha256` with a salt.

## Technologies Used

| Technology | Purpose |
|------------|---------|
| **Flask** | Web framework – handles routing, requests, responses, and template rendering. |
| **Flask-SQLAlchemy** | Database ORM – defines the `User` model and interacts with SQLite. |
| **Flask-Login** | Session management – provides `login_user`, `logout_user`, `@login_required`, and `current_user`. |
| **Werkzeug** | Password hashing – `generate_password_hash` and `check_password_hash` with `pbkdf2:sha256` and salt. |
| **Jinja2** | Templating engine – used for all HTML templates with inheritance and conditionals. |
| **SQLite** | Lightweight database – stores user data in `users.db`. |

## Features

- **User Registration** – New users can sign up with name, email, and password. Passwords are hashed before storage.
- **User Login** – Existing users can log in with email and password. Credentials are verified securely.
- **Protected Routes** – The `/secrets` and `/download` routes are accessible only to logged‑in users (decorated with `@login_required`).
- **File Download** – Authenticated users can download a secret PDF (`static/files/cheat_sheet.pdf`).
- **Flash Messages** – Informative one‑time messages for success, error, and info (e.g., incorrect password, duplicate email).
- **Conditional Navigation** – The navigation bar and home page change based on login status (hide Login/Register when logged in, show Logout).
- **Responsive CSS** – Basic styling for forms, buttons, flash messages, and layout.

## How to Run

1. **Clone or create the project** using the folder structure above.
2. **Place a PDF file** named `cheat_sheet.pdf` inside `static/files/`. (You can use any PDF or create an empty placeholder.)
3. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Run the application**:
   ```bash
   python main.py
   ```
6. **Open your browser** and go to `http://127.0.0.1:5000`.

## Project Structure Explained

- **main.py** – The core Flask application. Contains configuration, database model, routes, and Flask‑Login setup.
- **templates/** – Jinja2 HTML files. `base.html` provides the common layout; other pages extend it.
- **static/css/styles.css** – Custom styling for the entire application.
- **static/files/cheat_sheet.pdf** – The secret file that only authenticated users can download.
- **requirements.txt** – List of Python packages needed.

## Security Notes

- The `SECRET_KEY` in `main.py` should be changed to a strong, random value in production.
- The password hashing uses `pbkdf2:sha256` with 600,000 iterations (Werkzeug default) and a salt length of 8 (as per lesson requirements). For higher security, consider increasing the salt length or switching to `scrypt`.
- All sensitive routes are protected with `@login_required`.
- Flash messages are displayed only once and then cleared.

## Customization

- To change the downloadable file, replace `static/files/cheat_sheet.pdf` with your own file.
- Modify the CSS in `static/css/styles.css` to match your preferred look.
- Add more user fields (e.g., profile picture, bio) by extending the `User` model and updating the registration form.

## License

This project is for educational purposes. Feel free to use and modify it for your own learning.


---

### ✅ Final Steps

1. **Place a PDF** named `cheat_sheet.pdf` inside `static/files/`. If you don't have one, create an empty text file and rename it – the download will still work, but the content will be empty.
2. **Run the app** as described in the README.
3. **Test all features**: register, log in, log out, access secrets, download file, and observe flash messages.
