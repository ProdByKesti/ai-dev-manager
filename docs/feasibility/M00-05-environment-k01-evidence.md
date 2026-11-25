# M00-05 — Development environment and K01 evidence

Status: Evidence prepared for review; no maintainer acceptance or release authorization. Scope: Foundation research and documentation. Repository baseline: `5489a482a68e42ce655d7365bfddaf0c91740cbd`. The local checkout is intentionally deferred to M00-09.

## Acceptance criteria

The criterion wording is from [M00](../roadmap/reconstructed/M00.md). These are evidence assessments, not checked-off acceptance or proof of production readiness.

| Criterion | Evidence assessment | Remaining limitations |
| --- | --- | --- |
| M00-05-AC01 — Record versioned toolchain checks and minimal build evidence or blockers | Recorded below; Rust/MSVC offline build and two unit tests passed. Host Ubuntu validation was reported by the maintainer. | WebView2 and full Tauri build are not functionally validated; Codex-context WSL access is blocked. |
| M00-05-AC02 — Record current official provider integration/distribution evidence and remaining K01 questions | Official documentation and open questions recorded below; this is documentary evidence. | Eligibility, OAuth, inference, billing and actual public distribution are not validated. M02 and M11 gates remain. |
| M00-05-AC03 — Confirm no unapproved costs or privileged changes | The described work orders report no installations, administrative actions, paid services, live provider calls or global configuration changes. | Assessment is limited to the documented activities; maintainer review and acceptance remain outstanding. |

## Windows host observations

Work orders 1 and 2 recorded Windows 10 Pro 22H2 x64, build 19045.6466; Git 2.56.0.windows.2; Node.js 24.22.0; npm 11.19.1; Python 3.15.0; and Codex CLI 0.163.0. The npm and Codex versions were obtained using their `.cmd` launchers. The Codex version command exited 0 but reported access-denied warnings during its attempted temporary alias cleanup/setup; this is not a full CLI or app-server functional test.

Visual Studio Build Tools 2026 18.11.0 and the x86/x64 C++ tools component were detected via `vswhere`. MSVC 14.51.36231 included compiler file version 19.51.36260.0 and linker file version 14.51.36260.0; the files were present outside the normal PATH. Windows SDK 10.0.26100 was found. WebView2 Runtime 158.0.4370.33 was found via installed-application information, but was not functionally validated.

Rust 1.100.0, Cargo 1.100.0 and rustup 1.29.3 were reached using the executables under the user's `.cargo/bin`; the default host and installed target were `x86_64-pc-windows-msvc`, and the active default toolchain was `stable-x86_64-pc-windows-msvc`. Version and toolchain commands exited 0. The test process temporarily prepended the Cargo binary directory to PATH and used a temporary CARGO_HOME; no global environment change was made.

### Executed minimal Rust/MSVC test

An isolated temporary Rust binary project had no external dependencies. Its deterministic addition function was checked by two unit tests. Commands ran in the project directory; `cargo.exe` was invoked via its explicit user Cargo-bin path.

| Command | Exit | Relevant result |
| --- | ---: | --- |
| `cargo.exe check --offline` | 0 | Check completed. |
| `cargo.exe build --offline` | 0 | Debug binary built. |
| `cargo.exe test --offline` | 0 | 2 tests executed; 2 passed, 0 failed. |
| `target/debug/adm_rust_validation.exe` | 0 | `ADM_RUST_BUILD_OK` |
| `cargo.exe build --release --offline` | 0 | Release binary built. |
| `target/release/adm_rust_validation.exe` | 0 | `ADM_RUST_BUILD_OK` |

The successful Windows MSVC-targeted binaries provide a minimal compiler/linker and SDK-use functional demonstration, not validation of all SDK features. The temporary project and artifacts were removed; the subsequent existence check returned false. A complete Tauri build was not performed, and WebView2 runtime behavior remains untested.

## WSL evidence and execution boundary

**Maintainer-reported host evidence:** In normal Windows PowerShell, WSL default version was 2. `docker-desktop` was registered as the default distribution using WSL2, and `Ubuntu-24.04` was registered using WSL2. The three explicitly Ubuntu-targeted commands below each returned exit 0, reporting Ubuntu 24.04.5 LTS (Noble Numbat), x86_64, and kernel `6.18.58.1-microsoft-standard-WSL2`, respectively.

- `wsl.exe -d Ubuntu-24.04 -- cat /etc/os-release`
- `wsl.exe -d Ubuntu-24.04 -- uname -m`
- `wsl.exe -d Ubuntu-24.04 -- uname -r`

Host-level Ubuntu runtime validation: **PASSED, as reported by the maintainer**. These observations were not independently reproduced by Codex in its execution context.

**Codex-executed evidence:** In both environment work orders, `wsl.exe --status` and `wsl.exe --list --verbose` failed with exit code -1 as reported by PowerShell and `Wsl/EnumerateDistros/Service/E_ACCESSDENIED`. The cause was not established. No Ubuntu command was run in this context, no additional privileges were requested, and no security or WSL configuration was bypassed or changed. Agent-controlled Linux execution remains an open validation gate; the host result does not prove agent access or isolation.

## K01 — provider compatibility: documentary evidence

Sources reviewed 2026-11-25; service documentation and terms can change.

- [Sign in with ChatGPT quickstart](https://developers.openai.com/siwc/quickstart) and [open-source plan usage overview](https://developers.openai.com/siwc/token-sharing-open-source) describe a candidate flow for eligible users of open-source, locally hosted applications. Registration, user consent, eligible plans and granted scopes matter; paid or remotely hosted use is referred to an interest process. This does not establish ADM's eligibility or a general right to distribute.
- The [Codex app-server guide](https://developers.openai.com/siwc/token-sharing-open-source/codex-app-server) documents passing the application's authorized OAuth access token to an app-server child process configured for Responses. The app owns token renewal and restarts the child with a renewed token. `model/list` is a catalog, not an entitlement check.
- [Accounts and sessions](https://developers.openai.com/siwc/token-sharing-open-source/profiles-and-sessions) describes separate account registrations, protected credential storage, serialized rotating-token refresh and sign-out/revocation handling. The proposed design uses app-specific OAuth authorization; it does not copy existing CLI credentials. This is a design constraint, not an implemented security claim.
- [Preview limitations](https://developers.openai.com/siwc/token-sharing-open-source/preview-limitations) documents route-specific Responses and app-server restrictions, including HTTP streaming and unsupported hosted tools. These must be rechecked against the actual integration.
- [Europe Terms of Use](https://openai.com/policies/eu-terms-of-use/) identifies its regional and individual-service scope and references other applicable terms; the relevant product, business, service and distribution terms must be checked for the actual use. This document does not provide a legal determination.

The intended architecture remains provider-neutral, with Codex as the first provider. Do not assume unlimited or separate quota. Apply a central fail-closed cost and quota guard: unknown or invalid quota blocks affected inference; no unapproved paid fallback or service. The official account guidance describes shared usage for certain plans and user-configurable credit behavior, not a guarantee that ADM can enforce a hard cost limit.

**Not executed:** no ADM OAuth authorization, live inference, provider quota exhaustion, billing behavior or public distribution validation in these work orders. Documentary support is not a runtime or legal test.

## Future gates and invariant boundaries

M02 must validate critical authentication, protected token lifecycle, actual provider behavior, fail-closed quota/cost controls, and authenticated Linux execution with the required isolation. The Codex-context WSL denial remains unresolved. M11 must recheck applicable public distribution eligibility, terms and release evidence. Full Tauri/WebView2 validation belongs to the appropriate later build work. Unknown or unsupported states remain blocked rather than passed.

[INV-01–INV-12](../architecture/system-invariants.md) remain mandatory, including human authority, fail-closed security, least privilege, no unauthorized costs, evidence over claims, protected integration, traceability, bounded automation, isolation, non-destructive recovery, local-first independence and verified public releases. This evidence does not claim their runtime enforcement. K01 is an early compatibility investigation, not final acceptance; see [consolidation amendments](../architecture/consolidation.md).

No provider calls, installations, privileged changes, WSL configuration changes or paid actions were performed for this consolidation. Maintainer review and final acceptance are separate.
