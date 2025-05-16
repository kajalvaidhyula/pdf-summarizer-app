import smtplib
import ssl
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(recipient, summary):
    print("📨 Attempting to send email...")
    print(f"From: {EMAIL_SENDER}, To: {recipient}")

    try:
        msg = EmailMessage()
        msg['Subject'] = 'Your PDF Summary'
        msg['From'] = EMAIL_SENDER
        msg['To'] = recipient
        msg.set_content(summary)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        print("✅ Email sent successfully!")
        return True

    except Exception as e:
        print(f"❌ Error while sending email: {e}")
        return False
