"""
Unit Tests for RiskScorer and Fail-Fast Prioritization
Author: Saksham Singh (24BTRAO035)
"""
import pytest
from src.dtsr.impact_tracer import ImpactTracer
from src.dtsr.risk_scorer import RiskScorer


@pytest.fixture
def scorer():
    tracer = ImpactTracer()
    return RiskScorer(tracer)


def test_direct_scores_higher_than_transitive(scorer):
    p_direct = scorer.compute_risk("tests/unit/test_billing.py", is_direct=True, total_churn=20)
    p_trans = scorer.compute_risk("tests/unit/test_billing.py", is_direct=False, total_churn=20)
    assert p_direct.final_risk_score > p_trans.final_risk_score


def test_prioritize_tests_ordering(scorer):
    impacted = {"tests/unit/test_billing.py", "tests/integration/test_checkout_flow.py"}
    direct = {"tests/unit/test_billing.py"}
    ranked = scorer.prioritize_tests(impacted, direct, total_churn=50)
    assert len(ranked) == 2
    # Ensure descending order
    assert ranked[0].final_risk_score >= ranked[1].final_risk_score
