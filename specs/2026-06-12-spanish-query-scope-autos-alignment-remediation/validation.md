# Validation

## Status

- Planned on `2026-06-12`.
- Completed on `2026-06-12`.

## Required Checks

- Focused query-scope and grounded-answer regression checks for the benign
  Spanish autos assistance query.

## Required Scenarios

- The benign autos assistance query is supported.
- A clearly unrelated Spanish query remains unsupported.
- The real `answer-query` path no longer refuses the autos query at the scope
  boundary.

## Merge Readiness

This spec is ready when the current autos assistance query clears the scope
gate without broadening the classifier into speculative product expansion.

## Evidence

- Focused regression tests passed:
  - `./.venv/bin/python -m pytest tests/test_query_scope.py tests/test_grounded_answer_generation.py -q`
- The classifier was narrowed with explicit supported Spanish autos-assistance
  vocabulary in `core/query_scope.py`, and a dedicated regression case was added
  in `tests/test_query_scope.py` for:
  - `¿Qué cubre la asistencia en pequeños eventos para autos?`
- The real grounded path succeeded after the classifier update:
  - `/private/tmp/yini-fast-venv311/bin/python -m rag.ingestion answer-query --query '¿Qué cubre la asistencia en pequeños eventos para autos?' --top-k 5`
  - Result: `grounded_answer_execution_succeeded`, `confidence: high`,
    `citation_count: 5`, no scope refusal.

## Recorded Outcome

- The benign Spanish autos assistance query now clears the scope gate and
  produces a grounded answer with citations.
- The remediation remains narrow: it broadens support only across explicit
  autos/movilidad/asistencia vocabulary and does not change the refusal posture
  for clearly unrelated domains.
