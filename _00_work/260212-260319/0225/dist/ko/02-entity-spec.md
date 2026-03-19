[홈](README.md) | [← 개요](01-overview.md) | [다음: IAS →](03-ias-spec.md)

---

# Entity Spec — 도메인 모델

Entity Spec은 도메인 모델을 정의합니다. 엔티티(Entity), 속성(Attribute), 관계(Relation) — 애플리케이션을 구성하는 데이터의 구조를 기술하는 사양입니다. UASL의 기반이 되며, 다른 모든 사양이 이것을 참조합니다. 애플리케이션의 데이터 사전(Data Dictionary)을 기계가 읽을 수 있는 형식으로 작성한 것이라고 생각하면 됩니다.

SUIS는 `task`에 어떤 필드가 있는지 알아야 합니다. IAS는 리소스가 어떤 엔티티에 매핑되는지 알아야 합니다. Workflow는 어떤 enum 필드가 상태 머신을 구동하는지 알아야 합니다. 이 모든 것을 Entity Spec에서 찾습니다. Entity Spec을 먼저 작성하면, 나머지는 자연스럽게 따라옵니다.

---

## 문서 구조

Entity Spec은 두 개의 최상위 키(Top-Level Key)를 포함하는 YAML 문서입니다.

```yaml
entity_version: "1.0"

entities:
  task:
    # ...
  user:
    # ...
```

`entity_version`은 작성 대상 사양의 버전을 도구(Tooling)에 알려줍니다. 현재 유효한 값은 `"1.0"`뿐입니다.

`entities`는 맵(Map) 형태로, 각 키는 엔티티 이름(`snake_case` 사용)이고, 값은 해당 엔티티의 정의입니다. 최소 하나의 엔티티가 필요하지만, 실제 사양에는 대부분 여러 개가 포함됩니다.

---

## 엔티티

각 엔티티는 도메인 객체(Domain Object)를 나타냅니다 — Task, User, Order, Department 등 애플리케이션이 다루는 대상입니다.

모든 엔티티에는 반드시 두 가지가 필요합니다: `primary_key`와 `attributes`. 나머지는 모두 선택 사항입니다.

```yaml
entities:
  task:
    label: Task                   # 선택, 사람이 읽을 수 있는 이름
    primary_key: id               # 필수, 속성 이름과 일치해야 함
    meta: { ... }                 # 선택, 출처 추적 정보
    attributes: { ... }          # 필수, 최소 하나 이상
    relations: { ... }           # 선택
    computed: { ... }            # 선택
    display: { ... }            # 선택, 표시 힌트
```

`primary_key` 값은 `attributes` 블록에 정의된 속성 이름 중 하나여야 합니다. 예를 들어, 기본 키가 `id`라면 `attributes` 블록에 `id`라는 속성이 있어야 합니다.

기본 키 속성의 타입은 일반적으로 `uuid` 또는 `integer`입니다. 분산 시스템, 마이크로서비스, 또는 특별한 타입 요구가 없는 경우에는 `uuid`를 사용합니다. 레거시 데이터베이스, JPA/Hibernate 자동 증가(auto-increment) 패턴, 또는 사용자가 순차적 ID를 명시적으로 요청한 경우에는 `integer`를 사용합니다. 두 가지 모두 유효하며, 애플리케이션 맥락에 따라 선택합니다. 기본 키를 참조하는 외래 키 속성은 대상 엔티티의 기본 키 타입과 일치해야 합니다.

`label`은 생성된 UI, 오류 메시지, 문서에서 사용할 수 있는 사람 친화적인 이름입니다. 생략하면 도구가 엔티티 이름으로부터 자동으로 유도합니다.

---

## 속성(Attributes)

모든 속성에는 `type`이 필수입니다. 이것만 있으면 됩니다. `required`, `unique`, `default`, `label`, `constraints` 등은 모두 선택 사항이며, 표현하려는 내용에 따라 사용합니다.

```yaml
attributes:
  title:
    type: string
    required: true
    label: "Title"
    constraints:
      max_length: 200
```

### 사용 가능한 타입

| 타입 | 설명 | 주요 제약 조건 |
|------|------|---------------|
| `string` | 짧은 텍스트 (이름, 제목, 코드 등) | `max_length`, `min_length`, `pattern` |
| `text` | 긴 텍스트 (설명, 메모, 본문 등) | `max_length` |
| `integer` | 정수 (건수, 수량 등) | `min`, `max` |
| `decimal` | 정밀 소수점 수 (측정값, 비율 등) | `precision`, `scale` |
| `currency` | 금액 (가격, 합계, 잔액 등) | `precision`, `scale` |
| `boolean` | 참/거짓 | — |
| `date` | 날짜 (시간 미포함) | — |
| `datetime` | 날짜와 시간 | — |
| `uuid` | UUID 식별자 | — |
| `enum` | 고정된 값 집합에서 하나를 선택 | `values` (필수) |

`string`과 `text`의 차이는 의미론적(Semantic)입니다. `string`은 사람 이름 같은 짧은 값에 사용하고, `text`는 설명이나 댓글 본문 같은 긴 내용에 사용합니다. 도구는 이 구분을 활용하여 적절한 입력 위젯을 선택합니다 (텍스트 필드 vs. 텍스트 영역).

`currency`는 `decimal`의 특수한 형태입니다. 기술적으로는 동일하게 동작하지만, `currency`로 선언하면 이 필드가 금액을 나타낸다는 것을 하위 사양에 알려줍니다.

`enum`의 경우, `values` 목록을 반드시 제공해야 합니다:

```yaml
status:
  type: enum
  values: [draft, pending, approved, rejected]
  default: draft
```

### 비-Enum 타입의 Values

`string` 또는 `integer` 속성에도 `values`를 사용할 수 있습니다. 이것은 저장 타입을 변경하지 않습니다 -- 필드는 여전히 데이터베이스에 문자열이나 정수로 저장됩니다. 대신 코드 생성기에게 자유 텍스트 입력 대신 드롭다운/선택 컨트롤을 렌더링하라고 알려줍니다.

```yaml
priority:
  type: string
  values: [low, medium, high, critical]
  default: medium
```

이것은 일반 문자열로 저장되지만 고정된 값 집합만 허용하는 필드에 유용합니다. `enum`과의 차이는 의미론적입니다: `enum`은 타입 수준의 제약이고, `string` + `values`는 필드를 드롭다운으로 표시해야 한다는 UI 수준의 힌트입니다.

`values`가 단순 문자열 배열인 경우, 각 값은 코드와 라벨 모두로 취급됩니다. 사람이 읽을 수 있는 라벨은 Domain Graph에서 별도로 관리되며, 엔진이 주입합니다 -- Entity Spec 자체에는 포함되지 않습니다.

### 속성 옵션

| 옵션 | 설명 |
|------|------|
| `required` | 값이 반드시 있어야 합니다. 빈 값은 허용되지 않습니다. |
| `unique` | 같은 값을 가진 레코드가 두 개 이상 존재할 수 없습니다. |
| `readonly` | 생성 후에는 변경할 수 없습니다. 타임스탬프나 감사(Audit) 필드에 적합합니다. |
| `default` | 값이 제공되지 않을 때 사용할 기본값입니다. 리터럴 값 또는 현재 시각을 나타내는 특수 문자열 `"now()"`를 사용할 수 있습니다. |
| `label` | 생성된 UI와 문서에 표시할 사람이 읽을 수 있는 이름입니다. |
| `constraints` | `max_length`, `min`, `max`, `pattern`, `precision`, `scale` 등의 유효성 검사 규칙입니다. |

제약 조건은 타입에 따라 다릅니다. `integer`에 `max_length`를 지정하는 것은 의미가 없으며, 도구가 이를 알려줍니다.

---

## 관계(Relations)

관계는 엔티티 간의 연결 방식을 기술합니다. 네 가지 유형이 있으며, 각 유형은 하위 단계에서 서로 다른 UI 및 API 패턴을 활성화합니다.

### many_to_one (다대일)

가장 흔한 관계입니다. "각 태스크(Task)에는 담당자(User)가 한 명 있지만, 한 사용자(User)는 여러 태스크를 담당할 수 있다."

```yaml
# task 엔티티에 정의
relations:
  assignee:
    type: many_to_one
    target: user
    foreign_key: assignee_id     # task에 있는 FK 속성
    display_field: name           # 드롭다운에 표시할 user의 필드
    nullable: true
    on_delete: set_null
```

`foreign_key`는 필수이며, 현재 엔티티에 정의된 속성 이름이어야 합니다 (이 경우 `task`의 `assignee_id`). `display_field`는 *대상(Target)* 엔티티의 속성 이름으로, 관계를 렌더링할 때 UI에 무엇을 표시할지 알려줍니다 (예: 원시 UUID 대신 사용자의 `name`을 드롭다운에 표시).

생성된 UI에서 `many_to_one` 관계는 일반적으로 드롭다운(Dropdown) 또는 검색 선택(Search-Select) 컴포넌트가 됩니다. 옵션은 대상 엔티티의 레코드에서 채워지며, `display_field` 값이 옵션 라벨로 표시됩니다.

### one_to_many (일대다)

`many_to_one`의 역방향입니다. "한 사용자(User)는 여러 태스크(Task)를 가진다."

```yaml
# user 엔티티에 정의
relations:
  tasks:
    type: one_to_many
    target: task
    mapped_by: assignee           # 대상 엔티티에 정의된 관계 이름
```

`mapped_by`는 필수이며, 대상 엔티티에 정의된 관계 이름이어야 합니다. 이 관계가 어떤 `many_to_one`의 반대편인지 시스템에 알려줍니다.

생성된 UI에서 `one_to_many` 관계는 일반적으로 마스터/디테일(Master/Detail) 뷰를 생성합니다 — 사용자를 클릭하면 아래에 해당 사용자의 태스크 목록이 표시됩니다.

### one_to_one (일대일)

엄격한 1:1 매핑입니다. "각 사용자(User)는 정확히 하나의 프로필(Profile)을 가진다."

```yaml
# user 엔티티에 정의
relations:
  profile:
    type: one_to_one
    target: profile
```

### many_to_many (다대다)

양쪽 모두 여러 개를 가질 수 있습니다. "하나의 태스크(Task)에 여러 태그(Tag)가 있을 수 있고, 하나의 태그(Tag)가 여러 태스크에 붙을 수 있다."

```yaml
# task 엔티티에 정의
relations:
  tags:
    type: many_to_many
    target: tag
    join_table: task_tags          # many_to_many에 필수
```

`join_table`은 필수이며, 중간 테이블(Intermediate Table)의 이름입니다. 중간 테이블의 컬럼 이름이 관례를 따르지 않는 경우, `join_columns`를 선택적으로 지정할 수 있습니다:

```yaml
    join_columns:
      source: task_id
      target: tag_id
```

### 관계 옵션 참조표

| 옵션 | 설명 |
|------|------|
| `target` | 관계가 가리키는 엔티티입니다. 모든 관계 유형에 필수입니다. |
| `foreign_key` | 현재 엔티티에 있는 FK 속성 이름입니다. `many_to_one`에 필수입니다. |
| `display_field` | 대상 엔티티에서 표시에 사용할 속성입니다 — 드롭다운 라벨, 그리드 컬럼 등에 활용됩니다. |
| `nullable` | FK가 null일 수 있는지 여부입니다 (관계가 선택 사항인 경우). |
| `on_delete` | 대상 레코드가 삭제될 때의 동작입니다: `cascade` (함께 삭제), `restrict` (삭제 차단), `set_null` (FK를 null로 설정). |
| `mapped_by` | 대상 엔티티에 있는 역방향 관계 이름입니다. `one_to_many`에 필수입니다. |
| `join_table` | 중간 테이블 이름입니다. `many_to_many`에 필수입니다. |

### 관계가 활성화하는 기능

관계는 단순한 문서화가 아닙니다. 생성된 코드에서 구체적인 동작을 결정합니다:

- **드롭다운(Dropdown)**은 `many_to_one` + `display_field`에서 만들어집니다. UI가 대상 엔티티의 레코드를 가져와서 display field 값을 옵션 라벨로 표시합니다.
- **마스터/디테일(Master/Detail) 뷰**는 `one_to_many`에서 만들어집니다. 상위 행을 클릭하면 하위 컬렉션이 아래에 표시됩니다.
- **다중 선택(Multi-Select) 또는 태그 입력**은 `many_to_many`에서 만들어집니다. UI가 양쪽에서 여러 항목을 연결할 수 있는 방법을 제공합니다.
- **그리드의 조인 컬럼(Joined Column)**은 `many_to_one` + `display_field`에서 만들어집니다. 원시 외래 키 대신 관련 엔티티의 표시 값이 그리드에 나타납니다.

---

## 계산 필드(Computed Fields)

계산 필드는 수식(Expression)으로부터 도출되는 값입니다. 항상 readonly이며, 사용자가 직접 편집할 수 없습니다.

```yaml
computed:
  full_name:
    expression: "first_name || ' ' || last_name"
    type: string
    readonly: true
```

`expression`은 동일 엔티티의 다른 속성을 참조하는 문자열 수식입니다. `type`은 하위 도구에 어떤 종류의 값을 기대해야 하는지 알려줍니다.

계산 필드는 SUIS의 표시 블록(Display Block)에서 일반 필드처럼 사용할 수 있지만, 편집기에서는 항상 읽기 전용으로 렌더링됩니다.

---

## 표시 힌트(Display Hints)

표시 힌트는 엔티티의 기본 표시 방식에 대한 선택적 의미론적 제안입니다. 레이아웃 지시(Layout Instruction)가 아닙니다 — 어댑터(Adapter)는 이를 다르게 해석하거나 무시할 수 있습니다. 그러나 생성된 UI가 별도 설정 없이도 잘 동작하도록 유용한 기본값을 제공합니다.

```yaml
display:
  default_sort: created_at desc
  default_fields: [title, status, assignee, due_date]
  search_fields: [title, description]
```

| 힌트 | 설명 |
|------|------|
| `default_sort` | 목록 뷰의 기본 정렬 순서입니다. 형식: `필드명 asc` 또는 `필드명 desc`. |
| `default_fields` | 목록/그리드 뷰에 기본으로 표시할 필드 목록입니다. SUIS 화면에서 재정의할 수 있지만, 지정하지 않으면 이 값이 사용됩니다. |
| `search_fields` | 사용자가 텍스트 검색을 수행할 때 포함할 필드 목록입니다. |

표시 힌트는 SUIS 화면에서 일일이 상세하게 기술해야 하는 양을 줄여줍니다. 엔티티에 `default_fields: [title, status, assignee]`를 정의하면, 필드 목록을 명시하지 않은 SUIS 검색 화면은 이 기본값을 사용할 수 있습니다.

---

## 출처 추적(Source Tracking)

`meta` 블록은 엔티티 정의의 출처를 추적합니다. Entity Spec은 다양한 방식으로 작성될 수 있기 때문에 이것이 중요합니다 — 수작업으로 작성하거나, 데이터베이스에서 기계적으로 추출하거나, AI가 추론하거나, OpenAPI 정의에서 파생할 수 있습니다.

```yaml
meta:
  source: db               # 데이터베이스 스키마에서 기계적으로 추출
```

네 가지 source 값:

| Source | 의미 |
|--------|------|
| `db` | 기존 데이터베이스 스키마(SQL, Prisma 등)에서 추출 |
| `inferred` | 자연어 또는 부분적 요구사항으로부터 AI/LLM이 생성 |
| `openapi` | OpenAPI/Swagger 정의에서 파생 |
| `manual` | 사람이 직접 작성 |

`inferred`로 표시된 엔티티에는 0에서 1 사이의 `confidence` 점수를 포함해야 합니다:

```yaml
meta:
  source: inferred
  confidence: 0.85
```

confidence 점수는 추론 엔진이 해당 엔티티 정의에 대해 얼마나 확신하는지를 도구와 검토자에게 알려줍니다. 신뢰도가 낮은 엔티티는 코드 생성에 사용하기 전에 더 신중한 검토가 필요합니다.

권위 있는 출처(`db`, `openapi`)와 수작업으로 작성한 엔티티에는 confidence 점수가 필요하지 않습니다 — 이들은 정확한 기준(Ground Truth)으로 취급됩니다.

---

## 전체 예제

아래는 두 개의 엔티티, 엔티티 간 관계, 표시 힌트, 출처 추적을 포함한 태스크 관리 시스템의 실제적인 Entity Spec 예제입니다.

```yaml
# 태스크 관리 도메인 모델
entity_version: "1.0"

entities:
  task:
    label: Task
    primary_key: id

    meta:
      source: db                  # 기존 데이터베이스에서 추출

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
        values: [low, medium, high, critical]  # string + values -> 드롭다운으로 렌더링
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
        type: uuid                # assignee 관계를 위한 FK 컬럼

    relations:
      assignee:
        type: many_to_one
        target: user
        foreign_key: assignee_id  # 위의 속성을 가리킴
        display_field: name       # 드롭다운에 사용자 이름 표시
        nullable: true            # 미배정 태스크 허용
        on_delete: set_null       # 사용자 삭제 시 배정 해제

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
        type: one_to_many         # task.assignee의 역방향
        target: task
        mapped_by: assignee       # task에 정의된 관계 이름 참조

    display:
      default_sort: name asc
      default_fields: [name, email, department, active]
      search_fields: [name, email]
```

몇 가지 주목할 점:

- `task.assignee_id` 속성은 원시 FK 컬럼입니다. `task.assignee` 관계가 여기에 의미를 부여합니다 — 대상 엔티티, 표시 필드, 삭제 동작 등.
- `user.tasks`는 `task.assignee`의 역방향이며, `mapped_by`로 연결됩니다. 역방향에서는 FK 정보를 다시 기술할 필요가 없습니다.
- `is_overdue`는 계산 필드입니다. 다른 속성으로부터 도출되며 항상 readonly입니다. SUIS에서 일반 필드처럼 표시 블록에서 참조할 수 있습니다.
- 표시 힌트는 레이아웃을 강제하지 않으면서 합리적인 기본값을 제공합니다. SUIS 화면에서 이 중 어느 것이든 재정의할 수 있습니다.

---

## 다른 사양에서의 활용

Entity Spec은 기반 계층(Foundation Layer)입니다. 다른 세 가지 사양이 이를 참조하는 방식은 다음과 같습니다.

**SUIS**는 `subject.domain`을 통해 엔티티를 참조합니다. 화면이 `subject.domain: task`로 선언하면, 의미론적 검증기(Semantic Validator)가 `task` 엔티티를 조회하여 화면에서 사용된 모든 필드 이름이 실제로 속성이나 관계로 존재하는지 확인합니다. 이를 통해 오탈자나 오래된 참조가 코드 생성 단계까지 도달하는 것을 방지합니다.

**IAS**는 `resources[].entity`를 통해 엔티티를 참조합니다. IAS 리소스가 `entity: task`로 선언하면, 검증기가 해당 엔티티의 존재를 확인하고 속성 정의를 사용하여 필드 매핑의 유효성을 검사합니다.

**Workflow**는 엔티티와 해당 엔티티의 enum 필드에 바인딩됩니다. Workflow가 `entity: task`와 `status_field: status`로 선언하면, 검증기가 `task`에 `enum` 타입의 `status` 속성이 있는지 확인하고, Workflow의 상태 이름이 enum의 `values` 목록과 일치하는지 검증합니다.

세 가지 경우 모두 패턴은 동일합니다: 엔티티 이름을 선언하면, 검증기가 Entity Spec을 기준으로 이를 확인합니다. 엔티티나 필드가 존재하지 않으면, 잘못된 생성 결과물이 아닌 즉각적인 오류를 받게 됩니다.

---

[← 개요](01-overview.md) | [IAS →](03-ias-spec.md) | [용어집](glossary.md)

*Entity Spec v1.0 — 2026-02-25*
