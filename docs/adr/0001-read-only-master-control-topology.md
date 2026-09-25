# Read-only master-control topology

Yini uses a permanent, strictly read-only master control that points to
canonical registers, orients and classifies work, prepares visible tasks and
handoffs, receives receipts, and proposes owner decisions. Every implementation,
correction, formal or independent review, validation, Git, publication,
provider, deployment, pilot, production, or external action occurs in a fresh
visible task under separate authority. This trades some lifecycle handoffs for
a durable separation between coordination and execution, preventing the
control tower from silently acquiring mutation or acceptance authority.

## Consequences

Internal subagents may support only at least two independent, bounded,
non-mutating analyses and never replace visible tasks. Results, receipts, and
PASS states return to the owner; they do not auto-advance gates.

## Prospective amendment — 2026-09-25 (AOPS-YINI-ROUTING-006)

For a future grant that expressly selects the installed AgentOps local
objective bundle, one fresh visible executor task may include its separately
named, scoped implementation and affected-validation grants plus finite local
correction under `references/authority-grants.md`. The local routing owner and
task boundary remain `docs/agents/executor-workflow.md`. This does not change
the literal fresh-task terms of grants already issued, create default or
retroactive authority, or permit master control to implement, validate, or
correct. Independent review, owner acceptance, Git, provider, and external
actions remain separate authorities and tasks.
