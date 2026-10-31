"""
Dynamic CI Test Sharding & Bin-Packing Engine
Author: Saksham Singh (24BTRAO035)
Implements Greedy Longest Processing Time (LPT) bin-packing to balance parallel CI runners.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any
import os

from .risk_scorer import TestRiskProfile


@dataclass
class ShardBucket:
    shard_id: int
    test_files: List[str] = field(default_factory=list)
    estimated_duration_sec: float = 0.0

    def add_test(self, test_file: str, duration: float) -> None:
        self.test_files.append(test_file)
        self.estimated_duration_sec = round(self.estimated_duration_sec + duration, 4)


@dataclass
class ShardPlan:
    num_shards: int
    shards: List[ShardBucket]
    total_duration_sec: float
    max_shard_duration_sec: float
    imbalance_ratio: float  # max_shard_duration / (total_duration / num_shards)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "num_shards": self.num_shards,
            "total_duration_sec": round(self.total_duration_sec, 3),
            "max_shard_duration_sec": round(self.max_shard_duration_sec, 3),
            "imbalance_ratio": round(self.imbalance_ratio, 3),
            "shards": [
                {
                    "shard_id": s.shard_id,
                    "test_count": len(s.test_files),
                    "estimated_duration_sec": round(s.estimated_duration_sec, 3),
                    "tests": s.test_files,
                }
                for s in self.shards
            ]
        }


class Sharder:
    """Partitions selected test files evenly across K parallel runner workers."""

    def partition_lpt(self, test_profiles: List[TestRiskProfile], num_shards: int = 2) -> ShardPlan:
        if num_shards <= 0:
            raise ValueError("Number of shards must be at least 1")

        if not test_profiles:
            empty_shards = [ShardBucket(shard_id=i + 1) for i in range(num_shards)]
            return ShardPlan(
                num_shards=num_shards,
                shards=empty_shards,
                total_duration_sec=0.0,
                max_shard_duration_sec=0.0,
                imbalance_ratio=1.0
            )

        # Step 1: Sort by duration descending (LPT heuristic)
        sorted_tests = sorted(test_profiles, key=lambda x: x.avg_duration_sec, reverse=True)

        # Step 2: Initialize K buckets
        buckets = [ShardBucket(shard_id=i + 1) for i in range(num_shards)]

        # Step 3: Greedy assignment to least-loaded bucket
        for prof in sorted_tests:
            # Find bucket with minimum estimated duration
            least_loaded = min(buckets, key=lambda b: b.estimated_duration_sec)
            least_loaded.add_test(prof.test_file, prof.avg_duration_sec)

        total_dur = sum(b.estimated_duration_sec for b in buckets)
        max_dur = max(b.estimated_duration_sec for b in buckets)
        ideal_mean = total_dur / num_shards if num_shards > 0 else 1.0
        imbalance = max_dur / ideal_mean if ideal_mean > 0 else 1.0

        return ShardPlan(
            num_shards=num_shards,
            shards=buckets,
            total_duration_sec=total_dur,
            max_shard_duration_sec=max_dur,
            imbalance_ratio=imbalance
        )
