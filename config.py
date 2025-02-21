# config.py

import logging

# Google Sheets Configuration
SPREADSHEET_ID = '1dEo6zg3FctdIl3a4igc64H4lLAxFZcAXYi7ij9H-VGM'
SHEET_NAME = 'Leads'

# Email Configuration
FROM_EMAIL = 'dshome.abc@gmail.com'
FROM_EMAIL_PASSWORD = ''
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# IMAP Configuration for Checking Responses
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993  # Default port for IMAP over SSL

EMAIL_RESPONSE_CHECK_INTERVAL = 60

GROQ_API_URL = "https://api.groq.com/v1/chat/completions"
GROQ_API_KEY = ''

# Hunter.io Configuration
HUNTER_API_KEY = ''

# Logging Configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


