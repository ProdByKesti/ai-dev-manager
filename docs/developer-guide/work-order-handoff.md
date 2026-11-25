# Work orders and context handoff

M00-06 — practical templates for the central coordinator and seven specialist chats. Activate specialist chats only as needed; initialize with the current approved repository, working directory, branch/worktree and relevant documents. Actual local setup is a separate M00-09 task.

## Work order template

```text
Package ID and title:
Target specialist chat (existing or new):
Work-order number for this chat:
Selected model / thinking effort:
Repository / working directory:
Approved base commit / branch / worktree:
Objective and in-scope changes:
Out of scope / protected paths:
Relevant source documents and dependencies:
Allowed tools / operations / external side effects:
Resource, inference and retry limits:
Acceptance criteria and required checks:
Independent review / human acceptance requirements:
Expected deliverable and report format:
Stop conditions:
```

The coordinator selects the model and effort for the task; agents do not substitute models/providers or change budgets without authorization. Historical provider model names are not guaranteed to remain available. Prefer focused low-context work orders, deterministic checks and an effort level appropriate to complexity. State if a specific setting cannot be used. Do not invent a default model as a public product requirement.

## Specialist result template

```text
Package / work-order number:
Status (blocked / implementation ready / validation / review / acceptance / etc.):
Repository / worktree / branch / base / candidate commit:
Scope actually changed:
Files changed and why:
Validation evidence (commands, environment, counts, exit codes, artifacts):
Review findings and repairs:
Unexecuted checks / limitations:
Security, cost, dependency or external side effects:
Remaining work and blockers:
Integration readiness / authorization state:
Linear update status (if configured):
Context handoff:
```

Report only observed facts, including unsuccessful attempts and uncertainties. Never declare a package completed on behalf of the maintainer before required gates and integration are verified. Avoid full raw logs; give a concise sanitized summary and evidence references.

## Context handoff and rotation

The coordinator tracks work orders per specialist chat and explicitly notes existing/new chat in each assignment. Rotate proactively when context becomes large, stale, contradictory or unreliable, or a safe configured count is reached. Prefer completing the current bounded work order or checkpointing it explicitly before rotation. Do not automatically rotate solely due to a transient failure.

A validated handoff includes current repo/base/branch/worktree, package and status, decisions and applicable rules, changed files, actual evidence, unresolved defects, open approvals, pending side effects, remaining budgets and the next authorized action. Check the handoff against the current Git state and relevant versioned sources before continuing. Preserve old chat history; no blind replay of prior commands.

The manual development-chat counter is distinct from future ADM persistent agent identities, provider sessions and execution runs. ADR-005 documents the proposed product session default of 12 completed tasks; it does not impose a hard-coded manual Codex chat limit. Session replacement never resets cumulative task budgets or grants new permissions.

## Progress tracking

Once the production Linear project exists, use the stable package ID to find the existing issue, verify its current state and append accurate progress/evidence without overwriting unrelated history or creating duplicates. If sync is unavailable, record the pending update and reconcile later. Before M00-07 setup, keep coordination in the authorized repository/chat and do not mutate feasibility or unrelated projects. See [development rules](development-rules.md), [Git workflow](git-workflow.md) and [quality evidence](quality-evidence.md).
