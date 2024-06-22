import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(html_content):
    # Email configuration
    smtp_server = "smtp.office365.com"
    smtp_port = 587
    sender_email = "rm_newsletter_test@hotmail.com"
    receiver_emails = ["amine.bakkoury@keycapital.es"]
    password = "Rmnewsletter24!"

    # Create a MIMEMultipart object
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "RMCF Business Newsletter"
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
