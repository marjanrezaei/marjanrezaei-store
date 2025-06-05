import re
from django.core.exceptions import ValidationError

def validate_iranian_phone(phone_number):
    """Validate Iranian mobile numbers 
    (must start with '09' and contain 11 digits)."""
    pattern = r'^09\d{9}$'
    if not re.fullmatch(pattern, phone_number):
        raise ValidationError("Phone number must be a valid (e.g., 09123456789).")