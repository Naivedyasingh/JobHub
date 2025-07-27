import os
import json
from datetime import datetime, timedelta
from utils.data_helpers import read_json, write_json# ---------------- Authentication & Profile Helpers ----------------

def authenticate(identifier, pwd, role):
    users = read_json("data/users.json")
    for u in users:
        if u.get("role") == role and u.get("password") == pwd:
            if identifier.lower() == u["name"].lower() or identifier == u["phone"]:
                return u
    return None

def next_user_id(users):
    return max([u.get("id", 0) for u in users], default=0) + 1

def calculate_profile_completion(user):
    """Calculate profile completion percentage"""
    if user['role'] == 'job':
        required_fields = ['name', 'phone', 'email', 'aadhaar', 'address', 'city', 'experience', 'job_types', 'expected_salary', 'availability']
    else:  # employer
        required_fields = ['name', 'phone', 'email', 'company_name', 'company_type', 'address', 'city', 'business_description']
    
    completed = sum(1 for field in required_fields if user.get(field))
    return int((completed / len(required_fields)) * 100)

def update_user_profile(user_id, updates):
    """Update user profile in database"""
    users = read_json("data/users.json")
    for i, user in enumerate(users):
        if user['id'] == user_id:
            users[i].update(updates)
            write_json("data/users.json", users)
            return users[i]
    return None