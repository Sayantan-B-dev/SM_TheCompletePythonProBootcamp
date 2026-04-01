# HTTP PATCH – Update a Cafe's Coffee Price

## 1. Endpoint Overview
The `/update-price/<int:cafe_id>` endpoint allows clients to update the `coffee_price` field of a specific cafe. This is a perfect demonstration of the PATCH method, as we are modifying only a single attribute of an existing resource. The client supplies the new price in the request body, and the server applies the change while leaving all other fields untouched.

### Use Case Example
A mobile app for remote workers might allow users to report price changes at their favorite cafes. The app could send a PATCH request with the updated price, keeping the database current without requiring the user to resubmit the entire cafe record.

## 2. Endpoint Design
- **URL**: `/update-price/<int:cafe_id>` – the cafe ID is part of the URL path.
- **HTTP Method**: `PATCH`
- **Request Body**: The client must provide the new coffee price. This can be sent as form data or JSON, but typically JSON is used. The field name should be `coffee_price`.
- **Response**:
  - **200 OK** – Success, with a confirmation message.
  - **404 Not Found** – If no cafe exists with the given ID.
  - **400 Bad Request** – If the request is missing the `coffee_price` field or the value is invalid.

## 3. Implementation Steps

### 3.1 Create the Route
In `main.py`, define a route with a variable part for the cafe ID:

```python
@app.route('/update-price/<int:cafe_id>', methods=['PATCH'])
def update_price(cafe_id):
    # logic goes here
```

The `<int:cafe_id>` syntax tells Flask to convert the path segment to an integer and pass it as the `cafe_id` argument to the function.

### 3.2 Retrieve the Cafe from the Database
Use SQLAlchemy to fetch the cafe by primary key. The `get_or_404` method is convenient: it returns the object if found, otherwise automatically aborts with a 404 response. However, to customize the error message, we can manually query and handle the `None` case.

```python
cafe = db.session.get(Cafe, cafe_id)
if not cafe:
    return jsonify({"error": "Cafe with that id not found."}), 404
```

Alternatively, using `Cafe.query.get(cafe_id)` works similarly.

### 3.3 Extract the New Price from the Request
The client may send the data as JSON or form-encoded. We'll support both for flexibility, but prioritize JSON.

```python
data = request.get_json()
if not data:
    data = request.form

new_price = data.get('coffee_price')
```

### 3.4 Validate the Input
The `coffee_price` field is required for this operation. If it's missing or empty, return a 400 error.

```python
if not new_price:
    return jsonify({"error": "Missing field: coffee_price"}), 400
```

Optionally, we could perform additional validation (e.g., ensure it's a string starting with '£' or matches a price format). For simplicity, we accept any string.

### 3.5 Update the Cafe and Commit
Assign the new value to the cafe object and commit the session.

```python
cafe.coffee_price = new_price
db.session.commit()
```

If any database error occurs, we should catch it and roll back, returning a 500 error.

### 3.6 Return Success Response
```python
return jsonify({"success": "Successfully updated the price."}), 200
```

We could also return the updated cafe object, but a simple success message suffices.

### 3.7 Complete Code for /update-price Endpoint

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

@app.route('/update-price/<int:cafe_id>', methods=['PATCH'])
def update_price(cafe_id):
    # Attempt to retrieve the cafe
    cafe = db.session.get(Cafe, cafe_id)
    if not cafe:
        return jsonify({"error": "Cafe with that id not found."}), 404

    # Get the new price from request
    data = request.get_json()
    if not data:
        data = request.form

    new_price = data.get('coffee_price')
    if not new_price:
        return jsonify({"error": "Missing field: coffee_price"}), 400

    # Update and commit
    try:
        cafe.coffee_price = new_price
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    return jsonify({"success": "Successfully updated the price."}), 200
```

## 4. Testing with Postman

### 4.1 Create a PATCH Request in Postman
1. Open Postman and create a new request.
2. Set method to **PATCH**.
3. Enter URL: `http://localhost:5000/update-price/1` (replace `1` with an existing cafe ID).
4. Go to the **Body** tab.
5. Select **x-www-form-urlencoded**.
6. Add key: `coffee_price`, value: `£3.50`.
7. Click **Send**.

**Expected Response**: Status `200 OK` with `{"success": "Successfully updated the price."}`.

### 4.2 Test with JSON Payload
Change the body type to **raw** and select **JSON**. Enter:
```json
{
    "coffee_price": "£4.00"
}
```
Send. Should succeed.

### 4.3 Test with Invalid ID
Change the URL to `/update-price/9999` (assuming no such ID). Send. Should receive `404 Not Found` with error message.

### 4.4 Test with Missing Field
Remove the `coffee_price` key from the body. Send. Should receive `400 Bad Request`.

### 4.5 Save to Collection
Save this request as **Update Coffee Price** in your Postman collection. Add a description: "Updates the coffee price for a specific cafe. Provide the new price in the `coffee_price` field."

## 5. Edge Cases and Error Handling

### 5.1 Cafe Not Found
If the client provides an ID that doesn't exist, we return a 404 with a clear message. This is consistent with REST principles: the resource was not found, so the operation cannot be performed.

### 5.2 Missing `coffee_price` Field
The endpoint is designed specifically to update the price, so if the field is absent, it's a bad request. We return 400.

### 5.3 Empty String or Whitespace
If the client sends an empty string or only whitespace, our validation `if not new_price` will treat it as missing. This is acceptable. However, if we want to allow empty string as a valid price (unlikely), we could change the validation. For this API, an empty string is probably not a meaningful price, so rejecting it is fine.

### 5.4 Database Errors
Any exception during commit (e.g., database locked, integrity error) is caught, rolled back, and a 500 error is returned. In production, you might want to log the error and return a generic message.

### 5.5 Handling Other Fields
This endpoint only updates `coffee_price`. If the client accidentally includes other fields (e.g., `name`), they are ignored because we only extract `coffee_price`. This is a design choice. Alternatively, we could reject requests containing extra fields to enforce that only the price can be updated here.

## 6. Why PATCH and Not PUT?
- The client only wants to change one field. Using PUT would require sending the entire cafe object, which is unnecessary and could lead to accidental data loss if other fields are omitted.
- PATCH is semantically correct for partial updates.
- The endpoint is idempotent: sending the same price multiple times results in the same state.

## 7. What We Learned
- How to create a PATCH endpoint that updates a specific field.
- Extracting the cafe ID from the URL using variable rules.
- Using `db.session.get()` to retrieve an object by primary key.
- Handling the case where the object does not exist.
- Validating request data and returning appropriate HTTP status codes.
- The importance of committing changes to the database.
- Testing PATCH requests with Postman using both form data and JSON.
