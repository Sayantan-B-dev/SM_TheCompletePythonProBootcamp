# HTTP POST – Adding a New Cafe

## 1. Endpoint Overview
The POST endpoint allows clients to add a new cafe to the database. This is a critical write operation that enables data contributions, such as a user-submitted cafe suggestion feature. The endpoint accepts data in the request body (form-encoded or JSON) and creates a new record in the `cafe` table.

### Use Case Example
A website like `laptopfriendly.co` provides a "Suggest a Cafe" form. When a user fills out the form and submits, the frontend sends a POST request to the API with the cafe details, and the new cafe becomes part of the directory.

## 2. Endpoint Design
- **URL**: `/` or `/add` (both are acceptable; we'll use `/add` for clarity)
- **HTTP Method**: `POST`
- **Request Body**: The client must send all required fields. The body can be `application/x-www-form-urlencoded` (simulating an HTML form) or `application/json`. The server should handle both.
- **Response**: On success, returns a `201 Created` status with the newly created cafe object (including its generated ID). On failure, returns appropriate error status (`400 Bad Request`) with a message.

## 3. Implementation Steps

### 3.1 Create the Route
In `main.py`, define a new route `/add` that accepts POST requests:

```python
@app.route('/add', methods=['POST'])
def add_cafe():
    # logic goes here
```

### 3.2 Extract Data from the Request
Flask provides `request.form` for form-encoded data and `request.get_json()` for JSON. To support both, we can check the `Content-Type` header, but a simpler approach is to try JSON first, then fall back to form. However, for clarity, we can design the endpoint to accept form data (as that's what Postman's "x-www-form-urlencoded" sends) and also document that JSON is acceptable.

```python
def add_cafe():
    # Try to get JSON data first
    data = request.get_json()
    if not data:
        # If not JSON, try form data
        data = request.form
```

`request.form` is a `MultiDict` that behaves like a dictionary. We can access values using `data.get('field_name')`.

### 3.3 Validate Required Fields
All fields in the `cafe` table are required except `coffee_price` (nullable). The fields are: `name`, `map_url`, `img_url`, `location`, `has_sockets`, `has_toilet`, `has_wifi`, `can_take_calls`, `seats`, `coffee_price`. We should check that each field exists and is not empty. Boolean fields may come as strings ("true"/"false") or "1"/"0", so we need to convert them appropriately.

```python
required_fields = ['name', 'map_url', 'img_url', 'location', 'has_sockets', 'has_toilet', 'has_wifi', 'can_take_calls', 'seats']
for field in required_fields:
    if not data.get(field):
        return jsonify({"error": f"Missing required field: {field}"}), 400
```

### 3.4 Convert Boolean Fields
HTML forms send boolean values as strings. We need to convert them to Python booleans. For example:

```python
def str_to_bool(value):
    if isinstance(value, bool):
        return value
    return value.lower() in ['true', '1', 'yes', 'on']
```

Apply to each boolean field:

```python
has_sockets = str_to_bool(data.get('has_sockets'))
has_toilet = str_to_bool(data.get('has_toilet'))
has_wifi = str_to_bool(data.get('has_wifi'))
can_take_calls = str_to_bool(data.get('can_take_calls'))
```

### 3.5 Create a New Cafe Object
Instantiate a `Cafe` model instance with the extracted data:

```python
new_cafe = Cafe(
    name=data['name'],
    map_url=data['map_url'],
    img_url=data['img_url'],
    location=data['location'],
    has_sockets=has_sockets,
    has_toilet=has_toilet,
    has_wifi=has_wifi,
    can_take_calls=can_take_calls,
    seats=data['seats'],
    coffee_price=data.get('coffee_price')  # optional, may be None
)
```

### 3.6 Add to Database and Commit
Add the new object to the session and commit:

```python
db.session.add(new_cafe)
db.session.commit()
```

After commit, `new_cafe.id` will be populated with the auto-generated ID.

### 3.7 Return Success Response
Return the new cafe as JSON with status `201 Created`:

```python
return jsonify(new_cafe.to_dict()), 201
```

If any exception occurs during database operations, we should roll back and return a 500 error. In development, we can let it propagate, but for production we would wrap in try/except.

### 3.8 Complete Code for /add Endpoint

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

def str_to_bool(value):
    if isinstance(value, bool):
        return value
    return str(value).lower() in ['true', '1', 'yes', 'on']

@app.route('/add', methods=['POST'])
def add_cafe():
    # Try to get JSON data; fallback to form data
    data = request.get_json()
    if not data:
        data = request.form

    # Validate required fields
    required_fields = ['name', 'map_url', 'img_url', 'location', 'has_sockets', 'has_toilet', 'has_wifi', 'can_take_calls', 'seats']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Convert boolean fields
    try:
        has_sockets = str_to_bool(data['has_sockets'])
        has_toilet = str_to_bool(data['has_toilet'])
        has_wifi = str_to_bool(data['has_wifi'])
        can_take_calls = str_to_bool(data['can_take_calls'])
    except Exception:
        return jsonify({"error": "Invalid boolean value for one of the amenities fields."}), 400

    # Create new cafe object
    new_cafe = Cafe(
        name=data['name'],
        map_url=data['map_url'],
        img_url=data['img_url'],
        location=data['location'],
        has_sockets=has_sockets,
        has_toilet=has_toilet,
        has_wifi=has_wifi,
        can_take_calls=can_take_calls,
        seats=data['seats'],
        coffee_price=data.get('coffee_price')
    )

    try:
        db.session.add(new_cafe)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error: " + str(e)}), 500

    return jsonify(new_cafe.to_dict()), 201
```

## 4. Testing with Postman

### 4.1 Create a POST Request in Postman
1. Open Postman and create a new request.
2. Set method to **POST**.
3. Enter URL: `http://localhost:5000/add`.
4. Go to the **Body** tab.
5. Select **x-www-form-urlencoded**.
6. Enter the key-value pairs as shown in the table below:

| Key              | Value                             |
|------------------|-----------------------------------|
| name             | New Test Cafe                     |
| map_url          | https://goo.gl/maps/test          |
| img_url          | https://example.com/test.jpg      |
| location         | Test Location                     |
| has_sockets      | true                              |
| has_toilet       | false                             |
| has_wifi         | true                              |
| can_take_calls   | false                             |
| seats            | 20-30                             |
| coffee_price     | £2.95                             |

7. Click **Send**.

**Expected Response**: Status `201 Created` with the new cafe object, including an `id` field (e.g., `"id": 42`).

### 4.2 Test with Missing Fields
Remove one of the required keys (e.g., `name`) and send the request. You should receive a `400 Bad Request` with an error message indicating the missing field.

### 4.3 Test with JSON Payload
In a new tab, set method POST, same URL. Go to Body, select **raw** and set type to **JSON**. Enter:

```json
{
    "name": "JSON Cafe",
    "map_url": "https://goo.gl/maps/json",
    "img_url": "https://example.com/json.jpg",
    "location": "JSON Area",
    "has_sockets": true,
    "has_toilet": false,
    "has_wifi": true,
    "can_take_calls": true,
    "seats": "10-20",
    "coffee_price": "£3.00"
}
```

Send. Should succeed with 201. This confirms that both form-urlencoded and JSON are accepted.

### 4.4 Save to Collection
Save this request as **Add New Cafe** in your Postman collection. Add a description: "Creates a new cafe record. Required fields: name, map_url, img_url, location, has_sockets, has_toilet, has_wifi, can_take_calls, seats. coffee_price is optional."

## 5. Edge Cases and Error Handling

### 5.1 Duplicate Cafe Name
The `name` field has a `unique=True` constraint. If a client tries to add a cafe with a name that already exists, the database will raise an `IntegrityError`. Our try/except block will catch it and return a 500 error, but we could provide a more specific error message by checking for that exception type. For simplicity, we return a generic database error. In a production API, you would catch `sqlalchemy.exc.IntegrityError` and respond with a 409 Conflict or 400 with a message like "A cafe with that name already exists."

### 5.2 Invalid Boolean Strings
If the client sends a non-boolean value (e.g., "maybe"), our `str_to_bool` function will treat it as `False` because it only checks for truthy strings. To be safe, we can add validation that the string must be one of the accepted values. Alternatively, we could accept only `true`/`false` and reject others. Our implementation will convert anything not in the truthy set to `False`, which may be misleading. Better to strictly validate.

Improved boolean conversion with validation:

```python
def parse_bool(value):
    if isinstance(value, bool):
        return value
    if value is None:
        return False  # or raise error, depending on requirement
    lower_val = str(value).lower()
    if lower_val in ['true', '1', 'yes', 'on']:
        return True
    if lower_val in ['false', '0', 'no', 'off']:
        return False
    raise ValueError(f"Invalid boolean value: {value}")
```

Then catch `ValueError` and return 400.

### 5.3 Missing Optional Field
`coffee_price` is nullable, so omitting it is fine. Our code uses `data.get('coffee_price')`, which will be `None` if not present. That's acceptable.

### 5.4 Empty Strings
If the client sends an empty string for a required field, our validation `if not data.get(field)` will treat it as missing. That's appropriate. However, for `coffee_price`, an empty string might be considered as `None` or an empty string. Our code stores it as an empty string if present. We could convert empty string to `None` for consistency, but it's not required.

### 5.5 Database Commit Failure
Any other database error (e.g., connection lost) will be caught, rolled back, and a 500 error returned. This prevents the database from being left in an inconsistent state.

## 6. What We Learned

- How to handle POST requests in Flask, extracting data from both form-urlencoded and JSON payloads.
- The importance of validating required fields before attempting to create a database record.
- Converting string representations of booleans to Python booleans for model fields.
- Adding a new record to the database using SQLAlchemy's session management.
- Returning a `201 Created` status code along with the newly created resource.
- Using `try/except` to handle database exceptions and roll back on failure.
- Testing POST requests with Postman, including both form and JSON data.

## 7. Next Steps

With the POST endpoint implemented, the API now supports creating new resources. The following lessons will introduce the PATCH method for updating existing cafes (specifically the coffee price) and the DELETE method for removing cafes, including authentication via an API key. These will complete the CRUD operations for the Cafe & Wifi API.

After implementing all endpoints, we will use Postman to generate comprehensive documentation and link it from the project's index page.