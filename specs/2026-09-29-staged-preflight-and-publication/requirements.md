# Staged Preflight and Publication — Requirements

All requirements are proposed future behavior. Existing v1 remains unchanged.

## R1 — Public seam and version selection

New CLI: owner-bound absolute principal `.venv/bin/python -B`, absolute
`scripts/staged_readonly_preflight.py`, `verify --contract-sha256 HEX64`,
with complete UTF-8 contract bytes on stdin. New public seams:
`verify(contract_bytes: bytes, expected_sha256: str) -> dict` and
`main(argv: list[str]) -> int`. Import has no I/O. There is no freeze, stage,
commit, publication, raw-command, retry or output-file operation.

The [v1 R1–R3 input rules](../2026-09-17-deterministic-readonly-preflight/requirements.md)
apply by explicit reference: duplicate keys/options, unknown fields, wrong
types, BOM, non-finite JSON, unsafe paths and raw byte hash mismatches fail
before Git. Do not dispatch by trying versions until one passes.
A v1 invocation remains a v1 invocation, including its result schema and
12-process success sequence. V2 neither imports private v1 helpers nor changes
v1 files. Small deliberate local duplication is preferable to an unrequested
shared-framework extraction.

## R2 — Closed contract-v2 schema

Top-level fields are exactly those below; all are required:

| Field | Value or type |
|---|---|
| schema_version | literal `yini-readonly-preflight/contract-v2` |
| work_unit_id | v1 ASCII identifier, length 1–128 |
| repository_id | literal `yini-insurance-advisor` |
| root, common_dir, branch | same principal root, root/.git and main literals as v1 |
| head | full lowercase nonzero HEX40, supplied from Git |
| index_sha256 | raw physical .git/index bytes, HEX64 |
| config_sha256 | raw physical .git/config bytes, HEX64; values never emitted |
| index_tree_sha256 | canonical complete stage-0 index map digest defined below |
| state_kind | `empty_staged` or `staged_regular` |
| staged | sorted unique array, at most 32 rows, exact shape below |
| delta | sorted unique array, at most 128 v1-shaped worktree rows |
| absent | at most 128 sorted unique safe relative paths |
| ignored_inputs | literal `none` |
| git | closed object with canonical executable path and SHA-256 as in v1 |

Every digest is lowercase HEX64. Booleans are never integers. Paths are sorted
by UTF-8 bytes in the contract; ordering of Git records is not significant.
Empty_staged requires zero staged rows; staged_regular requires 1–32.
The complete delta permits exactly ` M`, `??`, `M `, `MM`, `A `, `AM`.
Leading and trailing XY spaces are significant. Delta remains the raw
worktree identity: path, xy, kind=regular, mode=644 or 755, sha256.
Absent paths are disjoint from delta and staged. Each staged path has exactly
one delta row with X equal to its change; every delta X=A/M has a staged row.
X=space or ? never has one. These consistency guards run before subprocess.

Each staged row has exactly:

| Field | Contract |
|---|---|
| path | safe relative path, same guards as v1 governed files |
| change | A or M |
| head_mode | A: 000000; M: 100644 or 100755 |
| head_oid | A: forty zeroes; M: nonzero full lowercase HEX40 |
| index_mode | 100644 or 100755 |
| index_oid | nonzero full lowercase HEX40 |
| blob_sha256 | SHA-256 of raw staged blob bytes |

For M, the old and new (mode, OID) pairs must differ; a mode-only change is
valid. No equivalence is assumed between index_mode and worktree mode or
between blob_sha256 and worktree sha256. This supports MM/AM and raw-byte
differences caused by line-ending normalization. No filter execution is allowed.

The complete index map is the UTF-8-path-sorted list of closed objects
`{"path":..., "mode":..., "oid":...}` for every index entry. Serialize with
sorted object keys, compact separators, ensure_ascii=True and one terminal LF;
index_tree_sha256 hashes those bytes. Stage must be exactly 0 and mode must
be 100644/100755 for every entry. Never collapse duplicate paths, stage records
or names before checking uniqueness. This is a canonical entry-map digest,
not Git's tree OID and not a replacement for raw index identity.

Index-wide names are metadata only: require valid UTF-8, nonempty relative
paths, no dot/dotdot, controls, repeated separators or duplicate normalized
names. V1's stronger safe-path and sensitive-directory exclusions apply to
governed delta/staged/absent paths before opening content. Never open an
unexpected status/index path or unstaged unrelated blob.

## R3 — Read-only guards, bounds and observation

Use the closed argv and sequence in [plan.md](plan.md). No shell, arbitrary
argv, remote call, index refresh, tree construction, hash-object, mutation,
permission escalation or fallback exists inside the observer. Bytecode is
disabled. V1's fixed minimal Git environment and immutable prefix apply;
no inherited GIT_* except GIT_OPTIONAL_LOCKS=0 is accepted. The caller removes
other inherited Git names before invocation without printing their values.

Before Git, validate every governed path and physical ancestor, executable,
index, config and expected absence, then hash. Preserve v1 regular-file,
single-link, no-symlink, physical-cwd, metadata-around-read and race guards.
Config hashing is bounded streaming identity only; no values are emitted.
Reject physical .git/objects indirection, objects/info/alternates,
objects/info/http-alternates, any pack/*.promisor, .git/shallow and
.git/info/grafts before child creation. Directory inventories are bounded to
8192 entries and rechecked each scan; do not traverse object content.
Unsupported or unreadable layouts fail closed, without lazy fetch.

Before status or blob reads, config-name inspection rejects include/includeIf,
filter.*, extensions.*, remote.*.promisor, remote.*.partialclonefilter,
core.sparsecheckout, core.sparsecheckoutcone, core.splitindex and core.worktree
keys, regardless of values. Only key names are parsed, never values.
Fixed argv disables hooks/fsmonitor/untracked-cache/external diff; no global
or system config is loaded. The linked-worktree file form of .git is rejected.
Split-index output must be empty. Complete index metadata must contain only
H-tagged, stage-0 regular entries; reject all lowercase tags, S, unmerged
stages, zero OIDs, symlinks, gitlinks and sparse-directory entries.

Bounds: input 262144 bytes; each physical file/index/config/executable 16 MiB;
three file scans, each at most 64 MiB; each process 5 seconds plus at most
5 seconds to kill/reap. Ordinary stdout and every stderr stream: 262144 bytes.
Index-list stdout: 2 MiB and 8192 entries. Blob stdout: 16 MiB per row and
64 MiB total per observation, streaming digests without retaining content.
All other limits are fixed, not contract-configurable. Exactly two successful
Git observations, 9+N children each, total 18+2N <= 82, where N=len(staged).
No deduplication skips a per-path blob observation. Output envelope <=262144
bytes. Detect cap+1 while reading; never capture unlimited then truncate.

Every command must exit 0 and its output validate before the next command.
Parse complete NUL records, reject malformed UTF-8/headers, missing terminal
NUL, duplicates, unexpected/missing paths and unsupported modes/statuses.
Compare full maps, not counts or raw record order. Cached raw diff must equal
staged rows' old/new mode/OID/change values. The index map must equal its
bound digest and each staged row. Read each staged blob through the trusted
Git executable using exactly its bound index_oid and blob type; stream SHA-256
and compare blob_sha256. Git supplies object lookup identity; the observer
does not reconstruct a Git OID or write an object.

Initial mismatch stops as OBSERVATION_MISMATCH; a changed subsequent
observation stops as OBSERVATION_DRIFT. Structural unsupported state is
STATE_UNSUPPORTED in either pass. Malformed streams use OBSERVATION_MISMATCH.
All filesystem identities and contents are compared before, between and after
Git observations; compare canonical maps between passes. Raw stream digests
may differ solely from valid record ordering. No later success heals a failure.

## R4 — Closed result-v2

Exactly the v1 R6 top-level field names are used, with schema_version
`yini-readonly-preflight/result-v2`. The process record shape, original-byte
contract_sha256, child exit propagation, canonical JSON plus LF, no raw-output
rule and deterministic serialization are unchanged. V2 observations have at
most 82 records, with fixed step IDs from plan.md. No timestamps or durations.

Fingerprint is null on STOP. On MATCH it contains exactly root, common_dir,
branch, head, index_sha256, config_sha256, index_tree_sha256, state_kind,
staged, delta and absent, equal to the verified input. successor_authority is
always false. MATCH requires exit_code=0, reason=MATCH, failed_step and
child_returncode null, and exactly 18+2N complete successful process records.

The closed reason/exit pairs are the entire v1 R6 set plus
STATE_UNSUPPORTED/4. Positive Git child codes 1–255 propagate; negative
signals retain child_returncode and map CLI exit to min(255,128+signal).
Launch/timeout/overflow preserve incomplete process evidence and stop without
a successor. Blob records carry only captured-stream hash/length; partial
hashes have complete=false. CLI/result-delivery failure never returns success.
Unsupported schema is CONTRACT_INVALID; runtime/tool/checkout/path errors
retain v1 categories. Guard order in plan.md determines the first failure.

## R5 — Publication authority and expected transitions

The only proposed order is:

`preflight -> stage (if authorized and needed) -> verify-index -> commit ->
capture full native OID -> verify parent/tree/paths -> push under own grant`.

This is a lifecycle graph, not observer functionality or current authority.
The installed plugin's authority-grants.md owns simple grants, explicit bundles
and compound Git anchoring; the repository owns visible-task boundaries.

A commit-only grant never stages. For a single ordered stage/commit anchoring
attempt, the owner must explicitly choose that specialist form and bind steps,
expected intermediate states and completion limit. Otherwise stage and commit
are separate fresh tasks/grants. Push is always its own named grant; an
explicit multi-grant bundle can group decisions without merging authority.

Before stage, bind accepted file bytes/modes, exact stage paths, protected
foreign rows, initial index and intended staged blob map. Partial files are
already-staged inputs only; this proposal does not add an interactive or
automatic partial-staging engine. A stage grant must say how exact accepted
content maps to intended blobs; unknown conversions or filters stop.

The post-stage raw index hash cannot be assumed equal to the initial hash.
An explicit anchoring grant may permit capturing the new raw hash ONLY after
successful authorized stage and exact full intended index-map/staged/worktree/
foreign comparisons. That authorized successor capture becomes the next
precondition under the declared sequence. The verify-only observer itself
never learns or freezes expectations. If successor derivation was not granted,
return evidence to owner for a new bound contract. No arbitrary observation
can be converted to expected state, and no mismatch can be repaired by rebinding.

Verify-index must pass the selected v2 contract before commit. Commit writes
only the already verified index; no -a, implicit stage, amend, reset, hooks,
automatic signing helper or cleanup. Exact invocation, identity/message and
helper policy belong in the fresh grant. A denied permission, failure,
interruption or unknown outcome ends the attempt; inspect only separately
authorized retained/read-only evidence and never replay a possible mutation.

Effective runtime permissions must be checked before the action. Where .git
is read-only, use the normal explicit escalation route for the named Git action
when its fresh grant permits it, anticipating the need before invocation.
No Full Access/config change or bypass is allowed. Escalation is not guaranteed
approval. Denial is STOP; there is no automatic retry, repeated escalation or
objective-bundle continuation. Any later attempt requires explicit renewal
against the observed state. A valid existing owner grant need not be requested
twice merely because it was relayed, but a relay cannot override runtime review.

## R6 — Native identity and publication evidence

Full commit OID must come from successful Git rev-parse, never the commit
banner's prefix, padding, guessed suffix, transcript inference or a hash
computed from text. Even a syntactically valid HEX40 is not native evidence.
After commit, separately authorized read-only checks must prove exactly one
expected parent, complete tree-map equality with the verified precommit index,
exact changed path/mode/blob map and preserved worktree/foreign state.
plan.md fixes the read-only command family. Do not call write-tree.

Push eligibility requires those checks, a still-current push grant binding
the full local OID, exact remote/ref and allowed transport, and its preconditions.
A stale fixed point or different remote rejects before push. Do not infer a
remote endpoint, use force, fetch to repair divergence or retry automatically.
Successful push is transport evidence only. Independent remote readback,
provider health, deployment and acceptance remain distinct.

Canonical semantic updates must be scoped before final review/acceptance and
Git close when semantics changed. A successful push alone triggers no recursive
document reconciliation. External-publication Full receipt handling follows
the existing receipt policy, with separate authority for persistence/readback;
the administrative tail does not recursively generate another Full receipt.

## R7 — Compatibility and completion criteria

| AC | Required outcome |
|---|---|
| AC1 | V1 code/tests/spec meaning preserved; v1 staged rejection and exact result regressions retained |
| AC2 | V2 closed schema and exact state_kind reject malformed/unsafe inputs before subprocess |
| AC3 | Raw index, index tree, staged blob/mode/OID and worktree bytes are independently bound; partial staging and mode-only changes match correctly |
| AC4 | Missing/extra/duplicate/unmerged/index-mismatch/unsupported records stop; record ordering never changes map comparison |
| AC5 | Exact argv/environment/bounds, no mutator/helpers/network, races and per-child failures stop without successor |
| AC6 | Deterministic complete result/exit/fingerprint agreement, successor_authority=false and no post-STOP fallback |
| AC7 | Publication graph has exact intermediate states, native OIDs, parent/tree/path verification, task-bound grants and denial STOP |
| AC8 | Canonical adoption precedes procedural use; review/acceptance/Git remain separate; no post-push documentary recursion |

Acceptance requires all applicable tests and documentary checks observed with
their real outcomes, exact candidate identity, independent review and owner
disposition. Internal PASS is not acceptance.

## W1 — Candidate contract-v3 and compatibility

Amendment candidate dated 2026-09-30; W1–W4 apply only to proposed v3.
R1–R7 continue to define v2. All v2 constraints carry into v3 except the
explicit schema, selective extension guard, process order/count and fingerprint
changes below. V1/result-v1 and v2/result-v2 remain unchanged.

V3 uses the same verify/main signatures and CLI verb as R1, selected from the
validated input schema before subprocess. There is no version-probing loop.
The closed top-level schema is exactly R2's fields with schema_version replaced
by `yini-readonly-preflight/contract-v3`, plus all three required fields:

| Field | Exact constraint |
|---|---|
| repository_format_version | JSON integer 0 only; reject bool, float and string |
| extension_worktree_config | JSON null (key absent), true or false; reject numeric/string substitutes |
| config_worktree | closed object exactly `{"state":"absent"}` |

These fields bind the principal configuration, not linked-worktree metadata.
No configurable config path, present-file shape, default, additional key or
digest for an absent file exists. JSON duplicates at every object level reject
before Git, as do unsupported version/shape/type combinations. R2 raw
config_sha256 still binds the complete common config bytes. The special
config_worktree absence is checked separately from governed absent[]:
R2's prohibition on putting .git paths in absent/delta/staged remains intact.

## W2 — Selective configuration and physical guards

Before any Git child, validate all existing physical ancestors and prove
principal .git is a directory. Use lstat semantics to bind
`common_dir + "/config.worktree"` as absent: dangling symlinks are present.
A symlink at that path/ancestor is PATH_UNSAFE/2; any other present leaf
(regular, hardlinked, directory or special file) is STATE_UNSUPPORTED/4.
Never open that leaf, even when the extension is false or absent. No linked
config is read, hashed or enumerated by v3. Common .git/config remains a
bounded, non-symlink, single-link regular file with its bound raw hash;
unsafe config/index/tool/path guards and every storage exclusion remain.

Read only key names from the already guarded common config through the
explicit --file probe in plan.md. Preserve R3's prohibited-name checks,
except for the exact case-insensitive key `extensions.worktreeConfig`.
A subsection variant is not that key and remains an excluded extension.
Includes/includeIf and every other extensions.* key still reject regardless
of values. Remote promisor/partialclonefilter, filters, sparse/split index and
core.worktree prohibitions remain unchanged.

Count the two protected names before dictionary insertion/value lookup:
core.repositoryformatversion must occur exactly once;
extensions.worktreeConfig must occur zero or one times. Repeated protected
keys reject STATE_UNSUPPORTED/4 even when values agree or differ only in
case; never use last-value-wins. Other permitted repeated names retain their
multiplicity in the sorted name multiset for between-pass comparison.
Malformed/unterminated/invalid-UTF-8 names reject OBSERVATION_MISMATCH/3.

Only two allowlisted values may be interpreted internally: repository format,
through Git --type=int, must produce exactly `0\n`; when the extension key
exists, Git --type=bool must produce exactly `true\n` or `false\n`.
Git's canonical boolean conversion accepts its documented lexical spellings;
no Python truthiness, bespoke coercion or last-value-wins is permitted.
Missing extension means null and skips the boolean child. It is distinct from
explicit false. Compare the normalized state with the bound JSON value using
strict types. Wrong normalized boolean/absence is OBSERVATION_MISMATCH on
the first pass; format other than zero is STATE_UNSUPPORTED. Missing/repeated
format or repeated extension rejects at config.names before value probes.
Invalid boolean/integer causing nonzero Git exit preserves GIT_EXIT and its
native code; malformed successful value output is OBSERVATION_MISMATCH.

No raw names, values, child output or configuration contents enter results.
Process evidence remains only digest/byte-count/exit/completeness. This narrow
value parsing is a versioned exception to v2's names-only rule, not permission
to dump config or inspect arbitrary values.

## W3 — Drift, guard order and fixed budgets

[The v3 process plan](plan.md#v3-candidate-process-plan) is normative.
The initial full physical scan includes config_worktree absence before the
first config child. After config-name/value guards, recheck common-config
bytes/metadata and principal absence before the first dependent root probe,
in each observation. A change stops before that dependent probe. Two extra
config-only scans have a 16 MiB cap each and count toward a fixed total
224 MiB physical hashing ceiling (three 64 MiB full scans plus two 16 MiB
config scans); they are not extra worktree/index scans. All existing scan,
input, stream, directory, blob, timeout and output-envelope caps remain fixed.

The between/final full scans also check principal absence. Initial expected
absence mismatch follows W2; later appearance/disappearance, type/identity/
mode/content changes or config hash/metadata change is OBSERVATION_DRIFT/3,
without opening a newly present config.worktree. Compare only explicit
dev/inode/mode/nlink/size/mtime_ns/ctime_ns tuples in memory; never atime or a
global stat_result. Preserve integer nanoseconds, not floating-point transport.
Unsafe initial config fails before dependent reads; drift never rebinds inputs.

Two successful observations have 10+B+N children each: B is 0 for bound null,
1 for a bound boolean; N is len(staged). Total is 20+2B+2N, at most 86.
No child is skipped except the declared absent-key boolean probe; no duplicate
blob is deduplicated. Existing first-failure and no-successor rules apply.
Config name/state mismatch prevents later probes; a changed second canonical
name multiset stops at after.config.names. Structural unsupported names remain
STATE_UNSUPPORTED; malformed streams remain OBSERVATION_MISMATCH. A changed
valid normalized boolean in the second pass is OBSERVATION_DRIFT.

These scans are not atomic. Exclusive use/trusted tools remain prerequisites;
ABA and adversarial races remain outside assurance. Do not claim prevention
of every concurrent config read merely because subsequent scans detect drift.

## W4 — Candidate result-v3 and completion

Use exactly R4's top-level fields and process-record shape, replacing only
schema_version with `yini-readonly-preflight/result-v3`. On MATCH the closed
fingerprint is exactly the v2 fingerprint plus repository_format_version,
extension_worktree_config and config_worktree, strictly equal to verified
input. Require exit 0, MATCH reason/outcome, null failed_step/child_returncode,
20+2B+2N complete ordered exit-0 records and successor_authority=false.
STOP always has fingerprint null; preserve all preceding/incomplete process
records and existing reason/exit pairs. New step IDs are only those in plan.md.
No timestamps, durations, raw values or silent result-v2 substitution.

| AC | Candidate v3 outcome |
|---|---|
| WAC1 | Legacy v1/v2 schema, rejection and exact-result behavior preserved |
| WAC2 | Closed v3 schema binds principal absence, normalized extension state and format 0 |
| WAC3 | Unsafe/present config, duplicate keys and all remaining exclusions fail before dependent observations |
| WAC4 | Fixed guard order, process/resource bounds and drift rules hold without config mutation |
| WAC5 | Both public seams produce exact deterministic versioned results and no successor |
| WAC6 | Spec, implementation, review, owner acceptance and adoption retain separate gates |

W01–W10 in validation.md trace these criteria. These are proposed acceptance
requirements, not current acceptance or execution evidence.
