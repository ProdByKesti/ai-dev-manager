# Reconstructed work package catalogue — review draft

Status: incomplete, **not authorized for Linear import**. Names and stable IDs reconstructed from retained planning summaries, not a verbatim copy of the original detailed roadmap. Milestone counts checked against [approved overview](overview.md). No requirements, dependencies or test descriptions silently invented. The [JSON catalogue](catalogue-draft.json) uses null for unrecovered package-level data. The 526 count is a milestone-level target, not 526 recovered individual checks.

## M00 — Project Foundation

10 packages; M00 package acceptance criteria.

| Stable ID | Work package | Scope |
| --- | --- | --- |
| M00-01 | Repository Foundation | P0 |
| M00-02 | Product Specification | P0 |
| M00-03 | Technical Architecture Documentation | P0 |
| M00-04 | Feasibility Test Documentation | P0 |
| M00-05 | Development Environment Validation | P0 |
| M00-06 | Development Rules & AGENTS.md | P0 |
| M00-07 | Linear Project Setup | P0 |
| M00-08 | Quality & CI Foundation | P0 |
| M00-09 | Codex Workspace Setup | P0 |
| M00-10 | Foundation Acceptance | P0 |

## M01 — Application Foundation

12 packages; 24 planned checks (individual definitions pending).

| Stable ID | Work package | Scope |
| --- | --- | --- |
| M01-01 | Rust Workspace Foundation | P0 |
| M01-02 | Desktop Application Foundation | P0 |
| M01-03 | Domain Model Foundation | P0 |
| M01-04 | Persistent Storage Foundation | P0 |
| M01-05 | Persistent Event Bus & Outbox | P0 |
| M01-06 | Independent Core Process | P0 |
| M01-07 | Secure Local IPC | P0 |
| M01-08 | Configuration & Application Settings | P0 |
| M01-09 | Desktop-Core Lifecycle Integration | P0 |
| M01-10 | Logging & Diagnostics Foundation | P0 |
| M01-11 | Initial Dashboard & System Status | P0 |
| M01-12 | Application Foundation Acceptance | P0 |

## M02 — Execution & Security

15 packages; 40 planned checks (individual definitions pending).

| Stable ID | Work package | Scope |
| --- | --- | --- |
| M02-01 | Threat Model & Security Specification | P0 |
| M02-02 | Provider & Execution Adapter Interfaces | P0 |
| M02-03 | WSL2 Environment Manager | P0 |
| M02-04 | Credential Store & Authentication Boundary | P0 |
| M02-05 | Codex App Server Transport | P0 |
| M02-06 | Codex Authentication & Capability Discovery | P0 |
| M02-07 | Dynamic Permission Engine | P0 |
| M02-08 | Linux Sandbox Runtime | P0 |
| M02-09 | Git & Worktree Manager | P0 |
| M02-10 | Controlled Windows Execution Broker | P0 |
| M02-11 | Process Supervision & Cancellation | P0 |
| M02-12 | Single Agent Execution Pipeline | P0 |
| M02-13 | Authenticated Linux Inference Validation | P0 |
| M02-14 | Execution & Security Regression Suite | P0 |
| M02-15 | Execution & Security Acceptance | P0 |

## M03 — Project & Task Management

12 packages; 30 planned checks (individual definitions pending).

| Stable ID | Work package | Scope |
| --- | --- | --- |
| M03-01 | Project Domain & Persistence | P0 |
| M03-02 | Repository & Workspace Association | P0 |
| M03-03 | Existing Project Import | P0 |
| M03-04 | Project Templates & Creation Wizard | P0 |
| M03-05 | Roadmap & Milestone Management | P0 |
| M03-06 | Task & Work Package Management | P0 |
| M03-07 | Task State Machine | P0 |
| M03-08 | Dependency Graph Engine | P0 |
| M03-09 | Project Priority & Configuration Management | P0 |
| M03-10 | Local Search, Filtering & Activity History | P0 |
| M03-11 | Project Management Workspace UI | P0 |
| M03-12 | Project & Task Management Acceptance | P0 |

## M04 — Agent Management

14 packages; 36 planned checks (individual definitions pending).

| Stable ID | Work package | Scope |
| --- | --- | --- |
| M04-01 | Agent Role & Capability Model | P0 |
| M04-02 | Persistent Agent Identity | P0 |
| M04-03 | Provider Session Management | P0 |
| M04-04 | Direct Agent Chat & Intervention | P0 |
| M04-05 | Hierarchical Memory Storage | P0 |
| M04-06 | Deterministic Context Selection | P0 |
| M04-07 | Validated Session Handover | P0 |
| M04-08 | Automatic Session Rotation | P0 |
| M04-09 | Persistent Agent Message Bus | P0 |
| M04-10 | Controlled Agent-to-Agent Communication | P0 |
| M04-11 | Temporary Specialist Lifecycle | P0 |
| M04-12 | Agent Management Workspace UI | P0 |
| M04-13 | Agent & Context Regression Suite | P0 |
| M04-14 | Agent Management Acceptance | P0 |

## M05 — Orchestration Engine

16 packages; 42 planned checks (individual definitions pending).

| Stable ID | Work package | Scope |
| --- | --- | --- |
| M05-01 | Orchestration Domain & Execution Plan | P0 |
| M05-02 | AI Project Manager | P0 |
| M05-03 | Structured Plan Generation & Validation | P0 |
| M05-04 | Plan Approval & Revision Management | P0 |
| M05-05 | Deterministic DAG Scheduler | P0 |
| M05-06 | Agent Assignment Engine | P0 |
| M05-07 | Work Package Prompt Builder | P0 |
| M05-08 | Execution Dispatch & Run Tracking | P0 |
| M05-09 | Parallel Execution & Workspace Reservations | P0 |
| M05-10 | Basic Resource & Quota Guard | P0 |
| M05-11 | Dependency Handover & Result Processing | P0 |
| M05-12 | Blocker, Retry & Escalation Management | P0 |
| M05-13 | Dynamic Plan Change & User Intervention | P0 |
| M05-14 | Planner & Orchestration Workspace UI | P0 |
| M05-15 | Orchestration Regression & End-to-End Suite | P0 |
| M05-16 | Orchestration Engine Acceptance | P0 |

## M06 — Quality Engine

15 packages; 42 planned checks (individual definitions pending).

| Stable ID | Work package | Scope |
| --- | --- | --- |
| M06-01 | Quality Policy & Gate Configuration | P0 |
| M06-02 | Persistent Quality Evidence Store | P0 |
| M06-03 | Modular Test Adapter Framework | P0 |
| M06-04 | Protected Test & Acceptance Baseline | P0 |
| M06-05 | Requirements & Artifact Validation | P0 |
| M06-06 | Automated Validation & Regression Engine | P0 |
| M06-07 | Independent Review Engine | P0 |
| M06-08 | Quality Gate State Machine | P0 |
| M06-09 | Bounded Automatic Repair Loop | P0 |
| M06-10 | Integration Candidate & Conflict Validation | P0 |
| M06-11 | Human Acceptance & Approval Center | P0 |
| M06-12 | Controlled Git Integration & Task Finalization | P0 |
| M06-13 | Quality Workspace UI | P0 |
| M06-14 | Quality & Integration Regression Suite | P0 |
| M06-15 | Quality Engine & Autonomous Workflow Acceptance | P0 |

## M07 — Resource & Recovery

15 packages; 42 planned checks (individual definitions pending).

| Stable ID | Work package | Scope |
| --- | --- | --- |
| M07-01 | Resource & Recovery Domain Foundation | P0 |
| M07-02 | Provider Quota Monitoring | P0 |
| M07-03 | Hardware & Process Monitoring | P0 |
| M07-04 | Resource Profiles & Budget Configuration | P0 |
| M07-05 | Adaptive Model & Thinking Selection | P0 |
| M07-06 | Adaptive Admission & Reservation Control | P0 |
| M07-07 | Error Classification & Recovery Policy | P0 |
| M07-08 | Persistent Execution Checkpoints | P0 |
| M07-09 | Controlled Retry & Resume Manager | P0 |
| M07-10 | Startup Recovery & State Reconciliation | P0 |
| M07-11 | Backup & Disaster Recovery Foundation | P0 |
| M07-12 | Resource & Recovery Workspace UI | P0 |
| M07-13 | Resource & Quota Regression Suite | P0 |
| M07-14 | Recovery & Failure Injection Suite | P0 |
| M07-15 | Resource & Recovery Acceptance | P0 |

## M08 — Linear Integration

14 packages; 42 planned checks (individual definitions pending).

| Stable ID | Work package | Scope |
| --- | --- | --- |
| M08-01 | Integration Domain & Sync Architecture | P0 |
| M08-02 | Linear Authentication & Connection Manager | P0 |
| M08-03 | Linear GraphQL Adapter | P0 |
| M08-04 | External Project Discovery & Import | P0 |
| M08-05 | Persistent External ID & Field Mapping | P0 |
| M08-06 | Synchronization Policy & Ownership | P0 |
| M08-07 | Persistent Outbox & Idempotent Operations | P0 |
| M08-08 | Incremental Bidirectional Synchronization | P0 |
| M08-09 | Three-Way Conflict Detection & Resolution | P0 |
| M08-10 | Automated Progress & Quality Reporting | P0 |
| M08-11 | Offline Sync & Recovery Integration | P0 |
| M08-12 | Integration & Synchronization Workspace UI | P0 |
| M08-13 | Linear Sync & Conflict Regression Suite | P0 |
| M08-14 | Connected Workflow Acceptance | P0 |

## M09 — Workspace Experience

14 packages; 42 planned checks (individual definitions pending).

| Stable ID | Work package | Scope |
| --- | --- | --- |
| M09-01 | Unified Design System | P0 |
| M09-02 | Application Shell & Global Navigation | P0 |
| M09-03 | Unified Frontend State & IPC Integration | P0 |
| M09-04 | Global & Project Dashboard | P0 |
| M09-05 | Unified Planner & Project Workspace | P0 |
| M09-06 | Unified Agent & Development Workspace | P0 |
| M09-07 | Global Attention & Approval Center | P0 |
| M09-08 | Standard & Expert Mode | P0 |
| M09-09 | Global Settings & Integration Management | P0 |
| M09-10 | System Tray, Notifications & Keyboard Navigation | P0 |
| M09-11 | Localization & Accessibility | P0 |
| M09-12 | Frontend Performance & Large Workspace Optimization | P0 |
| M09-13 | Workspace Regression & Usability Suite | P0 |
| M09-14 | Unified Workspace Acceptance | P0 |

## M10 — Internal Alpha

14 packages; 48 planned checks (individual definitions pending).

| Stable ID | Work package | Scope |
| --- | --- | --- |
| M10-01 | Alpha Test Strategy & Environment | P0 |
| M10-02 | Full System Regression | P0 |
| M10-03 | Synthetic End-to-End Development Workflow | P0 |
| M10-04 | Real Greenfield Project Pilot | P0 |
| M10-05 | Existing Project Import Pilot | P0 |
| M10-06 | Dogfooding & Internal Development Evaluation | P0 |
| M10-07 | Parallel Execution & Long-running Stability | P0 |
| M10-08 | Resource Efficiency & Workflow Benchmark | P0 |
| M10-09 | Security & Adversarial Regression | P0 |
| M10-10 | Recovery & Integration Stress Testing | P0 |
| M10-11 | Usability & Onboarding Evaluation | P0 |
| M10-12 | Alpha Bug Fixing & Optimization | P0 |
| M10-13 | Final Alpha Regression & Evidence Review | P0 |
| M10-14 | Internal Alpha Acceptance | P0 |

## M11 — Public MVP

16 packages; 48 planned checks (individual definitions pending).

| Stable ID | Work package | Scope |
| --- | --- | --- |
| M11-01 | Release Strategy & Distribution Requirements | P0 |
| M11-02 | Public Provider Authentication | P0 |
| M11-03 | Dependency, License & Supply Chain Audit | P0 |
| M11-04 | Production Build & CI/CD Pipeline | P0 |
| M11-05 | Windows Installer & Uninstaller | P0 |
| M11-06 | First Launch & Setup Wizard | P0 |
| M11-07 | WSL2 & Runtime Provisioning | P0 |
| M11-08 | Signed Updates & Release Channels | P0 |
| M11-09 | Upgrade, Migration & Rollback Safety | P0 |
| M11-10 | Public Documentation & User Guides | P0 |
| M11-11 | Privacy, Security Reporting & Community Foundation | P0 |
| M11-12 | Clean Windows Installation & Compatibility Suite | P0 |
| M11-13 | Public Beta Release | P0 |
| M11-14 | Beta Feedback & Release Stabilization | P0 |
| M11-15 | Portfolio, Release Presentation & Public Assets | P0 |
| M11-16 | Public MVP Acceptance & Release | P0 |

## M12 — Extended Platform

16 packages; 42 planned checks (individual definitions pending).

| Stable ID | Work package | Scope |
| --- | --- | --- |
| M12-01 | Extension Architecture & Compatibility Foundation | P1 |
| M12-02 | GitHub Authentication & Repository Integration | P1 |
| M12-03 | GitHub Development Workflow Automation | P1 |
| M12-04 | MCP Server Management & Discovery | P1 |
| M12-05 | Secure MCP Tool Broker | P1 |
| M12-06 | Advanced Automated Recovery | P1 |
| M12-07 | Extended Multi-Provider Architecture | P2 |
| M12-08 | Additional Cloud AI Providers | P2 |
| M12-09 | Optional Local AI Runtime | P2 |
| M12-10 | Semantic Memory & Embedding Infrastructure | P2 |
| M12-11 | Hybrid Context Retrieval & Optimization | P2 |
| M12-12 | Advanced Autonomous Planning | P2 |
| M12-13 | Additional Project Management & Test Adapters | P2 |
| M12-14 | Customizable Workspace & Developer Tools | P2 |
| M12-15 | Extension Regression & Security Validation | release-dependent P1/P2 |
| M12-16 | Extended Platform Release Acceptance | release-dependent P1/P2 |

## M13 — Community Ecosystem

18 packages; 48 planned checks (individual definitions pending).

| Stable ID | Work package | Scope |
| --- | --- | --- |
| M13-01 | Cross-platform Architecture Foundation | P2 |
| M13-02 | Native Linux Support | P2 |
| M13-03 | Native macOS Support | P2 |
| M13-04 | Cross-platform Compatibility & Release Matrix | P2 |
| M13-05 | Public Plugin SDK & Extension Contract | P3 |
| M13-06 | Isolated Plugin Runtime & Security Broker | P3 |
| M13-07 | Plugin Developer Tooling & Documentation | P3 |
| M13-08 | Community Plugin Registry & Discovery | P3 |
| M13-09 | Secure Plugin Distribution & Update Lifecycle | P3 |
| M13-10 | Community Templates & Workflow Sharing | P3 |
| M13-11 | Remote Worker Protocol & Device Trust | P3 |
| M13-12 | Remote Worker Runtime & Resource Management | P3 |
| M13-13 | Distributed Orchestration & Job Scheduling | P3 |
| M13-14 | Collaborative Team Workspace Architecture | P3 |
| M13-15 | Shared Context & Collaborative Synchronization | P3 |
| M13-16 | Optional Hosted Services & Sustainability Evaluation | P3 |
| M13-17 | Ecosystem Security, Compatibility & Regression | release-dependent P2/P3 |
| M13-18 | Community Ecosystem Release & Governance | release-dependent P2/P3 |

## Known limitations

The full historical package dependency graph is not available. The earlier reported 697 edges cannot be verified from the available sources. The explicitly retained K04 and K02 relationships, and one separately marked derived minimum gate, are included in the JSON as a tiny incomplete subset. No full graph validation is claimed. Do not dispatch from this subset.

See [import preflight](import-preflight.md), [consolidation amendments](../architecture/consolidation.md) and [system invariants](../architecture/system-invariants.md).
