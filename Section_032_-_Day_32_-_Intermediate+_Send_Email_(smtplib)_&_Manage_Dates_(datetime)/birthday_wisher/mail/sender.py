import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()

class MailSender:
    def __init__(self):
        self.my_email = os.getenv("EMAIL")
        self.my_password = os.getenv("PASSWORD")

        if not self.my_email or not self.my_password:
            raise ValueError("EMAIL and PASSWORD must be set")

    def send_email(self, msg: EmailMessage):
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(self.my_email, self.my_password)
            connection.send_message(msg)
