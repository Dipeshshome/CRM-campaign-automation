# test_email.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import FROM_EMAIL, FROM_EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT

def send_test_email():
    to_email = 'dshome.dbsl@example.com'
    subject = 'Test Email from Sales CRM'
    body = 'This is a test email to verify the SMTP configuration.'

    message = MIMEMultipart()
    message['From'] = FROM_EMAIL
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(FROM_EMAIL, FROM_EMAIL_PASSWORD)
        server.send_message(message)
        server.quit()

        print(f"Test email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send test email: {e}")

if __name__ == "__main__":
    send_test_email()
