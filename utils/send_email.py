from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import smtplib
import locale
import os


def send_email(html_content):
    # Email configuration
    smtp_server = "smtp.office365.com"
    smtp_port = 587
    sender_email = os.getenv('EMAIL_USERNAME')
    receiver_emails = ["imenaya@realmadrid.es", "rmaringm@realmadrid.es", "amine.bakkoury@keycapital.es"]
    password = os.getenv('EMAIL_PASSWORD')

    # Create a MIMEMultipart object
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    # Get today's date and format it
    today_date = datetime.today().strftime('%d de %B')

    # Capitalize the month name manually
    today_date_parts = today_date.split(' ')
    today_date_parts[2] = today_date_parts[2].capitalize()
    today_date = ' '.join(today_date_parts)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"RMCF Business Newsletter - {today_date}"
    msg["From"] = sender_email
    msg["To"] = ", ".join(receiver_emails)  # Join the list of recipient emails into a single string
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
