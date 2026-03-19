# UASL — Universal Application Specification Language

> Describe applications at the semantic level. Generate code for any framework.

---

## What is UASL?

UASL is a family of four declarative specifications that together describe a complete application — its domain model, user interface intent, API contract, and business workflow — without coupling to any framework, programming language, or runtime.

A conforming compiler reads UASL documents and generates production code for any target platform (xframe5, Vue, React, Spring Boot, etc.), producing identical output from identical input.

## Spec Family

| # | Spec | What it describes | Version |
|---|------|-------------------|---------|
| 1 | [Entity Spec](02-entity-spec.md) | Domain model: entities, attributes, relations | v1.0 |
| 2 | [IAS](03-ias-spec.md) | API contract: intent-to-HTTP mapping | v1.0 |
| 3 | [SUIS](04-suis-spec.md) | UI intent: screens, operations, navigation | v1.1 |
| 4 | [Workflow](05-workflow-spec.md) | State machines: states, transitions, guards | v1.0 |

Start with the [Overview](01-overview.md) to understand how the specs fit together, or jump directly to any spec above.

## Quick Navigation

- [Overview — Architecture & Design Philosophy](01-overview.md)
- [Entity Spec — Domain Model](02-entity-spec.md)
- [IAS — Intent API Specification](03-ias-spec.md)
- [SUIS — Semantic UI Specification](04-suis-spec.md)
- [Workflow Spec — State Machine](05-workflow-spec.md)
- [Glossary — All Terms](glossary.md)
- [Training Guide — LLM Prompt Engineering for UASL](UASL_TRAINING_GUIDE.md)

## Reading Order

For first-time readers, we recommend:

1. **[Overview](01-overview.md)** — understand the big picture
2. **[Entity Spec](02-entity-spec.md)** — the foundation all specs build on
3. **[IAS](03-ias-spec.md)** — how intents map to HTTP
4. **[SUIS](04-suis-spec.md)** — how UIs are described semantically
5. **[Workflow](05-workflow-spec.md)** — how state machines work

The [Glossary](glossary.md) is a useful reference to keep open alongside any spec.

---

*UASL v1.0 — Candidate Recommendation — 2026-01-29*

[한국어 버전](../ko/README.md)
