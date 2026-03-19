# UASL Spec Generation — LLM Training Guide

## Purpose

This document trains an LLM to generate UASL-compliant specifications from natural language user requests. The generation pipeline has two phases:

1. **Entity Inference** — Produce an Entity Spec from natural language (when no entity model is provided)
2. **SUIS Generation** — Produce a Semantic UI Specification from an Entity Spec + user request

The LLM must handle both scenarios:
- **Scenario A**: Entity Spec is provided externally → skip to SUIS generation
- **Scenario B**: No entity model found → infer Entity Spec first, then generate SUIS

---

## Part 1: Entity Spec v1.0 Language Reference

### Overview

The Entity Spec defines the canonical domain model. It describes entities (domain objects), their attributes, relations between entities, computed fields, and display hints. All other UASL specs reference it as the single source of domain truth.

### Document Structure

```yaml
entity_version: "1.0"       # Always "1.0"

entities:
  entity_name:               # snake_case entity name
    label: "Human Name"      # Human-readable singular noun
    primary_key: id          # Must name an attribute below

    meta:                    # Origin tracking (optional)
      source: inferred       # db | inferred | openapi | manual
      confidence: 0.85       # 0-1, required when source is "inferred"

    attributes:              # At least one attribute required
      field_name:
        type: string         # See type table below
        required: true       # Is this field mandatory?
        unique: false        # Must values be unique?
        readonly: false      # Read-only after creation?
        default: "value"     # Default value (or "now()" for timestamps)
        label: "Display"     # Human-readable label
        values: [a, b, c]    # Required when type is "enum"
        constraints:         # Optional validation
          max_length: 200
          min_length: 1
          pattern: "^[A-Z]"
          min: 0
          max: 100
          precision: 10
          scale: 2

    relations:               # Optional
      relation_name:
        type: many_to_one    # See relation types below
        target: other_entity # Must exist in entities
        foreign_key: fk_id   # FK attribute name (many_to_one)
        display_field: name  # Field on target for dropdown display
        nullable: true
        on_delete: set_null  # cascade | restrict | set_null

    computed:                # Optional
      full_name:
        expression: "first_name || ' ' || last_name"
        type: string
        readonly: true

    display:                 # Optional presentation hints
      default_sort: created_at desc
      default_fields: [name, status, created_at]
      search_fields: [name, description]
```

### Attribute Types

| Type | Description | Common Constraints |
|------|-------------|-------------------|
| `string` | Short text (names, codes) | `max_length`, `min_length`, `pattern` |
| `text` | Long text (descriptions, notes) | `max_length` |
| `integer` | Whole number | `min`, `max` |
| `decimal` | Precise number | `min`, `max`, `precision`, `scale` |
| `currency` | Money value (min defaults to 0) | `precision`, `scale` |
| `boolean` | True/false | — |
| `date` | Date only (YYYY-MM-DD) | `min`, `max` |
| `datetime` | Date and time | `min`, `max` |
| `uuid` | UUID v4 identifier | — |
| `enum` | Fixed set of values | `values` (REQUIRED) |

### Relation Types

| Type | Cardinality | Example | Required Fields |
|------|-------------|---------|-----------------|
| `one_to_one` | 1:1 | User → Profile | `target` |
| `many_to_one` | N:1 | Task → User | `target`, `foreign_key` |
| `one_to_many` | 1:N | User → Tasks | `target`, `mapped_by` |
| `many_to_many` | M:N | Task ↔ Tags | `target`, `join_table` |

### What Relations Enable in UI

| Relation | UI Pattern |
|----------|-----------|
| `many_to_one` with `display_field` | Dropdown selector, JOIN display in grid |
| `one_to_many` with `mapped_by` | Master/detail view, child collection |
| `many_to_many` with `join_table` | Multi-select, tag input |

### Validation Rules

Rules use three levels: **MUST** (violation = invalid spec), **SHOULD** (strong recommendation), **MAY** (optional).

**MUST (absolute):**
1. `entity_version` MUST be `"1.0"`
2. Every entity MUST have `primary_key` and `attributes`
3. `primary_key` MUST name an attribute in `attributes`
4. `enum` type MUST have non-empty `values` array
5. `relation.target` MUST name an entity in `entities`
6. `foreign_key` MUST name an attribute in the same entity
7. `many_to_one` MUST have `foreign_key`
8. `one_to_many` MUST have `mapped_by`
9. `many_to_many` MUST have `join_table`

**SHOULD (strong recommendation):**
10. Entity names SHOULD use `snake_case`
11. Every entity SHOULD have `label` for human readability
12. Inferred entities SHOULD include `meta.source` and `meta.confidence`
13. `many_to_one` relations SHOULD have `display_field` for UI rendering

**MAY (optional):**
14. Entities MAY include `display` hints for default presentation
15. Entities MAY include `computed` fields for derived values

---

## Part 2: SUIS v1.1 Language Reference

### Overview

SUIS (Semantic UI Specification) is an intent-driven, framework-agnostic UI description. It describes WHAT users intend to do — not HOW the UI is built. No grids, no datasources, no click handlers, no pixel positions, no CSS.

### Document Structure

```yaml
ui:
  suis_version: "1.1"       # Always "1.1"

  screens:
    screen_id:               # snake_case screen identifier
      subject:               # What entity and purpose
        domain: entity_name  # Must exist in Entity Spec
        purpose: browse      # browse | view | create | edit | dashboard | wizard
        title: "Screen Title"
        description: "Optional description"

      display:
        primary:             # Main content area (required)
          type: collection   # collection | single | summary
          fields:
            - name: field_name    # Must exist on entity
              label: "Label"
              format: text        # text|integer|decimal|currency|date|datetime|enum|boolean
              sortable: true
              width_hint: medium  # narrow | medium | wide | fill
              align_hint: start   # start | center | end
              editable: false
              required: true

        secondary:           # Optional additional areas
          - type: summary
            fields: [...]

        filters:             # Optional, for browse screens
          - field: status
            operator: eq     # eq|ne|gt|lt|gte|lte|range|contains|in
            input: dropdown  # text|number|date|date_range|dropdown|multi_select
            options: [...]

      operations:            # What actions are available
        - intent: search
        - intent: create
          opens: target_screen
        - intent: edit
          trigger: activate_item
          opens: target_screen
        - intent: delete
          trigger: bulk_selection
          confirmation: "Delete selected items?"
        - intent: submit
          success_feedback: "Saved successfully"
          post_action: close    # refresh | close | navigate

      navigation:            # Optional screen links
        to_editor:
          target: screen_id
          mode: modal        # modal | full

      permissions:
        roles: [admin, manager, user]
```

### Screen Purpose Types

| Purpose | Use When |
|---------|----------|
| `browse` | List/search with multiple records (main entry screens) |
| `view` | Read-only detail of a single record |
| `create` | New record form |
| `edit` | Edit form for existing record |
| `dashboard` | Aggregated summary with KPIs |
| `wizard` | Multi-step guided process |

### Display Block Types

| Type | Use When |
|------|----------|
| `collection` | Showing multiple records (grid/list) |
| `single` | Showing one record (form/detail) |
| `summary` | Aggregated data (counts, KPIs) |

### Operation Intents

| Intent | Description |
|--------|-------------|
| `browse` | View list of records |
| `view` | View single record detail |
| `search` | Filter/search records |
| `create` | Create new record |
| `edit` | Edit existing record |
| `delete` | Delete record(s) — MUST have `confirmation` |
| `submit` | Submit form data |
| `approve` / `reject` | Workflow transitions |
| `export` / `import` | Data import/export |
| `custom` | Custom operation |

### Semantic Triggers (NOT DOM events)

| Trigger | Meaning |
|---------|---------|
| `select_item` | User selects a row/item |
| `activate_item` | User wants to interact with an item (open/edit) |
| `bulk_selection` | User selects multiple items |
| `confirm_action` | User explicitly confirms |
| `value_change` | Reactive form change |
| `automatic` | On load / timer |

### Width Hints

| Hint | Use For |
|------|---------|
| `narrow` | IDs, status badges, booleans |
| `medium` | Names, dates, standard fields |
| `wide` | Titles, descriptions, long text |
| `fill` | Expand to fill remaining space |

### Align Hints

| Hint | Use For |
|------|---------|
| `start` | Text fields (default) |
| `center` | Status, boolean, enum |
| `end` | Numbers, currency, dates |

### SUIS Validation Rules

Rules use three levels: **MUST** (violation = invalid spec), **SHOULD** (strong recommendation, break only with good reason), **MAY** (optional, at LLM's discretion).

**MUST (absolute — violation makes the spec invalid):**
1. `suis_version` MUST be `"1.1"`
2. Every screen MUST have `subject`, `display`, and `operations`
3. `subject.domain` MUST reference an entity in the Entity Spec
4. `display.primary` MUST exist with `type` and at least one field
5. `fields[].name` in `collection` and `single` blocks MUST reference entity attributes, relation names, or computed field names
6. `delete` intent MUST have `confirmation`
7. `opens` and `navigation.target` MUST reference existing screen IDs
8. NEVER include framework-specific concepts (grids, datasources, click handlers, CSS, pixel values)

**SHOULD (strong recommendation — break only with clear justification):**
9. `edit`/`view` operations with `opens` SHOULD have a `trigger`
10. `browse` screens SHOULD include a `search` operation
11. `edit`/`create` screens SHOULD include a `submit` operation with `success_feedback`
12. Fields SHOULD have `width_hint` and `align_hint` for consistent adapter output

**MAY (optional — use when appropriate):**
13. `summary` display blocks MAY contain derived field names (e.g., `total_count`, `pending_amount`) that do not exist on the entity, since summaries represent aggregated metrics
14. Screens MAY include `permissions` for role-based access
15. `browse` screens MAY include `export` operation

---

## Part 3: Entity Spec → SUIS Field Mapping

When generating SUIS from an Entity Spec, map entity attributes to SUIS field properties:

| Entity Attribute Type | SUIS Format | Default Width Hint | Default Align Hint |
|-----------------------|-------------|--------------------|--------------------|
| `string` | `text` | `medium` | `start` |
| `text` | `text` | `wide` | `start` |
| `integer` | `integer` | `narrow` | `end` |
| `decimal` | `decimal` | `medium` | `end` |
| `currency` | `currency` | `medium` | `end` |
| `boolean` | `boolean` | `narrow` | `center` |
| `date` | `date` | `medium` | `center` |
| `datetime` | `datetime` | `medium` | `center` |
| `uuid` (primary key) | `text` | `narrow` | `end` |
| `enum` | `enum` | `narrow` | `center` |

Relations in SUIS:
- `many_to_one` relations appear as fields using the relation name (e.g., `assignee`), format `text`, with `display_field` providing the label value
- `one_to_many` relations may become secondary collection displays in detail/edit screens
- `many_to_many` relations may become multi-select fields in edit screens

---

## Part 4: Prompt — Entity Spec Generation from Natural Language

Use this prompt when no entity model is found and you need to infer one from the user's natural language request.

### System Prompt

```
You are an Entity Spec generator. Given a user's natural language description of an application or screen, you produce a valid Entity Spec v1.0 YAML document.

## Rules

1. Output ONLY valid Entity Spec v1.0 YAML. No explanation, no markdown fences.
2. entity_version MUST be "1.0".
3. Every entity MUST have primary_key and attributes.
4. Use snake_case for all entity names, attribute names, and relation names.
5. Always include an `id` attribute as primary key unless the user specifies otherwise. Choose the ID type based on context:
   - Use `integer` when: user mentions auto-increment, sequence, legacy system, or the domain is traditional RDBMS/JPA-based
   - Use `uuid` when: user mentions distributed systems, microservices, or does not specify a preference
   - If the user explicitly states an ID type, use that type
6. Always include `created_at` (datetime, readonly, default: now()) and `updated_at` (datetime, readonly, default: now()) on every entity.
7. Infer entity types from context. The following are common examples — infer unlisted terms using the same snake_case English convention:
   - "회원", "사용자", "user" → user entity
   - "주문", "order" → order entity
   - "상품", "product" → product entity
   - "부서", "department" → department entity
8. Infer relations from context:
   - "belonging to", "소속" → many_to_one
   - "has many", "목록" → one_to_many
   - "tagged with", "분류" → many_to_many
9. For enum attributes, infer reasonable values from context. If the user mentions statuses like "진행중", "완료", translate to English snake_case: pending, in_progress, completed.
10. Include display hints based on the entity's role:
    - List screens → default_fields with the most identifying fields
    - Search → search_fields with text-searchable fields
11. Mark all entities with meta.source: inferred and meta.confidence between 0.7-0.95.
12. Prefer FEWER entities with CORRECT relations over many disconnected entities.
13. If uncertain about an attribute or relation, OMIT it. Silence is preferred over hallucination.
14. foreign_key attributes MUST be explicitly declared in attributes when used in many_to_one relations.
15. When the foreign_key attribute type differs from the target entity's primary key type (e.g., integer FK referencing a uuid PK), match the target's primary key type.
```

### User Prompt Template

```
Generate an Entity Spec for the following application:

{user_request}

Requirements:
- Include all entities mentioned or implied
- Define relations between entities
- Add reasonable attributes based on the domain
- Include display hints for default list views
```

### Example Input/Output

**Input:**
```
사원 관리 시스템. 사원은 이름, 이메일, 입사일, 직급이 있고 부서에 소속된다. 부서는 이름과 코드가 있다.
```

**Output:**
```yaml
entity_version: "1.0"

entities:
  employee:
    label: Employee
    primary_key: id
    meta:
      source: inferred
      confidence: 0.90

    attributes:
      id:
        type: uuid
        required: true
      name:
        type: string
        required: true
        label: "Name"
        constraints:
          max_length: 100
      email:
        type: string
        required: true
        unique: true
        label: "Email"
        constraints:
          max_length: 200
      hire_date:
        type: date
        required: true
        label: "Hire Date"
      position:
        type: enum
        required: true
        label: "Position"
        values: [staff, senior, manager, director, executive]
      department_id:
        type: uuid
        label: "Department"
      created_at:
        type: datetime
        required: true
        readonly: true
        default: "now()"
      updated_at:
        type: datetime
        required: true
        readonly: true
        default: "now()"

    relations:
      department:
        type: many_to_one
        target: department
        foreign_key: department_id
        display_field: name
        nullable: false
        on_delete: restrict

    display:
      default_sort: name asc
      default_fields: [name, email, position, department, hire_date]
      search_fields: [name, email]

  department:
    label: Department
    primary_key: id
    meta:
      source: inferred
      confidence: 0.92

    attributes:
      id:
        type: uuid
        required: true
      name:
        type: string
        required: true
        label: "Name"
        constraints:
          max_length: 100
      code:
        type: string
        required: true
        unique: true
        label: "Code"
        constraints:
          max_length: 20
      created_at:
        type: datetime
        required: true
        readonly: true
        default: "now()"
      updated_at:
        type: datetime
        required: true
        readonly: true
        default: "now()"

    relations:
      employees:
        type: one_to_many
        target: employee
        mapped_by: department

    display:
      default_sort: name asc
      default_fields: [code, name]
      search_fields: [name, code]
```

---

## Part 5: Prompt — SUIS Generation from Entity Spec

Use this prompt when an Entity Spec is available and you need to generate SUIS screens.

### System Prompt

```
You are a SUIS (Semantic UI Specification) generator. Given an Entity Spec v1.0 and a user's natural language description, you produce a valid SUIS v1.1 YAML document.

## Rules

1. Output ONLY valid SUIS v1.1 YAML. No explanation, no markdown fences.
2. suis_version MUST be "1.1".
3. NEVER include framework-specific concepts:
   - No grids, datasources, click handlers
   - No pixel positions, CSS, widget names
   - No DOM events (onclick, onchange)
   - No API URLs or endpoints
4. Use semantic triggers (activate_item, select_item) NOT DOM events.
5. Use semantic hints (width_hint, align_hint) NOT pixel values.
6. subject.domain MUST reference an entity from the provided Entity Spec.
7. Field name binding:
   - In `collection` and `single` blocks: field names MUST reference entity attributes, relation names, or computed field names from the Entity Spec.
   - In `summary` blocks: field names MAY be derived metric names (e.g., `total_count`, `pending_amount`) that do not exist on the entity.
8. delete intent MUST always have a confirmation message.
9. edit/view operations that navigate SHOULD have trigger: activate_item.
10. Generate appropriate screens based on purpose:
    - browse screens: collection display, filters, search/create/edit/delete operations
    - edit/create screens: single display with editable fields, submit operation
    - view screens: single display with readonly fields
    - dashboard screens: summary + collection displays
11. Filter selection:
    - enum attributes → dropdown filter with operator: eq
    - date/datetime → date_range filter with operator: range
    - string attributes → text filter with operator: contains
    - integer/decimal → number filter with operator ranges
12. Field visibility:
    - Primary keys: include but width_hint: narrow
    - Timestamps (created_at, updated_at): include in detail, omit from browse unless relevant
    - Foreign keys (department_id): OMIT from display — use the relation name instead (department)
13. Operation patterns by purpose:
    - browse: search, create, edit (activate_item), delete (bulk_selection), optionally export
    - edit: submit (with success_feedback and post_action: close), browse (back navigation)
    - create: submit (with success_feedback and post_action: close), browse (back navigation)
    - view: edit, browse (back navigation)
14. Navigation:
    - browse → edit/create: mode: modal (for simple forms) or mode: full (for complex forms)
    - edit/create → browse: via operation with intent: browse
15. Screen ID naming convention: {entity}_{purpose} (e.g., task_browse, task_edit)
```

### User Prompt Template

```
Generate SUIS screens for the following request.

## Entity Spec
{entity_spec_yaml}

## User Request
{user_request}

Requirements:
- Generate all screens needed to fulfill the user's request
- Include appropriate filters for browse screens
- Include proper navigation between screens
- Map entity fields to appropriate SUIS field properties
```

### Example Input/Output

**Input Entity Spec:**
```yaml
entity_version: "1.0"

entities:
  employee:
    label: Employee
    primary_key: id
    attributes:
      id:
        type: uuid
        required: true
      name:
        type: string
        required: true
        constraints:
          max_length: 100
      email:
        type: string
        required: true
        unique: true
      hire_date:
        type: date
        required: true
      position:
        type: enum
        required: true
        values: [staff, senior, manager, director, executive]
      department_id:
        type: uuid
    relations:
      department:
        type: many_to_one
        target: department
        foreign_key: department_id
        display_field: name
    display:
      default_sort: name asc
      default_fields: [name, email, position, department, hire_date]
      search_fields: [name, email]

  department:
    label: Department
    primary_key: id
    attributes:
      id:
        type: uuid
        required: true
      name:
        type: string
        required: true
      code:
        type: string
        required: true
        unique: true
    relations:
      employees:
        type: one_to_many
        target: employee
        mapped_by: department
    display:
      default_sort: name asc
      default_fields: [code, name]
```

**Input Request:**
```
사원 목록 화면과 사원 편집 화면을 만들어줘. 부서별, 직급별 필터가 필요해.
```

**Output:**
```yaml
ui:
  suis_version: "1.1"

  screens:
    employee_browse:
      subject:
        domain: employee
        purpose: browse
        title: "Employee Management"
        description: "View and manage employee records"

      display:
        primary:
          type: collection
          fields:
            - name: id
              label: "ID"
              format: text
              width_hint: narrow
              align_hint: end
              sortable: true
            - name: name
              label: "Name"
              format: text
              width_hint: medium
              sortable: true
            - name: email
              label: "Email"
              format: text
              width_hint: wide
            - name: position
              label: "Position"
              format: enum
              width_hint: narrow
              align_hint: center
              sortable: true
            - name: department
              label: "Department"
              format: text
              width_hint: medium
            - name: hire_date
              label: "Hire Date"
              format: date
              width_hint: medium
              align_hint: center
              sortable: true

        filters:
          - field: department
            operator: eq
            input: dropdown
          - field: position
            operator: eq
            input: dropdown
            options: ["staff", "senior", "manager", "director", "executive"]
          - field: name
            operator: contains
            input: text

      operations:
        - intent: search
        - intent: create
          opens: employee_edit
        - intent: edit
          trigger: activate_item
          opens: employee_edit
        - intent: delete
          trigger: bulk_selection
          confirmation: "Delete selected employees?"
        - intent: export

      navigation:
        to_editor:
          target: employee_edit
          mode: modal

      permissions:
        roles: [admin, manager]

    employee_edit:
      subject:
        domain: employee
        purpose: edit
        title: "Employee Editor"

      display:
        primary:
          type: single
          fields:
            - name: name
              label: "Name"
              format: text
              required: true
            - name: email
              label: "Email"
              format: text
              required: true
            - name: position
              label: "Position"
              format: enum
              required: true
            - name: department
              label: "Department"
              format: text
              required: true
            - name: hire_date
              label: "Hire Date"
              format: date
              required: true

      operations:
        - intent: submit
          success_feedback: "Employee saved successfully"
          post_action: close
        - intent: browse
          opens: employee_browse

      permissions:
        roles: [admin, manager]
```

---

## Part 6: Two-Phase Pipeline

When processing a user request end-to-end:

### Phase 1: Entity Resolution

```
IF entity_spec is provided externally:
    Use it directly → go to Phase 2
ELSE:
    Run Entity Spec generation prompt (Part 4)
    Mark all entities with meta.source: inferred
    → go to Phase 2
```

### Phase 2: SUIS Generation

```
Take the Entity Spec (provided or inferred) + user request
Run SUIS generation prompt (Part 5)
Validate output:
  - All subject.domain references exist in Entity Spec
  - All field names exist as entity attributes or relations
  - All cross-screen references (opens, navigation.target) are valid
  - delete intents have confirmation
```

### Combined Prompt (Both Phases)

When no entity spec is available and you need to do both phases in a single pass:

```
You are a UASL specification generator. Given a user's natural language request, you produce two YAML documents:

1. An Entity Spec v1.0 defining the domain model
2. A SUIS v1.1 defining the UI screens

## Output Format

Output two YAML documents separated by a line containing only "---":

[Entity Spec v1.0 YAML]
---
[SUIS v1.1 YAML]

## Entity Spec Rules
[Include all rules from Part 4 system prompt]

## SUIS Rules
[Include all rules from Part 5 system prompt]

## Cross-Spec Consistency Rules
1. Every subject.domain in SUIS MUST reference an entity in the Entity Spec.
2. Field names in `collection` and `single` blocks MUST reference entity attributes, relations, or computed fields. Field names in `summary` blocks MAY be derived metrics.
3. Filter fields MUST reference entity attributes.
4. Enum filter options MUST match entity enum values.
5. Relation fields in SUIS use the relation name, not the foreign key attribute name.

## Failure Rules
1. If the request is too vague to identify entities, output an empty Entity Spec and signal clarification needed. Do NOT hallucinate entities.
2. If the request is outside CRUD scope, signal out-of-scope. Do NOT force-fit into UASL.
3. If entity inference confidence is below 0.6 for all entities, output the draft Entity Spec only. Do NOT proceed to SUIS generation.
4. Silence is always preferred over hallucination.
```

---

## Part 7: Failure Strategies

When the LLM cannot produce a valid spec, it must fail gracefully rather than hallucinate. These rules define behavior for edge cases.

### 7.1 Ambiguous or Insufficient Input

When the user request is too vague to infer a domain model (e.g., "make a management screen"):

```
IF request lacks identifiable entities or domain nouns:
    Output an empty Entity Spec stub:
      entity_version: "1.0"
      entities: {}
    AND return a clarification signal (not a hallucinated spec)
```

The LLM MUST NOT invent entities from generic words like "management", "system", or "data".

### 7.2 Non-CRUD Requests

When the request cannot be mapped to a CRUD-oriented domain model (e.g., "generate a chart", "build a login page"):

- If the request is for a non-entity UI (login, settings, static pages): output SUIS with `purpose: custom` and minimal operations. Do not force entity binding.
- If the request is outside UASL scope entirely (e.g., "write a REST API", "create a batch job"): output nothing and signal that the request is out of scope.

### 7.3 Partial Information

When some entities are clear but others are ambiguous:

- Generate specs for the clear entities only
- Mark ambiguous parts with lower `meta.confidence` (0.5-0.7)
- Do NOT fill gaps with generic placeholder entities

### 7.4 Conflicting Requirements

When the user's request contains contradictions (e.g., "read-only edit form"):

- Prefer the more specific instruction over the general one
- If truly irreconcilable, generate the spec for the dominant intent and omit the conflicting part
- Do NOT attempt to satisfy both contradictory requirements simultaneously

### 7.5 Entity Inference Failure

When Phase 1 (entity inference) produces low-confidence results:

```
IF all entities have confidence < 0.6:
    Output the draft Entity Spec as-is (do NOT proceed to SUIS generation)
    Signal that user confirmation is needed before proceeding
ELSE:
    Proceed to Phase 2 with available entities
    Exclude entities with confidence < 0.5 from SUIS generation
```

---

## Appendix A: Common Patterns

### A.1 Browse + Edit (Most Common)

```
Entity: order
Screens: order_browse (collection) + order_edit (single)
Pattern: browse has search/create/edit/delete → edit has submit/back
Navigation: browse → edit via modal or full
```

### A.2 Master/Detail

```
Entity: department (master) → employee (detail)
Screens: department_browse + department_view (with embedded employee collection)
Pattern: department_view has primary: single (department fields) + secondary: collection (employee fields)
```

### A.3 Dashboard

```
Entity: order
Screen: order_dashboard
Pattern: primary: summary (KPIs) + secondary: collection (recent orders)
Operations: search, export, navigate to browse
```

### A.4 Wizard (Multi-Step)

```
Entity: application
Screen: application_wizard
Pattern: purpose: wizard with multiple display sections representing steps
Operations: submit at final step, navigate back to previous screens
```

### A.5 Read-Only View

```
Entity: audit_log
Screen: audit_browse
Pattern: collection display with filters, NO create/edit/delete operations
Operations: search, export only
```

---

## Appendix B: Korean Business Domain Vocabulary (Examples)

The table below shows **representative examples** of how common Korean business terms map to entity/attribute names. This is not an exhaustive dictionary — for terms not listed here, infer the English snake_case equivalent using the same naming convention.

| Korean | Entity/Attribute | Type |
|--------|-----------------|------|
| 사원, 직원 | employee | entity |
| 부서 | department | entity |
| 직급 | position | enum |
| 입사일 | hire_date | date |
| 회원 | member / user | entity |
| 주문 | order | entity |
| 상품 | product | entity |
| 금액, 가격 | price / amount | currency |
| 수량 | quantity | integer |
| 상태 | status | enum |
| 분류, 카테고리 | category | entity or enum |
| 등록일 | created_at | datetime |
| 수정일 | updated_at | datetime |
| 목록 | browse screen | purpose |
| 등록/편집 | create/edit screen | purpose |
| 상세 | view screen | purpose |
| 대시보드 | dashboard screen | purpose |
| 검색 | search operation | intent |
| 삭제 | delete operation | intent |
| 저장 | submit operation | intent |
| 승인 | approve operation | intent |
| 반려 | reject operation | intent |

> **Note**: Domain-specific terms (e.g., 결재선 → approval_line, 품의서 → expenditure_request) should be inferred from context. Consistency within a single project is more important than matching this table.

---

*Document Version: 1.1*
*Last Updated: 2026-02-04*
