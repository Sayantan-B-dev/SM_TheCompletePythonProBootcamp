import smtplib
import os
import pandas as pd
import datetime as dt

from email.message import EmailMessage
from dotenv import load_dotenv

# LOAD ENV
load_dotenv()

my_email = os.getenv("EMAIL")
my_password = os.getenv("PASSWORD")

if not my_email or not my_password:
    raise RuntimeError("EMAIL or PASSWORD not set in .env")

# DATE LOGIC
now = dt.datetime.now()
day_to_send = "Friday"

week_dict = {
    0: "Monday", 1: "Tuesday", 2: "Wednesday",
    3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"
}

# EMAIL OBJECT
msg = EmailMessage()
msg["From"] = my_email
msg["To"] = my_email
msg["Subject"] = f"{day_to_send} Quote for You"

# LOAD QUOTES
try:
    quotes_df = pd.read_csv("quotes.csv")

    if quotes_df.empty:
        raise ValueError("Quotes file is empty")

    selected = quotes_df.sample(1).iloc[0]
    quote = selected.get("quote", "Stay positive. Work hard. Make it happen.")
    author = selected.get("author", "Unknown")

except FileNotFoundError:
    quote = "Every day may not be good, but there is something good in every day."
    author = "Unknown"

except Exception:
    quote = "Keep going. You are doing better than you think."
    author = "Unknown"

# EMAIL CONTENT
msg.set_content(
f"""
{day_to_send} Quote 🌸

"{quote}"

— {author}

Have a calm, meaningful {day_to_send}.
"""
)

msg.add_alternative(
f"""
<html>
  <body style="background-color:#f6f8fa; font-family: Arial, Helvetica, sans-serif; padding:20px;">
    <div style="
        max-width:600px;
        margin:auto;
        background:#ffffff;
        padding:30px;
        border-radius:10px;
        box-shadow:0 4px 10px rgba(0,0,0,0.1);
    ">
      <h2 style="color:#2c3e50; text-align:center;">
        🌅 {day_to_send} Quote
      </h2>

      <p style="font-size:18px; color:#34495e; text-align:center;">
        “{quote}”
      </p>

      <p style="text-align:right; color:#7f8c8d;">
        — {author}
      </p>

      <hr style="border:none; border-top:1px solid #eee;">

      <p style="font-size:14px; color:#95a5a6; text-align:center;">
        Wishing you peace, clarity, and quiet strength today 🌿
      </p>
    </div>
  </body>
</html>
""",
    subtype="html"
)

# SEND MAIL (ONLY ON TARGET DAY)
if week_dict[now.weekday()] == day_to_send:
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(my_email, my_password)
        connection.send_message(msg)

    print("Email sent successfully!")
else:
    print("Not the scheduled day. Email not sent.")
