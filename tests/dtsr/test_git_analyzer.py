"""
Unit Tests for GitAnalyzer and Change Classification
Author: Saksham Singh (24BTRAO035)
"""
import pytest
from src.dtsr.git_analyzer import GitAnalyzer, GitDiffSummary, ChangeType


def test_classify_docs_only():
    analyzer = GitAnalyzer()
    diff = GitDiffSummary(["README.md", "docs/architecture.png", "notes.txt"])
    assert analyzer.classify_changes(diff) == ChangeType.DOCS_ONLY


def test_classify_infra_config():
    analyzer = GitAnalyzer()
    diff = GitDiffSummary(["requirements.txt", "src/services/billing.py"])
    assert analyzer.classify_changes(diff) == ChangeType.INFRA_CONFIG

    diff_ci = GitDiffSummary([".github/workflows/ci.yml"])
    assert analyzer.classify_changes(diff_ci) == ChangeType.INFRA_CONFIG


def test_classify_tests_only():
    analyzer = GitAnalyzer()
    diff = GitDiffSummary(["tests/unit/test_billing.py"])
    assert analyzer.classify_changes(diff) == ChangeType.TESTS_ONLY


def test_classify_code_change():
    analyzer = GitAnalyzer()
    diff = GitDiffSummary(["src/services/auth.py", "src/utils/crypto.py"])
    assert analyzer.classify_changes(diff) == ChangeType.CODE_CHANGE


def test_git_diff_summary_properties():
    diff = GitDiffSummary(
        ["src/services/auth.py", "README.md", "requirements.txt", "tests/unit/test_auth.py"],
        lines_added=40,
        lines_deleted=10
    )
    assert diff.total_churn == 50
    assert len(diff.source_files) == 1
    assert len(diff.doc_files) == 1
    assert len(diff.infra_files) == 1
    assert len(diff.test_files) == 1
