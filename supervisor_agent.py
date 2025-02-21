# supervisor_agent.py
from agent_a import handle_verification
from agent_b import handle_outreach, check_email_response
from sheets_handler import read_leads, update_lead
from config import logger, EMAIL_RESPONSE_CHECK_INTERVAL  # Import logger and interval
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

def monitor_leads():
    """
    Monitors Google Sheets for new leads and assigns them to Agent A or Agent B.
    """
    logger.debug("Monitoring Google Sheets for new leads.")
    leads = read_leads()
    for i, lead in enumerate(leads):
        if lead[5] == "":  # Email Verified is empty
            logger.debug(f"Lead needs verification: {lead}")
            assign_to_agent_a(i + 2, lead)
        elif lead[5] == "Y" and lead[6] == "":  # Verified but no Response Status
            logger.debug(f"Lead needs outreach: {lead}")
            assign_to_agent_b(i + 2, lead)

def check_responses():
    """
    Periodically checks for email responses and updates Google Sheets accordingly.
    """
    logger.debug("Scheduled Check: Monitoring Google Sheets for responses.")
    leads = read_leads()
    
    for i, lead in enumerate(leads):
        # Check for responses only for leads marked as Awaiting Response
        if lead[5] == "Y" and lead[6] == "Awaiting Response":
            to_email = lead[1]
            lead_name = lead[0]
            logger.debug(f"Checking response for: {lead_name} ({to_email})")
            
            # Check the email response
            response_status = check_email_response(to_email, i + 2)
            logger.debug(f"Response Status for {lead_name}: {response_status}")
            
            # Update Google Sheets with the response status
            if response_status != "No Response":
                update_lead(i + 2, 'G', response_status)  # Update Response Status
                update_lead(i + 2, 'H', f"Response Analyzed: {response_status}")
            else:
                logger.debug("No response to update.")

def assign_to_agent_a(row, lead):
    """
    Assigns lead to Agent A for email verification.
    """
    logger.debug(f"Assigning Lead to Agent A: {lead}")
    update_lead(row, 'H', 'Assigned to A')  # Update Notes Column
    handle_verification(row, lead[1])  # Call Agent A for email verification

def assign_to_agent_b(row, lead):
    """
    Assigns lead to Agent B for email outreach.
    """
    logger.debug(f"Assigning Lead to Agent B: {lead}")
    update_lead(row, 'H', 'Assigned to B')  # Update Notes Column
    handle_outreach(row, lead[0], lead[1])  # Call Agent B for email outreach

def start_supervisor():
    """
    Starts the Supervisor Agent using APScheduler.
    """
    logger.debug("Starting Supervisor Agent.")
    
    jobstores = {
        'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
    }
    scheduler = BackgroundScheduler(jobstores=jobstores)
    scheduler.add_job(monitor_leads, 'interval', minutes=1)
    scheduler.add_job(monitor_leads, 'interval', minutes=EMAIL_RESPONSE_CHECK_INTERVAL)
    scheduler.start()
