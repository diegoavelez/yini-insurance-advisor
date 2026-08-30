#!/usr/bin/env python3
"""Validate the repository's versioned master-control baseline."""

from __future__ import annotations

import argparse
from pathlib import Path
import re

REQUIRED_FILES = (
    "AGENTS.md",
    "CHANGELOG.md",
    "docs/operations/master-control.md",
    "docs/operations/execution-state.md",
    "docs/agents/executor-workflow.md",
    "docs/operations/metrics-contract.md",
    "docs/operations/receipt-policy.md",
    "docs/operations/receipts/index.md",
    "docs/adr/0001-read-only-master-control-topology.md",
    "scripts/validate_master_control.py",
    "tests/test_validate_master_control.py",
)

REQUIRED_MARKERS = {
    "AGENTS.md": (
        "## Repository Governance",
        "strictly read-only",
        "docs/operations/master-control.md",
        "docs/operations/execution-state.md",
        "docs/agents/executor-workflow.md",
        "Stop fail-closed",
    ),
    "CHANGELOG.md": (
        "governance",
    ),
    "docs/operations/master-control.md": (
        "strictly read-only control tower",
        "## Pointer-Based Registers",
        "## Truth Sources",
        "## Reasoning-Necessity Dispatch",
        "## Manual Yini Routing",
        "## Gate Cadence",
        "## No-Action Authority",
        "## Strategic Stops",
    ),
    "docs/operations/execution-state.md": (
        "state schema: `yini-governance-v2`",
        "## Current Semantic Stage",
        "## Active Work",
        "## Evidence Available",
        "## Evidence Ceiling",
        "## Risks and Blockers",
        "## Next Owner Decision",
    ),
    "docs/agents/executor-workflow.md": (
        "## Visible Task Topology",
        "## Internal Subagents",
        "## Handoff Contract",
        "## Manual Yini Routing",
        "## Compact Gate Cadence",
        "## Execution Rules",
        "## Return Contract",
        "## Review and Acceptance",
        "gpt-5.6-luna",
        "gpt-5.6-terra",
        "gpt-5.6-sol",
        "Silent substitution is forbidden.",
    ),
    "docs/operations/metrics-contract.md": (
        "## Ownership",
        "## Definition Schema",
        "## Metric Semantics",
        "## Evidence Ceiling",
        "## Change Control",
        "## No Baseline or Savings Claim",
    ),
    "docs/operations/receipt-policy.md": (
        "references/receipt-policy.md",
        "## Provider-Eval Routing",
        "## Local Projection",
        "## Sensitive Evidence",
        "## No Historical Backfill",
    ),
    "docs/operations/receipts/index.md": (
        "## Scope",
        "## Entries",
    ),
    "docs/adr/0001-read-only-master-control-topology.md": (
        "strictly read-only",
        "fresh visible task",
    ),
}

FORBIDDEN_MASTER_DUTY = re.compile(
    r"^\s*(?:[-*]\s*)?master control\s+"
    r"(?:must\s+(?!(?:not|never)\b))?"
    r"(?:validates?|implements?|corrects?|reviews?|runs?|invokes?|stages?|"
    r"commits?|pushes?|publishes?|deploys?|accesses?|executes?|performs?)\b",
    re.IGNORECASE | re.MULTILINE,
)

TRANSIENT_GIT_FACT = re.compile(
    r"^\s*-\s*(?:canonical branch|canonical .*tracking|local tracking state|"
    r"head|index|worktree|refs?|remotes?|divergence|tracking|upstream|"
    r"git common-dir|git dir|detached head|current branch)\s*:"
    r"|^\s*(?:current\s+(?:head|branch)\s+is\b"
    r"|\|\s*current\s+(?:head|branch)\s*\|)",
    re.IGNORECASE | re.MULTILINE,
)

SILENT_ROUTING_SUBSTITUTION = re.compile(
    r"(?:use any available model|fallback to (?:an? )?(?:available|other) model|"
    r"^(?!\s*(?:[-*]\s*)?do not silently substitute\b).*?\bsilently substitute\b)",
    re.IGNORECASE | re.MULTILINE,
)

CURRENT_EVIDENCE_OVERCLAIM = re.compile(
    r"^\s*-\s*current evidence ceiling:\s*rung\s+[3-8]\b",
    re.IGNORECASE | re.MULTILINE,
)

RECEIPT_INDEX_ENTRY_MARKERS = (
    "receipt_id",
    "date",
    "work unit",
    "terminal class",
    "evidence ceiling",
    "receipt pointer",
    "retention/access",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    return parser.parse_args()


def _line_number(text: str, match: re.Match[str]) -> int:
    return text.count("\n", 0, match.start()) + 1


def _contains_required_marker(text: str, marker: str) -> bool:
    parts = re.split(r"(\s+)", marker)
    pattern_parts: list[str] = []
    for part in parts:
        if not part:
            continue
        if part.isspace():
            pattern_parts.append(r"\s+")
            continue

        pattern_parts.append(re.escape(part))

    return re.search("".join(pattern_parts), text) is not None


def _receipt_index_errors(text: str) -> list[str]:
    entries_heading = "## Entries"
    if entries_heading not in text:
        return []

    entries_text = text.split(entries_heading, 1)[1]
    entries_lines = entries_text.splitlines()
    entry_starts = [
        index
        for index, line in enumerate(entries_lines)
        if line.lstrip().startswith("- receipt_id:")
    ]
    has_empty_sentinel = any(
        line.strip() == "No entries." for line in entries_lines
    )

    if has_empty_sentinel:
        if entry_starts:
            return ["empty receipt index cannot contain entries"]
        return []

    if not entry_starts:
        return ["receipt index has no entries or empty sentinel"]

    errors: list[str] = []
    for entry_number, start in enumerate(entry_starts, start=1):
        end = (
            entry_starts[entry_number]
            if entry_number < len(entry_starts)
            else len(entries_lines)
        )
        fields: set[str] = set()
        for line in entries_lines[start:end]:
            candidate = line.lstrip()
            if candidate.startswith("- "):
                candidate = candidate[2:].lstrip()
            for marker in RECEIPT_INDEX_ENTRY_MARKERS:
                if candidate.startswith(f"{marker}:"):
                    fields.add(marker)

        for marker in RECEIPT_INDEX_ENTRY_MARKERS:
            if marker not in fields:
                errors.append(
                    f"incomplete receipt index entry: {entry_number}: {marker}"
                )
    return errors


def validate(repo: Path) -> list[str]:
    errors: list[str] = []
    loaded_text: dict[str, str] = {}
    for relative_path in REQUIRED_FILES:
        path = repo / relative_path
        if not path.is_file():
            errors.append(f"missing required file: {relative_path}")
            continue

        text = path.read_text(encoding="utf-8")
        loaded_text[relative_path] = text
        for marker in REQUIRED_MARKERS.get(relative_path, ()):
            if not _contains_required_marker(text, marker):
                errors.append(f"missing marker in {relative_path}: {marker}")
        if relative_path == "docs/operations/receipts/index.md":
            errors.extend(_receipt_index_errors(text))

    master_path = "docs/operations/master-control.md"
    master_text = loaded_text.get(master_path, "")
    master_match = FORBIDDEN_MASTER_DUTY.search(master_text)
    if master_match:
        errors.append(
            "forbidden executable master duty: "
            f"{master_path}:{_line_number(master_text, master_match)}"
        )

    state_path = "docs/operations/execution-state.md"
    state_text = loaded_text.get(state_path, "")
    transient_match = TRANSIENT_GIT_FACT.search(state_text)
    if transient_match:
        errors.append(
            "transient Git fact in execution state: "
            f"{state_path}:{_line_number(state_text, transient_match)}"
        )

    workflow_path = "docs/agents/executor-workflow.md"
    workflow_text = loaded_text.get(workflow_path, "")
    substitution_match = SILENT_ROUTING_SUBSTITUTION.search(workflow_text)
    if substitution_match:
        errors.append(
            "silent routing substitution: "
            f"{workflow_path}:{_line_number(workflow_text, substitution_match)}"
        )

    overclaim_match = CURRENT_EVIDENCE_OVERCLAIM.search(state_text)
    if overclaim_match:
        errors.append(
            "current evidence overclaim: "
            f"{state_path}:{_line_number(state_text, overclaim_match)}"
        )
    return errors


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve()
    errors = validate(repo)
    if errors:
        for error in errors:
            print(f"master_control_validation=FAIL error={error}")
        return 1

    print("master_control_validation=PASS schema=yini-governance-v2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
