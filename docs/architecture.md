# Architecture Notes

## Current Architecture State

- `PRD.md` defines the target architecture and milestones.
- `specs/mission.md` defines durable product principles and anti-goals.
- `specs/tech-stack.md` defines stack constraints and architecture boundaries.
- `specs/roadmap.md` defines implementation order and current status.
- Dated specs in `specs/` are the implementation truth.
- `Phase 0` through `Phase 19` are currently complete.

## Implemented Surfaces

- `app/` contains the Gradio demo surface and request/rendering seams.
- `agents/` contains the LangGraph workflow and agent orchestration seams.
- `rag/` contains ingestion, retrieval, indexing, and grounded-answer seams.
- `core/mcp_*` contains the implemented MCP integration boundaries.
- `ops/` contains observability and guardrail-facing operational seams.
- `tests/` contains regression, smoke, and compatibility coverage.

## Next Step

If new scope is approved, start from a new dated spec bundle and record it in
`specs/roadmap.md` before implementation.
