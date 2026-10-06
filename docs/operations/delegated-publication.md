# Delegated Publication Handoff

Status: candidate operational checklist, inactive pending independent
documentary review and owner acceptance of these exact bytes. This document
grants no action; the existing effective executor workflow remains in force.

## Owners

- Authority, task boundaries, and failure/retry rules: repository `AGENTS.md`,
  [`executor-workflow.md`](../agents/executor-workflow.md), and the installed
  AgentOps `references/authority-grants.md`.
- Preflight selection and publication transitions:
  [`staged-preflight-and-publication`](../../specs/2026-09-29-staged-preflight-and-publication/plan.md#proposed-publication-transitions)
  and its [requirements](../../specs/2026-09-29-staged-preflight-and-publication/requirements.md).
- Current semantic work and next owner decision:
  [`execution-state.md`](execution-state.md).
- Terminal receipt format and retention:
  [`receipt-policy.md`](receipt-policy.md) and
  [`receipts/index.md`](receipts/index.md).

## Master dispatch checklist

Before dispatch, bind the exact owner authorization source, executor task,
physical checkout/common-dir, starting full HEAD/tree, exact action and path
allowlist, staged and foreign state, expected path/blob map, required
read-only checks, runtime route, evidence required on return, and terminal
stops. For a commit, bind the expected parent and resulting tree/path check.
For a push, bind the full local OID, remote identity, credential-free effective
endpoint, target ref, and allowed transport. Resolve executable identities and
required source artifacts before spending a one-shot action grant. Do not
copy large contracts or repeat the linked documents here.

Normal named runtime permission review remains independent of owner
authorization. Use only its normal route for the exact granted effect; denial
ends the attempt without repeated escalation, Full Access/config changes, or
bypass. This checklist does not establish trusted reviewer context or approval.

## Executor return

Report only observed checkout/fixed-point facts, action and authority actually
used, exact changed-path delta, native command exits/results, runtime decision
if one occurred, evidence ceiling, unresolved gaps, and next owner decision.
Keep local continuity, commit identity, push transport, remote readback,
provider health, deployment, and acceptance distinct. Preserve foreign state.

Any mismatch, denied permission, Git write failure, interruption with unknown
effect, or drift ends that attempt under its grant. Incomplete retained
read-only output may be completed only through the existing bounded capture
rule in the executor workflow, in the same task and without replaying its
producer; if the required range is unavailable or the budget is exhausted,
stop. No helper fallback, rebinding, automatic retry, or successor action
follows.
