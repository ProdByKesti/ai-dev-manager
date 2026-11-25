# Master roadmap import preflight

M00-07 part B. Detailed reconstruction is available in [reconstruction review](reconstruction-review.md), but awaits owner approval. Use only an explicitly approved revision of the [manifest](reconstruction-manifest.json) and its linked machine-readable inputs. Historical index files are not import sources.

## Required pre-import gates

1. Verify owner approval binds exact reviewed Git commit, including new requirements, check definitions, fixed/conditional dependencies, owners, types, status mapping and milestone policies. Merge through protected main after approval, then verify resulting tree. No M01+ execution authorization.
2. Re-run structural checks on merged source; compare all 201 stable IDs and scope, 526 planned criteria plus 22 foundation criteria, K01–K18 and INV-01–INV-12. Hard graph and maximal potential graph acyclic. Conditional release scope must not turn into mandatory blockers.
3. Read actual target workspace/team/project and issue inventory immediately before writing. Confirm free-tier headroom; 7 visible pre-existing TEST issues at last check, 201 new planned, theoretical 42 reserve at 250 limit. Actual billed/limited usage is not verified from connector. Do not purchase or delete to make room.
4. Resolve milestones/labels by stable IDs/names; map proposed owner and issue type to available labels. Roadmap scope P0–P3 is not incident severity. For release-dependent packages, preserve conditional P labels in metadata; choose release-specific priority only after scope approval.
5. Read by stable ADM package ID before each create, match exact title prefix. Never create duplicate or retry ambiguous write without fresh inventory. Batch and verify outcomes; retain returned Linear identifiers and actual state. Do not overwrite unrelated issues.
6. Create issue with approved requirements, per-package checks, milestone notes/links, invariant and applicable amendment references, dependency IDs, planned status and current evidence. Use explicit hard blocked-by relations only once both issue IDs exist. Connector supports blockedBy/blocks; verify actual relationship read-back. Conditional dependencies remain structured release metadata until selected scope is approved. Do not represent them as permanent blockers.
7. Map existing evidence: PR #1 M00-01; PR #2 M00-02/03; PR #3 M00-04; PR #4 M00-06. Proposed Done for accepted integrated documentation scope only; M00-03 explicitly records K01 still open in M00-05 and later gates. M00-07 part A accepted, B in progress; other packages Backlog unless separately authorized. Obtain owner approval for this mapping. Do not count new criterion definitions as executed; attach actual evidence and limitations.
8. Verify all 201 mapped issues, expected labels/milestones/status, hard relation coverage and conditional metadata, original TEST issues unchanged and no duplicates. Report unverified relation fields or API limitations explicitly. Close M00-07 only after actual import verification and personal acceptance; update mapping/evidence in versioned docs through PR.

## Stop conditions

Wrong workspace/team, unexpected existing issue, capacity limit, ambiguous mutation, missing label/milestone, inaccessible required dependency verification, invalid graph, rejected revision or unexpected external change. Stop affected operations, reconcile actual state; no paid fallback or blind repeat.

The 526 planned checks are not separate Linear issues. No issue creation in this preparation revision. No application implementation or new live provider tests.
