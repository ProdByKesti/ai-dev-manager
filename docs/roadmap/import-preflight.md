# Master roadmap import preflight

M00-07 part B, preparation only. No production issues created in this step.

## Source reconciliation

The merged roadmap overview provides 14 milestones, 201 packages (167 P0 / 34 later), and 526 planned checks for M01–M13. The reconstructed catalogue contains 201 unique stable IDs and matches all milestone totals. Original detailed package descriptions, full edge list and named acceptance checks were not recovered from the accessible historical summaries or file search. They must be recovered or explicitly reconstructed as a new revision for owner approval. Do not silently fill gaps or count placeholders as recovered tests.

Known M00 progress for later status mapping: M00-01 integrated PR #1; M00-02 integrated PR #2; M00-03 documentation integrated PR #2, K01 open; M00-04 integrated PR #3; M00-06 integrated PR #4; M00-07 part A personally accepted, part B ongoing. Other M00 tasks remain pending. Exact status mapping must preserve open gates and evidence, not just a completion count.

## Import contract (proposed procedure)

1. Freeze a reviewed, approved versioned catalogue: stable ID, title, scope, owner, detailed requirement, acceptance criteria, dependency IDs, consolidation/invariant references and evidence/status.
2. Validate unique IDs, all edge endpoints, no self-dependencies/duplicates, DAG cycle detection and milestone/release gates. Resolve conditional extension edges per release scope. Recalculate actual edge count, not the previous reported count. Map all 526 named checks without creating separate issues.
3. Confirm the target ADM workspace/team/project and fresh issue inventory. Verify remaining capacity against the actual plan limits; no paid upgrade. Existing TEST issues must remain unchanged.
4. Reconcile by stable package ID before every creation. Stop on multiple matches, conflicting metadata or ambiguous writes. Use batches with read-back and preserve returned Linear IDs; never retry unknown effects blindly.
5. Create the approved issue metadata, then reconcile dependencies after both endpoints exist; check exact relation semantics. Do not assume a connector supports every operation.
6. Verify all 201 issue mappings, milestone placement, scope and role labels, status/evidence and dependency coverage against the approved catalogue. Record partial results and blockers; preserve external history.
7. Close M00-07 only after required checks and owner acceptance. No M01+ implementation before foundation acceptance and explicit authorization.

## Current validation

201 unique IDs; 167 P0; 34 later; 526 planned check count matched; 14 milestone groups. Three retained/derived minimum package edges have valid endpoints and the subset has no cycles. This is not the full dependency graph. Package requirements, assigned role, acceptance criteria and complete dependencies remain null pending verification. No dates or new technical decisions are authorized by this draft.
