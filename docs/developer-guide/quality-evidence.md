# Quality gates and evidence

M00-06 development policy. The product's automated Quality Engine is planned for M06; this document defines the human/agent development process now.

## Definition of done

A work package is complete only when all applicable requirements and mandatory acceptance criteria are met, automated checks and regression checks pass, security requirements are satisfied, required independent review and human acceptance are recorded, the authorized candidate is integrated and verified, and the relevant task/docs/evidence are updated. Document residual limitations. If an external sync fails, report it separately; do not claim it succeeded.

| Gate | Required evidence |
| --- | --- |
| Scope | Stable work package, approved requirements, relevant dependency state |
| Implementation | Actual diff and candidate commit, no unrelated changes |
| Automated validation | Applicable commands, environment, exact results and required test count |
| Regression/security | Relevant regression, negative tests and security boundary evidence |
| Review | Independent reviewer and findings when required; author review identified as such |
| Acceptance | Authorized human decision tied to candidate and policy where required |
| Integration | Verified target/base, candidate, actual merge result and resulting revision |
| Traceability | Updated existing task, documents, known limitations and handoff |

Documentation-only work uses relevant content, link, structural and consistency checks; do not claim a software build was run. Record truly non-applicable checks and the reason. A missing mandatory test cannot be converted to not-applicable by an implementing agent.

## Evidence states

Use separate gate states: Pending, Running, Passed, Failed, Skipped, Inconclusive, Invalidated, Blocked, Not applicable. Only a valid Passed result fulfills a mandatory gate. Approval of a policy revision is separate from a pass; never relabel skipped or invalid evidence as passed. An exit code of 0 with no required tests executed is insufficient. A historical probe, fake provider or simulation is not evidence of a live provider or production boundary.

## Evidence record

Record: package and requirement IDs; exact source and candidate commits, worktree and target revision; applicable policy/test baseline revision; environment/tool versions; command or review method; actual output summary, executed/passed/failed/skipped counts and exit code; artifact location and integrity reference where applicable; reviewer/acceptance reference; limitations and remaining gates. Sanitize public records. Retain original private evidence under authorized local storage if available. Do not fabricate counts, hashes, approval or outputs.

Protect requirements, test definitions, fixtures, runner, evidence capture and integration metadata from unauthorized changes. Independently review changes to mandatory test baselines; verify evidence belongs to the candidate. A successful model response is not proof of a successful test. Revalidate relevant gates if the candidate, target, environment or policy changes.

## Repair and escalation

Use bounded repairs and retries within the approved work order. Keep actual failed attempts visible; verify unknown side effects before retrying. If a gate cannot run or remains inconclusive, report the blocker and do not mark it passed. Independent review is not the author's self-review. No self-waiver; request a maintainer decision if requirements or scope need revision.

## Release rules

No release with open critical/high blockers (S0/S1); other issues reviewed case by case under the applicable release policy. Public release requires independent validation, verified artifacts and explicit authorization. Local historical feasibility is not release readiness. M02 requires authenticated Linux inference and real isolation evidence; K01 public provider compatibility is an early gate and is revalidated in M11. M12/M13 releases require scope-specific regression/security checks before publication. See [system invariants](../architecture/system-invariants.md), [consolidation](../architecture/consolidation.md), [feasibility matrix](../feasibility/validation-matrix.md) and [quality ADR](../architecture/decisions/adr-011-quality-gates.md).

## Foundation checks

Run `python3 scripts/check_foundation.py`, `python3 scripts/check_links.py`, and `python3 scripts/run_foundation_tests.py` using Python 3.11 or newer. The roadmap validator checks the approved baseline and consistency; baseline changes require explicit approval, reviewed updates to data and constants, and renewed evidence. The documentation checker validates internal links and core definitions; its module documentation describes its deliberately limited Markdown support and unsupported constructs.

The strict runner fails on missing test modules, zero tests, failures, errors, skipped tests, expected failures and unexpected successes, including a missing symlink regression test. Record actual source, PR head, base and checked-out revisions: a pull request run may test a synthetic merge commit. Standard GitHub-hosted runners are free for public repositories. Independent review of protected test definitions remains required. A successful CI run is evidence, not proof that merge protection or required status checks are configured.
