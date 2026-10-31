"""
Unit Tests for ASTDependencyGraph
Author: Saksham Singh (24BTRAO035)
"""
import pytest
from src.dtsr.ast_graph import ASTDependencyGraph


@pytest.fixture
def graph():
    return ASTDependencyGraph()


def test_graph_discovers_nodes(graph):
    # Should discover auth, billing, crypto, validators, and tests
    nodes = list(graph.forward_graph.nodes)
    assert any("src.services.auth" in n for n in nodes)
    assert any("src.services.billing" in n for n in nodes)
    assert any("src.utils.crypto" in n for n in nodes)


def test_crypto_dependency_closure(graph):
    # Changing crypto.py should impact auth.py and test_crypto.py / test_auth.py
    impacted = graph.get_transitive_dependents("src/utils/crypto.py")
    assert any("src/services/auth.py" in p for p in impacted)
    assert any("tests/unit/test_auth.py" in p or "tests/unit/test_crypto.py" in p for p in impacted)


def test_find_impacted_tests_for_billing(graph):
    impacted_tests = graph.find_impacted_tests(["src/services/billing.py"])
    assert any("test_billing.py" in t for t in impacted_tests)


def test_test_file_change_impacts_itself(graph):
    impacted = graph.find_impacted_tests(["tests/unit/test_notifications.py"])
    assert "tests/unit/test_notifications.py" in impacted
