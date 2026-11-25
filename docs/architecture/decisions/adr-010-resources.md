# ADR-010: Resource and quota management

Status: accepted design decision; implementation and verification pending.

## Decision

Deterministic admission control for all inference, hardware/resource monitoring, dynamic provider capabilities and short/long quota windows, persistent reservations and profiles. Tokio semaphores; platform measurements and sysinfo candidate.

## Rationale

Local scheduling must not consume inference; limited quotas require conservative admission and explicit budgets.

## Consequences and verification

Proposed Eco/Balanced/Performance slots 1/2/4 and quota reserves 25/15/10 percent. Start thresholds are not kill thresholds. Unknown quota holds automation; no paid fallback. Provider use/reset and WSL measurements pending.

Roadmap ownership: M02, M05, M07.

All applicable [system invariants](../system-invariants.md) and [consolidation amendments](../consolidation.md) apply. Provisional limits are targets or defaults, not measured results. No security downgrade or automatic additional cost is authorized by this decision.
