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
