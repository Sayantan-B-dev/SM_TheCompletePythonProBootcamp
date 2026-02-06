import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

my_email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

# =========================
# BUILD A STYLISH EMAIL
# =========================
msg = EmailMessage()

msg["From"] = f"Sayantan <{my_email}>"
msg["To"] = my_email
msg["Subject"] = "✨ Hello from your Python App!"

msg.set_content(
    """

"""
)

msg.add_alternative(
    """

""",
    subtype="html"
)

with smtplib.SMTP("smtp.gmail.com", 587) as connection:
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.send_message(msg)
