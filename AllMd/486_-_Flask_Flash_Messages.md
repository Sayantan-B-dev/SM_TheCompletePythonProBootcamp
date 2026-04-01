## Flask Flash Messages

### 1. Introduction to Flash Messages

In a web application, providing feedback to users about the outcome of their actions is essential for a good user experience. When a user submits a login form with an incorrect password, simply redirecting them back to the login page without any explanation leaves them confused. Similarly, if they try to register with an email that is already taken, they need to know why they cannot proceed.

**Flash messages** are a simple yet powerful way to send one‑time notifications from the server to the client. A flash message is stored in the session and is available to the next rendered template. After that, it is automatically removed. This makes them perfect for displaying error messages, success confirmations, or any transient information.

Flask provides built‑in support for flashing via the `flash()` function and the `get_flashed_messages()` template function.

---

### 2. How Flask Flashing Works

1. **In your route**, you call `flash(message, category)` to store a message. The `category` is optional and can be used to style the message (e.g., `'error'`, `'success'`, `'info'`).
2. **The message is saved in the user’s session** (which is a secure cookie) until the next request.
3. **In your template**, you call `get_flashed_messages(with_categories=True)` to retrieve all pending messages. They are removed from the session after being retrieved.
4. You then loop through the messages and display them in the HTML, often within a styled `<div>` or `<p>`.

This pattern ensures that messages appear exactly once and do not reappear after a page refresh.

---

### 3. Setting Up Flash Messages in the Application

Your Flask application already has a secret key configured (`app.config['SECRET_KEY']`), which is necessary for signing the session cookie. The flash system relies on the session, so no additional setup is required.

You will now modify three routes:

- `/login` – to handle two error cases: email not found and incorrect password.
- `/register` – to handle the case where a user tries to register with an email that already exists.

In each case, instead of returning a plain text error message, you will `flash()` an appropriate message and redirect back to the form.

---

### 4. Task 1: Flash Message for Non‑Existent Email in Login

When a user submits the login form with an email that is not in the database, you should inform them that the email does not exist and suggest they register.

**Updated `/login` route (partial):**

```python
from flask import flash

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash('That email does not exist. Please try again or register.')
            return redirect(url_for('login'))
        
        # ... rest of password verification
    return render_template('login.html')
```

**Explanation:**

- `flash('That email does not exist. Please try again or register.')` stores the message in the session.
- `redirect(url_for('login'))` sends the user back to the login page.
- When the login page template renders, it will retrieve and display this message.

---

### 5. Task 2: Flash Message for Incorrect Password in Login

If the email exists but the password is wrong, flash an error message.

**Extend the `/login` route:**

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash('That email does not exist. Please try again or register.')
            return redirect(url_for('login'))
        
        if not check_password_hash(user.password, password):
            flash('Incorrect password. Please try again.')
            return redirect(url_for('login'))
        
        # Password correct – log in
        login_user(user)
        return redirect(url_for('secrets'))
    
    return render_template('login.html')
```

**Note:** The order of checks matters. First check existence, then password. Both error cases flash a message and redirect back to the login page.

---

### 6. Task 3: Flash Message for Already Registered Email in Registration

When a user tries to register with an email that is already in the database, you should inform them that the email is taken and redirect them to the login page (since they may already have an account).

**Updated `/register` route:**

```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('You have already registered with that email. Please log in.')
            return redirect(url_for('login'))
        
        # Hash password and create user
        hashed_password = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return redirect(url_for('secrets'))
    
    return render_template('register.html')
```

**Explanation:**

- If the email exists, flash a message and redirect to the login page (so the user can log in with their existing account).
- If the email is new, proceed with registration.

---

### 7. Displaying Flash Messages in Templates

Now that messages are being flashed, you need to display them in your templates. Typically, you add a block near the top of your base template or in each form template.

**In `login.html` (or a shared template), add:**

```html
{% with messages = get_flashed_messages() %}
  {% if messages %}
    <ul class="flashes">
    {% for message in messages %}
      <li>{{ message }}</li>
    {% endfor %}
    </ul>
  {% endif %}
{% endwith %}
```

If you want to use categories (e.g., different colors for errors vs. success), use `get_flashed_messages(with_categories=True)`:

```html
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    {% for category, message in messages %}
      <p class="flash-{{ category }}">{{ message }}</p>
    {% endfor %}
  {% endif %}
{% endwith %}
```

Then in your CSS, you can define styles like `.flash-error { color: red; }`, `.flash-success { color: green; }`.

For simplicity, the hints suggest a `<p>` tag showing up as red text. You can achieve that by adding a CSS rule:

```css
.flash-error {
    color: red;
}
```

And in the template, assign that class based on the category.

**Example of displaying messages as red paragraphs:**

```html
{% with messages = get_flashed_messages() %}
  {% if messages %}
    {% for message in messages %}
      <p style="color: red;">{{ message }}</p>
    {% endfor %}
  {% endif %}
{% endwith %}
```

Place this code inside the login and register templates, typically above the form.

---

### 8. Styling Flash Messages with Categories

To make the messages more meaningful, you can pass a category when calling `flash()`. For example:

```python
flash('Incorrect password. Please try again.', 'error')
```

Then in the template, you can use the category to apply different styles.

**Update the flash calls in the routes:**

```python
flash('That email does not exist. Please try again or register.', 'error')
flash('Incorrect password. Please try again.', 'error')
flash('You have already registered with that email. Please log in.', 'info')
```

**Template code to display categorized messages:**

```html
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    {% for category, message in messages %}
      <p class="flash-{{ category }}">{{ message }}</p>
    {% endfor %}
  {% endif %}
{% endwith %}
```

**CSS:**

```css
.flash-error {
    color: red;
    font-weight: bold;
}
.flash-info {
    color: blue;
}
```

---

### 9. Complete Updated Code for Routes

Below are the complete `/login` and `/register` routes with flash messages integrated.

```python
from flask import flash

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash('That email does not exist. Please try again or register.', 'error')
            return redirect(url_for('login'))
        
        if not check_password_hash(user.password, password):
            flash('Incorrect password. Please try again.', 'error')
            return redirect(url_for('login'))
        
        login_user(user)
        return redirect(url_for('secrets'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('You have already registered with that email. Please log in.', 'info')
            return redirect(url_for('login'))
        
        hashed_password = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return redirect(url_for('secrets'))
    
    return render_template('register.html')
```

**Note:** You may also want to add flash messages for successful actions (e.g., "Registration successful! You are now logged in."). This is optional but can enhance user experience.

---

### 10. Testing the Flash Messages

1. **Run the application.**
2. **Login with a non‑existent email.** You should be redirected to the login page and see the message "That email does not exist. Please try again or register."
3. **Login with an existing email but wrong password.** You should see "Incorrect password. Please try again."
4. **Try to register with an email that already exists.** You should be redirected to the login page and see "You have already registered with that email. Please log in."

Refresh the login page after seeing a flash message; the message should disappear because it was consumed.

---

### 11. Common Pitfalls and Best Practices

| Pitfall | Solution |
|---------|----------|
| Flash messages not appearing | Ensure you have called `get_flashed_messages()` in the template **before** any output. Also verify that the session is working (secret key set). |
| Messages appearing on every page | Make sure you only retrieve flashed messages in templates where you intend to display them. If you place the code in `base.html`, they will appear on every page after a redirect. That might be desirable for a global notification area, but ensure it's styled appropriately. |
| Messages not disappearing after refresh | This indicates that `get_flashed_messages()` was not called in the template that rendered after the redirect. The message remains in the session until retrieved. |
| Using categories without styling | Categories are just strings; you must define corresponding CSS classes. |
| Over‑flashing | Do not overuse flash messages for trivial information; reserve them for important user feedback. |

---

### 12. Further Enhancements

- **Add a close button** to allow users to dismiss flash messages.
- **Use Bootstrap alerts** for pre‑styled messages if you are using Bootstrap.
- **Include a success flash** after registration or logout to confirm the action.
- **Implement message categories** for different severity levels (error, warning, success, info).

---

### 13. Summary

Flash messages are an integral part of a user‑friendly authentication system. They provide immediate, contextual feedback that guides users through the login and registration process. By integrating `flash()` and `get_flashed_messages()`, you have transformed your application from a silent system that simply redirects into one that communicates clearly with its users.

In the next lesson, you will learn how to conditionally render parts of your templates based on whether the user is authenticated, further refining the user experience.