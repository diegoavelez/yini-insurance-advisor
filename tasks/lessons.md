# Harness lessons

## AOPS-012 H4: bounded preflight repair

These controls document harness failures only. They do not classify the
seven-path candidate or grant any Git action.

## Historical references

The historical references for this record are:

- G1: `01a09af9-f49c-7083-a6e6-b80e59cfd505`
- G2: `01a09afc-fc1d-76b0-9156-13f474136c23`
- G3: `01a09d44-8849-7ed3-8a15-9b8653179c40`
- H4: `01a09d4a-ec90-70a3-a252-e7632780064a`

These IDs are historical references only. They grant no replay, validation,
correction, review, Git, or successor authority.

## AOPS-012 RH4: exact executable invocation

RH4 task `01a09d50-2468-7e41-9073-a243f5c4b2ad` ended in
`INVOCATION_ERROR`: it received the shorthand `repo/.venv/bin/python` and
executed that literal path, which did not exist. The cause was ambiguity in
the master handoff plus the absence of an exact executable check; this is not
evidence that the real runtime is absent. The control is to use complete,
absolute, copyable paths for every invocation and check that the exact path
exists and is executable before dispatch. This is mechanical invocation
hygiene, not a model problem and not a reason to increase reasoning effort.
No `selftest` or review `PASS` was observed; the RH4 axes remain unevaluated.

| ID | Classification and cause | Preventive control | Regression criterion |
| --- | --- | --- | --- |
| H4-G1-INDEX-LOCK | Observed invocation failure: a Git staging attempt could not create the index lock. | Treat an index-lock failure as terminal for that Git grant; do not probe permissions, remove locks, or retry. | Pending criterion, not executed: a fixture should record the failure as `HARNESS_DEFECT` and ensure the repair harness leaves staging unattempted. Git add was not reproduced because it is mutating. |
| H4-G2-ABSOLUTE-RM | Observed invocation failure: a preflight named an unavailable absolute cleanup executable. | Build manifests in memory; do not include cleanup in a read-only preflight. | The reusable command has no cleanup command and writes no repository artifact. |
| H4-G3-WRAPPER-SYNTAX | Observed invocation failure: mixed wrapper/base64 construction raised `SyntaxError` before preflight. | Store a small, reviewable Python file and compile inert malformed source only in its synthetic regression. | Synthetic sources for `def gt*()` and `for p:` fail compilation while the harness itself compiles and self-tests PASS. |
| H4-G3-INDEX-SEMANTICS | Static analysis of the unexecuted G3 wrapper found an invalid assumption that `git ls-files -s` should be empty. | Check that the index has baseline entries; use cached diff output to test for no staged delta. | An artificial non-empty `ls-files -s` fixture passes and an empty baseline fixture fails. |
| H4-G3-BYTES-NAME | Static analysis of the unexecuted G3 wrapper found `.name` used on bytes. | Decode only intentionally at output boundaries and use `Path` objects for paths. | The inert bytes-expression fixture raises `AttributeError`; the real harness reports UTF-8 status records. |
| H4-G3-PORCELAIN-SPACING | Static analysis of the unexecuted G3 wrapper found an ambiguous XY/path representation. | Preserve porcelain-v1 `-z` records byte-for-byte; never strip their leading status spaces. | Fixtures distinguish unstaged ` M path` from staged `M  path`. |
| H4-H4-MODE-FORMAT | Observed during this repair: permissions were first rendered as `0644` rather than contract-required octal without prefix. | Render modes with `:o`, not zero-padded formatting. | The seven-path real manifest hash is exactly `1a0868a9b3c82a15bf23ea067f8b0123da17b52943ecfb06ae9acf17646a1421`. |
| H4-H4-UNTRACKED-SUMMARY | Observed harness defect: Git without `--untracked-files=all` summarized `tasks/` and omitted the nested `tasks/lessons.md` path. | Pass `--untracked-files=all` explicitly for inventories and include a nested-untracked fixture. | Pending criterion, not executed: the fixture should distinguish the directory summary from the nested leaf path. |
| H6-LEXICAL-ORDER | Observed in the temporary H4 harness: it appended `tasks/lessons.md` after `tests/test_validate_master_control.py`, so both its manifest and expected raw-status fixture were not lexical. | Sort the complete path set before constructing either manifest entries or expected porcelain records. | Local RED showed `tests` before `tasks`; GREEN orders `tasks/lessons.md` before `tests/test_validate_master_control.py`. |
| H6-SELFTEST-EXIT | Observed in the temporary H4 harness: `--self-test` always returned exit 0, even when a check was false. | Return 0 only for a `PASS` result and 1 for `FAIL`; exercise the CLI seam by mocking the self-test result. | Local RED forced one false check and observed 0; GREEN returns 1 for that same result. |
| H6-PHASE-GUARDS | Observed during H6 fixture review: positive phase fixtures alone did not prove rejection of a changed HEAD, manifest, raw status, staged names, or dirty postcommit state. | Keep negative fixtures for each guard; staged fixtures require `A  tasks/lessons.md` and postcommit fixtures require empty status and no staged names. | Local fixtures reject every listed mismatch while valid staged and clean postcommit fixtures pass. |
| H7-H6-RAW-PORCELAIN-ORDER | Corrective diagnosis of the H6 harness regression: it compared a lexically ordered expected porcelain list with Git's valid tracked-first, then untracked, output, incorrectly treating record order as candidate drift. | Keep lexical order only for the canonical manifest. Parse complete NUL-delimited porcelain records into an exact route-to-XY mapping without stripping XY spaces, and compare mappings while rejecting malformed, duplicate, missing, extra, wrong-XY, rename, and copy records. | The exact tracked-first fixture is RED under list comparison and GREEN under mapping comparison; the local negative matrix rejects every listed invalid form, while synthetic staged and postcommit mappings pass. |

## Falsifiable diagnostic hypotheses

1. The G1 stop was an environment/index-lock invocation failure, not a change
   to candidate bytes; a read-only raw-status and cached-diff probe should
   retain seven unstaged paths and no staged names.
2. The G2 stop was caused by the harness executable path, not Git fixed-point
   drift; an in-memory manifest computation should succeed without cleanup.
3. The G3 stop occurred before its preflight probes; compiling the two malformed
   snippets as inert data reproduces syntax failure, while no candidate
   validator result may be inferred from it. This is not a reproduction of the
   complete historical wrapper: the wrapper's exact construction and runtime
   envelope were not replayed.
4. A repaired observer must retain raw porcelain spacing and a non-empty index
   baseline; synthetic records that erase either property must fail.

The H4/H6 temporary harness is support evidence only and was not approved by
independent review. Its local PASS is neither independent review, acceptance,
staging, commit, push, provider health, nor publication authority; it is not
authorized for Git use. H6 corrected its local lexical-order and self-test
exit behavior, but it is not a Git preflight by itself. A future separately
authorized Git task must directly verify the absolute common-dir, branch,
HEAD tree, parent relationship, staged blobs, and the relevant raw index and
status facts before it performs any Git action. Those direct checks remain
outside this task and were not run here.

H7 corrects only the temporary harness's raw-porcelain comparison. Its local
RED-to-GREEN regression and deterministic self-test are support evidence, not
an independent PASS or any acceptance, Git, provider, or publication evidence.

## Executor role and checkout boundary

R1H1 task `01a0a559-3689-73a1-b6cb-0a5044afbc0a` issued `create_thread` with
explicit worktree/working-tree selection despite its no-delegation grant;
only a provisional clientThreadId was observed. Keep dispatch with master,
retain the executor role after reading master instructions, and check physical
cwd/common-dir before work without corrective `cd`. Recover incomplete
read-only capture by pagination, never by repeating a mutation. This is a
contractual prevention lesson, not proven runtime enforcement or inferred
intent; the later master-dispatched test remains pending. Evidence and limits:
`specs/2026-09-15-executor-checkout-boundary/validation.md`. Revisit this lesson
if observed runtime controls supersede the documented contractual boundary.

## Defensive parsing for read-only tool capture

R1 task `01a0a573-b12e-7422-8483-86d8836e10ec` repeated a harness pattern:
an unconditional `JSON.parse` converted a non-JSON `read_thread` error into
`SyntaxError: Unexpected token 'r', "read_threa"... is not valid JSON` and
terminated the FULL review. Prevent recurrence by emitting response format,
`isError`, and block types first; then parse inside `try/catch`, validate the
expected `turns` or `items` shape before traversal, and classify nested
truncation as incomplete. Plain-text errors, malformed JSON, unexpected
shapes, and truncation are distinct non-PASS outcomes. Retire this local guard
only when the host provides a stable typed contract plus regression coverage
for all five classes and proves that error responses cannot bypass it.

C1 adds that an array container alone is insufficient: before returning a
complete capture, validate each `turn` record, its array `items`, and each
item record that the later traversal consumes. Keep the positive fixture
non-empty. Also distinguish a historical preflight that explicitly sets
`workdir` from evidence of the caller's unmodified initial cwd; either fact
does not prove future runtime enforcement.

## Executor recipe boundary

A SHA-256 digest of the physical `.git/index` file identifies those index
bytes; it is not a Git tree OID and must never be substituted or reconstructed
with an index/tree mutation. A source declared optional may be pruned only
after its bounded absence/no-match is recorded and an already-authorized
alternative is available. That pruning never invents content, replaces a
required source, renews a grant, or turns an incomplete capture into PASS.

## Capture size versus evidence completeness — 2026-09-17

Readiness review `01a0aa84-dcc1-76a2-99bf-5ad15c098afe` stopped after an
authorized diff exceeded its explicit 100-line capture grant. That historical
STOP remains valid history. The recurring documentary mechanism combined a
hard line cap with an unpaginated diff invocation, then supplied an externally
chosen `HARNESS_DEFECT` classification to the facade. No runtime 100-line
input limit was demonstrated. Future grants should use 100 lines as a starting
presentation target, preserve exit/source/completeness independently, and page
retained output before emission, including a single long line. The sole recipe
and regression record are in
[plan.md](../specs/2026-09-15-executor-checkout-boundary/plan.md#capture-size-amendment--2026-09-17)
and [validation.md](../specs/2026-09-15-executor-checkout-boundary/validation.md#capture-size-diagnosis--2026-09-17).
Prune this lesson when those canonical controls are stable and independent
regression evidence covers complete oversize, incomplete recovery, real errors,
drift, exhausted total budgets, and no mutation replay. Documentary/local
evidence does not promise future compliance or zero failures.
