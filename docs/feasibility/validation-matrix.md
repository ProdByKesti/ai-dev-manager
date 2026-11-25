# Validation matrix

Historical evidence vs remaining acceptance work. This matrix describes reports, not newly executed tests.

| ID | Reported evidence | Outstanding gate | Owner |
| --- | --- | --- | --- |
| [T01](T01-development-environment.md) | Partial feasibility | Rust/Cargo, Windows build tools, WebView2, Tauri builds, supported OS matrix and reproducible installation remain unverified. | M00-05, M01-01, M01-02 |
| [T02](T02-app-server-transport.md) | Demonstrated within probe | Production framing, malformed messages, timeouts, concurrent requests, stderr handling, authentication events and native Linux transport in authenticated operation require further testing. | M02-05, M02-06 |
| [T03](T03-authenticated-inference.md) | Demonstrated within probe | Public provider terms, public account onboarding, actual billing behavior, protected credentials, authenticated native Linux inference and quota exhaustion remain open. No automatic paid fallback. | M00-05, M02-06, M02-13, M11-02 |
| [T04](T04-session-isolation.md) | Demonstrated within probe | This was not a filesystem, network, IPC, credential, model-side retention or adversarial security isolation test. | M02-14, M04-03, M04-06 |
| [T05](T05-concurrent-execution.md) | Demonstrated within probe | The observation does not prove simultaneous inference on provider infrastructure, throughput scaling, larger concurrency limits or independent sandbox enforcement. Require M05-10 before parallel dispatch M05-09. | M05-09, M05-10, M10-07 |
| [T06](T06-process-management.md) | Demonstrated within probe | Exit 0 alone is not a test pass. Process-tree termination, hangs, output backpressure, abrupt host failure and safe cancellation remain to validate. | M02-11, M06-06, M07-10 |
| [T07](T07-intervention-cancellation.md) | Partial feasibility | No proof that all descendant processes or external side effects stopped. Test actual termination, interrupt races, persistent global stop and recovery. | M02-11, M05-13, M09-10 |
| [T08](T08-session-persistence.md) | Partial feasibility | Abrupt crashes, missing sessions, incomplete turns, concurrent resume, stale approvals and state reconciliation remain open. | M04-03, M04-07, M04-08, M07-10 |
| [T09](T09-model-capabilities.md) | Demonstrated within probe | Availability can change by account, version and provider. Test unsupported settings, capability refresh, model changes and approved bounded escalation. | M02-06, M04-03, M07-05 |
| [T10](T10-quota-management.md) | Partial feasibility | Real exhaustion, reset, account/rate-limit change events, stale readings and concurrent reservations remain unverified. No prediction of guaranteed remaining jobs and no automatic paid fallback. | M02-06, M02-12, M05-10, M07-02, M07-06 |
| [T11](T11-sandbox-security.md) | Partial feasibility | Authenticated agent-mediated enforcement, concurrent profiles, credential isolation, host interop and IPC, broader network coverage, cancellation and Git/toolchain trust remain mandatory validation work. | M02-01, M02-07, M02-08, M02-10, M02-13, M02-14, M10-09 |
| [T12](T12-linear-integration.md) | Partial feasibility | Public OAuth, persistent recovery, concurrent external writes, rate limits, long-running synchronization and public distribution remain open. No exactly-once guarantee. | M08-02 to M08-14, M11-02 |

## Evidence rules

All mandatory production checks must be bound to the tested candidate, environment, policy and actual result. Historical probes inform the design; they cannot satisfy a gate for a different runtime, commit or security boundary automatically. Acknowledgement is not termination; logical context separation is not sandbox isolation; overlap is not proof of provider parallel inference; successful external operations do not establish exactly-once semantics. Do not count skipped or inconclusive checks as passed.

No raw evidence files or test harnesses are asserted to exist in this repository. Obtain original logs or reproduce applicable scenarios in the assigned roadmap packages. See [quality-gates ADR](../architecture/decisions/adr-011-quality-gates.md).
