# Deterministic Read-Only Preflight — Plan

## Current specification pass

Objective: define a minimal executable preflight contract before implementation.
Affected files: only `spec.md`, `requirements.md`, `plan.md`, `tasks.md` and
`validation.md` in this new directory. Assumptions: exact principal checkout,
five inventoried foreign deltas, unchanged main/HEAD/raw index, empty staging.
Risks: ambiguous process failure, hidden helpers, incomplete inventories,
symlink escape, bypass, and concurrent drift. Static checks and pre/post hashes
verify this documentary scope; future vertical regressions verify behavior.

One specification pass plus at most two in-scope documentary adjustments for
checks; maximum 120 tool calls and 160 captured pages. Initial presentation
target 100 lines / 6500 characters per chunk is not an acceptance invariant.
Recover incomplete read-only capture by bounded missing-range reads. Real
errors, mismatches and scope conflicts stop with no retry or repair.

## Proposed implementation footprint

Future code paths only: `scripts/readonly_preflight.py` and
`tests/test_readonly_preflight.py`. Standard-library unittest, no app imports,
pytest plugins, dependencies, provider calls or product validators. Unit test
fixtures are invented; no live Git repository or real mutator is needed.

Do not copy the installed portable preflight or build a generic command
framework. Separate small internal helpers for schema/path guards, raw byte
hashing, bounded process observation, porcelain parsing and result emission.
Only verify/main are the public seams defined in requirements.md. The complete
future allowlist and any canonical-document adoption changes require an exact
fresh grant; these proposed paths authorize no writes now.

## Fixed observation sequence

Each process uses the owner-bound Git executable as argv[0], followed by this
constant prefix, then exactly one suffix from the table:

```text
--no-pager --no-optional-locks
-c core.fsmonitor=false
-c core.untrackedCache=false
-c core.hooksPath=/dev/null
-c diff.external=
```

These are literal argv elements, not shell text. All subprocess calls use the
R3 environment and bounds. The contract supplies no argv element except the
verified executable path. Scalar comparisons include output shape as well as
value; staged output must contain zero bytes. Every process requires exit 0.

| Order / step ID | Work or immutable argv suffix |
|---|---|
| `input` | Validate CLI, bounded stdin, hash, JSON and all closed fields |
| `environment` | Check bytecode disabled, inherited Git variables, construct environment |
| `paths` | Check physical cwd, principal .git, executable and every declared path/absence |
| `before.index` | Hash raw index and governed files; compare contract before Git |
| `before.root` | `rev-parse --show-toplevel` |
| `before.common` | `rev-parse --path-format=absolute --git-common-dir` |
| `before.branch` | `symbolic-ref --quiet --short HEAD` |
| `before.head` | `rev-parse HEAD` |
| `before.status` | `status --porcelain=v1 -z --untracked-files=all --ignore-submodules=all` |
| `before.staged` | `diff --cached --name-status -z --no-ext-diff --no-textconv --ignore-submodules=none` |
| `after.paths` | Recheck environment/cwd/executable/path guards without changing context |
| `after.index` | Rehash index/files, compare metadata and bytes with first observation |
| `after.root` through `after.staged` | Repeat the same six suffixes once, same order |
| `final.files` | Recheck raw index/file/executable hashes and absence after final Git process |
| `result` | Validate and serialize exactly R6; MATCH only after every check succeeds |

The file checks before, between and after Git processes count toward a fixed
three file scans, each at most 64 MiB; there are two Git observations and at
most 12 child processes. The per-file 16 MiB bound applies on every scan.
The initial scan rejects bound fingerprint mismatches before Git; later changes
are OBSERVATION_DRIFT. Metadata changes during any read are drift, even if
bytes happen to match. Malformed Git records are OBSERVATION_MISMATCH.
R2 unsupported path shapes fail before subprocess; unannounced paths discovered
in status stop before opening those paths or running the next command.

The status choice intentionally ignores submodule worktree internals; v1's
coverage is the superproject delta only. A task requiring submodule evidence
is unsupported. Staged gitlink changes still fail the empty staged invariant.
Ignored inputs are likewise excluded explicitly, never silently counted as
observed. No cached PASS, retained Git output or self-updated contract can
replace a fresh required observation.

## Bootstrap and later adoption

Current task uses only its specifically granted literal preflight. The future
adoption procedure is a proposal until accepted and materialized in the
canonical executor workflow and old recipe by a separate scoped action.

The narrowly named bootstrap consists of individual tool calls, in order:

1. `pwd -P`, `login:false`, no workdir override.
2. `GIT_OPTIONAL_LOCKS=0 git rev-parse --show-toplevel`.
3. `GIT_OPTIONAL_LOCKS=0 git rev-parse --path-format=absolute --git-common-dir`.

Each call checks its own exit and exact expected physical identity before the
next; no `&&`, semicolon, pipe, substitution, or success suffix. Bootstrap is
permitted only when an exact fresh grant names it. It exists to satisfy the
canonical physical-first rule, not to furnish branch/index/delta evidence or
authorize other Git. Never broaden bootstrap to `write-tree` or a substitute
index/tree operation. Unsupported Git/runtime behavior stops without fallback.

After bootstrap, invoke the trusted mechanism with an owner-bound contract via
stdin before other Git. Verify its complete result and process exit together.
STOP, missing/invalid/truncated result, nonzero exit or unsupported coverage
returns to master/owner. MATCH only reports observation; each subsequent action
still needs its named authority and fixed-point continuity. A future adoption
must make these pointers coherent without copying universal plugin policy.

## Future verification and exit

Run the public-seam vertical cycles in [tasks.md](tasks.md), with independently
specified expected bytes/argv and call counts. Mock subprocess and filesystem
system boundaries only; do not replace parsing/guards/comparison/result logic.
Use real ephemeral regular files for hash/path fixtures when authorized, with
no real Git initialization or mutation even in temporary directories.

Proposed future unit command (not executed in this specification pass):

```text
/Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor/.venv/bin/python -B -m unittest discover -s tests -p test_readonly_preflight.py
```

Verify that exact executable before dispatch; missing runtime stops, with no
installation or substitute interpreter. RED must demonstrate each intended
failure before its minimal GREEN. [validation.md](validation.md) owns the
coverage matrix. Any real harness failure returns to owner; it cannot be
hidden by a later PASS. Independent review and owner acceptance are separate.
