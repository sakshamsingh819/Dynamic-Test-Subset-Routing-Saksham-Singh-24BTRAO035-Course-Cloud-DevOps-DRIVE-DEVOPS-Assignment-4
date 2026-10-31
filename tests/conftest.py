"""
Pytest initialization and global fixtures.
Candidate: Saksham Singh (24BTRAO035) | AI DRIVE DEVOPS
"""
import pytest
import os
import sys

# Ensure root directory is on python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def sample_user_payload():
    return {
        "email": "student.saksham@university.ac.in",
        "password": "SecurePassword#2026",
        "role": "engineer"
    }
