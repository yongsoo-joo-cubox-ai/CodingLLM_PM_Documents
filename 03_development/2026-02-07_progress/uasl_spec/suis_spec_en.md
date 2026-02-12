[Home](README.md) | [<- IAS](03-ias-spec.md) | [Next: Workflow ->](05-workflow-spec.md)

---

# SUIS -- Semantic UI Specification

## What is SUIS?

SUIS describes user interfaces by **intent**, not by implementation. Instead of saying "create a grid with 5 columns and a double-click handler," SUIS says "display a collection of tasks with these fields; when the user activates an item, open the editor." Framework adapters decide how to render this.

Think of SUIS as a conversation with the system about what users want to accomplish. You describe screens, the data users need to see, and the actions they can take. You never mention grids, buttons, inputs, or any framework-level concept. The adapter -- whether it targets xframe5, Vue, React, or something else entirely -- handles all of that.

---

## The Key Idea

SUIS describes **WHAT users want to do**, not **HOW the UI looks**.

The same SUIS document can generate an xframe5 screen, a Vue page, or a React component -- because it never mentions any framework concepts. It talks about "a collection of tasks" instead of "an SBGrid." It talks about "the user activates an item" instead of "double-click on a row." It talks about "submit" instead of "POST to /api/tasks."

This separation is what makes SUIS portable. Change your target framework tomorrow, rewrite zero SUIS documents.

---

## What SUIS Does NOT Do

This is worth calling out explicitly, because the boundaries matter as much as the features.

SUIS does **not** describe:

| Off-Limits | Who Handles It |
|------------|----------------|
| Grids, data sources, or widgets | Adapter's job -- it picks the right component for each display block |
| Pixel positions, sizes, or CSS | Adapter's job -- SUIS only provides semantic hints like `width_hint: wide` |
| DOM events like click / dblclick | Use semantic triggers instead (more on this below) |
| API URLs or HTTP verbs | That's what IAS is for -- SUIS never contains `/api/tasks` or `GET` |
| Framework-specific constructs | No `v-model`, no `SBGrid`, no `useState` -- none of it |

If you find yourself typing a framework name in a SUIS document, stop. You have crossed the line.

---

## Document Structure

A SUIS document is YAML with a top-level `ui` key. Two fields live inside it:

```yaml
ui:
  suis_version: "1.1"        # Required -- always "1.1"

  screens:                     # Required -- at least one screen
    task_browse: { ... }
    task_edit:   { ... }

  components:                  # Optional -- reusable display blocks
    task_summary: { ... }
```

- `suis_version` is always `"1.1"`. If you see `"1.0"`, update it -- v1.1 added field hints and operation feedback.
- `screens` is where all your screens live. Each key is a screen ID you pick.
- `components` is optional. Use it when multiple screens share the same display block.

---

## Screens

Each screen has **3 required parts** and 2 optional ones:

```yaml
screens:
  task_browse:
    subject:      { ... }     # What entity and what purpose (required)
    display:      { ... }     # What data is visible (required)
    operations:   [ ... ]     # What actions users can perform (required)
    navigation:   { ... }     # Screen-to-screen links (optional)
    permissions:  { ... }     # Role-based access (optional)
```

Every screen answers three questions:
1. **What is this screen about?** (subject)
2. **What does the user see?** (display)
3. **What can the user do?** (operations)

Navigation and permissions are there when you need them, but a screen works without them.

---

## Subject (Semantic Anchor)

The `subject` tells the system what entity this screen operates on and why. It is the semantic anchor for everything else on the screen.

```yaml
subject:
  domain: task                # References an entity from Entity Spec
  purpose: browse             # What this screen is for
  title: "Task Management"   # Human-readable title
  description: "View and manage all tasks"  # Optional description
```

The `domain` field is a direct reference to your Entity Spec. If you have an entity called `task` in your entity-spec.yaml, that is what goes here. If the entity does not exist, the validator will reject your document.

### Purpose

The `purpose` field describes what the screen is for:

| Purpose | Use Case |
|---------|----------|
| `browse` | List and search view -- showing multiple records |
| `view` | Read-only detail -- looking at one record without editing |
| `create` | New record form -- making something from scratch |
| `edit` | Edit form -- changing an existing record |
| `dashboard` | Aggregated summary -- KPIs, charts, overview data |
| `wizard` | Multi-step guided process -- step 1, step 2, step 3 |

Pick the one that best matches what the user is trying to accomplish on this screen.

---

## Display Blocks

The `display` section describes what data appears on the screen. It has a required `primary` block and optional `secondary` and `filters` sections.

```yaml
display:
  primary:
    type: collection
    fields: [ ... ]

  secondary:
    - type: summary
      fields: [ ... ]

  filters:
    - field: status
      operator: eq
      input: dropdown
```

### Block Types

There are three display block types, and the adapter decides how to render each one:

| Type | What It Represents | Adapter Renders As... |
|------|--------------------|-----------------------|
| `collection` | Multiple records | Grid, table, card list -- adapter's choice |
| `single` | One record | Form, detail view, card -- adapter's choice |
| `summary` | Aggregated data | KPI cards, stat bar, dashboard tiles -- adapter's choice |

Notice how none of these types mention a specific widget. `collection` could become an SBGrid in xframe5, an `el-table` in Vue, or a `<table>` in plain HTML. SUIS does not care.

---

## Fields

Each field in a display block references an entity attribute by `name`. Everything else is optional hints that adapters can use (or ignore).

```yaml
fields:
  - name: id                  # Required -- must match an entity attribute
    label: "ID"               # Display label
    format: integer            # How to display the value
    width_hint: narrow         # Relative width suggestion
    align_hint: end            # Alignment suggestion
    sortable: true             # Can users sort by this field?
    editable: false            # Can users edit inline?
    required: true             # Is this field required for form submission?
    visible: true              # Should the field be shown? (default: true)
```

### Format

The `format` tells adapters what kind of data this field contains:

| Format | What It Means |
|--------|---------------|
| `text` | A string -- names, titles, descriptions |
| `integer` | A whole number -- IDs, counts, quantities |
| `decimal` | A precise number -- measurements, percentages |
| `currency` | A money value -- prices, totals, balances |
| `date` | A date without time -- due dates, birthdays |
| `datetime` | A date with time -- timestamps, created_at |
| `enum` | A fixed set of values -- status, priority, type |
| `boolean` | True/false -- active, completed, enabled |

### Width and Alignment Hints

These are **semantic hints**, not pixel values. The adapter interprets them according to its own conventions.

**Width hint** -- how much horizontal space this field wants:

| Value | Think of it as... |
|-------|-------------------|
| `narrow` | Compact. Good for IDs, status badges, boolean toggles. |
| `medium` | Standard column width. Names, dates, short text. |
| `wide` | Needs room. Titles, descriptions, email addresses. |
| `fill` | Take whatever space is left. Long text, notes. |

**Alignment hint** -- where content sits within its space:

| Value | Typical use |
|-------|-------------|
| `start` | Text, names (left-aligned in LTR languages) |
| `center` | Status badges, boolean indicators |
| `end` | Numbers, currency, dates (right-aligned in LTR) |

The key word here is *hint*. An xframe5 adapter might map `wide` to 300px. A Vue adapter might map it to `flex: 2`. A mobile adapter might ignore it entirely and stack everything vertically. The SUIS document stays the same regardless.

---

## Filters

Filters are for browse and search screens. They define what criteria users can search by.

```yaml
filters:
  - field: status              # Entity attribute to filter on
    operator: eq               # How to compare
    input: dropdown            # What kind of input to show
    options: ["pending", "in_progress", "completed"]

  - field: due_date
    operator: range
    input: date_range

  - field: title
    operator: contains
    input: text
```

### Operators

| Operator | What It Means |
|----------|---------------|
| `eq` | Equals -- exact match |
| `ne` | Not equals -- exclude this value |
| `gt` | Greater than |
| `lt` | Less than |
| `gte` | Greater than or equal to |
| `lte` | Less than or equal to |
| `range` | Between two values (inclusive) |
| `contains` | String contains -- substring search |
| `in` | Set membership -- value is in a given list |

### Input Types

| Input | What Users See |
|-------|----------------|
| `text` | Type freely |
| `number` | Enter a numeric value |
| `date` | Pick a single date |
| `date_range` | Pick a start and end date |
| `dropdown` | Pick from a list of options |
| `multi_select` | Pick multiple options from a list |

The adapter decides the actual widget. A `dropdown` might become a `<select>`, a combo box, or a searchable autocomplete depending on the framework. SUIS does not specify.

---

## Operations (User Intentions)

Operations are the core of SUIS. Each one describes something the user wants to do on this screen.

```yaml
operations:
  - intent: search

  - intent: create
    opens: task_edit

  - intent: edit
    trigger: activate_item
    opens: task_edit

  - intent: delete
    trigger: bulk_selection
    confirmation: "Delete selected tasks?"

  - intent: submit
    success_feedback: "Task saved successfully"
    post_action: close
```

### Intent

Every operation starts with an `intent` -- what the user wants to accomplish:

| Intent | What the User Wants |
|--------|---------------------|
| `browse` | See a list of records |
| `search` | Find records matching criteria |
| `create` | Make something new |
| `edit` | Change an existing record |
| `delete` | Remove something |
| `submit` | Save the current form |
| `approve` | Approve (workflow action) |
| `reject` | Reject (workflow action) |
| `export` | Get data out of the system |
| `import` | Bring data into the system |
| `custom` | Anything that does not fit the above |

Each intent maps to an IAS intent that defines the actual HTTP operation. SUIS never knows or cares about `GET /api/tasks` -- it just says `intent: search` and IAS handles the rest.

---

## Triggers (Semantic, Not DOM)

This is one of the most important concepts in SUIS, so let's really drive it home.

Triggers describe **how an operation is initiated** in terms of user intent, never in terms of DOM events. Here is the full list, with a column showing what you should absolutely not write:

| Trigger | What It Means | NOT This |
|---------|---------------|----------|
| `activate_item` | User wants to interact with this item | ~~dblclick~~ |
| `select_item` | User picks an item from a list | ~~onclick~~ |
| `bulk_selection` | User selects multiple items to act on | ~~checkbox~~ |
| `confirm_action` | User explicitly confirms an action | ~~button click~~ |
| `value_change` | A field value just changed | ~~onchange~~ |
| `automatic` | Happens on page load or on a timer | ~~DOMContentLoaded~~ |

Why does this matter? Because triggers describe **user intent**, and the adapter maps them to **framework events**. The same trigger produces different code on different platforms:

- `activate_item` becomes `row_double_click` in xframe5
- `activate_item` becomes `@dblclick` on a row in Vue
- `activate_item` becomes `onDoubleClick` in React

The SUIS document never changes. The adapter handles the translation. If you wrote `dblclick` in your SUIS document, you would be locked to a specific event model -- and the xframe5 adapter would not know what to do with it.

---

## Operation Hints

Operations can carry additional hints that tell adapters how to handle the result:

```yaml
operations:
  - intent: edit
    trigger: activate_item
    opens: task_edit                     # Navigate to this screen
    confirmation: "Edit this task?"      # Ask before proceeding (required for delete)
    success_feedback: "Saved!"           # Show this after success
    post_action: close                   # What to do after: refresh, close, or navigate
```

| Hint | What It Does |
|------|--------------|
| `opens` | Target screen ID to navigate to when the operation fires |
| `confirmation` | A message shown to the user before executing. Required for `delete` intent. |
| `success_feedback` | A message shown after successful completion |
| `post_action` | What happens next: `refresh` the current screen, `close` the current screen, or `navigate` elsewhere |

---

## Navigation

Navigation defines how screens connect to each other.

```yaml
navigation:
  to_editor:
    target: task_edit          # Screen ID -- must exist in screens
    mode: modal                # "modal" or "full" (default: full)
```

- `target` is a screen ID from your `screens` section. The validator checks that it exists.
- `mode` controls how the target screen appears. `modal` opens it as an overlay; `full` replaces the current screen. Default is `full`.

Navigation works hand-in-hand with the `opens` hint on operations. When an operation has `opens: task_edit`, the adapter looks at the navigation section to determine whether to open it as a modal or a full page.

---

## Permissions

Permissions declare which roles can access a screen.

```yaml
permissions:
  roles: [admin, manager, user]
```

This is a declaration, not enforcement. SUIS tells the adapter what roles are expected; the runtime (your backend, your auth middleware) enforces it. Generated code might include role checks, conditional button visibility, or route guards -- but that is the adapter's decision.

---

## Components

Components are reusable display blocks that can be shared across multiple screens. If you have a KPI summary that appears on both the dashboard and the browse screen, define it once as a component.

```yaml
components:
  task_summary:
    type: summary
    fields:
      - name: total_count
        label: "Total Tasks"
        format: integer
      - name: pending_count
        label: "Pending"
        format: integer
      - name: completed_count
        label: "Completed"
        format: integer
```

Components use the same structure as display blocks (`type` + `fields`). Screens can reference them instead of duplicating field definitions.

---

## Complete Example

Here is a full SUIS document with a browse screen and an edit screen. This is the kind of document you would write for a task management feature.

```yaml
ui:
  suis_version: "1.1"

  screens:
    # -------------------------------------------------------
    # Browse screen: list tasks, search, create, edit, delete
    # -------------------------------------------------------
    task_browse:
      subject:
        domain: task
        purpose: browse
        title: "Task Management"
        description: "View and manage all tasks"

      display:
        primary:
          type: collection
          fields:
            - name: id
              label: "ID"
              format: integer
              width_hint: narrow
              align_hint: end
              sortable: true

            - name: title
              label: "Title"
              format: text
              width_hint: wide
              sortable: true

            - name: assignee
              label: "Assignee"
              format: text
              width_hint: medium

            - name: due_date
              label: "Due Date"
              format: date
              width_hint: medium
              sortable: true

            - name: status
              label: "Status"
              format: enum
              width_hint: narrow
              align_hint: center

        # Search filters for the browse screen
        filters:
          - field: status
            operator: eq
            input: dropdown
            options: ["pending", "in_progress", "completed"]

          - field: due_date
            operator: range
            input: date_range

          - field: title
            operator: contains
            input: text

      operations:
        # Search: filter the list
        - intent: search

        # Create: open the editor for a new task
        - intent: create
          opens: task_edit

        # Edit: activate a row to open the editor
        - intent: edit
          trigger: activate_item
          opens: task_edit

        # Delete: select multiple, then confirm
        - intent: delete
          trigger: bulk_selection
          confirmation: "Delete selected tasks?"

        # Export: download the current list
        - intent: export

      navigation:
        to_editor:
          target: task_edit
          mode: modal

      permissions:
        roles: [admin, manager, user]

    # -------------------------------------------------------
    # Edit screen: edit or create a single task
    # -------------------------------------------------------
    task_edit:
      subject:
        domain: task
        purpose: edit
        title: "Task Editor"

      display:
        primary:
          type: single
          fields:
            - name: title
              label: "Title"
              format: text
              required: true

            - name: description
              label: "Description"
              format: text

            - name: assignee
              label: "Assignee"
              format: text

            - name: due_date
              label: "Due Date"
              format: date

            - name: status
              label: "Status"
              format: enum

      operations:
        # Submit: save the form and close
        - intent: submit
          success_feedback: "Task saved successfully"
          post_action: close

        # Back: return to the browse screen
        - intent: browse
          opens: task_browse

      permissions:
        roles: [admin, manager, user]
```

Notice a few things about this example:

- There is no mention of SBGrid, el-table, v-model, or any widget name.
- There are no URLs, no HTTP verbs, no fetch calls -- IAS handles all of that.
- The `activate_item` trigger does not say "double-click" -- the adapter maps it.
- The `delete` operation requires `confirmation` -- this is enforced by the validator.
- Fields use `width_hint` and `align_hint`, never pixel values.

---

## How SUIS Connects to Other Specs

SUIS does not exist in isolation. It connects to every other UASL spec:

**Entity Spec** -- `subject.domain` must name a real entity. Every field `name` in your display blocks must match an attribute or relation on that entity. If your Entity Spec defines `task` with attributes `title`, `status`, `due_date`, and `assignee_id` (plus a relation `assignee`), those are the names you use in SUIS.

**IAS (Intent API Specification)** -- every operation `intent` in SUIS must have a corresponding mapping in IAS. When SUIS says `intent: search`, IAS tells the adapter that this means `GET /api/tasks` with query parameters from filters. SUIS never contains API details -- that is the entire point of IAS.

**Workflow Spec** -- workflow intents like `approve` and `reject` in SUIS correspond to state transitions defined in the Workflow Spec. If the workflow says a task can transition from `pending` to `approved` via an `approve` event, then the SUIS screen can have an operation with `intent: approve`.

The semantic validator checks all of these connections. If you reference an entity that does not exist, a field that is not on the entity, or an intent that has no IAS mapping, the validator will reject your document before any code gets generated.

---

[<- IAS](03-ias-spec.md) | [Workflow ->](05-workflow-spec.md) | [Glossary](glossary.md)

*SUIS v1.1 -- 2026-01-29*
