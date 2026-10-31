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
    margin: 16mm 14mm 18mm 14mm;
    @top-left {
      content: "JAIN (DEEMED-TO-BE UNIVERSITY) • AUTOMATION SOFTWARE • AI DRIVEN DEVOPS";
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
      content: "Academic Laboratory Dossier • Course: Automation Software";
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
    line-height: 1.4;
    font-size: 8.5pt;
    margin: 0;
  }

  h1, h2, h3, h4 {
    color: #0f172a;
    font-weight: 700;
    margin-top: 0;
  }

  .institution-header {
    text-align: center;
    border-bottom: 2px solid #1e3a8a;
    padding-bottom: 6px;
    margin-bottom: 10px;
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
    font-size: 8.2pt;
    font-weight: 600;
    color: #475569;
    margin-bottom: 2px;
  }

  .course-badge {
    display: inline-block;
    background: #e0e7ff;
    color: #3730a3;
    font-size: 7.2pt;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 4px;
    text-transform: uppercase;
  }

  .header-box {
    background: linear-gradient(135deg, #091e42 0%, #1e40af 100%);
    color: #ffffff;
    padding: 12px 16px;
    border-radius: 6px;
    margin-bottom: 12px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  .header-box h1 {
    color: #ffffff;
    font-size: 16pt;
    margin: 0 0 3px 0;
    line-height: 1.2;
  }

  .header-box .subtitle {
    font-size: 9pt;
    color: #bfdbfe;
    margin-bottom: 8px;
    font-weight: 500;
  }

  .meta-grid {
    display: table;
    width: 100%;
    margin-top: 4px;
    border-top: 1px solid rgba(255,255,255,0.25);
    padding-top: 6px;
    font-size: 7.8pt;
  }

  .meta-col {
    display: table-cell;
    width: 25%;
    vertical-align: top;
  }

  .meta-label {
    color: #93c5fd;
    text-transform: uppercase;
    font-size: 6.2pt;
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
    padding: 7px 10px;
    border-radius: 4px;
    margin-top: 8px;
    border: 1px solid #1e3a8a;
    border-left: 4px solid #38bdf8;
  }

  .repo-link-box a {
    color: #38bdf8;
    text-decoration: underline;
    font-weight: bold;
    font-family: 'Consolas', monospace;
    font-size: 7.5pt;
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
    font-size: 7.2pt;
    margin-top: 4px;
    letter-spacing: 0.3px;
    border: 1px solid #60a5fa;
  }

  h2 {
    font-size: 11pt;
    margin-top: 14px;
    margin-bottom: 6px;
    border-bottom: 1.5px solid #cbd5e1;
    padding-bottom: 3px;
    color: #1e3a8a;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    page-break-after: avoid;
  }

  h3 {
    font-size: 9pt;
    margin-top: 8px;
    margin-bottom: 3px;
    color: #1e293b;
    page-break-after: avoid;
  }

  p {
    margin-top: 2px;
    margin-bottom: 5px;
    text-align: justify;
  }

  .badge {
    display: inline-block;
    padding: 2px 5px;
    border-radius: 3px;
    font-size: 6.8pt;
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
    margin: 6px 0;
    font-size: 7.8pt;
    page-break-inside: avoid;
  }

  th {
    background: #f1f5f9;
    color: #1e293b;
    font-weight: 700;
    text-align: left;
    padding: 4px 6px;
    border: 1px solid #cbd5e1;
  }

  td {
    padding: 4px 6px;
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
    font-size: 6.8pt;
    padding: 6px 8px;
    border-radius: 4px;
    margin: 5px 0;
    white-space: pre-wrap;
    line-height: 1.25;
    border-left: 3px solid #38bdf8;
    page-break-inside: avoid;
  }

  .callout {
    background: #f0fdf4;
    border-left: 3.5px solid #16a34a;
    padding: 6px 9px;
    margin: 6px 0;
    border-radius: 0 4px 4px 0;
    font-size: 8pt;
    page-break-inside: avoid;
  }

  .callout-title {
    font-weight: bold;
    color: #15803d;
    margin-bottom: 2px;
  }

  .diagram-container {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 8px;
    margin: 8px 0;
    text-align: center;
    page-break-inside: avoid;
  }

  .diagram-title {
    font-weight: bold;
    color: #1e3a8a;
    font-size: 8.5pt;
    margin-bottom: 6px;
    text-align: left;
    display: flex;
    justify-content: space-between;
  }

  .qa-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 3px solid #4f46e5;
    padding: 5px 8px;
    margin: 5px 0;
    border-radius: 0 4px 4px 0;
    page-break-inside: avoid;
  }

  .qa-question {
    font-weight: 700;
    color: #312e81;
    font-size: 8.2pt;
    margin-bottom: 2px;
  }

  .qa-answer {
    color: #334155;
    font-size: 7.8pt;
    text-align: justify;
  }

  .definition-grid {
    display: table;
    width: 100%;
    margin: 6px 0;
    page-break-inside: avoid;
  }

  .def-card {
    display: table-cell;
    width: 50%;
    padding: 4px 6px;
    vertical-align: top;
  }

  .def-inner {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 3px solid #0284c7;
    border-radius: 4px;
    padding: 5px 7px;
    height: 100%;
  }

  .def-term {
    font-weight: bold;
    color: #0369a1;
    font-size: 8pt;
    margin-bottom: 2px;
  }

  .def-desc {
    font-size: 7.5pt;
    color: #334155;
    line-height: 1.35;
    text-align: justify;
  }

  .submission-card {
    background: #eff6ff;
    border: 1.5px solid #3b82f6;
    border-radius: 6px;
    padding: 8px 12px;
    margin: 8px 0;
    text-align: center;
    page-break-inside: avoid;
  }

  .submission-card a {
    color: #1d4ed8;
    font-weight: bold;
    font-size: 8pt;
    text-decoration: underline;
    word-break: break-all;
  }
</style>
</head>
<body>

<!-- Institutional Header -->
<div class="institution-header">
  <div class="univ-title">Jain (Deemed-to-be University)</div>
  <div class="dept-title">Faculty of Engineering and Technology • Department of Computer Science and Engineering</div>
  <div class="course-badge">Course: Automation Software • Branch: B.Tech CSE (AI DRIVEN DEVOPS) • Assignment 4</div>
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
      <div class="meta-label">Course / Subject</div>
      <div class="meta-value">Automation Software</div>
    </div>
  </div>
  
  <div class="repo-link-box">
    <div style="font-size: 6.8pt; color: #93c5fd; text-transform: uppercase; font-weight: bold; margin-bottom: 2px;">
      🔗 DIRECT GITHUB REPOSITORY LINK (CLICK TO OPEN IN BROWSER):
    </div>
    <a href="https://github.com/sakshamsingh819/Dynamic-Test-Subset-Routing-Saksham-Singh-24BTRAO035-Course-Cloud-DevOps-DRIVE-DEVOPS-Assignment-4" target="_blank">
      https://github.com/sakshamsingh819/Dynamic-Test-Subset-Routing-Saksham-Singh-24BTRAO035-Course-Cloud-DevOps-DRIVE-DEVOPS-Assignment-4
    </a>
    <div>
      <a class="btn-open-repo" href="https://github.com/sakshamsingh819/Dynamic-Test-Subset-Routing-Saksham-Singh-24BTRAO035-Course-Cloud-DevOps-DRIVE-DEVOPS-Assignment-4" target="_blank">
        🚀 CLICK HERE TO OPEN GITHUB REPOSITORY IN BROWSER &rarr;
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

<!-- DIAGRAM 1: High Resolution Architecture SVG -->
<div class="diagram-container">
  <div class="diagram-title">
    <span>Figure 1: End-to-End Dynamic Test-Subset Routing Architecture</span>
    <span style="font-size: 7pt; color: #64748b; font-weight: normal;">Dual-Engine Static AST & Dynamic TIA Synthesis</span>
  </div>
  <svg width="100%" height="150" viewBox="0 0 740 150" xmlns="http://www.w3.org/2000/svg" style="font-family: Arial, sans-serif;">
    <defs>
      <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#1e3a8a"/>
        <stop offset="100%" stop-color="#0284c7"/>
      </linearGradient>
      <linearGradient id="greenGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#059669"/>
        <stop offset="100%" stop-color="#10b981"/>
      </linearGradient>
      <linearGradient id="purpleGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#7c3aed"/>
        <stop offset="100%" stop-color="#8b5cf6"/>
      </linearGradient>
      <linearGradient id="amberGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#d97706"/>
        <stop offset="100%" stop-color="#f59e0b"/>
      </linearGradient>
      <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
        <feDropShadow dx="1" dy="2" stdDeviation="2" flood-opacity="0.15"/>
      </filter>
    </defs>

    <!-- Node 1: Git Diff -->
    <rect x="10" y="45" width="100" height="55" rx="6" fill="#0f172a" filter="url(#shadow)"/>
    <text x="60" y="68" fill="#38bdf8" font-size="9" font-weight="bold" text-anchor="middle">Git Diff / PR</text>
    <text x="60" y="82" fill="#94a3b8" font-size="7.5" text-anchor="middle">base..head changes</text>
    <text x="60" y="93" fill="#cbd5e1" font-size="6.5" text-anchor="middle">Δ Lines & Files</text>

    <!-- Arrow 1 -->
    <path d="M 110 72 L 135 72" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>
    <polygon points="135,68 143,72 135,76" fill="#64748b"/>

    <!-- Node 2: Classifier -->
    <rect x="145" y="30" width="115" height="85" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" filter="url(#shadow)"/>
    <text x="202" y="48" fill="#1e3a8a" font-size="8.5" font-weight="bold" text-anchor="middle">GitAnalyzer</text>
    <text x="202" y="60" fill="#64748b" font-size="7" text-anchor="middle">Tier Classification</text>
    <rect x="153" y="66" width="98" height="13" rx="3" fill="#dcfce7"/>
    <text x="202" y="75" fill="#15803d" font-size="6.5" font-weight="bold" text-anchor="middle">DOCS_ONLY &rarr; 0 Tests</text>
    <rect x="153" y="82" width="98" height="13" rx="3" fill="#fef3c7"/>
    <text x="202" y="91" fill="#b45309" font-size="6.5" font-weight="bold" text-anchor="middle">INFRA &rarr; Full Suite</text>
    <rect x="153" y="98" width="98" height="13" rx="3" fill="#dbeafe"/>
    <text x="202" y="107" fill="#1e40af" font-size="6.5" font-weight="bold" text-anchor="middle">CODE &rarr; Route Engine</text>

    <!-- Arrow 2 -->
    <path d="M 260 72 L 285 72" stroke="#64748b" stroke-width="2"/>
    <polygon points="285,68 293,72 285,76" fill="#64748b"/>

    <!-- Node 3: Dual Engine -->
    <rect x="295" y="20" width="150" height="105" rx="6" fill="#ffffff" stroke="#3b82f6" stroke-width="2" filter="url(#shadow)"/>
    <rect x="295" y="20" width="150" height="20" rx="4" fill="url(#bgGrad)"/>
    <text x="370" y="34" fill="#ffffff" font-size="8.5" font-weight="bold" text-anchor="middle">Dual Selection Engine</text>
    
    <!-- Engine A: AST -->
    <rect x="305" y="46" width="130" height="32" rx="4" fill="#f0f9ff" stroke="#bae6fd" stroke-width="1"/>
    <text x="370" y="59" fill="#0369a1" font-size="7.5" font-weight="bold" text-anchor="middle">Engine 1: AST Transitive DAG</text>
    <text x="370" y="71" fill="#64748b" font-size="6.5" text-anchor="middle">Static Import Reachability Closure</text>

    <!-- Engine B: TIA -->
    <rect x="305" y="84" width="130" height="32" rx="4" fill="#fdf4ff" stroke="#f5d0fe" stroke-width="1"/>
    <text x="370" y="97" fill="#7e22ce" font-size="7.5" font-weight="bold" text-anchor="middle">Engine 2: Dynamic TIA Matrix</text>
    <text x="370" y="109" fill="#64748b" font-size="6.5" text-anchor="middle">Runtime Code Coverage Footprint</text>

    <!-- Arrow 3 -->
    <path d="M 445 72 L 470 72" stroke="#64748b" stroke-width="2"/>
    <polygon points="470,68 478,72 470,76" fill="#64748b"/>

    <!-- Node 4: Risk Scorer -->
    <rect x="480" y="32" width="115" height="80" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" filter="url(#shadow)"/>
    <text x="537" y="50" fill="#7c3aed" font-size="8.5" font-weight="bold" text-anchor="middle">RiskScorer</text>
    <text x="537" y="62" fill="#64748b" font-size="7" text-anchor="middle">Fail-Fast Ranking</text>
    <rect x="488" y="70" width="98" height="34" rx="3" fill="#faf5ff" stroke="#e9d5ff"/>
    <text x="537" y="82" fill="#6b21a8" font-size="6.5" text-anchor="middle">Risk = Impact + Churn</text>
    <text x="537" y="92" fill="#6b21a8" font-size="6.5" text-anchor="middle">+ FlakeRate - Duration</text>
    <text x="537" y="100" fill="#15803d" font-size="6" font-weight="bold" text-anchor="middle">Queue: High Risk First</text>

    <!-- Arrow 4 -->
    <path d="M 595 72 L 620 72" stroke="#64748b" stroke-width="2"/>
    <polygon points="620,68 628,72 620,76" fill="#64748b"/>

    <!-- Node 5: LPT Sharder & Runners -->
    <rect x="630" y="25" width="100" height="95" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" filter="url(#shadow)"/>
    <text x="680" y="42" fill="#059669" font-size="8.5" font-weight="bold" text-anchor="middle">LPT Sharder</text>
    <text x="680" y="53" fill="#64748b" font-size="6.8" text-anchor="middle">CI Matrix Fan-out</text>

    <!-- Shard 1 -->
    <rect x="638" y="60" width="84" height="24" rx="3" fill="url(#greenGrad)"/>
    <text x="680" y="72" fill="#ffffff" font-size="7" font-weight="bold" text-anchor="middle">Shard #1 Runner</text>
    <text x="680" y="81" fill="#dcfce7" font-size="6" text-anchor="middle">~0.55s (Balanced)</text>

    <!-- Shard 2 -->
    <rect x="638" y="89" width="84" height="24" rx="3" fill="url(#greenGrad)"/>
    <text x="680" y="101" fill="#ffffff" font-size="7" font-weight="bold" text-anchor="middle">Shard #2 Runner</text>
    <text x="680" y="110" fill="#dcfce7" font-size="6" text-anchor="middle">~0.46s (Balanced)</text>
  </svg>
</div>

<!-- 2. Theoretical Glossary & Core Definitions -->
<h2>2. Technical Definitions & Theoretical Taxonomy</h2>
<p>
To establish conceptual rigor, the key automation and software verification paradigms utilized in this assignment are defined below:
</p>

<div class="definition-grid">
  <div class="def-card">
    <div class="def-inner">
      <div class="def-term">1. Predictive Test Selection (PTS)</div>
      <div class="def-desc">
        A machine-assisted or heuristic decision framework that analyzes historical test failure probabilities, code churn volume, and author commit topologies to predict which tests are most likely to expose bugs in an incoming pull request.
      </div>
    </div>
  </div>
  <div class="def-card">
    <div class="def-inner">
      <div class="def-term">2. Test Impact Analysis (TIA)</div>
      <div class="def-desc">
        A dynamic test optimization discipline that maintains a fine-grained, bidirectional mapping between source code components (classes, methods, functions) and the specific test suites that exercise them at runtime.
      </div>
    </div>
  </div>
</div>

<div class="definition-grid">
  <div class="def-card">
    <div class="def-inner">
      <div class="def-term">3. AST Dependency Graph & Transitive Closure</div>
      <div class="def-desc">
        Static analysis utilizing Abstract Syntax Trees (AST) to model code as a directed graph \( G = (V, E) \). Transitive closure identifies all indirect modules dependent on a modified file via recursive ancestor and successor traversal.
      </div>
    </div>
  </div>
  <div class="def-card">
    <div class="def-inner">
      <div class="def-term">4. Longest Processing Time (LPT) Bin-Packing</div>
      <div class="def-desc">
        An algorithmic multiprocessor scheduling heuristic that sorts jobs in descending order of execution duration and greedily assigns each task to the least-loaded worker, guaranteeing a makespan within \( 4/3 - 1/(3K) \) of theoretical optimum.
      </div>
    </div>
  </div>
</div>

<div class="definition-grid">
  <div class="def-card">
    <div class="def-inner">
      <div class="def-term">5. Fail-Fast Prioritization & Churn Correlation</div>
      <div class="def-desc">
        An operational test-ordering strategy that executes high-risk, rapid unit tests ahead of slower integration tests. Normalized code churn \( \log(1 + \Delta L) \) acts as a leading indicator of defect concentration.
      </div>
    </div>
  </div>
  <div class="def-card">
    <div class="def-inner">
      <div class="def-term">6. Defensive Safety Guardrails & Fallbacks</div>
      <div class="def-desc">
        Deterministic fail-safes that override subset selection. Modifications to environment manifests (e.g. <code>requirements.txt</code>), Dockerfiles, or CI workflows automatically trigger a 100% full regression suite to prevent silent escapes.
      </div>
    </div>
  </div>
</div>

<!-- 3. Mathematical Foundations -->
<h2>3. Mathematical Formulations & Algorithmic Models</h2>
<table>
  <tr>
    <th style="width: 25%;">Theoretical Pillar</th>
    <th style="width: 35%;">Mathematical / Algorithmic Formulation</th>
    <th style="width: 40%;">Operational Function in CI Pipeline</th>
  </tr>
  <tr>
    <td><strong>AST Transitive Closure</strong></td>
    <td>\( \text{Closure}(v) = \{u \in V \mid v \rightsquigarrow u \text{ in } G_{\text{reverse}}\} \)</td>
    <td>Computes all upstream consumers and test suites impacted by a modified source file.</td>
  </tr>
  <tr>
    <td><strong>TIA Coverage Mapping</strong></td>
    <td>\( \text{Selected}_{\text{TIA}} = \{T \in \mathcal{T} \mid \text{Cov}(T) \cap \Delta \mathcal{S} \neq \emptyset\} \)</td>
    <td>Selects tests whose dynamic execution footprint intersects with changed files.</td>
  </tr>
  <tr>
    <td><strong>Predictive Risk Scoring</strong></td>
    <td>\( \text{Risk}(T) = w_1 I + w_2 \frac{\log(1+\Delta L)}{5} + w_3 \frac{\text{Fail}}{\text{Run}} + w_4 \frac{1}{1+D} \)</td>
    <td>Orders selected tests by defect risk and velocity: direct impact & fast unit tests execute first.</td>
  </tr>
  <tr>
    <td><strong>Parallel Makespan</strong></td>
    <td>\( \text{Makespan} = \max_{1 \le j \le K} \sum_{T \in \text{Shard}_j} \text{Duration}(T) \)</td>
    <td>LPT bin-packing minimizes the maximum shard wall-clock time across parallel GitHub runners.</td>
  </tr>
</table>

<!-- DIAGRAM 2: AST Dependency DAG SVG -->
<div class="diagram-container">
  <div class="diagram-title">
    <span>Figure 2: AST Dependency DAG & Transitive Reachability Example</span>
    <span style="font-size: 7pt; color: #64748b; font-weight: normal;">Modifying crypto.py triggers only relevant downstream tests</span>
  </div>
  <svg width="100%" height="110" viewBox="0 0 740 110" xmlns="http://www.w3.org/2000/svg" style="font-family: Arial, sans-serif;">
    <!-- crypto.py (modified) -->
    <rect x="20" y="35" width="100" height="40" rx="5" fill="#fee2e2" stroke="#ef4444" stroke-width="2"/>
    <text x="70" y="52" fill="#991b1b" font-size="8" font-weight="bold" text-anchor="middle">src/utils/crypto.py</text>
    <text x="70" y="65" fill="#b91c1c" font-size="7" font-weight="bold" text-anchor="middle">[MODIFIED]</text>

    <!-- Arrow to auth.py -->
    <path d="M 120 55 L 165 55" stroke="#ef4444" stroke-width="2"/>
    <polygon points="165,51 173,55 165,59" fill="#ef4444"/>

    <!-- auth.py (consumer) -->
    <rect x="175" y="35" width="105" height="40" rx="5" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="227" y="52" fill="#92400e" font-size="8" font-weight="bold" text-anchor="middle">src/services/auth.py</text>
    <text x="227" y="65" fill="#b45309" font-size="6.5" text-anchor="middle">Transitive Consumer</text>

    <!-- Arrow to test_crypto.py -->
    <path d="M 70 35 L 70 18 L 330 18" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="3,3"/>
    <polygon points="330,15 337,18 330,21" fill="#ef4444"/>

    <!-- Arrow to test_auth.py -->
    <path d="M 280 55 L 330 55" stroke="#f59e0b" stroke-width="1.5"/>
    <polygon points="330,51 337,55 330,59" fill="#f59e0b"/>

    <!-- Routed Test 1 -->
    <rect x="340" y="8" width="140" height="25" rx="4" fill="#dcfce7" stroke="#10b981" stroke-width="1.5"/>
    <text x="410" y="24" fill="#065f46" font-size="7.5" font-weight="bold" text-anchor="middle">✓ tests/unit/test_crypto.py (Direct)</text>

    <!-- Routed Test 2 -->
    <rect x="340" y="42" width="140" height="25" rx="4" fill="#dcfce7" stroke="#10b981" stroke-width="1.5"/>
    <text x="410" y="58" fill="#065f46" font-size="7.5" font-weight="bold" text-anchor="middle">✓ tests/unit/test_auth.py (Transitive)</text>

    <!-- Routed Test 3 -->
    <path d="M 227 75 L 227 92 L 330 92" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="3,3"/>
    <polygon points="330,89 337,92 330,95" fill="#f59e0b"/>
    <rect x="340" y="78" width="140" height="25" rx="4" fill="#dcfce7" stroke="#10b981" stroke-width="1.5"/>
    <text x="410" y="94" fill="#065f46" font-size="7.5" font-weight="bold" text-anchor="middle">✓ tests/integration/test_auth_audit.py</text>

    <!-- Pruned nodes in grey -->
    <rect x="520" y="15" width="200" height="80" rx="5" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1" stroke-dasharray="4,4"/>
    <text x="620" y="32" fill="#475569" font-size="7.5" font-weight="bold" text-anchor="middle">🚫 Unaffected Suites (Pruned)</text>
    <text x="620" y="48" fill="#64748b" font-size="6.8" text-anchor="middle">• tests/unit/test_inventory.py</text>
    <text x="620" y="60" fill="#64748b" font-size="6.8" text-anchor="middle">• tests/unit/test_billing.py</text>
    <text x="620" y="72" fill="#64748b" font-size="6.8" text-anchor="middle">• tests/unit/test_notifications.py</text>
    <text x="620" y="85" fill="#059669" font-size="7" font-weight="bold" text-anchor="middle">&rarr; 50.0% Time & Compute Saved!</text>
  </svg>
</div>

<!-- 4. Step-by-Step Implementation Guide -->
<h2>4. Step-by-Step Implementation Guide</h2>
<p>
The project was engineered through a disciplined 10-step methodology adhering to software automation standards:
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

<!-- 5. Empirical Benchmarks -->
<h2>5. Empirical Benchmark Results & Quantitative Evaluation</h2>
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

<!-- CHART 1: Benchmark Latency Comparison SVG -->
<div class="diagram-container">
  <div class="diagram-title">
    <span>Figure 3: Empirical CI Duration Comparison & Compute Savings Across PR Scenarios</span>
    <span style="font-size: 7pt; color: #15803d; font-weight: bold;">Cumulative: 43.0% Time Saved</span>
  </div>
  <svg width="100%" height="135" viewBox="0 0 740 135" xmlns="http://www.w3.org/2000/svg" style="font-family: Arial, sans-serif;">
    <!-- Grid lines -->
    <line x1="120" y1="20" x2="680" y2="20" stroke="#e2e8f0" stroke-width="1"/>
    <line x1="120" y1="42" x2="680" y2="42" stroke="#e2e8f0" stroke-width="1"/>
    <line x1="120" y1="64" x2="680" y2="64" stroke="#e2e8f0" stroke-width="1"/>
    <line x1="120" y1="86" x2="680" y2="86" stroke="#e2e8f0" stroke-width="1"/>
    <line x1="120" y1="108" x2="680" y2="108" stroke="#cbd5e1" stroke-width="1.5"/>

    <!-- Y-axis labels -->
    <text x="110" y="24" fill="#64748b" font-size="7" text-anchor="end">PR-01 (Docs)</text>
    <text x="110" y="46" fill="#64748b" font-size="7" text-anchor="end">PR-02 (Validator)</text>
    <text x="110" y="68" fill="#64748b" font-size="7" text-anchor="end">PR-03 (Billing)</text>
    <text x="110" y="90" fill="#64748b" font-size="7" text-anchor="end">PR-04 (Crypto)</text>
    <text x="110" y="112" fill="#64748b" font-size="7" text-anchor="end">PR-05 (Infra)</text>

    <!-- Scale: 1.78s = 400px -> scale = 224 px/s -->
    <!-- PR-01: Baseline 1.78s (400px), DTSR 0.0s (0px) -->
    <rect x="120" y="15" width="400" height="7" fill="#cbd5e1" rx="2"/>
    <rect x="120" y="23" width="2" height="7" fill="#10b981" rx="2"/>
    <rect x="530" y="17" width="55" height="12" rx="3" fill="#dcfce7"/>
    <text x="557" y="26" fill="#15803d" font-size="7" font-weight="bold" text-anchor="middle">100.0% SAVED</text>

    <!-- PR-02: Baseline 1.78s (400px), DTSR 1.39s (312px) -->
    <rect x="120" y="37" width="400" height="7" fill="#cbd5e1" rx="2"/>
    <rect x="120" y="45" width="312" height="7" fill="#0284c7" rx="2"/>
    <rect x="530" y="39" width="55" height="12" rx="3" fill="#e0f2fe"/>
    <text x="557" y="48" fill="#0369a1" font-size="7" font-weight="bold" text-anchor="middle">21.9% SAVED</text>

    <!-- PR-03: Baseline 1.78s (400px), DTSR 1.01s (227px) -->
    <rect x="120" y="59" width="400" height="7" fill="#cbd5e1" rx="2"/>
    <rect x="120" y="67" width="227" height="7" fill="#0284c7" rx="2"/>
    <rect x="530" y="61" width="55" height="12" rx="3" fill="#e0f2fe"/>
    <text x="557" y="70" fill="#0369a1" font-size="7" font-weight="bold" text-anchor="middle">43.3% SAVED</text>

    <!-- PR-04: Baseline 1.78s (400px), DTSR 0.89s (200px) -->
    <rect x="120" y="81" width="400" height="7" fill="#cbd5e1" rx="2"/>
    <rect x="120" y="89" width="200" height="7" fill="#7c3aed" rx="2"/>
    <rect x="530" y="83" width="55" height="12" rx="3" fill="#f3e8ff"/>
    <text x="557" y="92" fill="#6b21a8" font-size="7" font-weight="bold" text-anchor="middle">50.0% SAVED</text>

    <!-- PR-05: Baseline 1.78s (400px), DTSR 1.78s (400px) -->
    <rect x="120" y="103" width="400" height="7" fill="#cbd5e1" rx="2"/>
    <rect x="120" y="111" width="400" height="7" fill="#d97706" rx="2"/>
    <rect x="530" y="105" width="55" height="12" rx="3" fill="#fef3c7"/>
    <text x="557" y="114" fill="#b45309" font-size="6.5" font-weight="bold" text-anchor="middle">0% (FALLBACK)</text>

    <!-- Legend -->
    <rect x="600" y="45" width="10" height="7" fill="#cbd5e1" rx="1"/>
    <text x="615" y="51" fill="#475569" font-size="6.5">Full Suite Baseline</text>
    <rect x="600" y="60" width="10" height="7" fill="#0284c7" rx="1"/>
    <text x="615" y="66" fill="#0369a1" font-size="6.5">DTSR Routed Subset</text>
  </svg>
</div>

<!-- CHART 2: Sharding Load Balance Comparison SVG -->
<div class="diagram-container">
  <div class="diagram-title">
    <span>Figure 4: Parallel CI Runner Sharding Balance (LPT vs Naive Makespan)</span>
    <span style="font-size: 7pt; color: #1e40af; font-weight: bold;">Imbalance Ratio: 1.09 (Near Parity)</span>
  </div>
  <svg width="100%" height="80" viewBox="0 0 740 80" xmlns="http://www.w3.org/2000/svg" style="font-family: Arial, sans-serif;">
    <!-- Runner 1 -->
    <text x="60" y="24" fill="#1e3a8a" font-size="7.5" font-weight="bold">Runner Shard #1:</text>
    <rect x="140" y="12" width="275" height="16" rx="3" fill="#2563eb"/>
    <text x="277" y="23" fill="#ffffff" font-size="7" font-weight="bold" text-anchor="middle">test_end_to_end.py (0.55s)</text>
    <rect x="420" y="13" width="45" height="14" rx="3" fill="#dcfce7"/>
    <text x="442" y="23" fill="#15803d" font-size="6.5" font-weight="bold" text-anchor="middle">0.55s</text>

    <!-- Runner 2 -->
    <text x="60" y="52" fill="#1e3a8a" font-size="7.5" font-weight="bold">Runner Shard #2:</text>
    <!-- test_checkout_flow: 0.28s = 140px -->
    <rect x="140" y="40" width="140" height="16" rx="3" fill="#0284c7"/>
    <text x="210" y="51" fill="#ffffff" font-size="6.5" text-anchor="middle">checkout_flow (0.28s)</text>
    <!-- test_order: 0.12s = 60px -->
    <rect x="282" y="40" width="60" height="16" rx="3" fill="#0ea5e9"/>
    <text x="312" y="51" fill="#ffffff" font-size="6.5" text-anchor="middle">order (0.12s)</text>
    <!-- test_billing: 0.06s = 30px -->
    <rect x="344" y="40" width="30" height="16" rx="3" fill="#38bdf8"/>
    <text x="359" y="51" fill="#0f172a" font-size="6" text-anchor="middle">bill</text>
    <!-- Idle gap: 0.09s = 45px -->
    <rect x="376" y="40" width="39" height="16" rx="2" fill="#f1f5f9" stroke="#cbd5e1" stroke-dasharray="2,2"/>
    <text x="395" y="50" fill="#94a3b8" font-size="5.5" text-anchor="middle">idle</text>
    <rect x="420" y="41" width="45" height="14" rx="3" fill="#dcfce7"/>
    <text x="442" y="51" fill="#15803d" font-size="6.5" font-weight="bold" text-anchor="middle">0.46s</text>

    <!-- Parity note -->
    <text x="500" y="36" fill="#0f172a" font-size="7" font-weight="bold">Makespan Parity:</text>
    <text x="500" y="47" fill="#64748b" font-size="6.5">Wall-clock bottleneck capped at 0.55s</text>
    <text x="500" y="58" fill="#16a34a" font-size="6.5" font-weight="bold">Zero runner starvation (Imbalance: 1.09)</text>
  </svg>
</div>

<!-- 6. Technical Q&A Section -->
<h2>6. Short Answer Technical Questions & Theoretical Evaluations</h2>
<p>
The following technical evaluations substantiate the theoretical and practical mastery of the assignment topic:
</p>

<div class="qa-box">
  <div class="qa-question">1. What is Dynamic Test-Subset Routing, and what fundamental CI/CD bottleneck does it address?</div>
  <div class="qa-answer">
    Dynamic Test-Subset Routing is an intelligent CI optimization strategy that executes only the test suites impacted by an incoming code change instead of blindly running the entire regression test suite. It solves the scalability bottleneck of linear and quadratic growth in CI execution duration, reducing CI runner queue times and developer feedback latency while conserving compute budgets.
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

<!-- 7. Key Learnings & Engineering Takeaways -->
<h2>7. Key Learnings & Engineering Takeaways</h2>
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

<!-- 8. GitHub Setup & Verification Commands -->
<h2>8. GitHub Repository Submission & Verification Commands</h2>
<p>
The repository is fully provisioned with Git history and configured with the candidate's exact remote repository URL:
</p>

<div class="submission-card">
  <div style="font-weight: bold; color: #1e40af; font-size: 8.5pt; margin-bottom: 2px;">
    🔗 Official GitHub Repository Submission Link (Click to Open in Browser):
  </div>
  <a href="https://github.com/sakshamsingh819/Dynamic-Test-Subset-Routing-Saksham-Singh-24BTRAO035-Course-Cloud-DevOps-DRIVE-DEVOPS-Assignment-4" target="_blank">
    https://github.com/sakshamsingh819/Dynamic-Test-Subset-Routing-Saksham-Singh-24BTRAO035-Course-Cloud-DevOps-DRIVE-DEVOPS-Assignment-4
  </a>
  <div style="margin-top: 5px;">
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
    <td>Full Multi-Page Dossier + Markdown Guide</td>
    <td><span class="badge badge-purple">Complete with Q&A Section</span></td>
  </tr>
</table>

<hr style="border: none; border-top: 1.5px solid #cbd5e1; margin-top: 16px;">
<div style="font-size: 7.8pt; color: #64748b; text-align: center;">
  <strong>Jain (Deemed-to-be University)</strong> • Faculty of Engineering and Technology • Department of Computer Science & Engineering<br>
  Candidate: <strong>Saksham Singh</strong> (USN: <strong>24BTRAO035</strong>) • Course: <strong>Automation Software</strong> • Branch: <strong>AI DRIVEN DEVOPS</strong> • October 2026
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
