# Git and development workflow

Status: initial repository policy (M00-01). Detailed development and security instructions will be consolidated in AGENTS.md during M00-06.

## Branches and workspaces

- `main` is the integration branch. Do not develop directly on it.
- Use one focused branch per approved work package, e.g. `feature/m02-13-linux-inference` or `docs/m00-02-product-spec`.
- Use separate Git worktrees for concurrent work. Never assume worktrees alone provide a security sandbox.
- Start from a known base commit; keep a record of the assigned work package, branch and tested commit.
- Do not modify other projects, shared Git configuration, hooks or protected refs without explicit authorization.

## Review and integration

1. Confirm the approved scope and acceptance criteria.
2. Implement on the assigned branch/worktree.
3. Run applicable deterministic checks and record results against the candidate commit.
4. Obtain independent review and human acceptance where required.
5. Open a pull request; verify target branch state and applicable checks.
6. Integrate only after authorization. Revalidate changed integration candidates.
7. Update the task and evidence records; retain history.

Missing, stale or failed required evidence blocks integration. No force pushes, destructive resets, unapproved dependency changes or secret publication. Agent claims do not replace verification.

## Repository protection

The intended baseline is pull-request-based changes to main, no force pushes or branch deletion, and required CI checks once those checks exist. Any independent review requirement must match the actual maintainer setup; never claim a review was performed if it was not.

Technical enforcement must be verified in GitHub settings separately. This document does not itself configure branch protection.

## Public repository hygiene

Only approved public material may be committed. Do not publish account tokens, private workspaces, raw provider transcripts, sensitive test data or personal paths. Inspect changes before pushing. Use synthetic fixtures, sanitized evidence and narrowly scoped credentials. Do not commit generated builds, local runtime databases or private keys.
