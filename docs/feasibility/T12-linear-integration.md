# T12 — Linear integration

Status: Partial feasibility. Historical feasibility investigation completed; production acceptance not implied.

Evidence basis: reconstructed from retained Phase 0 test summaries and reported historical observations. Raw logs, scripts and complete original console transcripts are not available in this documentation pass. No new execution was performed; the report is not independently reproduced evidence. Private paths, identifiers, account data and credentials are intentionally omitted.

## Objective

Exercise Linear GraphQL operations and conflict/deduplication handling in an isolated test workspace.

## Reported observations

Historical T12a–g probes used a personal API key and three synthetic test issues in a dedicated feasibility project. Authentication, create/import, two-way status changes, append-only progress comments, unconfirmed creation reconciliation, UUID-based deduplication and conflict handling were exercised. See details below.

## Design implications

Use a durable outbox, stable external mappings, explicit field authority, three-way comparison and verify-before-retry. Preserve existing history; keep the feasibility workspace separate from production.

## Limitations and required validation

Public OAuth, persistent recovery, concurrent external writes, rate limits, long-running synchronization and public distribution remain open. No exactly-once guarantee.

Roadmap ownership: M08-02 to M08-14, M11-02.

See the [validation matrix](validation-matrix.md) and [open technical risks](open-technical-risks.md).

## Historical test setup and observations

A separate free Linear workspace/team and feasibility project were used, with three synthetic issues representing status/comment history, conflicts and deduplication. The production projects were not modified. API credentials, workspace IDs, issue IDs and comment IDs are not included. The historical issues were reported returned to Backlog.

The retained summary groups T12a–g as follows; the exact mapping of individual lettered probes to every API operation is not available and is not invented here:

| Area | Reported result |
| --- | --- |
| Authentication and discovery | GraphQL with a personal API key succeeded; synthetic issues could be created and read/imported. |
| Bidirectional status | Status changed in both directions in the controlled test. |
| Progress reporting | Two synthetic progress comments appended; previous comments and selected existing fields preserved. |
| Unconfirmed create | A real unconfirmed create was reconciled rather than blindly repeated. Markdown escaping of brackets affected marker matching; matching the operation token independently of formatting resolved the issue. |
| Deduplication | Repeated UUID-based upserts reconciled the intended synthetic issue. |
| Three-way conflict logic | 5/5 controlled cases passed; a stale mutation was blocked before sending. |
| Conflict resolution | Simulated KEEP_LINEAR resolution exercised and original test state restored. |

These are reported historical outcomes, not a new GraphQL session. Local state in the feasibility harness was in memory; no production SQLite outbox or crash recovery was established. The remote API cannot be assumed to offer atomic compare-and-set semantics for the tested mutations; a race between preflight and write remains possible. Add post-write verification and explicitly surface ambiguous state. Never assert exactly-once delivery from these probes.

## Required future checks

Public OAuth with permitted scopes and revocation, protected token storage, durable mappings/outbox across restart, pagination and rate-limit handling, unconfirmed mutation recovery, concurrent conflict handling, external field ownership and preserving history. Existing Linear projects remain authoritative for agreed external fields only; external completion cannot bypass ADM internal quality gates. Use a dedicated test project for real integration tests, never production data without authorization.
