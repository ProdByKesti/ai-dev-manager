# ADR-001: Technology stack

Status: accepted design decision; implementation and verification pending.

## Decision

Tauri 2, Rust, Tokio, SQLite/SQLx, React, TypeScript, Vite, Tailwind, Serde/JSON and JSON-RPC; Python for auxiliary tools; Git and Linear adapters.

## Rationale

A local desktop platform with a typed, asynchronous core and a small operational footprint. Keep dependencies replaceable rather than hard-code provider details.

## Consequences and verification

Rust/Cargo, Windows C++ build tools, WebView2 and actual library compatibility/builds remain to verify. No empty implementation crates during documentation.

Roadmap ownership: M00-05, M01.

All applicable [system invariants](../system-invariants.md) and [consolidation amendments](../consolidation.md) apply. Provisional limits are targets or defaults, not measured results. No security downgrade or automatic additional cost is authorized by this decision.
