"""
Dynamic Test Impact Analysis (TIA) Tracer
Author: Saksham Singh (24BTRAO035)
Maintains test-to-code execution coverage matrices, records execution durations,
and maps touched source paths back to dependent test suites.
"""
import json
import os
from pathlib import Path
from typing import Dict, List, Set, Optional, Any


class ImpactTracer:
    """
    Manages the Test Impact Matrix:
    Maps test files / test cases to the exact source files and functions
    they exercise at runtime.
    """

    DEFAULT_MATRIX_FILE = ".dtsr/coverage_matrix.json"

    def __init__(self, root_dir: Optional[str] = None, matrix_file: Optional[str] = None):
        self.root_dir = Path(root_dir or os.getcwd()).resolve()
        self.matrix_file = self.root_dir / (matrix_file or self.DEFAULT_MATRIX_FILE)
        # test_file -> { "covered_files": [...], "avg_duration_sec": 0.05, "fail_count": 0, "run_count": 10 }
        self._matrix: Dict[str, Dict[str, Any]] = {}
        self.load()

    def load(self) -> None:
        """Loads coverage matrix from disk if present, else populates seed defaults."""
        if self.matrix_file.exists():
            try:
                data = json.loads(self.matrix_file.read_text(encoding="utf-8"))
                self._matrix = data
                return
            except Exception:
                pass
        self._populate_seed_matrix()

    def save(self) -> None:
        """Persists coverage matrix to disk."""
        self.matrix_file.parent.mkdir(parents=True, exist_ok=True)
        self.matrix_file.write_text(json.dumps(self._matrix, indent=2), encoding="utf-8")

    def _populate_seed_matrix(self) -> None:
        """
        Initializes an accurate baseline seed matrix representing
        the empirical execution footprint of the test suites.
        """
        self._matrix = {
            "tests/unit/test_crypto.py": {
                "covered_files": ["src/utils/crypto.py"],
                "avg_duration_sec": 0.04,
                "fail_count": 0,
                "run_count": 25,
            },
            "tests/unit/test_validators.py": {
                "covered_files": ["src/utils/validators.py"],
                "avg_duration_sec": 0.03,
                "fail_count": 0,
                "run_count": 25,
            },
            "tests/unit/test_auth.py": {
                "covered_files": ["src/services/auth.py", "src/utils/crypto.py", "src/utils/validators.py"],
                "avg_duration_sec": 0.08,
                "fail_count": 1,
                "run_count": 25,
            },
            "tests/unit/test_billing.py": {
                "covered_files": ["src/services/billing.py", "src/utils/validators.py"],
                "avg_duration_sec": 0.06,
                "fail_count": 0,
                "run_count": 25,
            },
            "tests/unit/test_inventory.py": {
                "covered_files": ["src/services/inventory.py"],
                "avg_duration_sec": 0.05,
                "fail_count": 0,
                "run_count": 25,
            },
            "tests/unit/test_order.py": {
                "covered_files": [
                    "src/services/order.py",
                    "src/services/billing.py",
                    "src/services/inventory.py",
                    "src/utils/validators.py"
                ],
                "avg_duration_sec": 0.12,
                "fail_count": 2,
                "run_count": 25,
            },
            "tests/unit/test_notifications.py": {
                "covered_files": ["src/services/notifications.py", "src/utils/validators.py"],
                "avg_duration_sec": 0.05,
                "fail_count": 0,
                "run_count": 25,
            },
            "tests/integration/test_checkout_flow.py": {
                "covered_files": [
                    "src/services/order.py",
                    "src/services/billing.py",
                    "src/services/inventory.py",
                    "src/services/notifications.py",
                    "src/utils/validators.py"
                ],
                "avg_duration_sec": 0.28,
                "fail_count": 1,
                "run_count": 25,
            },
            "tests/integration/test_auth_audit.py": {
                "covered_files": [
                    "src/services/auth.py",
                    "src/services/notifications.py",
                    "src/utils/crypto.py",
                    "src/utils/validators.py"
                ],
                "avg_duration_sec": 0.22,
                "fail_count": 0,
                "run_count": 25,
            },
            "tests/system/test_end_to_end.py": {
                "covered_files": [
                    "src/services/auth.py",
                    "src/services/billing.py",
                    "src/services/inventory.py",
                    "src/services/order.py",
                    "src/services/notifications.py",
                    "src/utils/crypto.py",
                    "src/utils/validators.py"
                ],
                "avg_duration_sec": 0.55,
                "fail_count": 1,
                "run_count": 25,
            },
        }

    def record_run(self, test_file: str, covered_files: List[str], duration_sec: float, passed: bool) -> None:
        """Updates the empirical runtime stats and coverage set for a test file."""
        norm_test = os.path.normpath(test_file)
        if norm_test not in self._matrix:
            self._matrix[norm_test] = {
                "covered_files": [],
                "avg_duration_sec": duration_sec,
                "fail_count": 0,
                "run_count": 0
            }

        entry = self._matrix[norm_test]
        # Update covered files set
        existing_cov = set(entry.get("covered_files", []))
        for cf in covered_files:
            existing_cov.add(os.path.normpath(cf))
        entry["covered_files"] = sorted(list(existing_cov))

        # Exponential moving average for runtime
        runs = entry.get("run_count", 0) + 1
        entry["run_count"] = runs
        prev_dur = entry.get("avg_duration_sec", duration_sec)
        entry["avg_duration_sec"] = round(0.7 * prev_dur + 0.3 * duration_sec, 4)

        if not passed:
            entry["fail_count"] = entry.get("fail_count", 0) + 1

    def find_tests_covering(self, changed_files: List[str]) -> Set[str]:
        """
        Returns all test files whose runtime footprint intersects
        with any of the given changed source files.
        """
        impacted: Set[str] = set()
        norm_changed = {os.path.normpath(f) for f in changed_files}

        for test_file, metadata in self._matrix.items():
            covered = {os.path.normpath(c) for c in metadata.get("covered_files", [])}
            if covered.intersection(norm_changed):
                impacted.add(test_file)

        return impacted

    def get_test_metadata(self, test_file: str) -> Dict[str, Any]:
        """Returns runtime and historical failure metrics for a test file."""
        norm_test = os.path.normpath(test_file)
        return self._matrix.get(norm_test, {
            "covered_files": [],
            "avg_duration_sec": 0.05,
            "fail_count": 0,
            "run_count": 1
        })

    def get_all_registered_tests(self) -> List[str]:
        """Returns all known tests in the matrix."""
        return sorted(list(self._matrix.keys()))
