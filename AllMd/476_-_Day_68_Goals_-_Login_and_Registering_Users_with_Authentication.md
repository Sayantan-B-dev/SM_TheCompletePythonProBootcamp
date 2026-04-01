## Login and Registering Users with Authentication

### Introduction

Every interactive website relies on its users. Without users, a social media platform would be empty, a blog would be a solitary monologue, and an e‑commerce site would have no customers. To build a meaningful web application, you need to create a system that allows people to register, log in, and later return to their own personalized space. This is the essence of **authentication** – the process of verifying that a user is who they claim to be.

In this module, you will learn how to implement a complete authentication system using Flask. By the end, you will be able to:

- Allow new users to register by providing their name, email, and password.
- Securely store user passwords so that even if the database is compromised, the passwords remain protected.
- Let registered users log in with their email and password.
- Restrict access to certain pages (like a private profile) so that only authenticated users can view them.
- Provide a downloadable resource (a secret PDF cheat sheet) exclusively to logged‑in users.
- Give helpful feedback to users when something goes wrong (e.g., wrong password, email already taken).

This documentation will walk you through every concept and every line of code needed to build this system. You will understand not only *how* to write the code, but also *why* each step is necessary for security and usability.

---

### Why Authentication Matters

When a user registers on your site, they entrust you with personal information – typically their email address and a password. As a developer, you have a responsibility to protect that data. If an attacker gains access to your database, they should not be able to read the users’ passwords. This is achieved by **hashing** the passwords before storing them.

Authentication also answers the question: “Who is making this request?” Once you know who the user is, you can personalize their experience and, if needed, enforce **authorization** – deciding what that user is allowed to do (e.g., view their own profile, download a file, access an admin panel).

---

### What You Will Build

The final application will consist of several pages:

- A **home page** (`index.html`) with a simple welcome message and two buttons: **Login** and **Register**. When a user is already logged in, these buttons will be hidden and a small message “(you are already logged in)” will appear.
- A **registration page** (`register.html`) where a new user can enter their name, email, and password. Upon successful registration, they are automatically logged in and redirected to the secret page.
- A **login page** (`login.html`) where an existing user can enter their email and password. If correct, they are logged in and redirected to the secret page.
- A **secret page** (`secrets.html`) that is only accessible to authenticated users. It greets the user by name and contains a button to download a secret PDF file.
- A **logout** function that ends the user’s session and returns them to the home page.

All user data will be stored in an SQLite database (`users.db`) with a table that includes fields for the user’s name, email, and password. The password will never be stored in plain text; instead, we will store a secure hash.

---

### Key Concepts You Will Learn

#### 1. Hashing and Salting Passwords
- **Hashing** transforms a password into a fixed‑length string of characters that cannot be reversed. If an attacker obtains the hash, they cannot directly see the original password.
- **Salting** adds a unique random value to each password before hashing. This ensures that even if two users choose the same password, their stored hashes will be different. Salting also defeats precomputed attack tables (rainbow tables).
- You will use the **Werkzeug** library’s `generate_password_hash()` and `check_password_hash()` functions, which implement a strong, salted hash using the `pbkdf2:sha256` algorithm.

#### 2. User Sessions with Flask-Login
- After a user logs in, the server needs a way to remember that they are authenticated for subsequent requests. This is done with **sessions**.
- **Flask-Login** is an extension that manages user sessions, handles logging in and out, and provides a simple way to protect routes so that only logged‑in users can access them.
- You will learn how to integrate Flask‑Login with your Flask application, create a user class that inherits from `UserMixin`, and use the `@login_required` decorator to secure routes.

#### 3. Protecting Routes
- Certain pages (like the secret page and the download link) should be off‑limits to unauthenticated visitors. You will use Flask‑Login’s `login_required` decorator to automatically redirect anonymous users to the login page.

#### 4. Flash Messages
- To improve user experience, you will display temporary feedback messages when something goes wrong – for example, “Email already registered” or “Incorrect password”. Flask’s **flash messaging system** allows you to send one‑time messages from the server to the template.

#### 5. Template Inheritance and Conditional Rendering
- You will modify the base template (`base.html`) to conditionally show or hide the Login and Register links based on whether the current user is authenticated. This keeps the navigation clean and relevant.

---

### The Starting Project

Before you begin coding, you are provided with a starter project that includes:

- A basic Flask application with all the necessary HTML templates (home, login, register, secret).
- A pre‑created SQLite database (`users.db`) with a `users` table (initially empty).
- A PDF file (`cheat_sheet.pdf`) placed inside the `static/files/` directory that will be downloadable only to authenticated users.
- A `requirements.txt` file listing all the Python packages you will need: Flask, Flask‑Login, Werkzeug, etc.

The starting code already renders the pages correctly, but the login/register forms do nothing. Your task is to add the authentication logic step by step.

---

### Step‑by‑Step Roadmap

The lessons that follow will guide you through the implementation in a logical order:

1. **Register New Users** – Capture the form data from `register.html`, create a new user record, and save it to the database. For now, you will store the password as plain text (temporarily) so you can see it working.
2. **Downloading Files** – Add a route `/download` that uses `send_from_directory()` to serve the secret PDF, but only after the user is authenticated (you will later protect this route).
3. **Encryption and Hashing** – Understand the difference between encryption and hashing, and why hashing is the correct choice for passwords.
4. **How to Hack Passwords 101** – Learn about common attack vectors (brute force, dictionary attacks, rainbow tables) and how proper hashing and salting mitigate them.
5. **Salting Passwords** – Dive deep into what a salt is, how it is generated, and how it is stored alongside the hash.
6. **Hashing and Salting with Werkzeug** – Replace the plain‑text password storage with `generate_password_hash()` and adapt the registration and login logic to use it.
7. **Authenticating Users with Flask‑Login** – Install and configure Flask‑Login, create a user loader, protect the secret and download routes, and implement the login and logout functionality.
8. **Flask Flash Messages** – Add informative flash messages to guide the user when registration or login fails.
9. **Passing Authentication Status to Templates** – Modify the templates to hide login/register buttons for authenticated users and show a welcome message instead.

Each step builds on the previous one, and by the end you will have a fully functional, secure authentication system.

---

### Why This Matters for Your Future Projects

Authentication is a fundamental building block of almost every web application. Whether you are building a social network, an e‑commerce site, or a simple blog, you will need to manage users. The skills you learn here – secure password storage, session management, route protection – will be directly applicable to any Flask project you undertake. Moreover, understanding *why* certain practices (like hashing, salting, and using extensions like Flask‑Login) are essential will make you a more security‑conscious developer.

