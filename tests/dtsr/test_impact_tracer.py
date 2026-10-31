"""
Unit Tests for ImpactTracer
Author: Saksham Singh (24BTRAO035)
"""
import pytest
from src.dtsr.impact_tracer import ImpactTracer


@pytest.fixture
def tracer():
    return ImpactTracer()


def test_seed_matrix_loaded(tracer):
    all_tests = tracer.get_all_registered_tests()
    assert len(all_tests) >= 5
    assert "tests/unit/test_billing.py" in all_tests


def test_find_tests_covering_billing(tracer):
    impacted = tracer.find_tests_covering(["src/services/billing.py"])
    assert "tests/unit/test_billing.py" in impacted
    assert "tests/unit/test_order.py" in impacted


def test_record_run_updates_moving_average(tracer):
    t_file = "tests/unit/test_sample_ephemeral.py"
    tracer.record_run(t_file, ["src/utils/crypto.py"], duration_sec=0.10, passed=True)
    meta = tracer.get_test_metadata(t_file)
    assert meta["run_count"] == 1
    assert "src/utils/crypto.py" in meta["covered_files"]
