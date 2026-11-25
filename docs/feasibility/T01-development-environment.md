# T01 — Development environment

Status: Partial feasibility. Historical feasibility investigation completed; production acceptance not implied.

Evidence basis: reconstructed from retained Phase 0 test summaries and reported historical observations. Raw logs, scripts and complete original console transcripts are not available in this documentation pass. No new execution was performed; the report is not independently reproduced evidence. Private paths, identifiers, account data and credentials are intentionally omitted.

## Objective

Establish a Windows development host and discover available toolchain components.

## Reported observations

Windows 10 Pro build 19045.6466; Codex CLI 0.163.0; Node.js 24.22.0; npm 11.19.1; Git 2.56.0.windows.2; Python 3.15.0. PowerShell execution policy blocked npm/codex PowerShell shims; invoking the corresponding .cmd launchers worked. Codex was logged in. Rust and Cargo were not found on PATH.

## Design implications

Record tool versions and use explicit Windows command launchers when required; do not relax global execution policy merely to run shims.

## Limitations and required validation

This historical report describes the earlier investigation only. Subsequent M00-05 checks of Rust/Cargo and the minimal Windows MSVC build are recorded separately in [M00-05 environment and K01 evidence](M00-05-environment-k01-evidence.md). WebView2 behavior, a complete Tauri build, the supported OS matrix and reproducible installation remain unverified.

Roadmap ownership: M00-05, M01-01, M01-02.

See the [validation matrix](validation-matrix.md) and [open technical risks](open-technical-risks.md).
