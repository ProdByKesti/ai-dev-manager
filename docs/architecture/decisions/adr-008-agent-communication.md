# ADR-008: Agent communication

Status: accepted design decision; implementation and verification pending.

## Decision

Typed JSON messages routed by core; Tokio notifications and durable SQLite inbox/records. IDs, correlations and authorized routing for handovers, questions, results, blockers and change/review requests.

## Rationale

Allow agent coordination without uncontrolled direct access or endless conversations.

## Consequences and verification

Default cross-project deny. Proposed per-task limits: 3 question rounds, 8 automated technical messages, 4 extra communication inference calls and 1 temporary specialist; cumulative across retries. Verify delivery and recovery.

Roadmap ownership: M04, M05.

All applicable [system invariants](../system-invariants.md) and [consolidation amendments](../consolidation.md) apply. Provisional limits are targets or defaults, not measured results. No security downgrade or automatic additional cost is authorized by this decision.
