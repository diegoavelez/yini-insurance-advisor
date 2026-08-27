# Plan

## Objective

Correct the autos deductible retrieval-to-answer path so direct evidence leads
and confidence does not exceed the semantic strength of the selected evidence.

## Starting Point

- Required branch: `main`.
- Planning base: `c5ff813f891590b0ddee8bf742114c6e9b0749f5`.
- Required preflight: clean worktree and no divergence from the implementation
  task's declared starting ref.
- Active requirements:
  `specs/2026-08-27-autos-deductible-evidence-prioritization-and-confidence-remediation/requirements.md`.

## Expected Affected Files

- `rag/local_hybrid_recall.py`
- `rag/evidence_selection.py`
- `rag/grounded_answers.py`
- `rag/ingestion.py` only if narrow wiring is required
- `tests/test_retrieval.py`
- `tests/test_grounded_answer_generation.py`
- this spec bundle and `docs/operations/execution-state.md` for accepted status
  updates

The executor must stop and return a scope conflict before changing corpus
artifacts, equivalence rules, public contracts, provider configuration, or
unlisted production modules.

## Assumptions

- The restored corpus already contains direct `SEGURO DE AUTOS` deductible
  evidence; no ingestion or index mutation is required.
- The accepted autos family routing is correct.
- The remaining defect is bounded to candidate-pool size, fused ordering,
  evidence selection, and intent-specific confidence gating.
- Existing `RetrievedChunk`, `GroundedAnswerResult`, and citation contracts are
  sufficient.

## Implementation Sequence

1. Add a failing unit test for deterministic post-fusion score ordering and
   stable ties.
2. Add a failing public-seam retrieval test containing both lateral and direct
   `SEGURO DE AUTOS` deductible candidates, with requested `top_k` smaller than
   the candidate pool.
3. Implement the smallest bounded candidate-pool and fusion-order correction
   that makes those tests pass.
4. Add a failing grounded-answer test proving direct evidence leads answer
   input, documentary basis, and citations.
5. Add a failing grounded-answer test proving lateral-only evidence cannot
   yield `high` confidence for the target intent.
6. Implement the narrow autos deductible evidence selector and confidence gate,
   reusing existing normalization and typed contracts.
7. Run focused regressions for all movilidad deductible families and unrelated
   grounded-answer confidence behavior.
8. Run the local release gate and report any pre-existing baseline failures
   separately from slice failures.
9. Stop for master review. Do not commit, push, access providers, deploy, or
   open a successor slice without separate authority.

## Risks and Controls

- **Global ranking drift:** limit generic behavior to the invariant that fused
  scores determine fused order; use focused non-deductible regression cases.
- **Overbroad intent detection:** require both deductible intent and the
  normalized general autos family; preserve narrower Autos Basico PT and
  assistance routes.
- **False direct-evidence classification:** require explicit section/content
  support for definition or calculation, not the word `deducible` alone.
- **Confidence regression:** apply the new semantic gate only to the target
  intent and retain all existing grounding conditions.
- **Provider dependence:** use synthetic candidates and local artifacts for
  acceptance; keep live Qdrant and hosted UI checks as a later external gate.

## Verification Strategy

- Test the generic fusion invariant in isolation.
- Test retrieval through `retrieve_ranked_chunks` with deterministic fake
  Qdrant hits and local lexical candidates.
- Test answer behavior through `generate_grounded_answer` with deterministic
  retrieval results and a stub completion generator.
- Re-run the existing movilidad deductible QA routing and corpus-term checks.
- Run focused Ruff on changed Python files and the repository release gate.
- Treat hosted Qdrant and Hugging Face validation as follow-up evidence only.

