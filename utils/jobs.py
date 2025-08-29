from utils.data_helpers import read_json, write_json
import os
import streamlit as st
from datetime import datetime, timedelta

DATA_FOLDER = "data"
DEMO_JOBS_FILE = os.path.join(DATA_FOLDER, "demo_jobs.json")

def get_job_offers():
    """Get all job offers"""
    return read_json("data/job_offers.json")

def save_demo_job(job: dict) -> bool:
    jobs = get_demo_jobs()
    job['id'] = len(jobs) + 1
    jobs.append(job)
    return write_json(DEMO_JOBS_FILE, jobs)

def add_job_posting(employer_id, job_data):
    """Add a new job posting for employer"""
    users = read_json("data/users.json")
    for i, user in enumerate(users):
        if user.get('id') == employer_id and user.get('role') == 'hire':
            if 'job_postings' not in users[i]:
                users[i]['job_postings'] = []
            
            job_data['id'] = len(users[i]['job_postings']) + 1
            job_data['posted_date'] = datetime.now().isoformat()
            job_data['status'] = 'active'
            job_data['applications_count'] = 0
            
            users[i]['job_postings'].append(job_data)
            write_json("data/users.json", users)
            
            st.session_state.current_user = users[i]
            return True
    return False

def get_demo_jobs() -> list:
    return read_json(DEMO_JOBS_FILE)