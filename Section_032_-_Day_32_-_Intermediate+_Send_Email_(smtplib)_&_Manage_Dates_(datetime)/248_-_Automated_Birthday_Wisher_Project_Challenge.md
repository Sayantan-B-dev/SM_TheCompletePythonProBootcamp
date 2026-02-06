# Pandas + Email in a Professional Startup

*A deep, system-level documentation focused on real business regulation, automation, and control*

---

## 1. Why Pandas + Email Is a Power Combination

Email is **communication**.
Pandas is **decision-making over data**.

Together, they enable:

> “Emails that are *computed*, not written.”

This is how startups move from:

* manual emails
  → rule-based emails
  → **data-governed communication systems**

---

## 2. Core Philosophy (Very Important)

In professional systems:

* **Pandas decides**
* **Email delivers**

Email must never contain business logic.
Pandas must never care about SMTP.

This separation is non-negotiable at scale.

---

## 3. Canonical File Structure (Production-Grade)

```
email_automation/
│
├── data/
│   ├── users.csv
│   ├── invoices.csv
│   ├── subscriptions.csv
│   ├── events.csv
│
├── templates/
│   ├── invoice_due.txt
│   ├── invoice_due.html
│   ├── onboarding.txt
│   ├── onboarding.html
│
├── logic/
│   ├── filters.py
│   ├── aggregations.py
│   ├── selectors.py
│
├── mail/
│   ├── builder.py
│   ├── sender.py
│
├── main.py
├── .env
└── requirements.txt
```

**Mental model**

* `data/` → facts
* `logic/` → decisions
* `templates/` → presentation
* `mail/` → transport

---

## 4. CSV Is Your First Database (And That’s Fine)

### 4.1 users.csv

```csv
user_id,email,name,signup_date,status
101,alice@company.com,Alice,2024-01-10,active
102,bob@company.com,Bob,2024-02-15,inactive
```

### 4.2 invoices.csv

```csv
invoice_id,user_id,amount,due_date,status
5001,101,1999,2025-02-01,unpaid
5002,102,999,2025-01-10,paid
```

### 4.3 subscriptions.csv

```csv
user_id,plan,expiry_date
101,pro,2025-02-05
102,free,2024-12-31
```

---

## 5. Example 1 — Invoice Reminder System

### Business Requirement

* Send emails only to users:

  * with unpaid invoices
  * due in the next 3 days
  * account still active

---

### 5.1 Pandas Logic (filters.py)

```python
import pandas as pd
import datetime as dt

def get_due_invoices():
    invoices = pd.read_csv("data/invoices.csv")
    users = pd.read_csv("data/users.csv")

    # Convert date strings to datetime
    invoices["due_date"] = pd.to_datetime(invoices["due_date"])

    today = dt.datetime.now()
    deadline = today + dt.timedelta(days=3)

    # Filter unpaid & due soon
    due = invoices[
        (invoices["status"] == "unpaid") &
        (invoices["due_date"] <= deadline)
    ]

    # Join with users
    merged = due.merge(users, on="user_id")

    # Only active users
    return merged[merged["status_y"] == "active"]
```

**What Pandas does here**

* Filters rows
* Applies time logic
* Joins datasets
* Produces a *decision-ready table*

---

### 5.2 Resulting DataFrame (Conceptual)

| user_id | email                                         | name  | amount | due_date   |
| ------- | --------------------------------------------- | ----- | ------ | ---------- |
| 101     | [alice@company.com](mailto:alice@company.com) | Alice | 1999   | 2025-02-01 |

Only **this row deserves an email**.

---

## 6. Example 2 — Email Builder (mail/builder.py)

```python
from email.message import EmailMessage

def build_invoice_email(row):
    msg = EmailMessage()

    msg["To"] = row["email"]
    msg["Subject"] = "Invoice Due Reminder"

    msg.set_content(
        f"""
Hi {row['name']},

Your invoice of ₹{row['amount']} is due on {row['due_date'].date()}.

Please make payment to avoid service interruption.
"""
    )

    return msg
```

**Key idea**

* Builder receives **data row**
* Produces **pure email**
* No Pandas here

---

## 7. Example 3 — Main Orchestrator (main.py)

```python
from logic.filters import get_due_invoices
from mail.builder import build_invoice_email
from mail.sender import send_email

df = get_due_invoices()

for _, row in df.iterrows():
    email = build_invoice_email(row)
    send_email(email)
```

This loop is **business-critical**:

* Every iteration = justified communication
* No spam
* No duplication

---

## 8. Example 4 — Subscription Expiry Alerts

### subscriptions.csv

```csv
user_id,plan,expiry_date
201,business,2025-02-03
202,pro,2025-03-10
```

### Pandas Logic

```python
def get_expiring_subscriptions(days=7):
    subs = pd.read_csv("data/subscriptions.csv")
    users = pd.read_csv("data/users.csv")

    subs["expiry_date"] = pd.to_datetime(subs["expiry_date"])
    cutoff = dt.datetime.now() + dt.timedelta(days=days)

    expiring = subs[subs["expiry_date"] <= cutoff]
    return expiring.merge(users, on="user_id")
```

Used for:

* Renewal nudges
* Retention campaigns
* Revenue protection

---

## 9. Example 5 — Business Health Digest (Internal Email)

### events.csv

```csv
event_type,count
signup,45
churn,3
payment_failure,7
```

### Aggregation Logic

```python
def daily_summary():
    df = pd.read_csv("data/events.csv")
    return df.groupby("event_type")["count"].sum()
```

Email content generated from **aggregates**, not raw data.

This is how **CXOs consume email**.

---

## 10. Anti-Patterns (Very Important)

### ❌ Email Logic Inside Pandas

```python
df.apply(lambda r: send_email(...))
```

Bad because:

* Impossible to test
* No observability
* Tight coupling

---

### ❌ Pandas Inside Email Builder

```python
pd.read_csv(...) inside email function
```

Violates separation of concerns.

---

## 11. Scaling Beyond CSV

| Stage         | Data Source    |
| ------------- | -------------- |
| MVP           | CSV            |
| Early startup | PostgreSQL     |
| Growth        | Data warehouse |
| Scale         | Event streams  |

**The Pandas logic stays almost identical**.

---

## 12. What This Makes You Capable Of

After mastering this pattern, you can:

* Build notification engines
* Regulate outbound emails
* Prevent spam by logic
* Generate compliance-safe communication
* Explain *why* every email was sent

This is **engineering control over communication**, not scripting.

---

## 13. Senior Mental Model (Final)

> Pandas defines *who deserves attention*
> Email simply delivers that attention

When communication becomes data-driven,
your startup becomes **predictable, ethical, and scalable**.
