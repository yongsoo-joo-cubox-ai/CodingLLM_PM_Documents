[Home](README.md) | [← SUIS](04-suis-spec.md) | [Glossary](glossary.md)

# Workflow Spec — State Machines

> Define how entities move through business processes — approvals, lifecycles, escalations — with explicit states, transitions, and rules.

---

## What is the Workflow Spec?

The Workflow Spec defines state machines for business processes. Approval flows, order lifecycles, task progression — any process where an entity moves through defined states with rules about who can do what and when.

You write a YAML file that declares the states an entity can be in, the transitions between those states, and the conditions and side effects for each transition. A conforming compiler reads this and generates the state management logic, permission checks, notification triggers, and audit logging for the target platform.

Think of it as the blueprint for every "status" dropdown you have ever built — except instead of scattering the rules across controllers, services, and middleware, they live in one declarative document.

---

## When You Need It

Not every entity needs a workflow. A `Country` entity with `name` and `code` probably does not. But a `PurchaseOrder` that goes through drafting, review, approval, and fulfillment absolutely does.

Use the Workflow Spec when:

- **Records go through approval stages** — documents, requests, orders that need sign-off before they take effect.
- **Status changes have rules** — only managers can approve, only the author can resubmit, nobody can edit once it is finalized.
- **Transitions trigger side effects** — send a notification when something is submitted, stamp a timestamp when it is approved, fire a webhook when it is rejected.
- **You need an audit trail of state changes** — who moved this from "pending" to "approved" and when?

If your entity just has a boolean `active` flag, you probably do not need a full workflow. If it has a `status` field with three or more values and rules about how it moves between them, you do.

---

## Document Structure

A Workflow Spec file is YAML with a top-level `workflow` key:

```yaml
workflow:
  version: "1.0"
  name: purchase_order_approval
  entity: PurchaseOrder         # references an Entity Spec entity
  status_field: status          # the enum attribute that holds current state
  states:
    # ...
  transitions:
    # ...
```

**Required fields:**

| Field | What it is |
|-------|-----------|
| `version` | Always `"1.0"` for this spec version |
| `entity` | Name of an entity defined in the Entity Spec |
| `status_field` | Name of an enum attribute on that entity |
| `states` | Map of state definitions |
| `transitions` | List of transition definitions |

**Optional fields:**

| Field | What it is |
|-------|-----------|
| `name` | Human-readable workflow name |
| `description` | What this workflow manages |

The `entity` references an Entity Spec entity. The `status_field` names an enum attribute on that entity. The state names you define in `states` must match the enum values defined in the Entity Spec — this is how the two specs stay in sync.

---

## States

Each key under `states` is a state name, and each state has a `type`:

| Type | Meaning | Rules |
|------|---------|-------|
| `initial` | Starting point — where new records begin | Exactly one per workflow |
| `normal` | In-progress state — the entity is being worked on | Zero or more |
| `final` | End state — no further transitions out | At least one per workflow |

A workflow must have exactly one `initial` state and at least one `final` state. You can have as many `normal` states as your process requires.

### State Properties

Beyond `type`, states support optional properties:

| Property | Type | Purpose |
|----------|------|---------|
| `label` | string | Display name for UIs |
| `description` | string | What this state means in the process |
| `on_enter` | list of actions | Side effects when entering this state |
| `on_exit` | list of actions | Side effects when leaving this state |
| `permissions` | map | Who can view/edit the entity in this state |

### Example

```yaml
states:
  draft:
    type: initial
    label: "Draft"
    permissions:
      view: [author, admin]
      edit: [author]

  pending:
    type: normal
    label: "Pending Approval"
    on_enter:
      - action: notify
        params: { role: approver }
    permissions:
      view: [author, approver, admin]
      edit: []

  approved:
    type: final
    label: "Approved"
    on_enter:
      - action: set_field
        params: { field: approved_at, value: $now }
      - action: notify
        params: { role: author }
    permissions:
      view: [author, approver, admin]
      edit: []

  rejected:
    type: normal
    label: "Rejected"
    on_enter:
      - action: notify
        params: { role: author }
    permissions:
      view: [author, approver, admin]
      edit: [author]
```

Notice that `pending` and `approved` both have `edit: []` — nobody can modify the entity in those states. The record is locked during review and after approval. But `rejected` allows the `author` to edit, because they will need to revise and resubmit.

---

## Transitions

Transitions are the directed edges between states. They define how and when an entity moves from one state to another.

Here is the approval workflow from the states above, drawn as an ASCII diagram:

```
                                 +--approve--> [approved]
                                 |
[draft] --submit--> [pending] ---+
                                 |
                                 +--reject---> [rejected] --revise--> [draft]
```

The entity starts in `draft`. The author submits it, moving it to `pending`. From there, an approver either approves it (moving to the `approved` final state) or rejects it (moving to `rejected`). If rejected, the author can revise and resubmit, looping back to `draft`.

### Transition Properties

Each transition is an object in the `transitions` list:

| Property | Required | Type | Purpose |
|----------|----------|------|---------|
| `event` | yes | string | Trigger name — what the user "does" |
| `from` | yes | string | Source state |
| `to` | yes | string | Target state |
| `guard` | no | object | Condition that must be true |
| `action` | no | list | Side effects on this transition |
| `allowed_roles` | no | list of strings | Who can trigger this transition |
| `requires_comment` | no | boolean | Must provide a reason |

### Example

```yaml
transitions:
  - event: submit
    from: draft
    to: pending
    allowed_roles: [author]
    guard:
      all:
        - field: title
          operator: not_empty
        - field: amount
          operator: gt
          value: 0

  - event: approve
    from: pending
    to: approved
    allowed_roles: [approver, admin]
    requires_comment: false

  - event: reject
    from: pending
    to: rejected
    allowed_roles: [approver, admin]
    requires_comment: true

  - event: revise
    from: rejected
    to: draft
    allowed_roles: [author]
```

The `submit` transition has a guard — you cannot submit a purchase order without a title and a positive amount. The `reject` transition requires a comment — the approver must explain why. The `approve` transition does not require a comment, but the approver can still leave one.

---

## Guards

Guards are conditions that must be true for a transition to fire. Even if the user has the right role and the entity is in the right state, the transition will be blocked if the guard fails.

### Simple Guard

Check a single field:

```yaml
guard:
  field: title
  operator: not_empty
```

### Compound AND

All conditions must be true:

```yaml
guard:
  all:
    - field: title
      operator: not_empty
    - field: amount
      operator: gt
      value: 0
```

### Compound OR

At least one condition must be true:

```yaml
guard:
  any:
    - field: priority
      operator: eq
      value: high
    - field: escalated
      operator: eq
      value: true
```

### Nesting

You can nest `all` and `any` for more complex logic:

```yaml
guard:
  all:
    - field: title
      operator: not_empty
    - any:
        - field: priority
          operator: eq
          value: high
        - field: amount
          operator: gte
          value: 10000
```

This reads: "title must not be empty AND (priority must be high OR amount must be at least 10,000)."

### Operators

| Operator | Meaning | Needs `value`? |
|----------|---------|:--------------:|
| `eq` | Equal to | Yes |
| `ne` | Not equal to | Yes |
| `gt` | Greater than | Yes |
| `gte` | Greater than or equal | Yes |
| `lt` | Less than | Yes |
| `lte` | Less than or equal | Yes |
| `contains` | String/array contains | Yes |
| `in` | Value is in list | Yes |
| `not_empty` | Field is present and non-empty | No |
| `is_empty` | Field is absent or empty | No |

For `in`, the `value` is an array:

```yaml
guard:
  field: category
  operator: in
  value: [electronics, software, services]
```

---

## Actions

Actions are side effects that fire on state entry, state exit, or during a transition. They do not change the state itself — they are things that happen alongside the state change.

### Available Actions

| Action | What it does | Example params |
|--------|-------------|----------------|
| `notify` | Send in-app notification | `role: approver` |
| `email` | Send email | `to: author, template: approved` |
| `log` | Write audit log entry | `level: info` |
| `webhook` | Call HTTP endpoint | `url: ..., method: POST` |
| `set_field` | Update entity field | `field: approved_at, value: $now` |

### Where Actions Go

Actions can appear in three places:

**On state enter** — fires when the entity arrives in this state, regardless of which transition brought it here:

```yaml
states:
  approved:
    type: final
    on_enter:
      - action: set_field
        params: { field: approved_at, value: $now }
      - action: email
        params: { to: author, template: order_approved }
```

**On state exit** — fires when the entity leaves this state, regardless of where it is going:

```yaml
states:
  draft:
    type: initial
    on_exit:
      - action: log
        params: { level: info }
```

**On transition** — fires only for a specific transition:

```yaml
transitions:
  - event: reject
    from: pending
    to: rejected
    action:
      - action: log
        params: { level: warn }
```

If both a state's `on_enter` and a transition's `action` apply, the transition actions fire first, then the target state's `on_enter` actions.

### Variables

Actions support these built-in variables:

| Variable | Value |
|----------|-------|
| `$now` | Current timestamp (ISO 8601) |

---

## State Permissions

Each state can declare who can view and edit the entity while it is in that state. This gives you fine-grained control over record access as it moves through the workflow.

```yaml
permissions:
  view: [author, approver, admin]
  edit: [author]
```

- **`view`** — roles that can see the record in this state.
- **`edit`** — roles that can modify the record in this state. An empty list `[]` means the record is locked — nobody can edit it.

This is different from transition permissions (`allowed_roles`). State permissions control who can see and modify the record. Transition permissions control who can trigger a state change. You typically need both: the approver can view the pending record (state permission) and trigger the approve transition (transition permission), but cannot edit the record's fields while it is pending.

---

## Complete Example

Here is a full purchase order approval workflow bringing everything together:

```yaml
workflow:
  version: "1.0"
  name: purchase_order_approval
  description: "Purchase orders require manager approval above $500"
  entity: PurchaseOrder
  status_field: status

  states:
    draft:
      type: initial
      label: "Draft"
      description: "Author is preparing the order"
      permissions:
        view: [author, admin]
        edit: [author]

    pending_review:
      type: normal
      label: "Pending Review"
      description: "Waiting for manager approval"
      on_enter:
        - action: notify
          params: { role: manager }
        - action: email
          params: { to: manager, template: review_requested }
      permissions:
        view: [author, manager, admin]
        edit: []

    approved:
      type: final
      label: "Approved"
      description: "Order has been approved and can be fulfilled"
      on_enter:
        - action: set_field
          params: { field: approved_at, value: $now }
        - action: notify
          params: { role: author }
        - action: webhook
          params:
            url: /api/fulfillment/orders
            method: POST
      permissions:
        view: [author, manager, fulfillment, admin]
        edit: []

    rejected:
      type: normal
      label: "Rejected"
      description: "Order was rejected — author may revise and resubmit"
      on_enter:
        - action: notify
          params: { role: author }
        - action: email
          params: { to: author, template: order_rejected }
      permissions:
        view: [author, manager, admin]
        edit: [author]

    cancelled:
      type: final
      label: "Cancelled"
      description: "Order was cancelled by the author"
      on_enter:
        - action: log
          params: { level: info }
      permissions:
        view: [author, manager, admin]
        edit: []

  transitions:
    - event: submit
      from: draft
      to: pending_review
      allowed_roles: [author]
      guard:
        all:
          - field: title
            operator: not_empty
          - field: line_items
            operator: not_empty
          - field: total_amount
            operator: gt
            value: 0

    - event: approve
      from: pending_review
      to: approved
      allowed_roles: [manager, admin]
      requires_comment: false
      guard:
        field: total_amount
        operator: lte
        value: 50000
      action:
        - action: log
          params: { level: info }

    - event: reject
      from: pending_review
      to: rejected
      allowed_roles: [manager, admin]
      requires_comment: true
      action:
        - action: log
          params: { level: warn }

    - event: revise
      from: rejected
      to: draft
      allowed_roles: [author]

    - event: cancel
      from: draft
      to: cancelled
      allowed_roles: [author]

    - event: cancel
      from: rejected
      to: cancelled
      allowed_roles: [author]
```

The state diagram for this workflow:

```
                                           +--approve--> [approved]
                                           |
[draft] --submit--> [pending_review] ------+
   |                                       |
   |                                       +--reject---> [rejected]
   |                                                        |
   +--cancel--> [cancelled] <--cancel--+                    |
                                       +--------------------+
                                       |
                                       +--- revise --> [draft]
```

Things to notice:

- The `submit` guard ensures the order has a title, line items, and a positive total. You cannot submit an empty order.
- The `approve` guard caps single-manager approval at 50,000. Orders above that threshold would need a different workflow (or an extended one with escalation).
- `reject` requires a comment — the manager must explain why.
- The `cancel` event appears twice — you can cancel from `draft` or from `rejected`, but not from `pending_review` or `approved`. The same event name, different source states.
- When an order is approved, a webhook fires to the fulfillment system. This is how the workflow integrates with downstream processes.
- Both `approved` and `cancelled` are `final` states — once there, the record cannot transition further.

---

## How Workflow Connects to Other Specs

The Workflow Spec does not exist in isolation. It references and is referenced by the other UASL specs:

**Entity Spec** — The `entity` field references an entity defined in the Entity Spec. The `status_field` names an enum attribute on that entity. Your state names must match the enum values. If your Entity Spec defines:

```yaml
attributes:
  status:
    type: enum
    values: [draft, pending_review, approved, rejected, cancelled]
```

then your Workflow Spec states must use exactly those names.

**SUIS** — The Semantic UI Spec can reference workflow transitions using intent types. A button with `intent: approve` or `intent: reject` maps to the corresponding workflow event. The SUIS does not need to know the workflow rules — it just declares the intent, and the compiler wires it to the right transition with all its guards and permissions.

**IAS** — The Intent API Specification maps workflow events to HTTP endpoints. A `submit` event might become `POST /api/purchase-orders/{id}/submit`. The IAS defines the contract; the workflow defines the business rules behind it.

Together, the four specs describe the full picture: what the data looks like (Entity), how users interact with it (SUIS), how the API is shaped (IAS), and how the business process flows (Workflow).

---

[← SUIS](04-suis-spec.md) | [Glossary](glossary.md) | [Home](README.md)

*Workflow Spec v1.0 — 2026-01-29*
