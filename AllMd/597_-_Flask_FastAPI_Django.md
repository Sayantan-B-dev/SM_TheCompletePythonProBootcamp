# Comprehensive Comparison: Flask vs FastAPI vs Django

This document provides a detailed, feature-by-feature comparison of three popular Python web frameworks: **Flask**, **FastAPI**, and **Django**. It is designed as a study guide, explaining concepts and showing tiny code examples with extensive comments. Whether you're choosing a framework for a new project or deepening your understanding, this guide will help you see the strengths and trade-offs of each.

---

## 1. Introduction

| Framework | Description |
|-----------|-------------|
| **Flask** | A microframework that provides the essentials to build web applications. It is lightweight, flexible, and relies on extensions to add functionality. |
| **FastAPI** | A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. It is built on Starlette and Pydantic. |
| **Django** | A high-level, "batteries-included" framework that encourages rapid development and clean, pragmatic design. It comes with an ORM, admin panel, authentication, and more out of the box. |

---

## 2. Core Philosophy

| Framework | Philosophy |
|-----------|------------|
| **Flask** | "Micro" does not mean your entire application has to fit into a single file, but it means Flask aims to keep the core simple but extensible. You choose what components you need (database, forms, etc.) via extensions. |
| **FastAPI** | Designed for building APIs quickly with automatic interactive documentation, based on OpenAPI. It leverages Python type hints for request validation, serialization, and dependency injection. |
| **Django** | "The framework for perfectionists with deadlines." It includes everything you need to build a full-featured web application: ORM, authentication, admin interface, etc. Follows the "Don't Repeat Yourself" (DRY) principle. |

---

## 3. Project Structure

### Flask

Flask does not enforce any project structure. A minimal app can be a single file. Larger projects often use packages.

```python
# app.py (single file example)
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run()
```

A typical larger Flask project:

```
myflaskapp/
├── app/
│   ├── __init__.py          # creates Flask app, registers blueprints
│   ├── routes/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── models.py
│   ├── templates/
│   └── static/
├── config.py
├── requirements.txt
└── run.py
```

### FastAPI

FastAPI also doesn't enforce structure, but encourages modular organization with APIRouter.

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello FastAPI"}
```

Typical larger FastAPI project:

```
myfastapiapp/
├── app/
│   ├── __init__.py
│   ├── main.py               # creates FastAPI app, includes routers
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── items.py
│   │   │   │   └── users.py
│   │   │   └── __init__.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── models/
│   │   └── item.py           # Pydantic models / SQLAlchemy models
│   ├── crud/
│   │   └── item.py
│   └── db/
│       ├── base.py
│       └── session.py
├── requirements.txt
└── .env
```

### Django

Django has a very structured approach. Each project contains multiple apps.

```bash
django-admin startproject myproject
cd myproject
python manage.py startapp blog
```

Generated structure:

```
myproject/
├── manage.py
├── myproject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── blog/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── migrations/
    ├── models.py
    ├── tests.py
    └── views.py
```

---

## 4. Routing

### Flask

Use the `@app.route` decorator to bind a function to a URL.

```python
from flask import Flask

app = Flask(__name__)

# Basic route
@app.route('/')
def index():
    """Route for the home page."""
    return 'Home Page'

# Route with variable
@app.route('/user/<username>')
def show_user(username):
    """Dynamic URL capturing a string variable."""
    return f'User: {username}'

# Route with variable type
@app.route('/post/<int:post_id>')
def show_post(post_id):
    """Variable with int converter."""
    return f'Post ID: {post_id}'

# Multiple routes for same function
@app.route('/about')
@app.route('/about/')
def about():
    """Function accessible at /about and /about/."""
    return 'About page'

# HTTP methods
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle both GET and POST requests."""
    if request.method == 'POST':
        return "Logging in..."
    return "Login form"

# Blueprints for modular routing (not shown here)
```

### FastAPI

Upexpectedly simple: use decorators with path operations.

```python
from fastapi import FastAPI

app = FastAPI()

# Basic route (async optional)
@app.get("/")
async def root():
    """Async route for home."""
    return {"message": "Hello World"}

# Path parameter (type annotated)
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    """Item ID is automatically converted to int."""
    return {"item_id": item_id}

# Query parameters (function parameters not in path)
@app.get("/items/")
async def list_items(skip: int = 0, limit: int = 10):
    """Query parameters: /items/?skip=0&limit=10."""
    return {"skip": skip, "limit": limit}

# Mix path and query
@app.get("/users/{user_id}/items")
async def get_user_items(user_id: int, skip: int = 0, limit: int = 10):
    """Path parameter + query parameters."""
    return {"user_id": user_id, "skip": skip, "limit": limit}

# Multiple HTTP methods
@app.post("/items/")
async def create_item():
    """POST endpoint."""
    return {"message": "Item created"}

@app.put("/items/{item_id}")
@app.patch("/items/{item_id}")
async def update_item(item_id: int):
    """Both PUT and PATCH handled by same function."""
    return {"item_id": item_id}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """DELETE endpoint."""
    return {"message": f"Item {item_id} deleted"}
```

### Django

Django uses URL patterns defined in `urls.py` that map to view functions or classes.

```python
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),  # include app-specific URLs
]

# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Basic route
    path('', views.index, name='index'),
    
    # Path parameter (converter: int)
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    
    # Path parameter with slug
    path('article/<slug:article_slug>/', views.article, name='article'),
    
    # Optional parameters not directly supported; use two patterns or query strings
]
```

Views can be functions or classes:

```python
# blog/views.py
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    """Function-based view."""
    return HttpResponse("Blog Index")

def post_detail(request, post_id):
    """View with captured parameter."""
    return HttpResponse(f"Post ID: {post_id}")

# Query parameters accessed via request.GET
def search(request):
    query = request.GET.get('q', '')
    return HttpResponse(f"Searching for: {query}")
```

---

## 5. Request Handling

### Flask

The `request` object from Flask provides access to incoming data.

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/data', methods=['GET', 'POST', 'PUT'])
def handle_data():
    """Demonstrate accessing different parts of a request."""
    
    # Query parameters (GET /data?name=John)
    name = request.args.get('name')
    
    # Form data (POST with application/x-www-form-urlencoded or multipart)
    form_data = request.form.get('key')
    
    # JSON data (POST with application/json)
    json_data = request.get_json()
    
    # Headers
    user_agent = request.headers.get('User-Agent')
    
    # Cookies
    session_id = request.cookies.get('session_id')
    
    # Files
    uploaded_file = request.files.get('file')
    if uploaded_file:
        uploaded_file.save('uploads/' + uploaded_file.filename)
    
    # Method
    method = request.method
    
    return {
        'method': method,
        'name': name,
        'form_data': form_data,
        'json': json_data,
        'user_agent': user_agent,
        'session_id': session_id
    }
```

### FastAPI

FastAPI uses Python type hints to automatically parse request data. Parameters can be from the path, query, body, headers, cookies, etc.

```python
from fastapi import FastAPI, Request, Form, File, UploadFile, Header, Cookie
from pydantic import BaseModel

app = FastAPI()

# Define a Pydantic model for JSON body
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

@app.post("/items/")
async def create_item(
    # Query parameter
    q: str | None = None,
    # Header
    user_agent: str | None = Header(None),
    # Cookie
    session_id: str | None = Cookie(None),
    # JSON body (automatically validated)
    item: Item = None
):
    """Handle POST with JSON body plus optional query, header, cookie."""
    return {
        "q": q,
        "user_agent": user_agent,
        "session_id": session_id,
        "item": item
    }

# Form data (application/x-www-form-urlencoded)
@app.post("/form/")
async def handle_form(
    username: str = Form(...),
    password: str = Form(...)
):
    """Form data is parsed using Form(...)."""
    return {"username": username}

# File upload
@app.post("/files/")
async def upload_file(
    file: UploadFile = File(...)
):
    """Upload a single file."""
    contents = await file.read()
    # process contents...
    return {"filename": file.filename, "size": len(contents)}

# Access raw request object if needed
@app.get("/raw-request/")
async def raw_request(request: Request):
    """Get raw request object for advanced use."""
    body = await request.body()
    headers = request.headers
    client_host = request.client.host
    return {"client": client_host, "headers": dict(headers)}
```

### Django

In Django, views receive an `HttpRequest` object.

```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Function-based view
@csrf_exempt  # for demonstration only; in practice handle CSRF properly
def handle_data(request):
    # Method
    method = request.method
    
    # Query parameters (GET)
    name = request.GET.get('name')
    
    # POST form data
    form_data = request.POST.get('key')
    
    # JSON data (parse manually)
    json_data = None
    if request.body:
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            json_data = None
    
    # Headers
    user_agent = request.headers.get('User-Agent')
    
    # Cookies
    session_id = request.COOKIES.get('session_id')
    
    # Files
    uploaded_file = request.FILES.get('file')
    if uploaded_file:
        # handle file
        pass
    
    return JsonResponse({
        'method': method,
        'name': name,
        'form_data': form_data,
        'json': json_data,
        'user_agent': user_agent,
        'session_id': session_id
    })
```

---

## 6. Response Handling

### Flask

Flask views can return strings, tuples, or response objects.

```python
from flask import Flask, make_response, jsonify, redirect, url_for, abort

app = Flask(__name__)

@app.route('/')
def index():
    # Returning a string (default status 200)
    return "Hello"

@app.route('/json')
def json_response():
    # Return JSON using jsonify
    data = {'key': 'value'}
    return jsonify(data)

@app.route('/custom')
def custom_response():
    # Create a response object
    resp = make_response("Custom response", 200)
    resp.headers['X-Something'] = 'A value'
    resp.set_cookie('cookie_name', 'cookie_value')
    return resp

@app.route('/redirect')
def redirect_example():
    # Redirect to another endpoint
    return redirect(url_for('index'))

@app.route('/error')
def error_example():
    # Abort with HTTP error
    abort(404)  # triggers 404 handler
```

### FastAPI

FastAPI returns JSON by default, but can return any Starlette response.

```python
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse, PlainTextResponse
from fastapi import status

app = FastAPI()

@app.get("/")
async def root():
    # Return dict -> automatically JSON
    return {"message": "Hello"}

@app.get("/json")
async def custom_json():
    # Explicit JSONResponse
    content = {"message": "Hello"}
    return JSONResponse(content=content, status_code=200)

@app.get("/html")
async def html():
    # Return HTML
    html_content = "<h1>Hello</h1>"
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/text")
async def text():
    # Return plain text
    return PlainTextResponse("Just text", media_type="text/plain")

@app.get("/redirect")
async def redirect():
    # Redirect
    return RedirectResponse(url="/")

@app.get("/headers")
async def headers():
    # Set custom headers
    response = JSONResponse({"hello": "world"})
    response.headers["X-Custom"] = "Value"
    return response

@app.get("/cookies")
async def cookies():
    response = JSONResponse({"message": "cookies set"})
    response.set_cookie(key="session", value="abc123", max_age=3600)
    return response

@app.get("/status")
async def custom_status():
    # Use status constants
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"created": True})
```

### Django

Django views return `HttpResponse` or its subclasses.

```python
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse

def simple_response(request):
    # Plain text response
    return HttpResponse("Hello, world!")

def json_response(request):
    # JSON response
    data = {'key': 'value'}
    return JsonResponse(data)

def html_response(request):
    # Render a template
    return render(request, 'template.html', {'context_var': 'value'})

def redirect_response(request):
    # Redirect to URL by name
    return redirect('some-view-name')  # or reverse('some-view-name')

def custom_headers(request):
    response = HttpResponse("Headers example")
    response['X-Custom'] = 'some value'
    response.set_cookie('cookie', 'value')
    return response

def not_found(request):
    # Custom 404 response
    return HttpResponseNotFound("Page not found")
```

---

## 7. Templating

### Flask

Uses Jinja2 as its default templating engine.

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/hello/<name>')
def hello(name):
    # Renders hello.html from templates folder, passing variable 'name'
    return render_template('hello.html', name=name)
```

Template `templates/hello.html`:

```html
<!DOCTYPE html>
<html>
<head><title>Hello</title></head>
<body>
    <h1>Hello {{ name }}!</h1>
    {% if name == 'admin' %}
        <p>Welcome, admin.</p>
    {% endif %}
</body>
</html>
```

### FastAPI

FastAPI does not include a templating engine by default, but you can easily use Jinja2 with Starlette's `Jinja2Templates`.

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    # Render template with context
    return templates.TemplateResponse("item.html", {"request": request, "id": id})
```

Template `templates/item.html`:

```html
<html>
<body>
    <h1>Item ID: {{ id }}</h1>
</body>
</html>
```

### Django

Django has its own template language and built-in support.

```python
# views.py
from django.shortcuts import render

def article_list(request):
    articles = Article.objects.all()
    return render(request, 'blog/article_list.html', {'articles': articles})
```

Template `blog/templates/blog/article_list.html`:

```html
{% extends "base.html" %}

{% block content %}
<h1>Articles</h1>
<ul>
{% for article in articles %}
    <li>{{ article.title }} - {{ article.published_date|date:"Y-m-d" }}</li>
{% empty %}
    <li>No articles yet.</li>
{% endfor %}
</ul>
{% endblock %}
```

---

## 8. Database ORM / Models

### Flask

Flask does not include an ORM. Most developers use SQLAlchemy with Flask-SQLAlchemy extension.

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# Define a model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
```

### FastAPI

FastAPI works seamlessly with SQLAlchemy, but also encourages Pydantic models for data validation. Typically, you define SQLAlchemy models for the database and Pydantic models for API schemas.

```python
# models.py (SQLAlchemy)
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)

# schemas.py (Pydantic)
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True
```

Then in CRUD operations, you convert between SQLAlchemy and Pydantic.

### Django

Django has a powerful built-in ORM.

```python
# models.py
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=80, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
```

---

## 9. Migrations

### Flask

Flask doesn't have built-in migrations; use Alembic via Flask-Migrate.

```bash
pip install Flask-Migrate
```

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
```

Then commands:
```bash
flask db init
flask db migrate -m "message"
flask db upgrade
```

### FastAPI

No built-in migrations; use Alembic directly or integrate with SQLAlchemy.

Example `alembic.ini` and `env.py` configuration.

```bash
alembic init alembic
# edit alembic/env.py to point to your SQLAlchemy models
alembic revision --autogenerate -m "init"
alembic upgrade head
```

### Django

Django has built-in migrations.

```bash
python manage.py makemigrations
python manage.py migrate
```

Migrations are automatically generated based on model changes.

---

## 10. Forms & Validation

### Flask

Use WTForms via Flask-WTF.

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# In view
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # process form
        return redirect(...)
    return render_template('login.html', form=form)
```

### FastAPI

FastAPI uses Pydantic models for validation of request bodies. For HTML forms, you can use Pydantic as well, but you may also use Form parameters.

```python
from fastapi import FastAPI, Form
from pydantic import BaseModel, EmailStr, validator

app = FastAPI()

# Pydantic model with validation
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @validator('password')
    def password_length(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

@app.post("/users/")
async def create_user(user: UserCreate):
    # user is already validated
    return user
```

For form data:

```python
@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    # validate manually or use dependencies
    return {"username": username}
```

### Django

Django has its own forms system.

```python
# forms.py
from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

# views.py
from django.shortcuts import render, redirect
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # cleaned data available in form.cleaned_data
            email = form.cleaned_data['email']
            # process...
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
```

---

## 11. Authentication & Authorization

### Flask

Flask does not have built-in authentication. Use Flask-Login, Flask-Security, or JWT extensions.

```python
# Flask-Login example
from flask import Flask
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user

app = Flask(__name__)
app.secret_key = 'secret'
login_manager = LoginManager()
login_manager.init_app(app)

# User class
class User(UserMixin):
    # ...

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/login')
def login():
    user = User.authenticate(...)  # your auth logic
    login_user(user)
    return 'Logged in'

@app.route('/protected')
@login_required
def protected():
    return f'Hello {current_user.id}'
```

### FastAPI

FastAPI provides tools for authentication via dependencies. Common patterns: OAuth2 with JWT, API keys, etc.

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta

# Security config
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Token endpoint
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # authenticate user (pseudo-code)
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Dependency to get current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username)  # fetch from db
    if user is None:
        raise credentials_exception
    return user

# Protected endpoint
@app.get("/users/me")
async def read_users_me(current_user = Depends(get_current_user)):
    return current_user
```

### Django

Django has a built-in authentication system.

```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    # ...
]

# views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'logged in'})
        else:
            return JsonResponse({'error': 'invalid credentials'}, status=400)

@login_required
def profile(request):
    return JsonResponse({'username': request.user.username})
```

---

## 12. Middleware

### Flask

Flask middleware is implemented via `before_request`, `after_request`, etc., or using WSGI middleware.

```python
from flask import Flask, g, request

app = Flask(__name__)

@app.before_request
def before_request():
    """Executed before each request."""
    g.user = get_user_from_session()  # hypothetical
    print("Before request")

@app.after_request
def after_request(response):
    """Executed after each request."""
    response.headers['X-Powered-By'] = 'Flask'
    return response

@app.teardown_request
def teardown_request(exception=None):
    """Executed after response is sent."""
    print("Teardown")
```

### FastAPI

FastAPI uses Starlette middleware. You can add middleware using `app.add_middleware` or create custom ASGI middleware.

```python
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
import time

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

app = FastAPI()
app.add_middleware(TimingMiddleware)

# Or use built-in middleware like CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)
```

### Django

Django middleware is configured in `settings.MIDDLEWARE`. Each middleware is a class that processes requests/responses.

```python
# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # ...
]

# Custom middleware
class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to execute before view
        response = self.get_response(request)
        # Code to execute after view
        response['X-Custom'] = 'Value'
        return response
```

---

## 13. Error Handling

### Flask

Use `@app.errorhandler` decorator.

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error="Not found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error="Internal server error"), 500
```

### FastAPI

Use exception handlers.

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# Custom exception
class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something."},
    )

@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}

# Override default HTTPException handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
```

### Django

Django has several ways to handle errors: built-in error views, customizing handlers in URLconf, or middleware.

```python
# urls.py
handler404 = 'myapp.views.custom_404'
handler500 = 'myapp.views.custom_500'

# views.py
from django.http import JsonResponse

def custom_404(request, exception):
    return JsonResponse({'error': 'Not found'}, status=404)

def custom_500(request):
    return JsonResponse({'error': 'Server error'}, status=500)
```

---

## 14. Static Files

### Flask

By default, Flask serves static files from the `static/` folder at the `/static` URL.

```python
from flask import Flask, url_for

app = Flask(__name__)

# In template
# <img src="{{ url_for('static', filename='image.png') }}">
```

### FastAPI

FastAPI can serve static files using `Mount` or `StaticFiles`.

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# In template: <link href="{{ url_for('static', path='style.css') }}" rel="stylesheet">
```

### Django

Django has comprehensive static files handling.

```python
# settings.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]  # for development
STATIC_ROOT = BASE_DIR / "staticfiles"    # for production

# In template: {% load static %} <img src="{% static 'image.png' %}">
```

---

## 15. Admin Interface

### Flask

No built-in admin. Extensions like Flask-Admin provide admin interfaces.

```python
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

admin = Admin(app, name='My Admin')
admin.add_view(ModelView(User, db.session))
```

### FastAPI

No built-in admin. You can build a custom admin with FastAPI or use external tools.

### Django

Django has a powerful built-in admin interface.

```python
# admin.py
from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    search_fields = ('username', 'email')
```

---

## 16. REST API Support

### Flask

Flask doesn't have built-in REST support; use Flask-RESTful or Flask-RESTx extensions.

```python
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')
```

### FastAPI

FastAPI is built specifically for APIs, with automatic OpenAPI docs.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.get("/items/", response_model=list[Item])
async def get_items():
    return [{"name": "Foo", "price": 42.0}]

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item
```

### Django

Use Django REST Framework (DRF) for robust API building.

```python
# serializers.py
from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

# views.py
from rest_framework import generics
from .models import Item
from .serializers import ItemSerializer

class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
```

---

## 17. WebSockets / Real-time

### Flask

Flask is WSGI-based, not suitable for WebSockets out of the box. Use Flask-SocketIO which adds WebSocket support via gevent or eventlet.

```python
from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('message')
def handle_message(msg):
    print('Received: ' + msg)
    emit('response', {'data': 'got it'})

if __name__ == '__main__':
    socketio.run(app)
```

### FastAPI

FastAPI supports WebSockets natively via Starlette.

```python
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
```

### Django

Django is WSGI-based by default. For WebSockets, use Django Channels.

```python
# routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .consumers import ChatConsumer

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/chat/', ChatConsumer.as_asgi()),
    ]),
})

# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.send(text_data=json.dumps({'message': data}))
```

---

## 18. Testing

### Flask

Flask provides a test client.

```python
import pytest
from myapp import app

def test_home():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert b'Hello' in response.data
```

### FastAPI

FastAPI provides `TestClient` based on Starlette's test client (uses `requests` library).

```python
from fastapi.testclient import TestClient
from myapp import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
```

### Django

Django has its own test framework.

```python
from django.test import TestCase
from django.urls import reverse

class HomeViewTests(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello")
```

---

## 19. Deployment

### Flask

Common deployments: Gunicorn + Nginx, or using Waitress, uWSGI.

```bash
pip install gunicorn
gunicorn -w 4 myapp:app
```

### FastAPI

Since FastAPI is ASGI, use an ASGI server like Uvicorn or Hypercorn.

```bash
pip install uvicorn
uvicorn myapp:app --host 0.0.0.0 --port 8000 --workers 4
```

For production, often use Gunicorn with Uvicorn worker:

```bash
gunicorn -k uvicorn.workers.UvicornWorker myapp:app
```

### Django

WSGI deployment with Gunicorn or mod_wsgi, or ASGI with Daphne for Channels.

```bash
pip install gunicorn
gunicorn myproject.wsgi:application
```

Or use uWSGI, Waitress, etc.

---

## 20. Performance

| Framework | Performance Characteristics |
|-----------|-----------------------------|
| **Flask** | WSGI-based, synchronous by default. Can handle concurrent requests via multi-threading or multi-processing (Gunicorn workers). Good for I/O-bound tasks but not for high-concurrency real-time. |
| **FastAPI** | ASGI-based, asynchronous. Can handle high concurrency with async I/O. Performance is among the best for Python frameworks. |
| **Django** | WSGI-based by default, synchronous. With Django 3.1+, ASGI support allows async views. Typically slower than FastAPI for API-only workloads, but very efficient for full-stack apps. |

---

## 21. Community & Ecosystem

| Framework | Community | Extensions |
|-----------|-----------|------------|
| **Flask** | Large, mature. Many extensions available for almost any need. | Flask-SQLAlchemy, Flask-Migrate, Flask-Login, Flask-Admin, etc. |
| **FastAPI** | Rapidly growing, modern. Strong focus on APIs. | FastAPI Users, FastAPI Cache, etc. Leverages Starlette and Pydantic ecosystem. |
| **Django** | Huge, established. "Batteries included" but also many third-party packages. | Django REST Framework, Django Channels, Django Allauth, etc. |

---

## 22. Learning Curve

| Framework | Learning Curve |
|-----------|----------------|
| **Flask** | Gentle. Minimal setup, easy to start, but requires learning extensions as you go. |
| **FastAPI** | Moderate. Requires understanding of type hints, async/await, and Pydantic. But once grasped, very productive. |
| **Django** | Steep. Many concepts: models, views, templates, forms, admin, etc. But comprehensive documentation. |

---

## 23. Use Cases

| Framework | Best For |
|-----------|----------|
| **Flask** | Small to medium projects, microservices, APIs, prototyping, learning web development. |
| **FastAPI** | High-performance APIs, real-time applications, machine learning model serving, async-heavy apps. |
| **Django** | Large, complex web applications, content management systems, e-commerce, sites with admin interfaces. |

---

## 24. Summary Table

| Feature | Flask | FastAPI | Django |
|---------|-------|---------|--------|
| **Philosophy** | Micro, extensible | Modern, fast, API-first | Batteries-included, full-stack |
| **Project Structure** | Flexible | Flexible | Enforced (apps) |
| **Routing** | Decorator-based | Decorator with type hints | URL patterns |
| **Request Parsing** | `request` object | Type hints + Pydantic | `request` object + forms |
| **Response** | String, JSON, etc. | Any, automatic JSON | HttpResponse subclasses |
| **Templating** | Jinja2 (built-in) | Jinja2 (via Starlette) | Django template language |
| **ORM** | External (SQLAlchemy) | External (SQLAlchemy, etc.) | Built-in ORM |
| **Migrations** | External (Alembic) | External (Alembic) | Built-in migrations |
| **Forms/Validation** | WTForms | Pydantic | Django Forms |
| **Authentication** | Extensions | Dependencies + OAuth2 | Built-in auth |
| **Middleware** | `before_request`, etc. | ASGI middleware | Middleware classes |
| **Error Handling** | `@errorhandler` | Exception handlers | Custom handlers |
| **Static Files** | `/static` folder | `StaticFiles` mount | Static files app |
| **Admin Interface** | Extensions | None | Built-in admin |
| **REST API** | Extensions | Native | Django REST Framework |
| **WebSockets** | Flask-SocketIO | Native WebSocket support | Django Channels |
| **Testing** | Test client | TestClient (Starlette) | Django test framework |
| **Deployment** | WSGI (Gunicorn) | ASGI (Uvicorn) | WSGI/ASGI |
| **Performance** | Moderate | High | Moderate |
| **Community** | Large, mature | Growing | Huge, established |
| **Learning Curve** | Easy | Moderate | Steep |
| **Best Use Cases** | Microservices, small apps | High-performance APIs | Large full-stack apps |

---

## Conclusion

Each framework excels in different areas. **Flask** offers simplicity and flexibility, making it great for learning and small projects. **FastAPI** is the modern choice for high-performance APIs, leveraging Python's async capabilities and type hints. **Django** is the comprehensive solution for building large, feature-rich web applications quickly with its "batteries-included" approach.

Your choice depends on your project requirements, team expertise, and long-term goals. For a full-stack developer, knowing all three (or at least understanding their strengths) is a valuable skill that allows you to pick the right tool for each job.