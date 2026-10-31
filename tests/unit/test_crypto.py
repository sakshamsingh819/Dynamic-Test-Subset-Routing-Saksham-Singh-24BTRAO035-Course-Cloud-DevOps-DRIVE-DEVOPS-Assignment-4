"""
Unit Tests for Cryptographic Utilities
Author: Saksham Singh (24BTRAO035)
"""
import pytest
from src.utils.crypto import hash_token, verify_token, generate_salt, create_signature


def test_salt_generation():
    salt1 = generate_salt(16)
    salt2 = generate_salt(16)
    assert len(salt1) == 32  # 16 bytes = 32 hex chars
    assert salt1 != salt2


def test_salt_invalid_length():
    with pytest.raises(ValueError):
        generate_salt(0)


def test_hash_token_deterministic():
    token = "AlphaBravo2026"
    salt = "fixed_salt_hex_123"
    h1 = hash_token(token, salt)
    h2 = hash_token(token, salt)
    assert h1 == h2
    assert len(h1) == 64  # SHA-256 output


def test_verify_token_success():
    raw = "MySuperSecretKey"
    salt = generate_salt()
    expected_hash = hash_token(raw, salt)
    assert verify_token(raw, expected_hash, salt) is True


def test_verify_token_failure():
    raw = "MySuperSecretKey"
    salt = generate_salt()
    expected_hash = hash_token(raw, salt)
    assert verify_token("WrongPassword", expected_hash, salt) is False


def test_create_signature():
    msg = "order_id=5001&amount=299.99"
    key = "secret_signing_key"
    sig1 = create_signature(msg, key)
    sig2 = create_signature(msg, key)
    assert sig1 == sig2
    assert len(sig1) == 64


def test_create_signature_empty_key():
    with pytest.raises(ValueError):
        create_signature("msg", "")
