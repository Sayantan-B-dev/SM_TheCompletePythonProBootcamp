## Using PUT and DELETE Requests for Pixel Management in Pixela

### Why PUT and DELETE Exist Separately in Pixela

Pixela models each pixel as a **date-addressable resource**. Once a pixel exists for a given date, it becomes a stable entity that can either be **replaced** or **removed**, but never recreated using the same operation. This strict lifecycle is the reason Pixela exposes **PUT for updates** and **DELETE for removals**, rather than overloading POST.

In this project, these operations are intentionally separated to preserve correctness and avoid ambiguous behavior.

---

## Resource Identity for Existing Pixels

### Pixel URL Structure

```
https://pixe.la/v1/users/{username}/graphs/{graph_id}/{date}
```

Each segment carries meaning:

* `username` defines ownership
* `graph_id` defines the habit container
* `date` defines the exact pixel instance

At this point, the pixel is assumed to already exist, which is why the date moves from the request body into the URL.

---

## PUT — Updating an Existing Pixel

### Semantic Meaning of PUT in This Context

PUT represents a **full, deterministic replacement** of the pixel’s stored value for that date. Even though Pixela accepts only `quantity` in the body, the operation conceptually replaces the entire pixel resource.

Repeating the same PUT request produces the same final state, which is why PUT is considered idempotent.

---

### Endpoint for Updating a Pixel

```
PUT https://pixe.la/v1/users/my-username/graphs/graph1/20250208
```

The date is embedded directly in the URL, signaling that the resource already exists and is being addressed explicitly.

---

### Request Headers for Authentication

```python
headers = {
    "X-USER-TOKEN": "your-token",
    "Content-Type": "application/json"
}
```

Authentication remains in headers, not in the body or URL, maintaining separation between identity and authorization.

---

### Request Body for Updating a Pixel

```json
{
  "quantity": "15"
}
```

Only the mutable field is included. Pixela does not allow partial ambiguity; the new quantity fully replaces the previous value.

---

### PUT Request Example Aligned With the Project

```python
import requests

url = "https://pixe.la/v1/users/my-username/graphs/graph1/20250208"

headers = {
    "X-USER-TOKEN": "your-token",
    "Content-Type": "application/json"
}

pixel_data = {
    "quantity": "15"
}

response = requests.put(
    url,
    json=pixel_data,
    headers=headers
)

print(response.text)
```

### Expected Output

```text
{"message":"Success.","isSuccess":true}
```

---

### How This Is Implemented in the Project

```python
def update_pixel(self, graph_id: str, date: str, quantity: str):
    payload = {
        "quantity": quantity
    }

    url = f"{self.base_url}/users/{self.username}/graphs/{graph_id}/{date}"

    response = requests.put(
        url,
        headers=self.headers,
        json=payload,
        timeout=10
    )

    return self._handle_response(response)
```

This method guarantees that updates are explicit, deterministic, and scoped to a single calendar day.

---

## DELETE — Removing an Existing Pixel

### Semantic Meaning of DELETE

DELETE expresses **intentional removal** of a known resource. After deletion, the pixel no longer exists, and the graph visually shows an empty day.

DELETE is idempotent: deleting the same pixel multiple times results in the same final state.

---

### Endpoint for Deleting a Pixel

```
DELETE https://pixe.la/v1/users/my-username/graphs/graph1/20250208
```

The URL structure is identical to PUT, reinforcing the idea that the same resource is being addressed.

---

### DELETE Request Example Aligned With the Project

```python
import requests

url = "https://pixe.la/v1/users/my-username/graphs/graph1/20250208"

headers = {
    "X-USER-TOKEN": "your-token"
}

response = requests.delete(
    url,
    headers=headers
)

print(response.text)
```

### Expected Output

```text
{"message":"Success.","isSuccess":true}
```

---

### How DELETE Is Implemented in the Project

```python
def delete_pixel(self, graph_id: str, date: str):
    url = f"{self.base_url}/users/{self.username}/graphs/{graph_id}/{date}"

    response = requests.delete(
        url,
        headers=self.headers,
        timeout=10
    )

    return self._handle_response(response)
```

This design keeps deletion logic simple, explicit, and isolated from update logic.

---

## Behavioral Differences Between PUT and DELETE

| Aspect             | PUT                          | DELETE                  |
| ------------------ | ---------------------------- | ----------------------- |
| Purpose            | Replace existing pixel value | Remove pixel entirely   |
| Requires body      | Yes                          | No                      |
| Idempotent         | Yes                          | Yes                     |
| Visual result      | Changes intensity of day     | Clears the day          |
| Failure if missing | May error if pixel absent    | Often succeeds silently |

---

## Why Pixela Requires Date in URL for PUT and DELETE

Once a pixel exists, its identity becomes stable. Placing the date in the URL:

* Declares the resource as addressable
* Prevents accidental creation of new pixels
* Aligns with REST resource semantics
* Enables safe retries without duplication

This distinction between POST and PUT/DELETE is a deliberate design choice that your project respects fully.

---

## Mental Model for Pixel Mutation

> POST introduces a fact.
> PUT corrects a known fact.
> DELETE removes a fact entirely.

Your project maps each of these intentions to the correct HTTP verb, producing a Pixela integration that is predictable, expressive, and architecturally sound.
