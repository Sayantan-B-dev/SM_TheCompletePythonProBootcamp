# HTTP DELETE – Remove a Cafe from the Database

## 1. Endpoint Overview
The `/report-closed/<int:cafe_id>` endpoint allows authorized clients to delete a cafe record from the database. This operation is irreversible and should be protected to prevent accidental or malicious data loss. Therefore, the endpoint requires an **API key** as a query parameter for authentication. Only requests that include the correct API key will be permitted to delete a cafe.

### Use Case Example
A community-maintained cafe directory might allow trusted moderators or administrators to remove cafes that have permanently closed. The moderator's application includes the secret API key in the request to prove authorization. Once verified, the cafe is removed from the database.

## 2. Endpoint Design
- **URL**: `/report-closed/<int:cafe_id>` – the cafe ID is part of the URL path.
- **HTTP Method**: `DELETE`
- **Authentication**: The client must provide an `api-key` query parameter with the value `TopSecretAPIKey`. (In a real-world API, this key would be kept secret, possibly stored in environment variables, and rotated regularly.)
- **Response**:
  - **200 OK** – Cafe successfully deleted, with a confirmation message.
  - **403 Forbidden** – If the API key is missing or incorrect.
  - **404 Not Found** – If no cafe exists with the given ID.
  - **500 Internal Server Error** – If a database error occurs during deletion.

## 3. Security Considerations
DELETE operations modify data and can cause permanent loss. To secure such endpoints, common practices include:
- Requiring authentication (API key, OAuth token, etc.).
- Restricting DELETE access to specific user roles (admin, moderator).
- Logging deletion events for audit trails.
- Using HTTPS to prevent API key exposure.

In this API, we use a simple static API key for demonstration. In production, you would likely use more robust mechanisms like OAuth2 or JWTs, and the key would never be hardcoded but stored in environment variables.

## 4. Implementation Steps

### 4.1 Create the Route
In `main.py`, define a DELETE route with a variable for the cafe ID:

```python
@app.route('/report-closed/<int:cafe_id>', methods=['DELETE'])
def delete_cafe(cafe_id):
    # logic goes here
```

### 4.2 Extract and Validate the API Key
The API key is expected as a query parameter named `api-key`. Retrieve it using `request.args.get('api-key')`. Compare it to the expected secret. If it's missing or incorrect, return a 403 Forbidden response.

```python
api_key = request.args.get('api-key')
if api_key != "TopSecretAPIKey":
    return jsonify({"error": "You are not authorized to delete. Please provide the correct api-key."}), 403
```

**Note**: Hardcoding secrets in code is insecure. In a real project, store the key in an environment variable and access it via `os.environ.get('API_KEY')`.

### 4.3 Retrieve the Cafe from the Database
Fetch the cafe by ID. If not found, return 404.

```python
cafe = db.session.get(Cafe, cafe_id)
if not cafe:
    return jsonify({"error": "Cafe with that id not found."}), 404
```

### 4.4 Delete the Cafe and Commit
Use `db.session.delete(cafe)` to mark the object for deletion, then commit the transaction.

```python
try:
    db.session.delete(cafe)
    db.session.commit()
except Exception as e:
    db.session.rollback()
    return jsonify({"error": f"Database error: {str(e)}"}), 500
```

### 4.5 Return Success Response
```python
return jsonify({"success": "Cafe deleted successfully."}), 200
```

### 4.6 Complete Code for DELETE Endpoint

```python
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

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

# In production, load from environment variable: os.environ.get('API_KEY', 'default-fallback')
API_KEY = "TopSecretAPIKey"

@app.route('/report-closed/<int:cafe_id>', methods=['DELETE'])
def delete_cafe(cafe_id):
    # Check API key
    provided_key = request.args.get('api-key')
    if provided_key != API_KEY:
        return jsonify({"error": "You are not authorized to delete. Please provide the correct api-key."}), 403

    # Find cafe
    cafe = db.session.get(Cafe, cafe_id)
    if not cafe:
        return jsonify({"error": "Cafe with that id not found."}), 404

    # Delete and commit
    try:
        db.session.delete(cafe)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    return jsonify({"success": "Cafe deleted successfully."}), 200
```

## 5. Testing with Postman

### 5.1 Create a DELETE Request
1. Open Postman and create a new request.
2. Set method to **DELETE**.
3. Enter URL: `http://localhost:5000/report-closed/1` (replace `1` with an existing cafe ID).
4. Add a query parameter:
   - Key: `api-key`
   - Value: `TopSecretAPIKey`
   The URL will become `http://localhost:5000/report-closed/1?api-key=TopSecretAPIKey`.
5. Click **Send**.

**Expected Response**: Status `200 OK` with `{"success": "Cafe deleted successfully."}`.

### 5.2 Test with Incorrect API Key
Change the `api-key` value to something else, e.g., `wrong-key`. Send.

**Expected Response**: Status `403 Forbidden` with error message.

### 5.3 Test with Non-Existent ID
Change the URL to `/report-closed/9999` with correct API key. Send.

**Expected Response**: Status `404 Not Found` with error message.

### 5.4 Test Without API Key
Remove the query parameter entirely. Send.

**Expected Response**: Status `403 Forbidden` (since `provided_key` will be `None` and fail the comparison).

### 5.5 Save to Collection
Save this request as **Delete Closed Cafe** in your Postman collection. Add a description: "Deletes a cafe record. Requires the correct `api-key` query parameter. Use with caution."

## 6. Edge Cases and Error Handling

### 6.1 API Key Missing or Invalid
We return `403 Forbidden` (not `401 Unauthorized`) because the request lacks valid authentication credentials. The distinction:
- `401 Unauthorized` typically means the client must authenticate (e.g., provide credentials). It often includes a `WWW-Authenticate` header.
- `403 Forbidden` means the server understood the request but refuses to authorize it, regardless of authentication. Since we are using a simple API key, `403` is appropriate for missing or incorrect key. Some APIs use `401` for missing key and `403` for invalid key, but either is acceptable as long as documented.

### 6.2 Cafe Not Found
Return `404 Not Found` with a descriptive error message. This is idempotent: deleting a non-existent resource could return `404` or `200` with a message like "already deleted". REST purists might argue that DELETE on a non-existent resource should return `404` because the resource was not found. We follow that.

### 6.3 Database Error During Deletion
If an exception occurs (e.g., database locked, integrity constraint violation), we roll back and return `500 Internal Server Error`. In a production system, you might want to log the error and perhaps return a more generic message to avoid exposing internals.

### 6.4 Idempotency
DELETE is idempotent. After the first successful deletion, subsequent DELETE requests with the same ID and valid key should return either `404` (since the resource no longer exists) or `200` with a message indicating it's already deleted. Our implementation returns `404` after deletion, which is idempotent because the state (resource gone) remains the same.

## 7. Why DELETE Requires an API Key
- **Data Integrity**: Prevents unauthorized users from deleting records.
- **Auditability**: If keys are tied to specific users or applications, deletions can be traced.
- **Rate Limiting and Abuse Prevention**: Authenticated requests can be throttled.

In a real-world scenario, you would:
- Generate unique API keys for each client.
- Store keys hashed in a database.
- Allow key revocation.
- Use HTTPS to encrypt keys in transit.

## 8. What We Learned
- How to implement a DELETE endpoint in Flask.
- The importance of securing destructive operations with authentication (API key).
- Using query parameters for authentication tokens.
- Appropriate HTTP status codes: `403 Forbidden`, `404 Not Found`, `200 OK`.
- Deleting a record with SQLAlchemy: `db.session.delete()` and `commit()`.
- Handling exceptions and rolling back on errors.
- Testing DELETE requests with Postman, including query parameters.
- Understanding idempotency of DELETE.
