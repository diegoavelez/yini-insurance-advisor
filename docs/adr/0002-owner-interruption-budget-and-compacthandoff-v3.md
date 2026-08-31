# ADR 0002: Owner interruption budget and selective CompactHandoff v3

## Status

Delivered candidate pending independent review and owner disposition.

## Context

Yini already separates master control from lifecycle execution, but the local
contract did not consistently distinguish owner approval gates from executor
tasks. That ambiguity created avoidable owner interruptions while offering no
new authority control. The repository also needed a local selection rule for
the installed CompactHandoff v3 transport without making it universal ceremony.

## Decision

Owner gate budgets count decisions, not executor tasks. Level 0 normally uses
two owner decisions; Level 1 or 2 with an accepted applicable specification
normally uses three; the same depth without the required specification uses
four; Level 3 adds separately decided external rungs. Findings, drift, harness
defects, validation gaps, unavailable routes, and scope changes are classified
contingencies rather than hidden budget entries.

Grouped decisions preserve separately named grants, task identities,
preconditions, scopes, stops, consumption, and receipts. Master control may
dispatch a task already named by an applicable grant, but it remains strictly
read-only for implementation, validation, review, acceptance, Git, provider,
and external action.

CompactHandoff v3 is selective: it is required for Level 2/3 delivery to
independent review, correction to `NARROW_DELTA` or renewed `FULL`, and other
material governed worktree or candidate-bound retry boundaries. Level 0 and
low-risk Level 1 boundaries retain plain compact handoffs. V3 is transport only
and never authenticates authority or manifest truth.

## Consequences

Required v3 verification fails closed without fallback. The normal budget
reduces ceremonial owner decisions only by grouping already separate grants;
it does not measure or claim token, latency, cost, quality, or productivity
improvement. A semantic state change, not Git completion alone, determines
whether another documentary closeout is needed.
