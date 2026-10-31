"""
Unit Tests for TestRouter Orchestration
Author: Saksham Singh (24BTRAO035)
"""
import pytest
from src.dtsr.router import TestRouter, RoutingStrategy
from src.dtsr.git_analyzer import ChangeType


@pytest.fixture
def router():
    return TestRouter()


def test_docs_only_routing_saves_100_percent(router):
    decision = router.route(
        explicit_changed_files=["README.md", "docs/index.md"],
        strategy=RoutingStrategy.SMART
    )
    assert decision.change_type == ChangeType.DOCS_ONLY
    assert decision.routed_test_count == 0
    assert decision.time_saved_percent == 100.0


def test_infra_config_triggers_full_suite(router):
    decision = router.route(
        explicit_changed_files=["requirements.txt"],
        strategy=RoutingStrategy.SMART
    )
    assert decision.change_type == ChangeType.INFRA_CONFIG
    assert decision.routed_test_count == decision.total_suite_count
    assert decision.time_saved_percent == 0.0


def test_code_change_routing_for_billing(router):
    decision = router.route(
        explicit_changed_files=["src/services/billing.py"],
        strategy=RoutingStrategy.SMART,
        num_shards=2
    )
    assert decision.change_type == ChangeType.CODE_CHANGE
    assert decision.routed_test_count < decision.total_suite_count
    assert decision.time_saved_percent > 30.0
    assert any("test_billing.py" in t for t in decision.selected_tests)
    assert decision.shard_plan is not None


def test_tests_only_change_routes_only_modified_test(router):
    decision = router.route(
        explicit_changed_files=["tests/unit/test_inventory.py"],
        strategy=RoutingStrategy.SMART
    )
    assert decision.change_type == ChangeType.TESTS_ONLY
    assert decision.routed_test_count == 1
    assert "tests/unit/test_inventory.py" in decision.selected_tests
