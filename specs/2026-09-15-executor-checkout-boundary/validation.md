# Executor and Checkout Boundary — Validation

All sections preceding **S1 prospective validation** retain historical evidence
and historical next-gate wording. They do not renew grants, resume R1, or assert
current review/acceptance. S1 adds only static specification evidence and a
future NOT_RUN matrix; the final S1 capsule owns its fresh checks and hashes.

## Historical Correction and Repair Evidence

## Acceptance Map

| Criteria | Documentary seam | Required check |
|---|---|---|
| AC1 | AGENTS, executor topology, master topology | Role is retained; master alone dispatches an exact grant; no executor redelegation |
| AC2–AC3 | executor checkout boundary; AGENTS/master pointers | Principal default, explicit owner worktree choice/reason, physical preflight first, stop without corrective cd |
| AC4 | executor handoff and return contracts | Role, dispatch_owner, physical repo, absolute common-dir, checkout precondition |
| AC5 | executor capture rule; AGENTS/master pointers | Read-only pagination through EOF without mutation replay; true failures still stop |
| AC6 | executor enforcement limits | Contractual prevention only; no demonstrated per-task tool allowlist or tool removal |
| AC7 | terminal byte inventory and Git evidence | Seven allowed candidate paths; five readiness hashes/modes intact; index and marker unchanged |
| AC8 | evidence below and terminal capsule | Observed mechanism separated from hypotheses; later delegation test NOT_RUN |

## Current Sanitized Diagnostic Record

This records the current authorized historical inspection, not a retroactive
receipt or acceptance of R1H1. Diagnostic class: `forensic-failure`; profile:
`provider-eval`; sanitized Full evidence accompanies the terminal Capsule.
Retention/access policy pointer: `UNAVAILABLE`. Only bounded tool evidence
and identifiers are retained; no reasoning or other sessions were inspected.

Source:
`/Users/diegovelez/.codex/sessions/2026/09/15/rollout-2026-09-15T22-54-42-01a0a559-3689-73a1-b6cb-0a5044afbc0a.jsonl`
(33 JSONL records; record numbers below are one-based).

- Record 8, turn_context: principal cwd, `gpt-5.6-terra`, effort `high`.
  This historical context does not establish this task's permissions.
- Record 9, incoming tool output: bounded read-only R1H1 grant, “no delegar”,
  exact principal repository/common-dir, and five readiness deltas.
- Records 15/18: `list_projects` call/output identifies the Yini project.
- Record 22: explicit `create_thread` request selects that project with
  `environment.type="worktree"` and `startingState.type="working-tree"`.
- Record 25: output returns only
  `client-new-thread:816e31b8-47e8-48c1-9ad3-2048c12c8690` and local host.
  No completed child task or worktree linkage is established by that output.

Observed mechanism: an executor issued a new-task request with an explicit
worktree selection despite the received no-delegation boundary. This proves
the dispatch request, not successful worktree setup or internal motivation.
No mutation-capable reproducer was run; this is historical static diagnosis,
not a reproduced root-cause claim or proof that the correction prevents it.

### Ranked Falsifiable Hypotheses

1. Executor/master role confusion: predicts executor-side dispatch despite
   the grant. The call is compatible; internal intent remains unknown.
2. Tool default alone chose the worktree: predicts no explicit worktree in
   the request. Record 22 contradicts that prediction.
3. Wrong initial cwd forced relocation: predicts an initial cwd mismatch.
   Record 8 instead names the principal checkout; motivation is still unknown.
4. Queued setup completed and produced a particular registered worktree:
   requires a completed task-to-path link. That evidence is absent from the
   permitted source; inventory alone cannot resolve this hypothesis.

## Direct Preflight Observations

Physical cwd/root and normalized common-dir match the principal repository
and its `.git`. HEAD is `bc1e4667e065d6b1f6f9001fee4ecd85b7cb31a5` on `main`;
staged delta is empty. The five readiness files match the grant's SHA-256
identities and mode `644`. The declared quarantine directory exists.

`git worktree list --porcelain` reports:

| Physical checkout | HEAD | Ref state | Incident link |
|---|---|---|---|
| `/Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor` | `bc1e4667e065d6b1f6f9001fee4ecd85b7cb31a5` | `refs/heads/main` | Current principal only |
| `/Users/diegovelez/.codex/worktrees/e03c/yini-insurance-advisor` | `bc1e4667e065d6b1f6f9001fee4ecd85b7cb31a5` | detached | Unknown |
| `/Users/diegovelez/.codex/worktrees/e7a1/yini-insurance-advisor` | `b1f1e49f6aab0672e7d34e7b3fabbf5629e82c0a` | detached | Unknown |

No lock/prunable fields were emitted. This is registered-worktree inventory,
not inspection of those other working trees or proof of their cleanliness.

## Completion Evidence and Limits

The terminal capsule owns actually executed candidate checks and final
hashes/modes: complete paginated reads, tracked/untracked whitespace checks,
exact inventory, foreign preservation, and unchanged Git/managed-marker
identity. This file specifies criteria and records preflight/history; it
does not predeclare a final PASS.

Later master-dispatched delegation test: `NOT_RUN` here. Independent review,
owner acceptance, hard enforcement, future compliance, and product readiness
are not demonstrated. No cleanup, commit, push, provider, application imports,
pytest, readiness resumption, or R1H1 `advise` execution occurs in this task.
Maximum evidence ceiling: rung 1, static/documentary. Next gate: master receives
this candidate and coordinates only the already-authorized later test under
its exact grant; acceptance and any further lifecycle action remain separate.

## H1 Read-Thread Wrapper Repair — 2026-09-16

This is a new, separately authorized harness-repair action. It does not alter
the historical authoring evidence, the authoring-time `NOT_RUN`, or R1's
terminal `HARNESS_DEFECT`; it does not resume or complete the FULL review.

### Cause and falsifiable hypotheses

The observed R1 final reports that its wrapper applied `JSON.parse` to a
non-JSON `read_thread` response and preserved the exact source error:
`SyntaxError: Unexpected token 'r', "read_threa"... is not valid JSON`.

1. Unconditional parsing of plain-text tool errors predicts that a synthetic
   text error raises `SyntaxError`. The legacy wrapper produced that RED.
2. Malformed JSON predicts a protected parse failure distinct from plain text.
   The repaired wrapper classified it as `MALFORMED_JSON`.
3. A valid but unexpected shape or a truncated nested output predicts no
   traversal and no PASS. The repaired wrapper classified these separately as
   `UNEXPECTED_JSON_SHAPE` and `TRUNCATED_RESPONSE`.

H1 matches the observed R1 mechanism. H2 and H3 are ruled out as the recorded
source cause but remain required defensive cases. No deliberately invalid live
tool call was made.

### RED, GREEN, and controlled live evidence

The synthetic matrix used invented, non-sensitive fixtures at the ephemeral
JavaScript wrapper seam:

| Fixture | Initial protected classifier | Documented helper |
|---|---|---|
| plain-text error | legacy `SyntaxError` RED; new `PLAIN_TEXT_TOOL_ERROR` | `tool_error`, incomplete |
| malformed JSON | `MALFORMED_JSON`, incomplete | `malformed_json`, incomplete |
| valid unexpected shape | `UNEXPECTED_JSON_SHAPE`, incomplete | `unexpected_shape`, incomplete |
| valid `turns` response | `VALID_STRUCTURED_RESPONSE`, complete | `valid`, complete |
| valid response with truncation | `TRUNCATED_RESPONSE`, incomplete | `truncated`, incomplete |

The helper copied from `executor-workflow.md` was executed against the same
five fixture classes. It emitted envelope metadata for every case and returned
`complete=true` only for `valid`; this verifies the documented snippet rather
than treating similar prose or an earlier classifier as its test.

One controlled R1 read used `turnLimit=10`, `includeOutputs=true`, and
`maxOutputCharsPerItem=6500`. Before parsing, the wrapper emitted format
`object`, `isError=false`, block types `[text]`, and text length `143395`.
Protected parsing found valid JSON with `turns`, but nested truncated outputs;
classification was `TRUNCATED_RESPONSE`, `complete=false`, not PASS. The
bounded capture preserved the R1 grant identity and final error quoted above.

Separate bounded inspections of authoring task
`01a0a563-4643-7203-9cb8-3738933096a6` and test task
`01a0a56c-7663-7413-916e-b405359d83a4` retained only grants, tool
calls/outputs, and final messages; no reasoning was requested or retained.
Both envelopes were non-error JSON objects with `hasMore=false`. The later
test's read-only PASS remains evidence of that one task only; it does not
retroactively change authoring's `NOT_RUN`, R1's STOP, or future enforcement.

The documented H1 helper emits envelope metadata, protects parsing, validates
the top-level local `turns`/`items` container before traversal, and rejects
errors or truncation as complete evidence. Its inner-record guard is addressed
by the separate C1 candidate below. It is a bounded capture repair, not an
official global `read_thread` schema and not a content reconstruction method.

### C1 candidate response to FULL R2 findings — 2026-09-16

Independent FULL R2 task `01a0a7a5-0a31-7511-ba77-05e3ca5344a0` returned two
P2 candidate findings. C1 is a new, bounded documentary correction; it does
not change R1's `HARNESS_DEFECT`, H1's repair-only status, the historical
authoring-time `NOT_RUN`, or the absence of independent review and owner
acceptance.

1. The helper must reject a non-record turn, a turn without an array `items`,
   or a non-record item before it can return traversable `records`. Its
   ephemeral local matrix retains the earlier error, malformed, unexpected,
   and truncation cases and adds `turns:[null]`, `turns:[{}]`,
   `turns:[{items:7}]`, and an invalid item inside a turn, plus a real
   non-empty positive response. The expected negative result is
   `unexpected_shape`, `complete=false`, without a throw; no fixture is
   provider or live-tool evidence.
2. The historical read-only PASS from test task
   `01a0a56c-7663-7413-916e-b405359d83a4` remains evidence of that task's
   selected principal route, pre/post observations, and absence of
   redelegation. Record 15 of
   `/Users/diegovelez/.codex/sessions/2026/09/15/rollout-2026-09-15T23-15-43-01a0a56c-7663-7413-916e-b405359d83a4.jsonl`
   shows its first preflight call supplied `workdir` explicitly. It therefore
   does not prove initial cwd selection without an override; it also does not
   prove an incorrect initial cwd.

C1's checks remain local, ephemeral wrapper checks plus documentary/Git
integrity checks. They do not demonstrate a global response schema, future
executor compliance, hard enforcement, independent review, acceptance, Git
publication, provider behavior, or readiness.

Observed C1 TDD evidence: the legacy literal produced the intended RED for
each of `turns:[null]`, `turns:[{}]`, and `turns:[{items:7}]`: the test
captured an assertion because `complete=true` and the later traversal captured
`TypeError`. After the minimal inner-record guard, the literal extracted from
`executor-workflow.md` passed the eleven-fixture ephemeral matrix: plain text,
malformed JSON, unexpected top-level shape, and truncation remained incomplete;
the five new malformed inner/container forms returned `unexpected_shape`,
`complete=false`, without throwing; and non-empty `turns` and top-level
`items` positives returned `valid`, `complete=true`. This is local deterministic
evidence only and is not a resumed R1 run, a live tool call, or a FULL PASS.

### Receipt routing and limits

Diagnostic class: `forensic-failure`; profile: `provider-eval`; routing:
`FULL_REQUIRED` (Capsule plus this sanitized Full record). Retention/access
policy pointer: `UNAVAILABLE`. This record contains stable task identifiers,
classifications, bounded metadata, and sanitized results, not raw transcripts,
reasoning, secrets, provider/client payloads, or unrelated session content.

Evidence ceiling: local deterministic wrapper behavior plus bounded read-only
capture; no independent review, R1 resumption, candidate PASS, acceptance,
publication, Git mutation, provider action, or successor authority. Next gate:
master/owner disposition after `HARNESS_REPAIR_COMPLETED`.

## S1 Prospective Validation — 2026-09-16

S1 is ordinary local documentary delivery under profile `provider-eval`:
`CAPSULE_REQUIRED`. It preserves the preceding sanitized forensic Full record
and its `UNAVAILABLE` retention pointer without reopening that diagnostic
action or reclassifying its history. No new raw transcript is collected.

### Historical R3 and G1 Boundary

The current S1 dispatch carries these bounded historical observations:

- R3 task `01a0a7b7-a00a-7931-a488-13d778070b40` confused the raw index
  file digest with a `git write-tree` operation. That operation was rejected;
  it does not prove conserved state, successful review, or product failure.
- G1 task `01a0a7cd-e484-7e62-9c77-4643468f20ef` stopped while searching
  nonexistent source directories. It did not materialize the proposed work
  or establish a postflight. This is a search/harness failure, not a product
  defect or evidence of a changed candidate.

These are owner-bound dispatch context, not new independent transcript checks.
R2 task `01a0a7a5-0a31-7511-ba77-05e3ca5344a0` and C1 task
`01a0a7ae-3788-7090-b82b-7769de902a53` remain historical pointers. S1 needs
no transcript reread to specify the accepted decision map. R1's STOP, H1's
repair-only status, R2 findings, C1 local matrix, and the explicit `workdir`
caveat above remain intact. No R3 review PASS or G1 completion is claimed.

### S1 Fresh Preflight Observations

The first shell invocation used `login:false`, no workdir/cwd override, and
no `cd`. Physical cwd and Git root both matched
`/Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor`; absolute
common-dir matched that path plus `/.git`. The next shell invocation was
literally `shasum -a 256 .git/index`.

Fresh observations matched `main`, HEAD
`bc1e4667e065d6b1f6f9001fee4ecd85b7cb31a5`, empty staged state, and raw
index digest `6573ee020f8a226351f8f889dc5cf80886ec3a1ed93940ce091e9757dadd87c7`.
All twelve initial delta hashes, regular-file kind, and mode `644` matched
the current grant; `spec.md` and `tasks.md` were absent. Registered worktrees
matched principal/main at that HEAD, `e03c` detached at that HEAD, and `e7a1`
detached at `b1f1e49f6aab0672e7d34e7b3fabbf5629e82c0a`.
The managed marker excluding its following LF matched
`2ddf2376bd563fb19bd8b92eeb019b7d5b49cac8b41299d3a20adf1e5d804f47`.
This is fresh S1 integrity evidence, not inferred preservation from R3 or G1.

### S1 Documentary Check Map

| Check | Requirement mapping | Authorized observation |
|---|---|---|
| D1 Scope and integrity | S1-AC02–05, S1-AC16 | Pre/post identities, status, raw index, worktrees; fourteen final delta hashes/modes; nine protected paths unchanged |
| D2 Literal recipe and capture | S1-AC01, S1-AC06–09 | Manual command order/exit/input review; no execution of future recipe scenarios |
| D3 Flow and authority | S1-AC10–14 | Manual Mermaid/table edge and guard coherence, roles, FULL/narrow and two-cycle boundary |
| D4 Artifact coherence | S1-AC13, S1-AC15–16 | Five files, AC/DoD/task links, historical sections, static versus NOT_RUN wording |
| D5 File checks | S1-AC16 | Local relative links, newline/whitespace, selected tracked diff check and per-file no-index checks |

The terminal capsule reports results actually completed for D1–D5 after the
last edit. This document does not predeclare postflight success or embed its
own final hash. A clean whitespace check alone is not candidate review.

### Future Recipe and Control-Flow Matrix

Every row is **FUTURE / NOT_RUN in S1**. These are expected observations for a
later explicitly authorized verification task, not executed fixtures, runtime
proof, or automatic authority. Failure cases must use safe invented inputs or
static command-string inspection; never cause real drift or execute a forbidden
command to prove it is forbidden.

| Case | Input / seam | Expected observation and disposition | AC |
|---|---|---|---|
| V01 Physical mismatch | Different cwd/root/common-dir; first call has no override | STOP before other repository work; no cd or checkout selection | 02, 10 |
| V02 Raw index drift | Changed file digest with otherwise matching inputs | STOP; tree identity cannot substitute or cure mismatch | 03–04 |
| V03 Missing index | `.git/index` absent or linked-worktree recipe not bound | Block without creating index or inventing a path/command | 04 |
| V04 Permitted foreign state | Exact declared dirty paths/status/kind/mode/hash | Preserve and continue; no demand for a clean tree | 05 |
| V05 Unexpected candidate | New path, status, mode, hash, or missing manifest coverage | STOP; later successful tests cannot repair preflight | 03, 05, 09 |
| V06 Capture truncated | Authorized range incomplete or nested truncated output | C → C within remaining bound; incomplete until captured; no mutation replay | 06–08 |
| V07 Tool error | `isError`, missing text, or plain-text error | Guard before parsing/traversal; record error; safe authorized alternate capture only, otherwise STOP | 08–09 |
| V08 Invalid JSON/shape | Malformed JSON, null turn, missing/non-array items, non-record item | No throw-driven traversal or PASS; classify incomplete and bound recovery | 08 |
| V09 Complete response | Valid non-empty turns/items, complete authorized scope | Complete only after envelope/shape/truncation checks and native capture | 06, 08 |
| V10 Optional lookup absent | rg no-match or verified nonexistent optional lookup source | Record absence; bounded known-source alternative in same task; no new gate | 07 |
| V11 Required source absent | Required source still absent after safe known-parent lookup | Real block and owner disposition; no inferred contents | 07, 09 |
| V12 Read allowance exhausted | Missing range remains, no remaining calls/pages | STOP with explicit evidence gap | 09–10 |
| V13 Forbidden strings | Inspect `git write-tree`, `git read-tree`, `git update-index`, `git hash-object -w` as data | Reject as inspection substitutions; execution NOT_AUTHORIZED | 01, 04 |
| V14 Exit distinctions | Normal no-index difference versus whitespace/error; rg 1 versus 2 | Preserve exits/output; expected difference/no-match is not generic failure, diagnostics never PASS | 01, 07 |
| V15 Initial/new-boundary review | No prior FULL or new trust/public/transversal boundary | FULL under fresh exact review grant | 11 |
| V16 Narrow qualification | Prior applicable FULL and bounded delta without changed boundaries | NARROW_DELTA only with explicit qualification and own grant | 11 |
| V17 PASS path | Independent assessment PASS after candidate checks and canonical updates | Terminal READY_FOR_OWNER_DECISION; no acceptance/Git/readiness | 10, 13–14 |
| V18 Candidate finding | Eligible in-scope finding, cycles below 2, exact preauthorized C1/C2 | New correction task, then separately granted fresh review; no same-task repair | 12 |
| V19 Cycle/severity stop | Two cycles used, P0/P1, unresolved acceptance conflict, or missing grant | STOP/owner disposition before correction; no hidden third cycle | 12 |
| V20 Hard stop | True drift, unknown mutation, write failure, secret risk, or non-capture tool failure | Terminal STOP; no retry, escalation, cleanup, or fallback that crosses scope | 09 |
| V21 Documentation timing | Candidate code/text ready but required canonical updates absent | Not ready for review; return missing requirement within grant limits | 13 |
| V22 Owner acceptance | Owner accepts reviewed bytes | Git/readiness/provider nodes remain blocked until separate named grants | 14 |
| V23 Historical caveat | Prior successful principal test explicitly supplied workdir | Does not prove initial cwd selection or incorrect initial cwd | 15 |
| V24 Graph/table correspondence | Every Mermaid edge versus transition row | Same guards/terminal states; capture self-loop is bounded and non-authorizing | 10 |

Future wrapper checks must reuse the existing C1 helper as the seam, not build
a parallel parser. Any future test task must itself start without a workdir
override if it claims to test initial cwd selection. Runtime, formal review,
graph-scenario execution, wrapper fixtures, and Mermaid rendering are all
`NOT_RUN` in S1. Mermaid text receives manual coherence checking only.

### Recovery Log and Completion Boundary

S1 preflight and source capture so far required no recovery. If a subsequent
read-only lookup/capture requires continuation, the terminal capsule records
the symptom, classification, source/range, bounded continuation and unresolved
gap. No such entry may conceal drift or convert an error into PASS.

S1's evidence ceiling is static/documentary rung 1; historical local wrapper
evidence retains its earlier meaning. No product command, app import, pytest,
make, CI, install, synthetic harness, provider, corpus access, external render,
formal review, acceptance, or Git mutation is part of S1. Required final state:
`READY_FOR_OWNER_SPEC_DECISION`, with owner acceptance and every successor
still unobserved and separately authorized.
