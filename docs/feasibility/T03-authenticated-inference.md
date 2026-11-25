# T03 — Authenticated inference

Status: Demonstrated within probe. Historical feasibility investigation completed; production acceptance not implied.

Evidence basis: reconstructed from retained Phase 0 test summaries and reported historical observations. Raw logs, scripts and complete original console transcripts are not available in this documentation pass. No new execution was performed; the report is not independently reproduced evidence. Private paths, identifiers, account data and credentials are intentionally omitted.

## Objective

Verify real inference through the existing authenticated Windows Codex session without supplying an API key.

## Reported observations

The harness removed OPENAI_API_KEY and CODEX_API_KEY from the child environment, started a temporary read-only ephemeral thread with approval policy never, and requested an exact DEV_MANAGER_OK reply using gpt-6.1-terra. The reported response matched. The existing account authentication was used.

## Design implications

A successful Windows inference probe supports the initial provider choice. It does not establish that a public third-party app can redistribute this flow or that all requests are free.

## Limitations and required validation

Public provider terms, public account onboarding, actual billing behavior, protected credentials, authenticated native Linux inference and quota exhaustion remain open. No automatic paid fallback.

Roadmap ownership: M00-05, M02-06, M02-13, M11-02.

See the [validation matrix](validation-matrix.md) and [open technical risks](open-technical-risks.md).
