def validate_phone(phone: str) -> bool:
    return sum(1 for char in str(phone) if char.isdigit()) == 10


def validate_aadhaar(aadhaar: str) -> bool:
    return sum(1 for char in str(aadhaar) if char.isdigit()) == 12


def validate_email(email: str) -> bool:
    email = email.strip()
    at_count = email.count('@')
    
    if at_count != 1:
        return False
    
    local, _, domain = email.partition('@')
    
    return (local and domain and 
            '.' in domain and
            domain.count('..') == 0 and
            not domain.startswith('.') and
            not domain.endswith('.') and
            len(domain.split('.')[-1]) >= 2)


def validate_password(password: str) -> tuple[bool, str]:
    """
    Validates password and returns (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter."
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter."
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit."
    if not any(not c.isalnum() for c in password):
        return False, "Password must contain at least one special character (!@#$%^&* etc.)."
    
    return True, ""
