## Step 2: Routing and View Functions

Flask uses decorators to map URLs to Python functions, known as **view functions**. Each route defines which HTTP methods it accepts, how parameters are extracted, and what logic executes when the endpoint is accessed. The FlaskBlog application implements a clean set of routes that cover all user-facing pages and handle both GET and POST requests where appropriate.

### 2.1 Route Definitions Overview

All routes are defined in `app.py` using the `@app.route` decorator. The following routes exist:

| URL Pattern           | Methods      | View Function    | Description |
|----------------------|--------------|------------------|-------------|
| `/`                  | GET          | `home()`         | Homepage with featured blogs |
| `/blogs`             | GET          | `blogs()`        | Paginated list of all blogs |
| `/blog/<blog_id>`    | GET          | `blog_detail()`  | Individual blog post |
| `/about`             | GET          | `about()`        | About page |
| `/contact`           | GET, POST    | `contact()`      | Contact form with submission handling |
| `/search`            | GET          | `search()`       | Search results page |
| *404*                | -            | `page_not_found()`| Custom 404 error handler |
| *500*                | -            | `internal_server_error()`| Custom 500 error handler |

### 2.2 Home Route (`/`)

```python
@app.route('/')
def home():
    all_blogs = get_blogs_from_cache_or_api()
    featured_blogs = all_blogs[:3] if all_blogs else []
    return render_template('index.html', featured_blogs=featured_blogs)
```

- **Method**: GET only (default).
- **Logic**: Fetches all blogs via the caching mechanism, then slices the first three to display as featured posts.
- **Template**: Renders `index.html` and passes the `featured_blogs` list.
- **Edge Cases**: If the API returns no blogs, `all_blogs` is an empty list, so `featured_blogs` remains empty; the template includes fallback placeholders.

### 2.3 Blogs Listing with Pagination (`/blogs`)

```python
@app.route('/blogs')
def blogs():
    page = request.args.get('page', 1, type=int)
    all_blogs = get_blogs_from_cache_or_api()
    
    total_blogs = len(all_blogs)
    total_pages = math.ceil(total_blogs / POSTS_PER_PAGE) if total_blogs > 0 else 1
    page = max(1, min(page, total_pages))
    
    start_idx = (page - 1) * POSTS_PER_PAGE
    end_idx = start_idx + POSTS_PER_PAGE
    paginated_blogs = all_blogs[start_idx:end_idx]
    
    return render_template(
        'blogs.html',
        blogs=paginated_blogs,
        current_page=page,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )
```

- **Query Parameter**: `page` is extracted from the request’s query string using `request.args.get()`. The `type=int` ensures automatic conversion to integer; defaults to 1.
- **Pagination Calculation**: Total pages computed with `math.ceil`. The current page is clamped between 1 and `total_pages`.
- **Slicing**: Blogs for the current page are extracted from the full list.
- **Template Context**: Passes the paginated blogs, current page, total pages, and boolean flags for previous/next buttons.
- **URL Building**: In the template, links to other pages are generated with `url_for('blogs', page=p)`, which preserves the route and adds the `page` parameter.

### 2.4 Blog Detail with Dynamic URL Parameter (`/blog/<blog_id>`)

```python
@app.route('/blog/<string:blog_id>')
def blog_detail(blog_id):
    all_blogs = get_blogs_from_cache_or_api()
    blog = next((b for b in all_blogs if str(b.get('id')) == blog_id), None)
    
    if not blog:
        flash('Blog not found.', 'error')
        return render_template('404.html'), 404
    
    return render_template('blog_detail.html', blog=blog)
```

- **Dynamic Segment**: `<string:blog_id>` captures the blog identifier from the URL. Flask converts it to a string (default converter).
- **Data Lookup**: Iterates over all blogs, comparing the `id` field (converted to string) with the captured `blog_id`.
- **Error Handling**: If no matching blog is found, a flash message is set, and the 404 template is rendered with a 404 status code.
- **Template**: Passes the found `blog` object to `blog_detail.html`.

### 2.5 About Page (`/about`)

```python
@app.route('/about')
def about():
    return render_template('about.html')
```

- Simple static page; no dynamic data required.

### 2.6 Contact Page with Form Handling (`/contact`)

```python
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        if not all([name, email, subject, message]):
            flash('Please fill in all fields', 'error')
        else:
            contact_messages.append({
                'name': name,
                'email': email,
                'subject': subject,
                'message': message,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            flash('Your message has been sent successfully!', 'success')
            return redirect(url_for('contact'))
    
    return render_template('contact.html')
```

- **Methods**: Both GET and POST are allowed.
- **POST Processing**:
  - Extracts form fields from `request.form`.
  - Validates that all fields are present (truthy).
  - On success, appends the message to the in‑memory list, adds a success flash, and redirects back to the contact page (POST‑Redirect‑GET pattern).
  - On validation failure, sets an error flash and re‑renders the template (though the redirect is skipped, the template will show with flashed message).
- **GET**: Simply renders the contact form.

### 2.7 Search Route (`/search`)

```python
@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    if not query:
        return redirect(url_for('blogs'))
    
    all_blogs = get_blogs_from_cache_or_api()
    
    results = []
    for blog in all_blogs:
        title = blog.get('title', '')
        content = blog.get('content') or blog.get('body') or blog.get('description', '')
        summary = blog.get('summary', '')
        if (query.lower() in title.lower() or 
            query.lower() in content.lower() or 
            query.lower() in summary.lower()):
            results.append(blog)
    
    return render_template('search_results.html', results=results, query=query)
```

- **Query Parameter**: `q` is retrieved and stripped. If empty, redirects to the blogs listing.
- **Search Logic**: Iterates through all blogs, checking for case‑insensitive substring matches in title, content/body/description, and summary.
- **Template**: Renders `search_results.html` with the results list and the original query.

### 2.8 Error Handlers

```python
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
```

- **Decorator**: `@app.errorhandler(code)` registers a function to handle specific HTTP errors.
- **Return Value**: The function returns both a template and the corresponding HTTP status code.
- These handlers ensure that even when errors occur, the user sees a styled page consistent with the rest of the site.

### 2.9 URL Building with `url_for`

Throughout the application, `url_for()` is used to generate URLs dynamically. For example:

- In templates: `{{ url_for('blog_detail', blog_id=blog.id) }}` creates the link to the blog detail page.
- In redirects: `return redirect(url_for('contact'))` after form submission.

This approach decouples URLs from the code; if a route path changes, only the decorator needs updating, and all `url_for` calls automatically adapt.

### 2.10 Request/Response Cycle in Flask

1. **Client Request**: User navigates to a URL (e.g., `/blogs?page=2`).
2. **Routing**: Flask matches the URL against registered routes, extracting any variable parts and query parameters.
3. **View Function Execution**: The corresponding function is called with the captured parameters.
4. **Data Handling**: The function may call helper functions (like `get_blogs_from_cache_or_api()`) to retrieve data.
5. **Template Rendering**: `render_template()` compiles the Jinja2 template with the provided context, producing HTML.
6. **Response**: Flask returns the HTML (with appropriate status code) to the client.

---

**Key Takeaways from Step 2:**
- Flask routes map URLs to view functions using decorators.
- Dynamic segments (`<string:blog_id>`) capture parts of the URL.
- Query parameters are accessed via `request.args`.
- POST data is retrieved from `request.form`.
- The `url_for()` function provides reverse URL building.
- Error handlers customize the response for HTTP errors.
- The view functions orchestrate data retrieval, business logic, and template rendering.