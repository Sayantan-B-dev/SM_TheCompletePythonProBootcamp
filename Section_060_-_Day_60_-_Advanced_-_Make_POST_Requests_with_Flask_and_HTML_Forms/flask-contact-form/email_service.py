import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self, smtp_server, smtp_port, username, password, recipient):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.recipient = recipient

    def send_contact_email(self, name, email, phone, project_type, budget, message) -> Tuple[bool, str]:
        """Send a beautiful HTML email with all form fields."""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.username
            msg['To'] = self.recipient
            msg['Subject'] = f"New Contact Form: {project_type} from {name}"
            # Set Reply-To so you can reply directly to the user
            msg['Reply-To'] = email

            # Plain text fallback
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

            # HTML version – styled like a modern email
            html = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f4f4; padding: 20px; }}
                    .container {{ max-width: 600px; margin: auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
                    .header h1 {{ margin: 0; font-weight: 300; }}
                    .content {{ padding: 30px; }}
                    .field {{ margin-bottom: 20px; }}
                    .field-label {{ font-weight: 600; color: #333; margin-bottom: 5px; }}
                    .field-value {{ background: #f9f9f9; padding: 10px 15px; border-radius: 8px; color: #555; }}
                    .message-box {{ background: #f0f0f0; padding: 15px; border-radius: 8px; white-space: pre-wrap; }}
                    .footer {{ text-align: center; padding: 20px; color: #999; font-size: 0.9em; border-top: 1px solid #eee; }}
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
                        <div class="field">
                            <div class="field-label">📧 Email</div>
                            <div class="field-value">{email}</div>
                        </div>
                        <div class="field">
                            <div class="field-label">📞 Phone</div>
                            <div class="field-value">{phone or 'Not provided'}</div>
                        </div>
                        <div class="field">
                            <div class="field-label">🛠️ Project Type</div>
                            <div class="field-value">{project_type}</div>
                        </div>
                        <div class="field">
                            <div class="field-label">💰 Budget Range</div>
                            <div class="field-value">{budget}</div>
                        </div>
                        <div class="field">
                            <div class="field-label">💬 Message</div>
                            <div class="message-box">{message}</div>
                        </div>
                    </div>
                    <div class="footer">
                        Sent via your Flask contact form
                    </div>
                </div>
            </body>
            </html>
            """
            html_part = MIMEText(html, 'html')

            msg.attach(text_part)
            msg.attach(html_part)

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)

            logger.info(f"Email sent from {name} <{email}>")
            return True, "Your message has been sent successfully!"

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False, f"Failed to send email: {str(e)}"