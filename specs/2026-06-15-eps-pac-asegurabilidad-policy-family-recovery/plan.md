# Plan

## Objective

Fix the PAC `60 Más` asegurabilidad retrieval conflict that currently routes a
policy-intent query into the clausulado family.

## Affected files

- `ops/term-equivalences.json`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-15-mvp-current-category-acceptance-matrix/matrix.md`
- `specs/2026-06-15-eps-pac-asegurabilidad-policy-family-recovery/validation.md`

## Assumptions

- `politicas asegurabilidad pac 60 mas.pdf` is already ingested, embedded, and
  indexed with canonical `product=pac`, `document_type=policy`;
- the live PAC failure is caused by operator-rule ordering/specificity rather
  than missing corpus or missing Qdrant payload indexes.

## Risks

- narrowing the clausulado rule too aggressively could regress validated PAC
  coverage queries that should still land on the clausulado family;
- relying only on repo-rule order without regression coverage could let future
  operator edits reintroduce the same conflict.

## Execution

1. Add the narrow corrective spec bundle.
2. Tighten the PAC `60 mas` clausulado rule so it requires explicit
   coverage/clausulado language rather than the generic `pac` token.
3. Add regression tests for the repository PAC rules and their intended
   normalization outcome.
4. Rerun focused tests and live PAC retrieval/answer validation.
5. Update roadmap and MVP matrix only if the live PAC row now passes.

## Verification strategy

- run focused `pytest` on the PAC retrieval normalization coverage;
- inspect normalized PAC retrieval queries against the repository
  `ops/term-equivalences.json`;
- rerun live `retrieve-chunks` and `answer-query` for
  `¿Qué condiciones de asegurabilidad tiene PAC 60 Más?`.
