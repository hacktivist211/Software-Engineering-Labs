# Lab 2 — Agile Backlog Creation & Sprint Simulation

**Problem Statement #42 — Internal Microservice Catalog & Health Portal**
PES University · Dept. of CSE · Niraj · PES2UG24AM046 · 17 November 2026

The backlog is derived from the Lab 1 requirements FR-001 to FR-005, NFR-001 and NFR-002: **4 epics, 11 user
stories, 48 story points** on the Fibonacci scale, planned across **two one-week sprints of 24 points each**.

## Deliverables

| File | Contents |
| :--- | :--- |
| [`Lab2_Submission.docx`](Lab2_Submission.docx) · [`.pdf`](Lab2_Submission.pdf) | Backlog summary, backlog and sprint-plan tables, Definition of Done, sprint-simulation figures, the four reflection answers, and the Jira reproduction steps |
| [`Jira_Backlog_Import.csv`](Jira_Backlog_Import.csv) | The 4 epics and 11 stories in Jira's import column order (Issue Type, Summary, Description, Priority, Story Points, Epic Name, Epic Link, Sprint) |
| [`figures/`](figures) | `1_sprint_board.png` (board at end of Sprint 1), `2_sprint1_burndown.png`, `3_sprint2_burndown.png` |

## Backlog

| Epic | Story | Req | Priority | Points | Sprint |
| :--- | :--- | :--- | :--- | :-: | :-: |
| EPIC1 Service Catalog & Registration | S1 Register a microservice profile | FR-002 | High | 5 | 1 |
| | S2 Validate and de-duplicate catalog records | FR-002 | High | 3 | 1 |
| EPIC2 Dependency Intelligence | S3 Map dependencies between services | FR-003 | High | 5 | 1 |
| | S7 Render the interactive dependency graph | FR-003 · NFR-001 | High | 8 | 2 |
| EPIC3 API Documentation Index | S5 Ingest OpenAPI specifications | FR-004 | High | 5 | 1 |
| | S6 Search operations across services | FR-004 | Medium | 3 | 1 |
| EPIC4 Health Monitoring & Alerting | S4 Probe service health every 30 seconds | FR-001 · NFR-002 | High | 3 | 1 |
| | S8 Compute 24-hour availability dashboard | FR-001 | High | 5 | 2 |
| | S9 Configure probes, thresholds and alert channels | FR-005 | High | 5 | 2 |
| | S10 Dispatch downtime and recovery alerts | FR-005 | High | 3 | 2 |
| | S11 Enforce admin-only configuration with an audit trail | FR-005 | Medium | 3 | 2 |

**Sprint 1 — 24 points.** Goal: a DevOps Engineer can register a service, have it validated, declare its
dependencies, publish its OpenAPI specification and see it probed every 30 seconds.

**Sprint 2 — 24 points.** Goal: 200-service interactive topology graph, rolling 24-hour availability dashboard,
configurable thresholds, single audited downtime/recovery alerts.

Story points use the Fibonacci scale, with "Validate and de-duplicate catalog records" (3) as the baseline. The
8-point story carries the most uncertainty: a 200-service / 400-edge graph interactive in ≤ 3 s at p95 with
≥ 30 fps pan and zoom (NFR-001).

## Reproducing this in Jira

`Jira_Backlog_Import.csv` imports through **Settings → System → External system import → CSV**. Map the columns,
create Sprint 1 and Sprint 2 on the board, and drag the stories in the order above. The four views worth capturing
for a screenshot trail are: the backlog with the epic panel and story points, the Sprint 1 board mid-sprint, the
Sprint 1 burndown after completion, and the Sprint 2 burndown after completion.
