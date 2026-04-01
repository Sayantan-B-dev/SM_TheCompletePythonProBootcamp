# Cafe & Wifi API – Service Documentation

## 1. Overview
The **Cafe & Wifi API** is a RESTful web service that provides curated data about cafes in London, with a focus on their suitability for remote work. It allows developers to integrate cafe information into their own applications, such as websites or mobile apps that help users find places to work, study, or take calls.

The API is built using **Flask** and **SQLAlchemy**, with an SQLite database (cafes.db) that stores details about each cafe, including amenities like Wi-Fi availability, power sockets, toilet access, and coffee prices. The service is designed to be simple to use, follow REST conventions, and return data in JSON format.

## 2. Purpose and Motivation
Many companies collect valuable data and monetize it by offering API access. This project demonstrates how to create such an API from scratch. The data set includes personal recommendations of cafes suitable for remote work. By exposing this data via an API, other developers can build applications that help users discover these locations. Future extensions could include user contributions, authentication, and usage-based pricing.

## 3. Base URL
All API endpoints are relative to the base URL:

```
http://localhost:5000
```

When deployed to a production server, the base URL will change accordingly.

## 4. Data Model – Cafe Resource
Each cafe is represented as a JSON object with the following fields:

| Field          | Type    | Description                                                                 |
|----------------|---------|-----------------------------------------------------------------------------|
| id             | integer | Unique identifier for the cafe.                                             |
| name           | string  | Name of the cafe.                                                           |
| map_url        | string  | Google Maps (or other) URL pointing to the cafe’s location.                |
| img_url        | string  | URL of an image of the cafe.                                                |
| location       | string  | General area or neighbourhood (e.g., "Shoreditch", "Covent Garden").       |
| has_sockets    | boolean | Whether the cafe has power sockets available.                               |
| has_toilet     | boolean | Whether the cafe has a public toilet.                                       |
| has_wifi       | boolean | Whether Wi-Fi is available.                                                 |
| can_take_calls | boolean | Whether it is acceptable to take phone/video calls.                         |
| seats          | string  | Approximate number of seats (e.g., "10-20", "50+").                         |
| coffee_price   | string  | Price of a single black coffee (e.g., "£2.50").                             |

### Example Cafe Object
```json
{
  "id": 1,
  "name": "The Attendant",
  "map_url": "https://goo.gl/maps/...",
  "img_url": "https://.../photo.jpg",
  "location": "Fitzrovia",
  "has_sockets": true,
  "has_toilet": true,
  "has_wifi": true,
  "can_take_calls": false,
  "seats": "10-20",
  "coffee_price": "£2.75"
}
```

## 5. API Endpoints
The following endpoints are implemented. All responses are JSON-encoded.

| Endpoint                         | HTTP Method | Description                                                      |
|----------------------------------|-------------|------------------------------------------------------------------|
| `/random`                        | GET         | Returns a randomly selected cafe.                                |
| `/all`                           | GET         | Returns a list of all cafes in the database.                     |
| `/search`                        | GET         | Searches for cafes by location (query parameter `loc`).          |
| `/` (or `/add`)                  | POST        | Adds a new cafe to the database. Requires form data or JSON.     |
| `/update-price/<int:cafe_id>`    | PATCH       | Updates the coffee price of a specific cafe.                     |
| `/report-closed/<int:cafe_id>`   | DELETE      | Deletes a cafe from the database (requires an API key).          |

### 5.1 GET /random
Retrieves a single cafe chosen at random from the database.

**Request Example**
```
GET /random
```

**Response Example**
```json
{
  "id": 3,
  "name": "Look Mum No Hands!",
  "map_url": "https://goo.gl/maps/...",
  "img_url": "https://.../photo.jpg",
  "location": "Old Street",
  "has_sockets": true,
  "has_toilet": true,
  "has_wifi": true,
  "can_take_calls": true,
  "seats": "20-30",
  "coffee_price": "£2.50"
}
```

### 5.2 GET /all
Returns an array containing all cafe records.

**Request Example**
```
GET /all
```

**Response Example**
```json
[
  {
    "id": 1,
    "name": "The Attendant",
    ...
  },
  {
    "id": 2,
    "name": "Workshop Coffee",
    ...
  }
]
```

### 5.3 GET /search
Searches for cafes in a given location. The location is provided via a query parameter `loc`.

**Request Example**
```
GET /search?loc=Shoreditch
```

**Success Response (200 OK)**
```json
[
  {
    "id": 5,
    "name": "Shoreditch Grind",
    "location": "Shoreditch",
    ...
  }
]
```

If no cafes are found in that location, the API returns a 404 Not Found with an error message:
```json
{
  "error": "No cafes found in that location."
}
```

### 5.4 POST / (or /add)
Adds a new cafe to the database. The request must include all required fields. Data can be sent as `application/x-www-form-urlencoded` (form data) or `application/json`.

**Required Fields:** `name`, `map_url`, `img_url`, `location`, `has_sockets`, `has_toilet`, `has_wifi`, `can_take_calls`, `seats`, `coffee_price`.  
Boolean fields should be sent as `true`/`false` or `1`/`0`.

**Request Example (form-data)**
```
POST /add
name=Cafe+Name&map_url=http://...&img_url=http://...&location=Camden&has_sockets=1&has_toilet=0&has_wifi=1&can_take_calls=0&seats=10-20&coffee_price=2.50
```

**Response (201 Created)**
```json
{
  "id": 42,
  "name": "Cafe Name",
  ...
}
```

If any required field is missing, a 400 Bad Request is returned:
```json
{
  "error": "Missing required field: name"
}
```

### 5.5 PATCH /update-price/<cafe_id>
Updates the coffee price for a specific cafe identified by its `id`. The new price must be provided in the request body as a field named `coffee_price`.

**Request Example**
```
PATCH /update-price/3
coffee_price=3.00
```

**Success Response (200 OK)**
```json
{
  "success": "Successfully updated the price."
}
```

If the cafe ID does not exist, a 404 Not Found is returned:
```json
{
  "error": "Cafe with that id not found."
}
```

If the `coffee_price` field is missing, a 400 Bad Request is returned.

### 5.6 DELETE /report-closed/<cafe_id>
Deletes a cafe from the database. This operation requires an **API key** for authorization, passed as a query parameter `api-key`. The valid key is `TopSecretAPIKey`.

**Request Example**
```
DELETE /report-closed/3?api-key=TopSecretAPIKey
```

**Success Response (200 OK)**
```json
{
  "success": "Cafe deleted successfully."
}
```

If the API key is missing or incorrect, a 403 Forbidden is returned:
```json
{
  "error": "You are not authorized to delete. Please provide the correct api-key."
}
```

If the cafe ID does not exist, a 404 Not Found is returned.

## 6. Error Handling
The API uses standard HTTP status codes to indicate success or failure. In case of an error, the response body includes a JSON object with an `error` field describing the problem.

Common status codes:
- `200 OK` – The request succeeded.
- `201 Created` – A new resource was successfully created.
- `400 Bad Request` – The request was malformed or missing required data.
- `403 Forbidden` – The client is not authorized to perform the action.
- `404 Not Found` – The requested resource could not be found.
- `500 Internal Server Error` – An unexpected error occurred on the server.

## 7. Testing the API
Developers can test the API using tools like **Postman** or **curl**. The endpoints are designed to be intuitive and follow RESTful patterns. For example, to fetch a random cafe with curl:

```bash
curl http://localhost:5000/random
```

To add a new cafe using curl with JSON:

```bash
curl -X POST http://localhost:5000/add \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Cafe",
    "map_url": "https://goo.gl/maps/...",
    "img_url": "https://.../image.jpg",
    "location": "Soho",
    "has_sockets": true,
    "has_toilet": true,
    "has_wifi": true,
    "can_take_calls": false,
    "seats": "10-20",
    "coffee_price": "£2.80"
  }'
```

## 8. Future Enhancements
The API is designed to be extensible. Possible future additions include:
- User authentication and registration.
- Rate limiting to prevent abuse.
- Pagination for the `/all` endpoint.
- More advanced search filters (e.g., by amenities, price range).
- Monetization via API keys and subscription plans.

## 9. Documentation and Publishing
API documentation can be automatically generated using Postman. Once all endpoints are saved in a Postman collection, the collection can be published as interactive documentation, which can be linked from the project’s landing page (index.html).

Example of published documentation: [Cafe & Wifi API Docs](https://documenter.getpostman.com/view/...)

---
