## STEP 5 — ADDING EMAIL NOTIFICATIONS (WHAT TO ADD, WHAT TO CHANGE, WHAT TO AVOID)

### 5.1 Purpose of STEP 5

STEP 5 introduces **outbound user notification** without corrupting the existing ingestion, enrichment, and persistence pipeline.
Email must be treated as **non-critical side-effect infrastructure**, never as a core dependency.

Core rule
Data ingestion and persistence must succeed **even if email fails completely**.

---

### 5.2 New Responsibilities Introduced

With email added, the system gains **one new concern**:

| Concern            | Critical | Can Fail Safely |
| ------------------ | -------- | --------------- |
| Flight ingestion   | Yes      | No              |
| Sheet persistence  | Yes      | No              |
| Email notification | No       | Yes             |

Email is **observational**, not structural.

---

### 5.3 What NEW FILES Should Be Added

```
email_client.py
```

Single responsibility

* Sending emails
* Formatting email content
* Handling SMTP or API-based email providers

This file must not know:

* Aviationstack
* Sheety
* Flight ingestion logic

---

### 5.4 Example Minimal Email Client (SMTP-Based)

```python
# email_client.py
import smtplib
from email.message import EmailMessage
from config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD
from notification import log, warn

def send_flight_email(subject: str, body: str) -> None:
    try:
        message = EmailMessage()
        message["From"] = EMAIL_USER
        message["To"] = EMAIL_USER
        message["Subject"] = subject
        message.set_content(body)

        with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as server:
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(message)

        log("Email notification sent successfully")

    except Exception as exc:
        warn(f"Email delivery failed: {exc}")
```

Design explanation

* Wrapped in `try/except` to avoid pipeline termination
* Uses `warn`, never `error`
* Failure is visible but non-fatal

---

### 5.5 Configuration Changes Required

Add to `.env`:

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=465
EMAIL_USER=example@gmail.com
EMAIL_PASSWORD=app_specific_password
```

Update `config.py`:

```python
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "0"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
```

Important rule
Email credentials must **never block startup**.
Do not include them in the mandatory `all([...])` validation.

---

### 5.6 Where Email Should Be Triggered (Correct Placement)

Email must be triggered **after STEP 3 succeeds**, never before.

Correct place inside `main.py`:

```python
from email_client import send_flight_email

write_flight_record(flight)

send_flight_email(
    subject=f"Flight Logged: {flight.get('flight_iata')}",
    body=f"Flight data stored successfully for {flight.get('airline_name')}"
)
```

Reason
This guarantees:

* No email for failed writes
* No false success notifications
* No dependency inversion

---

### 5.7 What Must NOT Be Changed

| Component          | Reason                           |
| ------------------ | -------------------------------- |
| aviation_client.py | Email must not pollute ingestion |
| sheet_writer.py    | Persistence must remain pure     |
| fun_facts.py       | Enrichment stays optional        |
| notification.py    | Logging ≠ user notification      |

Mixing email into these files introduces tight coupling and hidden failure paths.

---

### 5.8 Failure Behavior With Email Enabled

Scenario outcomes:

| Scenario    | Sheet       | Email    | Result               |
| ----------- | ----------- | -------- | -------------------- |
| All succeed | Written     | Sent     | Success              |
| Email fails | Written     | Failed   | Success with warning |
| Sheet fails | Failed      | Not sent | Hard stop            |
| API fails   | Not reached | Not sent | Hard stop            |

This preserves **data integrity above convenience**.

---

### 5.9 Optional Enhancements (Still Safe)

These can be added later without breaking design:

* Batch email summary after all flights processed
* Email only on failures, not success
* Rate-limited notifications
* HTML templates
* Provider swap to SendGrid or SES

All of these remain external to core steps.

---

### 5.10 Mental Model for STEP 5

```
STEP 1–3 = System truth
STEP 4   = System rules
STEP 5   = System voice
```

If STEP 5 ever crashes STEP 1–3, the design is wrong.
