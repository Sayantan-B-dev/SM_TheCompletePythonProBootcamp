# HTTP GET – All Cafes Endpoint

## 1. Endpoint Overview
The `/all` endpoint returns a complete list of all cafes stored in the database. This is a fundamental read operation for clients that need to display a directory or index of available cafes. The response is a JSON array containing each cafe's full details.

### Use Case Example
A website like `laptopfriendly.co` could use this endpoint to populate a searchable, filterable list of cafes. The client can then render the list and allow users to browse.

## 2. Implementation Steps

### 2.1 Create the Route
In `main.py`, define a new route with the GET method:

```python
@app.route('/all', methods=['GET'])
def get_all_cafes():
    # logic goes here
```

### 2.2 Query All Cafes from the Database
Using SQLAlchemy's query interface, retrieve every record from the `cafe` table:

```python
cafes = db.session.execute(db.select(Cafe)).scalars().all()
```

Alternatively, the simpler and more common approach is:

```python
cafes = Cafe.query.all()
```

Both achieve the same result. The first uses the modern SQLAlchemy 2.0 style with `select()`, while the second is the legacy (but still widely used) `query` interface. For consistency with future lessons, we can use either.

`Cafe.query.all()` returns a list of `Cafe` objects.

### 2.3 Serialize the List of Cafes
Each `Cafe` object must be converted to a dictionary so that the entire list can be JSON-serialized. Using the `to_dict()` method defined in the model, we can map each object:

```python
cafes_list = [cafe.to_dict() for cafe in cafes]
```

This creates a list of dictionaries.

### 2.4 Return JSON Response
Pass the list to `jsonify()`:

```python
return jsonify(cafes_list)
```

By default, Flask will set the status code to `200 OK`.

### 2.5 Complete Code for /all Endpoint

```python
from flask import Flask, jsonify
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

@app.route('/all', methods=['GET'])
def get_all_cafes():
    """Return all cafes as a JSON list."""
    cafes = Cafe.query.all()
    return jsonify([cafe.to_dict() for cafe in cafes])

if __name__ == '__main__':
    app.run(debug=True)
```

### 2.6 Handling an Empty Database
If the database contains no records, `Cafe.query.all()` returns an empty list. The list comprehension will also produce an empty list, and `jsonify([])` will return a valid JSON array `[]`. This is acceptable – an empty collection is a valid response. No special error handling is needed, but you might optionally return a `404` if you consider an empty database to be an error state. However, that would violate REST conventions because the resource "all cafes" exists even if it is empty. A `200 OK` with an empty array is the appropriate response.

## 3. Testing the Endpoint

### 3.1 Using a Web Browser
Visit `http://127.0.0.1:5000/all` in a browser. The browser will display a JSON array containing all cafe objects. If you have a JSON viewer extension, it will format nicely; otherwise, you'll see raw JSON.

### 3.2 Using Postman
Create a new GET request to `http://127.0.0.1:5000/all`. Save it in your collection (e.g., "Cafe & Wifi" collection) for future use. You can add a description like "Retrieve all cafes". Test that the response is a JSON array and each object has the expected fields.

### 3.3 Using curl
```bash
curl http://127.0.0.1:5000/all
```

## 4. Pagination Considerations

Returning all records in one response works well for small datasets (like the provided cafes.db with a handful of cafes). However, as the database grows, returning hundreds or thousands of cafes in a single request can cause performance issues for both server and client. It also consumes more bandwidth.

A robust API should implement **pagination**. Common approaches:

- **Offset-based pagination**: Use `?page=2&per_page=20` query parameters.
- **Cursor-based pagination**: Use a unique, sequential column (like `id`) with `?after_id=100&limit=20`.

Example implementation with offset pagination:

```python
@app.route('/all', methods=['GET'])
def get_all_cafes_paginated():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    cafes = Cafe.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        "cafes": [cafe.to_dict() for cafe in cafes.items],
        "total": cafes.total,
        "page": cafes.page,
        "pages": cafes.pages,
        "per_page": cafes.per_page
    })
```

For the initial version, we omit pagination for simplicity, but it is a recommended enhancement for production APIs.

## 5. SQLAlchemy Query Details

### 5.1 Using `all()`
`Cafe.query.all()` executes the query and returns a list of model instances. Internally, it issues a `SELECT * FROM cafe` statement.

### 5.2 Using `select()` and `scalars()`
The modern SQLAlchemy 2.0 style uses `select()` to build a query, then `execute()` and `scalars().all()`:

```python
stmt = db.select(Cafe).order_by(Cafe.name)  # optional ordering
cafes = db.session.execute(stmt).scalars().all()
```

`scalars()` extracts the first column of each row (the Cafe object), and `all()` returns them as a list. This approach is more explicit and works well with complex queries.

### 5.3 Ordering
You may want to return cafes in a specific order, such as by name or location. Add `.order_by()` to the query:

```python
cafes = Cafe.query.order_by(Cafe.name).all()
```

or with select:

```python
stmt = db.select(Cafe).order_by(Cafe.name)
cafes = db.session.execute(stmt).scalars().all()
```

Ordering improves the user experience and makes the list predictable.

## 6. Serialization of Lists

The list comprehension `[cafe.to_dict() for cafe in cafes]` is a concise way to transform a list of objects into a list of dictionaries. The resulting list is passed to `jsonify()`, which converts it to a JSON array. The JSON array will look like:

```json
[
  {
    "id": 1,
    "name": "The Attendant",
    "map_url": "https://goo.gl/maps/...",
    ...
  },
  {
    "id": 2,
    "name": "Workshop Coffee",
    ...
  }
]
```

## 7. Error Handling and Edge Cases

- **Database Connection Issues**: If the database cannot be accessed, SQLAlchemy will raise an exception. In production, you would want to catch such exceptions and return a `500 Internal Server Error` with a generic message. For development, leaving the exception uncaught provides useful debugging information.
- **Empty List**: As mentioned, an empty list is returned as `[]` with status `200`. No error needed.

## 8. What We Learned

- How to retrieve all records from a database table using SQLAlchemy.
- How to serialize a list of model instances to JSON using `to_dict()` and list comprehension.
- The importance of returning JSON arrays for collection resources.
- Considerations for pagination in scalable APIs.
- Differences between SQLAlchemy query styles.

## 9. Next Steps

The following lesson (463) will introduce the `/search` endpoint, which allows filtering cafes by location using query parameters. This adds flexibility to the API and demonstrates handling of optional parameters.

We have now implemented two GET endpoints: `/random` (single resource) and `/all` (collection). Together they form the read-only part of the API. The next endpoints will cover creation (POST), modification (PATCH), and deletion (DELETE), building a complete CRUD interface.