# UASL Documentation Package

**Universal Application Specification Language**

This package contains the complete UASL language documentation for distribution. UASL is a family of four declarative specifications that describe applications at the semantic level, enabling deterministic code generation for any target framework.

## Languages

- **[English](en/README.md)** — Full documentation in English
- **[Korean / 한국어](ko/README.md)** — 한국어 전체 문서

## Contents

Each language folder contains:

| Document | Description |
|----------|-------------|
| `README.md` | Landing page with navigation |
| `01-overview.md` | UASL architecture, design philosophy, conformance |
| `02-entity-spec.md` | Entity Spec — domain model definition |
| `03-ias-spec.md` | IAS — intent-to-API mapping |
| `04-suis-spec.md` | SUIS — semantic UI specification |
| `05-workflow-spec.md` | Workflow Spec — state machine definition |
| `glossary.md` | Complete glossary of terms |

## JSON Schemas

The normative JSON Schemas are distributed separately in the `schemas/` directory:

```
schemas/
├── entity/v1.0/root.schema.json
├── suis/v1.1/root.schema.json
├── ias/v1.0/root.schema.json
└── workflow/v1.0/root.schema.json
```

## Version

- **UASL Version**: 1.0
- **Document Date**: 2026-02-25
- **Status**: Candidate Recommendation

## Changelog

### 2026-02-25

**Entity Spec (02-entity-spec.md)**
- Added "Values on Non-Enum Types" section — `string` and `integer` attributes now support `values` for dropdown rendering without changing storage type
- Updated example: `priority` changed from `type: enum` to `type: string` with `values` to demonstrate value-list feature

**SUIS (04-suis-spec.md)**
- Added "Field Values" section — `values` property on fields with `format: enum` for declaring allowed value codes
- Added `select` filter input type (alias for `dropdown`)
- Added composite purposes: `master_detail`, `list_detail_panel`, `tabbed_detail`
- Added "Composition" section for composite screens with parent-child entity relationships
- Added child properties reference table and purpose-composition constraints

**Dist package**
- Moved from `docs/dist/` to `docs/specs/dist/` to co-locate with source specs

### 2026-01-29

- Initial release of UASL Documentation Package
- All four specs at Candidate Recommendation status
- Bilingual documentation (English + Korean)
- LLM Training Guide included
