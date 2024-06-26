from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from babel.dates import format_date
from datetime import datetime
import smtplib
import locale
import os


def send_email(html_content):
    # Email configuration
    smtp_server = "smtp.office365.com"
    smtp_port = 587
    sender_email = os.getenv('EMAIL_USERNAME')
    receiver_emails = os.getenv('RECEIVER_EMAIL')
    password = os.getenv('EMAIL_PASSWORD')

    # Create a MIMEMultipart object
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    # Get today's date and format it
    current_date = datetime.now()
    formatted_date = format_date(current_date, format='full', locale='es_ES')

    # Capitalize the month name manually
    formatted_date = formatted_date.split(' ')
    formatted_date[2] = formatted_date[2].capitalize()
    today_date = ' '.join(formatted_date)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"RMCF Business Newsletter - {today_date}"
    msg["From"] = sender_email
    msg["To"] = receiver_emails
    # msg["To"] = receiver_emails

    # Attach the HTML content to the email
    part = MIMEText(html_content, "html")
    msg.attach(part)

    # Send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_emails, msg.as_string())
            print("Email sent successfully")
    except Exception as e:
        print(f"Error: {e}")
