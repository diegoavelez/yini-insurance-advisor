# Staged Preflight and Publication — Plan

## Current documentary plan

Objective: prepare the five-document Level 2 proposal without implementation.
Affected paths: only spec.md, requirements.md, plan.md, tasks.md and validation.md
in this directory. Assumptions: principal checkout, exclusive use, exact initial
five foreign files and unchanged main/HEAD/raw index with empty staging.
Risks: version confusion, conflating staged/worktree bytes, hidden helpers,
incomplete maps, races, fabricated OIDs and accidental successor authority.

Sequence: inspect canonical/code/test sources; one exact v1 observer invocation;
author the five documents using apply_patch; verify UTF-8/LF/whitespace,
conflicts/links, cross-document agreement, allowlist and final fixed point.
No product suite or second observer invocation. Read allowance: 100 calls,
140 captured pages; no artificial hard 100-line rule. Recover only missing
read-only source ranges within that allowance. Stop on actual drift, unsafe
failure, write error or material scope conflict.

## Future minimal implementation footprint

New code: `scripts/staged_readonly_preflight.py`.
New tests: `tests/test_staged_readonly_preflight.py`.
Keep `scripts/readonly_preflight.py`,
`tests/test_readonly_preflight.py` and v1 contracts unchanged.
Use Python standard library and unittest with invented OS/process fixtures;
no app imports, pytest plugins, dependency installation or real Git mutators.

The implementation is a single bounded observer with private schema, physical
scan, process capture, index/raw-diff parsing and serialization helpers. No
generic runner or publication executor. Publication/permission assertions are
documentary scenario checks, not claims of runtime authority enforcement.

## V2 immutable process plan

Every child starts with the contract-bound physical Git binary and this prefix:

```text
--no-pager --no-optional-locks
-c core.fsmonitor=false
-c core.untrackedCache=false
-c core.hooksPath=/dev/null
-c diff.external=
```

Use shell=False, stdin=DEVNULL, byte streams, exact already-observed cwd and
the v1 R3 fixed minimal environment. The only variable arguments are validated
full OIDs, never paths or arbitrary command text. Reject unsafe object-storage
layout before children; config key guards precede status/object access.

| Step | Fixed work or argv suffix |
|---|---|
| input | CLI, stdin cap, raw digest, JSON, exact schema and row relationships |
| environment | -B and inherited-Git-variable guards; construct minimal environment |
| paths | all physical/path/storage guards before content reads |
| before.index | hash index/config/executable/worktree/absence, compare bound identities |
| before.root | rev-parse --show-toplevel |
| before.common | rev-parse --path-format=absolute --git-common-dir |
| before.branch | symbolic-ref --quiet --short HEAD |
| before.head | rev-parse --verify HEAD^{commit} |
| before.config | config --local --no-includes --null --name-only --list |
| before.shared | rev-parse --shared-index-path |
| before.entries | ls-files --stage -v --sparse -z |
| before.status | status --porcelain=v1 -z --untracked-files=all --ignore-submodules=none |
| before.staged | diff --cached --raw -z --no-abbrev --no-renames --no-ext-diff --no-textconv --ignore-submodules=none HEAD -- |
| before.blob.000 through before.blob.031 | cat-file blob <index_oid>, one per staged path in contract order, only N steps |
| after.paths | recheck environment, cwd, physical and storage guards |
| after.index | second physical scan; compare bytes and metadata with initial scan |
| after.root through after.blob.NNN | identical nine fixed probes plus N blob reads, same order |
| final.files | third physical scan, including config, index and storage guards |
| result | validate complete result-v2; emit canonical JSON and actual exit |

Scalar outputs require exactly the expected value plus LF. Shared output must
be zero bytes. Config output is NUL-terminated key names; an empty config list
is permitted, a prohibited key is STATE_UNSUPPORTED. Parse index records as
`H SP mode SP oid SP 0 TAB path NUL`; complete raw/index/status maps are
compared independent of record order. Reject duplicate/conflicting records
before canonicalization. Raw diff's NUL-separated header/path pairs bind the
old/new full OIDs, modes and A/M status; reject rename/copy scores and all other
statuses. After validating entries/status/diff, read only the N bound blobs.
Use independent fixtures to pin exact Git 2.40 output framing.

First failure stops all later probes. Fixed guard step IDs distinguish path
guards from content hashes and Git parsing. Final.files owns final race
failures. Per-process evidence preserves exits and incomplete streams even if
kill/reap also fails; INTERNAL_DEFECT never becomes MATCH. A stable malformed
stream remains a failure rather than a retriable transient.

## Proposed publication transitions

| State | Prerequisite and next eligible action | Required evidence / terminal stop |
|---|---|---|
| P0 bound input | Fresh task, complete grant and selected adopted mechanism; physical bootstrap | MATCH for initial contract or STOP |
| P1 stage eligible | Named stage grant or explicit compound anchoring steps; exact accepted path/blob map | One exact stage attempt, otherwise skip only when already-staged index is bound |
| P2 successor capture | Authorized stage succeeded and successor derivation was expressly named | Compare complete intended maps and protected bytes, then bind new raw index hash; unknown mapping STOP |
| P3 verified index | Bound successor contract and selected v2 invocation | Complete MATCH; observer cannot create the contract |
| P4 commit eligible | Named commit grant, exact index/HEAD continuity and runtime permission route | One commit; failure/denial/unknown effect STOP, no restage |
| P5 native identity | Successful commit plus granted read-only identity checks | Full OID, single expected parent, exact full tree and changed paths |
| P6 push eligible | Separate own push grant names P5 full OID and exact remote/ref | One transport attempt; result does not prove remote readback |
| P7 returned receipt | Observed outcome and applicable receipt class | Return to master/owner; no successor implied |

P2's controlled capture is a permitted observation of an authorized mutation,
not a new freeze operation in the observer. A stage task without that authority
returns evidence for owner-bound P3 dispatch. The pre-stage contract must not
be reused after stage. P3 from already-staged state requires its own initial
full index identity, with no stage operation.

The following postcommit read-only suffixes are proposed for a fresh grant,
using the same trusted Git/prefix/environment and bounded capture. They are
outside the v2 observer and are not executed now:

1. `rev-parse --verify HEAD^{commit}`: capture full HEX40 from native stdout.
2. `rev-list --parents -n 1 <new_oid>`: exactly new_oid plus one bound parent.
3. `rev-parse --verify <new_oid>^{tree}`: record full native tree OID.
4. `ls-tree -r -z --full-tree <new_oid>`: canonical complete regular-file
   path/mode/OID map must equal precommit index_tree_sha256.
5. `diff-tree --no-commit-id --raw -r -z --no-abbrev --no-renames --no-ext-diff --no-textconv <parent_oid> <new_oid> --`:
   exact changed path/old-new mode/OID map must equal the verified staged map.
6. Bound read-only status, raw-index and protected-file postflight. Expected
   postcommit staging is empty and XY changes are derived from the authorized
   commit; partial worktree residuals remain bound. No assertion that postcommit
   raw index bytes necessarily equal precommit bytes.

These observations each require exit 0, complete parse and exact comparison
before continuing. Scalars/metadata use v2 ordinary caps; ls-tree uses the
2 MiB/8192-entry bound. Observe HEAD before and after this sequence; race or
divergence from new_oid stops. Native OID capture is not prefix expansion.
No tree object is written by validation.

## Future adoption scope and timing

After implementation evidence, independent review and owner acceptance, a
fresh exact O1 documentary grant must name these canonical paths:

- `docs/agents/executor-workflow.md`: coverage-based preflight selection and
  publication transition pointer; mandatory use only after accepted adoption.
- `specs/2026-09-15-executor-checkout-boundary/plan.md`: prospective pointer
  amendment linking the selection rule while preserving historical recipes.
- `docs/operations/execution-state.md`: stable semantic work/evidence/next
  gate update when warranted by owner-disposed delivery state.
- `specs/roadmap.md`: bounded follow-on status pointer when that semantic
  status changes; no transient HEAD/index/remote ownership.

The canonical owner remains the executor workflow. Do not edit v1
requirements, historical validation or duplicate universal grant policy.
AGENTS/master/ADR topology remains unchanged; a discovered required change
there is a new scope decision. No speculative lesson or new ledger is needed.
This task changes none of those four adoption paths.

O1's changed candidate requires its separately authorized documentary review
and owner disposition before procedural use/Git close. Semantic updates occur
before close as applicable; later push transport alone creates no reconciliation
task. Existing receipt-policy.md and receipts/index.md govern a separately
authorized sanitized publication receipt and its nonrecursive administrative
tail; this spec adds no receipt file now.

## Verification strategy and exits

I1's proposed exact affected command is:

```text
/Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor/.venv/bin/python -B -m unittest discover -s tests -p test*readonly_preflight.py
```

In shell, quote the pattern `'test*readonly_preflight.py'`; in structured argv
pass it as one literal element. It selects old/new observer tests only. Verify
runtime and fixture isolation before dispatch. Do not run make test-release,
application tests, real stage/commit/push or live staged integration under I1.
Expected public-seam RED precedes minimal GREEN; already-green cases are
reported as regressions, never fabricated REDs. Independent review is outside
the local objective. No implementation PASS authorizes adoption or publication.

## WorktreeConfig documentary amendment — 2026-09-30

Candidate objective: cover the reported principal/format-0/extension-enabled/
config.worktree-absent case without changing v1 or v2 semantics.
Current edits are append-only amendments to these same five specs. All fifteen
pre-existing delta rows are permitted; the other ten paths are protected.
Configuration identity/absence is read-only evidence, never mutation authority.
Risks are schema ambiguity, loading unbound config, races and overstating
legacy evidence. Verify documentary links/traceability/scope, then read-only
HEAD/tree/index/staged/config and protected-path preservation. No product
tests, config edit or second observer invocation.

## V3 candidate process plan

Future implementation footprint: extend only staged_readonly_preflight.py and
test_staged_readonly_preflight.py, plus actual validation evidence here under
a fresh explicit grant. Preserve the legacy v2 path and all v1 files; no
generic extraction, config migration or publication runner. Use the standard
library and invented system-boundary fixtures. This plan does not grant work.

Use R3's minimal environment, immutable Git prefix, shell=False and fixed
already-observed cwd. Let CONFIG mean the validated literal
`/Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor/.git/config`;
it is never a contract-supplied arbitrary path. All config probes use --file
and --no-includes, not effective/global/worktree config lookup.

| Order / step | Fixed action or suffix |
|---|---|
| input, environment, paths, before.index | Existing guards/full scan plus W1 schema and W2 principal config.worktree absence |
| before.config.names | config --file CONFIG --no-includes --null --name-only --list |
| before.config.format | config --file CONFIG --no-includes --type=int --get-all core.repositoryformatversion |
| before.config.worktree | Only B=1: config --file CONFIG --no-includes --type=bool --get-all extensions.worktreeConfig |
| before.config.guard | No child: recheck bound common-config bytes/metadata and principal absence against initial scan |
| before.root, common, branch, head, shared, entries, status, staged | Same eight suffixes and parsers as the v2 plan, in that order; omit its old config probe |
| before.blob.000 through before.blob.031 | N bound blob probes exactly as v2 |
| after.paths, after.index | Second complete physical scan, including principal absence |
| after.config.names, format, worktree, guard | Same config probes/guard and conditional B as before; compare names/state with input and first pass immediately |
| after.root through after.blob.NNN | Same eight dependent probes then N blob probes |
| final.files | Third complete physical scan including config identity and principal absence |
| result | Exact result-v3 validation, bound output size, canonical JSON plus LF and real exit |

Each child must exit 0 and its complete output pass before the next action.
Name guards and duplicate/cardinality checks precede format/boolean reads.
The absent-key branch checks bound null at config.names before format; it
does not run a getter that would return Git exit 1. A present-key versus bound
null mismatch also stops there. Typed probes use LF scalar framing, not NUL;
only name listing uses NUL. Full normalized state comparison precedes
config.guard. W2 owns classifications; W3 owns drift and resource ceilings.
The result records only children, never physical guard pseudo-records:
20+2B+2N <= 86. First failure cancels all later steps.

Physical path/common-config guards precede all config probes; every
configuration-dependent repository observation follows those probes and the
post-probe physical guard. No principal config.worktree is opened or allowed,
even empty; no linked config is consulted. Existing storage/name exclusions
remain active before status/object reads. A regular present-file design is
deliberately deferred, not left to the implementer.

## V3 verification and adoption boundary

Run future tests at both verify and main with independently specified
Git 2.40 framing, booleans, duplicate cases, fingerprints, process sequences
and literal output expectations. Preserve the C1 Unicode and oversized-result
regressions. Reuse the prior affected unittest discovery command only when a
fresh implementation/validation grant names it; nothing is run by this plan.

Accepting this appendix alone activates neither v3 nor O1 adoption.
After separately authorized implementation, independent review and owner
acceptance, a fresh documentary adoption task would have to update the same
four canonical owners listed above to select v3 by declared coverage.
The accepted v2 publication graph remains historical/valid in its own scope;
future use of v3 for P0/P3 requires that separately accepted selection change
and a new literal contract. No post-STOP migration or fallback is permitted.
