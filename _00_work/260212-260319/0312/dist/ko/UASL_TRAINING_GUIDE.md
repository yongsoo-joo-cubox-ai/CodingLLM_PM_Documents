# UASL 스펙 생성 — LLM 학습 가이드

## 목적

이 문서는 자연어 사용자 요청으로부터 UASL 규격 스펙을 생성하도록 LLM을 학습시키기 위한 가이드입니다. 생성 파이프라인은 두 단계로 구성됩니다:

1. **엔티티 추론** — 자연어로부터 Entity Spec 생성 (엔티티 모델이 제공되지 않은 경우)
2. **SUIS 생성** — Entity Spec + 사용자 요청으로부터 Semantic UI Specification 생성

LLM은 두 가지 시나리오를 모두 처리해야 합니다:
- **시나리오 A**: Entity Spec이 외부에서 제공됨 → SUIS 생성으로 바로 진행
- **시나리오 B**: 엔티티 모델이 없음 → Entity Spec을 먼저 추론한 후 SUIS 생성

---

## Part 1: Entity Spec v1.0 언어 레퍼런스

### 개요

Entity Spec은 정규 도메인 모델을 정의합니다. 엔티티(도메인 객체), 속성, 엔티티 간 관계, 계산 필드, 표시 힌트를 기술합니다. 다른 모든 UASL 스펙은 이 문서를 도메인 진실의 단일 소스(Single Source of Truth)로 참조합니다.

### 문서 구조

```yaml
entity_version: "1.0"       # 항상 "1.0"

entities:
  entity_name:               # snake_case 엔티티 이름
    label: "표시 이름"        # 사람이 읽을 수 있는 단수 명사
    primary_key: id          # 아래 attributes에 정의된 속성 이름

    meta:                    # 출처 추적 (선택)
      source: inferred       # db | inferred | openapi | manual
      confidence: 0.85       # 0-1, source가 "inferred"일 때 필수

    attributes:              # 최소 하나의 속성 필수
      field_name:
        type: string         # 아래 타입 표 참조
        required: true       # 필수 필드 여부
        unique: false        # 값 유일성 제약
        readonly: false      # 생성 후 수정 불가 여부
        default: "value"     # 기본값 (타임스탬프는 "now()")
        label: "표시명"       # 사람이 읽을 수 있는 레이블
        values: [a, b, c]    # type이 "enum"일 때 필수
        constraints:         # 유효성 검증 (선택)
          max_length: 200
          min_length: 1
          pattern: "^[A-Z]"
          min: 0
          max: 100
          precision: 10
          scale: 2

    relations:               # 선택
      relation_name:
        type: many_to_one    # 아래 관계 타입 참조
        target: other_entity # entities에 존재해야 함
        foreign_key: fk_id   # FK 속성 이름 (many_to_one)
        display_field: name  # 대상 엔티티에서 드롭다운 표시에 사용할 필드
        nullable: true
        on_delete: set_null  # cascade | restrict | set_null

    computed:                # 선택
      full_name:
        expression: "first_name || ' ' || last_name"
        type: string
        readonly: true

    display:                 # 표시 힌트 (선택)
      default_sort: created_at desc
      default_fields: [name, status, created_at]
      search_fields: [name, description]
```

### 속성 타입

| 타입 | 설명 | 주요 제약조건 |
|------|------|-------------|
| `string` | 짧은 텍스트 (이름, 코드) | `max_length`, `min_length`, `pattern` |
| `text` | 긴 텍스트 (설명, 비고) | `max_length` |
| `integer` | 정수 | `min`, `max` |
| `decimal` | 정밀 소수 | `min`, `max`, `precision`, `scale` |
| `currency` | 금액 (min 기본값 0) | `precision`, `scale` |
| `boolean` | 참/거짓 | — |
| `date` | 날짜만 (YYYY-MM-DD) | `min`, `max` |
| `datetime` | 날짜와 시간 | `min`, `max` |
| `uuid` | UUID v4 식별자 | — |
| `enum` | 고정 값 집합 | `values` (필수) |

### 관계 타입

| 타입 | 카디널리티 | 예시 | 필수 필드 |
|------|-----------|------|----------|
| `one_to_one` | 1:1 | User → Profile | `target` |
| `many_to_one` | N:1 | Task → User | `target`, `foreign_key` |
| `one_to_many` | 1:N | User → Tasks | `target`, `mapped_by` |
| `many_to_many` | M:N | Task ↔ Tags | `target`, `join_table` |

### 관계가 UI에서 활성화하는 패턴

| 관계 | UI 패턴 |
|------|---------|
| `many_to_one` + `display_field` | 드롭다운 선택기, 그리드에서 JOIN 표시 |
| `one_to_many` + `mapped_by` | 마스터/디테일 뷰, 하위 컬렉션 |
| `many_to_many` + `join_table` | 다중 선택, 태그 입력 |

### 유효성 검증 규칙

규칙은 세 단계로 구분됩니다: **MUST** (위반 시 스펙 무효), **SHOULD** (강력 권장, 명확한 이유가 있을 때만 예외), **MAY** (선택, LLM 판단에 위임).

**MUST (절대 — 위반 시 스펙 무효):**
1. `entity_version`은 반드시 `"1.0"`이어야 한다
2. 모든 엔티티는 반드시 `primary_key`와 `attributes`를 가져야 한다
3. `primary_key`는 반드시 `attributes`에 정의된 속성 이름이어야 한다
4. `enum` 타입은 반드시 비어 있지 않은 `values` 배열을 가져야 한다
5. `relation.target`은 반드시 `entities`에 존재하는 엔티티 이름이어야 한다
6. `foreign_key`는 반드시 같은 엔티티의 `attributes`에 정의된 속성 이름이어야 한다
7. `many_to_one`은 반드시 `foreign_key`를 가져야 한다
8. `one_to_many`는 반드시 `mapped_by`를 가져야 한다
9. `many_to_many`는 반드시 `join_table`을 가져야 한다

**SHOULD (강력 권장 — 명확한 이유 없이 생략하지 않는다):**
10. 엔티티 이름은 `snake_case`를 사용해야 한다
11. 모든 엔티티는 가독성을 위해 `label`을 포함해야 한다
12. 추론된 엔티티는 `meta.source`와 `meta.confidence`를 포함해야 한다
13. `many_to_one` 관계는 UI 렌더링을 위해 `display_field`를 포함해야 한다

**MAY (선택 — 적절할 때 사용):**
14. 엔티티는 기본 표시를 위한 `display` 힌트를 포함할 수 있다
15. 엔티티는 파생 값을 위한 `computed` 필드를 포함할 수 있다

---

## Part 2: SUIS v1.1 언어 레퍼런스

### 개요

SUIS(Semantic UI Specification)는 의도 기반의 프레임워크 비종속적 UI 기술 언어입니다. 사용자가 무엇을 하려는지를 기술하며, UI가 어떻게 구축되는지는 명시하지 않습니다. 그리드, 데이터소스, 클릭 핸들러, 픽셀 위치, CSS는 포함하지 않습니다.

### 문서 구조

```yaml
ui:
  suis_version: "1.1"       # 항상 "1.1"

  screens:
    screen_id:               # snake_case 화면 식별자
      subject:               # 어떤 엔티티와 목적인지
        domain: entity_name  # Entity Spec에 존재해야 함
        purpose: browse      # browse | view | create | edit | dashboard | wizard
        title: "화면 제목"
        description: "선택적 설명"

      display:
        primary:             # 주요 콘텐츠 영역 (필수)
          type: collection   # collection | single | summary
          fields:
            - name: field_name    # 엔티티에 존재해야 함
              label: "레이블"
              format: text        # text|integer|decimal|currency|date|datetime|enum|boolean
              sortable: true
              width_hint: medium  # narrow | medium | wide | fill
              align_hint: start   # start | center | end
              editable: false
              required: true

        secondary:           # 부가 영역 (선택)
          - type: summary
            fields: [...]

        filters:             # 필터 (선택, browse 화면용)
          - field: status
            operator: eq     # eq|ne|gt|lt|gte|lte|range|contains|in
            input: dropdown  # text|number|date|date_range|dropdown|multi_select
            options: [...]

      operations:            # 사용 가능한 작업
        - intent: search
        - intent: create
          opens: target_screen
        - intent: edit
          trigger: activate_item
          opens: target_screen
        - intent: delete
          trigger: bulk_selection
          confirmation: "선택한 항목을 삭제하시겠습니까?"
        - intent: submit
          success_feedback: "저장되었습니다"
          post_action: close    # refresh | close | navigate

      navigation:            # 화면 간 링크 (선택)
        to_editor:
          target: screen_id
          mode: modal        # modal | full

      permissions:
        roles: [admin, manager, user]
```

### 화면 목적 타입

| 목적 | 사용 시점 |
|------|----------|
| `browse` | 다수 레코드의 목록/검색 (메인 진입 화면) |
| `view` | 단일 레코드 읽기 전용 상세 |
| `create` | 새 레코드 등록 폼 |
| `edit` | 기존 레코드 편집 폼 |
| `dashboard` | KPI 등 집계 요약 뷰 |
| `wizard` | 다단계 안내 프로세스 |

### 표시 블록 타입

| 타입 | 사용 시점 |
|------|----------|
| `collection` | 다수 레코드 표시 (그리드/목록) |
| `single` | 단일 레코드 표시 (폼/상세) |
| `summary` | 집계 데이터 (건수, KPI) |

### 작업 의도 (Operation Intent)

| 의도 | 설명 |
|------|------|
| `browse` | 레코드 목록 조회 |
| `view` | 단일 레코드 상세 조회 |
| `search` | 레코드 필터/검색 |
| `create` | 새 레코드 등록 |
| `edit` | 기존 레코드 편집 |
| `delete` | 레코드 삭제 — 반드시 `confirmation` 필요 |
| `submit` | 폼 데이터 제출 |
| `approve` / `reject` | 워크플로우 전환 (승인/반려) |
| `export` / `import` | 데이터 내보내기/가져오기 |
| `custom` | 사용자 정의 작업 |

### 시맨틱 트리거 (DOM 이벤트가 아님)

| 트리거 | 의미 |
|--------|------|
| `select_item` | 사용자가 행/항목을 선택 |
| `activate_item` | 사용자가 항목과 상호작용하려 함 (열기/편집) |
| `bulk_selection` | 사용자가 여러 항목을 선택 |
| `confirm_action` | 사용자가 명시적으로 확인 |
| `value_change` | 반응형 폼 값 변경 |
| `automatic` | 로드 시 / 타이머 |

### 너비 힌트 (Width Hint)

| 힌트 | 용도 |
|------|------|
| `narrow` | ID, 상태 배지, 불리언 |
| `medium` | 이름, 날짜, 일반 필드 |
| `wide` | 제목, 설명, 긴 텍스트 |
| `fill` | 남은 공간을 모두 채움 |

### 정렬 힌트 (Align Hint)

| 힌트 | 용도 |
|------|------|
| `start` | 텍스트 필드 (기본값) |
| `center` | 상태, 불리언, 열거형 |
| `end` | 숫자, 금액, 날짜 |

### SUIS 유효성 검증 규칙

규칙은 세 단계로 구분됩니다: **MUST** (위반 시 스펙 무효), **SHOULD** (강력 권장, 명확한 이유가 있을 때만 예외), **MAY** (선택, LLM 판단에 위임).

**MUST (절대 — 위반 시 스펙 무효):**
1. `suis_version`은 반드시 `"1.1"`이어야 한다
2. 모든 화면은 반드시 `subject`, `display`, `operations`를 가져야 한다
3. `subject.domain`은 반드시 Entity Spec의 엔티티를 참조해야 한다
4. `display.primary`는 반드시 존재하며 `type`과 최소 하나의 필드를 가져야 한다
5. `collection`과 `single` 블록의 `fields[].name`은 반드시 엔티티의 속성, 관계 이름, 또는 계산 필드 이름을 참조해야 한다
6. `delete` 의도는 반드시 `confirmation`을 가져야 한다
7. `opens`와 `navigation.target`은 반드시 존재하는 화면 ID를 참조해야 한다
8. 프레임워크 종속 개념(그리드, 데이터소스, 클릭 핸들러, CSS, 픽셀 값)을 절대 포함하지 않는다

**SHOULD (강력 권장 — 명확한 이유 없이 생략하지 않는다):**
9. `opens`를 가진 `edit`/`view` 작업은 `trigger`를 가져야 한다
10. `browse` 화면은 `search` 작업을 포함해야 한다
11. `edit`/`create` 화면은 `success_feedback`이 있는 `submit` 작업을 포함해야 한다
12. 필드는 일관된 어댑터 출력을 위해 `width_hint`와 `align_hint`를 가져야 한다

**MAY (선택 — 적절할 때 사용):**
13. `summary` 표시 블록은 엔티티에 존재하지 않는 파생 필드 이름(예: `total_count`, `pending_amount`)을 포함할 수 있다. 요약 블록은 집계 지표를 나타내기 때문이다
14. 화면은 역할 기반 접근 제어를 위해 `permissions`를 포함할 수 있다
15. `browse` 화면은 `export` 작업을 포함할 수 있다

---

## Part 3: Entity Spec → SUIS 필드 매핑

Entity Spec에서 SUIS를 생성할 때, 엔티티 속성을 SUIS 필드 속성에 매핑합니다:

| 엔티티 속성 타입 | SUIS Format | 기본 Width Hint | 기본 Align Hint |
|-----------------|-------------|----------------|-----------------|
| `string` | `text` | `medium` | `start` |
| `text` | `text` | `wide` | `start` |
| `integer` | `integer` | `narrow` | `end` |
| `decimal` | `decimal` | `medium` | `end` |
| `currency` | `currency` | `medium` | `end` |
| `boolean` | `boolean` | `narrow` | `center` |
| `date` | `date` | `medium` | `center` |
| `datetime` | `datetime` | `medium` | `center` |
| `uuid` (기본 키) | `text` | `narrow` | `end` |
| `enum` | `enum` | `narrow` | `center` |

SUIS에서의 관계 표현:
- `many_to_one` 관계는 관계 이름을 필드 이름으로 사용 (예: `assignee`), format은 `text`, `display_field`가 레이블 값을 제공
- `one_to_many` 관계는 상세/편집 화면에서 secondary collection 표시로 활용 가능
- `many_to_many` 관계는 편집 화면에서 다중 선택 필드로 활용 가능

---

## Part 4: 프롬프트 — 자연어로부터 Entity Spec 생성

엔티티 모델이 없어서 사용자의 자연어 요청으로부터 추론해야 할 때 이 프롬프트를 사용합니다.

### 시스템 프롬프트

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

### 사용자 프롬프트 템플릿

```
Generate an Entity Spec for the following application:

{user_request}

Requirements:
- Include all entities mentioned or implied
- Define relations between entities
- Add reasonable attributes based on the domain
- Include display hints for default list views
```

### 입출력 예시

**입력:**
```
사원 관리 시스템. 사원은 이름, 이메일, 입사일, 직급이 있고 부서에 소속된다. 부서는 이름과 코드가 있다.
```

**출력:**
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

## Part 5: 프롬프트 — Entity Spec으로부터 SUIS 생성

Entity Spec이 제공되어 SUIS 화면을 생성해야 할 때 이 프롬프트를 사용합니다.

### 시스템 프롬프트

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

### 사용자 프롬프트 템플릿

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

### 입출력 예시

**입력 Entity Spec:**
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

**입력 요청:**
```
사원 목록 화면과 사원 편집 화면을 만들어줘. 부서별, 직급별 필터가 필요해.
```

**출력:**
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

## Part 6: 2단계 파이프라인

사용자 요청을 처음부터 끝까지 처리할 때의 흐름:

### 1단계: 엔티티 해결

```
IF entity_spec이 외부에서 제공됨:
    그대로 사용 → 2단계로 진행
ELSE:
    Entity Spec 생성 프롬프트 실행 (Part 4)
    모든 엔티티에 meta.source: inferred 표시
    → 2단계로 진행
```

### 2단계: SUIS 생성

```
Entity Spec (제공된 것 또는 추론된 것) + 사용자 요청을 입력으로
SUIS 생성 프롬프트 실행 (Part 5)
출력 검증:
  - 모든 subject.domain 참조가 Entity Spec에 존재하는지
  - 모든 필드 이름이 엔티티 속성 또는 관계로 존재하는지
  - 모든 화면 간 참조(opens, navigation.target)가 유효한지
  - delete 의도에 confirmation이 있는지
```

### 통합 프롬프트 (양쪽 단계를 한 번에)

Entity Spec이 없어서 한 번의 패스로 두 단계를 모두 수행해야 할 때:

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
[Part 4 시스템 프롬프트의 모든 규칙 포함]

## SUIS Rules
[Part 5 시스템 프롬프트의 모든 규칙 포함]

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

## Part 7: 실패 전략

LLM이 유효한 스펙을 생성할 수 없을 때, 환각(hallucination)보다 우아한 실패를 선택해야 합니다. 이 규칙들은 엣지 케이스에서의 동작을 정의합니다.

### 7.1 모호하거나 불충분한 입력

사용자 요청이 너무 모호하여 도메인 모델을 추론할 수 없을 때 (예: "관리 화면 만들어줘"):

```
IF 요청에서 식별 가능한 엔티티나 도메인 명사를 찾을 수 없으면:
    빈 Entity Spec 스텁을 출력:
      entity_version: "1.0"
      entities: {}
    그리고 명확화가 필요하다는 신호를 반환 (환각된 스펙이 아님)
```

LLM은 "관리", "시스템", "데이터" 같은 일반 단어로부터 엔티티를 발명해서는 안 된다.

### 7.2 비CRUD 요청

요청이 CRUD 지향 도메인 모델로 매핑할 수 없을 때 (예: "차트 생성", "로그인 페이지 만들기"):

- 비엔티티 UI(로그인, 설정, 정적 페이지) 요청인 경우: `purpose: custom`과 최소한의 작업으로 SUIS 출력. 엔티티 바인딩을 강제하지 않음.
- UASL 범위를 완전히 벗어나는 요청인 경우 (예: "REST API 작성", "배치 작업 생성"): 아무것도 출력하지 않고 범위 밖임을 알림.

### 7.3 부분적 정보

일부 엔티티는 명확하지만 다른 것은 모호할 때:

- 명확한 엔티티에 대해서만 스펙 생성
- 모호한 부분은 낮은 `meta.confidence` (0.5-0.7)로 표시
- 일반적인 플레이스홀더 엔티티로 빈 부분을 채우지 않음

### 7.4 상충하는 요구사항

사용자 요청에 모순이 있을 때 (예: "읽기 전용 편집 폼"):

- 일반적인 지시보다 더 구체적인 지시를 우선
- 진정으로 양립 불가능한 경우, 주요 의도에 맞는 스펙을 생성하고 충돌하는 부분은 생략
- 두 가지 모순된 요구사항을 동시에 만족시키려 하지 않음

### 7.5 엔티티 추론 실패

1단계(엔티티 추론)의 결과가 저신뢰도일 때:

```
IF 모든 엔티티의 confidence < 0.6:
    초안 Entity Spec을 그대로 출력 (SUIS 생성으로 진행하지 않음)
    진행 전 사용자 확인이 필요하다는 신호 반환
ELSE:
    사용 가능한 엔티티로 2단계 진행
    confidence < 0.5인 엔티티는 SUIS 생성에서 제외
```

---

## 부록 A: 공통 패턴

### A.1 목록 + 편집 (가장 일반적)

```
엔티티: order
화면: order_browse (collection) + order_edit (single)
패턴: browse에서 search/create/edit/delete → edit에서 submit/back
네비게이션: browse → edit (modal 또는 full)
```

### A.2 마스터/디테일

```
엔티티: department (마스터) → employee (디테일)
화면: department_browse + department_view (employee collection 내장)
패턴: department_view의 primary: single (부서 필드) + secondary: collection (사원 필드)
```

### A.3 대시보드

```
엔티티: order
화면: order_dashboard
패턴: primary: summary (KPI) + secondary: collection (최근 주문)
작업: search, export, browse로 이동
```

### A.4 위자드 (다단계)

```
엔티티: application
화면: application_wizard
패턴: purpose: wizard, 단계를 나타내는 다수의 display 섹션
작업: 마지막 단계에서 submit, 이전 화면으로 네비게이션
```

### A.5 읽기 전용 조회

```
엔티티: audit_log
화면: audit_browse
패턴: 필터가 있는 collection 표시, create/edit/delete 작업 없음
작업: search, export만 가능
```

---

## 부록 B: 한국어 비즈니스 도메인 용어 (예시)

아래 표는 일반적인 한국어 비즈니스 용어가 엔티티/속성 이름에 매핑되는 **대표적인 예시**입니다. 이것은 전체 사전이 아닙니다 — 여기에 없는 용어는 같은 snake_case 영어 명명 규칙을 사용하여 추론하세요.

| 한국어 | 엔티티/속성 | 타입 |
|--------|------------|------|
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
| 분류, 카테고리 | category | entity 또는 enum |
| 등록일 | created_at | datetime |
| 수정일 | updated_at | datetime |
| 목록 | browse 화면 | purpose |
| 등록/편집 | create/edit 화면 | purpose |
| 상세 | view 화면 | purpose |
| 대시보드 | dashboard 화면 | purpose |
| 검색 | search 작업 | intent |
| 삭제 | delete 작업 | intent |
| 저장 | submit 작업 | intent |
| 승인 | approve 작업 | intent |
| 반려 | reject 작업 | intent |

> **참고**: 도메인 특화 용어(예: 결재선 → approval_line, 품의서 → expenditure_request)는 문맥에서 추론해야 합니다. 이 표와의 일치보다 단일 프로젝트 내에서의 일관성이 더 중요합니다.

---

*문서 버전: 1.1*
*최종 수정일: 2026-02-04*
