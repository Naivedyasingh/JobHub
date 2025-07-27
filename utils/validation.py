# utils/validation.py

import re

def validate_phone(phone: str) -> bool:
    """
    phone is exactly 10 digits (Indian format).
    Strips non-digit characters before checking length.
    """
    cleaned = re.sub(r"\D", "", str(phone))
    return len(cleaned) == 10

def validate_aadhaar(aadhaar: str) -> bool:
    """
    Ensure Aadhaar is exactly 12 digits.
    Strips non-digit characters before checking length.
    """
    cleaned = re.sub(r"\D", "", str(aadhaar))
    return len(cleaned) == 12

def validate_email(email: str) -> bool:
    """
    Basic email format check.
    Returns True if matches pattern user@domain.tld
    """
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email))

def validate_password(password: str) -> bool:
    """
    Enforce a minimal password policy:
      - At least 8 characters
      - Contains at least one uppercase, one lowercase, one digit
    """
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    return True
