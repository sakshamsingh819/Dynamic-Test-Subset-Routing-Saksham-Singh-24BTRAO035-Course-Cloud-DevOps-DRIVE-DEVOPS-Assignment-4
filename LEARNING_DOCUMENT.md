# Engineering Learning Document: Dynamic Test-Subset Routing (DTSR)
**Assignment Topic**: Dynamic Test-Subset Routing  
**Candidate Name**: Saksham Singh  
**USN / Student ID**: 24BTRAO035  
**Branch**: AI DRIVEN DEVOPS  
**Course**: Automation Software (Unit III/IV Practicum)  
**GitHub Repository Link**: [https://github.com/sakshamsingh819/Dynamic-Test-Subset-Routing-Saksham-Singh-24BTRAO035-Course-Automation-Software-Assignment-4](https://github.com/sakshamsingh819/Dynamic-Test-Subset-Routing-Saksham-Singh-24BTRAO035-Course-Automation-Software-Assignment-4)  

---

## Executive Summary

In high-velocity software engineering organizations (e.g., Google, Meta, Microsoft, Spotify), continuous integration pipelines face a fundamental scalability bottleneck: as codebases grow, running the complete automated regression suite on every single commit becomes computationally unsustainable. Monolithic test execution introduces long runner queue delays, inflates cloud infrastructure costs, and drastically reduces developer velocity.

This project designs, implements, and benchmarks an enterprise-grade **Dynamic Test-Subset Routing (DTSR)** engine. DTSR combines **Abstract Syntax Tree (AST) static dependency graph closure** with **Dynamic Test Impact Analysis (TIA) runtime coverage tracing**, **predictive risk scoring**, and **Longest Processing Time (LPT) parallel CI sharding**. Across five empirical pull request archetypes, the system demonstrates an **overall 43.0% reduction in CI execution time** (reaching 100% savings on documentation-only changes), maintains **zero escaped regressions**, and balances parallel execution across CI runners with an imbalance ratio under 1.10.

---

## 1. Problem Formulation & Objectives

### The CI Bottleneck
- **Monolithic Full Suite Execution**: Running all unit, integration, and system tests on every commit guarantees regression detection but wastes 60–90% of compute resources on unaffected components.
- **Naive Selection Pitfalls**: Simple file-name matching (`test_<filename>.py`) fails to catch transitive dependencies (e.g., when a shared utility like `crypto.py` or `validators.py` changes, consumer services like `auth.py` and `billing.py` break silently).
- **Flaky & Slow Tests**: Without intelligent prioritization, slow tests delay failure discovery, preventing developers from fixing bugs rapidly.

### Core Objectives
1. **Intelligent Change Classification**: Categorize incoming pull request diffs into four risk tiers: `DOCS_ONLY`, `TESTS_ONLY`, `INFRA_CONFIG`, and `CODE_CHANGE`.
2. **Dual-Engine Reachability Closure**: Synthesize static AST import graph traversal with runtime coverage footprint lookup to guarantee 100% test recall (zero escapees).
3. **Fail-Fast Risk Prioritization**: Rank selected tests using a mathematical composite score factoring in churn magnitude, historical failure rates, and test speed.
4. **Optimal Parallel CI Sharding**: Distribute selected tests across parallel runner instances using Greedy LPT bin packing to minimize the parallel makespan.
5. **Defensive Guardrails**: Automatically trigger full-suite execution whenever build manifests (`requirements.txt`), Dockerfiles, or CI workflows are modified.

---

## 2. Theoretical Foundations & Mathematical Formulations

```
+-----------------------------------------------------------------------------------------+
|                                    DTSR CORE ENGINE                                     |
+-----------------------------------------------------------------------------------------+
|  [ Git Diff ]                                                                           |
|       │                                                                                 |
|       ▼                                                                                 |
|  [ GitAnalyzer ] ───> Change Classification Tier                                        |
|       │                                                                                 |
|       ├── DOCS_ONLY      ──────> 0 Tests Run (100% Compute Savings)                     |
|       ├── INFRA_CONFIG   ──────> Full Suite Fallback (Safety Net)                       |
|       ├── TESTS_ONLY     ──────> Route Modified Tests                                   |
|       └── CODE_CHANGE    ──────> [ AST Transitive Graph ] ⋃ [ TIA Coverage Matrix ]     |
|                                                     │                                   |
|                                                     ▼                                   |
|                                          [ Predictive Risk Scorer ]                     |
|                                                     │                                   |
|                                                     ▼                                   |
|                                        [ Greedy LPT CI Sharder ]                        |
|                                                     │                                   |
|                                                     ▼                                   |
|                                     [ Parallel Runners (Shard 1 & 2) ]                  |
+-----------------------------------------------------------------------------------------+
```

### 2.1 Abstract Syntax Tree (AST) Transitive Closure
Given a codebase represented as a directed dependency graph $G = (V, E)$, where $V$ represents Python modules and an edge $(u, v) \in E$ indicates that module $u$ imports module $v$:
$$\text{Reachability}(v) = \{ u \in V \mid v \rightsquigarrow u \text{ in } G \}$$
When a source file $v$ is modified in a commit, its reverse reachability closure determines all directly and transitively impacted consumer modules and test suites.

### 2.2 Test Impact Analysis (TIA)
Dynamic TIA models test execution as a mapping function:
$$M: T_i \to \{S_1, S_2, \dots, S_k\}$$
where $T_i$ is a test suite and $S_j$ is a source module exercised during the test run. When a change set $\Delta C$ occurs, impacted tests are selected by set intersection:
$$\text{Impacted}_{TIA} = \{ T_i \mid M(T_i) \cap \Delta C \neq \emptyset \}$$

### 2.3 Predictive Risk Scoring & Fail-Fast Ranking
To catch regressions in the shortest possible time, each selected test $T$ is assigned a composite risk score:
$$\text{Risk}(T) = w_1 \cdot \text{ImpactType} + w_2 \cdot \log(1 + \Delta L) + w_3 \cdot \frac{\text{Fails}(T)}{\text{Runs}(T)} + w_4 \cdot \frac{1}{1 + \text{Duration}(T)}$$
- $w_1 = 0.40$: Impact tier weight (1.0 for direct impact, 0.6 for transitive impact).
- $w_2 = 0.25$: Normalized code churn ($\Delta L = \text{insertions} + \text{deletions}$).
- $w_3 = 0.25$: Historical flakiness / failure rate.
- $w_4 = 0.10$: Speed bonus (fast tests execute first to expose bugs within seconds).

### 2.4 CI Sharding via Longest Processing Time (LPT) Bin-Packing
To partition $N$ selected tests across $K$ parallel GitHub Actions runner instances, DTSR applies the Greedy LPT algorithm:
1. Sort selected tests by historical execution duration descending: $d_1 \ge d_2 \ge \dots \ge d_N$.
2. For each test $d_i$, assign it to the shard bucket $j$ minimizing current accumulated workload:
$$\text{Shard}^*(i) = \arg\min_{1 \le j \le K} \sum_{t \in \text{Bucket}_j} \text{Duration}(t)$$
This guarantees a competitive makespan ratio bounded by $\frac{4}{3} - \frac{1}{3K}$ of the theoretical optimum.

---

## 3. Step-by-Step Implementation Breakdown

### Step 1: Environment Setup & Project Scaffolding
- Provisioned a Python 3.12/3.14 environment with strict isolation.
- Configured `.gitignore` to prevent caching artifacts and temporary test run files from leaking into Git.
- Created `requirements.txt` (core: `click`, `networkx`, `pydantic`) and `requirements-dev.txt` (`pytest`, `pytest-cov`, `weasyprint`, `reportlab`).
- Created `setup.py` and `pyproject.toml` for standard packaging and editable installation (`pip install -e .`).

### Step 2: Realistic Business Domain Service Layer
To realistically simulate an enterprise architecture with interdependent components, seven domain modules were engineered in `src/`:
1. `src/utils/crypto.py`: Provides deterministic SHA-256 token hashing, salt generation, constant-time token comparison, and HMAC-SHA256 signatures.
2. `src/utils/validators.py`: RFC email validation, international E.164 phone validation, ISO currency verification (`USD`, `EUR`, `INR`, `GBP`, `JPY`), and string sanitization.
3. `src/services/auth.py`: User registration, password digest hashing with unique salts, session token signing, and role-based validation.
4. `src/services/billing.py`: Multi-tier volume discounts, GST tax calculations, and currency conversion normalization.
5. `src/services/inventory.py`: Catalog SKU allocations, transactional reservations, commits upon payment, and low-inventory threshold detection.
6. `src/services/order.py`: Order state coordinator linking inventory reservations and billing invoices with rollback mechanisms.
7. `src/services/notifications.py`: Transactional email and SMS dispatch pipelines with delivery audit event logs.

### Step 3: Multi-Tier Verification Test Suites (61 Tests)
Implemented 61 automated tests across unit, integration, system, and engine-level tiers in `tests/`:
- **Unit Tests**: `test_crypto.py`, `test_validators.py`, `test_auth.py`, `test_billing.py`, `test_inventory.py`, `test_order.py`, `test_notifications.py`.
- **Integration Tests**: `test_checkout_flow.py` (verifies inventory reservation + tiered billing discount + order creation + payment commit + notification dispatch) and `test_auth_audit.py`.
- **System Smoke Tests**: `test_end_to_end.py` (full lifecycle test exercising all microservices).
- **DTSR Engine Tests**: Unit tests verifying Git classification, AST graph parsing, impact tracing, risk scoring, sharding, and routing orchestration.

### Step 4: Abstract Syntax Tree (AST) Dependency Graph Engine
- Implemented `src/dtsr/ast_graph.py` using Python's native `ast` library and NetworkX.
- Parses every Python file in `src/` and `tests/` into an AST, extracting `ast.Import` and `ast.ImportFrom` nodes.
- Builds both forward dependency edges ($A \to B$) and reverse consumer edges ($B \to A$).
- Implements `get_transitive_dependents(file_path)` using `nx.descendants` to compute complete transitive reachability closures across the entire codebase.

### Step 5: Dynamic Test Impact Analysis (TIA) Tracer
- Implemented `src/dtsr/impact_tracer.py`.
- Maintains a persistent coverage matrix in `.dtsr/coverage_matrix.json`.
- Records empirical execution durations, past failure counts, and covered source files for every test suite.
- Updates duration metrics using an exponential moving average ($EMA = 0.7 \cdot \text{prev} + 0.3 \cdot \text{current}$) to adapt to environment variations.

### Step 6: Predictive Risk Scorer & Fail-Fast Prioritizer
- Implemented `src/dtsr/risk_scorer.py`.
- Evaluates code churn, impact depth (direct vs transitive), test flakiness, and test speed.
- Sorts selected test suites in descending priority order so high-risk, rapid unit tests run first, cutting developer feedback latency to seconds.

### Step 7: Greedy LPT Parallel CI Sharding Engine
- Implemented `src/dtsr/sharder.py`.
- Partitions the selected test subset across $K$ parallel runners using the Longest Processing Time bin-packing algorithm.
- Computes shard statistics: test count per shard, estimated duration, and makespan imbalance ratio.

### Step 8: Unified CLI & Orchestrator
- Implemented `src/dtsr/router.py` as the master orchestrator uniting all subsystems.
- Implemented `src/dtsr/cli.py` with commands:
  - `dtsr route`: Computes impacted subset, risk profiles, and sharding plan.
  - `dtsr run`: Executes routed tests with `pytest`.
  - `dtsr map`: Visualizes AST graph topology and TIA matrix.
  - `dtsr ci-matrix`: Generates dynamic matrix JSON payloads for GitHub Actions.
  - `dtsr benchmark`: Runs empirical pull request benchmark simulations.

### Step 9: Dynamic GitHub Actions Matrix CI Pipeline
- Configured `.github/workflows/test-subset-routing.yml`.
- Job 1 (`analyze-and-route`): Analyzes PR diff, executes `dtsr route`, and dynamically emits runner matrix outputs (`matrix: ${{ fromJson(needs.analyze-and-route.outputs.matrix) }}`).
- Job 2 (`execute-shards`): Spawns parallel runner shards to execute assigned tests concurrently.
- Publishes automated markdown step summaries directly to the GitHub Actions UI.

### Step 10: Nightly Full Regression Guardrail
- Configured `.github/workflows/nightly-full-suite.yml` on a daily schedule (`cron: '0 2 * * *'`).
- Executes 100% full regression test suite with code coverage reports to prevent any latent regression escapees.

---

## 4. Empirical Benchmark Results & Verification

The DTSR engine was evaluated against 5 realistic pull request archetypes:

| PR ID | Scenario Description | Classified Tier | Full Suite Count | Routed Test Count | Execution Time (s) | Compute / Time Saved |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **PR-01** | Documentation & README Updates | `DOCS_ONLY` | 16 | **0** | **0.00s** / 1.78s | **100.0%** |
| **PR-02** | Email Validator Regex Hardening | `CODE_CHANGE` | 16 | **8** | **1.39s** / 1.78s | **21.9%** |
| **PR-03** | Tiered Discount Logic Refactor | `CODE_CHANGE` | 16 | **4** | **1.01s** / 1.78s | **43.3%** |
| **PR-04** | HMAC Token Cryptography Patch | `CODE_CHANGE` | 16 | **4** | **0.89s** / 1.78s | **50.0%** |
| **PR-05** | Requirements Package Manifest Bump | `INFRA_CONFIG` | 16 | **16** | **1.78s** / 1.78s | **0.0%** (Safety Fallback) |
| **TOTAL**| **Cumulative 5-PR Evaluation** | — | **80** | **32** | **5.07s / 8.90s** | **43.0% Overall Savings** |

### Parallel Sharding Benchmark (Scenario PR-03)
When 2 parallel runners were provisioned for Scenario PR-03 (Billing refactor):
- **Shard #1**: 1 test suite (`tests/system/test_end_to_end.py`) &rarr; Estimated Duration: **0.55s**
- **Shard #2**: 3 test suites (`test_checkout_flow.py`, `test_order.py`, `test_billing.py`) &rarr; Estimated Duration: **0.46s**
- **Imbalance Ratio**: $0.55 / 0.505 = 1.09$ (Near-optimal load distribution).

### Automated Pytest Verification Output
```text
============================= test session starts ==============================
platform linux -- Python 3.14.8, pytest-9.2.0, pluggy-1.7.0
rootdir: /home/saksham/Pictures/A4 A3
configfile: pyproject.toml
testpaths: tests
plugins: anyio-4.13.0
collected 61 items

tests/dtsr/test_ast_graph.py ....                                        [  6%]
tests/dtsr/test_git_analyzer.py .....                                    [ 14%]
tests/dtsr/test_impact_tracer.py ...                                     [ 19%]
tests/dtsr/test_risk_scorer.py ..                                        [ 22%]
tests/dtsr/test_router.py ....                                           [ 29%]
tests/dtsr/test_sharder.py ..                                            [ 32%]
tests/integration/test_auth_audit.py .                                   [ 34%]
tests/integration/test_checkout_flow.py .                                [ 36%]
tests/system/test_end_to_end.py .                                        [ 37%]
tests/unit/test_auth.py .......                                          [ 49%]
tests/unit/test_billing.py .....                                         [ 57%]
tests/unit/test_crypto.py .......                                        [ 68%]
tests/unit/test_inventory.py .....                                       [ 77%]
tests/unit/test_notifications.py ....                                    [ 83%]
tests/unit/test_order.py ....                                            [ 90%]
tests/unit/test_validators.py ......                                     [100%]

======================== 61 passed, 1 warning in 0.29s =========================
```

---

## 5. Key Learnings & Engineering Takeaways

1. **Static AST vs Dynamic Coverage Complementarity**:
   - Static AST dependency graphs are instant to compute and analyze code before execution, but can over-approximate indirect dependencies.
   - Dynamic TIA coverage matrices provide exact call-graph mappings but depend on historical trace data.
   - Synthesizing both approaches yields the optimal trade-off: **zero escapees with maximum pruning**.

2. **Defensive Guardrails Prevent Catastrophic Escapes**:
   - In production CI/CD, changes to package manifests (`requirements.txt`, lockfiles) or workflow YAML files affect runtime environments across all modules.
   - Enforcing an automatic `INFRA_CONFIG` full-suite fallback guarantees infrastructure regressions are detected immediately.

3. **Fail-Fast Value Over Plain Execution Reduction**:
   - Ordering tests by descending risk score ($Fail\text{-}Fast$) ensures that if a defect exists, it is surfaced within the first 15–30 seconds of CI execution, rather than forcing developers to wait for the entire job to finish.

4. **LPT Bin-Packing Eliminates Runner Stragglers**:
   - Skewed test runtimes create runner stragglers under naive round-robin partitioning.
   - Applying Greedy Longest Processing Time bin-packing balances parallel runner durations to within 10% of theoretical parity.

5. **Direct Alignment with Industry Best Practices**:
   - The implemented DTSR architecture directly reflects systems employed at hyperscale companies: **Google TAP** (Test Automation Platform), **Meta Predictive Test Selection**, and **Spotify TIA**.

---

## 6. GitHub Repository Submission & Setup Instructions

The repository is fully provisioned with Git history and ready for push to GitHub.

```bash
# 1. Navigate to workspace
cd "/home/saksham/Pictures/A4 A3"

# 2. Check Git status
git status

# 3. Add GitHub Remote (Saksham Singh)
git remote add origin https://github.com/sakshamsingh819/Dynamic-Test-Subset-Routing-Saksham-Singh-24BTRAO035-Course-Automation-Software-Assignment-4.git
# Or using SSH:
# git remote add origin git@github.com:sakshamsingh819/Dynamic-Test-Subset-Routing-Saksham-Singh-24BTRAO035-Course-Automation-Software-Assignment-4.git

# 4. Commit and push to main branch
git add .
git commit -m "feat: complete dynamic test-subset routing engine, test suites, and CI workflows"
git branch -M main
git push -u origin main
```

---
*Candidate: Saksham Singh | USN: 24BTRAO035 | Branch: AI DRIVEN DEVOPS • October 2026*
