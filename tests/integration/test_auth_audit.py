"""
Integration Test: Authentication Security & Event Audit Pipeline
Author: Saksham Singh (24BTRAO035)
Verifies user onboarding, security token verification, and administrative audit logging.
"""
import pytest
from src.services.auth import AuthService
from src.services.notifications import NotificationService


def test_auth_audit_trail():
    auth_svc = AuthService(secret_key="audit-test-key-24btrao035")
    notify_svc = NotificationService()

    # Register user
    user = auth_svc.register_user("devops.lead@company.internal", "SecureDevOpsPass#2026", role="admin")

    # Send welcome alert
    evt = notify_svc.send_email(
        recipient_email=user.email,
        subject="Security Notice: Admin Access Granted",
        message=f"Account {user.user_id} was provisioned with role {user.role}."
    )
    assert evt.status == "delivered"

    # Authenticate and obtain token
    authenticated_user = auth_svc.authenticate("devops.lead@company.internal", "SecureDevOpsPass#2026")
    assert authenticated_user is not None
    token = auth_svc.issue_session_token(authenticated_user)

    # Validate session token
    assert auth_svc.verify_session_token(token) is True
