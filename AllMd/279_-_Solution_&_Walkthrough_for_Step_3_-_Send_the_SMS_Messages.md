## WHATSAPP SMS (ALERTING) DOMAIN — COMPLETE DATA FLOW, ARCHITECTURE, AND EXECUTION ANALYSIS

---

## 1. External Dependencies and Installed Components for WhatsApp Alerting

### 1.1 Python Libraries Used

* `twilio` Python SDK is required to communicate with the Twilio REST API for WhatsApp message delivery.
* Standard library modules such as `os`, `time`, and `pathlib` are used for environment configuration, cooldown timing, and lightweight persistence.

These dependencies intentionally keep the alerting subsystem small, synchronous, and operationally predictable.

---

## 2. External Service and Messaging Platform

### 2.1 Messaging Provider

* The project uses **Twilio** as the sole messaging gateway.
* WhatsApp delivery is performed through Twilio’s **WhatsApp Business API integration**, not through direct WhatsApp endpoints.

### 2.2 Messaging Channel

* Messages are sent using **WhatsApp** via Twilio’s sandbox or approved WhatsApp sender number.
* This approach avoids reverse engineering WhatsApp and ensures policy-compliant delivery.

---

## 3. Authentication and Configuration Workflow

### 3.1 Environment Variables Used

All WhatsApp-related secrets and identifiers are loaded at runtime via environment variables.

* `TWILIO_ACCOUNT_SID`
  Identifies the Twilio account and scopes API access.

* `TWILIO_AUTH_TOKEN`
  Secret token used to authenticate REST API calls.

* `TWILIO_WHATSAPP_NUMBER`
  The Twilio-provisioned WhatsApp sender number.

* `MY_PHONE_NUMBER`
  The destination WhatsApp number receiving alerts.

No credentials are hardcoded, preventing accidental leaks and simplifying deployment across environments.

---

## 4. File-Level Ownership and Responsibility

### 4.1 whatsapp.py as a Dedicated Infrastructure Module

* All WhatsApp-related behavior is isolated inside `whatsapp.py`.
* No other module is allowed to interact directly with Twilio APIs.
* This enforces a strict boundary between business logic and external messaging infrastructure.

---

## 5. Cooldown and Rate-Control Strategy

### 5.1 Motivation for Cooldown Enforcement

* Prevents alert spam during volatile markets.
* Avoids Twilio usage quota exhaustion.
* Ensures alerts retain informational value rather than becoming noise.

### 5.2 Cooldown Configuration

```python
COOLDOWN_SECONDS = 12 * 60 * 60
```

This enforces a twelve-hour minimum gap between WhatsApp alerts.

---

## 6. Persistent Cooldown State Tracking

### 6.1 Lock File Mechanism

```python
LOCK_FILE = Path("whatsapp_last_sent.txt")
```

* Stores the Unix timestamp of the last successful alert.
* Provides persistence across program restarts.
* Avoids in-memory state loss when executed via cron or scheduler.

---

## 7. Cooldown Eligibility Algorithm

### 7.1 `_can_send()` Function

**Purpose**
Determines whether an alert is allowed to be sent at the current time.

**Algorithm Flow**

* If the lock file does not exist, sending is immediately permitted.
* If the file exists, its contents are read and parsed as a float timestamp.
* The current system time is compared against the stored value.
* Sending is permitted only if the elapsed duration exceeds the cooldown window.

**Edge Case Handling**

* If file content is corrupted or unreadable, sending is allowed by default.
* This prevents permanent lockout due to filesystem or parsing errors.

**Return Value**

* Boolean indicating whether sending is allowed.

---

## 8. Cooldown State Update Logic

### 8.1 `_mark_sent()` Function

**Purpose**
Persists the timestamp of a successful alert send.

**Behavior**

* Writes the current Unix timestamp to the lock file.
* Overwrites any existing value to maintain a single source of truth.

This guarantees consistent cooldown enforcement across executions.

---

## 9. Primary WhatsApp Alert Function

### 9.1 `send_whatsapp_alert(message: str) -> bool`

**Purpose**
Sends a WhatsApp alert message using Twilio, while enforcing cooldown and configuration safety.

---

## 10. Step-by-Step Execution Algorithm

### 10.1 Cooldown Check

* Calls `_can_send()`.
* Immediately exits if cooldown has not expired.

### 10.2 Credential Validation

* Reads all required environment variables.
* If any required value is missing, execution stops silently.
* This avoids raising runtime exceptions in production.

### 10.3 Twilio Client Initialization

```python
client = Client(account_sid, auth_token)
```

* Establishes an authenticated REST client.
* No global client is reused, preventing stale or invalid sessions.

### 10.4 Message Dispatch

```python
client.messages.create(
    body=message,
    from_=f"whatsapp:{from_number}",
    to=f"whatsapp:{to_number}",
)
```

* Explicit `whatsapp:` prefix ensures correct channel routing.
* Message body is passed verbatim without formatting assumptions.

### 10.5 Post-Send State Update

* `_mark_sent()` is called only after successful message creation.
* Prevents false cooldown activation on failed attempts.

### 10.6 Return Contract

* Returns `True` if message was sent successfully.
* Returns `False` for all failure paths.

---

## 11. Invocation Context Within the Project

### 11.1 Where the Alert Is Triggered

* Called exclusively from `main.py`.
* Invocation occurs only when:

  * Asset type is valid.
  * Stock percentage change exceeds the defined threshold.
  * NEWS retrieval is also triggered.

This ensures alerts represent **high-confidence, high-signal events**.

---

## 12. Variables Used in the WhatsApp Workflow

### 12.1 Configuration Variables

* `LOCK_FILE`
* `COOLDOWN_SECONDS`

### 12.2 Runtime Variables

* `account_sid`
* `auth_token`
* `from_number`
* `to_number`
* `message`

Each variable has a single responsibility and no cross-module mutation.

---

## 13. Edge Cases Explicitly Handled

* Missing or misconfigured Twilio credentials.
* Cooldown violations.
* Filesystem corruption or missing lock file.
* Network or Twilio API exceptions.
* Partial failures where message sending fails mid-process.

All failures fail safely without interrupting the rest of the program.

---

## 14. Why the WhatsApp Workflow Is Correct and Robust

* Messaging is strictly opt-in based on market significance.
* Cooldown prevents alert storms during high volatility.
* Infrastructure failures never crash the application.
* Credentials are validated before attempting API calls.
* Side effects occur only after confirmed success.

---

## 15. Mental Model of WhatsApp Alert Flow

```
Market Signal Confirmed
   ↓
Cooldown Eligibility Check
   ↓
Credential Validation
   ↓
Twilio Client Initialization
   ↓
WhatsApp Message Dispatch
   ↓
Persistent Cooldown Update
   ↓
Silent Success or Safe Failure
```

This WhatsApp subsystem functions as a **controlled, rate-limited notification channel**, translating verified market signals into timely human alerts while maintaining operational safety, external API compliance, and long-term reliability.
