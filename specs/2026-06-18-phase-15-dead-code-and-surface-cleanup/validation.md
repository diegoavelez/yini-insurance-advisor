# Validation — phase-15-dead-code-and-surface-cleanup

This slice is ready when the repository no longer exposes the empty `mcp/`
placeholder as part of the supported implementation surface, while the real MCP
boundary in `core/mcp_*` continues to validate cleanly.

## Checks

- `mcp/__init__.py` is removed from the versioned repository surface.
- `README.md` repository layout no longer lists `mcp/`.
- `docs/architecture.md` points MCP readers to `core/mcp_*`.
- `specs/roadmap.md` records `phase-15-dead-code-and-surface-cleanup` and notes
  that the dead-code cleanup deliverable is now closed by this narrow slice.
- Focused MCP regression tests pass.
