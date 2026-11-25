# ADR-015: Distribution and extension strategy

Status: accepted design decision; implementation and verification pending.

## Decision

Apache-2.0, guided Windows installer, verified signed updates, GitHub releases/CI, semantic versioning, optional later public plugin SDK and hosting. Telemetry off by default.

## Rationale

Keep local use independent of mandatory ADM subscription or server; publish measured evidence and limitations.

## Consequences and verification

Verify public provider terms/auth, signing, clean install, runtime setup, license compatibility and costs. Update signatures do not replace Windows code signing. No unsupervised release, admin changes or paid fallback.

Roadmap ownership: M00, M11, M13.

All applicable [system invariants](../system-invariants.md) and [consolidation amendments](../consolidation.md) apply. Provisional limits are targets or defaults, not measured results. No security downgrade or automatic additional cost is authorized by this decision.
