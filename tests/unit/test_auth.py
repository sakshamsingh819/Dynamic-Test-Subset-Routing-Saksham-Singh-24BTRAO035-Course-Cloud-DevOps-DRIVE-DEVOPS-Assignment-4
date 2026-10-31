"""
Unit Tests for AuthService
Author: Saksham Singh (24BTRAO035)
"""
import pytest
from src.services.auth import AuthService


@pytest.fixture
def auth_service():
    return AuthService(secret_key="test-secret-suite-key")


def test_register_user_success(auth_service):
    user = auth_service.register_user("saksham@test.com", "Password#2026")
    assert user.user_id.startswith("usr_")
    assert user.email == "saksham@test.com"
    assert user.password_hash != "Password#2026"
    assert auth_service.get_user_count() == 1


def test_register_duplicate_email(auth_service):
    auth_service.register_user("saksham@test.com", "Password#2026")
    with pytest.raises(ValueError, match="already exists"):
        auth_service.register_user("saksham@test.com", "AnotherPassword123")


def test_register_invalid_email(auth_service):
    with pytest.raises(ValueError, match="Invalid email"):
        auth_service.register_user("invalid_email", "Password#2026")


def test_register_short_password(auth_service):
    with pytest.raises(ValueError, match="at least 8 characters"):
        auth_service.register_user("saksham@test.com", "short")


def test_authenticate_success(auth_service):
    auth_service.register_user("saksham@test.com", "SecretPass123")
    user = auth_service.authenticate("saksham@test.com", "SecretPass123")
    assert user is not None
    assert user.email == "saksham@test.com"


def test_authenticate_wrong_password(auth_service):
    auth_service.register_user("saksham@test.com", "SecretPass123")
    user = auth_service.authenticate("saksham@test.com", "WrongPassword")
    assert user is None


def test_session_token_flow(auth_service):
    user = auth_service.register_user("token_user@test.com", "SecretPass123")
    token = auth_service.issue_session_token(user)
    assert "." in token
    assert auth_service.verify_session_token(token) is True
    assert auth_service.verify_session_token(token + "_tampered") is False
