# HTTP GET – Random Cafe Endpoint

## 1. Endpoint Overview
The `/random` endpoint is designed to return a single cafe selected at random from the database. This is a common requirement for applications that want to suggest a cafe to users, such as a "surprise me" feature. The endpoint responds to GET requests and returns a JSON representation of the chosen cafe.

### Use Case Example
A mobile app could call this endpoint whenever the user taps a "Random Cafe" button, displaying the returned cafe's details.

## 2. Implementation Steps

### 2.1 Create the Route
In `main.py`, define a new route with the appropriate decorator:

```python
@app.route('/random', methods=['GET'])
def get_random_cafe():
    # logic will go here
```

### 2.2 Query a Random Cafe from the Database
Using SQLAlchemy, we can fetch a random record. Different database engines have different functions for randomness. SQLite supports `func.random()` from SQLAlchemy's `func` object.

```python
from sqlalchemy import func

cafe = Cafe.query.order_by(func.random()).first()
```

If the database is empty, `cafe` will be `None`. We should handle that case gracefully.

### 2.3 Serialize the Cafe Object to JSON
The `Cafe` model instance cannot be directly returned by Flask; it must be converted to a JSON-serializable format (dictionary or list). Two common approaches:

#### Approach A: Manual Dictionary Construction
Create a dictionary manually, selecting only the fields you want:

```python
if cafe:
    cafe_dict = {
        "id": cafe.id,
        "name": cafe.name,
        "map_url": cafe.map_url,
        "img_url": cafe.img_url,
        "location": cafe.location,
        "has_sockets": cafe.has_sockets,
        "has_toilet": cafe.has_toilet,
        "has_wifi": cafe.has_wifi,
        "can_take_calls": cafe.can_take_calls,
        "seats": cafe.seats,
        "coffee_price": cafe.coffee_price
    }
else:
    cafe_dict = {"error": "No cafes found"}
```

#### Approach B: Use a Model Method (to_dict)
The provided `Cafe` model already includes a `to_dict()` method that automatically converts all columns to a dictionary:

```python
def to_dict(self):
    return {column.name: getattr(self, column.name) for column in self.__table__.columns}
```

This method uses introspection to fetch all column names and values, producing a complete dictionary representation. This is concise and maintainable.

```python
cafe_dict = cafe.to_dict() if cafe else {"error": "No cafes found"}
```

### 2.4 Return JSON Response with jsonify
Flask's `jsonify()` function converts a dictionary to a JSON response with the appropriate `Content-Type` header.

```python
from flask import jsonify

if cafe:
    return jsonify(cafe.to_dict())
else:
    return jsonify({"error": "No cafes found"}), 404
```

Note the use of HTTP status code `404 Not Found` when the database is empty. This provides meaningful feedback to the client.

### 2.5 Complete Code for /random Endpoint

```python
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

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

@app.route('/random', methods=['GET'])
def get_random_cafe():
    """Return a random cafe from the database."""
    cafe = Cafe.query.order_by(func.random()).first()
    if cafe:
        return jsonify(cafe.to_dict())
    else:
        return jsonify({"error": "No cafes found in the database"}), 404

if __name__ == '__main__':
    app.run(debug=True)
```

## 3. Testing the Endpoint

### 3.1 Using a Web Browser
Run the Flask application and navigate to `http://127.0.0.1:5000/random`. The browser will display the JSON response. Each refresh should return a different cafe (assuming there are multiple records).

### 3.2 Using Postman
Open Postman, create a new GET request to `http://127.0.0.1:5000/random`, and send. The response will be shown in the body pane. You can save this request to a collection for future testing.

### 3.3 Using curl
```bash
curl http://127.0.0.1:5000/random
```

## 4. Understanding Serialization
Serialization is the process of converting an object (like a SQLAlchemy model instance) into a format that can be easily transmitted over HTTP, typically JSON. Flask's `jsonify()` handles the conversion of Python dictionaries to JSON strings and sets the correct `Content-Type: application/json` header.

The `to_dict()` method leverages SQLAlchemy's introspection to dynamically create a dictionary containing all column values. This approach is flexible: if the model changes (columns added/removed), `to_dict()` automatically reflects those changes, reducing maintenance overhead.

Alternatively, you could manually construct a dictionary to:
- Omit sensitive fields (none in this case).
- Rename keys.
- Include computed properties.
- Nest related data (e.g., if cafes had reviews).

For the current API, the complete representation is appropriate.

## 5. Handling Edge Cases

### 5.1 Empty Database
If there are no cafes in the database, `Cafe.query.order_by(func.random()).first()` returns `None`. The code explicitly checks for this and returns a `404 Not Found` with an error message. This is more informative than returning an empty object or a `200 OK` with `null`.

### 5.2 Database Random Function Compatibility
Using `func.random()` works with SQLite. For PostgreSQL, you would use `func.random()` as well (but the function name might differ in some databases). MySQL uses `func.rand()`. To make the code more portable, you could use database-agnostic approaches like fetching all IDs and picking one randomly in Python, but that is less efficient for large tables. Since we are using SQLite, `func.random()` is perfectly acceptable.

## 6. What We Achieved
- Created a new GET endpoint `/random`.
- Learned to query a random record using SQLAlchemy's `order_by(func.random())`.
- Implemented serialization using a model method (`to_dict()`) and `jsonify()`.
- Handled the empty database case with proper HTTP status codes.
- Tested the endpoint using browser, Postman, or curl.

## 7. Next Steps
The following lessons will expand the API with:
- `/all` – retrieve all cafes.
- `/search` – filter cafes by location.
- POST – add a new cafe.
- PATCH – update a cafe's coffee price.
- DELETE – remove a cafe (with API key authentication).

Each endpoint will build on the concepts introduced here: routing, database queries, serialization, and error handling.