[홈](README.md) | [← Entity Spec](02-entity-spec.md) | [다음: SUIS →](04-suis-spec.md)

---

# IAS — 의도 API 사양 (Intent API Specification)

## IAS란?

IAS는 UI 의도(intent)와 HTTP 사이의 다리입니다. SUIS가 "사용자가 업무를 검색하려 한다"고 말하면, IAS는 "그건 `/api/tasks`에 대한 GET 요청이고 쿼리 파라미터를 사용한다"고 정의합니다. IAS 덕분에 SUIS에는 URL, HTTP 메서드, 페이로드(payload) 구조가 전혀 노출되지 않습니다.

IAS를 번역 테이블이라고 생각하면 됩니다. 한쪽은 사용자 의도(탐색, 검색, 생성, 승인)로 대화하고, 반대쪽은 HTTP(GET, POST, PUT, DELETE, 경로, 쿼리 문자열, 요청 본문)로 대화합니다. 두 쪽이 직접 만나는 일은 없으며, IAS가 그 사이에 위치합니다.

## IAS가 필요한 이유

IAS 이전에는 UI 사양에 API 세부사항이 직접 포함되어 밀결합(tight coupling)이 발생했습니다. URL, 메서드, 파라미터 매핑이 모든 UI 사양에 흩어져 있었고, API 경로 하나를 변경하면 해당 경로를 참조하는 모든 UI 사양을 함께 수정해야 했습니다.

IAS는 "사용자가 의도하는 것"과 "API가 구현하는 방식"을 분리합니다. 그로 인한 이점은 즉각적입니다:

- **UI 사양을 건드리지 않고 API 경로를 변경할 수 있습니다.** `/api/tasks`를 `/api/v2/tasks`로 바꿔도 한 곳만 수정하면 됩니다.
- **같은 SUIS 문서를 서로 다른 백엔드 API와 함께 사용할 수 있습니다.** Spring Boot 백엔드와 Express 백엔드가 동일한 SUIS를 공유하되, IAS 문서만 다르게 작성하면 됩니다.
- **어댑터(adapter)는 완전히 해석된 HTTP 연산을 받아 코드를 생성합니다.** xFrame5나 Vue 컴파일러가 추측할 필요가 없습니다. 구체적인 메서드, 경로, 파라미터 소스를 전달받습니다.

## 문서 구조

IAS 문서는 두 개의 최상위 키를 가진 YAML 파일입니다:

```yaml
api:
  version: "1.0"

  resources:
    # ... 리소스 정의
```

`api.version`은 현재 항상 `"1.0"`입니다. `api.resources` 맵이 핵심 영역으로, 각 키는 리소스 이름이고 각 값은 해당 리소스의 의도가 HTTP에 어떻게 매핑되는지를 기술합니다.

## 리소스(Resources)

각 리소스는 엔티티(Entity Spec에서 정의)와 기본 API 경로에 매핑됩니다. 다음은 최소한의 리소스 정의입니다:

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

**필수 필드:**

| 필드 | 규칙 | 예시 |
|------|------|------|
| `path` | `/`로 시작해야 함 | `/api/tasks` |
| `entity` | Entity Spec의 엔티티 이름과 일치해야 함 | `task` |
| `intents` | 하나 이상의 의도가 정의되어야 함 | 아래 참조 |

**선택 필드:**

| 필드 | 용도 | 예시 |
|------|------|------|
| `field_map` | 사양 명명과 백엔드 명명 간 변환 | `due_date: dueDate` |

`path`는 기본 경로입니다. 개별 의도는 `path_suffix`를 통해 이 경로에 추가할 수 있습니다.

## 의도 매핑(Intent Mapping)

각 의도는 의미적 이름(semantic name)을 HTTP 연산에 매핑합니다. 의미적 이름은 SUIS에서 오고, HTTP 세부사항은 여기에서 정의합니다.

```yaml
intents:
  view:
    method: GET
    path_suffix: "/{id}"
    returns: single
```

**필수 필드:**

| 필드 | 값 | 용도 |
|------|-----|------|
| `method` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` | HTTP 메서드 |
| `returns` | `collection`, `single`, `none` | 어댑터가 기대하는 반환 형태 |

**선택 필드:**

| 필드 | 용도 | 예시 |
|------|------|------|
| `path_suffix` | 리소스 `path`에 추가되는 경로 | `/{id}` |
| `query_from` | 쿼리 파라미터의 출처 | `filters` |
| `body_from` | 요청 본문의 출처 | `form` |

### 표준 CRUD 매핑

대부분의 리소스는 예측 가능한 패턴을 따릅니다. 다음은 대다수의 사용 사례를 커버하는 표준 CRUD 매핑입니다:

| 의도 | 메서드 | 경로 | 반환 |
|------|--------|------|------|
| browse | GET | /api/tasks | collection |
| search | GET | /api/tasks?{filters} | collection |
| view | GET | /api/tasks/{id} | single |
| create | POST | /api/tasks | single |
| edit | PUT | /api/tasks/{id} | single |
| delete | DELETE | /api/tasks/{id} | none |

이 여섯 가지에 한정되지 않습니다. 커스텀 의도(`approve`, `reject`, `export` 등)도 동일한 구조를 따릅니다.

## 파라미터 소스(Parameter Sources)

파라미터에는 출처가 있어야 합니다. IAS는 어댑터에게 데이터를 어디서 가져올지 알려주는 네 가지 소스를 정의합니다:

| 소스 | 출처 | 용도 |
|------|------|------|
| `filters` | SUIS 필터 정의에서 | 검색(search) 및 탐색(browse) 쿼리 |
| `form` | 화면의 편집기(editor) 필드 값에서 | 생성(create) 및 편집(edit) 제출 |
| `selection[]` | 다중 선택 체크박스 등에서 | 일괄 작업(bulk operation) |
| `context` | 화면 상태(현재 ID, 부모 ID 등)에서 | 컨텍스트 기반 조회 |

어떤 소스를 어디에 사용할 수 있는지에 대한 두 가지 규칙이 있습니다:

- **`query_from`은 `GET` 요청에서만 유효합니다.** POST 본문에 쿼리 파라미터를 넣을 수 없습니다.
- **`body_from`은 `POST`, `PUT`, `PATCH` 요청에서만 유효합니다.** GET과 DELETE는 요청 본문을 전달하지 않습니다.

검증기(validator)가 이 규칙을 강제합니다. DELETE 의도에 `query_from: filters`를 작성하면, 명확한 오류 메시지와 함께 검증이 실패합니다.

## 반환 타입(Return Types)

`returns` 필드는 어댑터에게 어떤 형태의 데이터를 기대해야 하는지 알려줍니다. 이 값은 UI가 응답을 렌더링하는 방식에 직접적인 영향을 미칩니다:

| 반환 타입 | 어댑터 동작 | 일반적인 UI |
|-----------|-------------|-------------|
| `collection` | 레코드 배열을 기대 | 그리드(grid), 목록, 테이블 |
| `single` | 단일 레코드를 기대 | 폼(form), 상세 보기 |
| `none` | 데이터 없음(성공/실패만) | 현재 화면 새로고침 |

`returns`가 `none`인 경우, 어댑터는 일반적으로 작업 완료 후 현재 화면을 새로고침합니다. 예를 들어, 삭제 연산은 그리드에서 해당 행을 제거하고 같은 화면에 머무릅니다.

## 필드 매핑(Field Mapping)

백엔드 API가 Entity Spec과 항상 같은 명명 규칙을 사용하지는 않습니다. Java API는 일반적으로 camelCase를 사용하는 반면, Entity Spec은 snake_case를 사용합니다. `field_map`이 이 변환을 담당합니다:

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

키는 엔티티 속성 이름(Entity Spec 기준)이고, 값은 백엔드 API 필드 이름입니다. 어댑터는 요청을 구성하고 응답을 파싱할 때 이 매핑을 적용합니다.

`field_map`이 제공되지 않으면, 속성 이름이 변환 없이 그대로 전달됩니다.

## 일괄 작업(Bulk Operations)

사용자가 여러 레코드를 선택하여 한 번에 처리하는 경우가 있습니다. 일괄 작업은 `selection[]`을 본문 소스로 사용합니다:

```yaml
intents:
  bulk_delete:
    method: POST
    path_suffix: /bulk-delete
    body_from: "selection[]"
    returns: none
```

어댑터는 UI에서 선택된 ID 목록을 수집하여 요청 본문으로 전송합니다. 일괄 작업은 삭제의 경우에도 일반적으로 POST를 사용합니다. DELETE 요청 본문에 ID 목록을 담는 방식은 모든 환경에서 지원되지 않기 때문입니다.

## 워크플로 액션(Workflow Actions)

승인(approve)이나 반려(reject) 같은 워크플로 전이(transition)는 커스텀 의도로 매핑됩니다. CRUD 의도와 동일한 구조를 따르되, 도메인 고유의 의미를 가집니다:

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

여기서 `body_from: form`은 승인 코멘트나 반려 사유를 전달합니다. SUIS가 폼 필드를 정의하고, IAS가 그 데이터를 어디로 보낼지를 정의합니다.

## 전체 예제

다음은 업무 관리 리소스를 위한 완전한 IAS 문서입니다. 표준 CRUD, 일괄 작업, 워크플로 액션, 필드 매핑을 모두 포함합니다:

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

이 하나의 문서로 어댑터는 HTTP 클라이언트 코드를 생성하는 데 필요한 모든 정보를 얻습니다. SUIS는 이 세부사항을 전혀 알 필요가 없습니다.

## IAS의 연결 관계

IAS는 독립적으로 존재하지 않습니다. Entity Spec과 SUIS 사이에 위치하며, 세 가지 바인딩 규칙을 통해 이들을 연결합니다.

**엔티티 바인딩(Entity binding).** 각 리소스의 `entity` 필드는 Entity Spec의 엔티티 이름을 참조합니다. Entity Spec에서 `task` 엔티티를 `id`, `title`, `status`, `due_date` 속성과 함께 정의했다면, `task`에 대한 IAS 리소스는 해당 속성을 `field_map`에서 사용할 수 있습니다. 검증기는 해당 엔티티가 존재하는지 확인합니다.

**SUIS 의도 바인딩(SUIS intent binding).** SUIS 화면에서 선언된 모든 작업 의도(operation intent)는 대응하는 IAS 리소스에 일치하는 의도가 있어야 합니다. SUIS 탐색 화면이 `intent: search`를 선언하면, IAS 리소스에 `search` 의도가 정의되어 있어야 합니다. 누락된 매핑은 치명적 오류(hard error)입니다. 검증기가 해당 사양을 거부합니다.

**워크플로 바인딩(Workflow binding).** Workflow Spec의 전이 이벤트(transition event)에 IAS 바인딩이 가능합니다. 워크플로가 `approve` 전이를 정의하면, IAS의 `approve` 의도가 HTTP 세부사항을 제공합니다. 이를 통해 워크플로 엔진이 HTTP 지식을 내장하지 않고도 API 호출을 트리거할 수 있습니다.

```
Entity Spec          IAS                    SUIS
-----------          ---                    ----
task entity  <----   task resource
  attributes         field_map
                     intents      ---->    operations
                       approve    ---->      intent: approve
                       search     ---->      intent: search
```

컴파일러는 세 가지 연결을 모두 검증합니다. 존재하지 않는 엔티티, 매핑 없는 의도, 알 수 없는 속성을 참조하는 필드 맵 등 어느 링크가 끊어져 있든, 문제의 정확한 위치를 가리키는 명확한 오류 메시지를 받게 됩니다.

---

*IAS v1.0 — 2026-01-29*

---

[← Entity Spec](02-entity-spec.md) | [SUIS →](04-suis-spec.md) | [용어집](glossary.md)
