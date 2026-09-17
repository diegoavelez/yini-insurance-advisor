# Deterministic Read-Only Preflight — Specification

## Status and objective

Level 2 specification candidate, 2026-09-17. Work unit:
`YINI-DETERMINISTIC-READONLY-PREFLIGHT-SPEC`. Terminal target:
`READY_FOR_OWNER_SPEC_DECISION`; acceptance remains an owner decision.

Replace free-form preflight construction with one small local deterministic
observer, proposed as `scripts/readonly_preflight.py`. It must compare a bound
principal-checkout fingerprint, preserve each individual process outcome, and
stop at the first invalid input, mismatch, or failure. This candidate defines
future behavior; it implements none of it.

The source dispatch reports a composed tool command containing `git write-tree`
that exited 128 while a final `printf` left the wrapper at exit 0; execution
continued until master stopped it. That supplied observation motivates a
regression, not a replay, independent forensic finding, or cognitive-cause
claim. The existing [closed recipe](../2026-09-15-executor-checkout-boundary/plan.md)
already prohibits such substitutions and success suffixes (lines 187–242 and
503–509 at inspection). Documentation alone did not prevent that observation.

## Ownership and current authority

Role: `specification executor`. Dispatch owner:
`019f71d6-632c-7870-bfa2-89513fdeb85a`. Required route: `gpt-6-astra / high`.
Checkout precondition: principal physical repository
`/Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor`, absolute
common-dir equal to that path plus `/.git`; no reselection or redelegation.

Current write scope is only the five new Markdown files in this directory.
Implementation, test execution, existing-document edits, Git mutation,
plugin/configuration changes, installation, network/providers, readiness
continuation, independent review, and acceptance are excluded. The supplied
five foreign deltas remain unchanged; [validation.md](validation.md) binds them.

The [executor workflow](../../docs/agents/executor-workflow.md),
[master control](../../docs/operations/master-control.md), and installed
AgentOps Operating Model retain their authority. The prior recipe remains
operationally canonical until a separately authorized delivery updates its
pointer and the executor workflow. This candidate prospectively specifies a
new mechanism; it does not silently supersede an accepted procedure.

## Smallest useful seam and decision

Use Python standard library only, one `verify` operation, one closed JSON input
and one deterministic JSON result. [requirements.md](requirements.md) owns
the exact public contract; [plan.md](plan.md) owns the proposed process sequence
and adoption procedure. No generic shell runner, raw argv option, plugin
framework, arbitrary repository adapter, or tool-response parser is proposed.

The inspected installed plugin resource
`scripts/portable_readonly_preflight.py` (version
`0.12.0+codex.20260910081654`, lines 209–277) requires the literal repository ID
`agentops-engineering`. Its wider contract also binds trees, capabilities,
ignored selections, and executable identities. Direct use for Yini is invalid;
spoofing that ID, patching the installed plugin, or copying its full utility is
excluded. Reuse only the design ideas of closed fields, safe paths and explicit
failure. A minimal local implementation avoids a runtime import from a mutable
plugin cache. Upstream portability remains the plugin owner's decision.

## Evidence and limitations

The mechanism verifies a bounded observation; it neither authenticates an
owner grant nor consumes grants, enforces a tool allowlist, or authorizes any
successor. Normal shell access can bypass it. Its procedural use becomes
mandatory only after implementation validation, independent review, owner
acceptance, and explicitly authorized operational adoption.

V1 supports only this principal checkout, attached `main`, empty staged delta,
and present regular modified/untracked files. Worktrees, deleted/renamed/copied
files, submodule deltas, relevant ignored inputs, missing index, and other
unsupported states stop instead of prompting fallback or overgeneralization.
Byte hashes identify raw index/file bytes, never a reconstructed tree.

Two observations detect changes visible between them; they do not provide an
atomic filesystem snapshot or protection against hostile concurrent writers,
ABA changes, a compromised Git binary, or a modified verifier. Exclusive
checkout use and a trusted, owner-bound runtime remain preconditions. No
security isolation, global enforcement, efficiency gain, or zero-failure claim
is supported. Relevant ignored/generated inputs require a new scope decision.

## Completion and next decision

This specification pass is complete when the five documents agree, static
checks pass, and the receipt shows exactly five preserved foreign deltas plus
five new candidate files with unchanged HEAD/index and empty staging. No
candidate file contains its own purported final hash.

Recommend a grouped owner decision that separately names spec acceptance and
bounded TDD implementation in a fresh visible task. [tasks.md](tasks.md) defines
the proposed stages; [validation.md](validation.md) separates current checks
from future regressions. Neither the recommendation nor a static PASS starts
implementation, review, operational adoption, or another lifecycle action.
