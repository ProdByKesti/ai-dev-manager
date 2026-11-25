# Open technical risks and gates

Historical evidence supports further development, subject to the following explicit unresolved checks. No new live verification was performed during M00-04.

| Risk / prerequisite | Required action | Roadmap gate |
| --- | --- | --- |
| Provider terms and public authentication | Check official permitted integration/distribution paths early; validate real auth; recheck public release. Do not assume subscription reuse is universally allowed. | K01: M00-05, M02-06, M11-02 |
| Rust/Tauri toolchain | Verify Rust/Cargo, Windows build prerequisites, WebView2 and reproducible desktop/core builds. | M00-05, M01 |
| Native Linux authenticated inference | Run actual authorized account-based agent execution with no API-key fallback, protected credentials and verified policy. | K02: M02-13, M02-15 |
| Host and execution isolation | Test real agent-mediated filesystem access, concurrent profiles, WSL interop/mounts, host IPC, credentials, broader network and protected Git/toolchains. | K06/K07: M02-08, M02-09, M02-10, M02-14, M10-09 |
| Complete cancellation | Verify process descendants and external effects independently from interrupt acknowledgement; persistent stop. | K09: M02-11, M05-13 |
| Quota and resource limits | Validate real exhaustion/reset/events, unknown quota blocking and shared admission; no automatic paid fallback. | K03/K04: M02, M05-10, M07 |
| Persistence and recovery | Inject abrupt crashes, preserve uncommitted work, reconcile ambiguous operations and verify backup restore. | M07, M10 |
| Trusted quality evidence | Protect test baseline and execution records, bind to commit and independently review when required. | K08: M06, M10 |
| Linear integration | Check free-plan capacity, public OAuth, protected credentials, durable outbox, conflicts and non-atomic write races. | K12: M08, M11 |
| Public distribution | Validate installer, signed update metadata and key lifecycle, code-signing options, clean systems, third-party terms and cost. | K13: M11 |

If a mandatory boundary cannot be enforced or a public integration is not permitted, stop the affected workflow and escalate. Do not silently weaken sandbox rules, reuse unauthorized credentials, purchase services or claim acceptance without evidence.

See [consolidation amendments](../architecture/consolidation.md) and [system invariants](../architecture/system-invariants.md).
