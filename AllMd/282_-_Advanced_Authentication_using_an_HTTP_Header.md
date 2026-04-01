## Advanced Authentication Using HTTP Headers in Pixela

### Core Authentication Model Used by Pixela

Pixela implements **token-based authentication via custom HTTP headers**, not query parameters and not cookies. This approach treats authentication as **request metadata**, not as part of the resource identity or payload.

In your project, this model is centralized and enforced inside `PixelaClient`, which ensures that authentication is consistently applied across all state-changing operations.

---

## Creating a New Graph — Endpoint and Intent

### Endpoint Definition

```
POST https://pixe.la/v1/users/{username}/graphs
```

This endpoint creates a **graph resource owned by an existing user**. The user identity is encoded in the URL path, while authentication is supplied through request headers.

---

## Graph Configuration Payload — JSON Body Semantics

### Request Body Structure

```json
{
  "id": "graph1",
  "name": "Coding",
  "type": "int",
  "unit": "mins",
  "color": "ajisai"
}
```

### Meaning of Each Field

| Field   | Purpose              | Why It Exists                                     |
| ------- | -------------------- | ------------------------------------------------- |
| `id`    | Graph identifier     | Becomes part of the graph URL and pixel endpoints |
| `name`  | Human-readable label | Used for UI display and graph title               |
| `type`  | Data constraint      | Enforces integer or float validation server-side  |
| `unit`  | Measurement unit     | Adds semantic meaning to numeric values           |
| `color` | Visual identity      | Differentiates graphs visually without metadata   |

Pixela enforces **strict schema validation** here. Any missing or malformed field results in immediate rejection.

---

## Authentication via HTTP Headers — Practical Implementation

### Header-Based Authentication Used by Pixela

```python
headers = {
    "X-USER-TOKEN": "your-token",
    "Content-Type": "application/json"
}
```

### Actual Request Execution

```python
requests.post(
    url,
    json=body,
    headers=headers
)
```

This approach is exactly what your `PixelaClient.create_graph` method encapsulates, ensuring no caller can accidentally omit authentication.

---

## Why Pixela Uses Headers Instead of Query Parameters

### Separation of Concerns at the Protocol Level

HTTP defines **headers as metadata** and **query parameters as resource selectors**. Authentication credentials are not resource identifiers; they are authorization context.

Placing tokens in headers preserves this semantic separation.

> Authentication answers *who you are*
> Query parameters answer *what you want*

Mixing these concerns weakens protocol clarity.

---

## Security Implications of Headers vs Query Parameters

### Token Leakage Risk Comparison

| Aspect                   | Headers        | Query Parameters   |
| ------------------------ | -------------- | ------------------ |
| Browser history exposure | Not stored     | Stored             |
| Server access logs       | Often redacted | Commonly logged    |
| Proxy visibility         | Less exposed   | Frequently exposed |
| URL sharing risk         | None           | Extremely high     |
| Cache poisoning risk     | Minimal        | Elevated           |

Query parameters are routinely logged by reverse proxies, load balancers, analytics systems, and error monitoring tools. Headers are far less likely to be persisted verbatim.

Pixela’s design minimizes accidental credential leakage by enforcing header usage.

---

## Why Not Put the Token in the JSON Body

Placing authentication credentials inside the request body introduces ambiguity and security concerns.

* Bodies are parsed at application level, not transport level
* Middleware layers cannot authenticate early
* Logging systems often dump request bodies for debugging
* Content-type parsing failures can block authentication entirely

Headers allow **early rejection**, **uniform validation**, and **consistent middleware handling**.

---

## Advanced HTTP Semantics: Why Headers Enable Better API Design

### Statelessness Enforcement

Each request contains:

* Full authentication context
* Full resource identity
* No reliance on server-side session state

This enables Pixela to scale horizontally without session replication.

---

### Middleware and Gateway Compatibility

Headers are natively supported by:

* API gateways
* Rate limiters
* Reverse proxies
* WAFs and security filters

By placing authentication in headers, Pixela enables infrastructure-level enforcement without inspecting payloads.

---

## How Your Project Implements This Correctly

### Centralized Authentication Injection

```python
self.headers = {
    "X-USER-TOKEN": token,
    "Content-Type": "application/json",
}
```

This ensures:

* No UI or business layer can forget authentication
* No accidental token duplication in URLs
* No credential sprawl across the codebase

---

### Clean Responsibility Separation

| Layer        | Responsibility                            |
| ------------ | ----------------------------------------- |
| UI           | Collects user intent only                 |
| HabitManager | Expresses domain operations               |
| PixelaClient | Handles HTTP, headers, and authentication |
| Config       | Loads and validates secrets securely      |

This design makes authentication **non-optional**, **non-duplicated**, and **non-leaky**.

---

## Why Pixela Rejects API Keys in Query Parameters by Design

Pixela’s API design intentionally discourages this pattern because:

* URLs are inherently unsafe for secrets
* URLs are designed for identification, not authorization
* Caching layers treat URLs as cache keys
* Browsers and tooling expose URLs everywhere

Headers, by contrast, are ephemeral, contextual, and purpose-built for authorization data.

---

## Mental Model to Retain

> URLs identify *where*.
> Bodies describe *what*.
> Headers declare *who*.

Pixela’s authentication model aligns perfectly with HTTP’s original architectural intent, and your project applies it correctly and defensively without shortcuts.
