# ADR-012: Integration adapters

Status: accepted design decision; implementation and verification pending.

## Decision

Rust adapter contracts, canonical model, central sync engine, durable mappings/outbox, three-way conflicts and verify-before-retry. Configurable directions and field authority; Codex/Git/Linear P0, GitHub/MCP P1, others later.

## Rationale

Support optional external services without coupling task truth to any one provider.

## Consequences and verification

Linear owns agreed imported fields, not internal quality gates; append history, preserve IDs. External writes cannot be assumed atomic or exactly-once. Public auth and race/recovery tests pending.

Roadmap ownership: M08, M11, M12.

All applicable [system invariants](../system-invariants.md) and [consolidation amendments](../consolidation.md) apply. Provisional limits are targets or defaults, not measured results. No security downgrade or automatic additional cost is authorized by this decision.
