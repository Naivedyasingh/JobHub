import os
from datetime import datetime, timedelta
from utils.data_helpers import read_json, write_json

DATA_FOLDER = "data"
OFFERS_FILE = os.path.join(DATA_FOLDER, "job_offers.json")

def get_job_offers():
    """
    Read and return all job offers from data/job_offers.json.
    """
    return read_json(OFFERS_FILE)

def save_job_offer(offer_data):
    """Save a job offer from employer to job seeker"""
    offers = read_json("data/job_offers.json")
    offer_data['id'] = len(offers) + 1
    offer_data['offered_date'] = datetime.now().isoformat()
    offer_data['status'] = 'pending'
    offer_data['expires_at'] = (datetime.now() + timedelta(days=1)).isoformat()  # 24 hours
    offers.append(offer_data)
    write_json("data/job_offers.json", offers)
    return True

def update_offer_status(offer_id, status, response_message=""):
    """Update job offer status"""
    offers = get_job_offers()
    for i, offer in enumerate(offers):
        if offer.get('id') == offer_id:
            offers[i]['status'] = status
            offers[i]['response_date'] = datetime.now().isoformat()
            offers[i]['response_message'] = response_message
            write_json("data/job_offers.json", offers)
            return True
    return False