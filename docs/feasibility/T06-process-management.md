# T06 — Process management

Status: Demonstrated within probe. Historical feasibility investigation completed; production acceptance not implied.

Evidence basis: reconstructed from retained Phase 0 test summaries and reported historical observations. Raw logs, scripts and complete original console transcripts are not available in this documentation pass. No new execution was performed; the report is not independently reproduced evidence. Private paths, identifiers, account data and credentials are intentionally omitted.

## Objective

Capture process lifecycle, output and exit status.

## Reported observations

Controlled subprocesses returned exit codes 0 and 7. A PowerShell wrapper propagated the native exit status using ; exit $LASTEXITCODE. Process output streams and controlled lifecycle were observed.

## Design implications

Capture exit code and streams as evidence; preserve native exit status when using a shell wrapper.

## Limitations and required validation

Exit 0 alone is not a test pass. Process-tree termination, hangs, output backpressure, abrupt host failure and safe cancellation remain to validate.

Roadmap ownership: M02-11, M06-06, M07-10.

See the [validation matrix](validation-matrix.md) and [open technical risks](open-technical-risks.md).
