"""
Unified Test-Subset Router Orchestrator
Author: Saksham Singh (24BTRAO035)
Coordinates Git Diff Analysis, AST Reachability, TIA Matrices, Risk Ranking, and Sharding.
"""
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Set, Dict, Any, Optional
import os
import time

from .git_analyzer import GitAnalyzer, ChangeType, GitDiffSummary
from .ast_graph import ASTDependencyGraph
from .impact_tracer import ImpactTracer
from .risk_scorer import RiskScorer, TestRiskProfile
from .sharder import Sharder, ShardPlan


class RoutingStrategy(str, Enum):
    SMART = "SMART"          # AST Graph Closure + TIA Coverage + Risk Prioritization
    AST_ONLY = "AST_ONLY"    # Pure Static AST Import Reachability
    IMPACT_ONLY = "IMPACT_ONLY"  # Pure Dynamic Coverage Footprint
    ALL = "ALL"              # Full Suite Regression Fallback
    NONE = "NONE"            # Docs only / Skip all tests


@dataclass
class RoutingDecision:
    strategy_applied: RoutingStrategy
    change_type: ChangeType
    changed_files: List[str]
    total_churn: int
    selected_tests: List[str]
    total_suite_count: int
    routed_test_count: int
    estimated_duration_sec: float
    full_suite_duration_sec: float
    time_saved_percent: float
    risk_profiles: List[Dict[str, Any]]
    shard_plan: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "strategy_applied": self.strategy_applied.value,
            "change_type": self.change_type.value,
            "changed_files": self.changed_files,
            "total_churn": self.total_churn,
            "selected_tests": self.selected_tests,
            "total_suite_count": self.total_suite_count,
            "routed_test_count": self.routed_test_count,
            "estimated_duration_sec": round(self.estimated_duration_sec, 3),
            "full_suite_duration_sec": round(self.full_suite_duration_sec, 3),
            "time_saved_percent": round(self.time_saved_percent, 2),
            "risk_profiles": self.risk_profiles,
            "shard_plan": self.shard_plan,
        }


class TestRouter:
    """Enterprise Routing Engine for CI/CD test optimization."""
    __test__ = False

    def __init__(self, repo_root: Optional[str] = None):
        self.repo_root = Path(repo_root or os.getcwd()).resolve()
        self.git_analyzer = GitAnalyzer(str(self.repo_root))
        self.ast_graph = ASTDependencyGraph(str(self.repo_root))
        self.impact_tracer = ImpactTracer(str(self.repo_root))
        self.risk_scorer = RiskScorer(self.impact_tracer)
        self.sharder = Sharder()

    def get_all_tests(self) -> List[str]:
        """Discovers all test files present in tests/ directory."""
        tests_dir = self.repo_root / "tests"
        if not tests_dir.exists():
            return []
        found = []
        for p in tests_dir.rglob("test_*.py"):
            rel = str(p.relative_to(self.repo_root))
            # Exclude dtsr internal test suite from app test counts if needed, or include all
            found.append(rel)
        return sorted(found)

    def route(
        self,
        base_ref: Optional[str] = None,
        head_ref: str = "HEAD",
        explicit_changed_files: Optional[List[str]] = None,
        strategy: RoutingStrategy = RoutingStrategy.SMART,
        num_shards: int = 1
    ) -> RoutingDecision:
        """Computes optimal test subset based on change impact analysis."""
        all_tests = self.get_all_tests()
        total_suite_count = len(all_tests)

        # Baseline full suite duration
        full_suite_dur = sum(
            self.impact_tracer.get_test_metadata(t).get("avg_duration_sec", 0.05)
            for t in all_tests
        )
        if full_suite_dur <= 0:
            full_suite_dur = total_suite_count * 0.05

        # Step 1: Detect changes
        if explicit_changed_files is not None:
            diff_summary = GitDiffSummary(explicit_changed_files, lines_added=15, lines_deleted=5)
        else:
            diff_summary = self.git_analyzer.get_diff_summary(base_ref=base_ref, head_ref=head_ref)

        change_type = self.git_analyzer.classify_changes(diff_summary)

        # Step 2: Handle Guardrails & Fallbacks
        if strategy == RoutingStrategy.ALL or change_type == ChangeType.INFRA_CONFIG:
            selected_tests = all_tests
            selected_profiles = [
                self.risk_scorer.compute_risk(t, is_direct=True, total_churn=diff_summary.total_churn)
                for t in selected_tests
            ]
            applied_strat = RoutingStrategy.ALL
            time_saved = 0.0
            est_dur = full_suite_dur

        elif change_type == ChangeType.DOCS_ONLY:
            selected_tests = []
            selected_profiles = []
            applied_strat = RoutingStrategy.NONE
            time_saved = 100.0
            est_dur = 0.0

        elif change_type == ChangeType.TESTS_ONLY:
            # Only run modified tests
            selected_tests = [t for t in diff_summary.test_files if t in all_tests]
            selected_profiles = [
                self.risk_scorer.compute_risk(t, is_direct=True, total_churn=diff_summary.total_churn)
                for t in selected_tests
            ]
            applied_strat = RoutingStrategy.SMART
            est_dur = sum(p.avg_duration_sec for p in selected_profiles)
            time_saved = ((full_suite_dur - est_dur) / full_suite_dur * 100.0) if full_suite_dur > 0 else 0.0

        else:
            # Source code modified: Apply routing algorithm
            applied_strat = strategy
            impacted_tests: Set[str] = set()
            direct_tests: Set[str] = set()

            if strategy in (RoutingStrategy.SMART, RoutingStrategy.AST_ONLY):
                ast_hits = self.ast_graph.find_impacted_tests(diff_summary.source_files)
                impacted_tests.update(ast_hits)

            if strategy in (RoutingStrategy.SMART, RoutingStrategy.IMPACT_ONLY):
                tia_hits = self.impact_tracer.find_tests_covering(diff_summary.source_files)
                impacted_tests.update(tia_hits)

            # Direct tests are those explicitly matching changed file name or direct imports
            for sf in diff_summary.source_files:
                base_stem = Path(sf).stem
                cand_test = f"tests/unit/test_{base_stem}.py"
                if cand_test in all_tests:
                    direct_tests.add(cand_test)

            # Guarantee: If empty due to new untracked modules, fallback safely to all unit tests
            if not impacted_tests and diff_summary.source_files:
                unit_tests = [t for t in all_tests if "unit" in t]
                impacted_tests.update(unit_tests or all_tests)

            # Filter only existing test files
            valid_impacted = [t for t in impacted_tests if t in all_tests]

            # Compute risk profiles and sort by risk descending (Fail-Fast)
            selected_profiles = self.risk_scorer.prioritize_tests(
                set(valid_impacted),
                direct_tests,
                diff_summary.total_churn
            )
            selected_tests = [p.test_file for p in selected_profiles]

            est_dur = sum(p.avg_duration_sec for p in selected_profiles)
            time_saved = ((full_suite_dur - est_dur) / full_suite_dur * 100.0) if full_suite_dur > 0 else 0.0

        # Step 3: Compute CI Sharding
        shard_plan_dict = None
        if num_shards > 1 and selected_profiles:
            plan = self.sharder.partition_lpt(selected_profiles, num_shards=num_shards)
            shard_plan_dict = plan.to_dict()

        return RoutingDecision(
            strategy_applied=applied_strat,
            change_type=change_type,
            changed_files=diff_summary.changed_files,
            total_churn=diff_summary.total_churn,
            selected_tests=selected_tests,
            total_suite_count=total_suite_count,
            routed_test_count=len(selected_tests),
            estimated_duration_sec=est_dur,
            full_suite_duration_sec=full_suite_dur,
            time_saved_percent=max(0.0, min(100.0, time_saved)),
            risk_profiles=[p.to_dict() for p in selected_profiles],
            shard_plan=shard_plan_dict
        )
