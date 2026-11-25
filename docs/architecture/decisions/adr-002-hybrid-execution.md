# ADR-002: Hybrid execution

Status: accepted design decision; implementation and verification pending.

## Decision

Windows desktop first; native Linux Codex under WSL2 for autonomous execution; explicitly authorized controlled Windows operations for platform-specific needs. Modular execution adapters; no automatic downgrade.

## Rationale

Preliminary Linux sandbox tests offer stronger scoped filesystem controls than the tested native Windows environment. Keep platform-specific execution separate.

## Consequences and verification

Authenticated Linux inference, credential and host isolation, WSL interop/mounts, concurrent profiles, Git/toolchain integration and Windows broker trust remain release gates.

Roadmap ownership: M02, M10.

All applicable [system invariants](../system-invariants.md) and [consolidation amendments](../consolidation.md) apply. Provisional limits are targets or defaults, not measured results. No security downgrade or automatic additional cost is authorized by this decision.
