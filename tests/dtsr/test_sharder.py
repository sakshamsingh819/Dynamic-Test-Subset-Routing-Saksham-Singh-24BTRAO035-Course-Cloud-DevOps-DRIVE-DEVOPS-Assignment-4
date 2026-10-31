"""
Unit Tests for Sharder LPT Bin-Packing
Author: Saksham Singh (24BTRAO035)
"""
import pytest
from src.dtsr.sharder import Sharder
from src.dtsr.risk_scorer import TestRiskProfile


def test_sharder_balances_buckets():
    sharder = Sharder()
    profiles = [
        TestRiskProfile("test_heavy.py", "DIRECT", 0.5, 0.1, 0.60, 0.9),
        TestRiskProfile("test_med1.py", "DIRECT", 0.5, 0.1, 0.30, 0.7),
        TestRiskProfile("test_med2.py", "DIRECT", 0.5, 0.1, 0.30, 0.7),
        TestRiskProfile("test_light1.py", "TRANSITIVE", 0.2, 0.0, 0.10, 0.4),
        TestRiskProfile("test_light2.py", "TRANSITIVE", 0.2, 0.0, 0.10, 0.4),
    ]
    # Total duration: 0.60 + 0.30 + 0.30 + 0.10 + 0.10 = 1.40s
    # In 2 shards, each should ideally get around 0.70s!
    plan = sharder.partition_lpt(profiles, num_shards=2)
    assert len(plan.shards) == 2
    assert plan.total_duration_sec == pytest.approx(1.40, rel=1e-2)
    # The heaviest shard should not exceed ~0.80s
    assert plan.max_shard_duration_sec <= 0.85
    assert plan.imbalance_ratio < 1.25


def test_sharder_empty_subset():
    sharder = Sharder()
    plan = sharder.partition_lpt([], num_shards=3)
    assert len(plan.shards) == 3
    assert plan.total_duration_sec == 0.0
