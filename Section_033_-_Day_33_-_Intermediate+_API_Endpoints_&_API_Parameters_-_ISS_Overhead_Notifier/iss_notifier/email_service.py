import smtplib
from email.message import EmailMessage
from config import EMAIL, PASSWORD, RECIPIENT_EMAIL, SMTP_SERVER, SMTP_PORT

def build_email(h1: str, p1: str) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = "ISS Overhead Notification"
    msg["From"] = EMAIL
    msg["To"] = RECIPIENT_EMAIL

    msg.add_alternative(f"""
    <html>
        <body>
            <h1>{h1}</h1>
            <p>{p1}</p>
        </body>
    </html>
    """, subtype="html")

    return msg

def send_email(h1: str, p1: str):
    msg = build_email(h1, p1)
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
