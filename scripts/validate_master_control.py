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
    "docs/agents/agentops-workflow.md",
    "docs/agents/executor-workflow.md",
    "docs/operations/metrics-contract.md",
    "docs/operations/receipt-policy.md",
    "docs/operations/receipts/index.md",
    "docs/adr/0001-read-only-master-control-topology.md",
    "docs/adr/0002-owner-interruption-budget-and-compacthandoff-v3.md",
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
        "## Owner Gate Budget",
        "Owner approval gates are counted separately from executor tasks.",
        "Level 2 with an accepted applicable spec: 3 owner approval gates.",
        "Contingencies are reported separately from the normal gate budget.",
        "## Grouped Decisions and Administrative Dispatch",
        "Grouped decisions retain separately named grants and receipts.",
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
        "## Owner Gates and Lifecycle Bundles",
        "## Retry and Harness Contingencies",
        "## CompactHandoff Selection",
        "Level 2/3 delivery to independent review requires `handoff.v3`",
    ),
    "docs/agents/agentops-workflow.md": (
        'agentops_policy_version: "1.4"',
        'profile: "provider-eval"',
        'plugin_minimum_version: "0.11.0"',
        "Level 2/3 delivery to independent review requires CompactHandoff v3",
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
    "docs/adr/0002-owner-interruption-budget-and-compacthandoff-v3.md": (
        "# ADR 0002: Owner interruption budget and selective CompactHandoff v3",
        "Owner gate budgets count decisions, not executor tasks.",
        "CompactHandoff v3 is selective",
        "Required v3 verification fails closed without fallback.",
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

GATE_TASK_CONFLATION = re.compile(
    r"owner approval gates? and executor tasks? are the same count",
    re.IGNORECASE,
)


def _normalized_contract_clauses(text: str) -> list[str]:
    clauses: list[str] = []
    for block in re.split(r"\n\s*\n", text):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue

        segments: list[str] = []
        if any(line.startswith("|") for line in lines):
            segments.extend(lines)
        else:
            current: list[str] = []
            for line in lines:
                if re.match(r"(?:[-*]|\d+\.)\s+", line) and current:
                    segments.append(" ".join(current))
                    current = []
                current.append(line)
            if current:
                segments.append(" ".join(current))

        for segment in segments:
            normalized = re.sub(r"\s+", " ", segment.casefold()).strip()
            clauses.extend(
                clause.strip()
                for clause in re.split(r"(?<=[.!?;])\s+", normalized)
                if clause.strip()
            )
    return clauses


def _match_is_negated(clause: str, match: re.Match[str]) -> bool:
    match_tokens = re.findall(r"[a-z0-9]+", clause[match.start() : match.end()])
    negations = {"no", "not", "never", "neither", "cannot"}
    if negations.intersection(match_tokens):
        return True

    proposition_prefix = re.split(
        r"(?:[,;:.!?]|\b(?:and|but|or)\b)", clause[: match.start()]
    )[-1]
    prefix_tokens = re.findall(r"[a-z0-9]+", proposition_prefix)
    if negations.intersection(prefix_tokens[-3:]):
        return True

    following = re.match(r"\s*(?:no|neither)\b", clause[match.end() :])
    return following is not None


LEVEL_SUBJECT = re.compile(r"\blevel ([0-3])\b")
OWNER_BUDGET = re.compile(
    r"\b(?:3|three|4|four)\b.{0,60}?"
    r"\bowner(?: approval)? (?:gates?|decisions?)\b"
)
SCOPE_BOUNDARY = re.compile(r"(?:[,;:.!?]|\b(?:and|but|or)\b)")


def _local_predicate_is_negated(scope: str, match: re.Match[str]) -> bool:
    """Evaluate polarity beside a predicate, never in an earlier relation."""
    preceding = list(SCOPE_BOUNDARY.finditer(scope[: match.start()]))
    start = preceding[-1].end() if preceding else 0
    local_tokens = re.findall(r"[a-z0-9]+", scope[start : match.end()])
    if {"no", "not", "never", "neither", "cannot"}.intersection(local_tokens):
        return True
    return re.match(r"\s*(?:no|neither)\b", scope[match.end() :]) is not None


def _anchored_level_scopes(clause: str) -> list[tuple[int, str, str]]:
    subjects = list(LEVEL_SUBJECT.finditer(clause))
    scopes: list[tuple[int, str, str]] = []
    for index, subject in enumerate(subjects):
        next_start = subjects[index + 1].start() if index + 1 < len(subjects) else len(clause)
        scope = clause[subject.start() : next_start]
        preceding = list(SCOPE_BOUNDARY.finditer(clause[: subject.start()]))
        relation_start = preceding[-1].end() if preceding else 0
        leading_fragment = clause[relation_start : subject.start()]
        relation_scope = scope
        if "core budget" in leading_fragment and not LEVEL_SUBJECT.search(
            leading_fragment
        ):
            relation_scope = leading_fragment + scope
        scopes.append((int(subject.group(1)), scope, relation_scope))
    return scopes


def _gate_budget_errors(text: str) -> list[str]:
    errors: list[str] = []
    for clause in _normalized_contract_clauses(text):
        for level, scope, relation_scope in _anchored_level_scopes(clause):
            budget_match = OWNER_BUDGET.search(scope)
            if budget_match and not _local_predicate_is_negated(scope, budget_match):
                invalid_budget = (
                    level == 0 and budget_match.group(0).split()[0] in {"3", "three"}
                ) or (
                    level in {1, 2}
                    and "accepted" in scope
                    and "spec" in scope
                    and budget_match.group(0).split()[0] in {"4", "four"}
                )
                if invalid_budget:
                    errors.append(
                        f"invalid Level {level} owner gate budget: "
                        "docs/operations/master-control.md"
                    )

            level_three_verb = re.search(r"\b(?:includes?|contains?)\b", relation_scope)
            if (
                level == 3
                and "core budget" in relation_scope
                and level_three_verb
                and re.search(r"\b(?:provider|deployment|pilot|production)\b", relation_scope)
                and not _local_predicate_is_negated(relation_scope, level_three_verb)
            ):
                errors.append(
                    "invalid Level 3 external-rung budget: "
                    "docs/operations/master-control.md"
                )
    return errors


RETRY_SUBJECT = re.compile(
    r"\b(?:first|second|third)\s+(?:attempt|invocation)\b"
    r"|\b(?:2|two|more than one)\s+dormant(?: mechanical)? retry grants?\b"
)


def _anchored_retry_scopes(clause: str) -> list[str]:
    subjects = list(RETRY_SUBJECT.finditer(clause))
    scopes: list[str] = []
    for index, subject in enumerate(subjects):
        start = 0 if index == 0 else subject.start()
        end = subjects[index + 1].start() if index + 1 < len(subjects) else len(clause)
        scopes.append(clause[start:end])
    return scopes


def _has_excess_retry_cardinality(text: str) -> bool:
    dormant_pattern = re.compile(
        r"\b(?:2|two|more than one)\s+dormant(?: mechanical)? retry grants?\b"
    )
    third_subject = re.compile(r"\bthird (?:attempt|invocation)\b")
    eligibility_predicate = re.compile(r"\b(?:eligible|allowed)\b")
    for clause in _normalized_contract_clauses(text):
        for scope in _anchored_retry_scopes(clause):
            dormant_match = dormant_pattern.search(scope)
            if dormant_match and not _local_predicate_is_negated(scope, dormant_match):
                return True
            third_match = third_subject.search(scope)
            eligibility_match = eligibility_predicate.search(scope)
            if (
                third_match
                and eligibility_match
                and not _local_predicate_is_negated(scope, eligibility_match)
            ):
                return True
    return False


def _has_automatic_post_git_reconciliation(text: str) -> bool:
    post_git_subject = re.compile(r"\bpost-git(?: documentary)? reconciliation\b")
    automatic_action = re.compile(r"\b(?:automatic(?:ally)?|occurs?)\b")
    unchanged_condition = re.compile(
        r"\b(?:without (?:a )?semantic(?: state)? change"
        r"|(?:when )?semantic state (?:does not|did not) change"
        r"|no semantic(?: state)? change)\b"
    )
    for clause in _normalized_contract_clauses(text):
        fragments = [
            fragment.strip()
            for fragment in re.split(r"(?:[,;:.!?]|\b(?:and|but|or)\b)", clause)
            if fragment.strip()
        ]
        for index, fragment in enumerate(fragments):
            if not post_git_subject.search(fragment):
                continue

            relation = [fragment]
            if index and unchanged_condition.search(fragments[index - 1]):
                relation.insert(0, fragments[index - 1])

            for continuation in fragments[index + 1 :]:
                if re.fullmatch(r"(?:exceptionally|however|otherwise)", continuation):
                    relation.append(continuation)
                    continue
                if re.match(r"^it\b", continuation):
                    relation.append(continuation)
                    continue
                break

            scope = "; ".join(relation)
            if not unchanged_condition.search(scope):
                continue
            for action_match in automatic_action.finditer(scope):
                if not _local_predicate_is_negated(scope, action_match):
                    return True
    return False


GOVERNANCE_CONTRACT_VIOLATIONS = (
    (
        "docs/operations/master-control.md",
        "hidden contingency",
        re.compile(
            r"normal gate budgets? include no contingency gate",
            re.IGNORECASE,
        ),
    ),
    (
        "docs/operations/master-control.md",
        "measured efficiency claim",
        re.compile(r"gate budget proves .*efficiency improvement", re.IGNORECASE),
    ),
    (
        "docs/agents/executor-workflow.md",
        "generic retry authority",
        re.compile(r"\bretry if needed\b", re.IGNORECASE),
    ),
    (
        "docs/agents/executor-workflow.md",
        "generic harness repair authority",
        re.compile(r"repair the harness if needed", re.IGNORECASE),
    ),
    (
        "docs/agents/executor-workflow.md",
        "automatic harness resume",
        re.compile(r"harness repair automatically resumes candidate work", re.IGNORECASE),
    ),
    (
        "docs/agents/executor-workflow.md",
        "handoff truth overclaim",
        re.compile(r"CompactHandoff v3 proves manifest truth", re.IGNORECASE),
    ),
    (
        "docs/operations/master-control.md",
        "recursive administrative closeout",
        re.compile(r"second administrative closeout is mandatory", re.IGNORECASE),
    ),
    (
        "docs/agents/agentops-workflow.md",
        "copied universal contract",
        re.compile(r"^# AgentOps Engineering Operating Model$", re.MULTILINE),
    ),
)

ADAPTER_FIELD_DRIFT = (
    (
        "adapter policy drift",
        re.compile(
            r'^agentops_policy_version:\s*"(?!1\.4"$)[^"]+"\s*$',
            re.MULTILINE,
        ),
    ),
    (
        "adapter profile drift",
        re.compile(r'^profile:\s*"(?!provider-eval"$)[^"]+"\s*$', re.MULTILINE),
    ),
    (
        "adapter minimum drift",
        re.compile(
            r'^plugin_minimum_version:\s*"(?!0\.11\.0"$)[^"]+"\s*$',
            re.MULTILINE,
        ),
    ),
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


def _has_positive_handoff_authority_claim(text: str) -> bool:
    authority_verb = re.compile(r"\bauthoriz(?:e|es)\b")
    for clause in _normalized_contract_clauses(text):
        if "compacthandoff v3" not in clause:
            continue
        for match in authority_verb.finditer(clause):
            if not _match_is_negated(clause, match):
                return True
    return False


def _has_positive_required_v3_fallback(text: str) -> bool:
    fallback_verb = re.compile(r"\bfall(?:s)? back\b")
    for clause in _normalized_contract_clauses(text):
        if "required v3" not in clause:
            continue
        for match in fallback_verb.finditer(clause):
            if not _match_is_negated(clause, match):
                return True
    return False


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

    gate_task_match = GATE_TASK_CONFLATION.search(master_text)
    if gate_task_match:
        errors.append("gate/task conflation: docs/operations/master-control.md")

    errors.extend(_gate_budget_errors(master_text))

    for relative_path, error_name, pattern in GOVERNANCE_CONTRACT_VIOLATIONS:
        if pattern.search(loaded_text.get(relative_path, "")):
            errors.append(f"{error_name}: {relative_path}")

    if _has_excess_retry_cardinality(workflow_text):
        errors.append("excess mechanical retry: docs/agents/executor-workflow.md")

    if _has_automatic_post_git_reconciliation(master_text):
        errors.append(
            "automatic post-Git reconciliation: docs/operations/master-control.md"
        )

    if _has_positive_handoff_authority_claim(workflow_text):
        errors.append("handoff authority overclaim: docs/agents/executor-workflow.md")
    if _has_positive_required_v3_fallback(workflow_text):
        errors.append("required v3 fallback: docs/agents/executor-workflow.md")

    adapter_path = "docs/agents/agentops-workflow.md"
    adapter_text = loaded_text.get(adapter_path, "")
    for error_name, pattern in ADAPTER_FIELD_DRIFT:
        if pattern.search(adapter_text):
            errors.append(f"{error_name}: {adapter_path}")
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
