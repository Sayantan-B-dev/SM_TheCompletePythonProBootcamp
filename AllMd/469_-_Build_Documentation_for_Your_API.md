# Building API Documentation with Postman

## 1. Importance of API Documentation
API documentation is the user manual for your web service. It tells developers how to interact with your API, what endpoints are available, what parameters they require, and what responses they can expect. Good documentation is essential for adoption, reduces support requests, and presents a professional image.

For the Cafe & Wifi API, documentation will include:
- A list of all endpoints (GET /random, GET /all, GET /search, POST /add, PATCH /update-price, DELETE /report-closed).
- The HTTP method for each endpoint.
- Required and optional parameters (query parameters, body fields).
- Example requests and responses.
- Authentication requirements (API key for DELETE).
- Error codes and messages.

Postman simplifies documentation generation by automatically creating interactive docs from your saved requests.

## 2. Prerequisites
Before generating documentation, ensure you have:
- **All API endpoints implemented** and tested in your Flask application.
- **Postman installed** and open.
- **A Postman collection** (e.g., "Cafe & Wifi API") containing **all saved requests** (GET /random, GET /all, GET /search, POST /add, PATCH /update-price, DELETE /report-closed). Each request should:
  - Have a meaningful name (e.g., "Get Random Cafe").
  - Include a description (added in the request edit view) explaining the endpoint's purpose, required parameters, and any special notes.
  - Have a saved example response (Postman automatically captures the last response when you save a request, or you can manually add examples).

## 3. Adding Descriptions to Requests
Descriptions make your documentation clear and helpful. To add or edit a description for a saved request in Postman:
1. In the sidebar, click on your collection to expand it.
2. Right-click on a request (e.g., "Get Random Cafe") and select **Edit** (or double-click the request to open it).
3. In the request builder, there is a **Description** field (usually a pencil icon or text area). Click it and write a description. For example:
   > "Returns a randomly selected cafe from the database. No parameters required."
4. Include details about parameters if applicable. For the search endpoint, you might write:
   > "Search for cafes by location. Provide the `loc` query parameter with the area name (e.g., 'Shoreditch'). Returns an array of matching cafes or a 404 error if none found."
5. For POST and PATCH, describe the required body fields.
6. For DELETE, mention the required `api-key` query parameter.
7. Click **Save** to update the request.

## 4. Publishing Documentation from Postman
Once all requests are saved and described, follow these steps to publish:

1. In the Postman sidebar, locate your collection (e.g., "Cafe & Wifi API").
2. Click on the **three dots (...)** next to the collection name.
3. Select **Publish Docs** from the context menu.
4. Postman will open a new browser tab (or a pane within Postman) showing a preview of your documentation.
5. In the preview, you can:
   - Edit the documentation title and description (top of the page).
   - Choose the visibility: **Public** (anyone with the link can view) or **Private** (requires a Postman account and team access). For a public API, select Public.
   - Reorder requests if needed (drag and drop in the left sidebar).
6. Click the **Publish** button.
7. After publishing, you'll receive a shareable URL, for example:
   ```
   https://documenter.getpostman.com/view/12345678/2s9YJZ4ZqR
   ```
8. Copy this URL.

## 5. Customizing Documentation
Postman's generated documentation includes:
- Collection name and description.
- Each request with its method, URL, and description.
- Example request (based on the last saved request or manually added examples).
- Example response (if saved).
- Headers and parameters tables.

You can further customize by:
- Adding **examples** (multiple request/response pairs) in Postman before publishing.
- Organizing requests into folders within the collection to group related endpoints.
- Including **environment variables** in the documentation (if you used variables like `{{base_url}}`, they will be shown as placeholders).

## 6. Linking Documentation from the Project's index.html
With the documentation URL in hand, update your project's landing page (`index.html`) to include a prominent link. This gives developers immediate access to your API docs.

Example `index.html` snippet:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Cafe & Wifi API</title>
</head>
<body>
    <h1>Welcome to the Cafe & Wifi API</h1>
    <p>This API provides data on remote-work-friendly cafes in London.</p>
    <p><a href="https://documenter.getpostman.com/view/..." target="_blank">View API Documentation</a></p>
    <p>Base URL: <code>http://localhost:5000</code> (or your production URL)</p>
</body>
</html>
```

Commit this change to your project. When you deploy the API, users will see a direct link to the interactive documentation.

## 7. Example Published Documentation
Here is what the published documentation might include (condensed):

**Cafe & Wifi API**  
Base URL: `http://localhost:5000`

**Endpoints**

- **GET /random**  
  Returns a random cafe.  
  *No parameters.*  
  **Example Response (200 OK)**  
  ```json
  {
    "id": 3,
    "name": "Look Mum No Hands!",
    "map_url": "https://goo.gl/maps/...",
    ...
  }
  ```

- **GET /all**  
  Returns all cafes.  
  *No parameters.*  
  **Example Response (200 OK)**  
  ```json
  [ { "id": 1, ... }, { "id": 2, ... } ]
  ```

- **GET /search**  
  Search cafes by location.  
  **Query Parameters**  
  - `loc` (string, required): Location area, e.g., "Shoreditch".  
  **Example Request**  
  `GET /search?loc=Shoreditch`  
  **Example Response (200 OK)**  
  ```json
  [ { "id": 5, "name": "Shoreditch Grind", "location": "Shoreditch", ... } ]
  ```
  **Error Response (404 Not Found)**  
  ```json
  { "error": "No cafes found in that location." }
  ```

- **POST /add**  
  Add a new cafe.  
  **Body (x-www-form-urlencoded or JSON)**  
  Required fields: `name`, `map_url`, `img_url`, `location`, `has_sockets`, `has_toilet`, `has_wifi`, `can_take_calls`, `seats`.  
  Optional: `coffee_price`.  
  Boolean fields accept `true`/`false` or `1`/`0`.  
  **Example Request (JSON)**  
  ```json
  {
    "name": "New Cafe",
    "map_url": "https://...",
    "img_url": "https://...",
    "location": "Soho",
    "has_sockets": true,
    "has_toilet": false,
    "has_wifi": true,
    "can_take_calls": true,
    "seats": "20-30",
    "coffee_price": "£3.00"
  }
  ```
  **Example Response (201 Created)**  
  Returns the created cafe object with its new `id`.

- **PATCH /update-price/{cafe_id}**  
  Update the coffee price of a specific cafe.  
  **URL Parameters**  
  - `cafe_id` (integer, required): ID of the cafe.  
  **Body (JSON or form)**  
  - `coffee_price` (string, required): New price.  
  **Example Request**  
  `PATCH /update-price/3` with body `{ "coffee_price": "£3.50" }`  
  **Example Response (200 OK)**  
  ```json
  { "success": "Successfully updated the price." }
  ```

- **DELETE /report-closed/{cafe_id}**  
  Delete a cafe (requires API key).  
  **URL Parameters**  
  - `cafe_id` (integer, required): ID of the cafe.  
  **Query Parameters**  
  - `api-key` (string, required): Must equal `TopSecretAPIKey`.  
  **Example Request**  
  `DELETE /report-closed/3?api-key=TopSecretAPIKey`  
  **Example Response (200 OK)**  
  ```json
  { "success": "Cafe deleted successfully." }
  ```
  **Error Responses**  
  - `403 Forbidden`: Invalid or missing API key.  
  - `404 Not Found`: Cafe ID does not exist.

## 8. Best Practices for Maintaining Documentation
- **Keep in sync**: Whenever you change an endpoint, update the corresponding request in Postman (and its description) before republishing.
- **Use examples**: Add multiple examples to illustrate different responses (success, error).
- **Version your API**: If you release a new version, create a new collection or use version indicators in the documentation.
- **Include authentication details**: Clearly explain how to obtain and use API keys.
- **Provide contact info**: Let users know how to reach you for support.

## 9. Completed Project Solution
The completed project solution code (all endpoints implemented) can be found in the resources accompanying this lesson. It includes:
- Full `main.py` with all routes.
- The `cafes.db` database.
- This documentation guide.

You can compare your implementation with the solution to ensure correctness.

## 10. Conclusion
Building comprehensive documentation for your API is a critical final step. Postman automates much of the work, allowing you to generate professional, interactive docs from the same requests you used for testing. By linking this documentation from your project's `index.html`, you provide a seamless experience for developers who want to use your Cafe & Wifi API. With this, the API is complete and ready to be shared with the world.

---
