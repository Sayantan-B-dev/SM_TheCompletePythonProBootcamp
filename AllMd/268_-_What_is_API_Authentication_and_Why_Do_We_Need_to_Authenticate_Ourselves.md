## What API Authentication Is

API authentication is the mechanism used to **prove the identity of a caller** before an API allows access to its endpoints. It answers one fundamental question every API must ask on each request: **who is calling this API, and can they be trusted to do what they are asking**.

Authentication is not about what a caller is allowed to do; it is strictly about **verifying identity**. Authorization happens only after authentication succeeds.

---

## Why APIs Need Authentication

APIs operate without human supervision and are designed for automation. This makes them extremely powerful and extremely dangerous if identity is not enforced.

### Core Reasons Authentication Is Required

• APIs expose direct access to backend systems without UI safeguards
• APIs are trivial to script, replay, and brute-force at scale
• APIs often control business logic, not just data retrieval
• APIs act as shared infrastructure across multiple clients
• APIs are reachable globally, not just within a trusted network

Without authentication, an API cannot distinguish between a legitimate client and a malicious script.

---

## What Happens If Authentication Is Missing

Lack of authentication leads to predictable and repeatable failures.

• Anyone can impersonate legitimate users or applications
• Automated scraping and data harvesting becomes trivial
• Resource exhaustion through uncontrolled requests is inevitable
• Business workflows can be reverse-engineered and abused
• Legal, compliance, and privacy violations become unavoidable

An unauthenticated API is effectively **public infrastructure**, whether intended or not.

---

## When Authentication Is Not Required

Authentication is unnecessary only when **identity provides no security benefit**.

### Valid Conditions for No Authentication

• Data is intentionally public and already accessible elsewhere
• API is strictly read-only with no side effects
• No user-specific or proprietary data is exposed
• Abuse impact is limited to bandwidth and availability
• Business logic exposure carries no competitive risk

In these cases, authentication would only add friction and operational cost without improving safety.

---

## Authentication vs Authorization (Critical Distinction)

| Aspect            | Authentication               | Authorization                  |
| ----------------- | ---------------------------- | ------------------------------ |
| Question answered | Who are you                  | What can you do                |
| Happens when      | First step of request        | After identity is verified     |
| Implemented using | Keys, tokens, credentials    | Roles, scopes, permissions     |
| Failure result    | Request rejected immediately | Request rejected due to access |

Many security failures occur because these two concerns are conflated.

---

## Common API Authentication Methods

### 1. API Key Authentication

A simple shared secret issued to a client application.

**How it works**

• Client sends a static key with each request
• Server validates the key against stored records
• Identity is inferred from key ownership

**Typical usage**

• Public or partner APIs
• Low-risk or read-heavy endpoints
• Traffic attribution and rate limiting

**Limitations**

• No user identity, only application identity
• Keys are long-lived and easily leaked
• No fine-grained permission control

---

### 2. Basic Authentication

Credentials are sent with each request using HTTP headers.

**How it works**

• Username and password are Base64 encoded
• Credentials are transmitted on every request
• Server validates credentials directly

**Typical usage**

• Internal tools
• Temporary or legacy systems

**Limitations**

• Password exposure risk
• No session control
• Poor scalability and rotation

---

### 3. Token-Based Authentication

A short-lived token represents an authenticated session.

**How it works**

• User authenticates once using credentials
• Server issues a signed token
• Client sends token on subsequent requests

**Typical usage**

• Modern APIs
• Mobile and web applications

**Advantages**

• Credentials are not sent repeatedly
• Tokens can expire automatically
• Supports stateless servers

---

### 4. OAuth 2.0 (Industry Standard)

Delegated authentication using access tokens and scopes.

**How it works**

• Identity provider authenticates the user
• Client receives a scoped access token
• API validates token signature and claims

**Typical usage**

• User-facing platforms
• Third-party integrations
• Enterprise systems

**Advantages**

• Strong security guarantees
• Fine-grained permission scopes
• Token revocation and rotation

---

## How API Authentication Is Implemented (Step-by-Step)

### Step 1: Decide the Security Level

Authentication strength must match risk.

| API Risk Level         | Recommended Method |
| ---------------------- | ------------------ |
| Public, read-only      | No authentication  |
| Low to moderate        | API keys           |
| User-specific data     | Token-based auth   |
| Sensitive or regulated | OAuth 2.0 or mTLS  |

---

### Step 2: Client Sends Credentials or Token

Example using a bearer token in HTTP headers.

```http
GET /user/profile HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

The token represents a previously authenticated identity.

---

### Step 3: Server Validates the Identity

Server-side validation typically includes:

• Token signature verification
• Expiration time validation
• Issuer and audience checks
• Revocation or blacklist checks

---

### Step 4: Identity Context Is Established

After validation, the server attaches identity metadata to the request.

• User ID or application ID
• Roles or scopes
• Trust level

This context is then passed to authorization logic.

---

## Concrete Example: Token Authentication Flow

### Authentication Endpoint

```python
# This endpoint verifies credentials and issues a signed token
# Credentials are checked once to reduce repeated exposure

def login(username, password):
    if verify_credentials(username, password):
        token = generate_signed_token(
            user_id=username,
            expires_in=900  # short lifetime reduces blast radius
        )
        return {"access_token": token}
    else:
        return {"error": "Invalid credentials"}
```

**Expected Output**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### Protected API Endpoint

```python
# This endpoint requires a valid token for access
# The token is verified on every request

def get_profile(request):
    token = extract_bearer_token(request.headers)

    identity = verify_token(token)
    if not identity:
        return {"error": "Unauthorized"}, 401

    return {
        "user_id": identity.user_id,
        "profile": "profile data"
    }
```

**Expected Output (Authorized Request)**

```json
{
  "user_id": "sayantan",
  "profile": "profile data"
}
```

**Expected Output (Invalid Token)**

```json
{
  "error": "Unauthorized"
}
```

---

## Security Practices That Must Always Accompany Authentication

Authentication alone is insufficient without surrounding controls.

### Mandatory Supporting Measures

• HTTPS enforced at all times
• Short-lived tokens instead of permanent secrets
• Key and token rotation policies
• Rate limiting even for authenticated users
• Logging without storing sensitive credentials
• Immediate revocation on compromise detection

---

## Key Principle

API authentication exists to **establish trust before execution**.
The more damage an API can cause, the stronger and more layered the authentication must be.
