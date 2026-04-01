## Python Scheduled Quote Email — Complete Professional Explanation

---

## 1. High-Level Purpose of This Script

This script implements a **day-based automated email sender** that:

* Runs anytime
* Checks the current weekday
* Sends an email **only on a specific day**
* Randomly selects content from a CSV
* Falls back safely if data or files are missing
* Sends a **proper MIME email (text + HTML)** using Gmail SMTP

This is a **clean example of real-world automation**, not a demo script.

---

## 2. Imports — Why Each One Exists

```python
import smtplib
import os
import pandas as pd
import datetime as dt
from email.message import EmailMessage
from dotenv import load_dotenv
```

### Purpose Breakdown

| Module         | Why It Is Used                         |
| -------------- | -------------------------------------- |
| `smtplib`      | SMTP protocol client (email transport) |
| `os`           | Access environment variables securely  |
| `pandas`       | CSV reading + random row selection     |
| `datetime`     | Weekday-based scheduling logic         |
| `EmailMessage` | RFC-compliant email construction       |
| `dotenv`       | Secure credential loading              |

This combination is **intentional and minimal**.

---

## 3. Environment Variable Handling (Security Layer)

```python
load_dotenv()

my_email = os.getenv("EMAIL")
my_password = os.getenv("PASSWORD")
```

### What This Achieves

* Credentials are **not hardcoded**
* `.env` file stays out of version control
* Code is portable across machines

### Safety Check

```python
if not my_email or not my_password:
    raise RuntimeError("EMAIL or PASSWORD not set in .env")
```

Why this matters:

* Fails **fast and loudly**
* Prevents silent authentication errors
* Professional-grade defensive programming

---

## 4. Date & Scheduling Logic

```python
now = dt.datetime.now()
day_to_send = "Friday"
```

* `now` captures the **current execution moment**
* `day_to_send` defines the **only allowed send day**

---

### Weekday Mapping

```python
week_dict = {
    0: "Monday", 1: "Tuesday", 2: "Wednesday",
    3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"
}
```

Why this exists:

* `datetime.weekday()` returns an integer
* Humans reason in names, not numbers
* Mapping improves readability and correctness

Used later as:

```python
week_dict[now.weekday()]
```

---

## 5. Email Object Construction (Correct Abstraction)

```python
msg = EmailMessage()
msg["From"] = my_email
msg["To"] = my_email
msg["Subject"] = f"{day_to_send} Quote for You"
```

### Why `EmailMessage` Is Used

* Handles headers correctly
* Prevents malformed emails
* Supports multipart messages
* Avoids manual string formatting bugs

This is the **right level of abstraction**.

---

## 6. Loading Quotes from CSV (Data Layer)

```python
quotes_df = pd.read_csv("quotes.csv")
```

Expected CSV structure:

```
quote,author
```

---

### Defensive Validation

```python
if quotes_df.empty:
    raise ValueError("Quotes file is empty")
```

Why:

* An empty CSV is worse than a missing one
* Forces fallback logic cleanly

---

### Random Quote Selection

```python
selected = quotes_df.sample(1).iloc[0]
quote = selected.get("quote", "...")
author = selected.get("author", "Unknown")
```

What this ensures:

* True randomness (`sample`)
* Safe dictionary-style access
* Default values if columns are missing

---

## 7. Robust Exception Handling (Production Behavior)

### File Missing

```python
except FileNotFoundError:
```

Fallback:

* Uses a default quote
* Script still succeeds
* No crash, no alert fatigue

---

### Any Other Unexpected Error

```python
except Exception:
```

This is intentional:

* Email automation should **degrade gracefully**
* Content failure should not stop scheduling logic

---

## 8. Plain Text Email Content (Mandatory)

```python
msg.set_content(f"""
{day_to_send} Quote

"{quote}"

— {author}

Have a calm, meaningful {day_to_send}.
""")
```

Why plain text matters:

* Required by email standards
* Used by:

  * Screen readers
  * Text-only clients
  * Spam filters
* Improves deliverability

Never skip this in professional systems.

---

## 9. HTML Alternative (Presentation Layer)

```python
msg.add_alternative(..., subtype="html")
```

### What This Adds

* Rich formatting
* Better user experience
* Still optional and safe

### Key Design Principles Used

* Inline CSS (email-safe)
* Fixed max width
* Neutral colors
* No JavaScript
* No external assets

This respects **email client limitations**.

---

## 10. Conditional Sending Logic (The Core Feature)

```python
if week_dict[now.weekday()] == day_to_send:
```

What this does:

* Compares **current weekday**
* Sends email **only if it matches**
* Makes script idempotent

This allows:

* Running via cron
* Running daily without duplication
* No external scheduler state needed

---

## 11. SMTP Transport (Correct Sequence)

```python
with smtplib.SMTP("smtp.gmail.com", 587) as connection:
    connection.starttls()
    connection.login(my_email, my_password)
    connection.send_message(msg)
```

### Transport Flow

```
SMTP connect
   ↓
STARTTLS encryption
   ↓
Authentication
   ↓
Message transfer
   ↓
Graceful close
```

Key points:

* Port `587` is correct
* TLS is mandatory
* `send_message` respects MIME boundaries

---

## 12. Terminal Feedback (Observability)

```python
print("Email sent successfully!")
```

or

```python
print("Not the scheduled day. Email not sent.")
```

Why this matters:

* Useful for cron logs
* Confirms correct branching
* No silent behavior

---

## 13. Execution Flow Summary

```
Load secrets
   ↓
Get current weekday
   ↓
Load quotes (or fallback)
   ↓
Build MIME email
   ↓
Check schedule condition
   ↓
Send or skip
```

---

## 14. Professional Assessment of This Code

### Strengths

* Secure credential handling
* Clear separation of concerns
* Defensive data access
* Deterministic scheduling
* Proper email construction
* Graceful failure paths

### Suitable For

* Personal automation
* Daily inspiration systems
* Internal notifications
* Cron-based jobs
* Learning production patterns

This is **well beyond beginner email scripting** and aligns with **real-world automation standards**.
