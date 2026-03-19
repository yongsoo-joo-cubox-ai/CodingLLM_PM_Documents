[Home](README.md) | [Overview](01-overview.md) | [Entity](02-entity-spec.md) | [IAS](03-ias-spec.md) | [SUIS](04-suis-spec.md) | [Workflow](05-workflow-spec.md)

---

# Glossary

This glossary defines every key term used across the UASL specification family. Terms are listed alphabetically, and each entry links to the spec where it is primarily defined.

---

### Action

A side effect executed on state entry, exit, or transition in a workflow. Actions describe what the system should do when a state change occurs, such as sending a notification, dispatching an email, or setting a field value. Actions are declarative — the spec names the effect, and the adapter decides how to implement it. See [Workflow Spec](05-workflow-spec.md).

### Adapter

A framework-specific compiler module that transforms the UASL intermediate representation into platform code. Each adapter targets a single technology stack (e.g., xframe5 adapter, Vue adapter, Spring Boot adapter). Adapters are the only place where framework-specific knowledge exists; the specs themselves remain platform-neutral. See [Overview](01-overview.md).

### Attribute

A named, typed field belonging to an entity. Every attribute has at minimum a `name` and a `type` (e.g., `title: string`, `amount: decimal`). Attributes may carry constraints, display hints, and meta information. They form the atomic data elements from which all other specs derive their field references. See [Entity Spec](02-entity-spec.md).

### Canonical

The authoritative, validated form of a spec, as opposed to a draft or inferred version. A canonical spec has passed all conformance checks for its declared conformance level and is considered the single source of truth. LLM-inferred specs are explicitly non-canonical until validated. See [Entity Spec](02-entity-spec.md).

### Collection

A display block type that presents multiple records, typically rendered as a grid or list. In SUIS, a collection block defines which fields to show per row and how records are laid out. The term also appears in IAS as a return type indicating that an intent responds with an array of items rather than a single object. See [SUIS Spec](04-suis-spec.md).

### Compiler

The toolchain that validates UASL specs against their JSON Schemas, checks cross-spec consistency, and transforms the validated specs into target artifacts through an adapter. A conforming compiler must implement fail-fast validation and must not silently coerce invalid input. See [Overview](01-overview.md).

### Component

A reusable display block that can be shared across multiple SUIS screens. Components allow common UI patterns (e.g., a status badge, an address card) to be defined once and referenced by name, reducing duplication and ensuring visual consistency. See [SUIS Spec](04-suis-spec.md).

### Computed Field

A derived field whose value is defined by an expression over other attributes rather than stored directly. Computed fields are always readonly — they cannot be assigned by users or API calls. The expression language is intentionally simple to remain framework-neutral. See [Entity Spec](02-entity-spec.md).

### Conformance Level

A progressive tier of validation depth applied to UASL specs. Level 1 (Structural) checks that the document matches the JSON Schema. Level 2 (Semantic) validates cross-references and type consistency. Level 3 (Complete) ensures full inter-spec coherence. Every conforming compiler must declare which level it supports. See [Overview](01-overview.md).

### Constraint

A validation rule applied to an entity attribute that restricts its acceptable values. Common constraints include `max_length`, `min`, `max`, `pattern` (regex), and `required`. Constraints are declared at the entity level and propagated to both UI validation and API validation by the compiler. See [Entity Spec](02-entity-spec.md).

### Display Block

A SUIS structure that defines how visible data is arranged on a screen. The three block types are `collection` (multiple records), `single` (one record), and `summary` (aggregated overview). Each block references entity fields and may include layout hints. See [SUIS Spec](04-suis-spec.md).

### Display Hint

A semantic suggestion attached to an entity attribute that guides default presentation without prescribing exact rendering. Examples include `default_sort` (which field to sort by), `default_fields` (which fields to show first), and format hints. Adapters may honor or override display hints. See [Entity Spec](02-entity-spec.md).

### Domain

The subject area an entity belongs to, representing a bounded context in the application. In SUIS, the domain is expressed through `subject.domain` and determines which entity a screen operates on. Domains help organize large applications into coherent groups. See [SUIS Spec](04-suis-spec.md).

### Entity

A domain object that models a real-world concept with attributes and relations. Entities are the foundation of UASL — every other spec references entities. Examples include Task, User, Order, and Product. Each entity has a primary key, zero or more attributes, and optional relations to other entities. See [Entity Spec](02-entity-spec.md).

### Event

A named action that triggers a workflow transition from one state to another. Events represent meaningful business occurrences such as `submit`, `approve`, or `reject`. An event fires on exactly one transition and may be subject to guards and permissions. See [Workflow Spec](05-workflow-spec.md).

### Fail-fast

The validation strategy mandated by UASL: reject invalid specs immediately with a clear error message rather than attempting to coerce, guess, or silently fix malformed input. This principle ensures that errors are caught at spec time, not at code generation time. See [Overview](01-overview.md).

### Field

In SUIS, a reference to an entity attribute within a display block or filter. A field reference may include optional presentation hints such as `format`, `width`, and `alignment` that inform the adapter how to render the data. Fields always trace back to an attribute defined in the Entity Spec. See [SUIS Spec](04-suis-spec.md).

### Field Map

An IAS mapping between spec-level naming conventions (snake_case) and backend API naming conventions (camelCase or other). Field maps allow the spec to use a consistent naming style while the generated API conforms to the target platform's idiomatic conventions. See [IAS Spec](03-ias-spec.md).

### Filter

A SUIS search criterion that binds an entity field to an operator (equals, contains, between, etc.) and an input type (text, select, date picker, etc.). Filters define how users can narrow down collection results. The adapter translates filters into platform-specific query mechanisms. See [SUIS Spec](04-suis-spec.md).

### Final State

A terminal state in a workflow from which no outgoing transitions exist. Every workflow must declare at least one final state. When an entity reaches a final state, the workflow is considered complete. Examples include `closed`, `approved`, or `archived`. See [Workflow Spec](05-workflow-spec.md).

### Foreign Key

An attribute that references another entity's primary key, establishing a link between the two entities. Foreign keys are the concrete mechanism underlying relations. The Entity Spec declares the foreign key attribute; the compiler generates the appropriate join or reference code. See [Entity Spec](02-entity-spec.md).

### Guard

A boolean condition that must evaluate to true for a workflow transition to fire. Guards prevent invalid state changes — for example, requiring that a document has at least one approver before the `approve` event can proceed. Guards are evaluated at runtime. See [Workflow Spec](05-workflow-spec.md).

### Initial State

The starting state of a workflow, assigned to new entity instances when they first enter the workflow. Every workflow must declare exactly one initial state. Examples include `draft`, `new`, or `pending`. See [Workflow Spec](05-workflow-spec.md).

### Intent

A semantic operation the user wants to perform, abstracted away from HTTP methods or UI events. Intents such as `search`, `create`, `update`, `delete`, and `approve` describe what the user means to do. In SUIS, intents drive operations; in IAS, intents map to HTTP endpoints. See [SUIS Spec](04-suis-spec.md) and [IAS Spec](03-ias-spec.md).

### Meta

Metadata that tracks the origin and reliability of an entity definition. Meta fields record the source of the definition (e.g., `ddl`, `manual`, `llm_inferred`) and a confidence score. This allows compilers and reviewers to distinguish authoritative definitions from inferred ones. See [Entity Spec](02-entity-spec.md).

### Navigation

SUIS screen-to-screen links that describe how a user moves between views. Each navigation entry specifies a `target` screen and a `mode` (modal or full page). Navigation is declarative — the adapter decides whether to use routes, dialogs, or tabs. See [SUIS Spec](04-suis-spec.md).

### Operation

A SUIS user action defined by an intent, a trigger, and optional navigation. Operations describe what the user can do on a screen — for example, clicking a row to view details, pressing a button to create a new record, or selecting items for bulk deletion. See [SUIS Spec](04-suis-spec.md).

### Parameter Source

The location from which an IAS intent obtains its input data. The four parameter sources are `filters` (from search criteria), `form` (from input fields), `selection[]` (from selected records), and `context` (from ambient application state such as the current user). See [IAS Spec](03-ias-spec.md).

### Path Suffix

An additional path segment appended to an IAS resource's base path to form the complete endpoint URL. Path suffixes such as `/{id}`, `/bulk-delete`, or `/export` distinguish operations on the same resource. The compiler concatenates the base path and suffix to produce the final route. See [IAS Spec](03-ias-spec.md).

### Permissions

Role-based access declarations that control who can see a SUIS screen or trigger a workflow transition. Permissions are declared as role lists (e.g., `[admin, manager]`) and are enforced by the generated code. A screen or transition with no permissions declared is accessible to all authenticated users. See [SUIS Spec](04-suis-spec.md) and [Workflow Spec](05-workflow-spec.md).

### Primary Key

The attribute that uniquely identifies each instance of an entity. Every entity must declare exactly one primary key. The primary key is referenced by foreign keys in related entities and is used by IAS for single-record operations. See [Entity Spec](02-entity-spec.md).

### Purpose

A SUIS screen's declared role, indicating the kind of user task it supports. The defined purposes are `browse` (list/search), `view` (read-only detail), `create` (new record), `edit` (modify record), `dashboard` (aggregated overview), and `wizard` (multi-step flow). Purpose guides the compiler's code generation strategy. See [SUIS Spec](04-suis-spec.md).

### Relation

A typed link between two entities that describes how they are connected. The four relation types are `one_to_one`, `many_to_one`, `one_to_many`, and `many_to_many`. Relations are declared in the Entity Spec and referenced by SUIS for navigation and by IAS for nested resource endpoints. See [Entity Spec](02-entity-spec.md).

### Resource

An IAS API endpoint group bound to a single entity. A resource defines a base path and a set of intents that operate on that entity. For example, a `tasks` resource at `/api/tasks` might expose `search`, `create`, `update`, and `delete` intents. See [IAS Spec](03-ias-spec.md).

### Return Type

What an IAS intent returns after execution. The three return types are `collection` (an array of records), `single` (one record), and `none` (no body, typically for delete operations). The return type informs the compiler how to shape the response handler. See [IAS Spec](03-ias-spec.md).

### Screen

The fundamental unit of SUIS, describing a user-facing view. A screen combines a subject (what entity and purpose), display blocks (what data to show), and operations (what the user can do). Screens are the starting point for UI code generation. See [SUIS Spec](04-suis-spec.md).

### State

A named position in a workflow state machine, representing a stage in an entity's lifecycle. States are connected by transitions. Each state may declare entry/exit actions and permissions. Common states include `draft`, `in_review`, `approved`, and `closed`. See [Workflow Spec](05-workflow-spec.md).

### Status Field

The entity attribute, always of enum type, that holds the current workflow state value. The status field is the bridge between the Entity Spec (which defines the attribute) and the Workflow Spec (which defines the state machine). The compiler ensures the enum values match the declared workflow states. See [Workflow Spec](05-workflow-spec.md).

### Subject

The semantic anchor of a SUIS screen, declaring which entity domain the screen operates on and what its purpose is. The subject connects a screen to the Entity Spec (via domain) and determines the screen's behavioral category (via purpose). See [SUIS Spec](04-suis-spec.md).

### Transition

A directed edge between two workflow states, triggered by an event. Transitions define the legal paths through a workflow. Each transition specifies a `from` state, a `to` state, the triggering event, and optional guards, actions, and permissions. See [Workflow Spec](05-workflow-spec.md).

### Trigger

A semantic user interaction that initiates an operation in SUIS. Triggers describe what the user does conceptually (e.g., `activate_item`, `bulk_selection`, `toolbar_button`) rather than mapping to specific DOM events. The adapter translates triggers into concrete UI interactions. See [SUIS Spec](04-suis-spec.md).

### UASL

Universal Application Specification Language. The umbrella name for the four-spec family — Entity Spec, IAS, SUIS, and Workflow Spec — that together describe a complete application at the semantic level. UASL is framework-agnostic, language-agnostic, and runtime-agnostic by design. See [Overview](01-overview.md).

---

*UASL v1.0 — 2026-01-29*

---

[Home](README.md) | [Overview](01-overview.md) | [Entity](02-entity-spec.md) | [IAS](03-ias-spec.md) | [SUIS](04-suis-spec.md) | [Workflow](05-workflow-spec.md)
