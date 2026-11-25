# Documentation

This repository is in the foundation phase. Approved decisions are versioned here; implementation and validation are separate work.

- [Product specification — 25 decisions](product/product-specification.md)
- [Technical architecture and 15 ADRs](architecture/README.md)
- [System invariants](architecture/system-invariants.md)
- [Consolidation amendments](architecture/consolidation.md)
- [Master roadmap overview](roadmap/overview.md)
- [Development workflow](developer-guide/git-workflow.md)

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
