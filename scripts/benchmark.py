"""
Dynamic Test-Subset Routing Benchmark Engine
Author: Saksham Singh (24BTRAO035) | AI DRIVE DEVOPS
Simulates 5 distinct PR archetypes and benchmarks Full Suite vs Naive vs DTSR.
"""
import json
import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Any

# Ensure project root is available
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.dtsr.router import TestRouter, RoutingStrategy


BENCHMARK_SCENARIOS = [
    {
        "id": "PR-01",
        "title": "Documentation & Schema Docs Update",
        "description": "Developer updates markdown docs and architectural diagrams",
        "changed_files": ["README.md", "docs/architecture.md", "docs/api_spec.json"],
        "churn": 45,
    },
    {
        "id": "PR-02",
        "title": "Email Regex Validator Hardening",
        "description": "Tightening input sanitation boundaries in utility module",
        "changed_files": ["src/utils/validators.py"],
        "churn": 18,
    },
    {
        "id": "PR-03",
        "title": "Tiered Volume Discount Logic Refactor",
        "description": "Adjusting VIP tier discounts and invoice aggregation",
        "changed_files": ["src/services/billing.py"],
        "churn": 32,
    },
    {
        "id": "PR-04",
        "title": "HMAC Token Cryptography Security Patch",
        "description": "Upgrading token salt derivation and constant-time compare",
        "changed_files": ["src/utils/crypto.py"],
        "churn": 24,
    },
    {
        "id": "PR-05",
        "title": "Core Dependency Manifest Bump",
        "description": "Upgrading production runtime packages in requirements.txt",
        "changed_files": ["requirements.txt"],
        "churn": 8,
    },
]


def run_benchmark() -> Dict[str, Any]:
    router = TestRouter()
    all_tests = router.get_all_tests()
    total_suites = len(all_tests)

    results: List[Dict[str, Any]] = []
    total_baseline_time = 0.0
    total_dtsr_time = 0.0

    print("=" * 78)
    print("      DYNAMIC TEST-SUBSET ROUTING (DTSR) EMPIRICAL BENCHMARK")
    print("      Candidate: Saksham Singh | USN: 24BTRAO035 | AI DRIVE DEVOPS")
    print("=" * 78)
    print(f"{'PR ID':<7} | {'Scenario Title':<30} | {'Full':<5} | {'Routed':<6} | {'Time (s)':<10} | {'Saved %':<7}")
    print("-" * 78)

    for sc in BENCHMARK_SCENARIOS:
        decision = router.route(
            explicit_changed_files=sc["changed_files"],
            strategy=RoutingStrategy.SMART,
            num_shards=2
        )

        full_dur = decision.full_suite_duration_sec
        routed_dur = decision.estimated_duration_sec
        saved_pct = decision.time_saved_percent

        total_baseline_time += full_dur
        total_dtsr_time += routed_dur

        scenario_res = {
            "id": sc["id"],
            "title": sc["title"],
            "change_type": decision.change_type.value,
            "strategy": decision.strategy_applied.value,
            "changed_files": sc["changed_files"],
            "churn": sc["churn"],
            "full_suite_count": total_suites,
            "routed_count": decision.routed_test_count,
            "baseline_duration_sec": round(full_dur, 2),
            "routed_duration_sec": round(routed_dur, 2),
            "time_saved_percent": round(saved_pct, 1),
            "selected_tests": decision.selected_tests,
            "shard_plan": decision.shard_plan,
        }
        results.append(scenario_res)

        dur_str = f"{routed_dur:.2f} / {full_dur:.2f}"
        print(f"{sc['id']:<7} | {sc['title'][:30]:<30} | {total_suites:<5} | {decision.routed_test_count:<6} | {dur_str:<10} | {saved_pct:>6.1f}%")

    print("-" * 78)
    overall_saved = ((total_baseline_time - total_dtsr_time) / total_baseline_time) * 100.0
    print(f"OVERALL CUMULATIVE SAVINGS: {overall_saved:.1f}% time and compute energy saved!")
    print(f"Cumulative Baseline Time: {total_baseline_time:.2f}s | Cumulative DTSR Time: {total_dtsr_time:.2f}s")
    print("=" * 78)

    benchmark_data = {
        "candidate": "Saksham Singh",
        "usn": "24BTRAO035",
        "timestamp": time.time(),
        "total_scenarios": len(BENCHMARK_SCENARIOS),
        "total_test_suites": total_suites,
        "overall_time_saved_percent": round(overall_saved, 1),
        "cumulative_baseline_sec": round(total_baseline_time, 2),
        "cumulative_dtsr_sec": round(total_dtsr_time, 2),
        "scenarios": results,
    }

    out_file = Path(__file__).resolve().parent.parent / ".dtsr" / "benchmark_summary.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(benchmark_data, indent=2), encoding="utf-8")
    print(f"\n[Artifact Persisted] -> {out_file}\n")
    return benchmark_data


if __name__ == "__main__":
    run_benchmark()
