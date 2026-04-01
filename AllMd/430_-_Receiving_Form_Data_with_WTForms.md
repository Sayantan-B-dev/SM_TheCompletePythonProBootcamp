This section marks a major milestone: you'll finally use the validated form data to make a decision—granting or denying access to the secret page. The key takeaway is how **WTForms simplifies data access** compared to raw HTML forms.

### 1. Accessing Form Data with `.data`
With a standard HTML form, you'd access data using the Flask `request` object:
```python
email = request.form.get('email')
```
WTForms provides a much cleaner, object-oriented way. After validation, each field's submitted value is available as an attribute of the form object using `.data`.

**Basic data access pattern:**
```python
if form.validate_on_submit():
    submitted_email = form.email.data
    submitted_password = form.password.data
    # Now you can use these variables
```

This is more readable and less error-prone than manually pulling from `request.form`.

### 2. The Power of `validate_on_submit()`
The tutorial correctly highlights that `validate_on_submit()` replaces the manual `if request.method == "POST"` check. It's a combined condition that:
- Checks for a POST request
- Runs all field validators
- Returns `True` only if **both** conditions are satisfied

This means you can safely access `.data` inside the `if` block, knowing the data is both present and valid.

### 3. Complete Route Logic for the Challenge
The challenge asks you to check specific credentials (`admin@email.com` / `12345678`) and render different pages based on the result. Here's the complete implementation:

```python
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__)
app.secret_key = "your-secret-key"

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Log In')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # This block runs only for POST with valid data
        if form.email.data == "admin@email.com" and form.password.data == "12345678":
            return render_template("success.html")
        else:
            return render_template("denied.html")
    # For GET requests or failed validation, show the login form
    return render_template("login.html", form=form)

if __name__ == '__main__':
    app.run(debug=True)
```

### 4. Understanding the Flow
- **GET request** (first visit to `/login`): `validate_on_submit()` is `False`, so it skips the `if` block and renders the empty form.
- **POST with invalid data**: `validate_on_submit()` is `False`, so it again renders the form—but this time with error messages populated (as set up in the previous lesson).
- **POST with valid but incorrect credentials**: `validate_on_submit()` is `True`, enters the block, checks credentials, finds they don't match, and renders `denied.html`.
- **POST with valid and correct credentials**: Enters block, credentials match, renders `success.html`.

### 5. Why This Approach Matters
1. **Separation of concerns**: Validation logic stays in the form class; business logic (checking credentials) stays in the route.
2. **Clean data access**: No manual parsing of `request.form`.
3. **Security**: You're working with data that has already passed validation rules.

### Common Pitfalls to Avoid
- Forgetting to add `methods=["GET", "POST"]` to the route—without POST, the form submission will fail.
- Trying to access `.data` outside the `validate_on_submit()` block for a POST request—it might be empty or invalid.
- Hardcoding credentials as shown—in a real app, you'd check against a database with hashed passwords.

### Final Check
Make sure you have both `success.html` and `denied.html` templates in your `templates` folder. They can be simple for now—the tutorial provides them in the starter files. With this code, your login system now has:
- ✅ Field validation (required, email format, password length)
- ✅ CSRF protection
- ✅ Credential checking
- ✅ Conditional rendering based on authentication result

This is the foundation of any user-based web application.