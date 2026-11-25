# M00-07 — controlled Linear import verification

Status: import and full read-back verified; owner acceptance and integration of this evidence pending. The development implementation hold remains in force.

## Authorization and source

The maintainer personally accepted commit `9a761c53910a9eebf8865db2c77b652492e6b6ea` and the reconstructed detail decisions/status mapping. PR #5 was merged to `main` at `c97ee800affffc3ae224866b18f189e779995a85`; the integrated tree `e21e5b928bf6dc0fd1dfb7287b3f2764b27a355e` exactly matched the accepted tree, and main was protected. The manifest's pre-approval snapshot is retained as historical evidence, not silently rewritten. The authorized import was performed after the merge.

## Scope

Target: AI Dev Manager – Development (P-ADM-2), ADM team. [Issue mapping](linear-issue-mapping.json) records the observed human-readable Linear identifiers; it is a snapshot, not a live status mirror. Internal UUIDs, credentials and account identifiers are excluded from this public document.

| Check | Observed result |
| --- | --- |
| Stable package IDs / native issues | 201/201 unique |
| Milestones | 14/14, matching counts |
| P0 / later | 167 / 34 |
| Planned acceptance definitions | 526/526 transferred and read back |
| Foundation criteria | 22/22 transferred and read back |
| Native hard blockedBy relationships | 614/614, exact expected set per issue |
| Conditional release dependencies | 31/31 in descriptions; not native unconditional blockers |
| Requirements, milestone notes, applicable amendments, invariant references | 201/201 matched by read-back checks |
| Titles, scope, specialist/type/scope labels, milestone, initial status, team, project, source revision | 201/201 matched |
| Duplicate stable IDs | 0 |
| Existing TEST-team issues | 7/7 retained; title, project, status matched before/after |
| Visible workspace issues | 208, no further page; theoretical 42 remaining at known 250 cap; actual plan consumption not available |

## Read-back batches

| Range | Issues matched | Criteria | Native incoming edges | Conditional metadata |
| --- | ---: | ---: | ---: | ---: |
| M00-01 – M01-07 | 17 | 36 | 35 | 0 |
| M01-08 – M02-12 | 17 | 44 | 49 | 0 |
| M02-13 – M04-02 | 17 | 42 | 62 | 0 |
| M04-03 – M04-14 | 12 | 30 | 39 | 0 |
| M05-01 – M06-01 | 17 | 45 | 63 | 0 |
| M06-02 – M07-03 | 17 | 48 | 59 | 0 |
| M07-04 – M08-05 | 17 | 48 | 71 | 0 |
| M08-06 – M09-08 | 17 | 51 | 61 | 0 |
| M09-09 – M09-14 | 6 | 18 | 33 | 0 |
| M10-01 – M11-03 | 17 | 57 | 47 | 0 |
| M11-04 – M12-04 | 17 | 51 | 43 | 0 |
| M12-05 – M13-05 | 17 | 45 | 27 | 15 |
| M13-06 – M13-18 | 13 | 33 | 25 | 16 |
| Total | 201 | 548 | 614 | 31 |

Read-back compared returned descriptions with normalized expected requirements, individual criterion text, scope, milestone policies, amendments, invariant references and source revision; exact incoming dependency ID sets and labels were checked. This validates imported metadata, not runtime acceptance or execution of the planned tests.

## Status and operational notes

Five accepted integrated documentation/foundation packages Done (M00-01/02/03/04/06); M00-07 In Progress; 195 Backlog. K01 remains explicitly open in M00-05 and later gates. The individual criteria are definitions, not newly executed tests. Four release-dependent packages (M12-15/16, M13-17/18) retain their conditional scope in metadata without a fixed P label until release selection. No incident urgency, due dates or assignments to a human account were inferred.

The initial creation batch hit the connector call limit after seven successful writes. The target inventory was reread and the remaining three foundation issues created without duplicates. Subsequent batches used fresh team inventory, exact stable-ID matching and serial creation with local inventory updates, then separate native relation writes and full individual read-back. This is controlled reconciliation, not a transactional exactly-once guarantee; concurrent external edits could race. No separate independent reviewer or new runtime tests were performed.

M00-07 remains open until this evidence is personally accepted and integrated. Implementation remains on hold until the foundation gate and separate authorization.
