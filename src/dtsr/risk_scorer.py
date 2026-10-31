"""
Predictive Test Risk Scorer & Fail-Fast Prioritizer
Author: Saksham Singh (24BTRAO035)
Ranks impacted test subsets by failure probability, code churn, and execution speed.
"""
import math
import os
from dataclasses import dataclass
from typing import List, Dict, Any, Set
from .impact_tracer import ImpactTracer


@dataclass
class TestRiskProfile:
    __test__ = False
    test_file: str
    impact_type: str        # "DIRECT" (1.0), "TRANSITIVE" (0.6), or "COVERAGE" (0.5)
    churn_score: float      # log(1 + churn in covered files)
    historical_failure_rate: float
    avg_duration_sec: float
    final_risk_score: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "test_file": self.test_file,
            "impact_type": self.impact_type,
            "churn_score": round(self.churn_score, 3),
            "historical_failure_rate": round(self.historical_failure_rate, 3),
            "avg_duration_sec": round(self.avg_duration_sec, 3),
            "final_risk_score": round(self.final_risk_score, 3),
        }


class RiskScorer:
    """
    Computes deterministic risk scores to prioritize high-risk, high-velocity tests.
    Ensures CI pipelines catch regressions in the first minute of execution.
    """

    WEIGHT_IMPACT = 0.40
    WEIGHT_CHURN = 0.25
    WEIGHT_HISTORICAL_FAIL = 0.25
    WEIGHT_SPEED_BONUS = 0.10

    def __init__(self, impact_tracer: ImpactTracer):
        self.tracer = impact_tracer

    def compute_risk(
        self,
        test_file: str,
        is_direct: bool,
        total_churn: int
    ) -> TestRiskProfile:
        norm_test = os.path.normpath(test_file)
        meta = self.tracer.get_test_metadata(norm_test)

        runs = max(1, meta.get("run_count", 1))
        fails = meta.get("fail_count", 0)
        fail_rate = min(1.0, fails / runs)

        duration = max(0.01, meta.get("avg_duration_sec", 0.05))

        # Base impact weighting
        impact_weight = 1.0 if is_direct else 0.6
        impact_label = "DIRECT" if is_direct else "TRANSITIVE"

        # Churn normalization
        churn_factor = math.log1p(total_churn) / 5.0  # normalized ~0..1 for typical churns
        churn_factor = min(1.0, churn_factor)

        # Speed bonus (faster tests score higher so they execute first)
        speed_factor = 1.0 / (1.0 + duration)

        # Composite score
        score = (
            self.WEIGHT_IMPACT * impact_weight +
            self.WEIGHT_CHURN * churn_factor +
            self.WEIGHT_HISTORICAL_FAIL * fail_rate +
            self.WEIGHT_SPEED_BONUS * speed_factor
        )

        return TestRiskProfile(
            test_file=norm_test,
            impact_type=impact_label,
            churn_score=churn_factor,
            historical_failure_rate=fail_rate,
            avg_duration_sec=duration,
            final_risk_score=round(score, 4)
        )

    def prioritize_tests(
        self,
        impacted_tests: Set[str],
        direct_tests: Set[str],
        total_churn: int
    ) -> List[TestRiskProfile]:
        """Returns sorted list of TestRiskProfile in descending priority (highest risk first)."""
        profiles: List[TestRiskProfile] = []
        for t in impacted_tests:
            is_dir = t in direct_tests
            p = self.compute_risk(t, is_dir, total_churn)
            profiles.append(p)

        profiles.sort(key=lambda x: x.final_risk_score, reverse=True)
        return profiles
