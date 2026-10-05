# Execution Fluency Roadmap — Requirements

All new behavior below is PROPOSED until separately reviewed, accepted and
adopted. Existing observers and grants keep their literal rules.

## R1 — Small reusable transport, F1

Proposed files: `scripts/execution_contract.py` and
`tests/test_execution_contract.py`. Standard library only; imports perform no
I/O. Public seams: `prepare(request_bytes) -> dict`,
`invoke(request_bytes) -> dict`, `main(argv) -> int`,
`literal_edit(before, old, new, expected_after_sha256) -> bytes`, and
`select_evidence(envelope, item_id) -> dict`. Types for byte arguments are
exact `bytes`; IDs/digests are strings. CLI verbs are exactly `prepare` and
`invoke`, with no other argv. Bounded request bytes arrive on stdin.
No arbitrary command, shell, output path, environment override or retry flag.

Request schema `yini-execution-transport/request-v1` is closed, all fields
required: `schema_version`, `source_contract_utf8`, `source_sha256`,
`work_unit_id`, `absent`, `python`, `observer`. The latter two objects have
exactly `path` and `sha256`. SHA fields are lowercase HEX64. Source string
encodes the exact original UTF-8 bytes, including terminal LF; its external
digest must match before parsing. Require v1 R2's complete closed schema,
including nested guards and duplicate-key rejection. No session scan or
role-based extraction. `work_unit_id` and sorted unique `absent` use v1 R2
rules; the only derivation is replacing those two fields. All other values,
including each delta row, stay identical. Serialize sorted compact ASCII JSON
plus one LF and compute the derived digest; never bind expectations to live
observations. No self-hash field or manually retyped manifest.

`prepare` is pure and returns the closed result below with derived bytes and
digest. It does not prove physical identity or invoke an observer. `invoke`
repeats preparation, verifies already-selected physical principal cwd,
absolute Python/observer/Git identities against external digests and invokes
only v1 once. Observer path must be principal `/scripts/readonly_preflight.py`;
Git identity is from the original contract. Python must be canonical,
non-symlink, regular executable with verified hash, invoked with `-B`.
No private observer helper is imported. Schema guards are locally testable
transport guards; v1 remains authoritative and still performs its own checks.

CLI process receives a caller-sanitized environment. The child Python
environment is a copy of `os.environ` with ALL `GIT_*` removed, then
`GIT_OPTIONAL_LOCKS=0`; verify its names before launch, never emit values.
Do not copy the observer's internal minimal Git environment into Python.
Reject inherited Python/loader injection variables (`PYTHONPATH`,
`PYTHONHOME`, `LD_PRELOAD`, `LD_LIBRARY_PATH`, any `DYLD_*`) before launch;
do not silently repair them. Use absolute argv, `shell=False`, exact stdin
bytes and digest, explicit verified cwd, no cwd correction. The observer
alone owns its internal Git environment and twelve-process sequence.

Support only v1 coverage in this first transport. V2 and future v3 remain
separately selected mechanisms under their existing contracts; unsupported
transport coverage stops before invocation, never tries versions. Adoption
must not require this v1-only transport for v2/v3 work.

## R2 — Closed result and capture, F1

Transport result fields, all required and no extras:

| Field | Exact contract |
|---|---|
| schema_version | `yini-execution-transport/result-v1` |
| work_unit_id | validated ID or null |
| outcome | `PREPARED`, `MATCH`, `STOP` |
| classification | `NONE`, `INPUT_ERROR`, `HARNESS_DEFECT`, `CANDIDATE_FINDING`, `DRIFT`, `DENIAL`, `OUTPUT_MISSING`, `OBSERVER_STOP` |
| exit_code | integer: 0 for PREPARED/MATCH; 2 input; 3 drift; 4 denial; 5 harness; 6 missing/invalid output; native nonzero observer exit for OBSERVER_STOP |
| contract_utf8, contract_sha256 | derived canonical string/digest, or null before valid preparation |
| invoked | boolean; true only once child launch succeeds |
| process | null before launch, otherwise closed record below |
| observer_result | exact validated R6 object, including STOP, or null |
| successor_authority | false always |

Process record fields are exactly `returncode`, `stdout_sha256`,
`stderr_sha256`, `stdout_bytes`, `stderr_bytes`, `complete`; returncode is
native integer or null for timeout/capture failure. Counts are nonnegative
integers, booleans rejected. Complete means both streams fully captured and
child reaped, not successful. Digests cover captured bytes, including partial
streams when complete=false. Raw streams remain bounded in memory until
classification; capture exit/stdout/stderr BEFORE assertions or JSON parsing.
Emit the safe process record even when result parsing fails. Emit a valid
native STOP as observer_result so its reason is retained. Never invent the
reason of a missing/malformed result or dump arbitrary stderr/config values.

Require exact canonical R6 keys, types, reason/exit agreement, native exit
agreement, complete ordered observations, exact fingerprint and false
successor authority before MATCH. MATCH requires exactly twelve exit-0,
complete records in v1 plan order and empty staged streams. STOP cannot
carry a MATCH fingerprint. R6's own closed reasons retain their meaning.
Any nonzero native exit is terminal even with a valid result. A malformed,
missing, truncated, mismatched or oversized result cannot PASS.

Fixed limits: request 524288 bytes, source/derived contract each 262144;
each child stream 262144, total process deadline 90 seconds; physical tool
hashes each 16 MiB. Bound reads incrementally; cap+1 or deadline terminates
and reaps the child, marks incomplete, launches no successor. Result JSON is
sorted compact ASCII plus LF, maximum 2097152 bytes (accounts for escaped
contract plus nested R6); failure to deliver is terminal, never success.
No file persistence or per-tool receipt store is added.

`select_evidence` accepts a caller-supplied native read_thread envelope only.
Check isError, content types and body structure before JSON parsing; accept
one text JSON body with `turns[].items[]` or `items[]`, then exact item ID.
Reject duplicate IDs, unknown shape, missing item or incomplete selected item.
Return exactly `{kind, item}` where kind is `COMPLETE`, `TOOL_ERROR`,
`INVALID`, `MISSING`, `INCOMPLETE`; item is null unless COMPLETE. Complete
item types allowed: `agentMessage` phase `final_answer` and
`commandExecution`; exclude reasoning. The caller binds the source thread,
turn/page and item identity. A complete selected item proves only that item,
not complete history; pagination remains a bounded read-only continuation.
No live API call or recursive scanning of sessions is part of the helper.

## R3 — Literals, config scope and failure classes

`literal_edit` is pure: require exactly one nonempty old-byte occurrence,
perform a single replacement, require externally supplied resulting digest,
return exact bytes. Retain every byte outside that span, including SPACE/LF
and final newline. Limit each input/result to 262144 bytes; mismatch raises
a closed error before mutation. The caller uses the authorized edit tool and
compares actual bytes with these prepared bytes afterward. This helper grants
no edit, mutating retry or permission to regenerate the expected digest from
the actual output. Its rejection is INPUT_ERROR, never intended TDD RED for
candidate behavior unless that rejection is the declared test scenario.

Principal `.git/config.worktree` absence uses lstat/lexists semantics at the
explicit common-dir path. Existing linked metadata files are different
identities; their presence is not drift or a reason to disable configuration.
The transport does not add config coverage to v1 or inspect linked config
values. When the grant binds principal config hash/absence, the scoped
pre/postflight preserves those checks outside v1's unchanged assurance.

| Class | Meaning | Permitted continuation only under fresh explicit bundle |
|---|---|---|
| INPUT_ERROR | Invalid/mistranscribed governed input or contract | Correct governed input only with separate authority; no live rebinding |
| HARNESS_DEFECT | Invocation/environment/capture construction fault, not candidate behavior | At most one invocation-only repair if oracle and governed inputs unchanged, before observer launch; deterministic repeat stops |
| CANDIDATE_FINDING | Valid validator observes in-scope candidate failing accepted behavior | At most two authorized semantic correction cycles; expected TDD RED is normal transition |
| DRIFT | Initial identity mismatch, unexplained state change or unknown mutation | Terminal; preserve state |
| DENIAL | Runtime approval/permission refused | Terminal; no bypass or automatic escalation |
| OUTPUT_MISSING | Required output incomplete/invalid/unavailable | Complete retained read-only range if available and allowed; never replay mutation or observer |
| OBSERVER_STOP | Observer invoked and returns STOP/nonzero or invalid result | Terminal; no retry, repair, fallback or changed expectation |

Invalid observer output retains classification OUTPUT_MISSING and the same
terminal no-reinvoke rule. Native STOP remains OBSERVER_STOP; nested reason
may explain input/drift but does not reopen the grant. The transport does not
emit CANDIDATE_FINDING for preparation/observation failures; that class belongs
to later valid candidate checks and their receipt. Plain-text tool errors are
classified before JSON.parse; do not assert them into candidate failures.

## R4 — Objective continuity and ownership, F2

Master prepares exact contract bytes and separately bound digests, source
item IDs, protected inventory, measurable objective, scopes, validators,
route, finite counters and successor expectations before dispatch. Executor
validates them; it does not reconstruct history or choose a checkout.
Owner decisions may group separately named grants. Administrative dispatch
and mechanical checks are not additional owner approval gates.

Proposed normal delivery is one visible executor objective containing edit,
affected validation and finite correction, then a fresh proportional
independent review task and owner acceptance. Local ceilings are 2 eligible
identical transient pre-mutation retries, 1 invocation/environment-only
repair, 2 semantic correction cycles after first complete validation; counters
are separate and recorded honestly. No replay after observer invocation.
No repeated broad suite after unchanged focused PASS. Grant expiry, actual
drift, unknown mutation, denial, sensitive data, scope conflict, exhausted
counter or changed oracle outside authority is terminal.

This guidance does not expand current policy. Any proposed new procedural
wording remains PROPOSED until canonical adoption and acceptance. Independent
review, acceptance, Git and external work remain separate named authorities.
No confirmation is requested merely because a declared in-scope edit produced
its expected successor. No promise of zero errors, gates or interruptions.

## R5 — O1 and pending bytes, F3

The owner, through dispatch, confirms O1 acceptance following FULL PASS in
review thread beginning `01a0f364`; the audit identifies native postflight
`exec-b1ed1961-f902-4224-908a-e494f71ad020`. The full thread ID was not supplied
here; do not fabricate it. Reuse the audit's exact item pointer or obtain the
complete accepted receipt reference in the future dispatch. FULL PASS alone
does not confer acceptance. Current execution-state and roadmap still project
O1 as pending: reconcile those current projections in a fresh task, without
claiming new review, integration, publication or provider evidence.

The WorktreeConfig appendix in the previous spec/validation repeats pending
O1. Add a dated prospective clarification that identifies the superseded
current projection and points to accepted O1 history; preserve historical
S1/I1/C1/W-S1 narratives and receipts as history. Do not replace all historical
occurrences of 'pending'. Prior C1/O1 acceptance does not accept v3.

Previous tasks.md currently contains the correct phrase `Prior C1 and O1
acceptances remain unchanged; neither accepts v3.` followed by LF before
`Git,`. Its supplied successor digest begins `c0db211a`; those bytes did not
pass the earlier SPACE-preserving oracle. Owner chooses exactly one option:

- Recommended: explicitly accept that LF as the new formatting disposition,
  leaving tasks.md unchanged; review the known bytes and document that this
  is a new acceptance, not historical PASS or a resumed old grant.
- Exact restoration: authorize one tasks.md literal LF-to-SPACE replacement
  after the phrase, with independently prepared old/new bytes, exact resulting
  digest and scoped preservation checks. No wording or other byte changes.

Do not force another recovery merely to close this spec. Both options need
new authority and review/acceptance of their actual resulting state. The
initial design task preserves c0db211a bytes. F3 can close independently of
F1 adoption, F4 transfer, v3 implementation and publication using existing v1
with an explicitly bound one-task local objective and in-memory patch check.

## R6 — Local proposal and external boundary, F4

Future local artifact:
`docs/operations/proposals/agentops-literal-transcription-clarification.md`.
It states evidence IDs, installed policy/version, exact owner of proposed
wording (`references/authority-grants.md`), current strict behavior, narrow
proposed change, risks, two examples, required tests and transfer boundary.
Do not modify/send to the plugin repo or master from this executor.

Positive proposed example: authoritative contract already binds principal
absence; an uninvoked local assertion accidentally names the inventoried
present linked file. Restoring the principal path is demonstrably a
transcription restoration to the original oracle. Negative example: expected
absence or expected hash is changed to match new observed state, or SPACE
changed to LF because the patch produced LF. That changes the oracle and is
ineligible. Preserve original authoritative bytes and independent comparison
evidence; ambiguous cases stop. Even the positive case is NOT presently
eligible under invocation-only repair without separately named authority.

Any proposed eligibility is pre-observer/pre-mutation only, finite, logged,
and never retroactive. It cannot cure historical STOP or grant a new attempt.
Local closure means review and owner acceptance of the transfer-ready proposal.
Actual messaging requires fresh explicit transfer authorization identifying
destination master, exact artifact bytes and allowed request. External master
owns evaluation, revision, acceptance, implementation and release; subsequent
Yini adoption is another explicit decision. No external response is required
to close F1–F3 or local F4 readiness.

## Acceptance criteria

| AC | Demonstrable condition | Front |
|---|---|---|
| AC1 | Exact source digest and only two-field derivation; no session/role extraction or live hash binding | F1 |
| AC2 | Separate Python/Git environments; single absolute shell-free invocation; trusted identity and unchanged v1/v2 | F1 |
| AC3 | Complete capture precedes assertions; closed native/transport results reject every malformed or missing success | F1 |
| AC4 | Literal helper preserves exact bytes; principal/linked identities never conflated | F1, F3 |
| AC5 | One objective has separate grants and finite counters; fresh review and owner acceptance; STOP never replayed | F2 |
| AC6 | Current O1 projection reconciled to received owner acceptance; frozen history retained; byte option explicitly disposed | F3 |
| AC7 | Local proposal demonstrates eligible/ineligible distinction while current rule stays strict; no cross-repo effect | F4 |
| AC8 | Bootstrap has no circular dependency; evidence rungs and future integration are explicit; global closure grants nothing | All |
