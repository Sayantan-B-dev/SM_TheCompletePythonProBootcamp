import os
from email.message import EmailMessage
from pathlib import Path

TEMPLATE_DIR = Path("templates")

def load_template(filename: str) -> str:
    path = TEMPLATE_DIR / filename
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Template not found: {path}")

def build_birthday_email(name: str, recipient: str) -> EmailMessage:
    msg = EmailMessage()

    sender = os.getenv("EMAIL")
    if not sender:
        raise ValueError("EMAIL not set in environment")

    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = f"Happy Birthday, {name}!"

    # -----------------------------
    # LOAD & FORMAT TEMPLATES
    # -----------------------------
    text_template = load_template("birthday.txt")
    html_template = load_template("birthday.html")

    msg.set_content(text_template.format(name=name))
    msg.add_alternative(
        html_template.format(name=name),
        subtype="html"
    )

    return msg
