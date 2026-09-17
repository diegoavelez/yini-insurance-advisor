# Deterministic Read-Only Preflight — Tasks

## S1 — Specification candidate (current authority)

Create only the five documents in this directory. Read applicable contracts,
verify exact starting point, preserve five foreign files, and run only static
document checks plus authorized postflight. Return hashes and
`READY_FOR_OWNER_SPEC_DECISION` when verified. No implementation or TDD run.

## I1 — Bounded implementation (proposed, ungranted)

Prerequisites: owner accepts this exact spec and separately grants a fresh
visible implementation task with route, physical checkout, new live fixed
point, complete foreign manifest, exact code/test allowlist, selected unit
command, bounds and stops. Master dispatches; executor never redelegates.

Deliver the following vertical public-seam RED → minimal GREEN cycles in
order. Each includes the preceding regressions; expected fixtures are authored
independently from production tables/serializers. No horizontal all-tests-first
batch, real mutator, provider call, or product-test run.

| Cycle | Observable public behavior and required evidence |
|---|---|
| 1 | CLI rejects unknown operations (including write-tree, add, update-index and shell-substitution text), raw argv options, malformed JSON/hash/schema/path inputs, inherited Git redirects and unsupported checkout before subprocess; spy count exactly zero |
| 2 | verify hashes known physical raw index bytes, compares delta mode/content/absence, and never invokes Git to derive an index digest; literal SHA-256 vector independent of implementation; byte/mode/index mismatch stops before subprocess |
| 3 | main propagates a stubbed Git exit 128 exactly and starts no later call, even when a tempting later success is queued; signal/launch/timeout/capture failures likewise STOP; immutable argv, shell=False and complete sanitized environment asserted independently |
| 4 | Matching nonempty candidate including tracked-first and nested-untracked status passes both observations; missing/extra/duplicate/malformed/renamed records, staging, branch/HEAD/root/common-dir or between-observation drift fail; repeat identical input yields byte-identical complete JSON and exit 0 only for MATCH |

Required negative cases within each cycle are listed in validation.md. Mock
only actual subprocess/filesystem boundaries, never verify, its guards, its
result, or its parser. Use main with fake stdin/stdout to test returned exit
and JSON together. Process fakes must model individual outputs, exits and
chunked timeout/overflow behavior, not provide a predeclared final PASS.

## R1 and A1 — Review and acceptance (proposed, ungranted)

Independent review receives the exact resulting candidate in a fresh visible
task, checks specification mapping and the zero-subprocess/error-propagation
negative matrix, and reports findings or PASS. Owner alone accepts delivery.
Any correction needs its own named scope and fresh task. Unit evidence is not
live repository integration, global enforcement or provider evidence.

## O1 — Operational adoption (proposed, ungranted)

After validated and accepted delivery, separately authorize the minimal
canonical executor-workflow and old-recipe pointer changes before operational
use. Name any live read-only integration check explicitly, including expected
contract bytes/hash and complete candidate. Until then, no mandatory mechanism
claim or readiness continuation is made. Git publication remains separately
authorized; no stage, commit, push or transport is implied by adoption.

The next recommended owner gate may group S1 acceptance and I1 authorization
as separately named grants. R1/A1/O1 remain later decisions; this list creates
no standing authority or automatic progression.
