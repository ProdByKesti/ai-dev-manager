# T02 — App Server transport

Status: Demonstrated within probe. Historical feasibility investigation completed; production acceptance not implied.

Evidence basis: reconstructed from retained Phase 0 test summaries and reported historical observations. Raw logs, scripts and complete original console transcripts are not available in this documentation pass. No new execution was performed; the report is not independently reproduced evidence. Private paths, identifiers, account data and credentials are intentionally omitted.

## Objective

Validate local JSON-RPC communication with Codex App Server.

## Reported observations

A Python harness launched cmd.exe /d /c codex.cmd app-server --stdio. Newline-delimited JSON transport, initialize with clientInfo, initialized notification and account/read with refreshToken false were successful. The response indicated ChatGPT authentication and Plus plan type.

## Design implications

Use supervised stdio transport with request correlation, lifecycle and error handling. No account credentials or full account responses are published.

## Limitations and required validation

Production framing, malformed messages, timeouts, concurrent requests, stderr handling, authentication events and native Linux transport in authenticated operation require further testing.

Roadmap ownership: M02-05, M02-06.

See the [validation matrix](validation-matrix.md) and [open technical risks](open-technical-risks.md).
