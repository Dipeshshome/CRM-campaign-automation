# sheets_handler.py

from google.oauth2 import service_account
from googleapiclient.discovery import build
from config import SPREADSHEET_ID, SHEET_NAME, logger  # Import logger

# Google Sheets Authentication
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials.json'

def get_google_sheets_service():
    logger.debug("Authenticating with Google Sheets API.")
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    return service

def read_leads():
    logger.debug("Reading leads from Google Sheets.")
    service = get_google_sheets_service()
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=SHEET_NAME, majorDimension='ROWS').execute()
    values = result.get('values', [])

    normalized_leads = []
    for row in values[1:]:  # Skip header row
        row += [""] * (8 - len(row))  # Ensure each row has 8 elements
        row = [cell if cell != "(empty)" else "" for cell in row]  # Convert "(empty)" to ""
        normalized_leads.append(row)

    logger.debug(f"Leads Fetched and Normalized: {normalized_leads}")
    return normalized_leads


def update_lead(row, col, value):
    logger.debug(f"Updating Google Sheet at row {row}, column {col} with value '{value}'.")
    service = get_google_sheets_service()
    sheet = service.spreadsheets()
    range_ = f"{SHEET_NAME}!{col}{row}"
    body = {'values': [[value]]}
    sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=range_, valueInputOption='USER_ENTERED', body=body).execute()
    logger.debug("Update Successful.")
