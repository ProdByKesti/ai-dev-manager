# Development work profile

**Status: Effective only after separately authorized integration; this document does not authorize execution.** This amendment supplements [development rules](development-rules.md) and [quality and evidence](quality-evidence.md). It does not override AGENTS.md, approved product decisions, INV-01–INV-12, K01–K18, ADRs, or mandatory acceptance and integration rules.

## Exploratory functional development

A maintainer-approved work order identifies the package, accountable specialist, source and target revisions, worktree, permitted paths, environments, operations, external effects, dependencies, budget, evidence and stop conditions, together with explicit maintainer authorization and documented acceptance of the identified execution risks. Within that scope the specialist may make ordinary implementation edits, compile, run approved tests, and repair technical errors without a new work order or separate approval for each minor edit. A new environment, execution class, dependency source, sensitive external action, paid service, privilege increase, or change outside that scope requires the applicable prior authorization.

Use disposable environments where execution of dependencies or generated code is authorized. Scope credentials and network access to the work order; use synthetic data, no repository or environment secrets, no write-capable token, and approved dependency sources unless a separate work order expressly authorizes more. A worktree or disposable VM is not a security boundary. No real inference with unknown quota, autonomous permission escalation, unsafe fallback or self-waiver. Dangerous product capabilities remain disabled until their required security controls are implemented and validated.

Track execution, provisioning and repair budgets cumulatively in a durable coordinator-controlled ledger across attempts, commits, branches, sessions, specialists and restarts. The work order specifies limits and counts a start before external execution. Stop on exhausted or unknown budget, unknown costs, unexpected permissions or sources, security-critical deviations, uncertain external effects or identity drift. Reconcile ambiguous effects before any retry; do not retry automatically after security-critical or uncertain effects. A profile cannot grant its own rights.

## Mandatory validation

Exploratory compilation or test results are observations tied to the exact candidate, environment, policy and attempt; they do not automatically satisfy mandatory quality or security gates. Preserve original evidence and failures, including commands, exit codes, applicable test counts, candidate and runner identity, relevant policy revision, budget consumption and limitations, without secrets or private data. A required skipped, failed, invalidated or inconclusive gate remains unpassed. Protect the test baseline, evidence and integration metadata.

Independent review is required where the work order or approved policy requires it, especially for security boundaries, sandbox or credential handling, execution permissions, protected tests, gate definitions and evidence capture. A different specialist reviews the actual candidate; author review is not independent. Ordinary in-scope repairs may proceed within budget without repeating independent review for each edit. Repairs affecting protected security boundaries or mandatory evidence require applicable independent review before reliance, and all required final candidate reviews remain mandatory. Reviews and human decisions remain separate.

## Integration and release

Revalidate the actual integration candidate and target after changes; obtain required independent review and explicit human acceptance and integration authorization. Preserve ADR-011 and all mandatory gates. Release requires its own independent validation, evidence and explicit authorization. A successful exploratory build is neither product-security validation nor integration or release approval.
