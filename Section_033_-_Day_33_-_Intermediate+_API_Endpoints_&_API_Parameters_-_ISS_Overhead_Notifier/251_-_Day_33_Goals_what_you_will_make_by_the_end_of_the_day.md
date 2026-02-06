### What an API actually is (core idea)

An **API (Application Programming Interface)** is a **contract** that allows two separate software systems to communicate in a controlled, predictable way. One system exposes **capabilities**; the other system **requests** those capabilities without knowing the internal implementation.

Key abstraction:

* You do **not** access internal code or databases directly
* You interact only through **defined inputs and outputs**
* The provider controls **what is allowed**, **how**, and **under what rules**

Think of an API as a **publicly exposed function over a network**.

---

### Why APIs exist (real reasons, not textbook)

1. **Decoupling**
   Frontend, backend, mobile apps, and third-party services evolve independently.

2. **Security boundaries**
   Direct database access is dangerous; APIs enforce validation and permissions.

3. **Scalability**
   APIs allow load balancing, caching, and horizontal scaling.

4. **Reusability**
   Same API can serve web apps, mobile apps, scripts, IoT devices.

5. **Business control**
   Rate limits, billing, quotas, analytics, monetization.

---

### Types of APIs (important distinctions)

#### 1) Local APIs

Used inside the same machine or process.

* Python standard library (`os`, `math`)
* OS system calls

No network involved.

---

#### 2) Web APIs (most common)

Communicate over the internet using HTTP/HTTPS.

Subtypes:

**REST APIs** (dominant)

* Stateless
* Resource-oriented
* Uses HTTP verbs

**GraphQL APIs**

* Client chooses exact fields
* Single endpoint
* More complex server logic

**RPC / gRPC**

* Function-call semantics
* High performance
* Binary protocols

**SOAP** (legacy, enterprise)

* XML-based
* Strict schemas
* Heavy and verbose

---

### REST API anatomy (deep but practical)

A REST API exposes **resources**, not actions.

Example resource:

```
/users
/users/42
/orders/2026/items
```

Each resource supports **HTTP methods**:

| Method | Meaning | Effect           |
| ------ | ------- | ---------------- |
| GET    | Read    | No state change  |
| POST   | Create  | New resource     |
| PUT    | Replace | Full update      |
| PATCH  | Modify  | Partial update   |
| DELETE | Remove  | Deletes resource |

---

### HTTP request structure (exact mechanics)

A request has **four layers**:

1. **Method**

```
GET /users/42
```

2. **Headers** (metadata)

```
Authorization: Bearer <token>
Content-Type: application/json
```

3. **Query parameters**

```
/users?limit=10&page=2
```

4. **Body** (for POST/PUT/PATCH)

```json
{
  "name": "Alex",
  "email": "alex@example.com"
}
```

---

### HTTP response structure

1. **Status code**
2. **Headers**
3. **Body**

#### Status codes (must-know)

* 200 OK → success
* 201 Created → resource created
* 204 No Content → success, no body
* 400 Bad Request → client error
* 401 Unauthorized → no auth
* 403 Forbidden → auth but no permission
* 404 Not Found → resource missing
* 429 Too Many Requests → rate limit
* 500 Internal Server Error → server bug

---

### API authentication methods (critical topic)

#### 1) API Keys

* Simple token
* Sent via header or query
* Weak security if leaked

Used for public APIs.

---

#### 2) Basic Auth

```
username:password → base64
```

* Insecure unless HTTPS
* Rare today

---

#### 3) Bearer Tokens (most common)

```
Authorization: Bearer eyJhbGciOi...
```

* Stateless
* Used with JWT or opaque tokens

---

#### 4) OAuth 2.0 (industry standard)

Used by Google, GitHub, Facebook.

Flow:

1. User logs in via provider
2. Provider returns token
3. App uses token to access API

Supports:

* Scopes
* Expiry
* Refresh tokens

---

### JWT (JSON Web Token) explained clearly

A JWT is **not encryption**, it is **signed data**.

Structure:

```
header.payload.signature
```

Payload contains:

* user_id
* role
* expiration

Server verifies signature → trusts content.

Stateless authentication.

---

### API versioning (real-world necessity)

APIs evolve. Breaking clients is unacceptable.

Common patterns:

```
/api/v1/users
/api/v2/users
```

or

```
Accept: application/vnd.app.v2+json
```

Versioning prevents system-wide outages.

---

### Rate limiting (why APIs block you)

APIs limit requests to:

* Prevent abuse
* Protect infrastructure
* Enforce paid tiers

Common rules:

* 100 requests/minute
* 10 requests/second

Response when exceeded:

```
429 Too Many Requests
```

---

### API design principles (professional-grade)

1. **Statelessness**
   No session stored on server.

2. **Idempotency**
   Repeating a request should not break state.

3. **Consistent naming**

```
/users/{id}/orders
```

4. **Predictable errors**

```json
{
  "error": "INVALID_EMAIL",
  "message": "Email format is incorrect"
}
```

5. **Proper status codes**
   Never misuse 200 for errors.

---

### API documentation standards

Good APIs always provide:

* Endpoint list
* Parameters
* Request examples
* Response examples
* Error cases

Popular tools:

* OpenAPI / Swagger
* Postman collections

---

### API security risks (important)

* Exposed secrets in frontend
* Missing rate limits
* SQL injection via APIs
* Broken object-level authorization
* Improper CORS configuration

Most data breaches happen at the API layer.

---

### How APIs are used in real systems

Frontend:

* Calls API via HTTP
* Displays data

Backend:

* Validates request
* Applies business logic
* Talks to database
* Returns response

Mobile apps:

* Same API
* Different client

Automation:

* Python scripts
* Cron jobs
* CI/CD pipelines

---

### API vs SDK (common confusion)

* **API** → communication contract
* **SDK** → helper library that wraps the API

SDKs are optional. APIs are not.

---

### Mental model to remember

API = **controlled doorway**

* Request = knock
* Headers = credentials
* Body = instructions
* Response = result

You never see what happens behind the door — and that’s the point.

If you want next:

* Building an API from scratch
* Designing a secure API
* API testing with Postman
* API integration in Python
* Real-world API architecture

Say which direction to go.
