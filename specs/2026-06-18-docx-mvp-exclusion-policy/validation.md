# Validation

This slice is ready when the current project docs no longer imply that `.docx`
forms belong to the MVP ingestion or answer surface.

## Acceptance Checks

- `README.md` states the ingestion contract is PDF-only and `.docx` forms are
  out of scope;
- `docs/category-onboarding-playbook.md` states operators should not onboard
  `.docx` files into the RAG corpus;
- `specs/roadmap.md` describes the PAC `.docx` files as excluded from the MVP,
  not deferred support.

## Completion Evidence

- focused grep over `README.md`, `docs/`, and `specs/roadmap.md` shows a
  consistent PDF-only MVP posture;
- no runtime code changes are required because ingestion already defaults to
  `*.pdf`.
