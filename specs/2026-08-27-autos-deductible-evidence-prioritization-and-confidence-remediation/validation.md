# Validation

## Evidence Ceiling

Local acceptance can prove deterministic ranking, answer-evidence selection,
citation order, confidence gating, and compatibility against controlled inputs.
It cannot prove current Qdrant contents, provider availability, Groq behavior,
Hugging Face deployment state, or hosted user experience.

## Local Acceptance Checks

1. Fusion ordering:
   - a semantic candidate whose fused score increases moves to its correct
     score position;
   - candidates with equal fused scores retain stable original order;
   - duplicate chunk ids remain deduplicated.
2. General autos deductible retrieval:
   - the normalized family remains `SEGURO DE AUTOS`;
   - the candidate pool is bounded and larger than requested `top_k` when
     needed;
   - the final `top_k` leads with a direct definition/calculation chunk;
   - lateral chunks do not displace direct evidence.
3. Grounded answer:
   - the completion prompt receives direct evidence first;
   - documentary basis and citations lead with the same direct support;
   - lateral-only evidence produces at most `medium` confidence and an explicit
     limitation;
   - direct evidence plus all existing grounding conditions can still produce
     `high` confidence.
4. Compatibility:
   - the current movilidad deductible QA fixture still passes;
   - existing Autos Basico PT, assistance, motos, bicicletas/patinetas,
     utilitarios/pesados, and Muevete Libre routing remains unchanged;
   - unrelated grounded-answer tests remain green.

## Planned Verification Commands

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. ./.venv/bin/python -B -m pytest tests/test_retrieval.py -q -k 'hybrid or movilidad_deductibles_qa or deductible or deducible'
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. ./.venv/bin/python -B -m pytest tests/test_grounded_answer_generation.py -q
PYTHONDONTWRITEBYTECODE=1 ./.venv/bin/python -B -m ruff check rag/local_hybrid_recall.py rag/evidence_selection.py rag/grounded_answers.py rag/ingestion.py tests/test_retrieval.py tests/test_grounded_answer_generation.py
make test-release
PYTHONDONTWRITEBYTECODE=1 ./.venv/bin/python -B scripts/validate_master_control.py
git diff --check
```

If implementation does not touch one of the listed production modules, omit it
from the focused Ruff command and report that narrowing.

## Representative Query Variants

- `Que es el deducible en el seguro de autos y como se calcula?`
- `Como se calcula el deducible de un seguro de vehiculo?`
- `En el seguro de autos, que significa deducible?`

These variants belong to the same root-cause family and do not justify separate
slices.

## Separately Authorized Hosted Follow-up

Only after local acceptance and explicit provider/deployment validation
authority:

1. run `retrieve-chunks` against the current Qdrant collection for the three
   representative variants;
2. run `answer-query` and confirm direct `SEGURO DE AUTOS` evidence leads the
   prompt-facing result and citations;
3. validate the deployed Hugging Face UI at the exact published SHA;
4. confirm confidence is not `Alta` when only lateral evidence is returned;
5. record provider state, collection identity, published SHA, and timestamp
   without exposing secrets.

Hosted follow-up is not part of the current planning/specification authority.

