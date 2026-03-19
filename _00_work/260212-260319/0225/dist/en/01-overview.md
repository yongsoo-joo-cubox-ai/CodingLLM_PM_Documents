[Home](README.md) | [Next: Entity Spec →](02-entity-spec.md)

---

# UASL Overview

## 1. What is UASL?

UASL stands for **Universal Application Specification Language**. It is a family of four specifications that describe applications at the semantic level -- what an application *is*, not how it is built.

The four specs are:

- **Entity Spec** -- the domain model (entities, attributes, relations)
- **SUIS** (Semantic UI Specification) -- the user interface intent (screens, operations, navigation)
- **IAS** (Intent API Specification) -- the API contract (intent-to-HTTP mapping)
- **Workflow Spec** -- the business process (state machines, transitions, guards)

Together, they give you a complete, machine-readable description of an application feature. That description is framework-agnostic: it says nothing about Spring Boot, Vue, React, or any other technology. A UASL compiler reads these specs and generates production code for whichever target platform you need.

The key property is **deterministic compilation**: the same specs always produce the same output. No randomness, no AI in the generation step. You write the specs (or an AI helps you draft them), the compiler validates them, and the compiler emits code. Every time.

---

## 2. Design Philosophy

Five principles guide every design decision in UASL.

| Principle | What it means | Example |
|-----------|---------------|---------|
| **Semantic over syntactic** | Describe *what* something is, not *how* it looks or works | A field is `type: enum`, not `<select>` or `SBCombo` |
| **Intent over implementation** | Name the user's goal, not the HTTP plumbing | `intent: search`, not `GET /api/tasks?q=...` |
| **Framework-agnostic** | No framework concepts leak into specs | No "Vue component", no "Spring controller" -- just entities, screens, intents |
| **Machine-verifiable** | Specs are validated by JSON Schema and semantic rules | You know a spec is valid *before* code generation starts |
| **Fail-fast** | Invalid specs are rejected immediately | A typo in a field name produces a clear error, never silently wrong code |

The underlying idea: if you get the semantics right, the compiler can handle the syntax for any target platform.

---

## 3. Layered Architecture

The four specs form a dependency hierarchy. Entity Spec is the foundation. Everything else builds on it.

```
                   ┌─────────────────────────┐
                   │       Entity Spec        │
                   │     (the foundation)     │
                   └────┬─────────────┬───────┘
                        │             │
                ┌───────▼───┐   ┌─────▼───────┐
                │    IAS    │   │  Workflow    │
                │ (API map) │   │ (states)    │
                └───────┬───┘   └─────────────┘
                        │
                ┌───────▼───────┐
                │     SUIS      │
                │  (UI intent)  │
                └───────────────┘
```

Reading the diagram bottom-up: SUIS depends on both Entity Spec (to know what domain it describes) and IAS (to know how intents map to HTTP). IAS depends on Entity Spec (to know which entities have API resources). Workflow depends on Entity Spec (to know which entity has a status field). Workflow is optionally referenced by SUIS and IAS, but does not require them.

Here are the dependencies spelled out:

| Spec | Depends on | Used by |
|------|------------|---------|
| **Entity Spec** | nothing | SUIS, IAS, Workflow |
| **IAS** | Entity Spec | SUIS |
| **SUIS** | Entity Spec, IAS | Workflow (optionally) |
| **Workflow** | Entity Spec | SUIS (optionally), IAS (optionally) |

Because Entity Spec is the foundation, it is always authored and validated first.

---

## 4. How It Works

Here is the typical flow from authoring to code generation:

```
 Step 1          Step 2           Step 3            Step 4           Step 5
┌──────┐      ┌──────────┐    ┌────────────┐    ┌────────────┐   ┌──────────┐
│ Write│      │ Validate │    │  Cross-Spec│    │  Compile   │   │  Output  │
│ YAML │ ───► │  against │ ──►│  Semantic  │ ──►│  to Target │──►│  Source  │
│ Specs│      │  Schemas │    │ Validation │    │  Framework │   │   Code   │
└──────┘      └──────────┘    └────────────┘    └────────────┘   └──────────┘
```

**Step 1: Author UASL documents.** You write your specs in YAML. Each spec describes one concern -- domain model, UI screens, API mapping, or workflow. You can write them by hand, or an AI system can draft them for you.

**Step 2: Validate against JSON Schemas.** Each spec has a corresponding JSON Schema. This catches structural problems: missing required fields, wrong types, unknown keys. Think of it as a type checker for your specs.

**Step 3: Cross-spec semantic validation.** The validator checks that specs are consistent with each other. Does the SUIS screen reference an entity that actually exists? Does every intent in SUIS have a corresponding IAS mapping? Does the workflow's status field match an enum attribute on the entity? This is where most real-world errors are caught.

**Step 4: Compile to target framework.** The compiler reads the validated specs and generates framework-specific code. An xframe5 adapter produces xframe5 DataSources and SBGrid handlers. A Vue adapter produces Vue components and composables. A Spring Boot adapter produces controllers and services.

**Step 5: Get source code.** Same specs, same output, every time. You can change the target framework without changing a single line in your specs.

---

## 5. Validation and Conformance

UASL defines three levels of validation, each building on the previous one.

### Level 1 -- Structural

The spec passes its JSON Schema. This verifies that required fields are present, values have the right types, and enum values are within allowed sets.

Example: an Entity Spec with a missing `primary_key` field fails L1 validation.

### Level 2 -- Semantic

The spec passes intra-spec semantic rules that JSON Schema alone cannot express.

Examples:
- An entity's `primary_key` value references an attribute that actually exists in that entity.
- A workflow has exactly one `initial` state.
- An enum attribute has at least one value.

### Level 3 -- Complete

All cross-spec referential integrity rules pass.

Examples:
- A SUIS screen's `subject.domain` references an entity defined in the Entity Spec.
- Every intent used in SUIS has a corresponding mapping in IAS.
- A workflow's `status_field` references an enum attribute on its bound entity.

### Validation Order

Cross-spec validation proceeds in a fixed order:

```
Entity Spec  ──►  IAS  ──►  SUIS  ──►  Workflow
     1              2          3            4
```

Entity Spec is validated first because it has no external dependencies. IAS is next because it only references entities. SUIS follows because it references both entities and IAS intents. Workflow is last because it may cross-reference entities and optionally SUIS screens.

---

## 6. Serialization

**Authoring format: YAML.** All UASL specs are written in YAML. It is readable, supports comments, and works well in code reviews.

**Validation format: JSON Schema.** Each spec has a corresponding JSON Schema file (Draft 2020-12). During validation, the YAML document is converted to JSON and checked against the schema.

Schema files live in the `schemas/` directory:

```
schemas/
├── entity/v1.0/
│   └── root.schema.json
├── ias/v1.0/
│   └── root.schema.json
├── suis/v1.1/
│   └── root.schema.json
└── workflow/v1.0/
    └── root.schema.json
```

---

## 7. Spec Status

All four specifications are currently at the **Candidate Recommendation** stage. This means they are feature-complete and being validated through implementation feedback. No breaking changes are expected, but minor additions may still occur before reaching Standard status.

| Spec | Version | Status |
|------|---------|--------|
| Entity Spec | v1.0 | Candidate Recommendation |
| IAS | v1.0 | Candidate Recommendation |
| SUIS | v1.1 | Candidate Recommendation |
| Workflow Spec | v1.0 | Candidate Recommendation |

**Versioning scheme:** Each spec uses major.minor versioning. A minor version bump (e.g., 1.0 to 1.1) adds new optional features and is always backward compatible. A major version bump (e.g., 1.x to 2.0) may introduce breaking changes and will include migration guidance.

---

## 8. Next Steps

Ready to dive into the specs? Here is the recommended reading order:

| Document | What you will learn |
|----------|---------------------|
| [Entity Spec](02-entity-spec.md) | How to define domain models -- entities, attributes, relations, computed fields |
| [IAS](03-ias-spec.md) | How to map semantic intents to HTTP operations |
| [SUIS](04-suis-spec.md) | How to describe UI screens without framework coupling |
| [Workflow Spec](05-workflow-spec.md) | How to define state machines with guards and actions |
| [Glossary](glossary.md) | All UASL terms in one place -- useful to keep open as a reference |

Start with Entity Spec. It is the foundation that every other spec builds on.

---

[← Home](README.md) | [Entity Spec →](02-entity-spec.md)

*UASL v1.0 -- 2026-01-29*
