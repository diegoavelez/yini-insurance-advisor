from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys

import pytest

from scripts.validate_master_control import validate


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_CLI = REPOSITORY_ROOT / "scripts" / "validate_master_control.py"


VALID_CONTRACT_FILES = {
    "AGENTS.md": """\
## Repository Governance

Master control is a strictly read-only control tower.
See `docs/operations/master-control.md`,
`docs/operations/execution-state.md`, and
`docs/agents/executor-workflow.md`.
Lifecycle actions use separate authorities. Stop fail-closed on drift.
""",
    "CHANGELOG.md": """\
# Changelog

## 2026-08-28

- Add a governance delivery candidate; it is not accepted or published.
""",
    "docs/operations/master-control.md": """\
# Yini Master Control

## Purpose

Master control is a strictly read-only control tower.

## Pointer-Based Registers

It points to canonical owners and receives receipts.

## Truth Sources

Repository truth keeps precedence over secondary context.

## Reasoning-Necessity Dispatch

Validated deterministic mechanics use no model when a mechanism exists.

## Manual Yini Routing

Routing is manual, revocable, non-authorizing, and permits no silent
substitution.

## Gate Cadence

Each lifecycle action retains separate authority.

## No-Action Authority

Master control never implements, corrects, formally reviews, validates, runs
Git, publishes, accesses providers, deploys, pilots, produces, or performs an
external action.

## Strategic Stops

Ambiguity returns to the owner.
""",
    "docs/operations/execution-state.md": """\
# Yini Execution State

## State Metadata

- state schema: `yini-governance-v2`
- repository profile: `provider-eval`

## Current Semantic Stage

Repository governance stabilization is the active semantic work unit.

## Active Work

The delivery candidate awaits independent review and owner acceptance.

## Evidence Available

The accepted Level 2 spec is the governing input.

## Evidence Ceiling

Document semantics reach rung 1; focused local validator tests may reach rung
2 in their task receipt.

## Risks and Blockers

Independent review and owner acceptance remain absent.

## Next Owner Decision

Decide whether to authorize independent full review.
""",
    "docs/agents/executor-workflow.md": """\
# Executor Workflow

## Visible Task Topology

Implementation, correction, independent review, Git, and external actions use
fresh visible tasks.

## Internal Subagents

Internal subagents support only at least two independent, bounded,
non-mutating analysis workstreams and never replace a visible task.

## Handoff Contract

Every handoff binds task, fixed point, allowlist, authority, validation, and
stops.

## Manual Yini Routing

Validated deterministic mechanics use no model when a mechanism exists. Level
0 and mechanical documentation use `gpt-5.6-luna` at `max`. TDD, correction,
and `NARROW_DELTA` use `gpt-5.6-terra` at `medium`, or `high` for transversal
risk. Master orientation, architecture, public contracts, trust boundaries,
`FULL`, P0/P1, and material ambiguity use `gpt-5.6-sol` at `high`. Sol/Terra
`xhigh` or `max` requires representative evidence or exceptional owner
authorization. Silent substitution is forbidden.

## Compact Gate Cadence

Delivery, independent review, acceptance, Git, and external gates retain their
declared boundaries.

## Execution Rules

Executors stop fail-closed on drift or scope conflict.

## Return Contract

Return Receipt Capsule v1 with exact evidence and next gate.

## Review and Acceptance

Independent review and owner acceptance occur outside the authoring task.
""",
    "docs/operations/metrics-contract.md": """\
# Metrics Contract

## Ownership
## Definition Schema
## Metric Semantics
## Formula and Denominator
## Window
## Evidence Source
## Evidence Ceiling
## Change Control
## No Baseline or Savings Claim
""",
    "docs/operations/receipt-policy.md": """\
# Local Receipt Policy

## Universal Owner

The installed `references/receipt-policy.md` remains the universal owner.

## Provider-Eval Routing
## Local Projection
## Sensitive Evidence
## No Historical Backfill
""",
    "docs/operations/receipts/index.md": """\
# Receipt Index

## Scope

Prospective entries only. No historical receipts are backfilled.

## Entries

No entries.
""",
    "docs/adr/0001-read-only-master-control-topology.md": """\
# Read-only master-control topology

Yini uses a strictly read-only control tower and fresh visible tasks for every
lifecycle action because coordination must not acquire execution authority.
""",
    "scripts/validate_master_control.py": "# governed validator placeholder\n",
    "tests/test_validate_master_control.py": "# public seam placeholder\n",
}


def _write_contract_repository(root: Path) -> None:
    for relative_path, content in VALID_CONTRACT_FILES.items():
        target_path = root / relative_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(content, encoding="utf-8")


def _errors_for(root: Path) -> list[str]:
    return validate(root)


def test_validate_accepts_complete_local_governance_projection(tmp_path: Path) -> None:
    _write_contract_repository(tmp_path)

    assert _errors_for(tmp_path) == []


def test_validate_accepts_required_marker_split_by_markdown_whitespace(
    tmp_path: Path,
) -> None:
    _write_contract_repository(tmp_path)
    adr_path = tmp_path / "docs/adr/0001-read-only-master-control-topology.md"
    adr_path.write_text(
        "# Read-only master-control topology\n\n"
        "Yini uses a strictly read-only control tower and fresh\n"
        "visible task for every lifecycle action.\n",
        encoding="utf-8",
    )

    assert _errors_for(tmp_path) == []


@pytest.mark.parametrize(
    "missing_owner",
    [
        "docs/operations/metrics-contract.md",
        "docs/operations/receipt-policy.md",
        "docs/adr/0001-read-only-master-control-topology.md",
    ],
)
def test_validate_rejects_missing_governance_owner(
    tmp_path: Path,
    missing_owner: str,
) -> None:
    _write_contract_repository(tmp_path)
    (tmp_path / missing_owner).unlink()

    errors = _errors_for(tmp_path)

    assert f"missing required file: {missing_owner}" in errors


def test_validate_rejects_executable_master_duty(tmp_path: Path) -> None:
    _write_contract_repository(tmp_path)
    master_path = tmp_path / "docs/operations/master-control.md"
    master_path.write_text(
        master_path.read_text(encoding="utf-8")
        + "\nMaster control validates executor evidence.\n",
        encoding="utf-8",
    )

    assert any(
        error.startswith("forbidden executable master duty:")
        for error in _errors_for(tmp_path)
    )


def test_validate_distinguishes_modal_master_duty_prohibitions(tmp_path: Path) -> None:
    _write_contract_repository(tmp_path)
    master_path = tmp_path / "docs/operations/master-control.md"
    master_path.write_text(
        master_path.read_text(encoding="utf-8")
        + "\nMaster control must validate executor evidence.\n",
        encoding="utf-8",
    )

    assert any(
        error.startswith("forbidden executable master duty:")
        for error in _errors_for(tmp_path)
    )

    master_path.write_text(
        VALID_CONTRACT_FILES["docs/operations/master-control.md"]
        + "\nMaster control must not validate executor evidence.\n"
        + "Master control must never validate executor evidence.\n",
        encoding="utf-8",
    )

    assert _errors_for(tmp_path) == []


def test_validate_rejects_transient_git_fact_in_execution_state(
    tmp_path: Path,
) -> None:
    _write_contract_repository(tmp_path)
    state_path = tmp_path / "docs/operations/execution-state.md"
    state_path.write_text(
        state_path.read_text(encoding="utf-8") + "\n- canonical branch: `main`\n",
        encoding="utf-8",
    )

    assert any(
        error.startswith("transient Git fact in execution state:")
        for error in _errors_for(tmp_path)
    )


def test_validate_rejects_current_head_in_execution_state_prose(tmp_path: Path) -> None:
    _write_contract_repository(tmp_path)
    state_path = tmp_path / "docs/operations/execution-state.md"
    state_path.write_text(
        state_path.read_text(encoding="utf-8")
        + "\nCurrent HEAD is `b1f1e49`.\n",
        encoding="utf-8",
    )

    assert any(
        error.startswith("transient Git fact in execution state:")
        for error in _errors_for(tmp_path)
    )


def test_validate_rejects_current_git_fact_in_execution_state_table(
    tmp_path: Path,
) -> None:
    _write_contract_repository(tmp_path)
    state_path = tmp_path / "docs/operations/execution-state.md"
    state_path.write_text(
        state_path.read_text(encoding="utf-8")
        + "\n| Current HEAD | `b1f1e49` |\n",
        encoding="utf-8",
    )

    assert any(
        error.startswith("transient Git fact in execution state:")
        for error in _errors_for(tmp_path)
    )


def test_validate_rejects_silent_routing_substitution(tmp_path: Path) -> None:
    _write_contract_repository(tmp_path)
    workflow_path = tmp_path / "docs/agents/executor-workflow.md"
    workflow_path.write_text(
        workflow_path.read_text(encoding="utf-8")
        + "\nIf the required route is unavailable, use any available model.\n",
        encoding="utf-8",
    )

    assert any(
        error.startswith("silent routing substitution:")
        for error in _errors_for(tmp_path)
    )


def test_validate_distinguishes_routing_substitution_polarity(tmp_path: Path) -> None:
    _write_contract_repository(tmp_path)
    workflow_path = tmp_path / "docs/agents/executor-workflow.md"
    workflow_path.write_text(
        workflow_path.read_text(encoding="utf-8")
        + "\nDo not silently substitute a different model.\n",
        encoding="utf-8",
    )

    assert _errors_for(tmp_path) == []

    workflow_path.write_text(
        workflow_path.read_text(encoding="utf-8")
        + "\nSilently substitute a different model.\n",
        encoding="utf-8",
    )

    assert any(
        error.startswith("silent routing substitution:")
        for error in _errors_for(tmp_path)
    )


def test_validate_rejects_current_evidence_overclaim(tmp_path: Path) -> None:
    _write_contract_repository(tmp_path)
    state_path = tmp_path / "docs/operations/execution-state.md"
    state_path.write_text(
        state_path.read_text(encoding="utf-8")
        + "\n- current evidence ceiling: rung 3 integration\n",
        encoding="utf-8",
    )

    assert any(
        error.startswith("current evidence overclaim:")
        for error in _errors_for(tmp_path)
    )


def test_physical_cli_has_stable_pass_and_fail_results(tmp_path: Path) -> None:
    _write_contract_repository(tmp_path)
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"

    passing = subprocess.run(
        [sys.executable, "-B", str(VALIDATOR_CLI), "--repo", str(tmp_path)],
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )

    assert passing.returncode == 0
    assert passing.stdout == "master_control_validation=PASS schema=yini-governance-v2\n"
    assert passing.stderr == ""

    (tmp_path / "docs/operations/metrics-contract.md").unlink()
    failing = subprocess.run(
        [sys.executable, "-B", str(VALIDATOR_CLI), "--repo", str(tmp_path)],
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )

    assert failing.returncode == 1
    assert failing.stdout == (
        "master_control_validation=FAIL error=missing required file: "
        "docs/operations/metrics-contract.md\n"
    )
    assert failing.stderr == ""
