"""
Unit Tests for NotificationService
Author: Saksham Singh (24BTRAO035)
"""
import pytest
from src.services.notifications import NotificationService


@pytest.fixture
def notify_svc():
    return NotificationService()


def test_send_email_success(notify_svc):
    evt = notify_svc.send_email(
        recipient_email="student@university.ac.in",
        subject="CI Pipeline Notification",
        message="Your test suite has passed dynamic routing validation."
    )
    assert evt.event_id.startswith("evt_mail_")
    assert evt.status == "delivered"
    assert evt.recipient == "student@university.ac.in"


def test_send_email_invalid_recipient(notify_svc):
    with pytest.raises(ValueError, match="Invalid email"):
        notify_svc.send_email("bad_email", "Subject", "Body")


def test_send_sms_success(notify_svc):
    evt = notify_svc.send_sms("+919876543210", "OTP code: 849201")
    assert evt.event_id.startswith("evt_sms_")
    assert evt.status == "delivered"


def test_send_sms_overlength(notify_svc):
    with pytest.raises(ValueError, match="160 character limit"):
        notify_svc.send_sms("+919876543210", "X" * 165)
