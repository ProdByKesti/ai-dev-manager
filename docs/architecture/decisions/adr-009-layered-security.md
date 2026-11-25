# ADR-009: Layered security

Status: accepted design decision; implementation and verification pending.

## Decision

Maximum role rights intersect global, project, agent and task restrictions; least privilege, deny by default, fail closed, risk-based approvals, scoped sandbox/brokers and separate credential storage. Treat external inputs as untrusted.

## Rationale

Prompts and worktrees do not enforce permissions. Prevent self-escalation and unsafe fallback technically.

## Consequences and verification

Threat model, WSL interop/IPC, credential boundary, child processes, Windows generated code, external tools and concurrent profiles require practical validation. No absolute security claim.

Roadmap ownership: M02, M10.

All applicable [system invariants](../system-invariants.md) and [consolidation amendments](../consolidation.md) apply. Provisional limits are targets or defaults, not measured results. No security downgrade or automatic additional cost is authorized by this decision.
