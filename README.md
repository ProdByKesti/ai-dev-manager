# AI Dev Manager

An open-source, local-first orchestration platform for AI-assisted software development, multi-agent coordination, quality assurance and project management.

> **Project status: foundation and planning.** The application is not implemented yet. There is no installer, runnable release or supported production workflow at this stage.

## Vision

Bring project planning, specialized AI agents, persistent development context, automated verification and controlled integration into a single desktop workspace, with humans retaining authority over consequential decisions.

## Planned first release

- Local project, milestone and task management with dependency-aware scheduling.
- Specialized agents, persistent context and controlled session rotation.
- Codex-first execution using an eligible user-provided account, subject to provider compatibility and terms.
- Scoped execution permissions, isolated workspaces and explicit approvals.
- Automated tests, independent reviews and evidence-based quality gates.
- Local Git workflows and optional bidirectional Linear synchronization.
- Resource limits, checkpoints and controlled recovery.
- Windows desktop application with English and German interfaces.

These are planned capabilities, not currently available features. Native Linux/macOS desktop support, additional providers, general MCP integration, public plugins and distributed collaboration are post-MVP directions.

## Planned architecture

The initial target is a Windows desktop client using Tauri, React and TypeScript, with an independent Rust core, SQLite persistence and a native Linux agent execution environment under WSL2. Platform-specific operations must be explicitly authorized. The implementation and public authentication paths still require validation.

The core is intended to work locally without mandatory hosting or an ADM subscription. AI providers may have their own account requirements and costs; automatic paid fallback is not planned.

## Development

The project is currently establishing its repository and documentation. Build and installation instructions will be added only when they have been tested.

See the [development workflow](docs/developer-guide/git-workflow.md) for branch, review and integration rules and the [documentation overview](docs/README.md) for the intended repository layout.

## License

Apache License 2.0. See [LICENSE](LICENSE).


Temporary M00-08 negative test — DO NOT MERGE: [intentionally missing document](m00-08-negative-test-intentionally-missing.md).
