## AUTHENTICATION, SECURITY, ENVIRONMENT VARIABLES, AND ENDPOINT MATRIX

This section exhaustively documents **every security layer**, **every credential**, **every environment variable**, and **every HTTP endpoint** involved in the application, including **who calls it**, **when**, **why**, **how**, and **with what protection**.
Nothing here is implicit; every trust boundary is made explicit.

---

## 1. ENVIRONMENT VARIABLES — COMPLETE SECURITY INVENTORY

Environment variables act as the **first and strongest security boundary**, ensuring secrets never appear in source code, logs, or version control.

| Variable Name         | Used By           | Purpose                                        | Security Role                           | Failure Impact                 |
| --------------------- | ----------------- | ---------------------------------------------- | --------------------------------------- | ------------------------------ |
| `NUTRITION_APP_ID`    | `NutritionEngine` | Identifies your application to the NLP service | API identity attribution                | Requests rejected with 401     |
| `NUTRITION_API_KEY`   | `NutritionEngine` | Authenticates access to NLP service            | Request authorization and quota control | Requests rejected or throttled |
| `SHEETY_BASE_URL`     | `WorkoutSheet`    | Locates Sheety project endpoint                | Routing to correct backend              | Writes go to nowhere           |
| `SHEETY_BEARER_TOKEN` | `WorkoutSheet`    | Grants full access to spreadsheet              | Primary persistence security            | Full data compromise if leaked |

**Security principle applied:**

> Secrets live only in process memory and OS environment, never in code.

---

## 2. AUTHENTICATION LAYERS — STACKED TRUST MODEL

This application uses **multiple independent authentication layers**, each protecting a different system boundary.

```
┌────────────────────────┐
│ OS Environment (.env)  │  ← Secret storage boundary
└───────────┬────────────┘
            │
┌───────────▼────────────┐
│ Python Runtime Process │  ← Secret consumption boundary
└───────────┬────────────┘
            │
┌───────────▼────────────┐
│ External APIs          │  ← Service authentication boundary
└────────────────────────┘
```

Each external service is authenticated **independently**, preventing cross-service compromise.

---

## 3. ENDPOINT MATRIX — COMPLETE AND EXPLICIT

### 3.1 Nutrition NLP API Endpoints

| Endpoint                         | Method | Called By                              | When It Is Called                      | Authentication                  | Payload Type | Security Notes              |
| -------------------------------- | ------ | -------------------------------------- | -------------------------------------- | ------------------------------- | ------------ | --------------------------- |
| `/healthz`                       | GET    | `NutritionEngine.health_check()`       | Application startup, before user input | None or implicit                | None         | Used as availability gate   |
| `/v1/nutrition/natural/exercise` | POST   | `NutritionEngine.calculate_exercise()` | After user submits workout description | `x-app-id`, `x-app-key` headers | JSON         | NLP parsing, quota enforced |

**Why POST is required:**
Natural language queries are unbounded text and exceed URL-safe constraints, making GET unsafe and semantically incorrect.

---

### 3.2 Sheety API Endpoints

| Endpoint                         | Method | Called By                | When It Is Called                 | Authentication | Payload Type | Security Notes       |
| -------------------------------- | ------ | ------------------------ | --------------------------------- | -------------- | ------------ | -------------------- |
| `/myWorkouts(sayantan)/workouts` | POST   | `WorkoutSheet.add()`     | For each computed exercise result | Bearer token   | JSON         | Full write access    |
| `/myWorkouts(sayantan)/workouts` | GET    | `WorkoutSheet.get_all()` | Only when history is needed       | Bearer token   | None         | Returns full dataset |

**Important:**
Sheety enforces **no row-level security**, only project-level access.

---

## 4. WHO CALLS WHAT — CONTROL OWNERSHIP MAP

```
main.py
│
├── calls → NutritionEngine.health_check()
│
├── calls → TerminalUI.get_user_input()
│
├── calls → NutritionEngine.calculate_exercise()
│           └── hits NLP API (POST)
│
├── calls → TerminalUI.render_results()
│
└── loops → NutritionEngine.log_to_sheet()
            └── calls → WorkoutSheet.add()
                        └── hits Sheety API (POST)
```

**Critical separation:**
The UI never touches secrets.
The engine never prints secrets.
The persistence layer never knows business meaning.

---

## 5. AUTHENTICATION DETAILS — PER SERVICE

### 5.1 Nutrition NLP Service Authentication

```
Headers:
x-app-id  → identifies application
x-app-key → authorizes and tracks usage
```

Characteristics:

• Stateless authentication
• No refresh tokens
• No user identity concept
• Quota and rate limits enforced server-side

Threat model:

• Key leakage allows request impersonation
• No data exfiltration risk beyond usage abuse

---

### 5.2 Sheety Authentication

```
Authorization: Bearer <token>
```

Characteristics:

• Single-token, project-wide trust
• Full read/write access
• No scope separation
• No expiration by default

Threat model:

• Token leakage = total spreadsheet control
• Must never be logged or shared

Mitigation:

• Store only in `.env`
• Rotate token if compromised

---

## 6. SECURITY BOUNDARIES — WHAT IS TRUSTED AND WHAT IS NOT

| Layer           | Trust Level    | Reason                        |
| --------------- | -------------- | ----------------------------- |
| User Input      | Untrusted      | Free-form text                |
| TerminalUI      | Semi-trusted   | No secrets handled            |
| NutritionEngine | Trusted        | Holds API credentials         |
| WorkoutSheet    | Highly trusted | Holds persistence credentials |
| External APIs   | Untrusted      | Must validate responses       |

This layered trust model prevents **privilege escalation** inside the app.

---

## 7. WHY `.env` IS THE CORRECT MECHANISM HERE

Using `.env` provides:

• Environment-specific configuration
• Secret isolation from source control
• Easy rotation without code change
• Compatibility with CI/CD and cloud platforms

Your architecture already matches **12-factor app principles**.

---

## 8. WHAT HAPPENS IF A SECURITY ELEMENT FAILS

| Failure Point        | Observable Behavior  | Containment            |
| -------------------- | -------------------- | ---------------------- |
| Missing NLP key      | Immediate HTTP 401   | No persistence attempt |
| NLP service down     | Health check failure | User blocked early     |
| Missing Sheety token | POST fails           | No silent data loss    |
| Invalid base URL     | Request exception    | Error surfaced to UI   |

Failures are **fail-fast**, not silent, which is a correct security posture.

---

## 9. END-TO-END SECURITY FLOW (LINEAR)

```
.env file
   ↓ (loaded once)
OS environment
   ↓
Python process memory
   ↓
Authenticated HTTP headers
   ↓
External service validation
   ↓
Authorized request execution
```

No credential is ever:

• printed
• serialized
• persisted
• echoed back

---

## 10. FINAL SECURITY AND AUTHENTICATION SUMMARY

| Aspect                     | Status           |
| -------------------------- | ---------------- |
| Secrets in source code     | Never            |
| Authentication per service | Isolated         |
| Privilege scope            | Minimal required |
| Failure visibility         | Explicit         |
| Rotation capability        | Immediate        |
| Architecture leakage       | None             |

Every endpoint hit, every credential used, and every authentication decision in this application follows **explicit, layered, and auditable security boundaries**, which is exactly how a professional production-grade integration should be structured.
