# Requirements

## Title

Recover filter compatibility for chunks with missing product metadata using source-relative path fallback.

## Context

Hybrid recall validation showed the AUTOS comparative chunks from `movilidad__autos__diferenciales-planes-autos` score strongly for comparison queries, but they are excluded before ranking because their persisted `product` metadata is `null`. When the user retrieves with `--product auto`, both semantic retrieval and local lexical recall lose those chunks.

The next narrow slice should add a deterministic fallback that infers canonical product values from `source_pdf_relative_path` when typed product metadata is missing.

## Scope

This slice should:

1. Infer a canonical product value from source-relative path segments.
2. Apply that inference only when persisted `product` metadata is missing.
3. Use the fallback in local lexical filter matching.
4. Preserve existing contracts and explicit metadata precedence.

This slice should not:

- rewrite stored chunk artifacts in place;
- change Qdrant payload contracts;
- infer unrelated metadata fields;
- override explicit non-null `product` values.

## Required Behavior

### 1. Missing-product fallback

Acceptance criteria:

- if a chunk record has `product=None`, retrieval may infer product from `source_pdf_relative_path`;
- explicit `product` values still win;
- inference remains deterministic and local.

### 2. Filter compatibility

Acceptance criteria:

- a product filter like `auto` can match a chunk whose path contains `AUTOS` even if stored product metadata is missing;
- non-matching paths remain excluded.

### 3. Backward compatibility

Acceptance criteria:

- non-product filters behave the same as before;
- focused retrieval tests pass;
- roadmap records the corrective slice.
