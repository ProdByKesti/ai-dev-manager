# ADR-004: Persistence and event log

Status: accepted design decision; implementation and verification pending.

## Decision

SQLite relational current state plus durable event log and transactional outbox; sole core writer; UUIDs, foreign keys, unique constraints, migrations and backups. Store secrets separately; large artifacts as references.

## Rationale

Atomic local state/event/outbox transitions support audit and recovery without full event sourcing.

## Consequences and verification

Schema, crash consistency, retention and restore must be validated. External effects are not covered by SQLite atomicity.

Roadmap ownership: M01, M07, M08.

All applicable [system invariants](../system-invariants.md) and [consolidation amendments](../consolidation.md) apply. Provisional limits are targets or defaults, not measured results. No security downgrade or automatic additional cost is authorized by this decision.
