# Dynamic Test-Subset Routing (DTSR)

[![CI Pipeline](https://img.shields.io/badge/CI-Passing-brightgreen?style=flat-square&logo=githubactions)](.github/workflows/test-subset-routing.yml)
[![Tests Passing](https://img.shields.io/badge/Tests-61%2F61%20Passed-success?style=flat-square&logo=pytest)](tests/)
[![Time Saved](https://img.shields.io/badge/CI%20Compute%20Saved-43.0%25-blue?style=flat-square)](scripts/benchmark.py)
[![Python Version](https://img.shields.io/badge/Python-3.12%20%7C%203.14-blue?style=flat-square&logo=python)](pyproject.toml)
[![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)](LICENSE)

**Candidate**: Saksham Singh  
**USN / Student ID**: 24BTRAO035  
**Branch**: AI DRIVEN DEVOPS  
**Course**: Automation Software (Unit III/IV Practicum)  
**Repository**: [https://github.com/sakshamsingh819/Dynamic-Test-Subset-Routing-Saksham-Singh-24BTRAO035-Course-Automation-Software-Assignment-4](https://github.com/sakshamsingh819/Dynamic-Test-Subset-Routing-Saksham-Singh-24BTRAO035-Course-Automation-Software-Assignment-4)  
**Dossier Report**: [`Dynamic_Test_Subset_Routing_Learnings_Report.pdf`](Dynamic_Test_Subset_Routing_Learnings_Report.pdf) | [`LEARNING_DOCUMENT.md`](LEARNING_DOCUMENT.md)

---

## Overview

**Dynamic Test-Subset Routing (DTSR)** is an enterprise-grade CI/CD optimization engine that accelerates software delivery pipelines by intelligently selecting and executing only the test suites impacted by incoming code changes.

Rather than executing monolithic regression suites on every commit, DTSR synthesizes:
1. **Abstract Syntax Tree (AST) Dependency Graph Closure**: Statically determines transitive consumers of changed modules.
2. **Dynamic Test Impact Analysis (TIA)**: Traces runtime code execution footprints to identify affected test suites.
3. **Predictive Risk Prioritization**: Computes fail-fast priority queues using code churn, failure rates, and test speeds.
4. **Greedy LPT Parallel CI Sharding**: Balances execution evenly across parallel GitHub Actions runners.
5. **Defensive Safety Guardrails**: Triggers automated full regression fallbacks for infrastructure or package manifest changes.

---

## Architecture Flow

```
[ Developer Git Diff / PR ]
           │
           ▼
[ GitAnalyzer: Change Classifier ]
    ├── DOCS_ONLY      ──────> [ 0 Tests Run | 100% Time Saved ]
    ├── INFRA_CONFIG   ──────> [ Fallback: 100% Full Regression Suite ]
    ├── TESTS_ONLY     ──────> [ Route Modified Test Suites Only ]
    └── CODE_CHANGE    ──────> [ AST Transitive Graph ] ⋃ [ TIA Coverage Matrix ]
                                            │
                                            ▼
                              [ RiskScorer: Fail-Fast Prioritization ]
                                            │
                                            ▼
                              [ Sharder: Greedy LPT Parallel Bin-Packing ]
                                            │
                                            ▼
                              [ Parallel GitHub Actions Runners (Shard 1 & 2) ]
```

---

## Quickstart & Installation

```bash
# Clone the repository
git clone https://github.com/sakshamsingh819/Dynamic-Test-Subset-Routing-Saksham-Singh-24BTRAO035-Course-Automation-Software-Assignment-4.git
cd Dynamic-Test-Subset-Routing-Saksham-Singh-24BTRAO035-Course-Automation-Software-Assignment-4

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies and DTSR in editable mode
pip install -r requirements-dev.txt
pip install -e .
```

---

## Running Verification & Pytest

Execute all 61 automated tests covering unit, integration, system, and engine components:

```bash
pytest -v
```

Output:
```text
======================== 61 passed in 0.29s =========================
```

---

## CLI Usage

The DTSR engine provides a command-line interface via `dtsr` or `python -m src.dtsr.cli`:

### 1. Compute Dynamic Test Route
```bash
# Route tests impacted by changes against main branch
dtsr route --base origin/main --head HEAD --shards 2

# Route tests for specific modified files
dtsr route --files "src/services/billing.py" --shards 2
```

### 2. Execute Routed Tests
```bash
dtsr run --files "src/services/billing.py"
```

### 3. Inspect AST & TIA Topology
```bash
dtsr map
```

### 4. Output GitHub Actions Matrix JSON
```bash
dtsr ci-matrix --base origin/main --head HEAD --shards 2
```

### 5. Run Empirical Benchmark Suite
```bash
python scripts/benchmark.py
```

---

## Empirical Benchmark Results

Evaluated across 5 pull request archetypes:

| PR ID | Scenario Title | Change Tier | Full Suites | Routed Suites | Duration (s) | Saved % |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **PR-01** | Documentation & README Updates | `DOCS_ONLY` | 16 | **0** | 0.00 / 1.78s | **100.0%** |
| **PR-02** | Validator Regex Boundary Hardening | `CODE_CHANGE` | 16 | **8** | 1.39 / 1.78s | **21.9%** |
| **PR-03** | Tiered Discount Logic Refactor | `CODE_CHANGE` | 16 | **4** | 1.01 / 1.78s | **43.3%** |
| **PR-04** | HMAC Token Cryptography Patch | `CODE_CHANGE` | 16 | **4** | 0.89 / 1.78s | **50.0%** |
| **PR-05** | Requirements Package Manifest Bump | `INFRA_CONFIG` | 16 | **16** | 1.78 / 1.78s | **0.0%** (Safety Fallback) |
| **TOTAL** | **Cumulative 5-PR Evaluation** | — | **80** | **32** | **5.07 / 8.90s** | **43.0% Overall Savings** |

---

## Project Structure

```
dynamic-test-subset-routing/
├── .github/
│   └── workflows/
│       ├── test-subset-routing.yml       # Dynamic PR matrix CI pipeline
│       └── nightly-full-suite.yml        # Nightly 100% full regression guardrail
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
├── setup.py
├── pyproject.toml
├── README.md
├── LEARNING_DOCUMENT.md                  # Comprehensive step-by-step learning dossier
├── Dynamic_Test_Subset_Routing_Learnings_Report.pdf  # Publication-grade PDF dossier
├── src/
│   ├── services/                         # Business microservice ecosystem
│   │   ├── auth.py
│   │   ├── billing.py
│   │   ├── inventory.py
│   │   ├── order.py
│   │   └── notifications.py
│   ├── utils/                            # Cryptography & schema validator utilities
│   │   ├── crypto.py
│   │   └── validators.py
│   └── dtsr/                             # Dynamic Test-Subset Routing Engine
│       ├── git_analyzer.py               # Diff inspection & change tier categorization
│       ├── ast_graph.py                  # Static AST dependency graph & reachability
│       ├── impact_tracer.py              # Dynamic runtime coverage matrix (TIA)
│       ├── risk_scorer.py                # Fail-fast predictive prioritization
│       ├── sharder.py                    # Greedy LPT parallel CI bin-packing
│       ├── router.py                     # Master routing orchestrator
│       └── cli.py                        # Unified Click CLI tool
├── tests/                                # 61 automated pytest test suites
│   ├── conftest.py
│   ├── unit/
│   ├── integration/
│   ├── system/
│   └── dtsr/
└── scripts/
    ├── benchmark.py                      # Multi-scenario empirical benchmark runner
    └── generate_pdf_report.py            # WeasyPrint PDF report generator
```

---

## License

This project is released under the MIT License. Academic Submission for **Saksham Singh (24BTRAO035)**.
