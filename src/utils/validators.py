"""
Validation Utilities Module
Author: Saksham Singh (24BTRAO035)
Provides schema checks and sanitization boundaries.
"""
import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
PHONE_REGEX = re.compile(r"^\+?[1-9]\d{7,14}$")
SUPPORTED_CURRENCIES = {"USD", "EUR", "INR", "GBP", "JPY"}


def validate_email(email: str) -> bool:
    """Validates RFC compliant email address formatting."""
    if not isinstance(email, str) or not email.strip():
        return False
    return bool(EMAIL_REGEX.match(email.strip()))


def validate_phone(phone: str) -> bool:
    """Validates international E.164 phone number formatting."""
    if not isinstance(phone, str) or not phone.strip():
        return False
    clean = phone.strip().replace(" ", "").replace("-", "")
    return bool(PHONE_REGEX.match(clean))


def validate_currency(code: str) -> bool:
    """Checks whether the ISO currency code is supported."""
    if not isinstance(code, str):
        return False
    return code.upper().strip() in SUPPORTED_CURRENCIES


def sanitize_string(value: str, max_length: int = 255) -> str:
    """Strips dangerous control characters and limits string length."""
    if not isinstance(value, str):
        raise TypeError("Input must be a string")
    cleaned = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", value).strip()
    return cleaned[:max_length]
