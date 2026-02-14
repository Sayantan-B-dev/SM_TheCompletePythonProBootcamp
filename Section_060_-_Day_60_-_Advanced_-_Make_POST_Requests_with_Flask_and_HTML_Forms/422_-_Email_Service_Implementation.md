## Step 4: Email Service Implementation

The email service is encapsulated in the `EmailService` class within `email_service.py`. This class is responsible for constructing professional-looking emails and delivering them via SMTP (Simple Mail Transfer Protocol). By isolating this logic, the application maintains a clean separation between web handling and email delivery, making the code more modular, testable, and maintainable.

### 4.1 Class Definition and Initialization

```python
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Tuple

class EmailService:
    def __init__(self, smtp_server, smtp_port, username, password, recipient):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.recipient = recipient
```

**Explanation:**

- **`smtplib`**: Python's built-in library for sending emails using SMTP.
- **`email.mime` modules**: Provide classes to construct email messages with various content types (plain text, HTML, attachments).
- **`__init__`**: The constructor stores the SMTP configuration and recipient address. These values are passed from `app.py` after being read from environment variables. This design allows the same service to be reused for multiple requests without re-reading configuration.

### 4.2 The Core Method: `send_contact_email`

```python
def send_contact_email(self, name, email, phone, project_type, budget, message) -> Tuple[bool, str]:
    """Send a beautiful HTML email with all form fields."""
    try:
        # Email construction and sending logic
        ...
        return True, "Your message has been sent successfully!"
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False, f"Failed to send email: {str(e)}"
```

- **Parameters**: All form fields are passed as strings.
- **Return type**: A tuple `(bool, str)`. The boolean indicates success or failure; the string is a user-friendly message.
- **Error handling**: Wrapped in a `try-except` block to catch any exceptions (network issues, authentication failures, etc.). On success, logs an info message; on failure, logs an error and returns a failure message.

### 4.3 Building the Email Message

#### 4.3.1 Creating a Multipart Container

```python
msg = MIMEMultipart('alternative')
msg['From'] = self.username
msg['To'] = self.recipient
msg['Subject'] = f"New Contact Form: {project_type} from {name}"
msg['Reply-To'] = email
```

- **`MIMEMultipart('alternative')`**: This creates a container that can hold multiple versions of the same message (plain text and HTML). Email clients will display the richest version they support.
- **Headers**:
  - `From`: The sender's email address (must match the authenticated user).
  - `To`: The recipient who will receive the inquiry.
  - `Subject`: A descriptive subject line including the project type and sender's name.
  - `Reply-To`: This header tells email clients to direct replies to the user who submitted the form, not to the SMTP sender. This is a critical usability feature.

#### 4.3.2 Creating the Plain Text Version

```python
text = f"""
Name: {name}
Email: {email}
Phone: {phone}
Project Type: {project_type}
Budget: {budget}

Message:
{message}
"""
text_part = MIMEText(text, 'plain')
```

- A simple, readable plain-text representation of the form data. This ensures that users with plain-text-only email clients can still read the inquiry.
- `MIMEText` with subtype `'plain'` marks this part as plain text.

#### 4.3.3 Creating the HTML Version

```python
html = f"""
<html>
<head>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f4f4; padding: 20px; }}
        .container {{ max-width: 600px; margin: auto; background: white; border-radius: 12px; ... }}
        ...
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>New Project Inquiry</h1>
        </div>
        <div class="content">
            <div class="field">
                <div class="field-label">👤 Name</div>
                <div class="field-value">{name}</div>
            </div>
            <!-- other fields similarly -->
        </div>
        <div class="footer">
            Sent via your Flask contact form
        </div>
    </div>
</body>
</html>
"""
html_part = MIMEText(html, 'html')
```

- The HTML version uses inline CSS to style the email as a modern, visually appealing card.
- All user-provided data is interpolated into the HTML. Note that this interpolation is safe because the data is text; however, in a more complex application, you might want to escape HTML entities to prevent injection (though email clients do not execute scripts).
- The `MIMEText` with subtype `'html'` marks this as HTML content.

#### 4.3.4 Attaching Both Versions

```python
msg.attach(text_part)
msg.attach(html_part)
```

- Both parts are attached to the multipart container. When an email client receives the message, it will choose the most appropriate part (usually HTML if supported, otherwise plain text).

### 4.4 Sending the Email via SMTP

```python
with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
    server.starttls()
    server.login(self.username, self.password)
    server.send_message(msg)
```

- **`smtplib.SMTP`**: Establishes a connection to the SMTP server.
- **`with` statement**: Ensures the connection is properly closed after the block, even if an exception occurs.
- **`starttls()`**: Upgrades the connection to TLS (Transport Layer Security) for encryption. This is essential for sending credentials securely.
- **`login()`**: Authenticates using the provided username and password. For Gmail, this may require an "App Password" if two-factor authentication is enabled.
- **`send_message(msg)`**: Sends the fully constructed email. This method handles the SMTP envelope and content delivery.

### 4.5 Logging and Return Values

```python
logger.info(f"Email sent from {name} <{email}>")
return True, "Your message has been sent successfully!"
```

On success, an info-level log is recorded, and a success message is returned to the caller (which will be passed to the frontend).

### 4.6 Exception Handling

```python
except Exception as e:
    logger.error(f"Failed to send email: {e}")
    return False, f"Failed to send email: {str(e)}"
```

- Any exception (e.g., connection refused, authentication failure, timeout) is caught.
- The error is logged with details (useful for debugging).
- A failure message is returned to the caller, which the frontend displays to the user.

### 4.7 Why Use Both Plain Text and HTML?

- **Plain text** guarantees readability on all devices and email clients, including those with limited HTML support.
- **HTML** provides a richer, branded experience that can improve user engagement and readability.
- The `multipart/alternative` structure ensures the client displays the most suitable version.

### 4.8 Security Considerations

- **Credentials**: The username and password are stored in environment variables, not in the code.
- **TLS**: Using `starttls()` encrypts the communication with the SMTP server.
- **Reply-To**: Prevents the recipient from accidentally replying to the SMTP sender (which might be a no-reply address) and instead replies directly to the inquirer.
- **Data interpolation**: In this simple case, no escaping is needed because the content is plain text inserted into HTML. However, for a production system, consider using a templating engine that auto-escapes.

### 4.9 Testing the Email Service

To test this service independently, you could create a small script:

```python
from email_service import EmailService

service = EmailService('smtp.gmail.com', 587, 'your-email@gmail.com', 'app-password', 'recipient@example.com')
success, message = service.send_contact_email('John Doe', 'john@example.com', '1234567890', 'Web Development', '$1000-$5000', 'Hello, I need a website.')
print(success, message)
```

This would attempt to send a test email without running the full Flask app.

### 4.10 Summary

The `EmailService` class abstracts all email functionality into a reusable component. It constructs a well-formatted, multipart email, securely connects to an SMTP server, and handles errors gracefully. By keeping this logic separate, the main Flask application remains focused on request handling and validation, leading to cleaner, more maintainable code.