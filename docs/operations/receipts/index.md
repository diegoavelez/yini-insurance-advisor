# Yini Receipt Index

## Scope

This is the prospective append-only index for sanitized durable Yini receipts.
It is not current semantic state, live Git state, an evidence ledger, or action
authority. `docs/operations/receipt-policy.md` owns the local projection and the
installed universal receipt policy owns classification.

Each future authorized entry must contain a stable receipt identifier, date,
work unit, terminal class, evidence ceiling, repository-relative receipt
pointer, and retention/access policy pointer or `UNAVAILABLE`. Entries never
embed raw sensitive evidence.

## Entries

- receipt_id: `YINI-GOVERNANCE-STABILIZATION-PUBLICATION-2026-08-28`
  date: `2026-08-28`
  work unit: `YINI-GOVERNANCE-STABILIZATION`
  terminal class: `external-publication`
  evidence ceiling: transport observed plus local postflight only
  receipt pointer: `docs/operations/receipts/2026-08-28-yini-governance-publication.md`
  retention/access: `UNAVAILABLE`

Historical receipts are intentionally not backfilled.
