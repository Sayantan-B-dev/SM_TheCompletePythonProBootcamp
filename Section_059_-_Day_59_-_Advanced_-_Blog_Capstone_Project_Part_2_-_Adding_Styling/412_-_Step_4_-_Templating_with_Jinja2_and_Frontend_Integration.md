## Step 4: Templating with Jinja2 and Frontend Integration

Flask uses the **Jinja2** templating engine to generate dynamic HTML pages. Templates combine static markup with placeholders and logic that are filled with data from view functions. The FlaskBlog project demonstrates a well‑structured template hierarchy, inheritance, and integration with Bootstrap for responsive design.

### 4.1 Template Inheritance: The Base Template

The `base.html` file serves as the skeleton for all pages. It contains the common HTML structure: `<!DOCTYPE html>`, `<head>` with meta tags, CSS links, the navigation bar, flash message container, main content area, footer, and JavaScript includes. Child templates extend `base.html` and override specific blocks.

**base.html structure (simplified):**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}FlaskBlog | Modern Interactive Blog{% endblock %}</title>
    <!-- Bootstrap, Font Awesome, AOS, Google Fonts, custom CSS -->
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Preloader, Navbar, Flash container -->
    <main>
        {% block content %}{% endblock %}
    </main>
    <!-- Footer, Back to top, Scripts -->
    {% block extra_js %}{% endblock %}
</body>
</html>
```

- **`{% block ... %}`**: Defines sections that child templates can fill. `title` and `content` are the primary blocks; `extra_css` and `extra_js` allow page‑specific additions.
- **`{{ ... }}`**: Used to output variables (e.g., `{{ url_for('home') }}`).

Child templates use `{% extends "base.html" %}` and then provide content for the blocks.

**Example: `404.html`**
```html
{% extends "base.html" %}
{% block title %}Page Not Found - FlaskBlog{% endblock %}
{% block content %}
<div class="error-page">
    <!-- error content -->
</div>
{% endblock %}
```

### 4.2 Passing Data from Views to Templates

View functions call `render_template()` with the template name and any number of keyword arguments. These become variables accessible in the template.

**From `blogs()` view:**
```python
return render_template(
    'blogs.html',
    blogs=paginated_blogs,
    current_page=page,
    total_pages=total_pages,
    has_next=page < total_pages,
    has_prev=page > 1
)
```

In `blogs.html`, these variables are used to render the list of blogs, pagination controls, etc.

### 4.3 Template Variables and Filters

Jinja2 variables are accessed using dot notation or square brackets. Filters modify variables; they are applied with the pipe symbol `|`.

**Example from `blog_detail.html`:**
```html
<h1>{{ blog.title }}</h1>
<span><i class="far fa-user me-1"></i> {{ blog.user.first_name ~ ' ' ~ blog.user.last_name if blog.user else 'Admin' }}</span>
```

- `blog.user.first_name` accesses nested object attributes.
- The `~` operator concatenates strings.
- The `if blog.user else 'Admin'` is an **inline conditional expression**.

**Filters:**
- `|truncate(100)` in `blogs.html`: limits text to 100 characters.
- `|safe` in `blog_detail.html`: marks content as safe HTML (used for `blog.main_content` which may contain rich text).
- `|length` in `search_results.html`: returns the number of items in a list.

### 4.4 Control Structures: Loops and Conditionals

**Looping over blog posts in `blogs.html`:**
```html
{% for blog in blogs %}
<div class="col-lg-4 col-md-6" data-aos="fade-up" data-aos-delay="{{ loop.index0 * 50 }}">
    <!-- blog card -->
</div>
{% else %}
<div class="col-12 text-center py-5">
    <!-- no blogs fallback -->
</div>
{% endfor %}
```

- `loop.index0` gives the zero‑based index of the current iteration, used here to stagger animations.
- `{% else %}` executes if the iterable is empty.

**Conditionals for pagination:**
```html
<li class="page-item {{ 'disabled' if not has_prev }}">
    <a class="page-link" href="{{ url_for('blogs', page=current_page-1) if has_prev else '#' }}">
        <i class="fas fa-chevron-left"></i>
    </a>
</li>
```

The `{{ 'disabled' if not has_prev }}` adds the `disabled` class when there is no previous page. The `href` is conditionally set using an inline if‑else.

**More complex conditionals:**
```html
{% if blog.featured_image %}
<img src="{{ blog.featured_image }}" ...>
{% endif %}
```

### 4.5 URL Building with `url_for`

In templates, the `url_for()` function generates URLs based on endpoint names. This keeps links decoupled from the actual URL patterns.

```html
<a href="{{ url_for('blog_detail', blog_id=blog.id) }}" class="btn btn-primary">Read More</a>
```

`url_for('blog_detail', blog_id=blog.id)` produces `/blog/123` (assuming the blog’s ID is 123). If the route definition changes, all links automatically update.

### 4.6 Static Files

CSS and JavaScript files are served from the `static` folder and linked using `url_for('static', filename='...')`.

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
<script src="{{ url_for('static', filename='js/main.js') }}"></script>
```

This ensures correct paths even if the application is mounted under a subpath.

### 4.7 Bootstrap Integration

Bootstrap 5 is loaded from a CDN in `base.html`. The templates make extensive use of Bootstrap classes for layout, components, and responsiveness:

- Grid system: `container`, `row`, `col-lg-4`, etc.
- Navigation: `navbar`, `navbar-nav`, `nav-link`.
- Cards: `card`, `card-body`, `card-title`.
- Buttons: `btn`, `btn-primary`, `btn-lg`.
- Forms: `form-control`, `input-group`.
- Pagination: `pagination`, `page-item`, `page-link`.

The use of Bootstrap ensures a consistent, mobile‑first design with minimal custom CSS.

### 4.8 Custom CSS and Theming

The `style.css` file defines custom styles, including CSS variables for light/dark theme switching. These variables are used throughout the templates to maintain a cohesive look. For example, the `.blog-card` class uses `var(--primary-color)` for its gradient background.

The theme toggle in `main.js` toggles a `data-theme` attribute on the `<html>` element, and CSS rules like `[data-theme="dark"] { ... }` adjust the variable values accordingly.

### 4.9 Template Organization

All templates reside in the `templates/` directory. The naming convention is straightforward: each route has a corresponding template (e.g., `index.html`, `blogs.html`, `blog_detail.html`). Error pages are named after the HTTP status code.

### 4.10 Example: Dynamic Content in `blog_detail.html`

The blog detail page demonstrates advanced template usage:

```html
{% extends "base.html" %}
{% block title %}{{ blog.title }} - FlaskBlog{% endblock %}
{% block content %}
<div class="container py-5">
    <div class="blog-detail">
        <h1>{{ blog.title }}</h1>
        <div class="blog-meta">
            <span><i class="far fa-calendar-alt"></i> {{ blog.created_at }}</span>
            <span><i class="far fa-user"></i> {{ blog.user.first_name ~ ' ' ~ blog.user.last_name if blog.user else 'Admin' }}</span>
            <span><i class="far fa-folder"></i> {{ blog.category or 'General' }}</span>
        </div>
        {% if blog.featured_image %}
        <img src="{{ blog.featured_image }}" class="img-fluid" alt="{{ blog.title }}">
        {% endif %}
        {% if blog.subtitle %}
        <p class="lead">{{ blog.subtitle }}</p>
        {% endif %}
        <div class="blog-content">
            {% if blog.main_content %}
                {{ blog.main_content|safe }}
            {% else %}
                <p>No content available.</p>
            {% endif %}
        </div>
        <!-- Tags, comments, etc. -->
    </div>
</div>
{% endblock %}
```

- The `title` block is overridden to include the blog’s title.
- The `content` block contains the entire page.
- Multiple conditionals check for optional fields (`blog.featured_image`, `blog.subtitle`, `blog.main_content`).
- The `|safe` filter is necessary because `main_content` may contain HTML that should be rendered, not escaped.

### 4.11 Flash Messages

The flash message container in `base.html` iterates over messages and displays them as Bootstrap alerts:

```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
            <div class="alert alert-{{ 'success' if category == 'success' else 'danger' }} ...">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

The category is used to choose between `alert-success` and `alert-danger` Bootstrap classes.

### 4.12 The `url_for` in JavaScript

While not directly Jinja2, note that the `url_for` function can also be used inside `<script>` tags if the script is rendered by the template (inline JavaScript). In this project, external `main.js` does not use Flask’s `url_for`, but any inline script could.

---

**Key Takeaways from Step 4:**
- Jinja2 templates inherit from a base template, promoting code reuse.
- View functions pass data as template variables.
- Filters like `truncate`, `safe`, and `length` manipulate output.
- Control structures (`for`, `if`) enable dynamic rendering.
- `url_for` generates links to routes.
- Bootstrap classes provide responsive layout and components.
- Custom CSS and theme switching are integrated via CSS variables.
- Flash messages are displayed using Bootstrap alerts.