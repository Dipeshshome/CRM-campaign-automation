# agent_a.py

import requests
from config import HUNTER_API_KEY, logger
from sheets_handler import update_lead

def verify_email(email):
    logger.debug(f"Verifying email: {email}")
    response = requests.get(f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={HUNTER_API_KEY}")
    data = response.json()
    logger.debug(f"Verification Result: {data}")
    return data.get('data', {}).get('status') == 'valid'

def handle_verification(row, email):
    is_valid = verify_email(email)
    status = "Y" if is_valid else "N"
    logger.debug(f"Email Verification Status for {email}: {status}")
    update_lead(row, 'F', status)
