# Changelog

## 2026-05-18

- Implement the `docling-ingestion-skeleton` Phase 2 slice with an admin-only
  CLI entrypoint, deterministic output paths, append-only manifest logging, and
  typed processed-document contracts.
- Add Docling as a project dependency and rebuild the repo’s local `.venv` on
  Python `3.11` to align the actual environment with the documented tech stack.
- Update `README.md` to reflect completed `Phase 0`, completed `Phase 1`, and
  the first implemented `Phase 2` ingestion slice.
- Tighten spec alignment with explicit CLI usage docs and added tests for
  append-only manifest reruns and invalid ingestion status values.

## 2026-05-17

- `chore: phase 0 foundation scaffold`
- `docs: add settings env validation spec`
- `docs: align roadmap with deployment posture`
- `feat: implement settings env validation`
- `docs: add changelog maintenance skill`
- `merge: settings-env-validation into main`
- Add the `shared-contracts-foundation` Phase 1 spec slice for retrieval, response, tool, and workflow-state contracts.
- Add typed shared contract models for documents, tools, responses, and agent state aligned with the PRD vocabulary.
- Expand contract validation coverage for typed filters, clause categories, comparisons, citations, wrapper results, and workflow state construction.
- Add deployment mode flags to the typed settings contract to close the last identified Phase 1 gap.
- Add the `deployment-mode-flags` spec slice and document allowed `APP_ENV` behavior for public MVP demo vs internal production.
- Add the `docling-ingestion-skeleton` Phase 2 kickoff spec with a CLI-first ingestion contract, deterministic storage rules, rerun policy, and processed-document contract expectations.
- Tighten roadmap and existing specs with credential activation timing, contract stability expectations, and a clearer MVP boundary.
