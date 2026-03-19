[Home](README.md) | [← Entity Spec](02-entity-spec.md) | [Next: SUIS →](04-suis-spec.md)

---

# IAS — Intent API Specification

## What is IAS?

IAS is the bridge between UI intent and HTTP. When SUIS says "the user wants to search tasks," IAS says "that's a GET request to `/api/tasks` with query parameters." IAS keeps SUIS clean — no URLs, no HTTP verbs, no payload structures leak into the UI specification.

Think of IAS as a translation table. One side speaks in user intentions (browse, search, create, approve). The other side speaks in HTTP (GET, POST, PUT, DELETE, paths, query strings, request bodies). The two sides never meet directly — IAS sits between them.

## Why IAS Exists

Before IAS, UI specs embedded API details directly — URLs, methods, parameter mappings, the whole mess. This created tight coupling: changing an API path meant updating every UI spec that referenced it.

IAS separates "what the user intends" from "how the API implements it." The benefits are immediate:

- **Change API paths without touching UI specs.** Rename `/api/tasks` to `/api/v2/tasks` in one place.
- **Same SUIS document works with different backend APIs.** A Spring Boot backend and an Express backend can share the same SUIS, with different IAS documents.
- **Adapters get fully resolved HTTP operations for code generation.** The xframe5 or Vue compiler never guesses — it receives a concrete method, path, and parameter source.

## Document Structure

An IAS document is a YAML file with two top-level keys:

```yaml
api:
  version: "1.0"

  resources:
    # ... resource definitions go here
```

`api.version` is always `"1.0"` for now. The `api.resources` map is where everything happens — each key is a resource name, and each value describes how that resource's intents map to HTTP.

## Resources

Each resource maps to an entity (from the Entity Spec) and a base API path. Here is a minimal resource:

```yaml
resources:
  task:
    path: /api/tasks
    entity: task
    intents:
      browse:
        method: GET
        returns: collection
```

**Required fields:**

| Field | Rule | Example |
|-------|------|---------|
| `path` | Must start with `/` | `/api/tasks` |
| `entity` | Must match an entity name from the Entity Spec | `task` |
| `intents` | At least one intent must be defined | See below |

**Optional fields:**

| Field | Purpose | Example |
|-------|---------|---------|
| `field_map` | Converts between spec names and backend names | `due_date: dueDate` |

The `path` is the base. Individual intents can append to it with `path_suffix`.

## Intent Mapping

Each intent maps a semantic name to an HTTP operation. The semantic name comes from SUIS; the HTTP details are defined here.

```yaml
intents:
  view:
    method: GET
    path_suffix: "/{id}"
    returns: single
```

**Required fields:**

| Field | Values | Purpose |
|-------|--------|---------|
| `method` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` | The HTTP verb |
| `returns` | `collection`, `single`, `none` | What the adapter expects back |

**Optional fields:**

| Field | Purpose | Example |
|-------|---------|---------|
| `path_suffix` | Appended to the resource `path` | `/{id}` |
| `query_from` | Where query parameters come from | `filters` |
| `body_from` | Where the request body comes from | `form` |

### Standard CRUD Mapping

Most resources follow a predictable pattern. Here is the standard CRUD mapping that covers the majority of use cases:

| Intent | Method | Path | Returns |
|--------|--------|------|---------|
| browse | GET | /api/tasks | collection |
| search | GET | /api/tasks?{filters} | collection |
| view | GET | /api/tasks/{id} | single |
| create | POST | /api/tasks | single |
| edit | PUT | /api/tasks/{id} | single |
| delete | DELETE | /api/tasks/{id} | none |

You are not limited to these six. Custom intents (like `approve`, `reject`, `export`) follow the same structure.

## Parameter Sources

Parameters have to come from somewhere. IAS defines four sources that tell the adapter where to pull data:

| Source | Comes From | Used For |
|--------|------------|----------|
| `filters` | SUIS filter definitions | search and browse queries |
| `form` | Editor fields on the screen | create and edit submissions |
| `selection[]` | Multi-select checkboxes or similar | bulk operations |
| `context` | Screen state (current ID, parent ID) | contextual lookups |

Two rules govern which source goes where:

- **`query_from`** is only valid on `GET` requests. You cannot put query parameters on a POST body.
- **`body_from`** is only valid on `POST`, `PUT`, and `PATCH` requests. GET and DELETE do not carry request bodies.

The validator enforces these rules. If you write `query_from: filters` on a DELETE intent, validation fails with a clear error.

## Return Types

The `returns` field tells the adapter what shape of data to expect. This directly affects how the UI renders the response:

| Return Type | Adapter Behavior | Typical UI |
|-------------|------------------|------------|
| `collection` | Expects an array of records | Grid, list, table |
| `single` | Expects one record | Form, detail view |
| `none` | Expects no data (success/failure only) | Refresh the current view |

When `returns` is `none`, the adapter typically refreshes the current screen after the operation completes. A delete operation, for example, removes the row from the grid and stays on the same screen.

## Field Mapping

Backend APIs do not always use the same naming conventions as your entity spec. Java APIs commonly use camelCase, while entity specs use snake_case. The `field_map` handles the translation:

```yaml
resources:
  task:
    path: /api/tasks
    entity: task
    field_map:
      due_date: dueDate
      created_at: createdAt
      assigned_to: assignedTo
    intents:
      # ...
```

Keys are the entity attribute names (from the Entity Spec). Values are the backend API field names. The adapter applies this mapping when constructing requests and parsing responses.

If no `field_map` is provided, attribute names pass through unchanged.

## Bulk Operations

Sometimes users select multiple records and act on them at once. Bulk operations use `selection[]` as the body source:

```yaml
intents:
  bulk_delete:
    method: POST
    path_suffix: /bulk-delete
    body_from: "selection[]"
    returns: none
```

The adapter collects the selected IDs from the UI and sends them as the request body. Note that bulk operations typically use POST even for deletions — sending a list of IDs in a DELETE request body is not universally supported.

## Workflow Actions

Workflow transitions like approve and reject are mapped as custom intents. They follow the same pattern as CRUD intents, but with domain-specific semantics:

```yaml
intents:
  approve:
    method: POST
    path_suffix: "/{id}/approve"
    body_from: form
    returns: single

  reject:
    method: POST
    path_suffix: "/{id}/reject"
    body_from: form
    returns: single
```

The `body_from: form` here carries the approval comment or rejection reason. SUIS defines the form fields; IAS defines where they go.

## Complete Example

Here is a complete IAS document for a task management resource. It covers standard CRUD, bulk operations, workflow actions, and field mapping:

```yaml
api:
  version: "1.0"

  resources:
    task:
      path: /api/tasks
      entity: task

      field_map:
        due_date: dueDate
        created_at: createdAt
        assigned_to: assignedTo

      intents:
        browse:
          method: GET
          returns: collection

        search:
          method: GET
          query_from: filters
          returns: collection

        view:
          method: GET
          path_suffix: "/{id}"
          returns: single

        create:
          method: POST
          body_from: form
          returns: single

        edit:
          method: PUT
          path_suffix: "/{id}"
          body_from: form
          returns: single

        delete:
          method: DELETE
          path_suffix: "/{id}"
          returns: none

        bulk_delete:
          method: POST
          path_suffix: /bulk-delete
          body_from: "selection[]"
          returns: none

        approve:
          method: POST
          path_suffix: "/{id}/approve"
          body_from: form
          returns: single

        reject:
          method: POST
          path_suffix: "/{id}/reject"
          body_from: form
          returns: single
```

This single document gives the adapter everything it needs to generate HTTP client code, without SUIS knowing any of these details.

## How IAS Connects

IAS does not exist in isolation. It sits between the Entity Spec and SUIS, connecting them through three binding rules:

**Entity binding.** Each resource's `entity` field references an entity name from the Entity Spec. If the Entity Spec defines a `task` entity with attributes `id`, `title`, `status`, and `due_date`, the IAS resource for `task` can use those attributes in its `field_map`. The validator checks that the entity exists.

**SUIS intent binding.** Every operation intent declared in a SUIS screen must have a matching intent in the corresponding IAS resource. If a SUIS browse screen declares `intent: search`, the IAS resource must have a `search` intent defined. Missing mappings are hard errors — the validator will reject the spec.

**Workflow binding.** Workflow transition events (from the Workflow Spec) can have IAS bindings. When a workflow defines an `approve` transition, the IAS `approve` intent provides the HTTP details. This lets the workflow engine trigger API calls without embedding HTTP knowledge.

```
Entity Spec          IAS                    SUIS
-----------          ---                    ----
task entity  <----   task resource
  attributes         field_map
                     intents      ---->    operations
                       approve    ---->      intent: approve
                       search     ---->      intent: search
```

The compiler validates all three connections. If any link is broken — an entity that does not exist, an intent without a mapping, a field map referencing an unknown attribute — you get a clear error pointing to the exact location of the problem.

---

*IAS v1.0 — 2026-01-29*

---

[← Entity Spec](02-entity-spec.md) | [SUIS →](04-suis-spec.md) | [Glossary](glossary.md)
