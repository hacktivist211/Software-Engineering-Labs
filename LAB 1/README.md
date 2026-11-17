# Lab 1 — Requirements Engineering & UML Use-Case Modelling

**Problem Statement #42 — Internal Microservice Catalog & Health Portal** (Developer Tools & IT Operations)
PES University · Dept. of CSE · Chennupati Niraj Kumar · PES2UG24AM046 · Sec 5-A · 17 November 2026

## Deliverables

| # | File | Contents |
| :-: | :--- | :--- |
| 1 | [`Requirements_Table.docx`](Requirements_Table.docx) · [`.pdf`](Requirements_Table.pdf) | **Exactly 5 FRs** (`FR-001`–`FR-005`) and **2 NFRs** (`NFR-001`, `NFR-002`), each with Req ID, Type, Description, Priority, measurable pass/fail Acceptance Criteria, Rationale and a peer-review Comments column |
| 2 | [`UML_Use_Case_Diagram.pdf`](UML_Use_Case_Diagram.pdf) · [`.png`](UML_Use_Case_Diagram.png) · [editable source](UML_Use_Case_Diagram_source.pptx) | 4 actors, system boundary, **9 use cases** (`UC-01`–`UC-09`), associations, **two `«include»`** and **one conditional `«extend»`**, notation legend and requirement traceability |
| 3 | [`Use_Case_Flow.docx`](Use_Case_Flow.docx) · [`.pdf`](Use_Case_Flow.pdf) | One-page flow for **UC-07 Monitor Service Health Dashboard**: preconditions, success/failure postconditions, 10-step main success scenario, alternate flows `4a` and `6a` |

The two briefs used for this lab are kept in [`reference/`](reference).

## Actors

| Actor | Type | Purpose |
| :--- | :--- | :--- |
| DevOps Engineer | Primary | Onboards services, browses API documentation, watches the health dashboard |
| System Architect | Primary | Maps dependencies and investigates the topology graph for blast radius |
| Platform Administrator | Primary | Owns probe/alert configuration, roles and the audit trail |
| Alerting Gateway | Secondary (external) | Receives downtime and recovery notifications |

## Use cases

| ID | Use case | Actor(s) | Requirement |
| :--- | :--- | :--- | :--- |
| UC-01 | Register / Update Microservice Profile | DevOps Engineer | FR-002 |
| UC-02 | Validate Service Manifest | *included by UC-01* | FR-002 |
| UC-03 | Map Service Dependencies | System Architect | FR-003 |
| UC-04 | View Interactive Dependency Topology | System Architect, DevOps Engineer | FR-003, NFR-001 |
| UC-05 | Browse Aggregated API Documentation | DevOps Engineer | FR-004 |
| UC-06 | Configure Health Probes & Alert Rules | Platform Administrator | FR-005 |
| UC-07 | Monitor Service Health Dashboard | Platform Administrator, DevOps, Architect | FR-001 |
| UC-08 | Compute Rolling Availability Metrics | *included by UC-07* | FR-001, NFR-002 |
| UC-09 | Dispatch Downtime Alert | Alerting Gateway | FR-001 |

## Relationships

| Relationship | From → To | Why |
| :--- | :--- | :--- |
| `«include»` | UC-01 → UC-02 | A service profile is always validated before it is stored |
| `«include»` | UC-07 → UC-08 | Opening the dashboard always requires availability to be computed |
| `«extend»` | UC-09 → UC-08 | Alert dispatch is conditional: `[3 consecutive failed probes]` |

## Compliance with the brief

| Requirement of the brief | Delivered |
| :--- | :--- |
| Exactly 5 FRs `FR-001`–`FR-005` | `FR-001` retained from the problem statement, `FR-002`–`FR-005` elicited |
| 2 NFRs `NFR-001`, `NFR-002` | `NFR-001` retained, `NFR-002` added |
| ID, Type, Description, Priority, Acceptance Criteria, Rationale | Present, plus the template's Comments column |
| Measurable pass/fail criteria on every row | Every row states an explicit Pass and Fail condition with a number |
| ≥ 1 `«include»` and ≥ 1 `«extend»` | 2 includes, 1 conditional extend |
| ≥ 3 actors, ≥ 5 use cases | 4 actors, 9 use cases |
| One-page flow with pre/postconditions, main scenario, alternate flow | 1 page, 2 alternate flows, exported to PDF |

`FR-001` and `NFR-001` are the requirements supplied in the problem statement; their wording is preserved and only
their acceptance criteria and rationale were made measurable, as the template requires.
