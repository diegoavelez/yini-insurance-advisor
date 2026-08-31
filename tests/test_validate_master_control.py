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

## Owner Gate Budget

Owner approval gates are counted separately from executor tasks.
Level 2 with an accepted applicable spec: 3 owner approval gates.
Contingencies are reported separately from the normal gate budget.

## Grouped Decisions and Administrative Dispatch

Master control may administratively dispatch only already-authorized visible
tasks. Grouped decisions retain separately named grants and receipts.

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
    "docs/agents/agentops-workflow.md": """\
---
agentops_policy_version: "1.4"
profile: "provider-eval"
plugin_minimum_version: "0.11.0"
---

# AgentOps Workflow

The installed handoff skill owns CompactHandoff v3. Level 2/3 delivery to
independent review requires CompactHandoff v3 without fallback.
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

## Owner Gates and Lifecycle Bundles

Owner approval gates are not executor tasks. Level 2 with an accepted spec
normally uses three owner approval gates. Grouped lifecycle decisions retain
separately named grants, task identities, preconditions, and receipts.

## Retry and Harness Contingencies

One primary invocation and one dormant mechanical retry are the maximum.
Generic retry or harness-repair language is not authority. A harness repair
never resumes candidate work automatically.

## CompactHandoff Selection

Level 2/3 delivery to independent review requires `handoff.v3`; a required v3
failure stops without fallback. CompactHandoff does not authenticate authority
or prove manifest truth.

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
    "docs/adr/0002-owner-interruption-budget-and-compacthandoff-v3.md": """\
# ADR 0002: Owner interruption budget and selective CompactHandoff v3

## Status

Accepted delivery candidate pending independent review.

## Decision

Owner gate budgets count decisions, not executor tasks. Grouped decisions keep
separate grants. CompactHandoff v3 is selective at material candidate-bound
boundaries and never creates authority.

## Consequences

Required v3 verification fails closed without fallback. No automatic post-Git
reconciliation occurs without semantic change.
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


def test_validate_accepts_complete_prospective_receipt_entry(
    tmp_path: Path,
) -> None:
    _write_contract_repository(tmp_path)
    index_path = tmp_path / "docs/operations/receipts/index.md"
    index_path.write_text(
        index_path.read_text(encoding="utf-8").replace(
            "No entries.\n",
            "- receipt_id: `YINI-GOVERNANCE-STABILIZATION-PUBLICATION-2026-08-28`\n"
            "  date: `2026-08-28`\n"
            "  work unit: `YINI-GOVERNANCE-STABILIZATION`\n"
            "  terminal class: `external-publication`\n"
            "  evidence ceiling: transport observed plus local postflight\n"
            "  receipt pointer: `docs/operations/receipts/publication.md`\n"
            "  retention/access: `UNAVAILABLE`\n",
        ),
        encoding="utf-8",
    )

    assert _errors_for(tmp_path) == []


def test_validate_rejects_incomplete_prospective_receipt_entry(
    tmp_path: Path,
) -> None:
    _write_contract_repository(tmp_path)
    index_path = tmp_path / "docs/operations/receipts/index.md"
    index_path.write_text(
        index_path.read_text(encoding="utf-8").replace(
            "No entries.\n",
            "- receipt_id: `incomplete`\n",
        ),
        encoding="utf-8",
    )

    errors = _errors_for(tmp_path)

    assert any(
        error.startswith("incomplete receipt index entry:")
        for error in errors
    )


def test_validate_rejects_empty_sentinel_with_receipt_entry(
    tmp_path: Path,
) -> None:
    _write_contract_repository(tmp_path)
    index_path = tmp_path / "docs/operations/receipts/index.md"
    index_path.write_text(
        index_path.read_text(encoding="utf-8").replace(
            "No entries.\n",
            "No entries.\n\n"
            "- receipt_id: `present`\n"
            "  date: `2026-08-28`\n"
            "  work unit: `YINI-GOVERNANCE-STABILIZATION`\n"
            "  terminal class: `external-publication`\n"
            "  evidence ceiling: local deterministic\n"
            "  receipt pointer: `docs/operations/receipts/present.md`\n"
            "  retention/access: `UNAVAILABLE`\n",
        ),
        encoding="utf-8",
    )

    assert _errors_for(tmp_path) == [
        "empty receipt index cannot contain entries"
    ]


def test_validate_rejects_complementary_incomplete_receipt_entries(
    tmp_path: Path,
) -> None:
    _write_contract_repository(tmp_path)
    index_path = tmp_path / "docs/operations/receipts/index.md"
    index_path.write_text(
        index_path.read_text(encoding="utf-8").replace(
            "No entries.\n",
            "- receipt_id: `first`\n"
            "  date: `2026-08-28`\n"
            "  work unit: `YINI-GOVERNANCE-STABILIZATION`\n"
            "  terminal class: `external-publication`\n\n"
            "- receipt_id: `second`\n"
            "  evidence ceiling: local deterministic\n"
            "  receipt pointer: `docs/operations/receipts/second.md`\n"
            "  retention/access: `UNAVAILABLE`\n",
        ),
        encoding="utf-8",
    )

    errors = _errors_for(tmp_path)

    assert "incomplete receipt index entry: 1: evidence ceiling" in errors
    assert "incomplete receipt index entry: 2: date" in errors


def test_validate_accepts_multiple_complete_prospective_receipt_entries(
    tmp_path: Path,
) -> None:
    _write_contract_repository(tmp_path)
    index_path = tmp_path / "docs/operations/receipts/index.md"
    index_path.write_text(
        index_path.read_text(encoding="utf-8").replace(
            "No entries.\n",
            "- receipt_id: `first`\n"
            "  date: `2026-08-28`\n"
            "  work unit: `YINI-GOVERNANCE-STABILIZATION`\n"
            "  terminal class: `external-publication`\n"
            "  evidence ceiling: local deterministic\n"
            "  receipt pointer: `docs/operations/receipts/first.md`\n"
            "  retention/access: `UNAVAILABLE`\n\n"
            "- receipt_id: `second`\n"
            "  date: `2026-08-29`\n"
            "  work unit: `YINI-GOVERNANCE-STABILIZATION`\n"
            "  terminal class: `external-publication`\n"
            "  evidence ceiling: local deterministic\n"
            "  receipt pointer: `docs/operations/receipts/second.md`\n"
            "  retention/access: `UNAVAILABLE`\n",
        ),
        encoding="utf-8",
    )

    assert _errors_for(tmp_path) == []


def test_validate_rejects_entries_without_sentinel_or_receipt_id(
    tmp_path: Path,
) -> None:
    _write_contract_repository(tmp_path)
    index_path = tmp_path / "docs/operations/receipts/index.md"
    index_path.write_text(
        index_path.read_text(encoding="utf-8").replace(
            "No entries.\n",
            "No receipt has been recorded.\n",
        ),
        encoding="utf-8",
    )

    assert _errors_for(tmp_path) == [
        "receipt index has no entries or empty sentinel"
    ]


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


def test_validate_rejects_gate_and_task_conflation(tmp_path: Path) -> None:
    _write_contract_repository(tmp_path)
    master_path = tmp_path / "docs/operations/master-control.md"
    master_path.write_text(
        master_path.read_text(encoding="utf-8")
        + "\nOwner approval gates and executor tasks are the same count.\n",
        encoding="utf-8",
    )

    assert _errors_for(tmp_path) == [
        "gate/task conflation: docs/operations/master-control.md"
    ]


def test_validate_rejects_missing_governance_cadence_marker(tmp_path: Path) -> None:
    _write_contract_repository(tmp_path)
    master_path = tmp_path / "docs/operations/master-control.md"
    master_path.write_text(
        master_path.read_text(encoding="utf-8").replace(
            "## Owner Gate Budget\n\n",
            "",
        ),
        encoding="utf-8",
    )

    assert _errors_for(tmp_path) == [
        "missing marker in docs/operations/master-control.md: "
        "## Owner Gate Budget"
    ]


@pytest.mark.parametrize(
    ("relative_path", "injected", "expected_error"),
    [
        (
            "docs/operations/master-control.md",
            "Level 2 with an accepted applicable spec: 4 owner approval gates.\n",
            "invalid Level 2 owner gate budget: docs/operations/master-control.md",
        ),
        (
            "docs/operations/master-control.md",
            "Normal gate budgets include no contingency gate.\n",
            "hidden contingency: docs/operations/master-control.md",
        ),
        (
            "docs/operations/master-control.md",
            "The gate budget proves a 40 percent efficiency improvement.\n",
            "measured efficiency claim: docs/operations/master-control.md",
        ),
        (
            "docs/agents/executor-workflow.md",
            "Retry if needed.\n",
            "generic retry authority: docs/agents/executor-workflow.md",
        ),
        (
            "docs/agents/executor-workflow.md",
            "Repair the harness if needed.\n",
            "generic harness repair authority: docs/agents/executor-workflow.md",
        ),
        (
            "docs/agents/executor-workflow.md",
            "Harness repair automatically resumes candidate work.\n",
            "automatic harness resume: docs/agents/executor-workflow.md",
        ),
        (
            "docs/agents/executor-workflow.md",
            "CompactHandoff v3 authorizes delivery.\n",
            "handoff authority overclaim: docs/agents/executor-workflow.md",
        ),
        (
            "docs/agents/executor-workflow.md",
            "CompactHandoff v3 proves manifest truth.\n",
            "handoff truth overclaim: docs/agents/executor-workflow.md",
        ),
        (
            "docs/agents/executor-workflow.md",
            "A required v3 failure falls back to plain text.\n",
            "required v3 fallback: docs/agents/executor-workflow.md",
        ),
        (
            "docs/operations/master-control.md",
            "A second administrative closeout is mandatory.\n",
            "recursive administrative closeout: docs/operations/master-control.md",
        ),
        (
            "docs/agents/agentops-workflow.md",
            "# AgentOps Engineering Operating Model\n",
            "copied universal contract: docs/agents/agentops-workflow.md",
        ),
    ],
)
def test_validate_rejects_governance_cadence_contract_violations(
    tmp_path: Path,
    relative_path: str,
    injected: str,
    expected_error: str,
) -> None:
    _write_contract_repository(tmp_path)
    target_path = tmp_path / relative_path
    target_path.write_text(
        target_path.read_text(encoding="utf-8") + "\n" + injected,
        encoding="utf-8",
    )

    assert expected_error in _errors_for(tmp_path)


@pytest.mark.parametrize(
    ("relative_path", "injected", "expected_error"),
    [
        (
            "docs/operations/master-control.md",
            "Level 0 normally uses three owner decisions.\n",
            "invalid Level 0 owner gate budget: docs/operations/master-control.md",
        ),
        (
            "docs/operations/master-control.md",
            "Level 1 with an accepted applicable spec normally uses four owner decisions.\n",
            "invalid Level 1 owner gate budget: docs/operations/master-control.md",
        ),
        (
            "docs/operations/master-control.md",
            "Level 2 with an accepted applicable spec normally uses four owner decisions.\n",
            "invalid Level 2 owner gate budget: docs/operations/master-control.md",
        ),
        (
            "docs/operations/master-control.md",
            "Level 3 includes provider, deployment, pilot, and production in its core budget.\n",
            "invalid Level 3 external-rung budget: docs/operations/master-control.md",
        ),
        (
            "docs/agents/executor-workflow.md",
            "A mechanical retry bundle has two dormant retry grants.\n",
            "excess mechanical retry: docs/agents/executor-workflow.md",
        ),
        (
            "docs/agents/executor-workflow.md",
            "A third invocation remains eligible.\n",
            "excess mechanical retry: docs/agents/executor-workflow.md",
        ),
        (
            "docs/operations/master-control.md",
            "Automatic post-Git documentary reconciliation occurs without semantic change.\n",
            "automatic post-Git reconciliation: docs/operations/master-control.md",
        ),
    ],
)
def test_validate_rejects_additional_governance_contract_contradictions(
    tmp_path: Path,
    relative_path: str,
    injected: str,
    expected_error: str,
) -> None:
    _write_contract_repository(tmp_path)
    target_path = tmp_path / relative_path
    target_path.write_text(
        target_path.read_text(encoding="utf-8") + "\n" + injected,
        encoding="utf-8",
    )

    assert expected_error in _errors_for(tmp_path)


@pytest.mark.parametrize(
    ("injected", "expected_error"),
    [
        (
            "Level 0 normally uses 3 owner approval gates.\n",
            "invalid Level 0 owner gate budget: docs/operations/master-control.md",
        ),
        (
            "Level 0 does not require a spec, but it requires 3 owner approval gates.\n",
            "invalid Level 0 owner gate budget: docs/operations/master-control.md",
        ),
        (
            "Level 1 with an accepted spec normally uses four owner approval gates.\n",
            "invalid Level 1 owner gate budget: docs/operations/master-control.md",
        ),
        (
            "Level 2 with an accepted applicable\n"
            "spec normally uses four owner approval gates.\n",
            "invalid Level 2 owner gate budget: docs/operations/master-control.md",
        ),
        (
            "The core budget for Level 3 contains provider execution and pilot.\n",
            "invalid Level 3 external-rung budget: docs/operations/master-control.md",
        ),
    ],
)
def test_validate_rejects_broader_gate_budget_contradictions(
    tmp_path: Path,
    injected: str,
    expected_error: str,
) -> None:
    _write_contract_repository(tmp_path)
    master_path = tmp_path / "docs/operations/master-control.md"
    master_path.write_text(
        master_path.read_text(encoding="utf-8") + "\n" + injected,
        encoding="utf-8",
    )

    assert expected_error in _errors_for(tmp_path)


def test_validate_keeps_gate_budgets_in_their_own_propositions(
    tmp_path: Path,
) -> None:
    _write_contract_repository(tmp_path)
    master_path = tmp_path / "docs/operations/master-control.md"
    master_path.write_text(
        master_path.read_text(encoding="utf-8")
        + "\nLevel 0 uses 2 owner decisions, but Level 3 uses 3 owner decisions.\n",
        encoding="utf-8",
    )

    assert _errors_for(tmp_path) == []


def test_validate_rejects_level_three_budget_after_a_negated_level_zero_subject(
    tmp_path: Path,
) -> None:
    _write_contract_repository(tmp_path)
    master_path = tmp_path / "docs/operations/master-control.md"
    master_path.write_text(
        master_path.read_text(encoding="utf-8")
        + "\nLevel 0 does not include provider execution, but Level 3 core budget contains provider execution.\n",
        encoding="utf-8",
    )

    assert "invalid Level 3 external-rung budget: docs/operations/master-control.md" in _errors_for(
        tmp_path
    )


@pytest.mark.parametrize(
    "injected",
    [
        "A mechanical retry bundle has 2 dormant retry grants.\n",
        "A third attempt remains eligible.\n",
        "A third attempt is not preferred, but remains eligible.\n",
        "A third\nattempt is allowed.\n",
    ],
)
def test_validate_rejects_broader_retry_cardinality_contradictions(
    tmp_path: Path,
    injected: str,
) -> None:
    _write_contract_repository(tmp_path)
    workflow_path = tmp_path / "docs/agents/executor-workflow.md"
    workflow_path.write_text(
        workflow_path.read_text(encoding="utf-8") + "\n" + injected,
        encoding="utf-8",
    )

    assert (
        "excess mechanical retry: docs/agents/executor-workflow.md"
        in _errors_for(tmp_path)
    )


def test_validate_accepts_explicit_retry_cardinality_prohibition(
    tmp_path: Path,
) -> None:
    _write_contract_repository(tmp_path)
    workflow_path = tmp_path / "docs/agents/executor-workflow.md"
    workflow_path.write_text(
        workflow_path.read_text(encoding="utf-8")
        + "\nA third attempt is never eligible.\n",
        encoding="utf-8",
    )

    assert _errors_for(tmp_path) == []


def test_validate_keeps_retry_eligibility_with_its_own_attempt(
    tmp_path: Path,
) -> None:
    _write_contract_repository(tmp_path)
    workflow_path = tmp_path / "docs/agents/executor-workflow.md"
    workflow_path.write_text(
        workflow_path.read_text(encoding="utf-8")
        + "\nA third attempt is prohibited, but a first attempt remains eligible.\n",
        encoding="utf-8",
    )

    assert _errors_for(tmp_path) == []


@pytest.mark.parametrize(
    "injected",
    [
        "Automatic post-Git reconciliation occurs without semantic state change.\n",
        "Post-Git reconciliation is automatic\n"
        "when semantic state does not change.\n",
        "Without semantic state change, post-Git reconciliation occurs automatically.\n",
        "Post-Git reconciliation is not automatic by default, but it occurs automatically "
        "when semantic state does not change.\n",
    ],
)
def test_validate_rejects_broader_automatic_post_git_reconciliation(
    tmp_path: Path,
    injected: str,
) -> None:
    _write_contract_repository(tmp_path)
    master_path = tmp_path / "docs/operations/master-control.md"
    master_path.write_text(
        master_path.read_text(encoding="utf-8") + "\n" + injected,
        encoding="utf-8",
    )

    assert (
        "automatic post-Git reconciliation: docs/operations/master-control.md"
        in _errors_for(tmp_path)
    )


def test_validate_accepts_post_git_reconciliation_that_is_not_automatic(
    tmp_path: Path,
) -> None:
    _write_contract_repository(tmp_path)
    master_path = tmp_path / "docs/operations/master-control.md"
    master_path.write_text(
        master_path.read_text(encoding="utf-8")
        + "\nPost-Git reconciliation is not automatic when semantic state does not change.\n",
        encoding="utf-8",
    )

    assert _errors_for(tmp_path) == []


def test_validate_accepts_prohibited_post_git_reconciliation(
    tmp_path: Path,
) -> None:
    _write_contract_repository(tmp_path)
    master_path = tmp_path / "docs/operations/master-control.md"
    master_path.write_text(
        master_path.read_text(encoding="utf-8")
        + "\nPost-Git reconciliation is prohibited when semantic state does not change.\n",
        encoding="utf-8",
    )

    assert _errors_for(tmp_path) == []


def test_validate_keeps_post_git_conditions_with_their_own_subject(
    tmp_path: Path,
) -> None:
    _write_contract_repository(tmp_path)
    master_path = tmp_path / "docs/operations/master-control.md"
    master_path.write_text(
        master_path.read_text(encoding="utf-8")
        + "\nPost-Git reconciliation occurs automatically when semantic state changes, "
        "but a separate audit applies when semantic state does not change.\n",
        encoding="utf-8",
    )

    assert _errors_for(tmp_path) == []


def test_validate_tracks_post_git_subject_across_a_short_modifier(
    tmp_path: Path,
) -> None:
    _write_contract_repository(tmp_path)
    master_path = tmp_path / "docs/operations/master-control.md"
    master_path.write_text(
        master_path.read_text(encoding="utf-8")
        + "\nPost-Git reconciliation has a distinct owner, exceptionally, it occurs "
        "automatically when semantic state does not change.\n",
        encoding="utf-8",
    )

    assert (
        "automatic post-Git reconciliation: docs/operations/master-control.md"
        in _errors_for(tmp_path)
    )


def test_validate_accepts_explicit_handoff_prohibitions(tmp_path: Path) -> None:
    _write_contract_repository(tmp_path)
    workflow_path = tmp_path / "docs/agents/executor-workflow.md"
    workflow_path.write_text(
        workflow_path.read_text(encoding="utf-8")
        + "\nCompactHandoff v3 authorizes no action.\n"
        + "A required v3 failure never falls back.\n",
        encoding="utf-8",
    )

    assert _errors_for(tmp_path) == []


def test_validate_rejects_positive_handoff_authority_and_fallback(
    tmp_path: Path,
) -> None:
    _write_contract_repository(tmp_path)
    workflow_path = tmp_path / "docs/agents/executor-workflow.md"
    workflow_path.write_text(
        workflow_path.read_text(encoding="utf-8")
        + "\nCompactHandoff v3 itself authorizes a successor action.\n"
        + "A required v3 issue failure can fall back to a plain handoff.\n",
        encoding="utf-8",
    )

    errors = _errors_for(tmp_path)

    assert "handoff authority overclaim: docs/agents/executor-workflow.md" in errors
    assert "required v3 fallback: docs/agents/executor-workflow.md" in errors


def test_validate_rejects_positive_handoff_authority_with_unrelated_negation(
    tmp_path: Path,
) -> None:
    _write_contract_repository(tmp_path)
    workflow_path = tmp_path / "docs/agents/executor-workflow.md"
    workflow_path.write_text(
        workflow_path.read_text(encoding="utf-8")
        + "\nCompactHandoff v3 can authorize a successor action, not merely transport it.\n",
        encoding="utf-8",
    )

    assert "handoff authority overclaim: docs/agents/executor-workflow.md" in _errors_for(
        tmp_path
    )


def test_validate_rejects_positive_required_v3_fallback_with_unrelated_negation(
    tmp_path: Path,
) -> None:
    _write_contract_repository(tmp_path)
    workflow_path = tmp_path / "docs/agents/executor-workflow.md"
    workflow_path.write_text(
        workflow_path.read_text(encoding="utf-8")
        + "\nA required v3 failure does not preserve context and may fall back to plain text.\n",
        encoding="utf-8",
    )

    assert "required v3 fallback: docs/agents/executor-workflow.md" in _errors_for(
        tmp_path
    )


def test_validate_accepts_neither_nor_handoff_authority_prohibition(
    tmp_path: Path,
) -> None:
    _write_contract_repository(tmp_path)
    workflow_path = tmp_path / "docs/agents/executor-workflow.md"
    workflow_path.write_text(
        workflow_path.read_text(encoding="utf-8")
        + "\nCompactHandoff v3 authorizes neither action nor authority.\n",
        encoding="utf-8",
    )

    assert _errors_for(tmp_path) == []


def test_validate_rejects_wrapped_positive_handoff_authority(
    tmp_path: Path,
) -> None:
    _write_contract_repository(tmp_path)
    workflow_path = tmp_path / "docs/agents/executor-workflow.md"
    workflow_path.write_text(
        workflow_path.read_text(encoding="utf-8")
        + "\nCompactHandoff v3 can\nauthorize a successor action.\n",
        encoding="utf-8",
    )

    assert (
        "handoff authority overclaim: docs/agents/executor-workflow.md"
        in _errors_for(tmp_path)
    )


@pytest.mark.parametrize(
    "injected",
    [
        "A required v3 failure must not fall back.\n",
        "A required v3 failure never silently falls back.\n",
    ],
)
def test_validate_accepts_required_v3_fallback_prohibitions(
    tmp_path: Path,
    injected: str,
) -> None:
    _write_contract_repository(tmp_path)
    workflow_path = tmp_path / "docs/agents/executor-workflow.md"
    workflow_path.write_text(
        workflow_path.read_text(encoding="utf-8") + "\n" + injected,
        encoding="utf-8",
    )

    assert _errors_for(tmp_path) == []


@pytest.mark.parametrize(
    "injected",
    [
        "A required v3 issue may fall back to plain text.\n",
        "A required v3 verification will fall back to plain text.\n",
    ],
)
def test_validate_rejects_positive_required_v3_fallback_without_failure_word(
    tmp_path: Path,
    injected: str,
) -> None:
    _write_contract_repository(tmp_path)
    workflow_path = tmp_path / "docs/agents/executor-workflow.md"
    workflow_path.write_text(
        workflow_path.read_text(encoding="utf-8") + "\n" + injected,
        encoding="utf-8",
    )

    assert "required v3 fallback: docs/agents/executor-workflow.md" in _errors_for(
        tmp_path
    )


@pytest.mark.parametrize(
    ("injected", "expected_error"),
    [
        (
            'agentops_policy_version: "1.3"\n',
            "adapter policy drift: docs/agents/agentops-workflow.md",
        ),
        (
            'profile: "product"\n',
            "adapter profile drift: docs/agents/agentops-workflow.md",
        ),
        (
            'plugin_minimum_version: "0.10.0"\n',
            "adapter minimum drift: docs/agents/agentops-workflow.md",
        ),
    ],
)
def test_validate_rejects_adapter_contract_drift(
    tmp_path: Path,
    injected: str,
    expected_error: str,
) -> None:
    _write_contract_repository(tmp_path)
    workflow_path = tmp_path / "docs/agents/agentops-workflow.md"
    workflow_path.write_text(
        workflow_path.read_text(encoding="utf-8") + "\n" + injected,
        encoding="utf-8",
    )

    assert expected_error in _errors_for(tmp_path)


def test_physical_cli_reports_adapter_minimum_drift(tmp_path: Path) -> None:
    _write_contract_repository(tmp_path)
    workflow_path = tmp_path / "docs/agents/agentops-workflow.md"
    workflow_path.write_text(
        workflow_path.read_text(encoding="utf-8")
        + '\nplugin_minimum_version: "0.10.0"\n',
        encoding="utf-8",
    )
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"

    result = subprocess.run(
        [sys.executable, "-B", str(VALIDATOR_CLI), "--repo", str(tmp_path)],
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )

    assert result.returncode == 1
    assert result.stdout == (
        "master_control_validation=FAIL error=adapter minimum drift: "
        "docs/agents/agentops-workflow.md\n"
    )
    assert result.stderr == ""


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
