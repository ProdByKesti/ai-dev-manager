# Master roadmap overview

Approved planning baseline: 14 milestones, 201 work packages (167 P0, 34 post-MVP), 526 planned higher-level acceptance checks in M01–M13; M00 uses package acceptance criteria. These are planning counts, not completed tests.

| Milestone | Name | Packages | Planned checks | Scope |
| --- | --- | ---: | ---: | --- |
| M00 | Project Foundation | 10 | Package criteria | P0 |
| M01 | Application Foundation | 12 | 24 | P0 |
| M02 | Execution & Security | 15 | 40 | P0 |
| M03 | Project & Task Management | 12 | 30 | P0 |
| M04 | Agent Management | 14 | 36 | P0 |
| M05 | Orchestration Engine | 16 | 42 | P0 |
| M06 | Quality Engine | 15 | 42 | P0 |
| M07 | Resource & Recovery | 15 | 42 | P0 |
| M08 | Linear Integration | 14 | 42 | P0 |
| M09 | Workspace Experience | 14 | 42 | P0 |
| M10 | Internal Alpha | 14 | 48 | P0 |
| M11 | Public MVP | 16 | 48 | P0 |
| M12 | Extended Platform | 16 | 42 | P1–P2 |
| M13 | Community Ecosystem | 18 | 48 | P2–P3 |
M00–M11 are required for public MVP. M12 and M13 are modular, independently scoped extensions. Release order and provisional performance targets are revisited against evidence. No dates or workload estimate are implied by package counts.

## Mandatory transitions

M00 foundation acceptance precedes M01. M02 acceptance requires authenticated Linux inference and isolation evidence. M05 parallel dispatch depends on the basic quota guard. M06 requires all mandatory quality gates and approved integration. M07 requires verified recovery. M08 requires controlled Linear synchronization. M09 requires the normal workflows through the GUI. M10 requires full regression and real isolated pilots, no open S0/S1 blockers. M11 requires public auth, distribution and installer/update validation, and explicit release authorization. Each optional extension release has separate security and regression acceptance.

The complete package catalogue, dependency edges, acceptance criteria and Linear mappings are recorded in the approved detailed roadmap and import verification documents. This overview does not replace the detailed roadmap.
