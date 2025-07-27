# utils/data_helpers.py

import os
import json

DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

def read_json(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []

def write_json(path, data):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception:
        return False


def cleanup_user_data():
    """Clean up existing user data to fix any invalid values"""
    users = read_json("data/users.json")
    updated = False
    
    for i, user in enumerate(users):
        # Fix gender field
        if user.get('gender') not in ['Male', 'Female', 'Other']:
            users[i]['gender'] = 'Male'
            updated = True
        
        # Fix expected_salary field
        salary = user.get('expected_salary', 15000)
        if not isinstance(salary, (int, float)) or salary < 5000:
            users[i]['expected_salary'] = 15000
            updated = True
        elif salary > 100000:
            users[i]['expected_salary'] = 100000
            updated = True
        
        # Fix experience field
        if user.get('experience') not in ['Fresher', '1-2 years', '2-5 years', '5+ years']:
            users[i]['experience'] = 'Fresher'
            updated = True
        
        # Add availability status if missing
        if 'availability_status' not in users[i]:
            users[i]['availability_status'] = 'available'
            updated = True
    
    if updated:
        write_json("data/users.json", users)
    
    return users