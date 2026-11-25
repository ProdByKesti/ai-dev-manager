# ADR-005: Agent identity and sessions

Status: accepted design decision; implementation and verification pending.

## Decision

Separate role, persistent agent identity, provider session and execution run. Configurable provider/model/effort/environment, temporary specialists and validated context handovers; adaptive safe session rotation.

## Rationale

Retain continuity without tying a long-lived agent to one chat or provider session.

## Consequences and verification

Proposed default 12 completed tasks per session, one concurrent turn per session, rotate only at safe boundaries. Transient failures do not automatically rotate; actual provider resume behavior requires testing.

Roadmap ownership: M04.

All applicable [system invariants](../system-invariants.md) and [consolidation amendments](../consolidation.md) apply. Provisional limits are targets or defaults, not measured results. No security downgrade or automatic additional cost is authorized by this decision.
