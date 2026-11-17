# Lab 3 — Architectural Pattern Selection & Component Modelling

**Problem Statement #42 — Internal Microservice Catalog & Health Portal**
PES University · Dept. of CSE · Chennupati Niraj Kumar · PES2UG24AM046 · Sec 5-A · 17 November 2026

Same scenario as Lab 1 and Lab 2.

## Deliverables

| File | Description |
| :--- | :--- |
| [`Component_Diagram.pdf`](Component_Diagram.pdf) · [`.png`](Component_Diagram.png) · [editable source](Component_Diagram_source.pptx) | UML component diagram: **8 components** grouped into edge / domain / operations / monitoring tiers, **10 provided interfaces** (lollipops) with assembly connections, **1 `«use»` dependency**, 2 external systems, a notation legend and requirement traceability |
| [`Architecture_Justification.docx`](Architecture_Justification.docx) · [`.pdf`](Architecture_Justification.pdf) | One-page justification: chosen architecture, styles compared, two reasons, security advantage, performance benefit and the trade-off accepted |

## Architecture: Microservices (edge tier → domain tier → monitoring tier)

| Component | Responsibility | Requirements |
| :--- | :--- | :--- |
| Portal Web UI | Health dashboard, dependency-graph viewer, API documentation search | FR-001, FR-003, FR-004 |
| Catalog API Gateway | SSO token validation, routing, rate limits, role filtering | FR-002, NFR-001 |
| Service Registry | Service records, owners, validation and de-duplication | FR-002 |
| API Doc Indexer | OpenAPI ingest, version pinning, search index | FR-004 |
| Dependency Graph Engine | Edges, cached layouts, impact queries | FR-003, NFR-001 |
| Availability & Alert Engine | Rolling 24-h availability, threshold rules, alert dispatch | FR-001, FR-005 |
| Config & Audit Service | Probe/alert configuration, RBAC, append-only audit log | FR-005 |
| Health Probe Scheduler | Sharded 30-second probe wheel at 2,000-service scale | FR-001, NFR-002 |

External systems: **Monitored Microservice** (exposes `/health`) and **Alerting Gateway** (Slack / PagerDuty /
e-mail webhook).

## Interfaces

| Interface | Provider → Requirer | Technology |
| :--- | :--- | :--- |
| ICatalogApi | Catalog API Gateway → Portal Web UI | HTTPS + JSON (REST) |
| ICatalogStore | Service Registry → Catalog API Gateway | gRPC, ACL-checked |
| IDocSearch | API Doc Indexer → Catalog API Gateway | REST (search query) |
| IGraphQuery | Dependency Graph Engine → Catalog API Gateway | REST (graph snapshot, p95 ≤ 3 s) |
| IHealthQuery | Availability & Alert Engine → Catalog API Gateway | REST (status + 24-h availability) |
| IManifest | Service Registry → API Doc Indexer | Internal call (spec URL + repo token) |
| IProbeConfig | Config & Audit Service → Health Probe Scheduler | Event stream (interval, timeout, threshold) |
| IProbeResult | Health Probe Scheduler → Availability & Alert Engine | Event stream (probe outcome) |
| IHealthEndpoint | Monitored Microservice → Health Probe Scheduler | HTTPS GET `/health` (≤ 5 s timeout) |
| IAlertTransport | Alerting Gateway → Availability & Alert Engine | HTTPS webhook (Slack / PagerDuty) |

Usage dependency (`«use»`): Availability & Alert Engine → Config & Audit Service (alert thresholds and channels).
