# main.py

from supervisor_agent import start_supervisor
from agent_a import handle_verification
from agent_b import handle_outreach
from sheets_handler import read_leads
from config import logger

def main():
    logger.debug("Starting Sales Campaign CRM System.")
    start_supervisor()
    
    # Read Leads
    leads = read_leads()
    for i, lead in enumerate(leads):
        lead += [""] * (8 - len(lead))  # Ensure each row has 8 elements
        
        logger.debug(f"Processing Lead: {lead}")
        
        # Assign to Agent A if Email Verified is empty
        if lead[5] == "":
            logger.debug(f"Lead assigned to Agent A: {lead[1]}")
            handle_verification(i + 2, lead[1])  # +2 to account for header row
    
    # Wait for the Google Sheets to update
    import time
    time.sleep(2)
    
    # Re-read Leads to get the updated Email Verification status
    leads = read_leads()
    for i, lead in enumerate(leads):
        lead += [""] * (8 - len(lead))  # Ensure each row has 8 elements
        
        logger.debug(f"Processing Lead for Outreach: {lead}")
        
        # Assign to Agent B if Email Verified is 'Y' and Response Status is empty
        if lead[5] == "Y" and lead[6] == "":
            logger.debug(f"Lead assigned to Agent B: {lead[1]}")
            handle_outreach(i + 2, lead[0], lead[1])


if __name__ == "__main__":
    main()
