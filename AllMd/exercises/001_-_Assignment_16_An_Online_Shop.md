# Complete Documentation for Art Ecom (Flask E-commerce)

This document provides a comprehensive, file-oriented, structured documentation for the Art Ecom project. It covers installation, environment setup, folder structure, detailed algorithmic explanations of every file and function, data flow, integrations (Razorpay, SQLite Cloud, cart, models, Jinja), and ends with 10 interview questions and answers.

---

![](./preview.gif)

---

## 1. Getting Started

### 1.1 Installation
1. Clone the repository.
2. Create a virtual environment and activate it.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 1.2 Environment Variables
Create a `.env` file in the project root with the following variables:
```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin
SQLITECLOUD_CONNECTION_STRING=your-sqlitecloud-connection-string
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret
```
- `SQLITECLOUD_CONNECTION_STRING`: Connection string for SQLite Cloud (e.g., `sqlitecloud://username:password@host:port/database`).
- Razorpay keys obtained from Razorpay dashboard.

### 1.3 Run the Application
```bash
python run.py
```
The app will start in debug mode at `http://localhost:5000`.

---

## 2. Folder Structure with Comments

```
.
├── .env                         # Environment variables (not in repo)
├── .gitignore                   # Git ignore file
├── all_source_files.txt         # Concatenated source (for reference)
├── app/                         # Main application package
│   ├── __init__.py              # Flask app factory, blueprint registration, error handlers
│   ├── decorators.py            # Custom decorators (e.g., admin_required)
│   ├── extensions.py            # Flask extensions initialization (LoginManager, JWTManager)
│   ├── forms.py                 # WTForms for login, registration, product management
│   ├── models.py                # Database models and helper functions (get_db, init_db, User, Product, Cart, Order)
│   ├── routes/                  # Blueprints for different parts of the app
│   │   ├── admin.py             # Admin dashboard route
│   │   ├── auth.py              # Authentication routes (login, register, logout, profile)
│   │   ├── cart.py              # Cart management routes (view, add, update, remove, count)
│   │   ├── main.py              # Home page route
│   │   ├── payment.py           # Checkout and payment processing with Razorpay
│   │   ├── product.py           # Product detail and admin CRUD routes
│   ├── services/                # Placeholder for service modules (currently empty)
│   │   ├── __init__.py
│   │   ├── payment_service.py   # (Empty, can be used for payment logic separation)
│   ├── static/                   # Static assets (CSS, JS, images)
│   │   ├── css/
│   │   │   └── style.css        # Custom CSS with glassmorphism effects
│   │   ├── images/               # (Empty, for product images)
│   │   └── js/
│   │       └── main.js           # Custom JS (minimal, cart count update handled inline)
│   ├── templates/                # Jinja2 HTML templates
│   │   ├── admin/
│   │   │   └── dashboard.html    # Admin dashboard listing products
│   │   ├── auth/
│   │   │   ├── login.html        # Login form
│   │   │   ├── profile.html      # User profile with order history
│   │   │   └── register.html     # Registration form
│   │   ├── cart/
│   │   │   ├── cart.html         # Shopping cart view
│   │   │   └── checkout.html     # Checkout page with Razorpay integration
│   │   ├── errors/
│   │   │   ├── 403.html          # Forbidden error page
│   │   │   ├── 404.html          # Not found error page
│   │   │   └── 500.html          # Internal server error page
│   │   ├── base.html              # Base template with navigation, flashes, footer
│   │   ├── index.html             # Home page listing products
│   │   └── product/
│   │       ├── admin_add.html     # Add product form (admin only)
│   │       ├── admin_edit.html    # Edit product form (admin only)
│   │       └── detail.html        # Product detail page
│   ├── utils.py                   # Utility functions (generate_session_id)
├── config.py                       # Configuration class loading from .env
├── requirements.txt                # Python dependencies
├── run.py                          # Entry point to run the app
└── __pycache__/                    # Compiled Python files (ignored)
```

---

## 3. Detailed File-by-File Explanation

### 3.1 `config.py`
**Purpose**: Load configuration from environment variables using python-dotenv. Provides a `Config` class with attributes used throughout the app.

**Algorithmic Steps**:
1. Load `.env` file.
2. Define `Config` class with:
   - `SECRET_KEY`: Flask secret key.
   - `JWT_SECRET_KEY`: Secret for JWT (though not heavily used).
   - `ADMIN_EMAIL`, `ADMIN_PASSWORD`: Default admin credentials.
   - `SQLITECLOUD_CONNECTION_STRING`: Connection string for SQLite Cloud.
   - `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`: Razorpay API keys.

### 3.2 `run.py`
**Purpose**: Entry point to run the Flask development server.

**Algorithmic Steps**:
1. Import `create_app` from `app`.
2. Create app instance.
3. Run app with `debug=True` if executed directly.

### 3.3 `app/__init__.py`
**Purpose**: Flask application factory. Creates and configures the app, registers blueprints, sets up login manager, JWT, error handlers, and initializes the database (including admin user creation).

**Algorithmic Steps**:
1. Create Flask app with `__name__`.
2. Load config from `config.Config`.
3. Initialize extensions: `login_manager.init_app(app)`, `jwt.init_app(app)`.
4. Import and register blueprints: `auth_bp`, `main_bp`, `product_bp`, `cart_bp`, `payment_bp`, `admin_bp`.
5. Define `@login_manager.user_loader` to load user by ID using `User.get(user_id)`.
6. Set `app.teardown_appcontext(close_db)` to close database connection after each request.
7. Inside app context:
   - Call `init_db()` to create tables if not exist.
   - Check if admin user exists; if not, create using `User.create(admin_email, admin_pass, is_admin=True)`.
8. Register error handlers for 404, 500, 403 that render custom templates.
9. Return app.

**Data Flow**:
- App creation → config loaded → extensions init → blueprints registered → teardown setup → DB init → admin creation → error handlers → ready.

### 3.4 `app/extensions.py`
**Purpose**: Centralize Flask extension objects to avoid circular imports.

**Algorithmic Steps**:
- Instantiate `LoginManager` and `JWTManager`. They are imported elsewhere and initialized in `__init__.py`.

### 3.5 `app/decorators.py`
**Purpose**: Custom decorators for route protection.

**Algorithmic Steps**:
- `admin_required(f)`: Wraps a route function. Checks if `current_user.is_authenticated` and `current_user.is_admin`. If not, aborts with 403. Otherwise calls the original function.

### 3.6 `app/forms.py`
**Purpose**: WTForms classes for user input validation.

**Algorithmic Steps**:
- `LoginForm`: Fields: email (validators: DataRequired, Email), password (DataRequired), submit.
- `RegistrationForm`: Fields: email, password (Length(min=6)), confirm_password (EqualTo('password')), submit.
- `ProductForm`: Fields: name, description, price (Float), stock (Integer), image_url, submit.

### 3.7 `app/models.py`
**Purpose**: Database connection management, table initialization, and model classes (User, Product, Cart, Order). Uses SQLite Cloud.

#### Functions:
- `get_db()`:
  1. Check if `'db'` is in Flask `g` object.
  2. If not, connect using `sqlitecloud.connect` with connection string from app config.
  3. Enable foreign keys with `PRAGMA foreign_keys = ON;`.
  4. Store connection in `g.db` and return it.
- `close_db(e=None)`:
  1. Pop `'db'` from `g`.
  2. If exists, close the connection.
- `init_db()`:
  1. Get DB connection.
  2. Execute CREATE TABLE IF NOT EXISTS for: users, products, carts, cart_items, orders, order_items.
  3. Commit changes.

#### Class `User` (inherits UserMixin):
- `__init__(id, email, is_admin, created_at)`: Set attributes.
- `get(user_id)`: Static method. Query user by id, return User object or None.
- `get_by_email(email)`: Static method. Query user by email, return User object or None.
- `create(email, password, is_admin)`: Static method.
  1. Hash password with `generate_password_hash`.
  2. Insert into users table.
  3. Commit and return lastrowid, or None if IntegrityError (duplicate email).
- `check_password(password)`: Instance method. Query password_hash for this user, verify with `check_password_hash`.

#### Class `Product` (static methods):
- `create(name, description, price, stock, image_url)`: Insert product, commit, return lastrowid.
- `get_all()`: Select all products ordered by created_at DESC, return list of dicts (using cursor.description for column names).
- `get_by_id(product_id)`: Select one product by id, return dict or None.
- `update_stock(product_id, quantity)`: Decrease stock by quantity only if stock >= quantity. Return boolean success.
- `update(product_id, name, description, price, stock, image_url)`: Update product fields, commit, return boolean.
- `delete(product_id)`: Delete product, commit, return boolean.

#### Class `Cart` (static methods):
- `get_or_create_cart(user_id=None, session_id=None)`:
  - If user_id: try to find cart by user_id; if exists return id, else create new cart with user_id and return id.
  - If session_id: similar for guest session.
- `merge_carts(user_id, session_id)`:
  1. Get guest cart by session_id.
  2. Get or create user cart.
  3. Move all items from guest cart to user cart (if product already exists, sum quantities; else insert).
  4. Delete guest cart.
  5. Commit.
- `add_item(cart_id, product_id, quantity=1)`:
  1. Check product exists and has enough stock.
  2. If item already in cart, check new total quantity <= stock, then update.
  3. Else insert new cart item.
  4. Commit; return True if successful, False if stock insufficient.
- `remove_item(cart_id, product_id)`: Delete cart_item.
- `update_item_quantity(cart_id, product_id, quantity)`:
  1. If quantity <= 0, remove item.
  2. Else check stock sufficiency and update quantity.
  3. Commit; return True/False.
- `get_cart_items(cart_id)`:
  1. Join cart_items with products to fetch details.
  2. Iterate rows, compute subtotal and total.
  3. Return list of item dicts and total amount.

#### Class `Order` (static methods):
- `get_by_user(user_id)`:
  1. Select orders and order_items with product names for given user.
  2. Build dictionary of orders with nested items list.
  3. Return list of order dicts.

### 3.8 `app/utils.py`
**Purpose**: Utility functions.

- `generate_session_id()`: Return a new UUID4 string for guest session identification.

### 3.9 `app/routes/main.py`
**Purpose**: Home page.

- `index()`: Get all products via `Product.get_all()`, render `index.html` with products.

### 3.10 `app/routes/auth.py`
**Purpose**: Authentication and user profile.

#### `set_session_id()` (before_app_request):
- If user not authenticated and no session_id in session, set `session['session_id'] = generate_session_id()`.

#### `login()` (GET/POST):
- If user already authenticated, redirect to home.
- Instantiate `LoginForm`.
- If POST and valid:
  - Get user by email.
  - If user exists and password matches:
    - `login_user(user)`.
    - If session_id exists (guest cart), call `Cart.merge_carts(user.id, session_id)` and pop session_id.
    - Redirect to next page or home.
  - Else flash error.
- Render `login.html` with form.

#### `register()` (GET/POST):
- Similar to login: check authenticated, instantiate `RegistrationForm`.
- If POST and valid:
  - Check if email already exists; if yes, flash error.
  - Create user with `User.create(...)`.
  - If success, log user in, flash success, redirect home.
- Render `register.html`.

#### `logout()`:
- `logout_user()`, flash info, redirect home.

#### `profile()` (login_required):
- Get orders for current user via `Order.get_by_user(current_user.id)`.
- Render `profile.html` with orders.

**Data Flow**:
- Guest visits site → `set_session_id` creates session_id.
- Guest adds items to cart → cart associated with session_id.
- Guest registers/logs in → `merge_carts` combines guest cart with user cart.
- User logs out → session cleared but user cart persists.

### 3.11 `app/routes/cart.py`
**Purpose**: Cart operations.

#### `get_current_cart_id()`:
- If user authenticated: get or create cart using `user_id`.
- Else: ensure session_id exists, get or create cart using `session_id`.
- Returns cart_id.

#### `view_cart()`:
- Get cart_id, items, total via `Cart.get_cart_items(cart_id)`.
- Render `cart.html` with items and total.

#### `add_to_cart(product_id)` (POST):
- Get cart_id, quantity from form.
- Call `Cart.add_item(cart_id, product_id, quantity)`.
- Flash success/error and redirect back or to product detail.

#### `update_cart(product_id)` (POST):
- Get cart_id, new quantity.
- Call `Cart.update_item_quantity(cart_id, product_id, quantity)`.
- Flash and redirect to cart view.

#### `remove_from_cart(product_id)` (POST):
- Get cart_id, call `Cart.remove_item(cart_id, product_id)`.
- Flash and redirect to cart.

#### `cart_count()` (GET):
- Get cart_id, items, total.
- Compute sum of quantities, return JSON `{'count': count}`.

**Data Flow**:
- User action → route → get cart_id → model method → DB update → redirect/JSON.

### 3.12 `app/routes/product.py`
**Purpose**: Product display and admin CRUD.

#### `detail(product_id)`:
- Get product by id; if None, abort 404.
- Render `product/detail.html` with product.

#### `admin_add()` (GET/POST, admin_required):
- Instantiate `ProductForm`.
- If POST and valid: create product with form data, flash success, redirect to product detail.
- Render `admin_add.html` with form.

#### `admin_edit(product_id)` (GET/POST, admin_required):
- Get product; if None, abort 404.
- Instantiate `ProductForm`.
- If GET: pre-populate form with product data.
- If POST and valid: update product, flash success/error, redirect to product detail.
- Render `admin_edit.html` with form and product.

#### `admin_delete(product_id)` (POST, admin_required):
- Get product; if None, abort 404.
- Call `Product.delete(product_id)`, flash result, redirect to home.

**Data Flow**:
- Admin requests add/edit → form rendered → POST → model update → redirect.

### 3.13 `app/routes/payment.py`
**Purpose**: Checkout and payment processing with Razorpay.

#### `checkout()` (login_required):
- Get cart_id, items, total via `Cart.get_cart_items`.
- If cart empty, flash and redirect to cart.
- Check stock for each item: if insufficient, flash and redirect.
- Initialize Razorpay client with key and secret.
- Create Razorpay order:
  - amount = total * 100 (paise), currency INR, receipt = cart_id.
- Insert order record into DB with status 'pending' and razorpay_order_id.
- Store `current_order_id` in session.
- Render `checkout.html` with order details, items, total, and Razorpay key ID.

#### `payment_success()` (POST, login_required):
- Get Razorpay callback params: razorpay_order_id, razorpay_payment_id, razorpay_signature.
- Verify signature using `client.utility.verify_payment_signature`.
- If valid:
  - Get order_id from session.
  - Update order status to 'paid'.
  - Insert order_items from cart items.
  - Reduce stock for each product using `Product.update_stock`.
  - Clear cart (delete cart_items).
  - Commit, flash success, remove session variable, redirect home.
- If verification fails or exception: flash error, log, redirect to cart.

**Data Flow**:
- User clicks checkout → stock check → Razorpay order created → DB pending order → Razorpay checkout.js opens.
- User pays → Razorpay POST to `/payment/success` → verify signature → update order, move items, clear cart → redirect.

### 3.14 `app/routes/admin.py`
**Purpose**: Admin dashboard.

#### `dashboard()` (admin_required):
- Get all products via `Product.get_all()`.
- Render `admin/dashboard.html` with products.

### 3.15 Templates (Jinja2)
**Purpose**: Render HTML with dynamic data. Extends `base.html` which contains common layout, navigation, flash messages, and footer.

**Key Features**:
- `base.html` includes a script that fetches `/cart/count` to update cart count dynamically.
- Flash messages displayed with categories (error, success, info) for styling.
- Forms use WTForms rendering with custom CSS classes.
- Razorpay checkout.js integrated in `checkout.html` with JavaScript to handle payment modal and form submission.

**Data Flow**:
- Route passes context (e.g., products, form) → template renders → user sees page.
- JavaScript updates cart count via fetch.

### 3.16 Static Files
- `style.css`: Custom glassmorphism styles, animations, input styling.
- `main.js`: Empty placeholder; cart count update is inline in base.html.

---

## 4. Key Integrations Explained

### 4.1 Razorpay Payment Gateway
- **Usage**: For processing payments.
- **Flow**:
  1. In `/checkout`, server creates an order via Razorpay API using `razorpay.Client.order.create()`.
  2. Order details (id, amount) are passed to the template.
  3. Frontend uses Razorpay checkout.js to open a payment modal with order_id and key.
  4. After payment, Razorpay POSTs to `/payment/success` with payment details.
  5. Server verifies signature using `client.utility.verify_payment_signature()`.
  6. On success, order status updated, cart items moved to order_items, stock reduced, cart cleared.

### 4.2 SQLite Cloud
- **Usage**: Cloud-hosted SQLite database.
- **How it works**:
  - Connection string in `.env` points to a remote SQLite Cloud instance.
  - `sqlitecloud.connect()` establishes connection.
  - All SQL operations (CREATE, INSERT, SELECT, UPDATE, DELETE) are executed on the remote database.
  - The connection is stored in Flask's `g` object per request and closed after each request via `close_db`.

### 4.3 Cart System
- **Two types**: Authenticated user cart (linked to `user_id`) and guest cart (linked to `session_id`).
- **Merging**: When a guest logs in, their cart items are merged into the user's cart using `Cart.merge_carts()`.
- **Cart operations**: Add, update quantity, remove, view. Stock validation occurs on add and update.
- **Cart count**: Fetched via AJAX in base.html to display updated count.

### 4.4 Models and Database
- Models are static methods (no SQLAlchemy ORM). Raw SQL executed via sqlitecloud connection.
- `Product.get_all()` returns list of dicts using cursor.description for dynamic column names.
- `Order.get_by_user()` uses a LEFT JOIN to fetch orders with their items in one query, then builds nested structure.

### 4.5 Jinja2 Templating
- **Template Inheritance**: All pages extend `base.html`.
- **Blocks**: `title`, `content`, `scripts` for page-specific content and JS.
- **Flashing**: `get_flashed_messages(with_categories=true)` used to display notifications.
- **Forms**: WTForms rendered with `form.hidden_tag()` and field methods; custom CSS classes added.
- **Dynamic Cart Count**: Inline script fetches `/cart/count` on every page load and updates the span.

---

## 5. Data Flow Overview

```
User Request (e.g., GET /) 
  → main.index() 
    → Product.get_all() 
      → get_db() -> execute SELECT -> return list of dicts 
    → render_template('index.html', products=products) 
      → base.html layout + index content 
      → HTML response

User adds to cart (POST /cart/add/1) 
  → cart.add_to_cart(1) 
    → get_current_cart_id() 
      → if authenticated: Cart.get_or_create_cart(user_id) 
      → else: ensure session_id, Cart.get_or_create_cart(session_id) 
    → Cart.add_item(cart_id, 1, quantity) 
      → check stock, insert/update cart_items 
    → flash -> redirect back

Guest logs in (POST /login) 
  → auth.login() 
    → User.get_by_email() and check_password 
    → login_user(user) 
    → if session_id in session: Cart.merge_carts(user.id, session_id) 
      → move items from guest cart to user cart, delete guest cart 
    → redirect to home

User checks out (GET /checkout) 
  → payment.checkout() 
    → get cart items, check stock 
    → create Razorpay order 
    → insert orders record (pending) 
    → store order_id in session 
    → render checkout.html with Razorpay key and order data

User pays (Razorpay modal) 
  → POST /payment/success with payment details 
    → payment.payment_success() 
      → verify signature 
      → update order status to paid 
      → insert order_items from cart 
      → reduce stock for each product 
      → clear cart 
      → flash success -> redirect home
```

---

## 6. Interview Questions and Answers

### Q1: How does the cart system handle guest users versus logged-in users?
**Answer**:  
The cart system uses two identifiers: `user_id` for authenticated users and `session_id` for guests. When a guest first visits, a unique session ID is generated and stored in the session cookie. All cart operations for guests use this session ID to retrieve or create a cart in the `carts` table. When a guest logs in, `Cart.merge_carts()` moves all items from the guest cart to the user's cart (combining quantities if the same product) and deletes the guest cart. This ensures no items are lost during login.

### Q2: Explain how stock validation is performed when adding items to the cart.
**Answer**:  
In `Cart.add_item()`, we first fetch the product by ID using `Product.get_by_id()`. We check if the product exists and if its current stock is at least the requested quantity. If the item is already in the cart, we calculate the new total quantity (existing + new) and ensure it does not exceed stock. Only then do we insert or update the cart item. This prevents overselling. Similar checks are done in `update_item_quantity()`.

### Q3: How does the application ensure database connections are properly closed?
**Answer**:  
The `get_db()` function stores the database connection in Flask's `g` object, which is unique per request. The `close_db()` function is registered with `app.teardown_appcontext`, so it is automatically called after each request (even if an exception occurs). It pops the connection from `g` and closes it, preventing connection leaks.

### Q4: Describe the flow of a successful payment using Razorpay.
**Answer**:  
1. User clicks "Checkout" → server creates a Razorpay order via API and stores a pending order in DB with `razorpay_order_id`.  
2. The checkout page loads with Razorpay checkout.js, passing the order ID and key.  
3. User completes payment in Razorpay modal → Razorpay sends a POST request to `/payment/success` with payment ID, order ID, and signature.  
4. Server verifies the signature using Razorpay's utility. If valid, it updates the order status to "paid", moves cart items to `order_items`, reduces stock, and clears the cart.  
5. User is redirected to home with a success message.

### Q5: What is the purpose of the `admin_required` decorator and how is it implemented?
**Answer**:  
The `admin_required` decorator protects routes that should only be accessible to admin users. It wraps a view function and checks if the current user is authenticated and has the `is_admin` flag set to True. If not, it aborts with a 403 Forbidden error. It uses `functools.wraps` to preserve the original function's metadata.

### Q6: How does the application merge guest and user carts after login? Walk through the SQL operations.
**Answer**:  
`Cart.merge_carts(user_id, session_id)` does:
1. Get guest cart ID from `carts` where `session_id = ?`.
2. Get or create user cart ID via `get_or_create_cart(user_id)`.
3. For each item in guest cart:
   - Check if user cart already has that product: if yes, update quantity = existing + guest quantity; if no, insert new row.
4. Delete the guest cart row (cascade deletes its items due to foreign key).
5. Commit transaction.

### Q7: Explain the use of `g` object in Flask for database connections.
**Answer**:  
`g` is a Flask global object that is unique to each request. It is used to store resources that need to be reused during a request, such as a database connection. By storing the connection in `g`, we avoid opening multiple connections per request. The connection is opened once when `get_db()` is first called, and closed automatically at the end of the request via `teardown_appcontext`.

### Q8: How does the application handle form validation and CSRF protection?
**Answer**:  
Flask-WTF is used, which integrates WTForms with CSRF protection. Each form includes `form.hidden_tag()` in the template, which renders a hidden CSRF token field. On form submission, Flask-WTF automatically validates the token. If validation fails, the form is not considered valid. Field validators (e.g., DataRequired, Email) are also checked.

### Q9: What would happen if two users try to purchase the last item simultaneously? How does the app prevent overselling?
**Answer**:  
The app uses stock checks at critical points: when adding to cart and during checkout. However, there is a race condition possibility if both users have the item in cart and proceed to checkout at the same time. The checkout route checks stock again before creating the Razorpay order. During payment success, `Product.update_stock()` uses `UPDATE products SET stock = stock - ? WHERE id = ? AND stock >= ?`, which is atomic in SQLite. Only one will succeed if stock is exactly one; the other's update will affect zero rows, and `db.total_changes` will be 0, allowing us to detect failure. However, the current code does not handle this race condition after payment; it assumes the stock check at checkout is sufficient. To fully prevent, we would need to use row-level locking or a transaction with `SELECT ... FOR UPDATE` (not supported in SQLite by default). But SQLite's default transaction behavior with `BEGIN IMMEDIATE` can help.

### Q10: How does Jinja2 help in rendering dynamic content, and how is data passed from routes to templates?
**Answer**:  
Jinja2 is a templating engine that allows embedding Python-like expressions in HTML. Routes pass data as keyword arguments to `render_template()`, e.g., `render_template('index.html', products=products)`. Inside the template, we use `{{ products }}` to output variables and `{% for product in products %}` for loops. Template inheritance (`{% extends "base.html" %}`) allows reusing common layout. Blocks like `{% block content %}` are overridden in child templates. Jinja also supports filters, macros, and includes.

### 11. How does the application prevent SQL injection attacks?
**Answer**:  
All database queries use parameterized SQL with placeholders (`?`). For example, in `Product.get_by_id(product_id)`, the query is `SELECT * FROM products WHERE id = ?`, and the `product_id` is passed as a tuple parameter to `db.execute()`. This ensures that user-supplied input is never directly concatenated into SQL strings, preventing SQL injection. The `sqlitecloud` module properly handles parameterized queries, escaping values as needed.

### 12. Explain how Flask-Login manages user sessions. What is stored in the session cookie?
**Answer**:  
Flask-Login uses the Flask session (which is a signed cookie) to store the user ID. When a user logs in, `login_user(user)` writes the user’s ID into the session. On subsequent requests, the `user_loader` function (defined in `__init__.py`) retrieves that ID and loads the user object from the database. The session cookie is signed with the app’s `SECRET_KEY` to prevent tampering. No sensitive data (like passwords) is stored in the cookie; only the user identifier.

### 13. Why is Flask-JWT-Extended included even though JWT tokens are not used for API authentication?
**Answer**:  
The inclusion appears to be for potential future expansion or because the developer originally planned to use JWT for API endpoints. Currently, the application relies on Flask-Login for session-based authentication, which is suitable for a traditional web app with server-rendered templates. JWT could be used later if the app exposes a REST API for mobile clients, but in the current code, it is initialized but not actively used.

### 14. Describe how the cart count is updated dynamically without refreshing the page.
**Answer**:  
In `base.html`, there is an inline script that executes immediately when the page loads. It uses the Fetch API to make a GET request to the `/cart/count` endpoint. This endpoint (`cart.cart_count`) returns a JSON object `{'count': total_quantity}`. The script then updates the text content of the `<span id="cart-count">` element with the returned count. This happens on every page load, ensuring the cart count is always up‑to‑date.

### 15. What would happen if a user closes their browser immediately after completing a payment on Razorpay but before the success callback executes?
**Answer**:  
If the user closes the browser right after payment but before the frontend sends the POST request to `/payment/success`, the payment will be captured by Razorpay (money deducted) but the order in our database will remain in "pending" state, and the cart won’t be cleared. To handle this, the application could implement a webhook on the Razorpay side that notifies the server of successful payments even if the user drops off. The webhook would update the order status and complete the transaction. Without a webhook, an administrator would need to manually reconcile pending orders.

### 16. How could you add product categories or search functionality to this app?
**Answer**:  
- **Categories**: Add a `category_id` foreign key to the `products` table and create a `categories` table. Update the `Product` model with methods to filter by category. Modify the product form to include a category dropdown. In the templates, add navigation links to browse by category.
- **Search**: Implement a search form that sends a query string to a new route (e.g., `/search`). Use SQL `LIKE` or `FULLTEXT` search (if using SQLite with FTS5) to match product names and descriptions. Pass the results to a template for display.

### 17. What are the main performance bottlenecks in this application, and how could you address them?
**Answer**:  
- **Database queries**: Each page load may execute multiple queries (e.g., fetching products, cart count). Using SQLite Cloud over the network adds latency. Mitigation: add caching (e.g., Flask-Caching) for product lists, or use connection pooling.
- **Concurrent stock updates**: Without proper locking, simultaneous checkouts could oversell. Use database transactions with `BEGIN IMMEDIATE` and retry logic, or implement optimistic locking.
- **Razorpay API calls**: Creating an order involves an external HTTP request. If the Razorpay API is slow, it delays checkout. Mitigation: offload to background tasks (Celery) but that complicates the flow.

### 18. How does the application ensure that only admin users can access the admin routes?
**Answer**:  
The `admin_required` decorator is applied to all admin routes (e.g., `/admin`, `/admin/product/add`). This decorator checks `current_user.is_authenticated` and `current_user.is_admin`. If the user is not an admin, it calls `abort(403)`, which triggers the 403 error handler and renders a "Forbidden" page. Additionally, the admin-only links (like "Add Product") are conditionally shown in the navigation only when `current_user.is_admin` is true, preventing non‑admins from seeing them.

### 19. How would you implement a "forgot password" feature?
**Answer**:  
1. Add a "Forgot Password?" link on the login page that leads to a form requesting the user's email.
2. When submitted, check if the email exists. If yes, generate a secure, time‑limited token (e.g., using `itsdangerous`) and store it (or its hash) in the database with an expiry.
3. Send an email to the user containing a link with the token (e.g., `/reset-password/<token>`).
4. The reset page validates the token and presents a form for new password.
5. Upon submission, update the user’s password hash and delete/expire the token.
This requires integrating an email sending service (like SMTP or SendGrid).

### 20. What are the advantages of using blueprints in this Flask application?
**Answer**:  
Blueprints allow modular organization of routes and templates. Each blueprint (`auth_bp`, `product_bp`, etc.) groups related functionality, making the codebase easier to navigate and maintain. They also enable features like:
- Prefixing routes (e.g., all admin routes could be under `/admin`).
- Isolating templates in blueprint‑specific folders (though here all templates share the same folder).
- Reusing blueprints in different projects or mounting them at different URL prefixes.
- Better separation of concerns, which simplifies testing and collaboration.