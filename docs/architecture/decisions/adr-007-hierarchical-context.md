# ADR-007: Hierarchical context

Status: accepted design decision; implementation and verification pending.

## Decision

Global/project/agent/task/session memory with structured SQLite and versioned documents. Deterministic metadata/dependency/file selection and FTS5 initially. Provenance, validation, timestamps and superseded markers; optional quota-aware summaries.

## Rationale

Preserve relevant project decisions without injecting entire histories or sharing unrelated context.

## Consequences and verification

No credentials in memory; enforce scope and prioritize current validated decisions. Semantic embeddings later, with index isolation and deletion tests.

Roadmap ownership: M04, M12.

All applicable [system invariants](../system-invariants.md) and [consolidation amendments](../consolidation.md) apply. Provisional limits are targets or defaults, not measured results. No security downgrade or automatic additional cost is authorized by this decision.
