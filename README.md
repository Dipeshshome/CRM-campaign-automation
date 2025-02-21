#Petabytz Sales Agent
##Overview
The Petabytz Sales Agent is an automated lead management and outreach system designed to streamline sales campaigns. It automates email verification, outreach, and response analysis using the following integrations:

Hunter.io for email verification
Gmail SMTP and IMAP for email communication
Groq API for sentiment analysis of email responses
Google Sheets for lead management and tracking
APScheduler for scheduling tasks


##Key Features
Email Verification: Verifies lead email addresses using Hunter.io API.
Automated Email Outreach: Sends personalized emails to verified leads.
Response Analysis: Analyzes email responses for sentiment and summary using Groq's Chat Completion API.
Lead Management: Reads and updates lead information in Google Sheets.
Automated Scheduling: Uses APScheduler for periodic tasks such as lead monitoring and email response checking.
Logging: Detailed logging for debugging and monitoring.

##Project Architecture


petabytz_sales_agent/<br>
│   agent_a.py          # Handles email verification<br>
│   agent_b.py          # Manages email outreach and response analysis<br>
│   supervisor_agent.py # Supervises and assigns tasks to agents<br>
│   sheets_handler.py   # Interacts with Google Sheets<br>
│   main.py             # Entry point of the application<br>
│   config.py           # Configuration file for environment variables and settings<br>
│   requirements.txt    # Required dependencies<br>
│   crm_bot.service     # Systemd service file for deployment<br>
│   .env                # Environment variables (Not included in the repository)<br>
└───logs/
        app.log         # Application logs


##Modules Overview
1. Agent A (agent_a.py)
Purpose: Verifies email addresses using Hunter.io API.<br>
Main Functions:
verify_email(email): Verifies the email and checks if it's valid.
handle_verification(row, email): Handles the verification and updates the status in Google Sheets.
1. Agent B (agent_b.py)
Purpose: Handles email outreach and analyzes responses.
Main Functions:
send_email(to_email, lead_name): Sends a personalized email.
analyze_response(text): Analyzes the email response using Groq API.
check_email_response(to_email, row): Checks inbox for replies and analyzes them.
handle_outreach(row, lead_name, email): Manages the outreach process and updates Google Sheets.
1. Supervisor Agent (supervisor_agent.py)
Purpose: Supervises and delegates tasks to Agent A and Agent B.
Main Functions:
monitor_leads(): Checks Google Sheets for new leads and assigns them to agents.
check_responses(): Periodically checks for email responses.
assign_to_agent_a(row, lead): Assigns leads to Agent A for email verification.
assign_to_agent_b(row, lead): Assigns leads to Agent B for email outreach.
start_supervisor(): Starts the APScheduler for monitoring.
1. Sheets Handler (sheets_handler.py)
Purpose: Manages interaction with Google Sheets.
Main Functions:
get_google_sheets_service(): Authenticates and connects to Google Sheets API.
read_leads(): Reads lead data from Google Sheets.
update_lead(row, col, value): Updates lead data in Google Sheets.
1. Main (main.py)
Purpose: Entry point of the application.
Functionality:
Starts the Supervisor Agent.
Monitors leads and assigns them to Agent A or B.
Handles re-checks and status updates.
1. Configuration (config.py)
Purpose: Stores configuration details such as API keys, email credentials, and settings.
Best Practice: Sensitive credentials are loaded from .env file using dotenv.
Installation and Setup
1. Clone the Repository

git clone https://github.com/your_username/petabytz_sales_agent.git
cd petabytz_sales_agent
1. Create a Virtual Environment

python3 -m venv .venv
source .venv/bin/activate
1. Install Required Packages

pip install -r requirements.txt
1. Environment Variables
Create a .env file in the root directory with the following configuration:

env

# Google Sheets Configuration
SPREADSHEET_ID='your_spreadsheet_id'
SHEET_NAME='Leads'

# Email Configuration
FROM_EMAIL='your_email@example.com'
FROM_EMAIL_PASSWORD='your_email_password'
SMTP_SERVER='smtp.gmail.com'
SMTP_PORT=587

# IMAP Configuration
IMAP_SERVER='imap.gmail.com'
IMAP_PORT=993

# API Keys
GROQ_API_URL='https://api.groq.com/v1/chat/completions'
GROQ_API_KEY='your_groq_api_key'
HUNTER_API_KEY='your_hunter_api_key'

# Email Response Interval
EMAIL_RESPONSE_CHECK_INTERVAL=60
5. Google Sheets Authentication
Create a Google Cloud Service Account and download credentials.json.
Place credentials.json in the project root.
Share the Google Sheet with the service account email (e.g., your_service_account@project.iam.gserviceaccount.com).
Usage
Run the Application

python main.py
Deployment as a Systemd Service
1. Update crm_bot.service
ini

[Unit]
Description=Petabytz Sales Agent CRM Bot Service
After=network.target

[Service]
WorkingDirectory=/path/to/petabytz_sales_agent
ExecStart=/usr/bin/python3 main.py
Restart=always
User=your_username
Environment=PYTHONUNBUFFERED=1
EnvironmentFile=/path/to/petabytz_sales_agent/.env
StandardOutput=append:/path/to/petabytz_sales_agent/logs/app.log
StandardError=append:/path/to/petabytz_sales_agent/logs/error.log

[Install]
WantedBy=multi-user.target
1. Install and Start the Service

sudo cp crm_bot.service /etc/systemd/system/crm_bot.service
sudo systemctl daemon-reload
sudo systemctl start crm_bot.service
sudo systemctl enable crm_bot.service
1. Check Service Status

sudo systemctl status crm_bot.service
Future Enhancements
Asynchronous Processing: Implement async requests for faster execution.
Distributed Task Queue: Migrate to Celery and Redis for scalable task management.
Advanced NLP Analysis: Integrate more advanced NLP models for sentiment and intent analysis.

