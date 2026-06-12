# Plan

## Objective

Remove the deterministic supported-scope rejection that still blocks ARL/RUI
queries in the public app flow.

## Affected Files

- `core/query_scope.py`
- `tests/test_query_scope.py`
- `tests/test_app_ui.py`
- `specs/roadmap.md`
- `specs/2026-06-12-arl-supported-scope-alignment-remediation/requirements.md`
- `specs/2026-06-12-arl-supported-scope-alignment-remediation/validation.md`

## Assumptions

- retrieval and corpus indexing for the ARL slice are already functioning;
- the remaining end-to-end gap is limited to deterministic scope admission;
- a narrow token expansion is safer than broader classifier redesign.

## Risks

- over-broadening supported scope with generic tokens;
- masking a downstream retrieval/runtime issue if tests stop at classification;
- leaving hosted validation undocumented after the code change.

## Verification Strategy

- add focused classifier coverage for ARL/RUI wording;
- add focused UI-query coverage proving the ARL path no longer refuses early;
- run targeted pytest and lint commands on the touched files.
