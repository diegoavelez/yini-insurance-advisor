# Requirements

## Title

Validate embedding runtime readiness and fail fast when model assets are not
cached locally.

## Context

The `PV` corpus is no longer blocked by chunk quality. The remaining blocker is
runtime: embedding generation still depends on a Hugging Face-hosted model that
may not be cached in the local environment.

The current behavior is too loose because a runtime can spend time attempting
network resolution before failing, and the operator workflow for warming assets
is not explicit.

## Scope

This slice should:

- add an explicit `warmup-embedding-assets` operator command;
- make local embedding and retrieval workflows prefer offline cached assets;
- fail fast with an actionable error when embedding assets are not cached
  locally;
- validate the offline failure path in the current environment.

This slice should not:

- change the embedding model;
- change retrieval ranking behavior;
- perform Qdrant indexing.

## Acceptance Criteria

### 1. Warm-up seam

- The CLI exposes an explicit embedding-asset warm-up command.

### 2. Offline-first runtime

- Offline embedding commands fail fast with a clear instruction to warm or
  pre-populate the model cache.

### 3. Regression coverage

- Focused tests cover:
  - parser wiring for the warm-up command;
  - successful warm-up dispatch;
  - fast failure when assets are not cached locally.
