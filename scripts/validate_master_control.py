#!/usr/bin/env python3
"""Validate the repository's versioned master-control baseline."""

from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED_FILES = (
    "AGENTS.md",
    "docs/operations/master-control.md",
    "docs/operations/execution-state.md",
    "docs/agents/executor-workflow.md",
    "scripts/validate_master_control.py",
)

REQUIRED_MARKERS = {
    "AGENTS.md": (
        "## Repository Governance",
        "docs/operations/master-control.md",
        "docs/operations/execution-state.md",
        "docs/agents/executor-workflow.md",
        "separate authorities",
        "Stop fail-closed",
    ),
    "docs/operations/master-control.md": (
        "## Truth Sources",
        "## Master Thread Responsibilities",
        "## Separate Authorities",
        "## Required Preflight",
        "## Evidence Standard",
        "## Strategic Stops",
        "Authorization for a local commit does not authorize a push.",
    ),
    "docs/operations/execution-state.md": (
        "state schema: `yini-master-control-v1`",
        "## Current Stage",
        "## Active Work",
        "## Evidence Available",
        "## Evidence Ceiling",
        "## Blockers and Unknowns",
        "## Next Decision",
    ),
    "docs/agents/executor-workflow.md": (
        "## Handoff Contract",
        "## Execution Rules",
        "## Return Contract",
        "## Review and Acceptance",
        "stop and return the",
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    return parser.parse_args()


def validate(repo: Path) -> list[str]:
    errors: list[str] = []
    for relative_path in REQUIRED_FILES:
        path = repo / relative_path
        if not path.is_file():
            errors.append(f"missing required file: {relative_path}")
            continue

        text = path.read_text(encoding="utf-8")
        for marker in REQUIRED_MARKERS.get(relative_path, ()):
            if marker not in text:
                errors.append(f"missing marker in {relative_path}: {marker}")
    return errors


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve()
    errors = validate(repo)
    if errors:
        for error in errors:
            print(f"master_control_validation=FAIL error={error}")
        return 1

    print("master_control_validation=PASS schema=yini-master-control-v1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
