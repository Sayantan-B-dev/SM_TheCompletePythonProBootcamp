## HTTP Requests — Conceptual Foundation and Practical Semantics

HTTP is a stateless request–response protocol where the **method verb** communicates intent, not implementation detail. Each verb carries a semantic contract that servers rely on to decide creation, mutation, replacement, deletion, or retrieval behavior. Pixela follows these semantics closely, which is why your project maps cleanly onto standard HTTP usage patterns.

---

## Core HTTP Methods Used in This Project

### Comparative Overview of HTTP Verbs

| HTTP Method | Intent Semantics                       | Data Mutation Behavior    | Idempotency | Pixela Usage in Project              |
| ----------- | -------------------------------------- | ------------------------- | ----------- | ------------------------------------ |
| GET         | Retrieve representation of a resource  | No server-side mutation   | Yes         | Graph HTML page retrieval            |
| POST        | Create a new subordinate resource      | Creates new server state  | No          | Create user, create graph, add pixel |
| PUT         | Replace or update an existing resource | Overwrites existing state | Yes         | Update existing pixel                |
| DELETE      | Remove an existing resource            | Destroys server state     | Yes         | Delete pixel for a date              |

Idempotency here means that **repeating the same request produces the same final server state**, not necessarily the same response body.

---

## POST — Resource Creation and Action Invocation

### Conceptual Meaning of POST

POST is used when:

* A new resource must be created under a parent endpoint
* The server decides the final storage location or outcome
* The operation is **not guaranteed to be repeat-safe**

Pixela uses POST for all *creation-style operations*, including user creation and pixel insertion.

---

### POST to `/v1/users` — Pixela User Creation

**Endpoint**

```
POST https://pixe.la/v1/users
```

**Purpose**
Registers a new Pixela user identity on the server.

**Why POST is required**
The user resource does not yet exist, and the server must validate and create it atomically.

---

### Required Parameters and Their Meaning

| Parameter             | Type           | Purpose and Reasoning                             |
| --------------------- | -------------- | ------------------------------------------------- |
| `token`               | string         | Acts as the permanent API credential for the user |
| `username`            | string         | Public identifier used in URLs and graph paths    |
| `agreeTermsOfService` | string (`yes`) | Legal confirmation required by Pixela backend     |
| `notMinor`            | string (`yes`) | Compliance requirement for data handling laws     |

Pixela intentionally uses **string literals instead of booleans** to avoid JSON boolean ambiguity across clients.

---

### How This Project Sends the POST Request

```python
def create_user(self) -> dict[str, Any]:
    payload = {
        # Token becomes the permanent authentication credential
        "token": self.headers["X-USER-TOKEN"],

        # Username becomes part of every future resource URL
        "username": self.username,

        # Legal confirmations required by Pixela API contract
        "agreeTermsOfService": "yes",
        "notMinor": "yes",
    }

    try:
        # POST is used because a new server-side resource is being created
        response = requests.post(
            f"{self.base_url}/users",
            json=payload,              # JSON body, not query parameters
            timeout=10,                # Prevents indefinite network blocking
        )
    except requests.RequestException as exc:
        # Network-layer failures are separated from API failures
        raise NetworkError(str(exc))

    return self._handle_response(response)
```

---

### Expected Server Response (Successful Case)

```json
{
  "message": "Success. Let's visit https://pixe.la/@yourusername",
  "isSuccess": true
}
```

**Important Behavioral Detail**
If the user already exists, Pixela returns an error response. Your project intentionally suppresses this error during setup because the desired end state — user existence — is already satisfied.

---

## PUT — Full Replacement or Deterministic Update

### Conceptual Meaning of PUT

PUT is used when:

* The resource already exists
* The client knows the full identity and location of the resource
* Repeating the request should not create duplicates

Pixela uses PUT specifically for **updating an existing pixel**.

---

### PUT in This Project — Updating a Pixel

```python
def update_pixel(self, graph_id: str, date: str, quantity: str):
    payload = {
        # Quantity fully replaces the previous value for that date
        "quantity": quantity
    }

    url = f"{self.base_url}/users/{self.username}/graphs/{graph_id}/{date}"

    try:
        response = requests.put(
            url,
            headers=self.headers,
            json=payload,
            timeout=10,
        )
    except requests.RequestException as exc:
        raise NetworkError(str(exc))

    return self._handle_response(response)
```

**Why PUT is correct here**
Each pixel is uniquely identified by `(graph_id, date)`. Updating it does not create a new entity; it replaces the value deterministically.

---

### Expected Response

```json
{
  "message": "Success.",
  "isSuccess": true
}
```

---

## DELETE — Explicit Resource Removal

### Conceptual Meaning of DELETE

DELETE communicates **intentional destruction** of a known resource. It must be safe to repeat, even if the resource no longer exists.

Pixela adheres strictly to this expectation.

---

### DELETE in This Project — Removing Today’s Pixel

```python
def delete_pixel(self, graph_id: str, date: str):
    url = f"{self.base_url}/users/{self.username}/graphs/{graph_id}/{date}"

    try:
        response = requests.delete(
            url,
            headers=self.headers,
            timeout=10,
        )
    except requests.RequestException as exc:
        raise NetworkError(str(exc))

    return self._handle_response(response)
```

**Behavioral Edge Case**
Deleting a non-existent pixel does not break system consistency. Pixela may still return success or a benign error, which your UI tolerates gracefully.

---

## GET — Retrieval Without Mutation

### Conceptual Meaning of GET

GET is reserved for **safe, read-only retrieval**. Pixela uses GET mainly for visualization, not API JSON responses.

---

### GET in This Project — Graph Visualization

```text
https://pixe.la/v1/users/{username}/graphs/{graph_id}.html
```

This endpoint:

* Returns an HTML document, not JSON
* Does not require authentication headers
* Is suitable for browser rendering

Your project opens this URL using the system browser rather than embedding it, which avoids UI complexity and security issues.

---

## Request Body vs Query Parameters

Pixela consistently expects **JSON request bodies** for POST and PUT operations rather than URL query strings.

Correct usage:

```python
requests.post(url, json=payload)
```

Incorrect and rejected usage:

```python
requests.post(url, params=payload)
```

This distinction matters because Pixela validates content type and payload structure strictly.

---

## Why This HTTP Design Works Well With Pixela

Pixela’s API design aligns closely with HTTP semantics, which enables:

* Predictable error handling
* Clear client intent
* Minimal ambiguity in request meaning
* Simple retry and recovery logic

Your project reflects this alignment correctly by mapping each habit action to its appropriate HTTP verb without overloading or abusing POST for everything.

---

## Mental Mapping Summary

> POST creates something new.
> PUT replaces something known.
> DELETE removes something known.
> GET observes without touching.

Pixela enforces these rules rigorously, and your project is architected in a way that respects them at both the transport and domain layers.
