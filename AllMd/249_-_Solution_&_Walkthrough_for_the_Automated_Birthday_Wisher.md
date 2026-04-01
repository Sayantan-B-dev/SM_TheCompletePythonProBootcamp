### 1️⃣ FULL PROJECT CODE — REWRITTEN WITH VERY DETAILED COMMENTS

(no logic changed, only comments added to explain *why* and *how*)

---

#### `data/birthdays.csv`

```csv
name,email,day,month
Sayantan Bharati,sayantanbharati611@gmail.com,6,2
Sayantan Bharati,sayantanbharati4@gmail.com,17,7
Sayantan Bharati,virus404beats@gmail.com,17,7
```

**What this file represents**

* This is the **data source**
* Each row = one person
* Columns:

  * `name` → used inside email template
  * `email` → receiver address
  * `day` + `month` → birthday matching logic

---

#### `logic/birthday_selector.py`

```python
import pandas as pd               # Used to read and filter CSV data
import datetime as dt             # Used to get today's date

class BirthdaySelector:
    def __init__(self, csv_path: str):
        # Read the CSV file into a pandas DataFrame
        # DataFrame is like an in-memory table
        self.birthdays = pd.read_csv(csv_path)

        # Capture current date and time ONCE
        # Stored so the same "today" value is reused
        self.today = dt.datetime.now()

    def get_birthdays(self):
        """
        Returns:
            A filtered DataFrame containing only rows
            whose day and month match today's date.
        """

        # Boolean filtering:
        # (month == today.month) AND (day == today.day)
        return self.birthdays[
            (self.birthdays["month"] == self.today.month) &
            (self.birthdays["day"] == self.today.day)
        ]
```

---

#### `mail/builder.py`

```python
import os
from email.message import EmailMessage
from pathlib import Path

# Directory where templates are stored
TEMPLATE_DIR = Path("templates")

def load_template(filename: str) -> str:
    """
    Loads a template file and returns its contents as a string.
    """

    path = TEMPLATE_DIR / filename

    try:
        # Open template file safely with UTF-8 encoding
        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    except FileNotFoundError:
        # Fail fast if template is missing
        raise FileNotFoundError(f"Template not found: {path}")

def build_birthday_email(name: str, recipient: str) -> EmailMessage:
    """
    Builds and returns a fully-formed EmailMessage object.
    """

    msg = EmailMessage()

    # Sender email loaded from environment variables
    sender = os.getenv("EMAIL")
    if not sender:
        raise ValueError("EMAIL not set in environment")

    # Email headers
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = f"Happy Birthday, {name}!"

    # Load both text and HTML templates
    text_template = load_template("birthday.txt")
    html_template = load_template("birthday.html")

    # Plain-text version (fallback for email clients)
    msg.set_content(text_template.format(name=name))

    # HTML version (rich formatting)
    msg.add_alternative(
        html_template.format(name=name),
        subtype="html"
    )

    return msg
```

---

#### `mail/sender.py`

```python
import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage

# Load variables from .env file into environment
load_dotenv()

class MailSender:
    def __init__(self):
        # Credentials from environment
        self.my_email = os.getenv("EMAIL")
        self.my_password = os.getenv("PASSWORD")

        if not self.my_email or not self.my_password:
            raise ValueError("EMAIL and PASSWORD must be set")

    def send_email(self, msg: EmailMessage):
        """
        Sends an EmailMessage using Gmail SMTP.
        """

        # Connect to Gmail SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()  # Encrypt the connection
            connection.login(self.my_email, self.my_password)
            connection.send_message(msg)
```

---

#### `main.py`

```python
from logic.birthday_selector import BirthdaySelector
from mail.builder import build_birthday_email
from mail.sender import MailSender

CSV_PATH = "data/birthdays.csv"

def main():
    # Initialize birthday logic
    selector = BirthdaySelector(CSV_PATH)

    # Initialize mail sender
    sender = MailSender()

    # Get people whose birthday is today
    birthdays = selector.get_birthdays()

    # If no birthdays, exit early
    if birthdays.empty:
        print("No birthdays today")
        return

    # Loop over matched rows
    for _, person in birthdays.iterrows():
        # Build personalized email
        msg = build_birthday_email(
            name=person["name"],
            recipient=person["email"]
        )

        # Send email
        sender.send_email(msg)

    print("Birthday emails sent successfully")

if __name__ == "__main__":
    main()
```

---

#### `templates/birthday.html`

```html
<html>
  <body style="font-family: Arial, sans-serif; background-color:#f6f8fa; padding:20px;">
    <div style="
        max-width:600px;
        margin:auto;
        background:#ffffff;
        padding:30px;
        border-radius:10px;
        box-shadow:0 4px 10px rgba(0,0,0,0.1);
    ">
      <h2>🎉 Happy Birthday, {name}!</h2>

      <p>
        Wishing you joy, peace, and success in the year ahead.
      </p>

      <p style="margin-top:30px; color:#555;">
        — Birthday Bot
      </p>
    </div>
  </body>
</html>
```

---

#### `templates/birthday.txt`

```txt
Hi {name},

Wishing you a very happy birthday 🎉
May the year ahead be calm, healthy, and fulfilling.

— Birthday Bot
```

---

## 2️⃣ DATA FLOW — END-TO-END (VERY IMPORTANT)

### Step 1: Program Entry

```python
if __name__ == "__main__":
    main()
```

* Python starts execution here
* Calls `main()`

---

### Step 2: Load Birthday Data

```python
selector = BirthdaySelector("data/birthdays.csv")
```

Inside constructor:

* `pd.read_csv()` loads CSV into memory
* `self.birthdays` becomes a **DataFrame**
* `self.today` stores **current date**

**Why store `today` once?**

* Prevents inconsistent results if date changes during runtime

---

### Step 3: Filter Today’s Birthdays

```python
birthdays = selector.get_birthdays()
```

Returned value:

* **DataFrame**
* Could be:

  * Empty → no birthdays
  * One or more rows → multiple emails

Key logic:

```python
(month == today.month) AND (day == today.day)
```

---

### Step 4: Guard Clause

```python
if birthdays.empty:
    print("No birthdays today")
    return
```

This prevents:

* Sending emails unnecessarily
* Running loops on empty data

---

### Step 5: Row-by-Row Processing

```python
for _, person in birthdays.iterrows():
```

Each `person` is:

* A **pandas Series**
* Behaves like a dictionary:

```python
person["name"]
person["email"]
```

---

### Step 6: Build Email

```python
msg = build_birthday_email(name, email)
```

Inside builder:

* Reads `.env` → sender email
* Loads templates
* Replaces `{name}`
* Constructs **EmailMessage object**

Returned value:

* `EmailMessage` (ready-to-send object)

---

### Step 7: Send Email

```python
sender.send_email(msg)
```

Internally:

* Connects to Gmail SMTP
* Encrypts connection
* Authenticates
* Sends email

---

## 3️⃣ TRICKY / NON-OBVIOUS DESIGN DECISIONS

### 1. Why Pandas Instead of CSV Reader?

* Easier filtering
* Cleaner boolean logic
* Scales better with large data

---

### 2. Why Separate Builder and Sender?

**Single Responsibility Principle**

* `builder.py` → *what the email looks like*
* `sender.py` → *how the email is sent*

Easy to:

* Replace Gmail
* Add SMS / WhatsApp later

---

### 3. Why Two Templates?

* Email clients vary
* Some don’t support HTML
* Plain text acts as fallback

---

### 4. Why `.env`?

* Credentials never hardcoded
* Safe for GitHub
* Environment-specific configs

---

### 5. Why `EmailMessage`?

* Handles MIME automatically
* Cleaner than raw SMTP strings
* Supports multipart messages naturally

---

### 6. Why `Path("templates")`?

* OS-independent
* Cleaner than string paths
* Safer file handling

---

## 4️⃣ WHAT EACH FUNCTION EXPECTS & RETURNS

| Function                 | Expects      | Returns                 |
| ------------------------ | ------------ | ----------------------- |
| `BirthdaySelector()`     | CSV path     | Object with loaded data |
| `get_birthdays()`        | Nothing      | Filtered DataFrame      |
| `load_template()`        | Filename     | Template string         |
| `build_birthday_email()` | Name, Email  | EmailMessage            |
| `send_email()`           | EmailMessage | None                    |

---

## 5️⃣ FAILURE MODES HANDLED

* Missing `.env` → raises error
* Missing template → raises error
* No birthdays → safe exit
* Invalid credentials → SMTP fails clearly

---

## 6️⃣ MENTAL MODEL (ONE LINE)

**CSV → Filter → Personalize → Build MIME → Secure SMTP → Send**

This project is clean, modular, production-grade, and extensible.
