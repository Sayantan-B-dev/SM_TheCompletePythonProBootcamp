# Postman – The All-in-One API Testing Tool

## 1. Introduction to Postman
Postman is a collaborative platform for API development and testing. It provides a graphical user interface to send HTTP requests, inspect responses, and organize APIs into collections. Postman is widely adopted by developers because it simplifies the process of building, testing, and documenting APIs.

For the Cafe & Wifi API, Postman serves multiple purposes:
- **Manual Testing**: Developers can quickly verify that each endpoint behaves as expected without writing frontend forms or using curl.
- **Automated Testing**: Postman allows writing test scripts and running collections in CI/CD pipelines.
- **Documentation**: Postman can automatically generate beautiful, interactive documentation from saved requests.
- **Collaboration**: Teams can share collections and environments, ensuring consistent API usage.

## 2. Download and Installation
Postman is available for Windows, macOS, and Linux. To install:

1. Visit the official website: [https://www.postman.com/downloads/](https://www.postman.com/downloads/)
2. Choose the appropriate version for your operating system.
3. Run the installer and follow the on-screen instructions.
4. After installation, launch Postman. You may be prompted to create a free account – this is optional but recommended for syncing collections across devices.

## 3. The Postman Interface
When you open Postman, the main interface consists of:
- **Sidebar**: On the left, showing Collections, APIs, Environments, and History.
- **Request Builder**: The central area where you construct requests (method, URL, headers, body).
- **Response Viewer**: Below the request builder, displaying the server's response, including status, time, size, and body.
- **Top Bar**: Contains the "New" button, import, workspace switcher, and user profile.

## 4. Creating a Collection for the Cafe & Wifi API
A collection is a group of saved requests. Organizing requests into a collection makes them easy to reuse and document.

**Steps to create a collection:**
1. In the sidebar, click on "Collections".
2. Click the "+" icon or the "Create Collection" button.
3. Name the collection, e.g., **Cafe & Wifi API**.
4. Optionally, add a description: "API for accessing remote-work-friendly cafes in London."
5. Click "Create".

Now you have an empty collection where you will save all your API requests.

## 5. Adding GET Requests to the Collection

### 5.1 GET /random
1. Click the "New" button (or use the `+` tab to open a new request tab).
2. Set the request method to **GET**.
3. Enter the URL: `http://localhost:5000/random`.
4. Click "Send". You should see a JSON response with a random cafe.
5. To save this request, click the "Save" button (or press `Ctrl+S` / `Cmd+S`).
6. Choose the **Cafe & Wifi API** collection and name the request "Get Random Cafe".
7. Optionally, add a description: "Returns a randomly selected cafe from the database."
8. Click "Save".

### 5.2 GET /all
1. Open a new tab.
2. Method: **GET**, URL: `http://localhost:5000/all`.
3. Send the request; you should receive a JSON array of all cafes.
4. Save as "Get All Cafes" in the same collection.

### 5.3 GET /search (with Query Parameters)
1. New tab, method **GET**.
2. URL: `http://localhost:5000/search`.
3. To add the `loc` query parameter, click on the "Params" tab below the URL field.
4. In the "Query Params" table, enter:
   - Key: `loc`
   - Value: `Shoreditch` (or any location present in your database).
5. The URL will automatically update to `http://localhost:5000/search?loc=Shoreditch`.
6. Send the request. If cafes exist in Shoreditch, you'll see a JSON array; otherwise, a 404 error.
7. Save as "Search Cafes by Location".

**Note**: You can test with different values by changing the parameter value directly in the table.

## 6. Adding POST Request to Add a New Cafe
POST requests typically send data in the request body. Postman makes it easy to construct form data or JSON.

1. New tab, method **POST**.
2. URL: `http://localhost:5000/add` (or just `http://localhost:5000/` if that's your endpoint; adjust as needed).
3. Click on the "Body" tab below the URL.
4. Select **x-www-form-urlencoded** (this simulates an HTML form submission). Alternatively, you can use **raw** and set type to JSON, but form-urlencoded is simpler for this example.
5. In the table, enter the key-value pairs for all required fields:
   - `name` : "Test Cafe"
   - `map_url` : "https://goo.gl/maps/example"
   - `img_url` : "https://example.com/cafe.jpg"
   - `location` : "Test Area"
   - `has_sockets` : "true" (or "1")
   - `has_toilet` : "false" (or "0")
   - `has_wifi` : "true"
   - `can_take_calls` : "false"
   - `seats` : "10-20"
   - `coffee_price` : "£2.50"
6. Click "Send". On success, you should receive a `201 Created` status and the newly created cafe object (including its new ID).
7. Save the request as "Add New Cafe".

**Important**: The API expects boolean values as `true`/`false` or `1`/`0`. Ensure your values are correctly formatted.

## 7. Adding PATCH Request to Update Coffee Price
PATCH requests are used for partial updates. They often include the resource ID in the URL and the fields to update in the body.

1. New tab, method **PATCH**.
2. URL: `http://localhost:5000/update-price/1` (replace `1` with an existing cafe ID).
3. Go to the "Body" tab, select **x-www-form-urlencoded**.
4. Add key: `coffee_price`, value: `£3.00`.
5. Send the request. Expected response: a success message.
6. Save as "Update Coffee Price".

You can also test with a non-existent ID to verify the 404 error response.

## 8. Adding DELETE Request with API Key
DELETE requests often require authentication. This API uses an `api-key` query parameter.

1. New tab, method **DELETE**.
2. URL: `http://localhost:5000/report-closed/1` (replace `1` with an existing ID).
3. In the "Params" tab, add:
   - Key: `api-key`
   - Value: `TopSecretAPIKey`
   The URL becomes `http://localhost:5000/report-closed/1?api-key=TopSecretAPIKey`.
4. Send the request. On success, you should see a deletion confirmation.
5. Save as "Delete Closed Cafe".

Test with wrong API key or non-existent ID to see the corresponding error responses.

## 9. Testing and Saving Responses
For each saved request, you can also add **tests** (in the "Tests" tab) to automate assertions. For example, after sending a request, you can write JavaScript to check that the status is 200 or that the response contains expected fields. However, for basic documentation, just saving requests with descriptions is sufficient.

## 10. Environment Variables (Optional)
Postman allows you to define variables that can be reused across requests. This is useful for base URLs, API keys, or IDs.

**Creating an environment:**
1. Click the "Environments" icon (gear) in the top right.
2. Click "Add" to create a new environment, e.g., "Local Development".
3. Add a variable:
   - Variable: `base_url`
   - Initial value: `http://localhost:5000`
   - Current value: same
4. Save and select this environment from the dropdown.

Now you can replace hardcoded URLs with `{{base_url}}/random`. If you later deploy to a production server, you can change the environment variable without editing each request.

## 11. Generating API Documentation from the Collection
One of Postman's most powerful features is its ability to generate beautiful, interactive documentation from a collection.

**Steps to publish documentation:**
1. In the sidebar, right-click on your **Cafe & Wifi API** collection.
2. Select **"Publish Docs"**.
3. Postman will open a new page showing a preview of the documentation.
4. You can customize the documentation's name, description, and visibility (public or private).
5. Click **"Publish"** to make it publicly accessible.
6. After publishing, you will receive a shareable URL, e.g., `https://documenter.getpostman.com/view/...`

The generated documentation includes:
- List of all requests in the collection.
- HTTP method and URL for each request.
- Descriptions you added.
- Example request and response bodies (based on the last saved response).
- Query parameters, headers, and body schemas (if configured).

## 12. Linking Documentation in the Project's index.html
With the documentation URL in hand, you can update your project's landing page (`index.html`) to include a link. For example:

```html
<a href="https://documenter.getpostman.com/view/..." target="_blank">View API Documentation</a>
```

This provides a professional touch and makes it easy for other developers to understand and use your API.

## 13. Conclusion
Postman streamlines the entire API development lifecycle. By using it to test the Cafe & Wifi API, you ensure that each endpoint works as expected before moving on. Saving requests in a collection and publishing documentation allows you to share your work with other developers and create a professional API service. The next steps involve building the remaining endpoints (POST, PATCH, DELETE) and continuing to test them with Postman.