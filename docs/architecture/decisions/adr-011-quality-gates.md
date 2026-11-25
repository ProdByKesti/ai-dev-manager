# ADR-011: Evidence-based quality gates

Status: accepted design decision; implementation and verification pending.

## Decision

Versioned requirements and risk-specific gates: deterministic tests, protected test baseline, independent review where required, integration candidate validation and human acceptance when required. Evidence tied to commit, environment and policy revision.

## Rationale

Agent success claims and exit zero alone cannot establish completion.

## Consequences and verification

Missing, skipped, invalidated or inconclusive mandatory tests block completion. Bounded repairs share budgets. No self-waiver; no integration of a changed candidate without revalidation.

Roadmap ownership: M06, M10.

All applicable [system invariants](../system-invariants.md) and [consolidation amendments](../consolidation.md) apply. Provisional limits are targets or defaults, not measured results. No security downgrade or automatic additional cost is authorized by this decision.
