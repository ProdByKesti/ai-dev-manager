# System invariants

Approved cross-cutting requirements (Phase 3.1). These apply to every work package; AGENTS.md and implementation policies will reference them.

## INV-01 — Human Authority

Agents cannot create their own security rights or binding human approvals.

## INV-02 — Fail Closed

Unknown or invalid security state blocks the affected action.

## INV-03 — Least Privilege

Grant only rights required for approved work.

## INV-04 — No Unauthorized Costs

No automatic paid provider fallback or additional paid service.

## INV-05 — Evidence over Claims

Agent statements do not replace executed mandatory checks.

## INV-06 — Protected Integration

Only adequately verified and authorized candidates may be integrated.

## INV-07 — Persistent Traceability

Persist relevant tasks, approvals, state transitions and external operations.

## INV-08 — Bounded Automation

Enforce persistent execution, retry, repair and communication budgets.

## INV-09 — Project Isolation

Keep projects, contexts, workspaces and credentials within authorized scope.

## INV-10 — Non-destructive Recovery

Verify ambiguous state before retry; preserve work.

## INV-11 — Local-first Independence

Local basic functions require neither inference, hosting nor optional integrations.

## INV-12 — Verified Public Releases

Require independent validation, evidence and authorized release approval.

A documented rule is not technical enforcement. Validate each relevant invariant in the applicable runtime, test suite and release scope. Unknown or unverified security states must not be marked passed.
