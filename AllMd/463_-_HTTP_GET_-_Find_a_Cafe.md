# HTTP GET – Search Cafes by Location

## 1. Endpoint Overview
The `/search` endpoint allows clients to retrieve cafes located in a specific area. By providing a `loc` query parameter (short for "location"), users can filter the cafe list to only those matching the given area. This is a common requirement for applications that need to display cafes near a user or within a chosen neighborhood.

### Use Case Example
A front-end application might present a dropdown of popular London areas. When the user selects "Shoreditch", the app makes a GET request to `/search?loc=Shoreditch` and displays the resulting cafes on a map or in a list.

## 2. Implementation Steps

### 2.1 Create the Route
Define a new route `/search` that accepts GET requests:

```python
@app.route('/search', methods=['GET'])
def search_cafe():
    # logic will go here
```

### 2.2 Extract the Query Parameter
The location value is provided as a query string parameter named `loc`. Use `request.args.get()` to retrieve it:

```python
location = request.args.get('loc')
```

If the client omits the `loc` parameter, `location` will be `None`. We must decide how to handle this: return an error or default behavior. A RESTful approach is to return a `400 Bad Request` indicating that a location is required.

### 2.3 Build the Database Query
We need to find all cafes whose `location` field matches the provided value. The `location` column stores strings like "Shoreditch", "Covent Garden", etc. We can use SQLAlchemy's `filter()` or `filter_by()`.

**Option A: Exact match using `filter_by`** (case-sensitive and exact)
```python
cafes = Cafe.query.filter_by(location=location).all()
```

**Option B: Case-insensitive partial match using `ilike`** (more user-friendly)
```python
cafes = Cafe.query.filter(Cafe.location.ilike(f"%{location}%")).all()
```

The `ilike` approach allows users to input partial names (e.g., "shire" for "Shoreditch") and ignores case differences. This improves usability but may return more results. For a simple search, exact match might suffice. The original challenge likely expects exact match on the location field. We'll implement exact match but also discuss alternatives.

### 2.4 Handle No Results
If the query returns an empty list, there are no cafes in that location. We should return a `404 Not Found` with an informative error message:

```python
if not cafes:
    return jsonify({"error": "No cafes found in that location."}), 404
```

### 2.5 Serialize and Return Results
If cafes are found, convert each to a dictionary and return as a JSON array:

```python
return jsonify([cafe.to_dict() for cafe in cafes])
```

### 2.6 Complete Code for /search Endpoint

```python
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

@app.route('/search', methods=['GET'])
def search_cafe():
    """Return cafes matching the given location."""
    location = request.args.get('loc')
    if not location:
        return jsonify({"error": "Missing 'loc' query parameter."}), 400

    cafes = Cafe.query.filter_by(location=location).all()
    if cafes:
        return jsonify([cafe.to_dict() for cafe in cafes])
    else:
        return jsonify({"error": "No cafes found in that location."}), 404

if __name__ == '__main__':
    app.run(debug=True)
```

## 3. Testing the Endpoint

### 3.1 Using a Web Browser
Start the Flask server and visit a URL with the query parameter, for example:

```
http://127.0.0.1:5000/search?loc=Shoreditch
```

If there are cafes with location exactly "Shoreditch", you'll see a JSON array. If not, you'll see the error JSON with status 404. The browser will display the JSON directly.

### 3.2 Using Postman
- Create a new GET request to `http://127.0.0.1:5000/search`.
- Add a query parameter: key `loc`, value e.g., "Shoreditch".
- Send the request. Observe the response and status code.
- Test with a location that exists (from the database) and one that does not.
- Test without providing the `loc` parameter to see the 400 error.

Save this request to your Postman collection, naming it "Search Cafes by Location".

### 3.3 Using curl
```bash
curl "http://127.0.0.1:5000/search?loc=Shoreditch"
curl "http://127.0.0.1:5000/search?loc=UnknownPlace"
curl "http://127.0.0.1:5000/search"  # missing loc
```

## 4. Advanced Filtering Options

### 4.1 Case-Insensitive Search with `ilike`
To make the search more flexible, replace `filter_by` with `filter` and `ilike`:

```python
cafes = Cafe.query.filter(Cafe.location.ilike(f"%{location}%")).all()
```

This will match any cafe whose location contains the input string, ignoring case. For example, `loc=shire` would match "Shoreditch". Be aware that this may return broader results.

### 4.2 Exact but Case-Insensitive Match
If you want exact match but ignoring case, use `func.lower()`:

```python
from sqlalchemy import func
cafes = Cafe.query.filter(func.lower(Cafe.location) == func.lower(location)).all()
```

### 4.3 Handling Multiple Query Parameters
Future enhancements might include filtering by amenities (e.g., `has_wifi=true`). You can extend the query by conditionally adding filters:

```python
query = Cafe.query
if location:
    query = query.filter_by(location=location)
if has_wifi:
    query = query.filter_by(has_wifi=True)
cafes = query.all()
```

## 5. Error Handling and Edge Cases

### 5.1 Missing `loc` Parameter
Returning a `400 Bad Request` is appropriate because the client failed to provide a required parameter. The error message should clearly indicate what is missing.

### 5.2 Empty String Parameter
If the client sends `?loc=` (empty string), `request.args.get('loc')` returns an empty string. You may choose to treat this as a missing parameter (error) or as a wildcard (return all). Our implementation currently treats empty string as a valid location, but likely no cafe has an empty location, so it will result in 404. It's better to check for empty string and return a 400 as well:

```python
if not location or location.strip() == "":
    return jsonify({"error": "Location query parameter cannot be empty."}), 400
```

### 5.3 Database Errors
If the database query fails due to connection issues, an exception will be raised. In production, you would catch exceptions and return a 500 error. For development, letting the exception propagate is acceptable for debugging.

## 6. What We Learned

- How to access query parameters using `request.args.get()`.
- How to filter SQLAlchemy queries using `filter_by` and `filter`.
- Returning multiple results as a JSON array.
- Proper use of HTTP status codes for missing parameters (400) and no results (404).
- Handling optional search parameters and designing flexible search endpoints.
- Testing with various tools and edge cases.

## 7. Next Steps

The following lessons will introduce POST, PATCH, and DELETE methods, allowing clients to modify the database. The `/search` endpoint completes the GET operations for this API. With `/random`, `/all`, and `/search`, clients can retrieve data in multiple ways. The next file (464) covers Postman, a tool for API testing and documentation. Then we'll move to creating new cafes with POST.