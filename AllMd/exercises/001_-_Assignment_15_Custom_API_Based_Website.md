# Art Search Flask Application Documentation

![](./art_search/sample.png)

## Table of Contents

- [Art Search Flask Application Documentation](#art-search-flask-application-documentation)
  - [Table of Contents](#table-of-contents)
  - [1. Project Overview](#1-project-overview)
  - [2. Quick Start](#2-quick-start)
    - [Prerequisites](#prerequisites)
    - [Installation Steps](#installation-steps)
    - [Running the Application](#running-the-application)
  - [3. Environment Variables](#3-environment-variables)
  - [4. Project File Structure](#4-project-file-structure)
  - [5. Backend: `app.py` Detailed Explanation](#5-backend-apppy-detailed-explanation)
    - [5.1 Imports](#51-imports)
    - [5.2 Flask App Initialization](#52-flask-app-initialization)
    - [5.3 Custom Jinja Filter: `exclude`](#53-custom-jinja-filter-exclude)
    - [5.4 Constants: API Key, Base URL, Filter Lists](#54-constants-api-key-base-url-filter-lists)
    - [5.5 Core API Calling Function: `call_api(endpoint, params=None)`](#55-core-api-calling-function-call_apendpoint-paramsnone)
    - [5.6 Route: `/` (Index)](#56-route--index)
    - [5.7 Route: `/search`](#57-route-search)
    - [5.8 Route: `/artwork/<int:id>`](#58-route-artworkintid)
    - [5.9 Route: `/random`](#59-route-random)
    - [5.10 Application Entry Point](#510-application-entry-point)
  - [6. Frontend Templates](#6-frontend-templates)
    - [6.1 Base Template: `base.html`](#61-base-template-basehtml)
      - [Key Sections](#key-sections)
      - [NProgress Integration](#nprogress-integration)
      - [AJAX Fetch Override](#ajax-fetch-override)
    - [6.2 Index Template: `index.html`](#62-index-template-indexhtml)
      - [Structure](#structure)
      - [Search Form](#search-form)
      - [Results Container](#results-container)
      - [JavaScript: AJAX Search and Pagination](#javascript-ajax-search-and-pagination)
    - [6.3 Partial Results Template: `_results.html`](#63-partial-results-template-_resultshtml)
      - [Conditional Rendering](#conditional-rendering)
      - [Artwork Grid](#artwork-grid)
      - [Pagination](#pagination)
    - [6.4 Artwork Detail Template: `artwork.html`](#64-artwork-detail-template-artworkhtml)
    - [6.5 Error Template: `error.html`](#65-error-template-errorhtml)
  - [7. Data Flow and Application Logic](#7-data-flow-and-application-logic)
    - [7.1 Initial Page Load](#71-initial-page-load)
    - [7.2 Performing a Search (AJAX)](#72-performing-a-search-ajax)
    - [7.3 Pagination (AJAX)](#73-pagination-ajax)
    - [7.4 Direct Access to Artwork Detail](#74-direct-access-to-artwork-detail)
    - [7.5 Random Artwork Redirect](#75-random-artwork-redirect)
    - [7.6 Error Handling Flow](#76-error-handling-flow)
  - [8. Key Features Explained](#8-key-features-explained)
    - [8.1 AJAX Navigation with NProgress](#81-ajax-navigation-with-nprogress)
    - [8.2 Custom Jinja Filter for Pagination](#82-custom-jinja-filter-for-pagination)
    - [8.3 Glassmorphism UI and Animations](#83-glassmorphism-ui-and-animations)
    - [8.4 API Error Handling](#84-api-error-handling)
  - [9. Configuration and Customization](#9-configuration-and-customization)
    - [9.1 Changing the API Key](#91-changing-the-api-key)
    - [9.2 Modifying Filter Options](#92-modifying-filter-options)
    - [9.3 Adjusting Timeout or Retry Logic](#93-adjusting-timeout-or-retry-logic)
    - [9.4 Changing UI Theme](#94-changing-ui-theme)
  - [10. Deployment Considerations](#10-deployment-considerations)
  - [11. Troubleshooting](#11-troubleshooting)
  - [12. Conclusion](#12-conclusion)

---

## 1. Project Overview

The **Art Search** application is a Flask-based web interface that allows users to explore artworks from the [artsearch.io](https://artsearch.io/) API. Users can search for artworks by keywords, filter by type, material, technique, origin, date ranges, and aspect ratio, and view detailed information about individual pieces. The interface features a modern glassmorphism design, AJAX-powered search and pagination, and comprehensive error handling. This api has 50 req per daily on free tier.

The application is built with:
- **Flask** (Python web framework)
- **Jinja2** templating
- **Tailwind CSS** for styling
- **NProgress** for loading indicators
- **Requests** library for API calls

---

## 2. Quick Start

Follow these steps to get the application running locally.

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for cloning)

### Installation Steps

1. **Clone the repository** (or create the project directory and add the files):
   ```bash
   git clone <repository-url>
   cd art-search
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install required packages**:
   ```bash
   pip install flask requests python-dotenv
   ```

   *Note: `python-dotenv` is optional but recommended for managing environment variables.*

4. **Set up environment variables**:
   - Create a `.env` file in the project root (or export variables directly).
   - Add your Artsearch API key. If you don't have one, you can use the default key provided in the code (`b84d8eee51814217a150f851ceec88a0`), but it's recommended to obtain your own from [artsearch.io](https://artsearch.io/).

   **`.env` file example:**
   ```
   ARTSEARCH_API_KEY=your_actual_api_key_here
   ```

5. **Run the Flask application**:
   ```bash
   python app.py
   ```

6. **Open your browser** and go to `http://127.0.0.1:5000`.

### Running the Application

- The app runs in debug mode by default (enabled in `app.py`). To run in production, set `debug=False` and use a production WSGI server like Gunicorn.
- If you don't set the API key via environment variable, the code falls back to a hardcoded default (`b84d8eee51814217a150f851ceec88a0`). This may have rate limits; it's better to use your own.

---

## 3. Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `ARTSEARCH_API_KEY` | Your Artsearch API key. Obtain from [artsearch.io](https://artsearch.io/). | No (fallback provided) | `b84d8eee51814217a150f851ceec88a0` |

The key is read via `os.environ.get('ARTSEARCH_API_KEY', 'b84d8eee51814217a150f851ceec88a0')`. In production, always set this environment variable securely.

---

## 4. Project File Structure

```
art-search/
│
├── app.py                     # Main Flask application
├── .env                       # Environment variables (not in repo)
├── requirements.txt           # (optional) List of dependencies
│
└── templates/                 # Jinja2 HTML templates
    ├── base.html              # Base layout with navigation, footer, global styles
    ├── index.html             # Main page: search form and results container
    ├── _results.html          # Partial template for search results grid
    ├── artwork.html           # Detailed view of a single artwork
    └── error.html             # Error page template
```

*Note: The application does not include a static folder because all CSS is from Tailwind CDN and icons are inline SVGs.*

---

## 5. Backend: `app.py` Detailed Explanation

### 5.1 Imports

```python
import os
import time
from flask import Flask, render_template, request, jsonify, url_for, redirect
import requests
```

- `os`: Used to read environment variables.
- `time`: Commented out, but could be used to simulate slow loading (for testing).
- `Flask`: Core Flask class.
- `render_template`: Renders Jinja templates.
- `request`: Access request data (args, headers, etc.).
- `jsonify`: Not used in current code but imported.
- `url_for`: Generate URLs for routes.
- `redirect`: Redirect to another endpoint.
- `requests`: Make HTTP calls to the external Artsearch API.

### 5.2 Flask App Initialization

```python
app = Flask(__name__)
```

Creates the Flask application instance.

### 5.3 Custom Jinja Filter: `exclude`

```python
@app.template_filter('exclude')
def exclude_dict(d, *keys):
    return {k: v for k, v in d.items() if k not in keys}
```

- Purpose: This filter allows templates to remove specific keys from a dictionary before using it to generate URLs. It's used in pagination links to exclude the `offset` parameter from the current query arguments when generating links for previous/next pages.
- How it works: Takes a dictionary `d` and a variable number of keys to exclude. Returns a new dict with all key-value pairs except those whose keys are in `*keys`.
- Usage in `_results.html`:
  ```html
  href="{{ url_for('search', offset=offset-number, **request.args|exclude('offset')) }}"
  ```
  This preserves all existing query parameters (like `query`, `type`, etc.) but removes the current `offset` so that the new offset can be added cleanly.

### 5.4 Constants: API Key, Base URL, Filter Lists

```python
API_KEY = os.environ.get('ARTSEARCH_API_KEY', 'b84d8eee51814217a150f851ceec88a0')
BASE_URL = 'https://api.artsearch.io/artworks'

TYPES = [ ... ]
MATERIALS = [ ... ]
TECHNIQUES = [ ... ]
```

- `API_KEY`: Retrieves from environment or uses a hardcoded fallback.
- `BASE_URL`: The endpoint for artworks.
- `TYPES`, `MATERIALS`, `TECHNIQUES`: Lists of possible filter values. These are passed to templates to populate dropdowns. They match the API's filterable fields.

### 5.5 Core API Calling Function: `call_api(endpoint, params=None)`

This function handles all communication with the Artsearch API, including error handling.

**Parameters:**
- `endpoint` (str): The API endpoint path (e.g., `''` for search, `'/{id}'` for single artwork, `'/random'` for random).
- `params` (dict, optional): Query parameters to include in the request.

**Process:**
1. Initialize params dict if None.
2. Add the API key to params (`params['api-key'] = API_KEY`).
3. Construct full URL: `f"{BASE_URL}{endpoint}"`.
4. Attempt GET request with timeout=10 seconds.
5. If successful, return JSON response.
6. Catch various exceptions and return a standardized error dictionary.

**Error Handling Details:**

| Exception | Returned Error |
|-----------|----------------|
| `requests.exceptions.Timeout` | `{'error': 'The server is taking too long to respond...'}` |
| `requests.exceptions.ConnectionError` | `{'error': 'Unable to connect to the art database...'}` |
| `requests.exceptions.HTTPError` | Based on status code: 401 (Invalid API Key), 404 (Not found), 429 (Too many requests), else generic server error. |
| `requests.exceptions.RequestException` | `{'error': 'An unexpected error occurred...'}` |

**Return Value:** A dictionary. If an error occurred, the dict contains an `'error'` key. Otherwise, it contains the API's JSON response.

### 5.6 Route: `/` (Index)

```python
@app.route('/')
def index():
    return render_template('index.html', types=TYPES, materials=MATERIALS, techniques=TECHNIQUES)
```

- Renders the main page.
- Passes the filter lists to the template so the dropdowns are populated.

### 5.7 Route: `/search`

This is the most complex route, handling both full page requests and AJAX partial requests.

**Parameters** (from request args):
- `query` (str): Search query.
- `number` (int, default 10): Number of results per page.
- `offset` (int, default 0): Pagination offset.
- Filters: `type`, `material`, `technique`, `origin`, `earliest_start`, `latest_start`, `min_ratio`, `max_ratio`. (Note: parameter names in API differ slightly, e.g., `earliest-start-date` but we use `earliest_start` in form and convert later.)

**Process:**
1. Extract all parameters from `request.args`.
2. Build a `params` dict for the API call:
   - Include `query`, `number`, `offset`.
   - Add any filter that is not `None` or empty string, mapping form field names to API parameter names (e.g., `earliest_start` becomes `earliest-start-date`).
3. Call `call_api('', params=params)`.
4. If the result contains an `'error'` key, render the error template.
5. Check if the request is AJAX by looking at the `X-Requested-With` header.
   - If AJAX (`XMLHttpRequest`), render only the `_results.html` partial with the artworks, total count, and current pagination info.
   - If not AJAX (full page load), render `index.html` with the results and the filter lists (so the form is populated).
6. In the AJAX case, the returned HTML will be inserted into the page by JavaScript.

**Important:** The `exclude` filter is used in the template to build pagination URLs, not in the route itself.

### 5.8 Route: `/artwork/<int:id>`

```python
@app.route('/artwork/<int:id>')
def artwork_detail(id):
    data = call_api(f'/{id}')
    if 'error' in data:
        return render_template('error.html', error=data['error'])
    return render_template('artwork.html', artwork=data)
```

- Fetches a single artwork by its ID.
- If error, renders error page with the error message.
- Otherwise, renders `artwork.html` passing the artwork data.

### 5.9 Route: `/random`

```python
@app.route('/random')
def random_artwork():
    data = call_api('/random')
    if 'error' in data:
        return render_template('error.html', error=data['error'])
    return redirect(url_for('artwork_detail', id=data['id']))
```

- Calls the API's random endpoint.
- If successful, redirects to the detail page of the returned artwork using its ID.
- If error, shows error page.

### 5.10 Application Entry Point

```python
if __name__ == '__main__':
    app.run(debug=True)
```

- Runs the Flask development server with debug mode on. Debug mode enables auto-reloading and detailed error pages. Should be disabled in production.

---

## 6. Frontend Templates

All templates extend `base.html` (except `_results.html`, which is a partial). They use Tailwind CSS for styling and custom glassmorphism classes.

### 6.1 Base Template: `base.html`

#### Key Sections

- **Head**: Contains meta tags, Tailwind CDN, Google Fonts (Outfit), NProgress CSS/JS, and custom styles.
- **Body**: 
  - Navigation bar with logo and external links.
  - `<main>` block for content.
  - Footer with API status indicator.
  - AJAX handling script (overrides `window.fetch` to show NProgress).

#### NProgress Integration

- NProgress is a slim progress bar library that shows when AJAX requests are in progress.
- The script overrides `window.fetch` to increment a pending request counter and start/stop NProgress accordingly. This ensures any fetch call (including those from our AJAX search) triggers the loading bar.

#### AJAX Fetch Override

```javascript
(function () {
    let pendingRequests = 0;
    const originalFetch = window.fetch;
    window.fetch = function () {
        if (pendingRequests === 0) NProgress.start();
        pendingRequests++;
        return originalFetch.apply(this, arguments).finally(() => {
            pendingRequests--;
            if (pendingRequests === 0) NProgress.done();
        });
    };
})();
```

### 6.2 Index Template: `index.html`

#### Structure

- A two-column grid using Tailwind's responsive classes:
  - Left column (`lg:col-span-4`): Contains the search form.
  - Right column (`lg:col-span-8`): Contains the results container.

#### Search Form

- The form has `id="search-form"` and uses method GET (though submission is intercepted by JavaScript).
- Fields:
  - `query` (text input)
  - `number` (number input, min=1 max=50)
  - `type` (select dropdown with options from `types`)
  - `material` (select from `materials`)
  - A submit button and a "Random" button (link to `/random`).

#### Results Container

- Initially contains a placeholder `#initial-state` with a message prompting the user to search.
- The container has `id="results-container"`. It will be replaced with the HTML from `_results.html` after a search.

#### JavaScript: AJAX Search and Pagination

- **`loadResults(url)`**: 
  - Fetches the given URL with `X-Requested-With: XMLHttpRequest` header.
  - Shows a loading spinner while waiting.
  - On success, replaces `resultsContainer.innerHTML` with the response text.
  - Adds a `fade-in` class to each result card with staggered animation.
  - Updates browser history using `pushState`.
  - On error, displays a friendly error message inside the container.
- **Form submission**: Prevents default, constructs URL from form data, calls `loadResults`.
- **Pagination delegation**: Listens for clicks on elements with class `pagination-link` inside the results container, prevents default, and loads the URL from `href`.
- **popstate event**: When user navigates back/forward, if URL has a query, reload results; otherwise reload the page to reset to initial state.
- **Initial load**: On page load, if URL already contains `?query=...`, automatically load results (useful after refresh).

### 6.3 Partial Results Template: `_results.html`

This template is used only for AJAX responses; it does not extend `base.html`.

#### Conditional Rendering

- If `artworks` list is not empty:
  - Shows a header with total count and number displayed.
  - Renders a grid of artwork cards.
  - Includes pagination controls.
- If `artworks` is empty:
  - Shows a "No masterpieces found" message.

#### Artwork Grid

- Each card contains:
  - Image (`artwork.image`)
  - Title (`artwork.title`)
  - Origin (`artwork.origin` or "Unknown Origin")
  - Link to detail page (`url_for('artwork_detail', id=artwork.id)`)
- Hover effects: image scales, gradient overlay appears.

#### Pagination

- Shown only if `total > number`.
- Previous link: `offset - number` (only if `offset > 0`).
- Current page indicator: `(offset // number) + 1 / (total // number) + 1`.
- Next link: `offset + number` (only if `offset + number < total`).
- Uses the custom `exclude` filter to remove `offset` from current query args before adding the new offset, ensuring other filters persist.

### 6.4 Artwork Detail Template: `artwork.html`

Extends `base.html`.

- Provides a "Return to Gallery" link.
- Two-column layout:
  - Left: large image, catalog ID, share buttons (non-functional).
  - Right (sticky): title, origin and date badges, description, technique and dimensions cards, and a "Discover Random Artwork" button.
- Uses the passed `artwork` object to display all fields.

### 6.5 Error Template: `error.html`

Extends `base.html`.

- Displays a stylized error card with the error message passed as `error`.
- Buttons: "Return to Gallery" (goes to index) and "Retry Connection" (reloads current page).

---

## 7. Data Flow and Application Logic

### 7.1 Initial Page Load

1. User navigates to `/`.
2. Flask route `index()` renders `index.html` with filter lists.
3. Browser displays the search form and placeholder.
4. No API call is made yet.

### 7.2 Performing a Search (AJAX)

1. User fills the form and clicks "Search Gallery".
2. JavaScript intercepts submit, constructs URL with form data (e.g., `/search?query=mona&number=10&type=painting`).
3. `loadResults()` is called:
   - Shows loading spinner.
   - Fetches the URL with `X-Requested-With: XMLHttpRequest`.
4. Flask `/search` route:
   - Builds params, calls API.
   - Detects AJAX header, renders `_results.html` with the data.
5. Browser receives HTML, replaces `#results-container` content.
6. Results cards fade in.
7. Browser URL updates via `pushState`.

### 7.3 Pagination (AJAX)

1. User clicks "Next" or "Previous" link in the results.
2. Click event is captured by delegated listener on `#results-container`.
3. The link's `href` is used to call `loadResults()` (similar to search).
4. The process repeats: AJAX request to `/search` with new offset, returns updated partial.
5. The results container is replaced with new results; pagination links update accordingly.

### 7.4 Direct Access to Artwork Detail

1. User clicks "Explore Details" on a card, or navigates to `/artwork/123`.
2. Browser makes a full page request.
3. Flask route `/artwork/<id>` calls API for that artwork.
4. If success, renders `artwork.html` with full layout.
5. If error, renders `error.html`.

### 7.5 Random Artwork Redirect

1. User clicks the dice button on the search form or the "Discover Random Artwork" button on detail page.
2. Request goes to `/random`.
3. Flask calls `/random` API, gets an artwork ID, and redirects to its detail page.
4. Browser loads the detail page (full page load).

### 7.6 Error Handling Flow

- Any API call (in routes) may return an error dict.
- If error, the route renders `error.html` with the message.
- In AJAX context (search), the error is caught in `loadResults()` and displayed inline within the results container, not as a full error page. This keeps the user on the same page.

---

## 8. Key Features Explained

### 8.1 AJAX Navigation with NProgress

- All searches and pagination happen without full page reloads, providing a smooth single-page-app-like experience.
- NProgress shows a loading bar at the top of the page during AJAX requests, giving visual feedback.
- The `window.fetch` override ensures any fetch call (including those from our manual fetch) triggers NProgress.

### 8.2 Custom Jinja Filter for Pagination

- The `exclude` filter is crucial for preserving search filters when navigating pages.
- Without it, the `offset` parameter would be duplicated or lost.
- Example: If current URL is `/search?query=mona&type=painting&offset=10`, the "Previous" link should go to `offset=0` but keep `query` and `type`. The filter removes `offset` from `request.args` before adding the new offset.

### 8.3 Glassmorphism UI and Animations

- Custom CSS classes (`glass-card`, `thin-border`, `hover-glow`) create a modern, translucent aesthetic.
- Animations: cards fade in on load, hover effects, and smooth transitions.
- The background has subtle radial gradients for depth.

### 8.4 API Error Handling

- Comprehensive exception handling in `call_api` ensures the app never crashes due to network issues.
- User-friendly error messages are displayed either in a full error page or inline.
- HTTP status codes are mapped to specific messages (e.g., 401 for invalid API key).

---

## 9. Configuration and Customization

### 9.1 Changing the API Key

- Set the environment variable `ARTSEARCH_API_KEY` before running the app.
- If you want to permanently change the default fallback, edit the line in `app.py`:
  ```python
  API_KEY = os.environ.get('ARTSEARCH_API_KEY', 'your-new-default-key')
  ```

### 9.2 Modifying Filter Options

The lists `TYPES`, `MATERIALS`, `TECHNIQUES` are hardcoded in `app.py`. To add or remove options, edit these lists. Ensure they match the valid values accepted by the Artsearch API.

### 9.3 Adjusting Timeout or Retry Logic

In `call_api`, the timeout is set to 10 seconds. You can increase it if needed. For production, you might add retry logic with exponential backoff.

### 9.4 Changing UI Theme

- All colors are defined in the `<style>` section of `base.html` using CSS variables (`--bg-deep`, `--accent`, etc.). Modify these to change the overall theme.
- Tailwind classes can be adjusted directly in templates.

---

## 10. Deployment Considerations

- **Production Server**: Do not use `app.run(debug=True)`. Use a WSGI server like Gunicorn:
  ```bash
  pip install gunicorn
  gunicorn -w 4 app:app
  ```
- **Environment Variables**: Ensure `ARTSEARCH_API_KEY` is set in the production environment (e.g., via your hosting platform's config).
- **Static Assets**: The app currently uses CDNs for Tailwind and fonts. For offline or private deployment, you may want to download these assets and serve them locally.
- **Security**: The API key is exposed in the client-side JavaScript? No, all API calls are made server-side, so the key remains hidden.
- **Rate Limiting**: The Artsearch API may have rate limits. Consider adding caching or request throttling if needed.

---

## 11. Troubleshooting

| Problem | Possible Solution |
|---------|-------------------|
| **API key invalid** | Check that `ARTSEARCH_API_KEY` is set correctly. The default key may have been revoked or rate-limited. Obtain your own key. |
| **No results found** | Ensure your search query matches artworks in the database. Try a broad term like "painting". |
| **AJAX search not working** | Check browser console for errors. Ensure the server is running and accessible. Verify that the `X-Requested-With` header is being sent. |
| **Pagination links not preserving filters** | The `exclude` filter should be working. Verify that `request.args` contains all expected parameters when generating the link. |
| **Styling issues** | Make sure Tailwind CDN is accessible. If behind a firewall, download Tailwind locally. |
| **Random button redirects to error page** | The API may be down or the random endpoint may be temporarily unavailable. Check server logs. |

---

## 12. Conclusion

The Art Search Flask application demonstrates a clean integration with an external API, providing a responsive and visually appealing interface for exploring artworks. Its architecture separates concerns between backend API handling and frontend AJAX interactions, making it easy to extend or modify.

For further development, consider adding features like:
- User authentication and saved favorites.
- Advanced search with more filters.
- Image zoom or lightbox.
- Caching API responses to reduce latency.
- Unit tests for routes and API error handling.

This documentation covers every aspect of the current codebase. Use it as a reference for understanding, maintaining, or extending the application.