# Deterministic Read-Only Preflight — Requirements

All requirements below describe future delivery. None is runtime evidence.

## R1 — Closed public interface

Proposed CLI: invoke the owner-bound absolute Python executable with `-B`,
the absolute `scripts/readonly_preflight.py`, `verify --contract-sha256 HEX64`.
Supply the complete UTF-8 JSON contract on stdin, not via a shell substitution
or a generated shell command. No output-file option or contract-file lookup.
Unknown operations/options, duplicate options, missing arguments, extra argv,
and attempts to supply shell text or Git commands fail before any subprocess.
Even a requested `write-tree` operation never reaches process creation.

Public Python seams: `verify(contract_bytes: bytes, expected_sha256: str) ->
dict` returns the result in R6; `main(argv: list[str]) -> int` reads bounded
stdin, calls verify, emits the result, and returns its `exit_code`. Import has
no I/O/process side effects. CLI parse failures emit the same result envelope.
No injectable runner is part of the public API; tests patch only real system
boundaries. Python must run with bytecode disabled; otherwise R6 failure.

## R2 — Exact input schema

Reject duplicate JSON object keys, BOM, non-UTF-8, non-finite numbers, unknown
or missing keys, wrong types (including booleans used as integers), and trailing
non-whitespace. Hash the original input bytes, including whitespace; compare
to the externally supplied lowercase SHA-256 before using any contract value.
No defaulting, coercion, extra schema dialect, or self-hash field.

Every object is closed. Top-level fields are exactly:

| Field | Required value/type |
|---|---|
| `schema_version` | literal `yini-readonly-preflight/contract-v1` |
| `work_unit_id` | 1–128 ASCII letters, digits, `_`, `-`, or `.` |
| `repository_id` | literal `yini-insurance-advisor` |
| `root` | literal principal physical path from spec.md |
| `common_dir` | literal root plus `/.git` |
| `branch` | literal `main` |
| `head` | 40 lowercase hexadecimal characters |
| `index_sha256` | 64 lowercase hexadecimal characters |
| `staged` | empty array only |
| `delta` | at most 128 rows, sorted by UTF-8 path bytes, unique paths |
| `absent` | at most 128 sorted unique safe relative paths, disjoint from delta |
| `ignored_inputs` | literal `none`; asserts none relevant to this observation |
| `git` | object containing exactly `path` and `sha256` |

Each delta row contains exactly `path`, `xy`, `kind`, `mode`, `sha256`.
`xy` is exactly ` M` or `??` (leading space is significant); `kind` is
`regular`; `mode` is string `644` or `755`; `sha256` is lowercase HEX64.
An empty delta is valid. `absent` binds proposed outputs that must not exist;
it grants no write authority. Postflight uses a separately bound successor
contract, removing created paths from absent and recording their actual hashes.
Foreign rows retain the original grant's identities.

Safe relative paths consist of nonempty `/`-separated ASCII segments using
letters, digits, `.`, `_`, `-`, and spaces. Reject absolute paths, `.` or `..`
segments, leading/trailing segment spaces, repeated separators, backslashes,
controls, shell metacharacters and substitutions. Reject any segment `.git`,
`.venv`, `data`, `corpus`, or beginning `.env`. All existing components must
be non-symlinks, below the physical root; final present paths must be regular
files with link count one. For absent paths, check every existing ancestor and
use lstat semantics so dangling symlinks are not absence. Never open unexpected
status paths or follow symlinks to compute evidence.

`git.path` is an absolute canonical physical executable regular file, with no
symlink components, verified against `git.sha256` before the first subprocess.
Only that executable is used, with no PATH lookup. Owner dispatch separately
binds trusted Python and verifier identities; this program is not its own trust
root. Every contract/path/environment/executable guard completes before Git.
The physical cwd must already equal root; never chdir or use Git `-C` to repair it.
`.git` must be a physical directory and its index a non-symlink regular file;
linked worktrees, bare repositories and alternate common-dirs are unsupported.

## R3 — Processes, environment and resource bounds

Only [plan.md](plan.md)'s immutable argv tuples may reach subprocess. Use
`shell=False`, stdin disconnected, explicit cwd equal to the already-verified
cwd, byte streams, and the declared minimal environment. No command strings,
eval, aliases, hooks, external diff/textconv, fsmonitor, nested shell, remote
action, mutator, index/tree reconstruction, retry, escalation, or repair.

Reject inherited `GIT_*` except `GIT_OPTIONAL_LOCKS=0` before any subprocess.
Pass only the following environment to Git: `PATH=/usr/bin:/bin`, `LC_ALL=C`,
`LANG=C`, `TZ=UTC`, `HOME=/dev/null`, `XDG_CONFIG_HOME=/dev/null`,
`GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_SYSTEM=/dev/null`,
`GIT_CONFIG_GLOBAL=/dev/null`, `GIT_ATTR_NOSYSTEM=1`, `GIT_OPTIONAL_LOCKS=0`,
`GIT_TERMINAL_PROMPT=0`, `GIT_NO_REPLACE_OBJECTS=1`.
No inherited environment is forwarded, including loader/Python/shell settings.
Repository configuration is not rewritten. Fixed argv overrides disable its
relevant helper paths; unsupported configuration behavior fails closed.

Fixed bounds: stdin 262144 bytes, each subprocess 5 seconds, each stdout/stderr
stream 262144 bytes, each governed file/index/executable 16 MiB, total bytes
hashed per file scan 64 MiB including the Git executable, exactly three file
scans on success, two Git observations and at most 12 Git processes. Early
failure stops without completing remaining scans. Read streams incrementally
with a deadline, detect cap+1,
terminate/reap the current child on timeout/overflow, and start no later child.
Do not use unlimited capture followed by truncation. The contract cannot raise
bounds. A cap is an execution limit, unlike the UI's initial 100-line or
6500-character presentation targets. No partial observation can PASS.

## R4 — Complete fingerprint and fail-fast observation

Hash physical `.git/index` bytes with hashlib, without any Git subprocess for
that hash and without interpreting its contents. Check mode/kind and hash of
each expected delta file. Compare the entire NUL-delimited porcelain map to
delta, independent of Git's tracked-first record ordering; never strip XY.
Reject malformed/missing terminal NUL, invalid UTF-8/unsafe paths, duplicate
paths, unexpected XY, directory summaries, rename/copy pairs, missing or extra
records. Preserve raw output hashes as well as the canonical map.

Cached diff must be empty, not merely exit 0. Root/common-dir/branch/HEAD must
match exactly (remove only the single terminal LF expected for scalar outputs).
Evaluate each exit before parsing its output, each output before starting the
next process, and stop on the first failure. Match every field to its expected
contract identity; no inference from counts alone. Do not hash ignored data.

Run the fixed observation twice in order. Recheck cwd, executable, index,
files, absent paths and filesystem identities in both observations. Compare
both with the bound contract and each other, including inode/device/size/mtime
and ctime around reads, to catch visible changes. Metadata is compared in
memory, not emitted as nondeterministic telemetry. Stop on any observed drift;
the second pass is an explicit stability check, never a retry after failure.

## R5 — Outcome and no continuation

Any failing command ends the invocation immediately; never append a success
command or evaluate a later probe. A child exit 128 must produce result
`reason=GIT_EXIT`, `child_returncode=128` and CLI exit 128. Positive child
codes 1–255 propagate exactly; signal termination retains the negative code
and maps CLI exit to `128 + signal` (capped at 255). No process launch is exit
5, timeout 124, capture overflow 125. Result reason distinguishes overlapping
numeric exit codes. No implicit retry, repair, cleanup, fallback, or escalation.

## R6 — Exact deterministic result

Emit exactly one UTF-8 JSON object plus LF, `sort_keys=True`,
`separators=(',', ':')`, `ensure_ascii=True`, with these fields only:

| Field | Contract |
|---|---|
| `schema_version` | `yini-readonly-preflight/result-v1` |
| `work_unit_id` | validated ID, otherwise null |
| `contract_sha256` | computed raw digest, or null when complete input unavailable |
| `outcome` | `MATCH` or `STOP` |
| `reason` | one closed value below |
| `exit_code` | integer as defined here/R5 |
| `failed_step` | null or one fixed step ID from plan.md |
| `child_returncode` | integer for terminating child error/signal, otherwise null |
| `observations` | ordered completed/failed process records, at most 12 |
| `fingerprint` | null on STOP; on MATCH exact root/common_dir/branch/head/index_sha256/delta/absent fields from verified contract |
| `successor_authority` | always false |

Each process record has exactly `step`, `returncode` (integer or null for
launch/timeout/overflow), `stdout_sha256`, `stderr_sha256`, `stdout_bytes`,
`stderr_bytes`, `complete`. Digests identify captured byte streams; incomplete
streams are explicitly marked false. Record no raw stderr/stdout, environment
values, content, timestamps, random IDs, durations, or tracebacks. Incomplete
hashes are never represented as full-output evidence. Terminate safely if JSON
output cannot be delivered; never substitute a success exit.

Closed reason/exit pairs: `MATCH/0`, `INVALID_INPUT/2`, `CONTRACT_HASH_MISMATCH/2`,
`CONTRACT_INVALID/2`, `PATH_UNSAFE/2`, `ENVIRONMENT_UNSUPPORTED/4`,
`CHECKOUT_UNSUPPORTED/4`, `TOOL_IDENTITY_MISMATCH/4`, `OBSERVATION_MISMATCH/3`,
`OBSERVATION_DRIFT/3`, `FILESYSTEM_ERROR/5`, `PROCESS_LAUNCH_ERROR/5`,
`GIT_EXIT` per R5, `TIMEOUT/124`, `CAPTURE_LIMIT/125`, `INTERNAL_DEFECT/70`.
Use plan.md guard order and report the first failure; no unordered aggregation.
Identical input, captured outputs and outcomes produce byte-identical JSON.

## R7 — Procedural adoption and evidence ceiling

After separate validation/review/acceptance and authorized adoption, owner
handoffs must select this mechanism before any other Git observation except
the named bootstrap in plan.md. Missing or unsupported mechanism stops; no
ad hoc substitute. Mechanism use still needs explicit read-only authority and
an exact owner-bound contract. MATCH proves only a bounded local observation;
it is not spec acceptance, authority authentication, hard tool enforcement,
implementation approval, independent review, or permission for a later action.
