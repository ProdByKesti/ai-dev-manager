# Reconstructed master roadmap — owner review

Status: detailed reconstruction complete, awaiting approval. **Not import-authorized or implementation-authorized.** All requirements, acceptance descriptions, role/type mappings and dependency assignments are newly reconstructed unless explicitly retained from approved decisions. The original full Phase 2 data was not recovered. The 25 product decisions, 15 ADRs, 12 system invariants and 18 consolidation amendments remain controlling; no changes to them are proposed.

## Review by milestone

| Milestone | Packages | Planned criteria | Details |
| --- | ---: | ---: | --- |
| M00 — Project Foundation | 10 | 22 foundation (separate) | [Review](reconstructed/M00.md) |
| M01 — Application Foundation | 12 | 24 | [Review](reconstructed/M01.md) |
| M02 — Execution & Security | 15 | 40 | [Review](reconstructed/M02.md) |
| M03 — Project & Task Management | 12 | 30 | [Review](reconstructed/M03.md) |
| M04 — Agent Management | 14 | 36 | [Review](reconstructed/M04.md) |
| M05 — Orchestration Engine | 16 | 42 | [Review](reconstructed/M05.md) |
| M06 — Quality Engine | 15 | 42 | [Review](reconstructed/M06.md) |
| M07 — Resource & Recovery | 15 | 42 | [Review](reconstructed/M07.md) |
| M08 — Linear Integration | 14 | 42 | [Review](reconstructed/M08.md) |
| M09 — Workspace Experience | 14 | 42 | [Review](reconstructed/M09.md) |
| M10 — Internal Alpha | 14 | 48 | [Review](reconstructed/M10.md) |
| M11 — Public MVP | 16 | 48 | [Review](reconstructed/M11.md) |
| M12 — Extended Platform | 16 | 42 | [Review](reconstructed/M12.md) |
| M13 — Community Ecosystem | 18 | 48 | [Review](reconstructed/M13.md) |

Machine-readable authoritative review inputs (once approved): [M00–M04](reconstructed-m00-m04.json), [M05–M09](reconstructed-m05-m09.json), [M10–M13](reconstructed-m10-m13.json), [manifest](reconstruction-manifest.json), [dependency graph](dependency-graph.json). The old [catalogue index](catalogue-draft.md) is retained for provenance, not import.

## Structural checks executed against the persisted reconstruction at fae7db241a33da608b76101a7478d7565dc670b8

| Check | Result |
| --- | --- |
| 201 unique package IDs | Passed |
| Stable titles and scope match prior reconstructed index | Passed |
| 14 milestone counts and check totals | Passed |
| 167 P0 and 34 later | Passed |
| 526 planned plus 22 foundation criteria, unique IDs | Passed |
| All required reconstructed fields and recognized labels | Passed |
| Valid edge endpoints, no self edges or duplicates | Passed |
| Hard and maximal conditional graph are acyclic | Passed |
| No P0 dependency on later scope | Passed |
| Foundation acceptance precedes all implementation | Passed |
| Public MVP acceptance includes every other P0 package transitively | Passed |
| K02 authenticated Linux and regression precede M02 acceptance | Passed |
| K03/K04 guard precedes dispatch, parallel and communication | Passed |
| K01 early compatibility before M00 acceptance | Passed |
| 18 consolidation corrections reference valid package IDs | Passed |
| Optional release scope preserved as conditional dependencies | Passed |

Graph: 614 hard dependencies, 31 conditional relationships, 645 potential total; both hard and maximal potential graph sorted all 201 nodes. No duplicate, invalid or self-referencing relationships. The historical reported 697 is unrecovered; the new count is not a claim of equivalence or an optimization. All potential optional edges must not become unconditional blockers. The topological order is a feasible ordering, not a calendar or approval to dispatch.

All 526 planned acceptance criteria and 22 foundation criteria have stable IDs and are marked not-executed in the draft. They are proposed check definitions, not test results. Owner review must also verify semantic completeness; structural validation does not prove the plan is optimal, the tests executable, or the software secure.

## Retained decision traceability

All packages inherit [INV-01–INV-12](../architecture/system-invariants.md). The following mappings are copied from the accepted [consolidation document](../architecture/consolidation.md); applicable rules must be included during import and work-order creation.

| Amendment | Package references | Rule |
| --- | --- | --- |
| K01 — Early public provider compatibility | M00-03, M00-05, M02-06, M11-02 | Check permitted integration/distribution paths early, confirm critical authentication feasibility in M02 and recheck public distribution in M11. |
| K02 — Authenticated Linux inference gate | M02-06, M02-13, M02-15 | Require real authenticated Linux agent execution with protected account boundary and verified sandbox before M02 acceptance. |
| K03 — Early central quota guard | M02-06, M02-12, M04-10, M05-10, M07-06 | All inference routes use one minimal guard from M02, expanded in M05/M07; unknown quota holds automation. |
| K04 — Parallelization dependency | M05-09, M05-10 | Make M05-10 an explicit prerequisite of M05-09. Before guard completion, use fake providers or explicitly controlled single runs. |
| K05 — Separate domain states | M03-07, M04-03, M05-01, M06-08, M08-06 | Separate project/task, agent/session/run, quality and external sync states; run success is not task completion. |
| K06 — Protected Git metadata | M02-09, M06-10, M06-12 | Protect shared config, hooks and refs; bind integration approval to source/target commits; reconcile uncertain writes. |
| K07 — Linux/Windows boundary | M02-08, M02-10, M02-14 | Test interop, host IPC, mounts, credentials and broker; disable unsupported/unsafe paths. |
| K08 — Trusted quality evidence | M06-02, M06-04, M06-06, M06-07 | Protected test definitions, trusted execution capture and candidate identity; independently authorize test baseline changes. |
| K09 — Stop semantics | M02-11, M05-13, M09-10 | Separate Pause New Starts, Cancel Run and Emergency Stop; persist global stop; track descendant termination and external effects separately. |
| K10 — Cumulative budgets | M04-10, M05-12, M06-09, M07-09 | Central persistent counters; retries, session/model changes and restart must not reset budgets implicitly. |
| K11 — Backup retention safety | M07-11, M11-09 | Retention and size are targets; protect last verified restore basis and required migration backups; warn/block updates on insufficient space. |
| K12 — Sync guarantees | M08-07, M08-09, M08-11 | Preflight and post-write verification; block ambiguous effects; document residual non-atomic race risk. |
| K13 — Update trust | M11-04, M11-05, M11-08, M11-09 | Bind versions and artifacts, plan key rotation/revocation and downgrade protection; distinguish Windows code signing. |
| K14 — External field authority | M12-03, M12-13 | One authority per synchronized field or explicit conflict rule; prevent synchronization loops. |
| K15 — MCP server trust | M12-04, M12-05 | Isolate local server processes, constrain external data transfers, deny unknown tools by default. |
| K16 — Semantic index scope | M12-10, M12-11 | Enforce scope during indexing and candidate selection, including deletion, reindexing, model versions and external transfer. |
| K17 — Distributed leases | M13-11, M13-12, M13-13 | Use versioned leases/fencing for supported integration effects; reject stale results and block unresolvable side effects. |
| K18 — Pre-release ecosystem validation | M13-05, M13-06, M13-17, M13-18 | Validate release candidates before publication; conditional dependencies per release; platform-specific plugin isolation checks. |

## Decisions for owner review

- Newly proposed detailed graph, role/issue-type assignments, and allocation of the 526 checks to individual packages; milestone counts remain unchanged. The graph is not forced to match an unverifiable historical edge count.
- M00-03 documentation was accepted and integrated; the proposed tracking mapping records completion of that documentation scope only, with K01 still explicitly open and assigned to M00-05 before M00-10. This does not mark K01 passed. A later rejection of this interpretation requires revising the dependency/status mapping rather than blocking M00-05 on its own prerequisite.
- No estimated hours, dates, model catalogue or unapproved cost commitment introduced. Performance targets and numerical defaults retained in milestone notes are provisional until tested.
- Extension release gate packages recur per approved release scope; a single Linear status cannot prove future releases accepted. Record each release's own evidence and conditional scope.
- The 22 M00 criteria are separate from the 526 planning count. Existing foundation evidence must be mapped from actual PRs and approvals during import, not replaced by invented new tests.

See [import preflight](import-preflight.md). No Linear issues or relations have been created in this reconstruction. No code implementation or release is authorized.
