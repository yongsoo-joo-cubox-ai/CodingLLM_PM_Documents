[홈](README.md) | [<- IAS](03-ias-spec.md) | [다음: Workflow ->](05-workflow-spec.md)

---

# SUIS -- 의미적 UI 사양 (Semantic UI Specification)

## SUIS란?

SUIS는 사용자 인터페이스를 **구현이 아닌 의도**로 기술합니다. "5개 컬럼의 그리드를 만들고 더블클릭 핸들러를 추가하라"가 아니라, "이 필드들로 업무 컬렉션을 표시하고, 사용자가 항목을 활성화하면 편집기를 열어라"라고 기술합니다. 프레임워크 어댑터가 이를 실제 렌더링으로 변환합니다.

SUIS를 시스템과의 대화라고 생각하면 됩니다. 사용자가 달성하고자 하는 것에 대해 기술합니다. 화면을 기술하고, 사용자가 볼 데이터를 기술하고, 수행할 수 있는 작업을 기술합니다. 그리드, 버튼, 입력 필드, 기타 프레임워크 수준의 개념은 절대 언급하지 않습니다. xframe5, Vue, React, 또는 전혀 다른 프레임워크를 대상으로 하는 어댑터가 그 모든 것을 처리합니다.

---

## 핵심 아이디어

SUIS는 사용자가 **하려는 것(WHAT)**을 기술하지, **UI가 어떻게 보이는지(HOW)**를 기술하지 않습니다.

동일한 SUIS 문서가 xframe5 화면, Vue 페이지, React 컴포넌트를 생성할 수 있습니다. SUIS는 프레임워크 개념을 전혀 언급하지 않기 때문입니다. "SBGrid"가 아니라 "업무 컬렉션"이라 말합니다. "행을 더블클릭"이 아니라 "사용자가 항목을 활성화"라고 말합니다. "POST /api/tasks"가 아니라 "제출"이라고 말합니다.

이 분리가 SUIS를 이식 가능하게 만드는 핵심입니다. 내일 대상 프레임워크를 변경하더라도 SUIS 문서는 단 한 줄도 수정할 필요가 없습니다.

---

## SUIS가 하지 않는 것 (명시적 비목표)

경계가 기능만큼이나 중요하므로, 이를 명시적으로 밝혀두겠습니다.

SUIS는 다음을 기술하지 **않습니다**:

| 제외 항목 | 이유 |
|-----------|------|
| 그리드 / DataSource / 위젯 | 어댑터 책임 -- 각 표시 블록에 적합한 컴포넌트를 어댑터가 선택 |
| API URL / HTTP 메서드 | IAS에서 도출 -- SUIS에 `/api/tasks`나 `GET`이 들어가면 안 됨 |
| 픽셀 위치 (x, y, width, height) | 레이아웃은 어댑터 담당 -- SUIS는 `width_hint: wide` 같은 의미적 힌트만 제공 |
| DOM 이벤트 (click, dblclick, onchange) | 의미적 트리거 사용 (아래에서 자세히 설명) |
| 위젯 이름 (Button, Input, SBGrid) | format + purpose 사용 -- 프레임워크 이름이 나오면 안 됨 |
| 프레임워크 고유 구문 | `v-model`, `SBGrid`, `useState` 등 일체 불가 |

SUIS 문서에 프레임워크 이름을 적고 있다면, 멈추세요. 경계를 넘은 것입니다.

---

## 문서 구조

SUIS 문서는 YAML 형식이며 최상위 `ui` 키를 가집니다. 내부에 두 가지 필드가 있습니다:

```yaml
ui:
  suis_version: "1.1"        # 필수 -- 항상 "1.1"

  screens:                     # 필수 -- 최소 하나의 화면
    task_browse: { ... }
    task_edit:   { ... }

  components:                  # 선택 -- 재사용 가능한 표시 블록
    task_summary: { ... }
```

- `suis_version`은 항상 `"1.1"`입니다. `"1.0"`이 보이면 업데이트하세요 -- v1.1에서 필드 힌트와 작업 피드백이 추가되었습니다.
- `screens`에 모든 화면이 정의됩니다. 각 키는 직접 지정하는 화면 ID입니다.
- `components`는 선택 사항입니다. 여러 화면이 동일한 표시 블록을 공유할 때 사용합니다.

---

## 화면(Screen)

각 화면은 **3가지 필수 요소**와 2가지 선택 요소로 구성됩니다:

```yaml
screens:
  task_browse:
    subject:      { ... }     # 주제 -- 어떤 엔티티이고 어떤 목적인지 (필수)
    display:      { ... }     # 표시 -- 어떤 데이터가 보이는지 (필수)
    operations:   [ ... ]     # 작업 -- 사용자가 수행할 수 있는 행동 (필수)
    navigation:   { ... }     # 내비게이션 -- 화면 간 연결 (선택)
    permissions:  { ... }     # 권한 -- 역할 기반 접근 (선택)
```

모든 화면은 세 가지 질문에 답합니다:
1. **이 화면은 무엇에 관한 것인가?** (subject)
2. **사용자가 무엇을 보는가?** (display)
3. **사용자가 무엇을 할 수 있는가?** (operations)

내비게이션과 권한은 필요할 때 사용하지만, 없어도 화면은 동작합니다.

---

## 주제(Subject) -- 의미적 앵커

`subject`는 이 화면이 어떤 엔티티를 대상으로 하며 왜 존재하는지를 시스템에 알려줍니다. 화면의 다른 모든 요소에 대한 의미적 앵커입니다.

```yaml
subject:
  domain: task                # Entity Spec의 엔티티를 참조
  purpose: browse             # 이 화면의 목적
  title: "Task Management"   # 사람이 읽을 수 있는 제목
  description: "View and manage all tasks"  # 선택 설명
```

`domain` 필드는 Entity Spec에 대한 직접 참조입니다. entity-spec.yaml에 `task`라는 엔티티가 있다면, 여기에 그 이름을 사용합니다. 엔티티가 존재하지 않으면 검증기가 문서를 거부합니다.

### 목적(Purpose)

`purpose` 필드는 화면의 존재 이유를 기술합니다:

| 목적 | 용도 |
|------|------|
| `browse` | 목록/검색 뷰 -- 여러 레코드를 표시 |
| `view` | 읽기 전용 상세 뷰 -- 편집 없이 하나의 레코드를 확인 |
| `create` | 새 레코드 생성 폼 -- 처음부터 새로 만들기 |
| `edit` | 기존 레코드 편집 폼 -- 기존 레코드 변경 |
| `dashboard` | 집계 요약 뷰 -- KPI, 차트, 개요 데이터 |
| `wizard` | 다단계 안내 프로세스 -- 1단계, 2단계, 3단계 순서대로 진행 |

이 화면에서 사용자가 달성하려는 것에 가장 부합하는 하나를 선택합니다.

---

## 표시 블록(Display Blocks)

`display` 섹션은 화면에 어떤 데이터가 나타나는지를 기술합니다. 필수인 `primary` 블록과 선택인 `secondary`, `filters` 섹션으로 구성됩니다.

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

### 블록 유형

3가지 표시 블록 유형이 있으며, 어댑터가 각각을 어떻게 렌더링할지 결정합니다:

| 유형 | 의미 | 어댑터가 렌더링하는 형태 |
|------|------|--------------------------|
| `collection` | 다중 레코드 | 그리드, 테이블, 카드 목록 -- 어댑터가 선택 |
| `single` | 단일 레코드 | 폼, 상세 뷰, 카드 -- 어댑터가 선택 |
| `summary` | 집계 데이터 | KPI 카드, 통계 바, 대시보드 타일 -- 어댑터가 선택 |

이 유형 중 어느 것도 특정 위젯을 언급하지 않습니다. `collection`은 xframe5에서 SBGrid가 될 수 있고, Vue에서 `el-table`이 될 수 있고, 순수 HTML에서 `<table>`이 될 수 있습니다. SUIS는 관여하지 않습니다.

---

## 필드(Fields)

표시 블록의 각 필드는 `name`으로 엔티티 속성을 참조합니다. 나머지는 모두 어댑터가 사용하거나 무시할 수 있는 선택적 힌트입니다.

```yaml
fields:
  - name: id                  # 필수 -- 엔티티 속성과 일치해야 함
    label: "ID"               # 표시 레이블
    format: integer            # 값 표시 형식
    width_hint: narrow         # 상대적 너비 제안
    align_hint: end            # 정렬 제안
    sortable: true             # 이 필드로 정렬 가능한가?
    editable: false            # 인라인 편집 가능한가?
    required: true             # 폼 제출 시 필수인가?
    visible: true              # 필드를 표시할 것인가? (기본값: true)
```

### 형식(Format)

`format`은 이 필드가 어떤 종류의 데이터를 담고 있는지 어댑터에게 알려줍니다:

| 형식 | 의미 |
|------|------|
| `text` | 문자열 -- 이름, 제목, 설명 |
| `integer` | 정수 -- ID, 건수, 수량 |
| `decimal` | 정밀 숫자 -- 측정값, 백분율 |
| `currency` | 금액 -- 가격, 합계, 잔액 |
| `date` | 시간 없는 날짜 -- 마감일, 생년월일 |
| `datetime` | 시간 포함 날짜 -- 타임스탬프, 생성일시 |
| `enum` | 고정 값 집합 -- 상태, 우선순위, 유형 |
| `boolean` | 참/거짓 -- 활성, 완료, 사용 여부 |

### 너비 힌트(Width Hint)와 정렬 힌트(Align Hint)

이것은 **의미적 힌트**이지 픽셀 값이 아닙니다. 어댑터가 자체 규약에 따라 해석합니다.

**너비 힌트** -- 이 필드가 원하는 수평 공간:

| 값 | 의미 |
|----|------|
| `narrow` | 최소 공간. ID, 상태 배지, 불리언 토글에 적합 |
| `medium` | 표준 컬럼 너비. 이름, 날짜, 짧은 텍스트 |
| `wide` | 넓은 공간 필요. 제목, 설명, 이메일 주소 |
| `fill` | 남은 공간 전부 사용. 긴 텍스트, 비고 |

**정렬 힌트** -- 콘텐츠가 공간 내 어디에 위치하는지:

| 값 | 일반적 용도 |
|----|-------------|
| `start` | 텍스트, 이름 (LTR 언어에서 왼쪽 정렬) |
| `center` | 상태 배지, 불리언 표시기 |
| `end` | 숫자, 금액, 날짜 (LTR 언어에서 오른쪽 정렬) |

핵심은 *힌트*라는 단어입니다. xframe5 어댑터는 `wide`를 300px로 매핑할 수 있습니다. Vue 어댑터는 `flex: 2`로 매핑할 수 있습니다. 모바일 어댑터는 이를 완전히 무시하고 모든 것을 수직으로 쌓을 수 있습니다. SUIS 문서는 어떤 경우든 동일하게 유지됩니다.

---

## 필터(Filters)

필터는 browse 및 search 화면에서 사용됩니다. 사용자가 어떤 기준으로 검색할 수 있는지를 정의합니다.

```yaml
filters:
  - field: status              # 필터링할 엔티티 속성
    operator: eq               # 비교 방법
    input: dropdown            # 어떤 종류의 입력을 표시할지
    options: ["pending", "in_progress", "completed"]

  - field: due_date
    operator: range
    input: date_range

  - field: title
    operator: contains
    input: text
```

### 연산자(Operators)

| 연산자 | 의미 |
|--------|------|
| `eq` | 같음 -- 정확히 일치 |
| `ne` | 같지 않음 -- 이 값을 제외 |
| `gt` | 보다 큼 |
| `lt` | 보다 작음 |
| `gte` | 크거나 같음 |
| `lte` | 작거나 같음 |
| `range` | 두 값 사이 (경계 포함) |
| `contains` | 문자열 포함 -- 부분 문자열 검색 |
| `in` | 집합 포함 -- 주어진 목록에 값이 포함됨 |

### 입력 유형(Input Types)

| 입력 | 사용자가 보는 것 |
|------|------------------|
| `text` | 자유 텍스트 입력 |
| `number` | 숫자 입력 |
| `date` | 단일 날짜 선택 |
| `date_range` | 시작일과 종료일 선택 |
| `dropdown` | 옵션 목록에서 선택 |
| `multi_select` | 목록에서 복수 선택 |

어댑터가 실제 위젯을 결정합니다. `dropdown`은 `<select>`가 될 수도 있고, 콤보 박스가 될 수도 있고, 검색 가능한 자동완성이 될 수도 있습니다. SUIS는 지정하지 않습니다.

---

## 작업(Operations) -- 사용자 의도

작업은 SUIS의 핵심입니다. 각 작업은 사용자가 이 화면에서 하고 싶은 것을 기술합니다.

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

### 의도(Intent)

모든 작업은 `intent`로 시작합니다 -- 사용자가 달성하고자 하는 것:

| 의도 | 사용자가 원하는 것 |
|------|---------------------|
| `browse` | 레코드 목록 보기 |
| `search` | 기준에 맞는 레코드 찾기 |
| `create` | 새로 만들기 |
| `edit` | 기존 레코드 변경하기 |
| `delete` | 삭제하기 |
| `submit` | 현재 폼 데이터 저장 |
| `approve` | 승인 (워크플로 작업) |
| `reject` | 반려 (워크플로 작업) |
| `export` | 시스템에서 데이터 내보내기 |
| `import` | 시스템으로 데이터 가져오기 |
| `custom` | 위 항목에 해당하지 않는 커스텀 작업 |

각 의도는 실제 HTTP 작업을 정의하는 IAS 의도에 매핑됩니다. SUIS는 `GET /api/tasks`를 알지도, 신경 쓰지도 않습니다. 단지 `intent: search`라고 말하면 IAS가 나머지를 처리합니다.

---

## 트리거(Triggers) -- 의미적이며 DOM이 아님

이것은 SUIS에서 가장 중요한 개념 중 하나이므로, 확실히 짚고 넘어가겠습니다.

트리거는 작업이 **어떻게 시작되는지**를 사용자 의도 관점에서 기술하며, **절대로 DOM 이벤트 관점에서 기술하지 않습니다**. 전체 목록과 함께, 절대로 쓰면 안 되는 것을 보여주는 컬럼을 추가합니다:

| 트리거 | 의미 | 이것이 아님 |
|--------|------|-------------|
| `activate_item` | 사용자가 이 항목과 상호작용하려 함 | ~~dblclick~~ |
| `select_item` | 사용자가 목록에서 항목을 선택 | ~~onclick~~ |
| `bulk_selection` | 사용자가 여러 항목을 선택하여 일괄 처리 | ~~checkbox~~ |
| `confirm_action` | 사용자가 명시적으로 작업을 확인 | ~~버튼 클릭~~ |
| `value_change` | 필드 값이 변경됨 | ~~onchange~~ |
| `automatic` | 페이지 로드 시 또는 타이머에 의해 자동 실행 | ~~DOMContentLoaded~~ |

왜 이것이 중요한가? 트리거는 **사용자 의도**를 기술하고, 어댑터가 이를 **프레임워크 이벤트**로 매핑하기 때문입니다. 동일한 트리거가 플랫폼마다 다른 코드를 생성합니다:

| SUIS 트리거 | xframe5 | Vue |
|-------------|---------|-----|
| `activate_item` | `row_double_click` | `@dblclick` |
| `select_item` | `row_click` | `@click` |
| `value_change` | `onchange` | `@change` / `v-model` |
| `confirm_action` | `button_click` | `@click` + confirm dialog |
| `bulk_selection` | `checkbox_select` | checkbox selection |

SUIS 문서는 변하지 않습니다. 어댑터가 변환을 담당합니다. SUIS 문서에 `dblclick`을 적었다면, 특정 이벤트 모델에 종속된 것입니다 -- xframe5 어댑터는 이를 어떻게 처리해야 할지 알 수 없을 것입니다.

---

## 작업 힌트(Operation Hints)

작업은 어댑터에게 결과 처리 방법을 알려주는 추가 힌트를 포함할 수 있습니다:

```yaml
operations:
  - intent: edit
    trigger: activate_item
    opens: task_edit                     # 이 화면으로 이동
    confirmation: "Edit this task?"      # 진행 전 확인 (delete는 필수)
    success_feedback: "Saved!"           # 성공 후 표시할 메시지
    post_action: close                   # 이후 행동: refresh, close, navigate
```

| 힌트 | 역할 |
|------|------|
| `opens` | 작업 실행 시 이동할 대상 화면 ID |
| `confirmation` | 실행 전 사용자에게 표시할 확인 메시지. `delete` 의도에는 **필수** |
| `success_feedback` | 성공적 완료 후 표시할 메시지 |
| `post_action` | 이후 행동: `refresh` (현재 화면 새로고침), `close` (현재 화면 닫기), `navigate` (다른 곳으로 이동) |

---

## 내비게이션(Navigation)

내비게이션은 화면 간의 연결을 정의합니다.

```yaml
navigation:
  to_editor:
    target: task_edit          # 화면 ID -- screens에 존재해야 함
    mode: modal                # "modal" 또는 "full" (기본값: full)
```

- `target`은 `screens` 섹션에 정의된 화면 ID입니다. 검증기가 존재 여부를 확인합니다.
- `mode`는 대상 화면이 어떻게 나타나는지를 제어합니다. `modal`은 오버레이로 열고, `full`은 현재 화면을 대체합니다. 기본값은 `full`입니다.

내비게이션은 작업의 `opens` 힌트와 함께 동작합니다. 작업에 `opens: task_edit`가 있으면, 어댑터는 내비게이션 섹션을 확인하여 모달로 열지 전체 페이지로 열지를 결정합니다.

---

## 권한(Permissions)

권한은 어떤 역할이 화면에 접근할 수 있는지를 선언합니다.

```yaml
permissions:
  roles: [admin, manager, user]
```

이것은 선언이지 강제가 아닙니다. SUIS는 어댑터에게 어떤 역할이 예상되는지를 알려줍니다. 런타임(백엔드, 인증 미들웨어)이 이를 강제합니다. 생성된 코드에 역할 검사, 조건부 버튼 가시성, 라우트 가드가 포함될 수 있지만, 그것은 어댑터의 판단입니다.

---

## 컴포넌트(Components)

컴포넌트는 여러 화면에서 공유할 수 있는 재사용 가능한 표시 블록입니다. 대시보드와 browse 화면 모두에 나타나는 KPI 요약이 있다면, 컴포넌트로 한 번만 정의합니다.

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

컴포넌트는 표시 블록과 동일한 구조(`type` + `fields`)를 사용합니다. 화면에서 필드 정의를 중복하는 대신 이를 참조할 수 있습니다.

---

## 전체 예제

browse 화면과 edit 화면을 포함하는 완전한 SUIS 문서입니다. 업무 관리 기능을 위해 작성하는 전형적인 형태입니다.

```yaml
ui:
  suis_version: "1.1"

  screens:
    # -------------------------------------------------------
    # Browse 화면: 업무 목록, 검색, 생성, 편집, 삭제
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

        # Browse 화면의 검색 필터
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
        # 검색: 목록 필터링
        - intent: search

        # 생성: 편집기를 열어 새 업무 작성
        - intent: create
          opens: task_edit

        # 편집: 행을 활성화하면 편집기 열기
        - intent: edit
          trigger: activate_item
          opens: task_edit

        # 삭제: 여러 항목 선택 후 확인
        - intent: delete
          trigger: bulk_selection
          confirmation: "Delete selected tasks?"

        # 내보내기: 현재 목록 다운로드
        - intent: export

      navigation:
        to_editor:
          target: task_edit
          mode: modal

      permissions:
        roles: [admin, manager, user]

    # -------------------------------------------------------
    # Edit 화면: 단일 업무 편집 또는 생성
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
        # 제출: 폼 저장 후 닫기
        - intent: submit
          success_feedback: "Task saved successfully"
          post_action: close

        # 돌아가기: browse 화면으로 복귀
        - intent: browse
          opens: task_browse

      permissions:
        roles: [admin, manager, user]
```

이 예제에서 주목할 점:

- SBGrid, el-table, v-model 등 어떤 위젯 이름도 언급되지 않습니다.
- URL, HTTP 메서드, fetch 호출이 없습니다 -- IAS가 그 모든 것을 처리합니다.
- `activate_item` 트리거는 "더블클릭"이라고 말하지 않습니다 -- 어댑터가 매핑합니다.
- `delete` 작업에는 `confirmation`이 필수입니다 -- 검증기가 이를 강제합니다.
- 필드는 `width_hint`와 `align_hint`를 사용하며, 절대 픽셀 값을 사용하지 않습니다.

---

## SUIS의 연결 관계

SUIS는 단독으로 존재하지 않습니다. 다른 모든 UASL 사양과 연결됩니다:

**Entity Spec** -- `subject.domain`은 실제 엔티티를 이름으로 참조해야 합니다. 표시 블록의 모든 필드 `name`은 해당 엔티티의 속성 또는 관계와 일치해야 합니다. Entity Spec이 `task`를 `title`, `status`, `due_date`, `assignee_id` 속성(및 `assignee` 관계)으로 정의했다면, SUIS에서는 바로 그 이름들을 사용합니다.

**IAS (Intent API Specification)** -- SUIS의 모든 작업 `intent`는 IAS에 대응하는 매핑이 있어야 합니다. SUIS가 `intent: search`라고 말하면, IAS가 어댑터에게 이것이 필터의 쿼리 파라미터를 사용하는 `GET /api/tasks`라고 알려줍니다. SUIS에는 API 상세가 절대 포함되지 않습니다 -- 그것이 IAS의 존재 이유입니다.

**Workflow Spec** -- SUIS의 `approve`와 `reject` 같은 워크플로 의도는 Workflow Spec에 정의된 상태 전이에 대응합니다. 워크플로가 `pending`에서 `approved`로의 `approve` 이벤트 전이를 정의했다면, SUIS 화면에 `intent: approve` 작업을 포함할 수 있습니다.

의미적 검증기가 이 모든 연결을 검사합니다. 존재하지 않는 엔티티를 참조하거나, 엔티티에 없는 필드를 참조하거나, IAS 매핑이 없는 의도를 사용하면, 코드가 생성되기 전에 검증기가 문서를 거부합니다.

---

[<- IAS](03-ias-spec.md) | [Workflow ->](05-workflow-spec.md) | [용어집](glossary.md)

*SUIS v1.1 -- 2026-01-29*
