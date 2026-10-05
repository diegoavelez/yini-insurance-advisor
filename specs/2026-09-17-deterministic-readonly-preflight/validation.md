# Deterministic Read-Only Preflight — Validation

## Evidence classification

Ordinary local documentary specification, provider-eval profile:
`CAPSULE_REQUIRED` under the [local receipt policy](../../docs/operations/receipt-policy.md).
Current ceiling: static documentary evidence only. This task does not re-open
forensic diagnosis. The incident description in spec.md is supplied context;
no original command, session history, memory search or mutation was replayed.

## Starting observation

Physical cwd/root:
`/Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor`.
Absolute common-dir: the same path plus `/.git`. Both matched the grant after
first-call `pwd -P` with `login:false` and no workdir override.
Branch `main`; HEAD `9f13f185be2edaf82122f8e401bd6b6f76c0ce25`.
Raw index SHA-256:
`cb3492d1806f9ab78eace0ac92e0697d062a38f9759001346353c90f44d1ae51`.
Cached name-status output empty. These are historical observations for this
pass, not semantic state or authority for a later task.

The entire initial porcelain map contained exactly these five owner-permitted
foreign regular files, all mode `644`; every digest matched before editing:

| Path | XY | SHA-256 |
|---|---|---|
| `docs/operations/execution-state.md` | ` M` | `b57ee0c9136457974267d10663ba4651c5d206881a2d2fd24dd8474aff1e7ed0` |
| `specs/roadmap.md` | ` M` | `9d6283cfa7243990da1a10aa38adc7d90844295d3eb570e35276cdf8abd55c04` |
| `specs/2026-09-15-operational-readiness/requirements.md` | `??` | `f9c391eef73b9cb2e73e95c8ec90b492376274cc29ded1262ee0a51a8f20de77` |
| `specs/2026-09-15-operational-readiness/plan.md` | `??` | `72efa04c6f10fef658cfee15ccbf80af086c7fbf7585f583256e2c16150a409e` |
| `specs/2026-09-15-operational-readiness/validation.md` | `??` | `45fbb30eaf189d3959b7cc3cb8b7e1b07195f5502b66008e5422f764c4357571` |

The new spec directory was absent. Proposed script/test paths were also
observed absent. No scoped AGENTS.md was present in specs/scripts/tests.

## Current checks and capture accounting

Executed starting commands individually, each preserving its exit: `pwd -P`;
the six authorized Git observations (`rev-parse --show-toplevel`,
`rev-parse --path-format=absolute --git-common-dir`,
`symbolic-ref --quiet --short HEAD`, `rev-parse HEAD`,
`status --porcelain=v1 -z --untracked-files=all`,
`diff --cached --name-status`), all with `GIT_OPTIONAL_LOCKS=0`;
`shasum -a 256 .git/index`; Python standard-library mode/hash/absence reads.
Every starting command exited 0 and the complete returned fields matched.

Source reads used cat/sed/wc and bounded repository file discovery, with no
symlink-following search or access to excluded data. A broad specs filename
listing and a batched display were truncated; the listing was not used as
complete-inventory evidence. Required source content was completed by bounded
explicit-path reads, including lessons lines 35–100 and 101–134. No real tool
error or state mismatch was converted into success. Plugin source was read
only, never executed/imported or patched. Its repository restriction is a
static finding, not evidence of its operational behavior in Yini.

The first static pass checked all five regular mode-644 files, 12 local links,
UTF-8, final newlines, trailing whitespace and conflict markers with zero
findings. One bounded documentary adjustment then clarified the three file
scans versus two Git observations; the same static checks are repeated after
that edit. Selected final checks additionally cover the exact delta map,
root/common-dir/main/HEAD/empty staging, foreign kinds/modes/digests and raw
index rehash. The final capsule records
actual outcomes and all five candidate hashes after the last edit. Expected
delta is exactly ten paths: two ` M` and eight `??`; only five new files belong
to this task. No final self-hash is embedded in a candidate document.

Skipped intentionally: implementation, unit/TDD execution, pytest, product
tests, make test-release, formal independent review, live mechanism execution,
Git mutations, network/provider checks, installation and operational adoption.

## Future regression matrix — all unexecuted

| Requirement | Independent fixture / public-seam assertion |
|---|---|
| R1 | main receives denied verbs, raw argv, semicolon/pipe/backtick/$() text and extra args; STOP and zero process calls; importing module has zero I/O |
| R2 | Wrong root/repo ID, missing/extra/duplicate keys, bool/type confusion, bad digest/raw whitespace mismatch, oversized/invalid UTF-8/BOM/trailing JSON, unknown fields: failure before subprocess |
| R2 | Absolute/traversal/repeated-separator/control/shell paths, symlink ancestor/leaf/dangling absent, hardlink, nonregular file, `.git` indirection/worktree, forbidden data path, missing index: zero process calls |
| R2–R3 | Inherited GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE/GIT_CONFIG_COUNT and all other disallowed GIT_* rejected; fixed environment/argv never carries redirects, loader vars, helpers or raw contract text |
| R3 | Bytecode enabled, executable mismatch, per-file/aggregate limit, timeout and cap+1 output each STOP; bounded reader cannot allocate an unlimited stream or start next process |
| R4 | Raw file bytes `abc` have literal SHA-256 `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`; assert no tree/index-writing argv, no Git invocation for hashing, no file change |
| R4 | Mode/hash/absence/index mismatch; wrong branch/HEAD/root/common-dir; nonempty staged output; all fail at their first step |
| R4 | Nonempty tracked-first plus nested untracked fixture matches canonical sorted map; leading XY space remains; reorder input records without changing map does not create drift |
| R4 | Missing/extra/duplicate/unsafe path, unsupported XY, directory summary, rename/copy pair, malformed UTF-8 or missing final NUL stop before subsequent probes |
| R4 | Changes to executable/index/file/hash/mode/absence/metadata between or during reads stop; no later MATCH heals them; unexpected paths are never opened |
| R5 | First failed Git child exit 128 is preserved in result and main return; a queued success remains uncalled; signal/launch/timeout/overflow retain correct reason and exit |
| R6 | Positive nonempty invented candidate yields full exact envelope, 12 ordered process records, no unauthorized extra keys or raw output, false successor authority and byte-identical repeat JSON |
| R6–R7 | Partial/failed/malformed output never supports MATCH; canonical handoff procedure keeps bootstrap bounded, mechanism mandatory only after adoption, and subsequent authority separate |

Expected digests, complete argv tuples, process counts and result envelopes
must be authored independently rather than derived by the production helper
under test. Public main/verify remain real; only subprocess/filesystem system
boundaries are mocked. No real mutator is run, including inside temporary Git
repositories, without a future explicit owner grant.

## Residual risk and next gate

Static coherence cannot prove future implementation compliance. Normal-shell
bypass and filesystem race limits remain explicit. The mechanism excludes
submodule internals and relevant ignored inputs; tasks needing that coverage
must stop. Bootstrap remains a narrowly authorized procedural exception.
Recommend owner spec acceptance plus a separately named bounded I1 TDD grant,
then independent review and owner acceptance before operational adoption.

## I1 implementation attempt — 2026-09-17

Role `executor implementation`; dispatch owner
`019f71d6-632c-7870-bfa2-89513fdeb85a`. The owner-authorized I1 attempt
observed the principal physical checkout, common-dir, `main`, HEAD
`5c39875f8a6e75e5e01001126fd3cafb86dacb19`, raw index SHA-256
`623e67bff98d304acd7c6e4f5d988846fd2c83b97c37f8968a09cfc36868c91c`,
empty staging, and the five foreign files above with their declared hashes and
mode `644` before editing. The selected `.venv/bin/python` existed.

Cycle 1 RED: the selected unittest discovery command exited 1 because the
new public module did not exist. Cycle 1 GREEN: after adding the module, the
same command exited 0; three tests passed for denied CLI commands, malformed
contracts and inherited Git/bytecode guards. These tests do not establish the
remaining cycle-1 matrix.

Cycle 2 attempted RED: the selected command exited 1 with four failed
assertions. The cases intended to reach physical index/file checks instead
received `ENVIRONMENT_UNSUPPORTED` at the earlier environment guard. A
read-only probe found the inherited name `GIT_PAGER`; its value was not read
or recorded. This is an unexpected fixture/environment interaction, not an
intended physical-hash RED. The attempt stopped without changing the fixture,
relaxing the guard, continuing to GREEN, or starting cycles 3–4. The current
module has only partial schema/environment behavior and a deliberate
`CHECKOUT_UNSUPPORTED` placeholder. No readiness, independent-review PASS,
operational adoption, live integration, Git mutation, provider execution, or
successor authority is claimed. Owner disposition and a fresh scoped task are
required for any repair or continuation.

## I2 repair attempt — historical receipt retained

The fresh I2 task repaired the inherited `GIT_PAGER` test-environment
interaction and kept the production module unchanged during that repair.
Cycle 2 then reached its intended physical-index/file RED and passed after
minimal implementation. The next run reached a different fixture defect:
`test_raw_index_and_file_hash_before_any_git` used a bare `Popen` mock with no
defined streams or return lifecycle. Its expected first-step assertion instead
saw `INTERNAL_DEFECT`; the task stopped at six tests, five passing and one
failing. I2 made no second repair and claimed no completed matrix or review
readiness. Its final candidate hashes were script
`847a00b7f3151b8752b636c3ee5593631516138d762fe895b174ac7822abe790`,
test `dfc49eed30ca3d5683574f51e8ee0255fd31d9e3a7fb0da7d7cb4b09855868d3`,
and this validation file
`3a25b221567a5f67a12c666cfc5e676fcfbb533d556ed8efd4ceccb2d60792ab`.
This paragraph records I2's stop and does not convert its failed run to PASS.

## I3 bounded fixture repair and TDD continuation — 2026-09-17

Role `executor`; dispatch owner `019f71d6-632c-7870-bfa2-89513fdeb85a`.
The fresh owner grant bound the principal physical checkout and common-dir,
`main`, HEAD `5c39875f8a6e75e5e01001126fd3cafb86dacb19`, raw index hash
`623e67bff98d304acd7c6e4f5d988846fd2c83b97c37f8968a09cfc36868c91c`,
empty staging, eight exact regular mode-644 deltas, and writes to only this
file, the script, and its test. The initial branch, HEAD, index, staging,
porcelain inventory, file hashes and modes matched that grant. The five
foreign files in the starting table remained outside the edit scope.

H2 repaired the process fixture by replacing the bare `Popen` mock with a
bounded `FakeProcess` providing real pipe streams, a return code, wait/poll,
kill state and stream closure by the observer. The inherited test now asserts
the actual root stream record and its subsequent first failed scalar step.
The selected unittest command passed 6/6; production SHA-256 remained
`847a00b7f3151b8752b636c3ee5593631516138d762fe895b174ac7822abe790`
through H2. This is a fixture repair, not a retroactive I2 PASS.

Continuation used the public `verify`/`main` seams and only OS/process/time
boundaries as fakes. Seven new behavior increments had intended REDs followed by
GREENs: full two-observation MATCH (70→0), distinct bound-executable digest
reason, distinct missing-executable reason, disappearance classified as drift,
the `after.paths` and initial `paths` step IDs, and the already-exited child
race during timeout cleanup. The earlier exit-128 case
was already green with a concrete `FakeProcess`; additional negative cases
that existing code already satisfied were retained as regression coverage.
The final selected command passed 29/29 tests. No failed harness invocation
was reclassified as an intended RED.
The successive intended RED/GREEN unittest totals were 7/7, 8/8, 17/17,
18/18, 19/19, 20/20 and 28/28; other runs added already-green
negative coverage, including the later index, executable, mode, absence and
nonregular-file cases. Every run used the selected `.venv/bin/python -B -m unittest
discover -s tests -p test_readonly_preflight.py` with bytecode disabled.

The executed unit matrix covers R1 denied CLI verbs, shell text, extra argv,
bounded stdin and inert import; R2 raw hash/JSON/schema/path rejects, physical
symlink/hardlink/index/worktree guards and exact bytes/modes; R3 inherited Git
variables, bytecode, complete fixed argv/environment, file/scan limits,
timeout, launch, signal and cap+1 capture; R4 literal `abc` digest, two scans
plus final scan, status map ordering and malformed/unexpected records, scalar
and staged mismatch, metadata and file drift, and unopened unexpected paths;
R5 preserved child 128 and no queued successor; and R6 exact successful result
envelope, 12 ordered process records, false successor authority and identical
repeat JSON. Procedural R7 adoption remains unperformed by this task.

Evidence ceiling: rung 2, local deterministic unit tests with invented data.
No live repository invocation of the new observer, independent review,
acceptance, adoption, Git mutation, provider run, or later authority is
claimed. The existing spec's non-atomic snapshot and unsupported-input limits
still apply. The next gate is fresh independent review of the exact candidate
under master dispatch, followed by owner disposition.

## C1 fixture repair and bounded correction continuation — 2026-09-17

Role `executor`; dispatch owner `019f71d6-632c-7870-bfa2-89513fdeb85a`.
The received task matched the principal physical checkout and common-dir,
`main`, HEAD `5c39875f8a6e75e5e01001126fd3cafb86dacb19`, raw index SHA-256
`623e67bff98d304acd7c6e4f5d988846fd2c83b97c37f8968a09cfc36868c91c`,
empty staging and the eight declared mode-644 deltas. The five foreign paths
remained outside the edit scope. This correction follows the separate C1 stop;
it does not reclassify that run as a candidate RED.

H1 changed only the test fixture's `os.read` interception. It routed reads for
the created fake child's stdout descriptor to the injected failure and
delegated other descriptors to the preserved real `os.read`. A regular-file
read was checked under the patch before the negative case. The production
script retained SHA-256
`614af2afdfe3482babd1682eec55d16075820e19a14327275394759dfa23ee81`
through H1. The selected unittest command then ran 32 tests and failed on the
intended capture behavior: `INTERNAL_DEFECT` was reported at `result` instead
of `before.root`, with no preserved partial process record. The minimum
production change recorded and reaped the failing child at that step; 32/32
then passed.

Two further vertical corrections had intended REDs followed by GREENs. A
selector-registration error paired with a failed `kill` initially lost the
process step at `result`; bounded `wait` is now attempted and the incomplete
record remains attached to `before.root` (33/33). A child whose `wait` and
reap both time out initially lost the captured bytes and record; recording
before reap preserved the three captured `abc` bytes and incomplete flag
(34/34). Each test asserted a single launched child and no successor.

Additional negative cases were already green when first run and are retained
as regression coverage, not claimed as RED/GREEN cycles: closed nested Git and
delta objects, duplicate/unsorted/overlapping paths, CLI error envelope and
stdout delivery failure, selector error and timeout, deadline during pipe
capture, positive child exit codes 1/7/255, and OS `wait` failure. The final
selected command was
`PYTHONDONTWRITEBYTECODE=1 /Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor/.venv/bin/python -B -m unittest discover -s tests -p test_readonly_preflight.py`;
40/40 local unit tests passed. No live observer invocation, independent review,
owner acceptance, adoption, Git mutation, provider run, or later gate was
performed. Evidence ceiling remains rung 2, local deterministic tests with
invented data; non-atomic filesystem snapshots and unsupported inputs remain
the specified limits. The candidate is ready for a separately dispatched
independent differential review and owner disposition.

## C3 R3 physical-guard correction and CLI-envelope regression — 2026-09-17

Role `executor`; dispatch owner `019f71d6-632c-7870-bfa2-89513fdeb85a`.
The fresh C3 preflight matched the principal physical checkout and common-dir,
`main`, HEAD `5c39875f8a6e75e5e01001126fd3cafb86dacb19`, raw index SHA-256
`623e67bff98d304acd7c6e4f5d988846fd2c83b97c37f8968a09cfc36868c91c`,
empty staging, and the eight declared mode-644 deltas. The five foreign files
remained outside the three-path write scope.

R3 RED used the selected unittest command after public-`verify` regressions
introduced simultaneous invalid index bytes and a declared missing file,
directory, or hardlink. The initial and second-scan subcases failed only
because the prior `_scan` opened the index before completing every declared
regular-file guard: 43 tests ran with six assertion failures (the expected
three initial and three `after.index` cases). The minimal production change
now retains the component/type/link-count guard before every content hash,
while leaving `_read_regular`'s open/fstat/metadata race checks in place.
The same command then passed 43/43 tests.

The CLI already produced the required invalid-input behavior, so its new
public-`main` regression was green on first execution rather than a fabricated
RED. It independently asserts the literal full R6 envelope and exact sorted,
compact ASCII JSON plus LF for an invalid verb, invalid extra arguments and
262145-byte stdin, including repeat byte determinism; no production change
was needed for that coverage.

Evidence ceiling remains rung 2, local deterministic unit tests with invented
OS/process fixtures. No live observer invocation, independent review, owner
acceptance, adoption, Git mutation, provider run, or later gate was performed.
The next gate is a separately dispatched independent differential review of
the exact candidate, followed by owner disposition.

## C4 R4 failure-step correction — 2026-09-17

Role `executor`; dispatch owner `019f71d6-632c-7870-bfa2-89513fdeb85a`.
The owner explicitly disposed the exhausted semantic budget (2/2) with this
exceptional bounded correction; the prior budget was not reset or reused.
Independent review remains a separate visible task. The C4 preflight matched
the principal physical checkout and absolute common-dir, `main`, HEAD
`5c39875f8a6e75e5e01001126fd3cafb86dacb19`, raw index SHA-256
`623e67bff98d304acd7c6e4f5d988846fd2c83b97c37f8968a09cfc36868c91c`,
empty staging and all eight declared regular mode-644 deltas. Only the script,
its tests and this validation history are writable; the five foreign files
and the other four specification documents remain protected.

R4 task `01a0af71-41a0-74e3-b4e4-9148f94aba2f` reported 43/43 passing tests
but retained one P2: the new existence/type/link-count guards attributed their
failures to `before.index`/`after.index`, contrary to the plan's
`paths`/`after.paths` steps. Its terminal result was
`NARROW_DELTA_FINDINGS -> REQUEST_OWNER_DISPOSITION` after semantic budget 2/2.
This invalidates any inference of contract compliance or acceptance from C3's
GREEN; the historical run and its incorrect test expectations remain recorded
above. R4 confirmed the CLI-envelope gap closed, and C4 does not reopen it.

Before RED, all affected inherited expectations were updated from the plan,
including missing executable and disappearance between observations. The two
guard regressions now cover index, executable and declared delta file, each
missing, a directory or a hardlink, before any content read in that scan.
Additional assertions preserve the distinction between guards and hashing:

| Observed failure | Initial step | Second-scan step |
|---|---|---|
| Missing/nonregular/multiple-link index, executable or declared file at the guard | `paths` | `after.paths` |
| Symlink or unexpected presence at an absent path | `paths` | `after.paths` |
| Index/file/executable digest mismatch or declared file-mode mismatch | `before.index` | `after.index` |
| Declared file becomes missing/nonregular/multiple-link after guards, while hashing has begun | `before.index` | `after.index` |
| Metadata change observed during or between reads | `before.index` | `after.index` |

The final scan retains `final.files`. Existing file-size/aggregate bounds and
metadata regressions were preserved. The six new during-hashing subcases use
only the OS open boundary to change the fixture after the guard; they were
already green at RED and are regression coverage, not a separate RED/GREEN
claim. No production guard or public seam was mocked.

One vertical RED -> minimal GREEN cycle used exactly this command twice:

```text
PYTHONDONTWRITEBYTECODE=1 /Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor/.venv/bin/python -B -m unittest discover -s tests -p test_readonly_preflight.py
```

RED exited 1: 44 tests ran with 23 expected assertion failures, all differing
only in failure-step attribution (18 guard-matrix subcases, three strengthened
physical-path subcases, missing executable and between-observation disappearance).
The production script still had R4 SHA-256
`9bb9f909e500dcc950b894c7db02b7d1cadd1e23afab9c4f34a5c32fd3f5b562`
for that RED. The minimal change replaced `step` with `path_step` in only the
two guard exceptions. GREEN exited 0 with 44/44 tests passing. Reasons, public
API, scan order, security bounds and read-time race checks remain unchanged.
No unexpected harness failure, retry or repair occurred in this cycle.

Evidence ceiling remains rung 2, local deterministic unit tests with invented
OS/process fixtures. Live observer execution, product tests, independent
review, owner acceptance, canonical adoption, Git mutation, network/providers
and publication remain unperformed. The non-atomic snapshot limits still
apply. The terminal capsule binds final postflight results and successor
hashes; this file does not contain its own final hash. Next gate: separately
dispatched independent differential review, then owner disposition.

## O1 live observer and procedural adoption candidate — 2026-09-25

Role `executor`; dispatch owner `019f71d6-632c-7870-bfa2-89513fdeb85a`.
This is the fresh O1 attempt after a prior procedural stop; it does not resume
or reclassify that grant. The three individually completed bootstrap calls
matched the principal physical checkout and absolute `.git` common-dir.
Before the observer, only filesystem and contract/tool identity reads followed.
The selected Python resolved to a physical regular executable with SHA-256
`4df3f520de9c3b86c4ae895c68921509ff29cfb9562656f7c31ed25591d68b29`;
the canonical Git executable's SHA-256 was
`6dc35ae68ae1b4a83f239bb22c7d6abc36b630d7f605de9f974cc4deb6510e1b`.
The immutable observer script and test SHA-256 values were respectively
`7cc19e45f21415b5b513f4b462ca91b67deb5f228178a29da83d8281770d7059`
and `aa8cef4c2cbf5fa2d2b51fe8aa1f6b28b39aaa7d67623c71a8c4520f42cd1f02`.
The inherited `GIT_PAGER` name was detected and excluded from the observer's
environment; no value was read.

The complete canonical R2 stdin contract for
`YINI-READONLY-PREFLIGHT-O1-2` had SHA-256
`9c47096206d99f7df7d80f9a303b93794767512ec644dedc39710f93c962b347`.
It bound principal `main`, HEAD
`705727392764b0a34ebd73b15d93220bab901468`, raw index SHA-256
`827e0c8b171ed50c29ab6e64dc3b54242792e710feaa1030ebe4246bb527fb30`,
empty staging, and all eight declared regular mode-644 deltas. The single CLI
invocation used absolute Python, `-B`, the immutable script, `verify`, the
literal contract digest, fixed stdin bytes, `shell=False`, and a Git-clean
inherited environment with `GIT_OPTIONAL_LOCKS=0`. It exited 0 and emitted one
complete canonical R6 `MATCH` result with the contract digest and exact
fingerprint, 12 ordered complete Git process records (all exit 0), no stderr,
and `successor_authority=false`. The before/after status stream digest was
`67f17f8cc54e00008db0ad438900df9be6d494a2cabfd14873c24532601c674e`;
both staged streams were empty. This is bounded local live-observation evidence,
not independent review, owner acceptance, provider evidence or future authority.

O1 then changed only the executor workflow, historical recipe pointer and this
append-only history. The five operational-readiness/semantic foreign deltas,
observer script and test remain outside write scope. This document does not
embed its own resulting hash. Required checks and successor hashes belong in
the terminal receipt. Owner acceptance is still required before the new
procedure becomes mandatory for future grants; independent review is the next
gate. No Git mutation, provider run, network, product test or 44/87 test rerun
is claimed here.
