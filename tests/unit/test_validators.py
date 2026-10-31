"""
Unit Tests for Validator Utilities
Author: Saksham Singh (24BTRAO035)
"""
import pytest
from src.utils.validators import validate_email, validate_phone, validate_currency, sanitize_string


def test_validate_email_valid():
    assert validate_email("saksham@university.ac.in") is True
    assert validate_email("student.devops_123@domain.org") is True


def test_validate_email_invalid():
    assert validate_email("plainaddress") is False
    assert validate_email("@missingusername.com") is False
    assert validate_email("user@.com") is False
    assert validate_email("") is False


def test_validate_phone_valid():
    assert validate_phone("+919876543210") is True
    assert validate_phone("9876543210") is True
    assert validate_phone("+1-800-555-0199") is True


def test_validate_phone_invalid():
    assert validate_phone("123") is False
    assert validate_phone("invalid_phone_number") is False


def test_validate_currency():
    assert validate_currency("USD") is True
    assert validate_currency("inr") is True
    assert validate_currency("EUR") is True
    assert validate_currency("XYZ") is False


def test_sanitize_string():
    dirty = "Hello\x00World\x1f\nTest"
    cleaned = sanitize_string(dirty, max_length=15)
    assert "\x00" not in cleaned
    assert "\x1f" not in cleaned
    assert len(cleaned) <= 15
