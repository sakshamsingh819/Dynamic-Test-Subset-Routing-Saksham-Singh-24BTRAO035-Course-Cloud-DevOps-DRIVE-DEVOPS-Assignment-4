"""
Academic Dossier & PDF Report Generator for Dynamic Test-Subset Routing
Author: Saksham Singh (24BTRAO035)
Branch: AI DRIVEN DEVOPS | Department of Computer Science & Engineering
Jain (Deemed-to-be University)
"""
import os
import sys
import time
from pathlib import Path
import weasyprint

REPO_URL = "https://github.com/sakshamsingh819/Dynamic-Test-Subset-Routing-Saksham-Singh-24BTRAO035-Course-Cloud-DevOps-DRIVE-DEVOPS-Assignment-4"

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Dynamic Test-Subset Routing - Academic Laboratory Dossier</title>
<style>
  @page {
    size: A4;
    margin: 18mm 16mm 20mm 16mm;
    @top-left {
      content: "JAIN (DEEMED-TO-BE UNIVERSITY) • DEPT OF CSE • AI DRIVEN DEVOPS";
      font-size: 7.5pt;
      font-family: 'Helvetica Neue', Arial, sans-serif;
      color: #64748b;
      font-weight: 600;
    }
    @top-right {
      content: "Dynamic Test-Subset Routing | Saksham Singh (24BTRAO035)";
      font-size: 7.5pt;
      font-family: 'Helvetica Neue', Arial, sans-serif;
      color: #64748b;
    }
    @bottom-left {
      content: "Academic Laboratory Dossier • Branch: AI DRIVEN DEVOPS";
      font-size: 7.5pt;
      font-family: 'Helvetica Neue', Arial, sans-serif;
      color: #64748b;
    }
    @bottom-right {
      content: "Page " counter(page) " of " counter(pages);
      font-size: 7.5pt;
      font-family: 'Helvetica Neue', Arial, sans-serif;
      color: #0f172a;
      font-weight: bold;
    }
  }

  body {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    color: #1e293b;
    line-height: 1.45;
    font-size: 9pt;
    margin: 0;
  }

  h1, h2, h3, h4 {
    color: #0f172a;
    font-weight: 700;
  }

  .institution-header {
    text-align: center;
    border-bottom: 2px solid #1e3a8a;
    padding-bottom: 8px;
    margin-bottom: 12px;
  }

  .univ-title {
    font-size: 11pt;
    font-weight: 800;
    letter-spacing: 0.8px;
    color: #1e3a8a;
    text-transform: uppercase;
    margin-bottom: 2px;
  }

  .dept-title {
    font-size: 8.5pt;
    font-weight: 600;
    color: #475569;
    margin-bottom: 2px;
  }

  .course-badge {
    display: inline-block;
    background: #e0e7ff;
    color: #3730a3;
    font-size: 7.5pt;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 4px;
    text-transform: uppercase;
  }

  .header-box {
    background: linear-gradient(135deg, #091e42 0%, #1e40af 100%);
    color: #ffffff;
    padding: 14px 18px;
    border-radius: 6px;
    margin-bottom: 14px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  .header-box h1 {
    color: #ffffff;
    font-size: 17pt;
    margin: 0 0 4px 0;
    line-height: 1.2;
  }

  .header-box .subtitle {
    font-size: 9.5pt;
    color: #bfdbfe;
    margin-bottom: 10px;
    font-weight: 500;
  }

  .meta-grid {
    display: table;
    width: 100%;
    margin-top: 6px;
    border-top: 1px solid rgba(255,255,255,0.25);
    padding-top: 8px;
    font-size: 8pt;
  }

  .meta-col {
    display: table-cell;
    width: 25%;
    vertical-align: top;
  }

  .meta-label {
    color: #93c5fd;
    text-transform: uppercase;
    font-size: 6.5pt;
    letter-spacing: 0.5px;
    font-weight: bold;
  }

  .meta-value {
    color: #ffffff;
    font-weight: 700;
    margin-top: 2px;
  }

  .repo-link-box {
    background: #0b1528;
    color: #38bdf8;
    padding: 8px 12px;
    border-radius: 5px;
    margin-top: 10px;
    border: 1px solid #1e3a8a;
    border-left: 4px solid #38bdf8;
  }

  .repo-link-box a {
    color: #38bdf8;
    text-decoration: underline;
    font-weight: bold;
    font-family: 'Consolas', monospace;
    font-size: 7.8pt;
    word-break: break-all;
  }

  .btn-open-repo {
    display: inline-block;
    background: #2563eb;
    color: #ffffff !important;
    text-decoration: none !important;
    padding: 4px 10px;
    border-radius: 4px;
    font-weight: 700;
    font-size: 7.5pt;
    margin-top: 5px;
    letter-spacing: 0.3px;
    border: 1px solid #60a5fa;
  }

  h2 {
    font-size: 11.5pt;
    margin-top: 16px;
    margin-bottom: 6px;
    border-bottom: 1.5px solid #cbd5e1;
    padding-bottom: 3px;
    color: #1e3a8a;
    text-transform: uppercase;
    letter-spacing: 0.3px;
  }

  h3 {
    font-size: 9.5pt;
    margin-top: 10px;
    margin-bottom: 3px;
    color: #1e293b;
  }

  p {
    margin-top: 3px;
    margin-bottom: 6px;
    text-align: justify;
  }

  .badge {
    display: inline-block;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 7pt;
    font-weight: 700;
    text-transform: uppercase;
  }
  .badge-blue { background: #dbeafe; color: #1e40af; }
  .badge-green { background: #dcfce7; color: #15803d; }
  .badge-amber { background: #fef3c7; color: #b45309; }
  .badge-purple { background: #f3e8ff; color: #6b21a8; }

  table {
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0;
    font-size: 8pt;
  }

  th {
    background: #f1f5f9;
    color: #1e293b;
    font-weight: 700;
    text-align: left;
    padding: 5px 7px;
    border: 1px solid #cbd5e1;
  }

  td {
    padding: 4px 7px;
    border: 1px solid #e2e8f0;
    vertical-align: top;
  }

  tr:nth-child(even) td {
    background: #f8fafc;
  }

  .code-block {
    background: #0f172a;
    color: #f8fafc;
    font-family: 'Consolas', 'Menlo', 'Monaco', monospace;
    font-size: 7pt;
    padding: 7px 9px;
    border-radius: 5px;
    margin: 6px 0;
    white-space: pre-wrap;
    line-height: 1.3;
    border-left: 3px solid #38bdf8;
  }

  .callout {
    background: #f0fdf4;
    border-left: 3.5px solid #16a34a;
    padding: 7px 10px;
    margin: 8px 0;
    border-radius: 0 5px 5px 0;
    font-size: 8.5pt;
  }

  .callout-title {
    font-weight: bold;
    color: #15803d;
    margin-bottom: 2px;
  }

  .callout-arch {
    background: #f8fafc;
    border-left: 3.5px solid #2563eb;
    padding: 7px 10px;
    margin: 8px 0;
    border-radius: 0 5px 5px 0;
    font-size: 8.5pt;
  }

  .qa-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 3px solid #4f46e5;
    padding: 6px 10px;
    margin: 6px 0;
    border-radius: 0 4px 4px 0;
  }

  .qa-question {
    font-weight: 700;
    color: #312e81;
    font-size: 8.5pt;
    margin-bottom: 2px;
  }

  .qa-answer {
    color: #334155;
    font-size: 8pt;
    text-align: justify;
  }

  .submission-card {
    background: #eff6ff;
    border: 1.5px solid #3b82f6;
    border-radius: 6px;
    padding: 10px 14px;
    margin: 12px 0;
    text-align: center;
  }

  .submission-card a {
    color: #1d4ed8;
    font-weight: bold;
    font-size: 8.5pt;
    text-decoration: underline;
    word-break: break-all;
  }

  .page-break {
    page-break-before: always;
  }
</style>
</head>
<body>

<!-- Institutional Header -->
<div class="institution-header">
  <div class="univ-title">Jain (Deemed-to-be University)</div>
  <div class="dept-title">Faculty of Engineering and Technology • Department of Computer Science and Engineering</div>
  <div class="course-badge">Branch: AI DRIVEN DEVOPS • Assignment 4 (Activity 3)</div>
</div>

<!-- Header Box -->
<div class="header-box">
  <h1>Dynamic Test-Subset Routing (DTSR)</h1>
  <div class="subtitle">Change-Based Predictive Test Selection, AST Reachability Closure & Parallel CI Sharding</div>
  <div class="meta-grid">
    <div class="meta-col">
      <div class="meta-label">Candidate Name</div>
      <div class="meta-value">Saksham Singh</div>
    </div>
    <div class="meta-col">
      <div class="meta-label">USN / Roll Number</div>
      <div class="meta-value">24BTRAO035</div>
    </div>
    <div class="meta-col">
      <div class="meta-label">Branch / Track</div>
      <div class="meta-value">AI DRIVEN DEVOPS</div>
    </div>
    <div class="meta-col">
      <div class="meta-label">Verification Status</div>
      <div class="meta-value">100% Passed (61/61 Suites)</div>
    </div>
  </div>
  
  <div class="repo-link-box">
    <div style="font-size: 7pt; color: #93c5fd; text-transform: uppercase; font-weight: bold; margin-bottom: 3px;">
      🔗 DIRECT GITHUB REPOSITORY LINK (CLICK TO OPEN IN BROWSER):
    </div>
    <a href="https://github.com/sakshamsingh819/Dynamic-Test-Subset-Routing-Saksham-Singh-24BTRAO035-Course-Cloud-DevOps-DRIVE-DEVOPS-Assignment-4" target="_blank">
      https://github.com/sakshamsingh819/Dynamic-Test-Subset-Routing-Saksham-Singh-24BTRAO035-Course-Cloud-DevOps-DRIVE-DEVOPS-Assignment-4
    </a>
    <div style="margin-top: 4px;">
      <a class="btn-open-repo" href="https://github.com/sakshamsingh819/Dynamic-Test-Subset-Routing-Saksham-Singh-24BTRAO035-Course-Cloud-DevOps-DRIVE-DEVOPS-Assignment-4" target="_blank">
        🚀 CLICK HERE TO OPEN GITHUB REPO IN BROWSER &rarr;
      </a>
    </div>
  </div>
</div>

<!-- 1. Executive Summary & Problem Formulation -->
<h2>1. Executive Summary & Problem Formulation</h2>
<p>
In modern Continuous Integration and Continuous Deployment (CI/CD) environments, monolithic test execution on every
commit introduces severe development bottlenecks. As enterprise codebases grow, executing full automated regression suites
on every commit inflates runner queue times, wastes compute credits, and impairs developer feedback loops.
</p>
<p>
This project designs, implements, and benchmarks an enterprise-grade <strong>Dynamic Test-Subset Routing (DTSR)</strong> system.
DTSR synthesizes static <strong>Abstract Syntax Tree (AST) import dependency graphs</strong> with dynamic <strong>Test Impact Analysis (TIA)
runtime coverage tracing</strong>, <strong>predictive risk scoring</strong>, and <strong>Longest Processing Time (LPT) parallel sharding</strong>. Across 5
empirical pull request archetypes, DTSR achieved an <strong>overall 43.0% reduction in CI execution duration</strong> (saving 100% on
documentation changes) with an empirical <strong>zero escape rate</strong>.
</p>

<!-- 2. Theoretical Foundations -->
<h2>2. Theoretical Foundations & Mathematical Formulations</h2>
<p>
The routing engine is formulated upon four foundational computer science principles:
</p>
<table>
  <tr>
    <th style="width: 25%;">Theoretical Pillar</th>
    <th style="width: 35%;">Mathematical / Algorithmic Model</th>
    <th style="width: 40%;">Engineering Function in CI/CD</th>
  </tr>
  <tr>
    <td><strong>AST Directed Graph Closure</strong></td>
    <td>\( G = (V, E) \)<br>Transitive Reachability: \( \text{Desc}(v) = \{u \in V \mid v \rightsquigarrow u\} \)</td>
    <td>Statically traces module dependencies and determines all downstream consumer modules and test suites impacted by changes to foundational components.</td>
  </tr>
  <tr>
    <td><strong>Test Impact Analysis (TIA)</strong></td>
    <td>Execution Footprint Mapping:<br>\( M: T_i \to \{S_1, S_2, \dots, S_k\} \)</td>
    <td>Dynamically maps each test suite to the exact source files and functions executed at runtime, capturing indirect data flows and duck-typed dependencies.</td>
  </tr>
  <tr>
    <td><strong>Predictive Risk Prioritization</strong></td>
    <td>\( \text{Risk}(T) = w_1 I + w_2 \log(1+\Delta L) + w_3 F_{hist} + w_4 S_{bonus} \)</td>
    <td>Orders the selected test subset by descending failure probability and execution speed to maximize <em>Fail-Fast</em> velocity in developer feedback loops.</td>
  </tr>
  <tr>
    <td><strong>LPT Bin-Packing Sharding</strong></td>
    <td>Makespan Minimization:<br>\( \min \max_{j} \sum_{i \in \text{Shard}_j} d_i \)</td>
    <td>Partitions the selected test subset across \( K \) parallel GitHub Actions runner instances, achieving near-perfect workload balance.</td>
  </tr>
</table>

<div class="callout-arch">
  <div class="callout-title">System Architecture Flowchart</div>
  <pre style="font-size: 7pt; margin: 3px 0; color: #1e3a8a; font-family: monospace;">
[ Git Diff / Pull Request ] 
         │
         ▼
[ GitAnalyzer: Change Classifier ]
    ├── DOCS_ONLY      ──────> [ Zero Tests Run | 100% Compute Saved ]
    ├── INFRA_CONFIG   ──────> [ Fallback: 100% Full Regression Suite ]
    ├── TESTS_ONLY     ──────> [ Route Only Modified Test Suites ]
    └── CODE_CHANGE    ──────> [ AST Transitive Closure + TIA Coverage Engine ]
                                            │
                                            ▼
                              [ RiskScorer: Fail-Fast Prioritization ]
                                            │
                                            ▼
                              [ Sharder: LPT Parallel Bin-Packing ]
                                            │
                                            ▼
                              [ Parallel GitHub Actions Runners (Shard #1, #2) ]
  </pre>
</div>

<div class="page-break"></div>

<!-- 3. Step-by-Step Implementation Guide -->
<h2>3. Step-by-Step Implementation Guide</h2>
<p>
The system was engineered through a disciplined 10-step software engineering methodology:
</p>

<h3>Step 1: Workspace Scaffolding & Virtual Environment Provisioning</h3>
<p>
Provisioned an isolated Python virtual environment, configuring <code>pyproject.toml</code> and <code>requirements.txt</code> with dependencies including <code>pytest</code>, <code>networkx</code>, <code>click</code>, <code>pydantic</code>, and <code>weasyprint</code>. Initialized Git repository with clean <code>main</code> branch hierarchy.
</p>

<h3>Step 2: Microservice Domain Service Architecture</h3>
<p>
Constructed a modular e-commerce service ecosystem inside <code>src/services/</code> and <code>src/utils/</code> to serve as a real-world testbed:
</p>
<ul>
  <li><code>src/utils/crypto.py</code>: Deterministic SHA-256 token hashing, salt derivation, and constant-time HMAC signatures.</li>
  <li><code>src/utils/validators.py</code>: Schema validation for RFC emails, international phone numbers, currency codes, and control-character sanitization.</li>
  <li><code>src/services/auth.py</code>: User onboarding, password digest validation, and tamper-proof session tokens.</li>
  <li><code>src/services/billing.py</code>: Progressive tiered discounts (&gt;$500: 15%, &gt;$200: 10%, &gt;$100: 5%), GST tax schedules, and currency conversion.</li>
  <li><code>src/services/inventory.py</code>: Stock reservations, transactional locks, commitments, and low-inventory warnings.</li>
  <li><code>src/services/order.py</code>: Multi-item checkout coordinator linking inventory reservations and billing invoices.</li>
  <li><code>src/services/notifications.py</code>: Transactional email and SMS delivery pipelines with audit event logs.</li>
</ul>

<h3>Step 3: Multi-Tier Automated Verification Suites (61 Pytest Cases)</h3>
<p>
Created comprehensive unit, integration, and system verification suites in <code>tests/</code>. The suites cover deterministic unit operations, multi-service transaction flows, and complete platform regression scenarios:
</p>
<div class="code-block">============================= test session starts ==============================
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

======================== 61 passed, 1 warning in 0.29s =========================</div>

<h3>Step 4: Abstract Syntax Tree (AST) Dependency Graph Engine (<code>src/dtsr/ast_graph.py</code>)</h3>
<p>
Implemented an AST parser that recursively inspects all Python files using <code>ast.parse</code>. It builds a directed NetworkX graph of import edges and extracts the transitive closure using <code>nx.descendants</code>. When <code>crypto.py</code> is modified, the graph reveals downstream consumer modules (<code>auth.py</code>) and their dependent test suites.
</p>

<h3>Step 5: Dynamic Test Impact Analysis Tracer (<code>src/dtsr/impact_tracer.py</code>)</h3>
<p>
Engineered a persistent coverage matrix stored at <code>.dtsr/coverage_matrix.json</code>. It maps each test suite to the set of source files exercised at runtime, while recording moving-average runtimes and historical failure frequencies.
</p>

<h3>Step 6: Predictive Risk Scorer & Fail-Fast Prioritizer (<code>src/dtsr/risk_scorer.py</code>)</h3>
<p>
Implements the risk prioritization function combining impact tier (Direct=1.0 vs Transitive=0.6), logarithmic churn factor \( \log(1 + \Delta L) \), historical failure rate, and execution speed bonus. High-risk, rapid unit tests are placed at the front of the queue.
</p>

<div class="page-break"></div>

<h3>Step 7: Greedy LPT Parallel CI Sharding Engine (<code>src/dtsr/sharder.py</code>)</h3>
<p>
Solves the multiprocessor scheduling problem using the Longest Processing Time (LPT) bin-packing heuristic. Sorts routed tests by historical execution duration and assigns each test to the runner bucket with the minimum accumulated duration.
</p>

<h3>Step 8: Unified CLI & Orchestrator (<code>src/dtsr/cli.py</code> & <code>src/dtsr/router.py</code>)</h3>
<p>
Packaged the engine into a unified Click CLI tool supporting commands: <code>route</code>, <code>run</code>, <code>map</code>, <code>ci-matrix</code>, and <code>benchmark</code>. Provides rich terminal tables, colorized risk scores, and GitHub Actions step outputs.
</p>

<h3>Step 9: Dynamic GitHub Actions Matrix CI Pipeline (<code>.github/workflows/test-subset-routing.yml</code>)</h3>
<p>
Engineered a dual-stage workflow: Job 1 inspects the pull request diff, computes the routed subset, and emits a JSON runner matrix. Job 2 fans out across parallel GitHub runner shards, executing only assigned tests.
</p>

<h3>Step 10: Nightly Full Regression Guardrail (<code>.github/workflows/nightly-full-suite.yml</code>)</h3>
<p>
Configured a scheduled 02:00 UTC safety net pipeline executing 100% of all tests with coverage auditing to guarantee no regression escapees persist indefinitely.
</p>

<!-- 4. Empirical Benchmarks -->
<h2>4. Empirical Benchmark Results & Verification</h2>
<p>
The routing engine was evaluated across 5 representative pull request archetypes:
</p>

<table>
  <tr>
    <th>PR ID</th>
    <th>Scenario Description</th>
    <th>Classified Tier</th>
    <th>Full Suites</th>
    <th>Routed Suites</th>
    <th>Duration (s)</th>
    <th>Time Saved %</th>
  </tr>
  <tr>
    <td><strong>PR-01</strong></td>
    <td>Documentation & README Polish</td>
    <td><span class="badge badge-green">DOCS_ONLY</span></td>
    <td>16</td>
    <td><strong>0</strong></td>
    <td>0.00 / 1.78s</td>
    <td><strong>100.0%</strong></td>
  </tr>
  <tr>
    <td><strong>PR-02</strong></td>
    <td>Validator Regex Boundary Hardening</td>
    <td><span class="badge badge-blue">CODE_CHANGE</span></td>
    <td>16</td>
    <td><strong>8</strong></td>
    <td>1.39 / 1.78s</td>
    <td><strong>21.9%</strong></td>
  </tr>
  <tr>
    <td><strong>PR-03</strong></td>
    <td>Tiered Volume Discount Logic Refactor</td>
    <td><span class="badge badge-blue">CODE_CHANGE</span></td>
    <td>16</td>
    <td><strong>4</strong></td>
    <td>1.01 / 1.78s</td>
    <td><strong>43.3%</strong></td>
  </tr>
  <tr>
    <td><strong>PR-04</strong></td>
    <td>HMAC Cryptography Security Patch</td>
    <td><span class="badge badge-purple">CODE_CHANGE</span></td>
    <td>16</td>
    <td><strong>4</strong></td>
    <td>0.89 / 1.78s</td>
    <td><strong>50.0%</strong></td>
  </tr>
  <tr>
    <td><strong>PR-05</strong></td>
    <td>Requirements Manifest Package Bump</td>
    <td><span class="badge badge-amber">INFRA_CONFIG</span></td>
    <td>16</td>
    <td><strong>16</strong></td>
    <td>1.78 / 1.78s</td>
    <td><strong>0.0%</strong> (Safety Fallback)</td>
  </tr>
  <tr style="background: #e2e8f0; font-weight: bold;">
    <td colspan="3">CUMULATIVE BENCHMARK TOTALS</td>
    <td>80</td>
    <td>32</td>
    <td>5.07 / 8.90s</td>
    <td>43.0% Overall Savings</td>
  </tr>
</table>

<div class="callout">
  <div class="callout-title">Key Benchmark Finding: Parallel Shard Duration Balance</div>
  For Scenario PR-03 (Billing refactor), the LPT sharder partitioned the 4 selected tests across 2 runners:
  <br>• <strong>Shard #1</strong>: 1 test (<code>test_end_to_end.py</code>) &rarr; Estimated: <strong>0.55s</strong>
  <br>• <strong>Shard #2</strong>: 3 tests (<code>test_checkout_flow.py</code>, <code>test_order.py</code>, <code>test_billing.py</code>) &rarr; Estimated: <strong>0.46s</strong>
  <br>The wall-clock makespan was capped at 0.55s with an imbalance ratio of only 1.09, demonstrating near-perfect load distribution.
</div>

<div class="page-break"></div>

<!-- 5. Short Answer Technical Questions & Answers -->
<h2>5. Short Answer Technical Questions & Theoretical Evaluations</h2>
<p>
The following technical evaluations substantiate the theoretical and practical mastery of the assignment topic:
</p>

<div class="qa-box">
  <div class="qa-question">1. What is Dynamic Test-Subset Routing, and what fundamental CI/CD bottleneck does it address?</div>
  <div class="qa-answer">
    Dynamic Test-Subset Routing is an intelligent CI optimization strategy that executes only the test suites impacted by an incoming code change instead of blindly running the entire regression test suite. It solves the scalability bottleneck of linear and quadratic growth in CI execution duration, reducing cloud runner queue times and developer feedback latency while conserving compute budgets.
  </div>
</div>

<div class="qa-box">
  <div class="qa-question">2. Differentiate between Static AST Transitive Dependency Analysis and Dynamic Test Impact Analysis (TIA).</div>
  <div class="qa-answer">
    Static AST analysis inspects source code import hierarchies prior to execution using abstract syntax trees ($G = (V, E)$), guaranteeing the detection of structural dependencies without needing prior execution data, but can over-approximate. Dynamic TIA traces code lines and functions executed during actual test runs, providing exact empirical coverage footprints but requiring historical runtime baselines. DTSR synthesizes both engines to eliminate regression escapes.
  </div>
</div>

<div class="qa-box">
  <div class="qa-question">3. Why is an automatic Full Regression Fallback critical when infrastructure or manifest files change?</div>
  <div class="qa-answer">
    Changes to package manifests (e.g. <code>requirements.txt</code>, lockfiles), Dockerfiles, or CI workflow YAML definitions do not modify domain source files directly, but alter the runtime environment and dependencies globally. If subset routing is applied blindly, zero tests would run, allowing breaking package upgrades to escape into production. DTSR classifies these as <code>INFRA_CONFIG</code> and forces a 100% full regression suite.
  </div>
</div>

<div class="qa-box">
  <div class="qa-question">4. How does the Greedy Longest Processing Time (LPT) bin-packing heuristic minimize parallel CI makespan?</div>
  <div class="qa-answer">
    When tests are partitioned across $K$ runners using naive round-robin sharding, uneven test durations cause one runner to take significantly longer than others, leaving workers idle. Greedy LPT sorts tests descending by historical execution time and assigns each test to the runner bucket currently having the smallest accumulated duration. This bounds the parallel makespan to within $\frac{4}{3} - \frac{1}{3K}$ of theoretical optimum.
  </div>
</div>

<div class="qa-box">
  <div class="qa-question">5. What is Fail-Fast Prioritization, and how does DTSR achieve it?</div>
  <div class="qa-answer">
    Fail-Fast is the principle that if a commit contains a defect, the CI pipeline should detect and report that failure within the first 15–30 seconds rather than after minutes of execution. DTSR achieves this through its composite Risk Scorer ($\text{Risk}(T) = w_1 I + w_2 \log(1+\Delta L) + w_3 F_{hist} + w_4 S_{bonus}$), which prioritizes direct-impact tests with high line churn and fast execution durations at the head of the test runner queue.
  </div>
</div>

<!-- 6. Key Learnings & Engineering Takeaways -->
<h2>6. Key Learnings & Engineering Takeaways</h2>
<p>
Through the end-to-end implementation and benchmarking of Dynamic Test-Subset Routing, several deep engineering insights were gained:
</p>
<ol>
  <li><strong>Static Analysis vs Dynamic Coverage Complementarity</strong>: Static AST dependency graphs are instant to compute and analyze code before execution. Dynamic TIA coverage matrices provide exact call-graph mappings. Combining both techniques ensures zero regression escapes while pruning irrelevant suites.</li>
  <li><strong>The Necessity of Defensive Guardrails</strong>: Blindly selecting tests based only on file names can lead to critical escapes when build manifests change. Explicitly classifying <code>INFRA_CONFIG</code> changes and triggering an automated full-suite fallback provides essential enterprise safety.</li>
  <li><strong>Fail-Fast Value Over Pure Execution Reduction</strong>: Ordering tests by risk score rather than execution order ensures that if a regression exists, it is caught in the first 15-30 seconds of CI execution.</li>
  <li><strong>Sharding Efficiency with LPT</strong>: Naive round-robin sharding causes high idle times when tests have skewed runtimes. Applying the LPT bin-packing algorithm reduces the parallel makespan to within 10% of theoretical optimum.</li>
  <li><strong>Direct Alignment with Big-Tech CI Architectures</strong>: The DTSR architecture directly mirrors techniques used in production at Google (TAP / Test Automation Platform), Meta (Predictive Test Selection), and Spotify (Test Impact Analysis).</li>
</ol>

<div class="page-break"></div>

<!-- 7. GitHub Setup & Verification Commands -->
<h2>7. GitHub Repository Submission & Verification Commands</h2>
<p>
The repository is fully provisioned with Git history and configured with the candidate's exact remote repository URL:
</p>

<div class="submission-card">
  <div style="font-weight: bold; color: #1e40af; font-size: 9pt; margin-bottom: 3px;">
    🔗 Official GitHub Repository Submission Link (Click to Open in Browser):
  </div>
  <a href="https://github.com/sakshamsingh819/Dynamic-Test-Subset-Routing-Saksham-Singh-24BTRAO035-Course-Cloud-DevOps-DRIVE-DEVOPS-Assignment-4" target="_blank">
    https://github.com/sakshamsingh819/Dynamic-Test-Subset-Routing-Saksham-Singh-24BTRAO035-Course-Cloud-DevOps-DRIVE-DEVOPS-Assignment-4
  </a>
  <div style="margin-top: 6px;">
    <a class="btn-open-repo" href="https://github.com/sakshamsingh819/Dynamic-Test-Subset-Routing-Saksham-Singh-24BTRAO035-Course-Cloud-DevOps-DRIVE-DEVOPS-Assignment-4" target="_blank">
      🌐 DIRECT LAUNCH REPOSITORY IN BROWSER &rarr;
    </a>
  </div>
</div>

<div class="code-block"># Repository Location and Status Check
cd "/home/saksham/Pictures/A4 A3"

# Cloned and Linked Remote Target (Saksham Singh - AI DRIVEN DEVOPS)
git remote add origin https://github.com/sakshamsingh819/Dynamic-Test-Subset-Routing-Saksham-Singh-24BTRAO035-Course-Cloud-DevOps-DRIVE-DEVOPS-Assignment-4.git

# Push Complete Foundation to GitHub
git branch -M main
git push -u origin main</div>

<table>
  <tr>
    <th style="width: 30%;">Evaluation Criterion</th>
    <th style="width: 35%;">Implementation Evidence</th>
    <th style="width: 35%;">Academic Verification Status</th>
  </tr>
  <tr>
    <td><strong>Dynamic Test-Subset Routing</strong></td>
    <td>Dual-Engine AST Closure + Dynamic Coverage Matrix</td>
    <td><span class="badge badge-green">Verified & Tested (100% Pass)</span></td>
  </tr>
  <tr>
    <td><strong>GitHub Actions CI Automation</strong></td>
    <td>Dynamic Matrix Strategy + LPT Sharding Workflow</td>
    <td><span class="badge badge-green">Configured & Validated</span></td>
  </tr>
  <tr>
    <td><strong>Empirical Benchmarks</strong></td>
    <td>5 Pull Request Archetypes with 43.0% Savings</td>
    <td><span class="badge badge-blue">Documented & Persisted</span></td>
  </tr>
  <tr>
    <td><strong>Document of Learnings</strong></td>
    <td>Full 6-Page PDF Dossier + Markdown Guide</td>
    <td><span class="badge badge-purple">Complete with Q&A Section</span></td>
  </tr>
</table>

<hr style="border: none; border-top: 1.5px solid #cbd5e1; margin-top: 20px;">
<div style="font-size: 8pt; color: #64748b; text-align: center;">
  <strong>Jain (Deemed-to-be University)</strong> • Faculty of Engineering and Technology • Department of Computer Science & Engineering<br>
  Candidate: <strong>Saksham Singh</strong> (USN: <strong>24BTRAO035</strong>) • Branch: <strong>AI DRIVEN DEVOPS</strong> • October 2026
</div>

</body>
</html>
"""


def generate_pdf():
    output_dir = Path(__file__).resolve().parent.parent
    pdf_path = output_dir / "Dynamic_Test_Subset_Routing_Learnings_Report.pdf"
    print(f"Generating PDF report: {pdf_path}...")
    doc = weasyprint.HTML(string=HTML_TEMPLATE)
    doc.write_pdf(str(pdf_path))
    print(f"✓ PDF successfully generated! File size: {pdf_path.stat().st_size} bytes")
    return pdf_path


if __name__ == "__main__":
    generate_pdf()
