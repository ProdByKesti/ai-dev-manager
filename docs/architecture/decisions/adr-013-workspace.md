# ADR-013: Workspace architecture

Status: accepted design decision; implementation and verification pending.

## Decision

Modular dashboard, planner, roadmap, tasks, agent chats/sessions, quality, repository, memory, activity, resources, recovery, security and integrations. Global project switch, attention center and tray. Standard/Expert share backend.

## Rationale

Expose a coherent desktop workflow without requiring a terminal for normal MVP use.

## Consequences and verification

Candidates: shadcn/ui, Lucide, React Router, Zustand, TanStack Query, React Flow, i18next, Vitest, Testing Library and Playwright plus native desktop tests. Verify compatibility, accessibility, safe rendering, state isolation and resource use.

Roadmap ownership: M01, M09.

All applicable [system invariants](../system-invariants.md) and [consolidation amendments](../consolidation.md) apply. Provisional limits are targets or defaults, not measured results. No security downgrade or automatic additional cost is authorized by this decision.
