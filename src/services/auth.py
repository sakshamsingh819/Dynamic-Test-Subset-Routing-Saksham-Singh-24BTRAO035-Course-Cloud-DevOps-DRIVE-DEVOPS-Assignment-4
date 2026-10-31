"""
Authentication Domain Service
Author: Saksham Singh (24BTRAO035)
Implements user account lifecycle, password hashing, and session tokens.
"""
from dataclasses import dataclass
from typing import Dict, Optional
import time

from src.utils.crypto import hash_token, verify_token, generate_salt, create_signature
from src.utils.validators import validate_email, sanitize_string


@dataclass
class UserAccount:
    user_id: str
    email: str
    password_hash: str
    salt: str
    role: str = "customer"
    is_active: bool = True
    created_at: float = 0.0


class AuthService:
    """Manages secure registration, credential verification, and token signing."""

    def __init__(self, secret_key: str = "dtsr-secure-secret-key-24btrao035"):
        self._users: Dict[str, UserAccount] = {}
        self.secret_key = secret_key

    def register_user(self, email: str, raw_password: str, role: str = "customer") -> UserAccount:
        if not validate_email(email):
            raise ValueError(f"Invalid email address: {email}")
        if len(raw_password) < 8:
            raise ValueError("Password must be at least 8 characters")

        email_clean = sanitize_string(email.lower())
        if email_clean in self._users:
            raise ValueError(f"User with email {email_clean} already exists")

        salt = generate_salt(16)
        pwd_hash = hash_token(raw_password, salt)
        user_id = f"usr_{len(self._users) + 1:04d}"

        user = UserAccount(
            user_id=user_id,
            email=email_clean,
            password_hash=pwd_hash,
            salt=salt,
            role=role,
            is_active=True,
            created_at=time.time()
        )
        self._users[email_clean] = user
        return user

    def authenticate(self, email: str, raw_password: str) -> Optional[UserAccount]:
        clean_email = email.strip().lower()
        user = self._users.get(clean_email)
        if not user or not user.is_active:
            return None

        if verify_token(raw_password, user.password_hash, user.salt):
            return user
        return None

    def issue_session_token(self, user: UserAccount) -> str:
        payload = f"{user.user_id}:{user.role}:{int(time.time())}"
        signature = create_signature(payload, self.secret_key)
        return f"{payload}.{signature}"

    def verify_session_token(self, token: str) -> bool:
        try:
            payload, signature = token.rsplit(".", 1)
            expected = create_signature(payload, self.secret_key)
            return expected == signature
        except (ValueError, AttributeError):
            return False

    def get_user_count(self) -> int:
        return len(self._users)
