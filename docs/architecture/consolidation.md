# Consolidation amendments

Approved Phase 3.1 corrections K01–K18. Amend existing work packages without creating additional work packages. These clarifications override contradictory earlier detail but do not expand the mandatory MVP scope.

## K01 — Early public provider compatibility

Affected packages: M00-03, M00-05, M02-06, M11-02.

Check permitted integration/distribution paths early, confirm critical authentication feasibility in M02 and recheck public distribution in M11.

## K02 — Authenticated Linux inference gate

Affected packages: M02-06, M02-13, M02-15.

Require real authenticated Linux agent execution with protected account boundary and verified sandbox before M02 acceptance.

## K03 — Early central quota guard

Affected packages: M02-06, M02-12, M04-10, M05-10, M07-06.

All inference routes use one minimal guard from M02, expanded in M05/M07; unknown quota holds automation.

## K04 — Parallelization dependency

Affected packages: M05-09, M05-10.

Make M05-10 an explicit prerequisite of M05-09. Before guard completion, use fake providers or explicitly controlled single runs.

## K05 — Separate domain states

Affected packages: M03-07, M04-03, M05-01, M06-08, M08-06.

Separate project/task, agent/session/run, quality and external sync states; run success is not task completion.

## K06 — Protected Git metadata

Affected packages: M02-09, M06-10, M06-12.

Protect shared config, hooks and refs; bind integration approval to source/target commits; reconcile uncertain writes.

## K07 — Linux/Windows boundary

Affected packages: M02-08, M02-10, M02-14.

Test interop, host IPC, mounts, credentials and broker; disable unsupported/unsafe paths.

## K08 — Trusted quality evidence

Affected packages: M06-02, M06-04, M06-06, M06-07.

Protected test definitions, trusted execution capture and candidate identity; independently authorize test baseline changes.

## K09 — Stop semantics

Affected packages: M02-11, M05-13, M09-10.

Separate Pause New Starts, Cancel Run and Emergency Stop; persist global stop; track descendant termination and external effects separately.

## K10 — Cumulative budgets

Affected packages: M04-10, M05-12, M06-09, M07-09.

Central persistent counters; retries, session/model changes and restart must not reset budgets implicitly.

## K11 — Backup retention safety

Affected packages: M07-11, M11-09.

Retention and size are targets; protect last verified restore basis and required migration backups; warn/block updates on insufficient space.

## K12 — Sync guarantees

Affected packages: M08-07, M08-09, M08-11.

Preflight and post-write verification; block ambiguous effects; document residual non-atomic race risk.

## K13 — Update trust

Affected packages: M11-04, M11-05, M11-08, M11-09.

Bind versions and artifacts, plan key rotation/revocation and downgrade protection; distinguish Windows code signing.

## K14 — External field authority

Affected packages: M12-03, M12-13.

One authority per synchronized field or explicit conflict rule; prevent synchronization loops.

## K15 — MCP server trust

Affected packages: M12-04, M12-05.

Isolate local server processes, constrain external data transfers, deny unknown tools by default.

## K16 — Semantic index scope

Affected packages: M12-10, M12-11.

Enforce scope during indexing and candidate selection, including deletion, reindexing, model versions and external transfer.

## K17 — Distributed leases

Affected packages: M13-11, M13-12, M13-13.

Use versioned leases/fencing for supported integration effects; reject stale results and block unresolvable side effects.

## K18 — Pre-release ecosystem validation

Affected packages: M13-05, M13-06, M13-17, M13-18.

Validate release candidates before publication; conditional dependencies per release; platform-specific plugin isolation checks.

## Risk register summary

Critical early dependencies are permitted public provider integration, authenticated Linux execution with credential and host isolation, and Rust/Tauri prerequisites. Other risks include shared quota exhaustion, Linear free-tier capacity and public auth, manipulated quality evidence, low-end hardware performance, signing/distribution costs, uncontrolled scope and recovery failures. These are qualitative planning risks, not measured probabilities. Record evidence and unresolved blockers in the responsible package. Do not assume unavailable infrastructure or buy services without approval.

M00-05 includes early provider compatibility and development environment checks; M02 blocks further live agent development if core authenticated isolation cannot be established. M11 revalidates public terms and actual distribution. A full machine-readable dependency graph and per-package acceptance criteria belong to the roadmap import; this document does not claim to validate a graph that is not yet in the repository.
