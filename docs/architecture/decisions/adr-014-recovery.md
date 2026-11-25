# ADR-014: Recovery engine

Status: accepted design decision; implementation and verification pending.

## Decision

Typed deterministic error classification, persistent checkpoints, bounded retries with backoff/jitter, verify ambiguous external effects, startup reconciliation and consistent backups. Preserve uncommitted work and escalate unknown or critical states.

## Rationale

Avoid blind retries, destructive recovery and false claims of restored inference state.

## Consequences and verification

Checkpoints cover approval, workspace, run, implementation, validation, acceptance and integration. Daily backups if running, pre-migration/update backup; proposed 7 daily/4 weekly and 2 GB target subject to last verified recovery basis. Abrupt failure and restore remain to test.

Roadmap ownership: M07, M10, M12.

All applicable [system invariants](../system-invariants.md) and [consolidation amendments](../consolidation.md) apply. Provisional limits are targets or defaults, not measured results. No security downgrade or automatic additional cost is authorized by this decision.
