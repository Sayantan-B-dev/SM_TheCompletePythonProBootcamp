## Hashing and Salting Passwords using Werkzeug

### 1. Introduction

In the current state of the project, user passwords are stored in the `users.db` database as **plaintext**. This is a critical security vulnerability. If an attacker gains access to the database, they can immediately read every user's password. Since many users reuse passwords across multiple sites, a single breach could compromise their accounts elsewhere.

To fix this, you must **hash** passwords before storing them. Hashing transforms a password into a fixed-length string of characters using a one-way mathematical function. From the hash, it is computationally infeasible to recover the original password. Additionally, you will add a **salt** – a random value unique to each user – to ensure that even if two users choose the same password, their stored hashes will be different.

Flask uses **Werkzeug**, a comprehensive WSGI utility library, which includes robust security helpers for password hashing. This lesson guides you through using Werkzeug's `generate_password_hash` and `check_password_hash` functions to implement secure password storage.

---

### 2. Why Werkzeug for Password Hashing?

Werkzeug is a dependency of Flask and is already installed in your project. Its security module provides:

- **Industry-standard algorithms:** Supports `pbkdf2:sha256` and `scrypt` (from version 2.3 onwards).
- **Automatic salt generation:** Generates a cryptographically secure random salt for each password.
- **Salted hash storage:** The salt is embedded in the resulting hash string, so you don't need a separate database column.
- **Constant-time comparison:** The verification function `check_password_hash` uses a constant-time algorithm to prevent timing attacks.

By using Werkzeug's built-in functions, you avoid the common pitfalls of implementing your own cryptographic code.

---

### 3. The `generate_password_hash` Function

#### 3.1 Function Signature

```python
werkzeug.security.generate_password_hash(password, method='scrypt', salt_length=16)
```

**Parameters:**

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `password` | `str` | The plaintext password to hash. | (required) |
| `method` | `str` | The key derivation function and its parameters. | `'scrypt'` |
| `salt_length` | `int` | The number of characters to generate for the salt. | `16` |

**Return Value:** A string containing the salt, the algorithm parameters, and the hash itself, all encoded in a format that `check_password_hash` can later parse.

#### 3.2 Available Methods

Werkzeug 3.0.x supports two primary methods:

- **`'scrypt'` (default):** Uses the `hashlib.scrypt` function. You can specify parameters like `scrypt:32768:8:1` (where 32768 = `n`, 8 = `r`, 1 = `p`). Scrypt is memory-hard, making it more resistant to GPU-based attacks.
- **`'pbkdf2'`:** Uses `hashlib.pbkdf2_hmac`. You can specify the hash algorithm and iterations, e.g., `'pbkdf2:sha256:600000'`. This is a widely used, NIST-approved key derivation function.

For this lesson, the requirement is to use **`pbkdf2:sha256`** with a **salt length of 8**. Although the default `salt_length` is 16, you will explicitly set it to 8 to match the lesson instructions.

**Note:** In production, a salt length of 16 or higher is recommended. The lesson uses 8 for simplicity and to demonstrate the parameter.

---

### 4. Step-by-Step Implementation

#### 4.1 Delete Existing Plaintext Entries

Before you start, open the `users.db` database using a tool like DB Browser for SQLite and delete any rows that contain plaintext passwords. Alternatively, you can simply delete the database file and let SQLAlchemy recreate it (this will also delete all data). For a clean start:

```bash
# From the terminal in your project folder
rm users.db
```

Then, in `main.py`, ensure that `db.create_all()` is called within an application context so that a fresh, empty `users.db` is created when you run the app.

#### 4.2 Import the Security Functions

At the top of `main.py`, add the necessary imports from `werkzeug.security`:

```python
from werkzeug.security import generate_password_hash, check_password_hash
```

#### 4.3 Modify the Registration Route to Hash Passwords

In the `/register` route, replace the line that stores the plaintext password with a call to `generate_password_hash`.

**Before (insecure):**

```python
new_user = User(
    name=name,
    email=email,
    password=password  # Stored as plaintext
)
```

**After (secure):**

```python
# Hash the password using pbkdf2:sha256 with salt length 8
hashed_password = generate_password_hash(
    password,
    method='pbkdf2:sha256',
    salt_length=8
)

new_user = User(
    name=name,
    email=email,
    password=hashed_password
)
```

**Complete updated `/register` route:**

```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Hash the password
        hashed_password = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=8
        )
        
        # Create new user with hashed password
        new_user = User(
            name=name,
            email=email,
            password=hashed_password
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Redirect to secrets page
        return redirect(url_for('secrets', name=name))
    
    return render_template('register.html')
```

**What happens now:**

- The password is hashed using PBKDF2-HMAC-SHA256 with 600,000 iterations (default for `pbkdf2:sha256` in Werkzeug 3.0+).
- A random 8-character salt is generated and used in the hashing process.
- The final string stored in the database will look something like:  
  `pbkdf2:sha256:600000$8-character-salt$actual-hash`  
  (The exact format is `method$salt$hash`.)

#### 4.4 Update the Login Route to Verify Hashed Passwords

The login route must now use `check_password_hash` to verify the password against the stored hash.

**Current `/login` route (placeholder):**

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # TODO: Find user by email and verify password
        # For now, just redirect to secrets with a placeholder name
        return redirect(url_for('secrets', name="User"))
    
    return render_template('login.html')
```

**Updated `/login` route with password verification:**

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Verify password against stored hash
            if check_password_hash(user.password, password):
                # Password correct – log the user in (Flask-Login will handle this later)
                return redirect(url_for('secrets', name=user.name))
            else:
                # Password incorrect
                return "Incorrect password. <a href='/login'>Try again</a>"
        else:
            # User not found
            return "Email not found. <a href='/register'>Register</a>"
    
    return render_template('login.html')
```

**Explanation of `check_password_hash`:**

- It takes the stored hash (from the database) and the plaintext password attempt.
- It parses the stored hash to extract the method, salt, and iterations.
- It re-hashes the provided password using the extracted method, salt, and iterations.
- It compares the newly computed hash to the stored hash in constant time (to prevent timing attacks).
- Returns `True` if they match, `False` otherwise.

#### 4.5 Understanding the Stored Hash Format

After hashing a password with `generate_password_hash(method='pbkdf2:sha256', salt_length=8)`, the stored string looks like:

```
pbkdf2:sha256:600000$abcdefgh$hashedvalue
```

| Component | Example | Description |
|-----------|---------|-------------|
| Method | `pbkdf2:sha256:600000` | The key derivation function, underlying hash, and iteration count. |
| Salt | `abcdefgh` | The 8-character random salt (base64 encoded). |
| Hash | `hashedvalue` | The actual derived key (also base64 encoded). |

When verifying, `check_password_hash` splits this string, re-applies the same parameters to the input password, and compares.

---

### 5. Testing the Implementation

1. **Run the Flask application.**
2. **Register a new user** with any name, email, and password.
3. **Inspect the database** using DB Browser for SQLite. You should see a row in the `users` table where the `password` column contains a long string starting with `pbkdf2:sha256:600000$...`. The plaintext password is **not** stored.
4. **Log in** with the same email and password. You should be redirected to the secrets page and see the greeting with your name.
5. **Test incorrect passwords:** Try logging in with a wrong password. You should see the "Incorrect password" message.
6. **Test non-existent email:** Try logging in with an email that wasn't registered. You should see the "Email not found" message.

---

### 6. Important Considerations

#### 6.1 Salt Length
The lesson specifies `salt_length=8` to match the instructions. In a real application, **use the default of 16** (or higher) for stronger security. A longer salt increases the randomness and makes precomputed attacks even more infeasible.

#### 6.2 Method Selection
`pbkdf2:sha256` with 600,000 iterations is secure for many applications. However, if your application handles highly sensitive data, consider using `scrypt` (the default in newer Werkzeug versions) or migrating to `bcrypt`/`Argon2` via dedicated libraries.

#### 6.3 Migration of Existing Hashes
If you later decide to increase the iteration count or change the algorithm, you can implement a gradual migration. During login, when a user successfully authenticates with an old hash, you can re-hash their password using the new method and update the database record.

#### 6.4 Error Handling
The code above uses simple string responses for errors. In a later lesson, you will replace these with **flash messages** to provide a better user experience.

#### 6.5 Session Management
Currently, after successful login, the user is redirected to `/secrets?name=...`, but the application does not "remember" that they are logged in. That will be handled when you integrate **Flask-Login** in the next lesson.

---

### 7. Common Mistakes to Avoid

| Mistake | Consequence | Correct Approach |
|---------|-------------|------------------|
| Storing plaintext passwords | Immediate compromise if database leaked | Always hash with `generate_password_hash`. |
| Using a fast hash (e.g., MD5, SHA-1) | Easy brute-force cracking | Use PBKDF2, bcrypt, or scrypt with sufficient iterations. |
| Hardcoding a single salt | Same password yields same hash for all users | Let `generate_password_hash` generate a unique salt each time. |
| Setting `salt_length` too low | Reduces randomness, aids precomputation | Use at least 16 bytes (default). |
| Forgetting to call `check_password_hash` | Cannot verify logins | Always use `check_password_hash` for verification. |

---

### 8. Summary

You have now replaced plaintext password storage with secure, salted hashing using Werkzeug's `generate_password_hash`. The registration route hashes the password before saving, and the login route verifies it using `check_password_hash`. This ensures that even if the database is compromised, the actual passwords remain protected.

**Key takeaways:**

- Passwords are hashed with `pbkdf2:sha256` and a unique 8-character salt (per lesson requirements).
- The salt is stored as part of the hash string, eliminating the need for a separate database column.
- Verification uses constant-time comparison to prevent timing attacks.

In the next lesson, you will integrate **Flask-Login** to manage user sessions, protect routes, and implement a proper login/logout flow. The groundwork laid here ensures that user credentials are stored securely before session management is added.