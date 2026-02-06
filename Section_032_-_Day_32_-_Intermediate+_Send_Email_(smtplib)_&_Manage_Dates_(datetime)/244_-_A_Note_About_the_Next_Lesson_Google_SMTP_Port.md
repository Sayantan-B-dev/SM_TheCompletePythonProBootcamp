## Sending Email with Python (`smtplib`) — Clear, Practical Breakdown

---

## 1. What Problem This Lesson Solves

When using Python’s `smtplib` to send emails, a common error is:

```
Connection unexpectedly closed
```

This error almost always means **the SMTP connection was rejected** due to:

* Wrong SMTP server
* Wrong port
* Authentication restrictions
* Security policies of the email provider

This lesson explains **how SMTP actually works** and **why each configuration step is required**, especially for Gmail.

---

## 2. Choosing the Correct SMTP Server

SMTP servers are **provider-specific**.
If you connect to the wrong server, authentication will fail even with the correct password.

### Common Providers

| Provider | SMTP Server Address     |
| -------- | ----------------------- |
| Gmail    | `smtp.gmail.com`        |
| Hotmail  | `smtp.live.com`         |
| Outlook  | `outlook.office365.com` |
| Yahoo    | `smtp.mail.yahoo.com`   |

If your provider is not listed:

```
Search: "<provider name> SMTP server settings"
```

Why this matters:

> SMTP servers enforce strict identity rules.
> Logging into Gmail through Yahoo’s server is impossible.

---

## 3. Why Gmail Requires Extra Steps

Google **does not allow normal account passwords** for third-party apps like Python scripts.

### Reason

* Prevents credential theft
* Blocks automated abuse
* Enforces modern security standards

So Gmail requires:

* **2-Step Verification**
* **App Passwords**

---

## 4. Enabling 2-Step Verification (Mandatory)

### Steps

1. Go to:

```
https://myaccount.google.com/
```

2. Open:

```
Security → How you sign in to Google
```

3. Enable:

```
2-Step Verification
```

Why this is required:

> App Passwords only exist **after** 2-Step Verification is active.

---

## 5. Creating an App Password (Critical Step)

An **App Password** is a **one-time generated password** that:

* Works only for apps
* Cannot log into your Google account UI
* Can be revoked anytime

### Steps

1. In Google Account → Security
2. Search for:

```
App Passwords
```

3. Create a new password:

```
App name: Python Mail
```

You will receive:

```
A 16-character password (no spaces)
```

**Important**

> This password is shown **only once**.
> Store it securely.

---

## 6. Why Your Normal Password Will Fail

| Password Type           | Works with `smtplib` |
| ----------------------- | -------------------- |
| Google account password | ❌ No                 |
| App password            | ✅ Yes                |

Reason:

> Google blocks automated logins using real passwords.

---

## 7. Understanding SMTP Ports (Very Important)

### Default Behavior

```python
smtplib.SMTP("smtp.gmail.com")
```

This uses:

```
Port 25 (default)
```

### Why Port 25 Fails

* Historically abused for spam
* Blocked by ISPs
* Blocked by Gmail for client apps

---

## 8. Correct Port for Gmail

| Port    | Purpose                                |
| ------- | -------------------------------------- |
| 25      | Server-to-server (blocked for clients) |
| 465     | SSL (legacy)                           |
| **587** | **STARTTLS (recommended)**             |

**Always use port 587 for Gmail**

---

## 9. Correct SMTP Initialization (Required)

```python
import smtplib

# Create SMTP connection to Gmail using STARTTLS
server = smtplib.SMTP("smtp.gmail.com", port=587)

# Upgrade connection to secure encrypted channel
server.starttls()

# Login using email + APP PASSWORD
server.login("your_email@gmail.com", "YOUR_16_CHAR_APP_PASSWORD")

# Send email
server.sendmail(
    from_addr="your_email@gmail.com",
    to_addrs="recipient@example.com",
    msg="Subject: Test Email\n\nThis email was sent using Python."
)

# Close connection
server.quit()
```

### What Each Step Does

| Line              | Purpose                          |
| ----------------- | -------------------------------- |
| `SMTP(host, 587)` | Connects to Gmail’s SMTP gateway |
| `starttls()`      | Encrypts the connection          |
| `login()`         | Authenticates using app password |
| `sendmail()`      | Sends raw email                  |
| `quit()`          | Gracefully closes connection     |

---

## 10. Expected Output

If successful:

```
(no output, program exits cleanly)
```

If authentication fails:

```
SMTPAuthenticationError: 535-5.7.8 Username and Password not accepted
```

If port is wrong:

```
Connection unexpectedly closed
```

---

## 11. Common Failure Causes (Quick Diagnosis)

| Error                          | Likely Cause            |
| ------------------------------ | ----------------------- |
| Connection unexpectedly closed | Using port 25           |
| Authentication failed          | Used normal password    |
| SMTPServerDisconnected         | Forgot `starttls()`     |
| Timeout                        | Firewall / ISP blocking |

---

## 12. Mental Model to Remember

> **SMTP = Door + Lock + ID**
>
> * SMTP server → Door
> * Port → Which door is open
> * App password → Accepted ID
> * TLS → Secure hallway

If any part is wrong, the door closes immediately.
