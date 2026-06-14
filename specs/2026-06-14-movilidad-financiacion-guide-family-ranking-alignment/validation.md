# Validation

This slice is ready when explicit financing-guide queries stay inside
`Manual Procedimiento Financiacion de polizas individuales` by default instead
of being outranked by adjacent PV financing mentions.

## Acceptance Checks

- The new spec bundle exists.
- `ops/term-equivalences.json` includes a financing-guide `document_name`
  query filter rule.
- Focused retrieval tests prove the normalized financing query carries the
  financing-guide `document_name` filter.
- Focused retrieval tests prove local lexical candidates from generic
  movilidad guides are excluded for this narrow intent.
- Live retrieval for financing-oriented queries returns financing-guide chunks
  ahead of `PV` financing mentions.

## Baseline Gap Evidence

- After extraction recovery, `cómo funciona la financiación de pólizas en movilidad`
  still returned `PROPUESTA DE VALOR MOVILIDAD` first, even though financing
  chunks were now present in lower ranks.
- After extraction recovery, `qué opciones de financiación hay para la póliza`
  returned a mixed top-k where the financing guide appeared but did not fully
  dominate the result set.

## Completion Evidence

- `ops/term-equivalences.json` now adds a curated financing-guide
  `document_name` filter rule anchored on `financiacion` plus explicit
  operational phrasing such as `como funciona`, `opciones`, `cuotas`,
  `procedimiento`, and `paso a paso`.
- Focused retrieval coverage now passes in `tests/test_retrieval.py` for:
  - financing-query normalization into
    `document_name = Manual Procedimiento Financiacion de polizas individuales`;
  - explicit `document_name` precedence;
  - Qdrant filter construction;
  - local lexical exclusion of adjacent `PROPUESTA DE VALOR MOVILIDAD` chunks.
- Focused validation now passes:
  - `./.venv/bin/python -m pytest tests/test_retrieval.py -q`
  - `./.venv/bin/python -m ruff check tests/test_retrieval.py`
  - `python -m json.tool ops/term-equivalences.json >/dev/null`
- Live retrieval now stays inside the financing guide family for both target
  queries:
  - `cómo funciona la financiación de pólizas en movilidad`
  - `qué opciones de financiación hay para la póliza`
- The top-5 live results for both queries now all come from
  `Manual Procedimiento Financiacion de polizas individuales`, closing the
  remaining financing guide-family ranking gap.
