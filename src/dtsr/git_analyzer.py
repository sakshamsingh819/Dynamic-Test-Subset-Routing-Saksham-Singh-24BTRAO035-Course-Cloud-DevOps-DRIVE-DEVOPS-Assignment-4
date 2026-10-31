"""
Git Diff and Change Impact Analyzer
Author: Saksham Singh (24BTRAO035)
Extracts changed files, computes churn metrics, and categorizes commits into impact tiers.
"""
from enum import Enum
from pathlib import Path
from typing import List, Set, Dict, Optional
import subprocess
import os


class ChangeType(str, Enum):
    DOCS_ONLY = "DOCS_ONLY"            # Markdown, txt, license, images -> 0 tests
    TESTS_ONLY = "TESTS_ONLY"          # Only test files modified -> Run those tests directly
    INFRA_CONFIG = "INFRA_CONFIG"      # Build manifests, Docker, CI YAML -> Full suite
    CODE_CHANGE = "CODE_CHANGE"        # Source code touched -> AST/TIA routing


class GitDiffSummary:
    def __init__(self, changed_files: List[str], lines_added: int = 0, lines_deleted: int = 0):
        self.changed_files = [os.path.normpath(f) for f in changed_files]
        self.lines_added = lines_added
        self.lines_deleted = lines_deleted

    @property
    def total_churn(self) -> int:
        return self.lines_added + self.lines_deleted

    @property
    def source_files(self) -> List[str]:
        return [f for f in self.changed_files if f.startswith("src/") and f.endswith(".py")]

    @property
    def test_files(self) -> List[str]:
        return [f for f in self.changed_files if f.startswith("tests/") and f.endswith(".py")]

    @property
    def doc_files(self) -> List[str]:
        doc_exts = {".md", ".rst", ".pdf", ".png", ".jpg", ".jpeg", ".svg"}
        infra_set = set(self.infra_files)
        return [
            f for f in self.changed_files
            if (Path(f).suffix.lower() in doc_exts or (Path(f).suffix.lower() == ".txt" and f not in infra_set) or "docs/" in f)
            and f not in infra_set
        ]

    @property
    def infra_files(self) -> List[str]:
        infra_names = {
            "requirements.txt",
            "requirements-dev.txt",
            "setup.py",
            "pyproject.toml",
            "dockerfile",
            ".dockerignore",
            ".gitignore",
        }
        return [
            f for f in self.changed_files
            if Path(f).name.lower() in infra_names or f.startswith(".github/")
        ]


class GitAnalyzer:
    """Interacts with git to inspect commit diffs and categorize change severity."""

    def __init__(self, repo_root: Optional[str] = None):
        self.repo_root = Path(repo_root or os.getcwd()).resolve()

    def _run_git(self, args: List[str]) -> str:
        try:
            res = subprocess.run(
                ["git"] + args,
                cwd=str(self.repo_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            return res.stdout.strip()
        except subprocess.CalledProcessError as e:
            # Return empty or fallback
            return ""
        except FileNotFoundError:
            return ""

    def get_diff_summary(self, base_ref: Optional[str] = None, head_ref: str = "HEAD") -> GitDiffSummary:
        """
        Computes changed files and line churn.
        If base_ref is given, runs `git diff --name-only base_ref..head_ref`.
        If base_ref is None, checks unstaged + staged changes against HEAD.
        """
        changed: Set[str] = set()
        added = 0
        deleted = 0

        if base_ref:
            raw_files = self._run_git(["diff", "--name-only", f"{base_ref}..{head_ref}"])
            if raw_files:
                changed.update(line.strip() for line in raw_files.splitlines() if line.strip())

            raw_stat = self._run_git(["diff", "--shortstat", f"{base_ref}..{head_ref}"])
            added, deleted = self._parse_shortstat(raw_stat)
        else:
            # Check staged + unstaged changes
            staged = self._run_git(["diff", "--cached", "--name-only"])
            if staged:
                changed.update(line.strip() for line in staged.splitlines() if line.strip())

            unstaged = self._run_git(["diff", "--name-only"])
            if unstaged:
                changed.update(line.strip() for line in unstaged.splitlines() if line.strip())

            # Also check untracked files
            untracked = self._run_git(["ls-files", "--others", "--exclude-standard"])
            if untracked:
                changed.update(line.strip() for line in untracked.splitlines() if line.strip())

            # Churn calculation
            raw_stat = self._run_git(["diff", "--shortstat", "HEAD"])
            added, deleted = self._parse_shortstat(raw_stat)

        return GitDiffSummary(sorted(list(changed)), added, deleted)

    def _parse_shortstat(self, text: str) -> tuple[int, int]:
        # Example format: " 3 files changed, 25 insertions(+), 8 deletions(-) "
        import re
        add_match = re.search(r"(\d+)\s+insertion", text)
        del_match = re.search(r"(\d+)\s+deletion", text)
        added = int(add_match.group(1)) if add_match else 0
        deleted = int(del_match.group(1)) if del_match else 0
        return added, deleted

    def classify_changes(self, summary: GitDiffSummary) -> ChangeType:
        """
        Classifies change tiers according to strict safety hierarchy:
        1. INFRA_CONFIG: changes to requirements, setup, CI workflows -> FULL SUITE
        2. CODE_CHANGE: any python changes in src/ -> AST & TIA ROUTING
        3. TESTS_ONLY: changes exclusively inside tests/ -> RUN ONLY THOSE TESTS
        4. DOCS_ONLY: changes purely in docs, readmes, text -> ZERO TESTS
        """
        if not summary.changed_files:
            return ChangeType.DOCS_ONLY

        # Priority 1: Infrastructure or core config
        if summary.infra_files:
            return ChangeType.INFRA_CONFIG

        # Priority 2: Source code changes
        if summary.source_files:
            return ChangeType.CODE_CHANGE

        # Priority 3: Only test files changed
        if summary.test_files and not summary.source_files:
            return ChangeType.TESTS_ONLY

        # Priority 4: Pure documentation
        if summary.doc_files and len(summary.doc_files) == len(summary.changed_files):
            return ChangeType.DOCS_ONLY

        # Default fallback
        return ChangeType.CODE_CHANGE
