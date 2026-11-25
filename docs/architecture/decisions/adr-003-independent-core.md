# ADR-003: Independent modular core

Status: accepted design decision; implementation and verification pending.

## Decision

Modular monolith Rust core as an independent background process; separate Tauri desktop and tray; secured local IPC; separate execution workers. Core owns services and event bus.

## Rationale

UI closure or a frontend failure must not inherently stop execution; avoid distributed complexity in MVP.

## Consequences and verification

Windows named pipes with restricted ACL and additional client authorization are candidates, not a proven boundary against unrestricted same-user processes. Explicit shutdown and process supervision require testing.

Roadmap ownership: M01, M07.

All applicable [system invariants](../system-invariants.md) and [consolidation amendments](../consolidation.md) apply. Provisional limits are targets or defaults, not measured results. No security downgrade or automatic additional cost is authorized by this decision.
