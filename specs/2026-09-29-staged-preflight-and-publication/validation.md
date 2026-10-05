# Staged Preflight and Publication — Validation

## Classification and source ceiling

Ordinary local specification, provider-eval profile: CAPSULE_REQUIRED under
[local receipt policy](../../docs/operations/receipt-policy.md).
The candidate's evidence ceiling is rung 1, static/documentary. The single
live existing-v1 preflight is bounded checkout observation, not evidence that
v2 works. No product/unit test, independent review, acceptance, implementation,
Git mutation, network or publication is claimed.

Inputs inspected: root AGENTS, AgentOps workflow, executor/master/state,
roadmap post-completion section, ADRs 0001/0002, v1 spec/code and relevant
public-seam tests; installed to-spec, OPERATING-MODEL, authority-grants and
receipt-policy. Local Git 2.40 manual sections informed ls-files, config and
shared-index output choices; the proposed v2 sequence was not executed.
The incident/approval history in spec.md is owner-dispatch context, not a
new forensic audit. Prior memory supplied only boundary reminders; live
repository and grant sources control this candidate.

## Bound initial state and actual preflight

Role: specification executor. Dispatch owner:
`019f71d6-632c-7870-bfa2-89513fdeb85a`.
Physical root:
`/Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor`.
Absolute common-dir: that root plus `/.git`; principal precondition MATCH.

Three individual bootstrap commands, in order, exited 0:
`pwd -P` with login:false/no workdir, then
`GIT_OPTIONAL_LOCKS=0 git rev-parse --show-toplevel`, then
`GIT_OPTIONAL_LOCKS=0 git rev-parse --path-format=absolute --git-common-dir`.
No other Git ran before the observer.

Bound main HEAD: `9e05e3d1fd9db4cd5b710c9ab12fd3b37607d456`.
Raw index SHA-256:
`a2ae62f153742487c20196563115e9ea8539dc72f88a5ea416f8695f13b49256`.
Staged: empty. ignored_inputs: none. Five initial foreign files, all regular
mode 644, protected from edits:

| XY | Path | SHA-256 |
|---|---|---|
| ` M` | docs/agents/executor-workflow.md | c9a59a6a0466fae09cc5941b6e7b7ea63c876845bb75ea0881d1c2d17cbf5b56 |
| `??` | scripts/readonly_preflight.py | 7cc19e45f21415b5b513f4b462ca91b67deb5f228178a29da83d8281770d7059 |
| ` M` | specs/2026-09-15-executor-checkout-boundary/plan.md | 8b475d6930e98478c598c87cabec41a22f3297dc1b784a36552e708c6f9101ee |
| ` M` | specs/2026-09-17-deterministic-readonly-preflight/validation.md | 3b406c4ea2a9dc5a9f1258aabcedbaf4433f50b91e0934498aa3cf8ced995246 |
| `??` | tests/test_readonly_preflight.py | aa8cef4c2cbf5fa2d2b51fe8aa1f6b28b39aaa7d67623c71a8c4520f42cd1f02 |

Absent outputs were the five files of this directory, sorted by UTF-8 path.
The exact R2 v1 contract used work_unit_id YINI-STAGED-PREFLIGHT-SPEC and
repository_id yini-insurance-advisor. Canonical bytes (sorted keys, compact
ASCII JSON plus LF) and digest were emitted before the one invocation.
Contract SHA-256:
`a2c1ec53a99d8fe3b2897cc716bb17697f7296e352510db25f48cac433b07773`.

Python entry was principal/.venv/bin/python, physically resolved to
`/opt/homebrew/Cellar/python@3.11/3.11.12/Frameworks/Python.framework/Versions/3.11/bin/python3.11`,
version 3.11.12, SHA-256
`4df3f520de9c3b86c4ae895c68921509ff29cfb9562656f7c31ed25591d68b29`.
Git physical executable:
`/opt/homebrew/Cellar/git/2.40.0/bin/git`, SHA-256
`6dc35ae68ae1b4a83f239bb22c7d6abc36b630d7f605de9f974cc4deb6510e1b`.
The script matched its foreign-file digest above. No installation/substitution.

The caller removed inherited GIT_* names and set GIT_OPTIONAL_LOCKS=0 without
printing values. One absolute Python -B / script / verify invocation received
the emitted bytes and digest on stdin. Exit 0, canonical R6 MATCH, 12 complete
ordered exit-0 observations, exact fingerprint and successor_authority=false
were checked together. Both staged outputs were empty; before/after status
stream SHA-256 was
`08138c2a8bba829f1bb4475b2023df2d1d6ac12d17cc54d0761982ad564992e7`.
No retry, repair, fallback or repeated observer occurred.

## Current documentary checks and expected postflight

Only apply_patch writes the five new candidate documents. The final capsule
records actual final checks and hashes, avoiding self-referential hashes here.
Required checks: regular mode-644 UTF-8 files, LF/final newline, no trailing
whitespace/conflict markers, valid local links, AC-to-matrix agreement and
coherent schema/process bounds across all five docs.

Postflight must compare the full porcelain path/XY map independent of record
order: exactly initial five foreign rows plus these five new ?? rows, no other
delta. Recheck all foreign kinds/modes/digests, unchanged main/HEAD/raw index,
and zero-byte cached diff. Use expressly granted read-only Git and filesystem
checks; do not invoke the observer again or manufacture a successor grant.
A static PASS never supplies runtime evidence for future AC tests.

Source capture used bounded cat/sed/rg reads. Oversized combined displays were
completed with narrower source ranges for required content. The optional
top-level decisions directory was absent; relevant ADRs were found under
docs/adr. That discovery diagnostic is not Git failure or v2 runtime evidence.
No scoped AGENTS file was found under specs/scripts/tests/docs. No missing
required source was substituted with memory.

## Future public-seam TDD matrix — NOT_RUN

| ID | AC / requirement | Independent scenario and required assertion |
|---|---|---|
| T01 | AC1 / R1 | Existing v1 fixtures preserve literal result-v1, 12 children, empty staged enforcement; v2 input never silently enters v1 |
| T02 | AC2 / R1–R2 | Missing/extra/duplicate JSON keys, wrong types/bool, BOM, invalid UTF-8, bad raw digest and unsafe CLI all STOP before any subprocess |
| T03 | AC2 / R2 | Empty/nonempty state_kind mismatch, unsorted/duplicate staged rows, wrong XY, zero/abbreviated OIDs, absent overlap and inconsistent staged/delta relationships reject |
| T04 | AC3 / R2–R3 | Independent raw index/config bytes and literal hash vectors; wrong bytes/mode/absence/tool identity reject before subprocess |
| T05 | AC3 / R2 | M-space/A-space positive fixtures, MM/AM with distinct staged/worktree bytes, executable-mode-only delta and empty_staged all MATCH exact fingerprint |
| T06 | AC3 / R2–R3 | Right worktree hash but wrong staged blob, right staged blob but wrong index mode/OID, or right raw index but wrong canonical map must STOP |
| T07 | AC4 / R3 | Missing/extra/duplicate status, raw-diff or index entries; missing NUL, invalid record/UTF-8; reject without opening unexpected paths/blobs |
| T08 | AC4 / R3 | Stage 1/2/3 unmerged, A-intent, deleted/rename/copy, sparse/gitlink/symlink, split or assume-unchanged states fail closed; no downgrade to empty staging |
| T09 | AC4 / R3 | Permute tracked/untracked/status/index/raw-diff record order independently; same maps MATCH; preserve XY spaces and raw stream hashes |
| T10 | AC5 / R3 | Fixed argv/environment/cwd/stdin are asserted independently; no add/commit/write-tree/read-tree/update-index/hash-object -w or shell ever reaches Popen |
| T11 | AC5 / R3 | Unsafe physical paths, symlink/hardlink config/index/files, alternate/promisor storage and prohibited config keys STOP before unsafe reads/helpers |
| T12 | AC5 / R3 | File/config/index/executable/metadata/absence/HEAD or staged-map change between/during scans stops; later success remains uncalled |
| T13 | AC5 / R3–R4 | Child exit128, positive exits, signal, launch error, selector/read/wait/kill/reap faults, timeout and stream cap+1 preserve first failed step/partial evidence |
| T14 | AC5 / R3 | Input, file, scan, index entry/output, per-blob and total blob caps; bounded memory, process count and reaping; no next process after cap |
| T15 | AC6 / R4 | Exactly 18+2N complete records on MATCH; literal full result-v2, deterministic repeated bytes, exact fingerprint and successor false; invalid/partial output never PASS |
| T16 | AC6 / R1,R4 | Coverage-selected v1/v2 before invocation; unsupported mechanism/STOP cannot select another observer, ad hoc probe or changed expected contract |
| T17 | AC7 / R5 | Commit-only cannot stage; stage requires bound intended blobs; authorized post-stage capture uses changed raw hash only after map checks; ungranted capture/partial-stage generation rejects |
| T18 | AC7 / R5–R6 | Full native OID source required; short banner/padded HEX40 cannot prove capture; wrong parent/tree/paths/HEAD prevents push even after successful commit |
| T19 | AC7 / R5 | Fresh task/simple/compound/explicit bundle cases retain own grants; .git read-only routes normal named escalation, denial STOP, no automatic retry or access change |
| T20 | AC8 / R6–R7 | Adoption paths and acceptance gates coherent; semantic update precedes close when needed; push proves transport only and cannot recursively force docs/Full receipts |

T01–T15 are proposed executable observer regressions with invented fixtures.
T16–T20 are bounded documentary scenario checks; no new lifecycle state-machine
implementation is required. Mocks cover system boundaries only. Expected Git
framing, hashes, maps, result fields, exits and process counts must be specified
independently; tests do not derive their oracle from production helpers.

The intended future command is recorded in plan.md, not run in S1. Expected
RED then GREEN must be public behavior evidence; a fixture or invocation error
is a harness defect, not a RED. No real temporary Git init/stage/commit/push,
provider call or product suite is authorized by this matrix.

## Gaps, risks and next gate

V2 code, all T01–T20 outcomes, future canonical adoption, actual staged live
integration, independent review and owner acceptance are unobserved. Runtime
approval cannot be predicted by these specs. Nonatomic/ABA and bypass limits
remain. The broad conservative exclusions may stop future legitimate work;
expansion requires an explicit decision, not an implementation shortcut.

Next gate: owner decision on the exact five-file proposal, with separately
named spec acceptance and optional I1 authority. No current implementation
readiness or successor authority is claimed.

## I1 recovery execution — 2026-09-29

This section records later execution; the S1 statements above describe the
earlier specification task. The owner accepted the five S1 files and issued a
new `YINI-STAGED-PREFLIGHT-I1-RECOVERY-1` local objective bundle after the
predecessor I1 task stopped. Role: executor; dispatch owner:
`019f71d6-632c-7870-bfa2-89513fdeb85a`; route: `gpt-6-sol/high`.
Physical root and absolute common-dir matched the principal paths above in
three separate bootstrap commands, each exit 0. No checkout was reselected.
The trusted v1 script, Python and Git hashes matched the bound identities.
One v1 invocation used canonical contract bytes with SHA-256
`0e67055b46c18967abcfc747c0eacc96554d98d32829d2db07715a0b7699e880`;
it returned exit 0, valid result-v1 MATCH, twelve complete exit-0 records,
the exact twelve-row input fingerprint and `successor_authority=false`.
There was no second observer invocation.

The predecessor I1 task preserved the partial v2 candidate and reported these
native focused unittest transitions: I1.1 RED 4 tests/44 failures/exit 1,
then GREEN 4/exit 0; I1.2 RED 4/11 failures/exit 1, then accumulated GREEN
7/exit 0; I1.3 RED 4/16 failures/exit 1, then accumulated GREEN 11/exit 0;
I1.4 initial RED 6/4 failures, then accumulated GREEN 17/exit 0. Its later
13-test FailureTests run had two failures and ended `HARNESS_DEFECT` before a
complete suite. That task made no validation.md edit. These are predecessor
records, not new REDs or a renewed predecessor grant.

This recovery corrected only the named fixture and process finding. The
8193-entry fixture had counted its own `Path.touch()` setup calls in the
observer's `os.open` ledger. Clearing the ledger after setup kept all 8193
entries, the `STATE_UNSUPPORTED/paths` oracle, zero observer file opens and
zero Popen calls. Its focused run: 1 test, exit 0. The existing `wait(None)`
test then produced the intended RED: 1 test, 1 failure, exit 1; actual result
was `OBSERVATION_MISMATCH/before.common` with 2 records versus expected
`INTERNAL_DEFECT/before.root` with 1. The minimal returncode guard rejects
non-integer and out-of-native-range values before advancing. The same test
turned GREEN, 1 test/exit 0, and was extended to `None`, both booleans, 256
and -256 with the same oracle. Focused retest: 1 test/exit 0. FailureTests:
13 tests/exit 0. The final declared proportional command was
`PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest discover -s tests -p 'test*readonly_preflight.py'`:
68 tests (44 v1, 24 v2), exit 0. No later code/test edit occurred.

| Matrix | Recovery evidence and ceiling |
|---|---|
| T01 | The 44 unchanged v1 tests passed; v1/result-v1 and empty-stage rejection remain covered. |
| T02–T03 | V2 input/CLI tests exercise closed schema, digest, row relationships and unsafe paths before Popen. |
| T04–T06 | Physical fixtures and staged-mode/blob/map cases cover distinct raw index, config, index map, staged object and worktree identities. |
| T07–T09 | Invented complete Git streams cover malformed, missing, duplicate, unsupported and reordered maps; no unexpected content path is opened. |
| T10–T12 | Fixed argv/env/cwd assertions, physical/config/storage guards and between/during-scan race cases passed. |
| T13–T15 | Exit/launch/selector/read/wait/timeout/cap tests preserve first failure; 8193 inventory and blob bounds stop; literal full result, 18+2N records and repeated bytes passed. |
| T16 | Documentary PASS: spec.md coverage selection and requirements R1/R4 reject version probing or fallback after STOP; adoption remains a later grant. |
| T17 | Documentary PASS: requirements R5 and plan P1–P3 require bound stage bytes, explicit successor capture and fresh verify-index; commit-only does not stage or construct partial content. |
| T18 | Documentary PASS: requirements R6 and plan P5–P6 require native full OID plus parent/tree/path/HEAD checks before separately granted push; a banner prefix cannot substitute. |
| T19 | Documentary PASS: requirements R5 and plan P1/P4 keep fresh simple/compound/bundle grants distinct; normal named escalation may be requested for a permitted Git action, and denial stops. |
| T20 | Documentary PASS: requirements R6–R7 and plan O1 require separate adoption review/acceptance and scoped canonical updates before close; push proves transport only and creates no recursive document or Full receipt action. |

T16–T20 are source-consistency scenarios, not executable permission or
publication enforcement. This task performed no live staged-v2 integration,
independent review, owner acceptance, adoption, Git mutation, provider call,
remote readback or deployment. The evidence ceiling is local deterministic
observer tests plus documentary scenarios. New bundle counters used:
identical-invocation retries 0/2, invocation-only harness repairs 0/1,
post-validation semantic corrections 0/2. The owner-authorized fixture
correction and wait guard were primary recovery work, not charges to those
counters. The candidate proceeds only to fresh independent review after
exact postflight; this section itself grants no successor action.

## R1 findings and C1 correction — 2026-09-29

R1 task `01a0ef52-a7df-76d0-a947-c53ba63d7e8d` returned
`FULL CANDIDATE_FINDING` with two P2 findings. The owner then granted
`YINI-STAGED-PREFLIGHT-C1`, role executor, dispatch owner
`019f71d6-632c-7870-bfa2-89513fdeb85a`, route `gpt-6.1-sol/high`,
with separate CORRECTION-IMPLEMENT and CORRECTION-VALIDATE authorities.
The write allowlist is only the v2 script, v2 tests and this document.
The oracle/fixture changes below are explicitly authorized primary semantic
correction work, not invocation-only harness repairs.

Principal bootstrap: the three separate ordered commands (`pwd -P`, Git
show-toplevel, absolute common-dir) each exited 0 and matched the required
physical root/common-dir. Filesystem-only verification matched the trusted
v1 script and absolute Python/Git identities recorded above. All twelve
starting delta hashes, regular/single-link mode-644 identities matched the
new grant, including the protected gpt-6.1 routing amendment. The exact v1
R2 contract used work_unit_id `YINI-STAGED-PREFLIGHT-C1`, empty staged/absent
arrays, ignored_inputs `none`, and the bound twelve-row map. Its canonical
bytes were emitted before invocation, SHA-256
`2a49c84de0fe35fb4def772a8e5d41e1bb0beb6dfe0586df2401a68aa06bc932`.
The single absolute-runtime `-B` v1 verify invocation, shell=False with
sanitized inherited GIT_* names, returned exit 0, complete canonical R6 MATCH,
twelve ordered complete exit-0 records, the exact input fingerprint and
successor_authority=false. No second observer was used. The native HEAD tree
observation was `348df7a93b51f87b5ad9bc389b98543fe92764b6`, as bound.

P2-1: the old Unicode-control/normalized-duplicate test used an index-map
digest that disagreed with the supplied stream, so its GREEN did not prove
path rejection. C1 now retains the valid staged entry, includes the forbidden
metadata in both streams, and binds the exact full UTF-8-sorted map digest
independently of production parsing. Focused RED: one test, two subcase
failures, exit 1; both U+0085 and the NFC-equivalent café/cafe-combining-accent
pair incorrectly returned MATCH with twenty processes. Minimum correction:
reject Unicode Cc controls and detect NFC-normalized name collisions before
inserting rows, while preserving original path strings. Focused GREEN:
one test, exit 0; both cases STOP/OBSERVATION_MISMATCH/3 at before.entries,
seven processes, fingerprint null, and no unexpected content opens.

P2-2: a valid fixture with 128 long ASCII absent paths has input within
262144 bytes but would produce a MATCH envelope exceeding that output cap.
The fixture uses bounded segments and absent first ancestors; it creates no
long physical paths. Independent expected output preserves all twenty
successful process records. Focused RED: one test, two public-seam failures,
exit 1; verify and main both returned INTERNAL_DEFECT/70 but retained
outcome=MATCH and a non-null fingerprint. Minimum correction: _stop always
sets STOP and clears the fingerprint. main also checks canonical output size
before delivery and never emits an oversized envelope. Focused GREEN:
one test, exit 0; both seams return the exact deterministic STOP envelope,
INTERNAL_DEFECT/70 at result, fingerprint null, successor_authority=false,
all twenty process records, canonical JSON plus LF within 262144 bytes.
The process evidence and R4 public field/reason semantics remain intact.

Each focused invocation used the absolute principal `.venv/bin/python -B -m
unittest discover -s tests -p 'test*readonly_preflight.py'`, with `-k
metadata_unicode` or `-k oversized_match`, PYTHONDONTWRITEBYTECODE=1 and
sanitized inherited GIT_* names except GIT_OPTIONAL_LOCKS=0. One declared
final proportional invocation used that command without -k: **69 tests
(44 unchanged v1, 25 v2), exit 0**. No code/test edits followed that suite.
Logs and exact bootstrap contract/result are retained at
`/private/tmp/yini-staged-c1/` for this execution; that temporary location is
not a durable receipt register.

| Matrix | Explicit correction to the historical recovery claims |
|---|---|
| T07 | The prior 68-test GREEN did not establish Unicode-control or normalized-duplicate rejection. C1's corrected full-stream oracle now proves both named cases reject at before.entries without unexpected content reads. |
| T08 | Existing unsupported tag/stage/mode cases remain regression evidence; they did not imply the omitted metadata guards. All remain GREEN in C1's final suite. |
| T09 | Existing map-order permutation evidence remains valid. C1 adds normalized-name uniqueness checks without rewriting original index paths or treating distinct normalized collisions as reorderings. |
| T15 | The prior 68-test GREEN did not prove the output-size/fingerprint invariant for large legal contracts. C1 now exercises both verify and main with a legal oversized-MATCH scenario and exact bounded STOP output retaining process evidence. |

Historical S1/I1 evidence above is preserved; its broad claims are limited by
these explicit R1 findings and C1 observations. No result is retrospectively
reported as a RED that was not observed. C1 counters: identical-invocation
retries 0/2, invocation/environment-only harness repairs 0/1,
semantic corrections after first complete validation 0/2. The two named P2
cycles were primary authorized work; expected TDD REDs consume none of those
contingency counters. Final suite invocations: 1/1. Observer invocations: 1/1.

The terminal capsule records the final exact three output hashes, nine
protected hashes/modes, twelve-row porcelain map, unchanged main/HEAD/tree/raw
index, empty staging and whitespace checks. Evidence ceiling: local
deterministic public-seam tests and bounded read-only checkout observations.
Live staged-v2 integration, product tests, provider/network, independent
review, acceptance, adoption, Git writes and publication were not performed.
Nonatomic/ABA and trusted-runtime assumptions remain. The next gate is fresh
independent differential review through master under the owner's separate
grant; C1 does not dispatch that task or create successor authority.

## WorktreeConfig amendment evidence — 2026-09-30

Candidate work unit: `YINI-WORKTREECONFIG-SPEC-AMENDMENT-RECOVERY-1`.
This appendix preserves all S1/I1/C1 history above and the separately accepted
C1/pending O1 state recorded by execution-state.md. Ordinary documentary
candidate: CAPSULE_REQUIRED, rung 1. It performs no implementation, formal
review, owner acceptance, product suite, config mutation or Git write.

The renewal follows a predecessor extraction HARNESS_DEFECT, not a candidate
defect. One mechanical repair uses the contract supplied directly in the
dispatch, verifies its raw SHA-256
`1933f9ba913d364cbcbff630808c2ee5f2607f10038459e94b4bbb3a0c103298`,
then changes only work_unit_id programmatically and serializes sorted compact
ASCII JSON plus LF. No session-file parser, role=user filter or reconstructed
manual map was used. Repair accounting: 1/1 for this authorized replacement;
observer invocation 1/1; observer retries 0; mutation retries 0.
Oversized source display was completed through bounded read-only ranges;
capture completion is not another extraction repair.

Three separate ordered bootstrap calls each exited 0 and matched principal
root/common-dir. Physical Python, Git and v1 script matched the dispatch
digests. All fifteen initial delta identities matched; three config hashes,
modes and sizes matched, and principal config.worktree was absent.
Configuration values were not inspected or emitted; the extension/format
diagnosis is supplied evidence. Local Git 2.40 git-config manual sections on
--file, --type and extensions.worktreeConfig informed the proposed commands;
no new live config-value probe or network lookup was performed.

Derived contract SHA-256:
`8099315b540007e31ee4318e7ac18ef7fe0ded775787dd5c054f3bd02b24f1a8`.
One verified physical Python -B/script/verify subprocess, shell=False, received
those bytes/digest with inherited GIT_* removed except GIT_OPTIONAL_LOCKS=0.
Observed exit 0 and a complete canonical result-v1 MATCH: exact closed
envelope/fingerprint, twelve ordered complete exit-0 records, zero-byte staged
streams and successor_authority=false. No second verify invocation.
Native HEAD tree matched `348df7a93b51f87b5ad9bc389b98543fe92764b6`;
HEAD/index remain the bound identities recorded in the terminal capsule.

Only the five current specs may change, through apply_patch. Final focal checks
must prove UTF-8/LF/whitespace/conflict/link integrity, WAC/matrix and version/
process-count agreement, append-only preservation of original spec text,
unchanged ten protected delta identities, config identity/absence and exact
main/HEAD/tree/raw-index/empty-staged/fifteen-row status map. The terminal
capsule reports actual outcomes and all fifteen successor hashes/modes for
programmatic transfer; this paragraph is the check contract, not a claim that
future implementation tests ran. No atime or global stat_result comparison.

## WorktreeConfig public-seam matrix — NOT_RUN

Every W01–W09 executable scenario must cover both public verify and CLI main,
with filesystem/process boundaries patched only; expected results, digests,
argv and counts are independent of production helpers. W10 is documentary.
Fixtures are invented, never copies of local config or linked-worktree values.

| ID | AC | Future required assertion |
|---|---|---|
| W01 | WAC1 | V1/result-v1 unchanged (12 records); v2/result-v2 unchanged (18+2N), still rejects every extensions.* including worktreeConfig; v3 never falls back or coerces old input |
| W02 | WAC2 | Exact v3 fields; missing/extra/duplicate nested keys, bool-as-int, float/string format, numeric/string extension, present config shape and schema/result mixing reject before Popen |
| W03 | WAC2, WAC5 | Format 0 with absent/false/true extension and principal absence matches; empty/partial/mode-only staged cases retain distinct identities; literal fingerprints and 20+2B+2N counts for N=0 and N=32 |
| W04 | WAC3 | Initial regular-empty/nonempty/hardlink/directory/special config.worktree rejected without opening it; dangling symlink/unsafe ancestor rejected; common-config symlink/hardlink rejected before config child |
| W05 | WAC3 | Duplicate protected config keys (equal/conflicting/case variants), missing format, nonzero format, malformed bool and malformed NUL/value streams stop at exact first step; true/yes/on/1 and false/no/off/0 canonicalize via Git bool fixtures, implicit/empty values use independently pinned Git framing |
| W06 | WAC3 | Includes/includeIf, other extensions/subsection lookalikes, filters/promisor/partialclone/core.worktree/sparse/split, linked .git file and prior unsafe storage all remain rejected; no linked config opens or values |
| W07 | WAC4 | Config-worktree appearance after first scan/between passes/final scan; config inode/mode/content/metadata or normalized-state change; guard after config parsing prevents next dependent child; later success never heals failure; atime-only changes do not create false drift |
| W08 | WAC4 | Exact explicit-file/no-includes argv, fixed environment, config-before-root ordering, absent-key getter omission, 86-child maximum, three full/two config scan caps, stream cap+1, timeout/reap and exit propagation; no mutator/helper/network |
| W09 | WAC5 | Exact canonical result-v3, strict fields/types, ordered complete records, STOP/null fingerprint/successor false, partial process evidence, deterministic repeated bytes and oversized-result invariant at both seams |
| W10 | WAC6 | Candidate versus acceptance/implementation/adoption clear; C1/O1 history unchanged; no config disablement, origin attribution, post-STOP version switch, publication grant or linked/present-file scope expansion |

W01–W10 are NOT_RUN for the proposed v3 behavior. The existing 69-test C1
record supplies historical v1/v2 evidence only, not v3 coverage or a new suite
execution. No runtime hard enforcement, atomic snapshot, integration,
provider, remote, deployment or acceptance claim follows from this amendment.

## F3 prospective O1 evidence clarification — 2026-10-02

The WorktreeConfig evidence appendix's C1/pending O1 projection records its
historical state. The current received O1 owner acceptance follows independent
FULL PASS, with provenance in audit `01a0f475-4599-7aa0-ad68-83b0286d722f`,
final item `msg_03cd4fae84e8eb02016abd8ff1bd3087d19738ea1521fbf6eb`, native
review postflight `exec-b1ed1961-f902-4224-908a-e494f71ad020`, exit 0.
The full review thread ID is unavailable. See the
[dated specification clarification](spec.md#f3-prospective-o1-projection-clarification--2026-10-02)
and [current execution state](../../docs/operations/execution-state.md).

All preceding bytes and frozen S1/I1/C1/W-S1 receipts remain unchanged.
The owner selected retention of the known tasks.md LF under R5; its protected
SHA-256 remains `c0db211aea31ccaadc9d5e4c5049460eabddc2333a0a254859514c7230edbc80`.
The earlier SPACE-preserving oracle did not pass. This prospective disposition
neither converts that failure nor resumes its grant. F3 scratch preparation
does not establish repository application, independent review or acceptance.
V3/W01–W10 remain future NOT_RUN evidence; publication and F4 remain pending.

## W-I1 authorized implementation evidence — 2026-10-03

This appendix records the owner's fresh W-I1 local objective, work unit
`YINI-W3-IMPLEMENTATION-1`, separately named implementation and affected
validation authorities, executor role, dispatch owner
`019f71d6-632c-7870-bfa2-89513fdeb85a`, route `gpt-6.1-sol/high`.
The owner selected the exact W1–W4/WAC1–WAC6 absent-only design and finite
continuity in this task. Earlier PROPOSED/NOT_RUN headings and receipts remain
historical; this authorization does not accept old runs or the new candidate.
Only the staged observer, its existing test file and this append-only evidence
document are editable. Independent W-R1 review, owner acceptance, four-path
W-O1 adoption and Git publication remain separate gates.

The three individual bootstrap calls matched the principal physical root and
absolute common-dir, each exit 0. Separate filesystem hash reads matched the
bound Python, Git, unchanged transport and v1 observer before runtime use.
The immutable source/request files were
`/private/tmp/yini-w3-source-20261003.json` and
`/private/tmp/yini-w3-request-20261003.json`; their SHA-256 values were
`d66dbbf966ea6a37723f198a7391d457f5a58b66e25751742d51b666d8389eeb`
and `fe360b4de9acba7870b4e5dd456914025d348e6fa04745f06b108f99b980bd06`.
The exact absolute Python -B execution_contract.py `prepare` invocation
returned PREPARED/0. Only then, one `invoke` with the same stdin request
returned complete MATCH/0, the exact 24-row result-v1 fingerprint, twelve
complete exit-0 observer records and successor_authority=false in both
envelopes. Transport child environment was sanitized. No second observer or
live v2/v3 observer invocation occurred.

Before repository edits, this document's entire historical prefix was
28,641 bytes, SHA-256
`887ddaae81837778b1b404d63ff4a3605fc3c8b102428e1bb57826ca6f2771dd`.
A byte-for-byte snapshot is retained at
`/private/tmp/yini-w-i1-validation-prefix-20261003.md`; it is task scratch,
not a new durable receipt register. All writes used apply_patch. The initial
common-config SHA-256 was
`7b30c0127e80eb0436d20a6d76c5ec2866604c8f6d40088cb8e30ab0beaf3af9`;
principal config.worktree was lexists-false. Configuration values were not
read or emitted by task probes; fixtures contain invented configuration only.

### Actual vertical transitions and regression evidence

All commands below used the verified physical Python 3.11.12 executable
`/opt/homebrew/Cellar/python@3.11/3.11.12/Frameworks/Python.framework/Versions/3.11/bin/python3.11`
with `-B -m unittest discover -s tests -p
'test_staged_readonly_preflight.py'`, adding the named literal `-k` selector.
No real Git subprocess is launched by these tests: public verify/main exercise
real observer logic with only filesystem/process/time boundaries patched.
Expected fields, streams, hashes, argv, counts and serialized results are
independently specified in the test file; private schema/comparison/result
helpers are never stubbed.

| Selector | Observed RED and minimal GREEN |
|---|---|
| v3_valid_schema | One test, two seam failures, exit 1: v2 CONTRACT_INVALID/input instead of v3 ENVIRONMENT_UNSUPPORTED/environment. Closed v3 branch added; same test GREEN, exit 0. |
| v3_present_config | One test, twelve seam/kind failures, exit 1: present empty/nonempty/directory/FIFO/symlink incorrectly advanced; hardlink classification was wrong. Initial absence guard added without opening the leaf; same test GREEN, exit 0. |
| v3_true_exact | One test, two seam failures, exit 1: first v2 root probe mismatched the v3 names stream. Fixed explicit-file config names/int/bool probes, physical config guard, sequence/count/fingerprint added; literal full-result/argv/five-scan test GREEN, exit 0. |
| v3_later_common | One test, four seam/timing failures, exit 1: late common-config symlink returned PATH_UNSAFE/2 rather than OBSERVATION_DRIFT/3. V3-only later-config classification corrected; same test GREEN, exit 0. The guard-timing subcase was already GREEN and is regression evidence. |

All further new cases were observed already GREEN and are reported as
regressions, never fabricated REDs. Focused runs: V3PhysicalTests 5 tests,
V3FailureTests 6 tests, v3_legacy 1 test, V3 25 tests, and the final strict
null/boolean fingerprint check v3_absent_false 1 test; all exit 0.
Additional accumulated V3 run earlier passed 11 tests. Expected TDD REDs
were primary transitions, not contingency correction cycles.

### W01–W10 actual matrix

| ID | Actual evidence and applicable criteria |
|---|---|
| W01 | v3_legacy pins complete v1 (12 records) and v2 (20 for N=1) results at both seams, old-schema/staged rejection, and v2 worktreeConfig/other-extension rejection. Final suite preserves all 44 v1 and 25 legacy v2 tests. WAC1. |
| W02 | v3_closed_fields and v3_input cover missing/extra fields, nested/top-level duplicates, bool/float/string format, numeric/string extension, present shape, schema/result mixing and inherited guards before Popen at both seams. WAC2. |
| W03 | v3_absent_false covers null/false/true, N=0, full/partial additions/modifications and mode-only state, exact typed fingerprints/bytes; v3_thirty_two proves N=32, 84/86 records and 64 per-path blob probes despite repeated OIDs. Both seams. WAC2/WAC5. |
| W04 | v3_present_config and v3_initial_unsafe cover empty/nonempty/hardlinked/directory/FIFO config.worktree, dangling symlink, unsafe common ancestor and common-config symlink/hardlink without opening the forbidden leaf or launching children. Both seams. WAC3. |
| W05 | v3_config_name, v3_duplicate_equal, v3_typed_format and v3_documented_git cover protected duplicate/case/cardinality checks, equal/conflicting physical values, malformed names/value framing, format nonzero, normalized boolean mismatch and Git exit128. Typed boolean fixtures independently pin true/yes/on/1/implicit and false/no/off/0/empty from local Git 2.40 git-config(1) Values; no live conversion claim. Both seams. WAC3. |
| W06 | v3_config_name preserves include/includeIf, other/subsection extensions, filters, promisor/partialclone, core.worktree/sparse/split rejection. v3_initial_unsafe preserves linked .git and unsafe storage rejection; v3_does_not_open proves existing linked config is untouched. v3_remaining_index preserves unmerged/tag/mode/status/object exclusions; v3_unicode retains corrected C1 metadata rejection with exact full-map binding. Both seams. WAC3. |
| W07 | v3_physical_drift, v3_later_common and v3_nanosecond cover config.worktree appearance, late symlink, common-config content/mode/inode/mtime/link/absence drift at guards/between/final scans, exact first step, no following dependent probe, integer one-nanosecond mtime/ctime change and atime-only MATCH. Name multiset drift stops immediately at after.config.names; valid changed bool stops at after.config.worktree. Both seams. WAC4. |
| W08 | v3_true_exact pins explicit-file/no-includes argv, fixed environment, cwd/stdin/shell, config-before-root order and three full/two config-only reads. v3_absent_false pins getter omission. v3_thirty_two pins 86 maximum. v3_three_full measures exactly 224 MiB and rejects full-scan cap+1; v3_config_scan covers file/guard/directory bounds. v3_stream covers stream/index/blob cap+1 and per-pass blob aggregate without deduplication; v3_exits/v3_selector cover native exits/signals, launch, selector/read/wait faults, timeout and kill/reap failure with partial evidence. Both seams. WAC4. |
| W09 | v3_expected independent full-envelope fixture pins canonical result-v3, strict fingerprint types, ordered complete records, hashes/lengths, no raw config/output and successor false. v3_exits and v3_selector pin closed STOP/null fingerprint/partial evidence. v3_oversized pins exact bounded STOP for legal oversized-MATCH input and repeated identical bytes; C1 v2 regression also remains. Both seams. WAC5. |
| W10 | Documentary source-consistency PASS against the five spec files: absent-only principal scope, no config disablement/origin attribution, preserved historical C1/O1 meaning, no post-STOP switch, and separate implementation/review/owner/adoption/publication authorities. Current task performs W-I1 only; it does not activate canonical v3 selection. This is documentary evidence, not runtime authority enforcement or independent review. WAC6. |

The one declared final observer suite was the absolute physical Python
`-B -m unittest discover -s tests -p 'test*readonly_preflight.py'`:
**94 tests (44 unchanged v1, 25 legacy v2, 25 new), exit 0**, 9.040 seconds
as native test output. No code/test edit followed that suite.

The separately authorized routing-test gap check used the existing principal
`.venv/bin/python` symlink, resolving to the same bound Python executable/hash.
Version 3.11.12, principal venv prefix and pytest availability were inspected
before tests; no venv changes or installation occurred. Source inspection
confirmed invented tmp_path repositories and read-only validator subprocesses.
One exact invocation,
`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor/.venv/bin/python -B -m pytest -p no:cacheprovider tests/test_validate_master_control.py`,
returned **88 passed, exit 0**. It is separate routing evidence, not a
substitute runtime for the W-series tests. The transport import seam is
unaffected; its separate regression suite was not run. Application/release,
live v2/v3 integration, provider/network and deployment checks were not run.

Contingency counters consumed: identical transient retries 0/2,
invocation/environment repairs 0/1, semantic correction cycles after first
complete candidate validation 0/2. Final observer suite 1/1; initial observer
invoke 1/1; routing pytest 1/1. Evidence ceiling: rung 2 local deterministic
public-seam tests plus documentary consistency and bounded checkout evidence.
Nonatomic/ABA races, exclusive checkout use and trusted tools remain limits.
MATCH neither authenticates authority nor establishes acceptance/readiness.

The native terminal postflight item owns complete machine JSON with all 24
successor rows and exact hashes/modes, three changed identities, protected-row
checks, prefix equality and observed Git/config state; it avoids hand-copied
hash manifests. This appendix grants no successor. Return is eligible only
after that postflight passes, at READY_FOR_INDEPENDENT_REVIEW for fresh W-R1.
