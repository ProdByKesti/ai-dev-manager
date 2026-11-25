# Documentation

This repository is in the foundation phase. Approved decisions are versioned here; implementation and validation are separate work.

- [Product specification — 25 decisions](product/product-specification.md)
- [Technical architecture and 15 ADRs](architecture/README.md)
- [System invariants](architecture/system-invariants.md)
- [Consolidation amendments](architecture/consolidation.md)
- [Technical feasibility evidence (T01–T12)](feasibility/README.md)
- [Master roadmap overview](roadmap/overview.md)
- [Detailed roadmap reconstruction (accepted in PR #5)](roadmap/reconstruction-review.md)
- [Linear import verification and issue mapping](roadmap/linear-import-verification.md)
- [Agent instructions](../AGENTS.md)
- [Development workflow](developer-guide/git-workflow.md)
- [Development rules](developer-guide/development-rules.md)
- [Quality gates and evidence](developer-guide/quality-evidence.md)
- [Work orders and context handoff](developer-guide/work-order-handoff.md)

## Intended monorepo layout

| Path | Purpose |
| --- | --- |
| `apps/desktop/` | Desktop client |
| `crates/` | Rust core and focused modules |
| `docs/product/` | Product requirements |
| `docs/architecture/` | Architecture and decision records |
| `docs/feasibility/` | Sanitized feasibility evidence and limitations |
| `docs/roadmap/` | Versioned roadmap and acceptance plans |
| `docs/user-guide/` | Tested user documentation |
| `docs/developer-guide/` | Development guidance |
| `tests/` | Integration, security, regression and end-to-end tests |
| `scripts/` | Development and validation utilities |
| `fixtures/` | Synthetic test data |
| `.github/` | Repository automation and contribution templates |

Directories and modules will be created when needed. No empty application crates or untested build instructions are introduced during repository setup. Private project data, credentials and unsanitized logs must never be published.
