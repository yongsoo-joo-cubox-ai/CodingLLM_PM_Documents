[Home](README.md) | [<- Overview](01-overview.md) | [Next: IAS ->](03-ias-spec.md)

---

# Entity Spec -- Domain Model

The Entity Spec defines the domain model: entities, their attributes, how they relate to each other. It is the foundation of UASL -- every other spec references it. Think of it as your application's data dictionary in a machine-readable format.

SUIS needs to know what fields exist on a `task`. IAS needs to know which entity a resource maps to. Workflow needs to know which enum field drives the state machine. They all look it up in the Entity Spec. Write this one first, and the rest falls into place.

---

## Document Structure

An Entity Spec is a YAML document with two required top-level keys:

```yaml
entity_version: "1.0"

entities:
  task:
    # ...
  user:
    # ...
```

`entity_version` tells tooling which version of the spec you are writing against. Right now, the only valid value is `"1.0"`.

`entities` is a map where each key is an entity name (use `snake_case`) and the value describes that entity. You need at least one entity, but most real specs have several.

---

## Entities

Each entity represents a domain object -- Task, User, Order, Department, whatever your application works with.

Every entity needs two things: a `primary_key` and `attributes`. Everything else is optional.

```yaml
entities:
  task:
    label: Task                   # optional, human-readable name
    primary_key: id               # required, must match an attribute name
    meta: { ... }                 # optional, origin tracking
    attributes: { ... }          # required, at least one
    relations: { ... }           # optional
    computed: { ... }            # optional
    display: { ... }            # optional, presentation hints
```

The `primary_key` value must name one of the attributes you define. If your entity has `id` as its primary key, you need an attribute called `id` in the `attributes` block.

The primary key attribute is typically `uuid` or `integer`. Use `uuid` for distributed systems, microservices, or when no specific type is required. Use `integer` for legacy databases, JPA/Hibernate auto-increment patterns, or when the user explicitly requests sequential IDs. Both are valid -- the choice depends on application context. Foreign key attributes that reference a primary key should match the target entity's primary key type.

The `label` is a human-friendly name that tooling can use in generated UIs, error messages, and documentation. If you omit it, tools will typically derive one from the entity name.

---

## Attributes

Every attribute needs a `type`. That is the only required field. Everything else -- `required`, `unique`, `default`, `label`, `constraints` -- is optional and depends on what you need to express.

```yaml
attributes:
  title:
    type: string
    required: true
    label: "Title"
    constraints:
      max_length: 200
```

### Available Types

| Type | What it is | Useful constraints |
|------|-----------|-------------------|
| `string` | Short text (names, titles, codes) | `max_length`, `min_length`, `pattern` |
| `text` | Long text (descriptions, notes, content) | `max_length` |
| `integer` | Whole numbers (counts, quantities) | `min`, `max` |
| `decimal` | Precise numbers (measurements, rates) | `precision`, `scale` |
| `currency` | Money values (prices, totals, balances) | `precision`, `scale` |
| `boolean` | True or false | -- |
| `date` | Date only, no time component | -- |
| `datetime` | Date and time together | -- |
| `uuid` | UUID identifier | -- |
| `enum` | One value from a fixed set | `values` (required) |

The difference between `string` and `text` is semantic: `string` is for short values like a person's name, `text` is for potentially long content like a description or comment body. Tooling uses this to pick appropriate input widgets (text field vs. textarea).

`currency` is a specialized `decimal` -- they work the same way technically, but declaring something as `currency` tells downstream specs that this field represents money.

For `enum`, you must provide a `values` list:

```yaml
status:
  type: enum
  values: [draft, pending, approved, rejected]
  default: draft
```

### Values on Non-Enum Types

You can also use `values` on `string` or `integer` attributes. This does not change the storage type -- the field is still stored as a string or integer in the database -- but it tells code generators to render a dropdown/select control instead of a free-text input.

```yaml
priority:
  type: string
  values: [low, medium, high, critical]
  default: medium
```

This is useful when you have a field that is stored as a plain string but only accepts a fixed set of values. The difference from `enum` is semantic: `enum` declares a type-level constraint, while `string` with `values` is a UI-level hint that the field should be presented as a dropdown.

When `values` is a plain string array, each value is treated as both the code and the label. Human-readable labels are managed separately in the Domain Graph and injected by the engine -- they are not part of the Entity Spec itself.

### Attribute Options

| Option | What it does |
|--------|-------------|
| `required` | The attribute must have a value. Blank is not allowed. |
| `unique` | No two records can share the same value for this attribute. |
| `readonly` | The attribute cannot be changed after creation. Good for timestamps and audit fields. |
| `default` | Value to use when none is provided. Can be a literal value or the special string `"now()"` for the current timestamp. |
| `label` | Human-readable name for display in generated UIs and documentation. |
| `constraints` | Validation rules like `max_length`, `min`, `max`, `pattern`, `precision`, `scale`. |

Constraints are type-specific. Putting `max_length` on an `integer` does not make sense and tooling will tell you so.

---

## Relations

Relations describe how entities connect to each other. There are four types, and each one unlocks different UI and API patterns downstream.

### many_to_one

The most common relation. "Each task has one assignee (a user), but a user can be assigned many tasks."

```yaml
# On the task entity
relations:
  assignee:
    type: many_to_one
    target: user
    foreign_key: assignee_id     # attribute on task that holds the FK
    display_field: name           # which field on user to show in dropdowns
    nullable: true
    on_delete: set_null
```

The `foreign_key` is required and must name an attribute you have defined on this entity (in this case, `assignee_id` on `task`). The `display_field` names an attribute on the *target* entity -- it tells the UI what to show when rendering this relation (e.g., the user's `name` in a dropdown instead of a raw UUID).

In the generated UI, a `many_to_one` relation typically becomes a dropdown or search-select component. The options are populated from the target entity, showing the `display_field` value.

### one_to_many

The inverse of `many_to_one`. "A user has many tasks."

```yaml
# On the user entity
relations:
  tasks:
    type: one_to_many
    target: task
    mapped_by: assignee           # name of the relation on the target
```

`mapped_by` is required and must name a relation defined on the target entity. It tells the system which `many_to_one` this is the other side of.

In generated UIs, `one_to_many` relations typically produce master/detail views -- click on a user and see their tasks listed below.

### one_to_one

A strict 1:1 mapping. "Each user has exactly one profile."

```yaml
# On the user entity
relations:
  profile:
    type: one_to_one
    target: profile
```

### many_to_many

Both sides can have multiple. "A task can have many tags, and a tag can be on many tasks."

```yaml
# On the task entity
relations:
  tags:
    type: many_to_many
    target: tag
    join_table: task_tags          # required for many_to_many
```

`join_table` is required and names the intermediate table. You can optionally specify `join_columns` if the column names in the join table do not follow conventions:

```yaml
    join_columns:
      source: task_id
      target: tag_id
```

### Relation Options Reference

| Option | What it does |
|--------|-------------|
| `target` | The entity this relation points to. Required for all relation types. |
| `foreign_key` | The FK attribute name on the current entity. Required for `many_to_one`. |
| `display_field` | An attribute on the target entity used for display -- dropdown labels, grid columns, etc. |
| `nullable` | Whether the FK can be null (the relation is optional). |
| `on_delete` | What happens when the target record is deleted: `cascade` (delete this too), `restrict` (block deletion), or `set_null` (clear the FK). |
| `mapped_by` | The inverse relation name on the target entity. Required for `one_to_many`. |
| `join_table` | The join table name. Required for `many_to_many`. |

### What Relations Enable

Relations are not just documentation -- they drive concrete behavior in generated code:

- **Dropdowns** come from `many_to_one` + `display_field`. The UI knows to fetch the target entity's records and show the display field as option labels.
- **Master/detail views** come from `one_to_many`. Click a parent row, see the child collection below.
- **Multi-select or tag inputs** come from `many_to_many`. The UI presents a way to associate multiple items from both sides.
- **Joined columns in grids** come from `many_to_one` + `display_field`. Instead of showing a raw foreign key, the grid shows the related entity's display value.

---

## Computed Fields

Computed fields are derived values that the system calculates from an expression. They are always readonly -- users cannot edit them directly.

```yaml
computed:
  full_name:
    expression: "first_name || ' ' || last_name"
    type: string
    readonly: true
```

The `expression` is a string formula that references other attributes on the same entity. The `type` tells downstream tools what kind of value to expect.

Computed fields can appear in SUIS display blocks like any other field, but editors will render them as readonly.

---

## Display Hints

Display hints are optional semantic suggestions about how an entity should be presented by default. They are not layout instructions -- adapters are free to interpret them differently or ignore them. But they give the system useful defaults so generated UIs work well out of the box.

```yaml
display:
  default_sort: created_at desc
  default_fields: [title, status, assignee, due_date]
  search_fields: [title, description]
```

| Hint | What it does |
|------|-------------|
| `default_sort` | The default ordering for list views. Format: `field_name asc` or `field_name desc`. |
| `default_fields` | Which fields to show in list/grid views by default. A SUIS screen can override this, but when none is specified, this is what you get. |
| `search_fields` | Which fields to include when the user performs a text search. |

These hints reduce the amount of detail you need to spell out in SUIS screens. If you define `default_fields: [title, status, assignee]` on the entity, a SUIS browse screen that does not explicitly list fields can fall back to these defaults.

---

## Source Tracking

The `meta` block tracks where an entity definition came from. This matters because Entity Specs can be authored in different ways -- manually written, mechanically extracted from a database, inferred by an AI, or derived from an OpenAPI definition.

```yaml
meta:
  source: db               # mechanically extracted from database schema
```

The four source values:

| Source | Meaning |
|--------|---------|
| `db` | Extracted from an existing database schema (SQL, Prisma, etc.) |
| `inferred` | Generated by an AI/LLM from natural language or partial requirements |
| `openapi` | Derived from an OpenAPI/Swagger definition |
| `manual` | Written by hand |

For `inferred` entities, you should include a `confidence` score between 0 and 1:

```yaml
meta:
  source: inferred
  confidence: 0.85
```

The confidence score tells tooling and reviewers how sure the inference engine was about this entity definition. Lower confidence entities typically require more careful review before they are used for code generation.

Authoritative sources (`db`, `openapi`) and manually written entities do not need a confidence score -- they are treated as ground truth.

---

## Complete Example

Here is a realistic Entity Spec for a task management system with two entities, relations between them, display hints, and source tracking.

```yaml
# Task management domain model
entity_version: "1.0"

entities:
  task:
    label: Task
    primary_key: id

    meta:
      source: db                  # extracted from existing database

    attributes:
      id:
        type: uuid
        required: true

      title:
        type: string
        required: true
        label: "Title"
        constraints:
          max_length: 200

      description:
        type: text
        label: "Description"

      status:
        type: enum
        values: [draft, pending, approved, rejected]
        default: draft
        label: "Status"

      priority:
        type: string
        values: [low, medium, high, critical]  # string with values -> renders as dropdown
        default: medium
        label: "Priority"

      due_date:
        type: date
        label: "Due Date"

      created_at:
        type: datetime
        required: true
        default: now()
        readonly: true
        label: "Created"

      updated_at:
        type: datetime
        default: now()
        readonly: true
        label: "Updated"

      assignee_id:
        type: uuid                # FK column for the assignee relation

    relations:
      assignee:
        type: many_to_one
        target: user
        foreign_key: assignee_id  # points to the attribute above
        display_field: name       # show user's name in dropdowns
        nullable: true            # tasks can be unassigned
        on_delete: set_null       # unassign if user is deleted

    computed:
      is_overdue:
        expression: "due_date < current_date AND status NOT IN ('approved', 'rejected')"
        type: boolean
        readonly: true

    display:
      default_sort: created_at desc
      default_fields: [title, status, priority, assignee, due_date]
      search_fields: [title, description]

  user:
    label: User
    primary_key: id

    meta:
      source: db

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
          pattern: "^[\\w.-]+@[\\w.-]+\\.\\w+$"

      department:
        type: string
        label: "Department"

      active:
        type: boolean
        default: true
        label: "Active"

    relations:
      tasks:
        type: one_to_many         # inverse of task.assignee
        target: task
        mapped_by: assignee       # references the relation name on task

    display:
      default_sort: name asc
      default_fields: [name, email, department, active]
      search_fields: [name, email]
```

A few things to notice:

- The `task.assignee_id` attribute is the raw FK column. The `task.assignee` relation adds meaning to it -- target entity, display field, delete behavior.
- `user.tasks` is the inverse of `task.assignee`, linked via `mapped_by`. You do not need to repeat the FK information on the inverse side.
- `is_overdue` is a computed field. It derives from other attributes and is always readonly. SUIS can reference it in display blocks like any other field.
- Display hints give sensible defaults without dictating layout. A SUIS screen can override any of these.

---

## How Other Specs Use Entities

The Entity Spec is the foundation layer. Here is how the other three specs reference it:

**SUIS** references entities through `subject.domain`. When a screen declares `subject.domain: task`, the semantic validator looks up the `task` entity and verifies that every field name used in the screen actually exists as an attribute or relation. This prevents typos and stale references from reaching code generation.

**IAS** references entities through `resources[].entity`. When an IAS resource declares `entity: task`, the validator confirms the entity exists and uses its attribute definitions to validate field mappings.

**Workflow** binds to an entity and one of its enum fields. When a workflow declares `entity: task` and `status_field: status`, the validator confirms that `task` has a `status` attribute of type `enum`, and that the workflow's state names match the enum's `values` list.

In all three cases, the pattern is the same: declare an entity name, and the validator resolves it against the Entity Spec. If the entity or field does not exist, you get an error immediately -- not a broken generated artifact.

---

[<- Overview](01-overview.md) | [IAS ->](03-ias-spec.md) | [Glossary](glossary.md)

*Entity Spec v1.0 -- 2026-02-25*
