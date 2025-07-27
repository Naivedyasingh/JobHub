import os
from datetime import datetime, timedelta
from utils.data_helpers import read_json, write_json

DATA_FOLDER = ""
APPLICATIONS_FILE = os.path.join(DATA_FOLDER, "applications.json")

def get_job_applications():
    """Get job applications data"""
    return read_json("data/applications.json")

def save_job_application(application):
    """Save a new job application"""
    applications = get_job_applications()
    application['id'] = len(applications) + 1
    application['applied_date'] = datetime.now().isoformat()
    application['status'] = 'pending'
    applications.append(application)
    write_json("data/applications.json", applications)
    return True

def update_application_status(app_id, status, response_message=""):
    """Update application status (accept/reject)"""
    applications = get_job_applications()
    for i, app in enumerate(applications):
        if app.get('id') == app_id:
            applications[i]['status'] = status
            applications[i]['response_date'] = datetime.now().isoformat()
            applications[i]['response_message'] = response_message
            write_json("data/applications.json", applications)
            return True
    return False