"""
Command Line Interface (CLI) for Dynamic Test-Subset Routing
Author: Saksham Singh (24BTRAO035)
"""
import click
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

from .router import TestRouter, RoutingStrategy
from .ast_graph import ASTDependencyGraph
from .impact_tracer import ImpactTracer


@click.group()
def main():
    """Dynamic Test-Subset Routing (DTSR) CLI for high-velocity CI/CD pipelines."""
    pass


@main.command()
@click.option("--base", default=None, help="Base git ref for diff comparison (e.g. origin/main)")
@click.option("--head", default="HEAD", help="Head git ref (default: HEAD)")
@click.option("--files", default=None, help="Comma-separated explicit list of changed files")
@click.option(
    "--strategy",
    type=click.Choice(["SMART", "AST_ONLY", "IMPACT_ONLY", "ALL", "NONE"], case_sensitive=False),
    default="SMART",
    help="Routing strategy heuristic"
)
@click.option("--shards", default=1, type=int, help="Number of parallel CI shards")
@click.option("--json-out", is_flag=True, help="Print output as JSON")
def route(base, head, files, strategy, shards, json_out):
    """Computes the intelligent test subset impacted by recent changes."""
    router = TestRouter()
    file_list = [f.strip() for f in files.split(",")] if files else None
    strat_enum = RoutingStrategy(strategy.upper())

    decision = router.route(
        base_ref=base,
        head_ref=head,
        explicit_changed_files=file_list,
        strategy=strat_enum,
        num_shards=shards
    )

    if json_out:
        click.echo(json.dumps(decision.to_dict(), indent=2))
        return

    # Formatted terminal UI
    click.secho("\n=======================================================", fg="cyan", bold=True)
    click.secho("    DYNAMIC TEST-SUBSET ROUTING ENGINE (DTSR)        ", fg="cyan", bold=True)
    click.secho("    Candidate: Saksham Singh | USN: 24BTRAO035       ", fg="white")
    click.secho("=======================================================\n", fg="cyan", bold=True)

    click.echo(f"  Change Type:       {decision.change_type.value}")
    click.echo(f"  Strategy Applied:  {decision.strategy_applied.value}")
    click.echo(f"  Changed Files:     {len(decision.changed_files)} file(s)")
    for cf in decision.changed_files[:5]:
        click.echo(f"    • {cf}")
    if len(decision.changed_files) > 5:
        click.echo(f"    ... and {len(decision.changed_files) - 5} more")

    click.echo(f"  Total Churn:       {decision.total_churn} lines")
    click.echo("-" * 55)

    click.secho("  ROUTING & IMPACT METRICS:", bold=True)
    click.echo(f"  Full Suite Tests:   {decision.total_suite_count} test suites")
    click.secho(f"  Routed Subset:      {decision.routed_test_count} test suites", fg="green" if decision.routed_test_count < decision.total_suite_count else "yellow", bold=True)
    click.echo(f"  Est. Duration:      {decision.estimated_duration_sec:.2f}s (vs {decision.full_suite_duration_sec:.2f}s baseline)")
    click.secho(f"  Pipeline Savings:   {decision.time_saved_percent:.1f}% time / compute saved", fg="green", bold=True)
    click.echo("-" * 55)

    if decision.selected_tests:
        click.secho("  SELECTED TESTS (Prioritized Fail-Fast Order):", bold=True)
        for p in decision.risk_profiles:
            t = p["test_file"]
            impact = p["impact_type"]
            risk = p["final_risk_score"]
            dur = p["avg_duration_sec"]
            click.echo(f"    [Risk: {risk:.2f} | {impact:10s} | {dur:.2f}s] {t}")
    else:
        click.secho("  ✓ No impacted tests! Changes are documentation or non-functional.", fg="green")

    if decision.shard_plan:
        click.echo("-" * 55)
        click.secho(f"  PARALLEL CI SHARDING PLAN ({shards} runners):", bold=True)
        for s in decision.shard_plan["shards"]:
            click.echo(f"    Shard #{s['shard_id']}: {s['test_count']} tests (~{s['estimated_duration_sec']:.2f}s)")
            for st in s["tests"]:
                click.echo(f"      - {st}")
    click.echo("")


@main.command()
@click.option("--base", default=None)
@click.option("--head", default="HEAD")
@click.option("--files", default=None)
@click.option("--shard-id", default=None, type=int, help="Run only tests assigned to this shard index (1-based)")
@click.option("--shards", default=1, type=int, help="Total shards")
def run(base, head, files, shard_id, shards):
    """Executes the dynamically routed tests using pytest."""
    router = TestRouter()
    file_list = [f.strip() for f in files.split(",")] if files else None

    decision = router.route(
        base_ref=base,
        head_ref=head,
        explicit_changed_files=file_list,
        num_shards=shards
    )

    tests_to_run = decision.selected_tests
    if shard_id and decision.shard_plan:
        shard_matches = [
            s for s in decision.shard_plan["shards"] if s["shard_id"] == shard_id
        ]
        if shard_matches:
            tests_to_run = shard_matches[0]["tests"]

    if not tests_to_run:
        click.secho("✓ No tests required for execution (Docs / 0 impact). Exiting cleanly.", fg="green")
        sys.exit(0)

    click.secho(f"Running {len(tests_to_run)} routed test suite(s)...", fg="cyan", bold=True)
    cmd = [sys.executable, "-m", "pytest", "-v"] + tests_to_run
    res = subprocess.run(cmd)
    sys.exit(res.returncode)


@main.command()
def map():
    """Builds and prints the static AST dependency graph and coverage matrix."""
    click.secho("Analyzing project AST and dependency topology...", fg="cyan")
    ast_graph = ASTDependencyGraph()
    tracer = ImpactTracer()

    click.echo(f"Discovered modules: {len(ast_graph.forward_graph.nodes)}")
    for node in sorted(ast_graph.forward_graph.nodes):
        deps = list(ast_graph.forward_graph.successors(node))
        if deps:
            click.echo(f"  {node} -> {', '.join(deps)}")

    click.secho("\nTest Impact Footprint Matrix:", fg="cyan")
    for t in tracer.get_all_registered_tests():
        meta = tracer.get_test_metadata(t)
        cov = meta.get("covered_files", [])
        dur = meta.get("avg_duration_sec", 0.0)
        click.echo(f"  {t} ({dur:.2f}s)")
        for c in cov:
            click.echo(f"    covers -> {c}")


@main.command("ci-matrix")
@click.option("--base", default=None)
@click.option("--head", default="HEAD")
@click.option("--shards", default=2, type=int)
def ci_matrix(base, head, shards):
    """Outputs GitHub Actions matrix JSON payload for parallel matrix runners."""
    router = TestRouter()
    decision = router.route(base_ref=base, head_ref=head, num_shards=shards)

    matrix_items = []
    if decision.shard_plan:
        for s in decision.shard_plan["shards"]:
            matrix_items.append({
                "shard_id": s["shard_id"],
                "test_count": s["test_count"],
                "tests_args": " ".join(s["tests"]) if s["tests"] else "tests/conftest.py"
            })
    else:
        matrix_items.append({
            "shard_id": 1,
            "test_count": len(decision.selected_tests),
            "tests_args": " ".join(decision.selected_tests) if decision.selected_tests else "tests/conftest.py"
        })

    payload = {"include": matrix_items}
    click.echo(json.dumps(payload))


if __name__ == "__main__":
    main()
