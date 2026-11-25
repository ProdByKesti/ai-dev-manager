# ADR-006: Deterministic scheduler

Status: accepted design decision; implementation and verification pending.

## Decision

Approved, structured AI-generated plans feed a deterministic Rust DAG scheduler. Validate cycles, priorities, dependencies, quality gates, workspace compatibility and resource reservations. Escalate blockers and approval-sensitive changes.

## Rationale

Planning may be probabilistic; dispatch and state transitions must be auditable and deterministic.

## Consequences and verification

Scheduling needs no inference. Baseline quota guard before live execution; parallel work requires M05-10 before M05-09. Exact state transitions are specified during implementation.

Roadmap ownership: M03, M05.

All applicable [system invariants](../system-invariants.md) and [consolidation amendments](../consolidation.md) apply. Provisional limits are targets or defaults, not measured results. No security downgrade or automatic additional cost is authorized by this decision.
