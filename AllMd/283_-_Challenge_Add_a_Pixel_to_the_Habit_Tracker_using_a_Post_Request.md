## Adding a Pixel to a Habit Graph Using HTTP POST

### Conceptual Meaning of “Adding a Pixel” in Pixela

In Pixela’s domain model, **adding a pixel means creating a daily data point** for a specific graph on a specific date. A pixel is not an abstract object; it is a **date-indexed numeric value** that becomes part of the graph’s visual timeline. Because a pixel represents a *new server-side resource*, Pixela correctly requires an HTTP **POST** request for this operation.

Each pixel is uniquely identified by the tuple:

```
(username, graph_id, date)
```

This uniqueness constraint is enforced server-side and directly influences the HTTP method choice.

---

## Endpoint Structure and Resource Identity

### Pixel Creation Endpoint

```
POST https://pixe.la/v1/users/{username}/graphs/{graph_id}
```

This URL expresses **ownership and containment**, not authentication.

* `users/{username}` identifies the account namespace
* `graphs/{graph_id}` identifies the habit graph container
* The pixel itself is defined entirely by the request body

The date is intentionally *not* placed in the URL during creation, because the pixel does not yet exist.

---

## Authentication via HTTP Headers

### Required Request Headers

```python
headers = {
    "X-USER-TOKEN": "your-token",
    "Content-Type": "application/json"
}
```

### Why Authentication Lives in Headers

* Authentication is request metadata, not business data
* Headers allow early rejection before payload parsing
* Tokens are protected from URL logging and caching
* Infrastructure layers can enforce security without inspecting JSON bodies

Your project centralizes this logic inside `PixelaClient`, ensuring no request can bypass authentication accidentally.

---

## Request Body Structure and Validation Rules

### Pixel Payload Definition

```python
pixel_data = {
    "date": "20250208",
    "quantity": "10"
}
```

### Field-Level Semantics

| Field      | Type   | Meaning                    | Validation Rules                |
| ---------- | ------ | -------------------------- | ------------------------------- |
| `date`     | string | Calendar key for the pixel | Must be `YYYYMMDD`, zero-padded |
| `quantity` | string | Numeric habit value        | Must match graph `type`         |

Pixela intentionally requires **strings**, even for numeric values, to ensure consistent JSON parsing across languages.

---

## Why POST Is the Correct HTTP Method Here

### POST Semantics Applied to Pixels

POST is used because:

* A new resource is being created
* The server enforces uniqueness constraints
* Repeating the request may fail or change behavior
* The client does not control the storage outcome

If a pixel already exists for that date, Pixela will reject the request, proving that POST is **non-idempotent**, exactly as HTTP semantics require.

---

## Concrete Implementation in This Project

### Pixel Creation Method in `PixelaClient`

```python
def add_pixel(self, graph_id: str, date: str, quantity: str):
    payload = {
        "date": date,           # Unique daily identifier
        "quantity": quantity    # Habit value for that day
    }

    url = f"{self.base_url}/users/{self.username}/graphs/{graph_id}"

    try:
        response = requests.post(
            url,
            headers=self.headers,   # Authentication injected here
            json=payload,           # JSON body, not query parameters
            timeout=10              # Prevents UI blocking on network stalls
        )
    except requests.RequestException as exc:
        raise NetworkError(str(exc))

    return self._handle_response(response)
```

### Why This Design Is Correct

* Authentication is injected once and reused
* Business logic never touches HTTP internals
* Payload structure mirrors Pixela’s contract exactly
* Network failures are isolated from API failures

---

## Expected Server Response

### Successful Pixel Creation

```json
{
  "message": "Success.",
  "isSuccess": true
}
```

### Failure Case: Pixel Already Exists

```json
{
  "message": "Pixel already exists.",
  "isSuccess": false
}
```

Your UI layer interprets this distinction correctly by guiding users toward **Update** instead of **Add**.

---

## Edge Cases and Behavioral Constraints

### One Pixel Per Day Rule

Pixela enforces a strict invariant:

> A graph may contain at most one pixel per date.

This means:

* POST is valid only once per day
* Subsequent changes must use PUT
* DELETE removes the date entirely

Your project models this cleanly through separate UI actions rather than attempting auto-retries or silent overrides.

---

## Why Date Is in the Body and Not the URL

During creation, the pixel does not yet exist, so placing the date in the URL would imply resource existence. Pixela reserves date-based URLs for **already-existing pixels**, which is why:

* POST uses `/graphs/{graph_id}` with date in body
* PUT and DELETE use `/graphs/{graph_id}/{date}`

This is a textbook example of correct REST resource lifecycle modeling.

---

## Full Example Usage Aligned With the Project

```python
import requests

PIXELA_ENDPOINT = "https://pixe.la/v1/users/my-username/graphs/graph1"

headers = {
    "X-USER-TOKEN": "your-token",
    "Content-Type": "application/json"
}

pixel_data = {
    "date": "20250208",
    "quantity": "10"
}

response = requests.post(
    url=PIXELA_ENDPOINT,
    json=pixel_data,
    headers=headers
)

print(response.text)
```

### Expected Console Output

```text
{"message":"Success.","isSuccess":true}
```

---

## Mental Model for Pixel Creation

> A pixel is a daily fact.
> POST records that fact for the first time.
> PUT corrects the fact if needed.
> DELETE erases the fact entirely.

Your project adheres to this model rigorously, which is why its Pixela integration is predictable, debuggable, and semantically correct.
