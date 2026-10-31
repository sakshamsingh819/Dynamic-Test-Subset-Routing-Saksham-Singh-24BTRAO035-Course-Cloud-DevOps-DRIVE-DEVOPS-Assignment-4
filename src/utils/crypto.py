"""
Cryptographic Utilities Module
Author: Saksham Singh (24BTRAO035)
Provides deterministic hashing, HMAC generation, and salt derivation.
"""
import hashlib
import hmac
import secrets


def generate_salt(length: int = 16) -> str:
    """Generates a secure cryptographically random hex salt."""
    if length <= 0:
        raise ValueError("Salt length must be positive")
    return secrets.token_hex(length)


def hash_token(data: str, salt: str = "") -> str:
    """Computes a SHA-256 digest of input data with optional salt."""
    if not isinstance(data, str):
        raise TypeError("Data must be a string")
    payload = f"{salt}:{data}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def verify_token(raw_token: str, expected_hash: str, salt: str = "") -> bool:
    """Timing-attack-resistant comparison of raw token hash against expected digest."""
    computed = hash_token(raw_token, salt)
    return hmac.compare_digest(computed, expected_hash)


def create_signature(message: str, secret_key: str) -> str:
    """Generates an HMAC-SHA256 signature for message integrity verification."""
    if not secret_key:
        raise ValueError("Secret key cannot be empty")
    return hmac.new(
        secret_key.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
