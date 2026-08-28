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
