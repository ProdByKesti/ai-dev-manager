# T11 — Sandbox and security profiles

Status: Partial feasibility. Historical feasibility investigation completed; production acceptance not implied.

Evidence basis: reconstructed from retained Phase 0 test summaries and reported historical observations. Raw logs, scripts and complete original console transcripts are not available in this documentation pass. No new execution was performed; the report is not independently reproduced evidence. Private paths, identifiers, account data and credentials are intentionally omitted.

## Objective

Investigate technically enforced filesystem, process and network permissions on Windows and WSL2.

## Reported observations

See the detailed historical evidence below. Native Windows isolation was limited; native Linux under WSL2 demonstrated scoped permissions for controlled commands. The recorded total 188/188 covers selected successful Linux probe groups, not all T11 attempts or all possible threats.

## Design implications

Use native Linux execution as the initial candidate, with explicit Windows broker boundaries and fail-closed enforcement. Treat prompts and worktrees as insufficient for isolation.

## Limitations and required validation

Authenticated agent-mediated enforcement, concurrent profiles, credential isolation, host interop and IPC, broader network coverage, cancellation and Git/toolchain trust remain mandatory validation work.

Roadmap ownership: M02-01, M02-07, M02-08, M02-10, M02-13, M02-14, M10-09.

See the [validation matrix](validation-matrix.md) and [open technical risks](open-technical-risks.md).

## Native Windows findings

The reported native Windows probes verified read-only and workspace-write behavior, but foreign reads were possible. The legacy readOnlyAccess approach was unsupported. Custom named permission profiles with explicit filesystem rules and experimental App Server capabilities were explored. The unelevated backend failed closed on split-read policies; MXC was not available in the tested Windows 10 environment. The elevated backend used a separate offline sandbox identity; root read permission was required. Explicit denial of a synthetic location blocked reads and writes, while a separate permitted location remained readable. A strict read allowlist was not established on Windows. Do not treat these results as full Windows isolation.

## Native Linux environment (T11k)

WSL2 Ubuntu 24.04, kernel 6.18.58.1-microsoft-standard-WSL2; user namespaces available. Native Codex CLI 0.163.0, x86_64 musl package, bundled bubblewrap resource. Historical package SHA-256: `582646c6bf0561eb0de540f7fc85b9121b0091a826bc6e96830b7f1722122182`. Package checksum was reported verified. Isolated temporary environment and separate Codex home; no system package installation, administrator change or account login in these Linux probe groups.

## Counted Linux probe groups

| Group | Reported passed | Scope |
| --- | ---: | --- |
| T11l | 9/9 | Strict CLI filesystem allow/deny/hidden synthetic paths |
| T11m | 5/5 | Local IPv4 TCP connectivity with network enabled/disabled |
| T11n | 55/55 | Parent, child and grandchild inheritance of file/network restrictions |
| T11o | 36/36 | Native App Server profile discovery and per-command execution A/B/A with different file/network policies |
| T11p | 83/83 | Clean combined regression: strict/read-only/network-on, direct/relative/symlink paths, Linux and Windows mounts, host-side verification |
| Total | 188/188 | Sum of selected successful assertions; overlapping cases possible |

The total is 9 + 5 + 55 + 36 + 83 = 188. It excludes preliminary Windows probes, setup checks and failed harness attempts. It is not a count of unique threats or independently reproduced tests.

### T11l–n

In T11l an allowed synthetic workspace could be read and written. An explicitly denied directory returned errno 13; a hidden directory returned errno 2. The wrapper later reported a heredoc NameError and exit 1 despite the nine observed assertion successes. The clean T11p regression supersedes this incomplete wrapper result. T11m tested local TCP with network enabled and disabled, including separate host-side connection checks. T11n reported inherited permissions across three process generations; this was an inheritance probe, not a full process-containment or cancellation proof.

### T11o

The first App Server harness attempt contained a ProbeServer naming error. The corrected attempt completed 36/36 checks with exit 0. Native stdio initialization used experimental API capabilities; permissionProfile/list discovered both custom profiles and a dangerous default. Explicit named profiles were selected for command/exec in A/B/A order on one server. Different filesystem/network rights were observed without cross-profile leakage in those sequential probes. Five RPC requests, zero inference; the bundled bubblewrap fallback was reported working. Dangerous defaults must never be selected automatically.

### T11p

The clean combined harness completed 83/83 with exit 0. Direct, relative and symlink access to synthetic Linux and Windows-mount locations was exercised under strict, read-only and network-enabled profiles. Own workspace operations succeeded; denied/hidden and Windows-mount paths were blocked as expected. Read-only writes reported EROFS. Host-side verification found only four expected allowed files and no other writes; original protected test data remained unchanged and temporary test directories were removed. Zero inference in the Linux command probe groups.

## Interpretation

These results support proceeding with the Linux sandbox candidate, not declaring it secure for arbitrary agents. Local IPv4 TCP tests do not establish comprehensive network isolation. Sequential profile switching does not establish concurrent isolation. Native command execution tests do not establish authenticated agent tool enforcement, WSL interop/host IPC resistance, credential protection or protection against unrestricted same-user host processes. The actual agent path must be independently validated before M02 acceptance (K02/K07). Do not downgrade to unconfined Windows execution if the required boundary cannot be established.
