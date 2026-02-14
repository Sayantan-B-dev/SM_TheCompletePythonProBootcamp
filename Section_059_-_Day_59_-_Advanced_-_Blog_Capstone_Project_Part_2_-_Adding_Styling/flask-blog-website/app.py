from flask import Flask, render_template, request, session, redirect, url_for, flash
import requests
import math
import logging
import time
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "asdgadsgadgadgadg"
app.permanent_session_lifetime = timedelta(hours=1)  # Session lasts 1 hour

BLOG_API_URL = "https://jsonfakery.com/blogs"
POSTS_PER_PAGE = 6
CACHE_DURATION = 3600  # 1 hour in seconds

logging.basicConfig(level=logging.DEBUG)

# In-memory cache: {session_id: (timestamp, blog_data)}
blog_cache = {}
contact_messages = []

def get_session_id():
    """Generate or retrieve a unique session ID"""
    if 'session_id' not in session:
        # Create a unique ID for this session
        session['session_id'] = str(time.time()) + str(hash(str(session) + str(time.time())))
        # Make the session permanent
        session.permanent = True
    return session['session_id']

def get_blogs_from_cache_or_api():
    """Fetch blogs from cache if available and fresh, otherwise from API"""
    session_id = get_session_id()
    current_time = time.time()
    
    # Check if we have fresh cached data for this session
    if session_id in blog_cache:
        cache_time, cached_data = blog_cache[session_id]
        if current_time - cache_time < CACHE_DURATION:
            app.logger.debug(f"Returning cached blogs for session {session_id}")
            return cached_data
    
    # Fetch from API
    try:
        app.logger.debug(f"Fetching fresh blogs from API for session {session_id}")
        response = requests.get(BLOG_API_URL, timeout=5)
        response.raise_for_status()
        all_blogs = response.json()
        
        # Handle different response formats
        if isinstance(all_blogs, dict):
            all_blogs = all_blogs.get('data', []) or all_blogs.get('blogs', []) or []
        
        if not isinstance(all_blogs, list):
            all_blogs = []
        
        # Store in cache
        blog_cache[session_id] = (current_time, all_blogs)
        
        # Clean up old cache entries (optional)
        cleanup_cache()
        
        return all_blogs
    except Exception as e:
        app.logger.error(f"API request failed: {e}")
        # Return stale cache if available, otherwise empty list
        if session_id in blog_cache:
            return blog_cache[session_id][1]
        return []

def cleanup_cache():
    """Remove expired cache entries"""
    current_time = time.time()
    expired = [sid for sid, (timestamp, _) in blog_cache.items() 
               if current_time - timestamp > CACHE_DURATION]
    for sid in expired:
        del blog_cache[sid]

@app.route('/')
def home():
    all_blogs = get_blogs_from_cache_or_api()
    featured_blogs = all_blogs[:3] if all_blogs else []
    return render_template('index.html', featured_blogs=featured_blogs)

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

@app.route('/blog/<string:blog_id>')
def blog_detail(blog_id):
    all_blogs = get_blogs_from_cache_or_api()
    blog = next((b for b in all_blogs if str(b.get('id')) == blog_id), None)
    
    if not blog:
        flash('Blog not found.', 'error')
        return render_template('404.html'), 404
    
    return render_template('blog_detail.html', blog=blog)

@app.route('/about')
def about():
    return render_template('about.html')

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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)