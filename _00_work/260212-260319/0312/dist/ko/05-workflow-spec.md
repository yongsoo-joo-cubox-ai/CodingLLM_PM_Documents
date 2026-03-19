[홈](README.md) | [← SUIS](04-suis-spec.md) | [용어집](glossary.md)

# Workflow Spec — 상태 기계

> 비즈니스 프로세스를 통해 엔티티가 어떻게 이동하는지 — 승인, 수명주기, 에스컬레이션 — 명시적인 상태, 전이, 규칙으로 정의합니다.

---

## Workflow Spec이란?

Workflow Spec은 비즈니스 프로세스를 위한 상태 기계(State Machine)를 정의합니다. 승인 흐름, 주문 수명주기, 업무 진행 — 엔티티가 정의된 상태를 통해 이동하면서 누가 무엇을 언제 할 수 있는지에 대한 규칙이 존재하는 모든 프로세스를 기술합니다.

YAML 파일에 엔티티가 가질 수 있는 상태, 상태 간의 전이, 각 전이의 조건과 부수 효과를 선언합니다. 준거 컴파일러가 이를 읽고 대상 플랫폼에 맞는 상태 관리 로직, 권한 확인, 알림 트리거, 감사 로깅을 생성합니다.

지금까지 만들어 온 모든 "상태" 드롭다운의 설계도라고 생각하면 됩니다. 다만 규칙이 컨트롤러, 서비스, 미들웨어에 흩어져 있는 대신, 하나의 선언적 문서에 모여 있습니다.

---

## 언제 필요한가?

모든 엔티티에 워크플로가 필요하지는 않습니다. `name`과 `code`만 가진 `Country` 엔티티에는 필요 없습니다. 하지만 초안 작성, 검토, 승인, 이행을 거치는 `PurchaseOrder`에는 반드시 필요합니다.

다음과 같은 경우에 Workflow Spec을 사용합니다:

- **레코드가 승인 단계를 거칠 때** — 문서, 요청, 주문 등이 효력을 발휘하기 전에 결재가 필요한 경우.
- **상태 변경에 규칙이 있을 때** — 관리자만 승인할 수 있고, 작성자만 재제출할 수 있으며, 확정 후에는 아무도 편집할 수 없는 경우.
- **전이가 부수 효과를 발생시킬 때** — 제출 시 알림 전송, 승인 시 타임스탬프 기록, 반려 시 웹훅 발생 등.
- **상태 변경의 감사 추적이 필요할 때** — 누가 이것을 "대기"에서 "승인"으로 이동시켰고, 언제였는지?

엔티티에 단순한 `active` boolean 플래그만 있다면 전체 워크플로는 필요 없습니다. 하지만 3개 이상의 값을 가진 `status` 필드가 있고 값들 사이의 이동 규칙이 있다면, 필요합니다.

---

## 문서 구조

Workflow Spec 파일은 최상위 `workflow` 키를 가진 YAML입니다:

```yaml
workflow:
  version: "1.0"
  name: purchase_order_approval
  entity: PurchaseOrder         # Entity Spec의 엔티티 참조
  status_field: status          # 현재 상태를 보관하는 enum 속성
  states:
    # ...
  transitions:
    # ...
```

**필수 필드:**

| 필드 | 설명 |
|------|------|
| `version` | 이 스펙 버전에서는 항상 `"1.0"` |
| `entity` | Entity Spec에 정의된 엔티티 이름 |
| `status_field` | 해당 엔티티의 enum 속성 이름 |
| `states` | 상태 정의 맵 |
| `transitions` | 전이 정의 목록 |

**선택 필드:**

| 필드 | 설명 |
|------|------|
| `name` | 사람이 읽을 수 있는 워크플로 이름 |
| `description` | 이 워크플로가 관리하는 대상 |

`entity`는 Entity Spec의 엔티티를 참조합니다. `status_field`는 해당 엔티티의 enum 속성 이름입니다. `states`에 정의하는 상태 이름은 Entity Spec에 정의된 enum 값과 일치해야 합니다 — 이것이 두 스펙의 동기화 방식입니다.

---

## 상태(States)

`states` 아래 각 키는 상태 이름이며, 각 상태는 `type`을 가집니다:

| 유형 | 의미 | 규칙 |
|------|------|------|
| `initial` | 시작점 — 새 레코드가 시작되는 곳 | 워크플로당 정확히 1개 |
| `normal` | 중간 상태 — 엔티티가 작업 중인 상태 | 0개 이상 |
| `final` | 종료 상태 — 이후 전이가 불가능 | 최소 1개 |

워크플로에는 정확히 하나의 `initial` 상태와 최소 하나의 `final` 상태가 있어야 합니다. `normal` 상태는 프로세스에 필요한 만큼 가질 수 있습니다.

### 상태 속성

`type` 외에 상태는 다음 선택 속성을 지원합니다:

| 속성 | 타입 | 용도 |
|------|------|------|
| `label` | string | UI 표시용 이름 |
| `description` | string | 프로세스에서 이 상태의 의미 |
| `on_enter` | 액션 목록 | 이 상태에 진입할 때의 부수 효과 |
| `on_exit` | 액션 목록 | 이 상태에서 퇴장할 때의 부수 효과 |
| `permissions` | 맵 | 이 상태에서 누가 엔티티를 조회/편집할 수 있는지 |

### 예제

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

`pending`과 `approved` 모두 `edit: []`입니다 — 이 상태에서는 아무도 엔티티를 수정할 수 없습니다. 검토 중과 승인 후에는 레코드가 잠깁니다. 반면 `rejected`는 `author`에게 편집을 허용합니다. 수정 후 재제출이 필요하기 때문입니다.

---

## 전이(Transitions)

전이는 상태 간의 방향성 있는 간선입니다. 엔티티가 한 상태에서 다른 상태로 어떻게, 언제 이동하는지 정의합니다.

위의 상태 예제로 구성한 승인 워크플로를 ASCII 다이어그램으로 그리면 다음과 같습니다:

```
                                 +--approve--> [approved]
                                 |
[draft] --submit--> [pending] ---+
                                 |
                                 +--reject---> [rejected] --revise--> [draft]
```

엔티티는 `draft`에서 시작합니다. 작성자가 제출하면 `pending`으로 이동합니다. 이후 승인자가 승인하면(`approved` 최종 상태로 이동) 또는 반려하면(`rejected`로 이동) 됩니다. 반려된 경우 작성자가 수정하여 재제출할 수 있으며, `draft`로 되돌아갑니다.

### 전이 속성

각 전이는 `transitions` 목록의 객체입니다:

| 속성 | 필수 | 타입 | 용도 |
|------|------|------|------|
| `event` | 예 | string | 트리거 이름 — 사용자가 수행하는 "행위" |
| `from` | 예 | string | 출발 상태 |
| `to` | 예 | string | 도착 상태 |
| `guard` | 아니오 | object | 참이어야 하는 조건 |
| `action` | 아니오 | list | 이 전이의 부수 효과 |
| `allowed_roles` | 아니오 | 문자열 목록 | 이 전이를 발동할 수 있는 역할 |
| `requires_comment` | 아니오 | boolean | 사유를 입력해야 하는지 여부 |

### 예제

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

`submit` 전이에는 가드가 있습니다 — 제목이 없거나 금액이 양수가 아니면 구매 주문을 제출할 수 없습니다. `reject` 전이는 코멘트를 요구합니다 — 승인자가 반려 사유를 설명해야 합니다. `approve` 전이는 코멘트를 요구하지 않지만, 승인자가 원하면 남길 수 있습니다.

---

## 가드 조건(Guards)

가드는 전이가 발생하기 위해 참이어야 하는 조건입니다. 사용자가 올바른 역할을 가지고 있고 엔티티가 올바른 상태에 있더라도, 가드가 실패하면 전이는 차단됩니다.

### 단순 가드

단일 필드를 확인합니다:

```yaml
guard:
  field: title
  operator: not_empty
```

### 복합 가드 (AND)

모든 조건이 참이어야 합니다:

```yaml
guard:
  all:
    - field: title
      operator: not_empty
    - field: amount
      operator: gt
      value: 0
```

### 복합 가드 (OR)

최소 하나의 조건이 참이면 됩니다:

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

### 중첩

더 복잡한 로직을 위해 `all`과 `any`를 중첩할 수 있습니다:

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

이것은 "제목이 비어있지 않아야 하고 AND (우선순위가 high이거나 OR 금액이 10,000 이상)"으로 읽힙니다.

### 연산자

| 연산자 | 의미 | `value` 필요? |
|--------|------|:-------------:|
| `eq` | 같음 | 예 |
| `ne` | 같지 않음 | 예 |
| `gt` | 보다 큼 | 예 |
| `gte` | 보다 크거나 같음 | 예 |
| `lt` | 보다 작음 | 예 |
| `lte` | 보다 작거나 같음 | 예 |
| `contains` | 문자열/배열에 포함 | 예 |
| `in` | 값이 목록에 포함 | 예 |
| `not_empty` | 필드가 존재하고 비어있지 않음 | 아니오 |
| `is_empty` | 필드가 없거나 비어있음 | 아니오 |

`in` 연산자의 경우 `value`는 배열입니다:

```yaml
guard:
  field: category
  operator: in
  value: [electronics, software, services]
```

---

## 액션(Actions)

액션은 상태 진입, 퇴장, 전이 시 실행되는 부수 효과입니다. 상태 자체를 변경하지는 않으며, 상태 변경과 함께 발생하는 작업입니다.

### 사용 가능한 액션

| 액션 | 기능 | 주요 파라미터 |
|------|------|---------------|
| `notify` | 앱 내 알림 전송 | `role: approver` |
| `email` | 이메일 전송 | `to: author, template: approved` |
| `log` | 감사 로그 항목 기록 | `level: info` |
| `webhook` | HTTP 엔드포인트 호출 | `url: ..., method: POST` |
| `set_field` | 엔티티 필드 값 업데이트 | `field: approved_at, value: $now` |

### 액션이 위치하는 곳

액션은 세 곳에 배치할 수 있습니다:

**상태 진입 시** — 어떤 전이로 도착했는지와 관계없이, 이 상태에 진입하면 실행됩니다:

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

**상태 퇴장 시** — 어디로 이동하는지와 관계없이, 이 상태를 떠나면 실행됩니다:

```yaml
states:
  draft:
    type: initial
    on_exit:
      - action: log
        params: { level: info }
```

**전이 시** — 특정 전이에서만 실행됩니다:

```yaml
transitions:
  - event: reject
    from: pending
    to: rejected
    action:
      - action: log
        params: { level: warn }
```

상태의 `on_enter`와 전이의 `action`이 모두 해당되는 경우, 전이 액션이 먼저 실행되고 이어서 도착 상태의 `on_enter` 액션이 실행됩니다.

### 변수

액션은 다음 내장 변수를 지원합니다:

| 변수 | 값 |
|------|-----|
| `$now` | 현재 타임스탬프 (ISO 8601) |

---

## 상태별 권한

각 상태는 해당 상태에서 누가 엔티티를 조회하고 편집할 수 있는지 선언할 수 있습니다. 워크플로를 통해 이동하는 레코드에 대해 세밀한 접근 제어를 제공합니다.

```yaml
permissions:
  view: [author, approver, admin]
  edit: [author]
```

- **`view`** — 이 상태에서 레코드를 볼 수 있는 역할.
- **`edit`** — 이 상태에서 레코드를 수정할 수 있는 역할. 빈 목록 `[]`은 레코드가 잠김 상태임을 의미합니다 — 아무도 편집할 수 없습니다.

이것은 전이 권한(`allowed_roles`)과 다릅니다. 상태 권한은 레코드를 누가 보고 수정할 수 있는지를 제어합니다. 전이 권한은 상태 변경을 누가 발동할 수 있는지를 제어합니다. 보통 둘 다 필요합니다: 승인자는 대기 중인 레코드를 조회할 수 있고(상태 권한) 승인 전이를 발동할 수 있지만(전이 권한), 대기 상태에서 레코드의 필드를 편집할 수는 없습니다.

---

## 전체 예제

모든 것을 통합한 완전한 구매 주문 승인 워크플로입니다:

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

이 워크플로의 상태 다이어그램입니다:

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

주목할 점:

- `submit` 가드는 주문에 제목, 항목, 양수 합계가 있는지 확인합니다. 빈 주문은 제출할 수 없습니다.
- `approve` 가드는 단일 관리자 승인을 50,000 이하로 제한합니다. 그 이상의 주문에는 다른 워크플로(또는 에스컬레이션이 추가된 확장 워크플로)가 필요합니다.
- `reject`는 코멘트를 요구합니다 — 관리자가 반려 사유를 설명해야 합니다.
- `cancel` 이벤트가 두 번 나타납니다 — `draft` 또는 `rejected`에서 취소할 수 있지만, `pending_review`나 `approved`에서는 불가능합니다. 같은 이벤트 이름, 다른 출발 상태입니다.
- 주문이 승인되면 이행 시스템으로 웹훅이 발생합니다. 이것이 워크플로가 하류 프로세스와 통합되는 방식입니다.
- `approved`와 `cancelled` 모두 `final` 상태입니다 — 일단 도달하면 더 이상 전이할 수 없습니다.

---

## Workflow의 연결 관계

Workflow Spec은 독립적으로 존재하지 않습니다. 다른 UASL 스펙을 참조하고 또 참조됩니다:

**Entity Spec** — `entity` 필드는 Entity Spec에 정의된 엔티티를 참조합니다. `status_field`는 해당 엔티티의 enum 속성 이름입니다. 상태 이름은 enum 값과 일치해야 합니다. Entity Spec에 다음과 같이 정의되어 있다면:

```yaml
attributes:
  status:
    type: enum
    values: [draft, pending_review, approved, rejected, cancelled]
```

Workflow Spec의 상태는 정확히 같은 이름을 사용해야 합니다.

**SUIS** — Semantic UI Spec에서 `intent: approve` 또는 `intent: reject`와 같은 intent 유형으로 워크플로 전이를 참조할 수 있습니다. SUIS는 워크플로 규칙을 알 필요가 없습니다 — intent만 선언하면 컴파일러가 모든 가드와 권한을 포함한 적절한 전이에 연결합니다.

**IAS** — Intent API Specification이 워크플로 이벤트를 HTTP 엔드포인트에 매핑합니다. `submit` 이벤트는 `POST /api/purchase-orders/{id}/submit`이 될 수 있습니다. IAS가 계약을 정의하고, 워크플로가 그 뒤의 비즈니스 규칙을 정의합니다.

네 개의 스펙이 함께 전체 그림을 기술합니다: 데이터가 어떤 모습인지(Entity), 사용자가 어떻게 상호작용하는지(SUIS), API가 어떤 형태인지(IAS), 그리고 비즈니스 프로세스가 어떻게 흐르는지(Workflow).

---

[← SUIS](04-suis-spec.md) | [용어집](glossary.md) | [홈](README.md)

*Workflow Spec v1.0 — 2026-01-29*
