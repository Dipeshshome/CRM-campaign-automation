# agent_b.py

import smtplib
import imaplib
import requests
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import FROM_EMAIL, FROM_EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT, IMAP_SERVER, IMAP_PORT, GROQ_API_URL, GROQ_API_KEY, logger
from sheets_handler import update_lead

def send_email(to_email, lead_name):
    logger.debug(f"Sending email to: {to_email}")
    message = MIMEMultipart()
    message['From'] = FROM_EMAIL
    message['To'] = to_email
    message['Subject'] = 'Special Offer Just For You!'
    body = f"Hi {lead_name},\n\nWe have an exclusive offer for you!\n\nBest Regards,\nYour Company"
    message.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(FROM_EMAIL, FROM_EMAIL_PASSWORD)
    server.send_message(message)
    server.quit()

    logger.debug(f"Email sent successfully to {to_email}")
    return "Sent"

def analyze_response(text):
    """
    Analyze the email response using Groq's Chat Completion API.
    """
    logger.debug("Analyzing response with Groq Chat Completion API.")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    
    prompt = (
        "Analyze the following email response and provide the following details:\n"
        "- Sentiment (Positive, Negative, Neutral)\n"
        "- Summary of the response in one sentence\n"
        "\nEmail Response:\n"
        f"{text}\n"
        "\nAnalysis Format: Sentiment: <Sentiment>. Summary: <Summary>."
    )
    
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are an AI that analyzes email responses."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 100,
        "temperature": 0.3
    }

    try:
        response = requests.post(GROQ_API_URL, json=payload, headers=headers)
        response_data = response.json()
        logger.debug(f"Groq Chat Completion API Response: {response_data}")

        analysis = response_data.get("choices", [])[0].get("message", {}).get("content", "No analysis available.")
        
        return analysis
    except Exception as e:
        logger.error(f"Groq API Error: {e}")
        return "Analysis failed."

def check_email_response(to_email, row):
    """
    Check the Gmail inbox for a reply from the recipient.
    Analyze response with Groq Chat Completion API and update the Notes column.
    """
    logger.debug(f"Checking for response from: {to_email}")
    
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(FROM_EMAIL, FROM_EMAIL_PASSWORD)
    mail.select('inbox')

    status, data = mail.search(None, f'FROM "{to_email}"')
    mail_ids = data[0].split()

    if not mail_ids:
        logger.debug("No response received.")
        return "No Response"
    
    latest_email_id = mail_ids[-1]
    status, data = mail.fetch(latest_email_id, '(RFC822)')
    raw_email = data[0][1]
    email_message = email.message_from_bytes(raw_email)
    
    email_body = ""
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == 'text/plain':
                email_body += part.get_payload(decode=True).decode()
    else:
        email_body = email_message.get_payload(decode=True).decode()

    logger.debug(f"Email Body: {email_body}")

    # Analyze Response with Groq Chat Completion API
    analysis = analyze_response(email_body)
    logger.debug(f"Analysis Result: {analysis}")

    # Update Notes Column in Google Sheets
    update_lead(row, 'H', analysis)
    
    email_body = email_body.lower()
    if "interested" in email_body:
        return "Interested"
    elif "not interested" in email_body:
        return "Not Interested"
    else:
        return "No Response"

def handle_outreach(row, lead_name, email):
    logger.debug(f"Outreach Started for {lead_name} at {email}")
    # Send the email
    send_email(email, lead_name)
    logger.debug("Email Sent Successfully")

    # Update Google Sheets to indicate awaiting response
    update_lead(row, 'G', 'Awaiting Response')
    update_lead(row, 'H', 'Email Sent, Waiting for Response')
    logger.debug("Google Sheet Updated: Awaiting Response")

