# Product specification

Status: approved conceptual baseline, recorded for M00-02; implementation not started. Detailed work packages and acceptance plans will be recorded separately. No claim of current product availability.

## Vision and intended users

AI Dev Manager (ADM) is a local-first development coordination platform for individual developers and small development projects using specialized AI agents. Its purpose is to reduce repetitive planning, handoffs, testing and progress coordination while preserving human authority, engineering evidence and project isolation. It is not a general IDE replacement or an unrestricted autonomous code execution service.

## Approved product decisions (25)

### PD-01 — Human-in-the-loop orchestration

Start with semi-automated coordination of specialized agents. Humans approve consequential scope, permissions, acceptance and releases. Bounded autonomous cycles are post-MVP.

Roadmap: M05, M06, M12.

### PD-02 — Provider neutrality

Use versioned provider adapters, Codex first. The initial owner workflow targets an eligible existing ChatGPT account without extra paid fallback. Provider eligibility, terms and public authentication require validation.

Roadmap: M02, M11, M12.

### PD-03 — Local desktop platform

Windows-first hybrid desktop application; independent local core, Tauri client, Linux execution under WSL2. No mandatory hosting.

Roadmap: M01, M02.

### PD-04 — Project templates and roles

Support empty projects and configurable templates for desktop, web, Android, games and custom projects; users can define roles and capabilities.

Roadmap: M03, M04.

### PD-05 — Collaborative planning

The AI planner proposes structured roadmaps and work packages; the human approves the plan before deterministic dispatch. Changes outside approved scope require approval.

Roadmap: M05.

### PD-06 — Risk-based human control

Use risk-based approvals with milestone acceptance; approvals bind to the exact revision and operation. Agents cannot grant themselves permissions or waive required gates.

Roadmap: M02, M05, M06.

### PD-07 — Persistent agent memory

Maintain agent identities independently of provider sessions, hierarchical persistent context, validated handovers and automatic safe session rotation.

Roadmap: M04.

### PD-08 — Parallel development

Use dependency-aware scheduling and separate Git worktrees for compatible jobs; enforce resource reservations and execution isolation. Worktrees are not a sandbox.

Roadmap: M02, M05.

### PD-09 — Standalone core

Local project management works without integrations or inference. Codex, Git, Linear and later GitHub/MCP connect through adapters.

Roadmap: M01, M08, M12.

### PD-10 — Configurable synchronization

Support off/import/export/bidirectional per project; imported projects initially read-only. Linear owns agreed external fields of existing Linear projects; internal gates stay ADM-owned. Preserve history and resolve conflicts explicitly.

Roadmap: M08.

### PD-11 — Resource management

Offer Eco, Balanced and Performance profiles; measure hardware and available provider limits. Unknown quota blocks automatic inference. No fixed prediction of remaining tasks.

Roadmap: M05, M07.

### PD-12 — Bounded escalation

Technical retries, repairs, model escalation and communication use cumulative persistent budgets; unknown or security-critical failures stop or escalate.

Roadmap: M05, M06, M07.

### PD-13 — Workspace UI

Modular dashboard and chat-oriented workspace, project switcher, activity, attention center, light/dark themes and live status.

Roadmap: M09.

### PD-14 — Public MVP integration scope

Linear synchronization is required in the public MVP even though connecting an account is optional for individual users. Import, status/progress updates, stable IDs, history, deduplication and conflict handling are mandatory.

Roadmap: M08, M11.

### PD-15 — Existing project import

Read-only inspection and preview before importing or writing; optional AI assistance within approved budget, manual fallback, no automatic mutation of source repositories.

Roadmap: M03, M08.

### PD-16 — Controlled agent communication

Direct agent-to-agent communication through a typed, persistent, authorized local message bus; no default cross-project routing or rights escalation.

Roadmap: M04.

### PD-17 — Adaptive quality assurance

Use project-specific tests, protected requirements, independent reviews as required, integration validation and personal acceptance when required. Claims are not evidence.

Roadmap: M06.

### PD-18 — Background operation

Independent core continues when the UI closes; tray controls and explicit shutdown. Controlled recovery in MVP, broader automatic crash recovery later.

Roadmap: M01, M07, M12.

### PD-19 — Project priorities

Configurable project/task priorities with starvation prevention and resource-aware scheduling.

Roadmap: M03, M05.

### PD-20 — Observability and interventions

Expose actual run states, logs, blockers, approvals and controls. Distinguish pause, cancel and emergency stop.

Roadmap: M05, M09.

### PD-21 — Enforced least privilege

Security is enforced by runtime boundaries, brokers and policies, not merely prompts. Unknown permissions fail closed; no insecure fallback.

Roadmap: M02, M10.

### PD-22 — Modular extensibility

Versioned internal adapter contracts in MVP and extended platform; public plugin SDK and isolated community runtime later.

Roadmap: M12, M13.

### PD-23 — Standard and Expert modes

Same core, data and security rules; Expert exposes additional details and configuration, Standard is default. Critical warnings and required decisions remain visible in both.

Roadmap: M09.

### PD-24 — Internationalization

English application default, German equally supported; independent conversation and documentation language preferences. Extensible translations; do not rewrite existing documents automatically.

Roadmap: M09, M11.

### PD-25 — Free open-source local product

Apache-2.0 local core and local functionality without mandatory ADM subscription. Optional future hosting requires separate feasibility, cost and security decisions; external providers may impose their own charges.

Roadmap: M00, M11, M13.

## MVP scope and boundaries

P0 covers M00–M11: Windows desktop and independent core, Codex-first execution, local Git, persistent agents/context, deterministic coordination, quality gates, resource and controlled recovery management, optional connection to mandatory MVP Linear support, unified English/German workspace and public release preparation. Public beta precedes proposed v0.1.0. Public auth, safe runtime, distribution terms and installer/update validation are release gates, not assumed capabilities.

P1/P2 in M12: GitHub workflow integration, secure MCP, fuller safe recovery, additional providers and optional local models, hybrid semantic context, bounded autonomous cycles and customizable workspace. P2/P3 in M13: native Linux/macOS desktop, isolated plugin SDK and catalogue, shared templates, remote workers, collaboration and optional hosting evaluation. These are modular later directions, not MVP requirements.

## Product success and constraints

Required workflows must pass their mandatory checks with evidence and authorized human acceptance. No open S0/S1 release blockers. The proposed 50% reduction of active human coordination time is a benchmark hypothesis, not a proven benefit or automatic release gate. No additional mandatory paid services; provider quotas and eligibility vary. The initial development environment and public distribution assumptions still require validation.

See [architecture](../architecture/README.md), [system invariants](../architecture/system-invariants.md), [consolidation decisions](../architecture/consolidation.md) and [roadmap overview](../roadmap/overview.md).
