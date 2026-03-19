[홈](README.md) | [개요](01-overview.md) | [Entity](02-entity-spec.md) | [IAS](03-ias-spec.md) | [SUIS](04-suis-spec.md) | [Workflow](05-workflow-spec.md)

---

# 용어집

본 용어집은 UASL 사양 전반에서 사용되는 핵심 용어를 정의합니다. 항목은 한글 가나다순으로 정렬되어 있으며, 각 항목은 해당 용어가 주로 정의된 사양 문서로의 링크를 포함합니다.

---

### 가드 (Guard)

워크플로 [전이](#전이-transition)가 발생하기 위해 참으로 평가되어야 하는 부울 조건. 가드는 유효하지 않은 상태 변경을 방지한다. 예를 들어, `approve` [이벤트](#이벤트-event)가 진행되기 전에 문서에 승인자가 1명 이상 있어야 하는 조건을 설정할 수 있다. 가드는 런타임에 평가된다. [Workflow Spec](05-workflow-spec.md) 참조.

### 계산 필드 (Computed Field)

다른 [속성](#속성-attribute)에 대한 수식으로 값이 정의되는 도출 필드. 계산 필드는 직접 저장되지 않으며 항상 읽기 전용이다. 수식 언어는 프레임워크 중립성을 유지하기 위해 의도적으로 단순하게 설계되어 있다. [Entity Spec](02-entity-spec.md) 참조.

### 경로 접미사 (Path Suffix)

IAS [리소스](#리소스-resource)의 기본 경로에 추가되어 완전한 엔드포인트 URL을 구성하는 경로 세그먼트. `/{id}`, `/bulk-delete`, `/export` 등의 접미사를 통해 동일 리소스에 대한 서로 다른 작업을 구별한다. [컴파일러](#컴파일러-compiler)는 기본 경로와 접미사를 결합하여 최종 라우트를 생성한다. [IAS Spec](03-ias-spec.md) 참조.

### 관계 (Relation)

두 [엔티티](#엔티티-entity) 간의 연결 방식을 기술하는 타입이 있는 링크. 관계 유형은 `one_to_one`, `many_to_one`, `one_to_many`, `many_to_many` 네 가지이다. 관계는 Entity Spec에서 선언되며, SUIS에서는 [내비게이션](#내비게이션-navigation)에, IAS에서는 중첩 리소스 엔드포인트에 활용된다. [Entity Spec](02-entity-spec.md) 참조.

### 권한 (Permissions)

SUIS [화면](#화면-screen)을 볼 수 있거나 워크플로 [전이](#전이-transition)를 실행할 수 있는 역할을 통제하는 역할 기반 접근 선언. 권한은 역할 목록(예: `[admin, manager]`)으로 선언되며, 생성된 코드에서 적용된다. 권한이 선언되지 않은 화면이나 전이는 인증된 모든 사용자가 접근할 수 있다. [SUIS Spec](04-suis-spec.md), [Workflow Spec](05-workflow-spec.md) 참조.

### 기본 키 (Primary Key)

[엔티티](#엔티티-entity)의 각 인스턴스를 고유하게 식별하는 [속성](#속성-attribute). 모든 엔티티는 반드시 하나의 기본 키를 선언해야 한다. 기본 키는 관련 엔티티의 [외래 키](#외래-키-foreign-key)가 참조하며, IAS에서 단일 레코드 작업에 사용된다. [Entity Spec](02-entity-spec.md) 참조.

### 내비게이션 (Navigation)

사용자가 뷰 간을 이동하는 방법을 기술하는 SUIS [화면](#화면-screen) 간 링크. 각 내비게이션 항목은 대상 화면(`target`)과 모드(`modal` 또는 `full`)를 지정한다. 내비게이션은 선언적이며, [어댑터](#어댑터-adapter)가 라우트, 다이얼로그, 탭 중 어느 방식으로 구현할지 결정한다. [SUIS Spec](04-suis-spec.md) 참조.

### 도메인 (Domain)

[엔티티](#엔티티-entity)가 속하는 주제 영역으로, 애플리케이션 내의 경계 컨텍스트를 나타낸다. SUIS에서는 `subject.domain`을 통해 표현되며, [화면](#화면-screen)이 어떤 엔티티를 대상으로 동작하는지 결정한다. 도메인은 대규모 애플리케이션을 일관된 그룹으로 조직하는 데 도움을 준다. [SUIS Spec](04-suis-spec.md) 참조.

### 목적 (Purpose)

SUIS [화면](#화면-screen)이 지원하는 사용자 작업의 종류를 나타내는 역할 선언. 정의된 목적은 `browse`(목록/검색), `view`(읽기 전용 상세), `create`(신규 생성), `edit`(수정), `dashboard`(집계 개요), `wizard`(다단계 흐름)이다. 목적은 [컴파일러](#컴파일러-compiler)의 코드 생성 전략을 안내한다. [SUIS Spec](04-suis-spec.md) 참조.

### 반환 타입 (Return Type)

IAS [의도](#의도-intent)가 실행 후 반환하는 결과 형태. 세 가지 반환 타입은 `collection`(레코드 배열), `single`(단일 레코드), `none`(본문 없음, 주로 삭제 작업)이다. 반환 타입은 [컴파일러](#컴파일러-compiler)가 응답 핸들러를 구성하는 방식을 결정한다. [IAS Spec](03-ias-spec.md) 참조.

### 상태 (State)

워크플로 상태 기계에서의 명명된 위치로, [엔티티](#엔티티-entity) 생명 주기의 한 단계를 나타낸다. 상태는 [전이](#전이-transition)로 연결된다. 각 상태는 진입/퇴장 [액션](#액션-action)과 [권한](#권한-permissions)을 선언할 수 있다. 일반적인 상태로는 `draft`, `in_review`, `approved`, `closed` 등이 있다. [Workflow Spec](05-workflow-spec.md) 참조.

### 상태 필드 (Status Field)

현재 워크플로 [상태](#상태-state) 값을 보유하는 [엔티티](#엔티티-entity) [속성](#속성-attribute)으로, 항상 enum 타입이다. 상태 필드는 Entity Spec(속성을 정의)과 Workflow Spec(상태 기계를 정의)을 연결하는 다리 역할을 한다. [컴파일러](#컴파일러-compiler)는 enum 값이 선언된 워크플로 상태와 일치하는지 보장한다. [Workflow Spec](05-workflow-spec.md) 참조.

### 속성 (Attribute)

[엔티티](#엔티티-entity)에 속하는 이름과 타입이 있는 필드. 모든 속성은 최소한 `name`과 `type`(예: `title: string`, `amount: decimal`)을 가진다. 속성에는 [제약 조건](#제약-조건-constraint), [표시 힌트](#표시-힌트-display-hint), 메타 정보를 부여할 수 있다. 속성은 다른 모든 사양이 필드를 참조하는 원자적 데이터 요소이다. [Entity Spec](02-entity-spec.md) 참조.

### 액션 (Action)

워크플로에서 [상태](#상태-state) 진입, 퇴장, [전이](#전이-transition) 시 실행되는 부수 효과. 액션은 상태 변경이 일어날 때 시스템이 수행해야 하는 동작을 기술한다. 알림 전송, 이메일 발송, 필드 값 설정 등이 대표적이다. 액션은 선언적이며, [어댑터](#어댑터-adapter)가 구현 방식을 결정한다. [Workflow Spec](05-workflow-spec.md) 참조.

### 어댑터 (Adapter)

UASL 중간 표현을 플랫폼별 코드로 변환하는 프레임워크 특화 컴파일러 모듈. 각 어댑터는 단일 기술 스택을 대상으로 한다(예: xframe5 어댑터, Vue 어댑터, Spring Boot 어댑터). 프레임워크 고유의 지식은 어댑터에만 존재하며, 사양 자체는 플랫폼 중립을 유지한다. [개요](01-overview.md) 참조.

### 엔티티 (Entity)

[속성](#속성-attribute)과 [관계](#관계-relation)를 가진 도메인 객체로, 실세계의 개념을 모델링한다. 엔티티는 UASL의 기반이며 다른 모든 사양이 엔티티를 참조한다. Task, User, Order, Product 등이 대표적 예시이다. 각 엔티티는 [기본 키](#기본-키-primary-key), 0개 이상의 속성, 선택적 관계를 가진다. [Entity Spec](02-entity-spec.md) 참조.

### 외래 키 (Foreign Key)

다른 [엔티티](#엔티티-entity)의 [기본 키](#기본-키-primary-key)를 참조하여 두 엔티티 간의 연결을 설정하는 [속성](#속성-attribute). 외래 키는 [관계](#관계-relation)를 뒷받침하는 구체적 메커니즘이다. Entity Spec에서 외래 키 속성을 선언하면, [컴파일러](#컴파일러-compiler)가 적절한 조인 또는 참조 코드를 생성한다. [Entity Spec](02-entity-spec.md) 참조.

### 의도 (Intent)

사용자가 수행하려는 의미론적 작업으로, HTTP 메서드나 UI 이벤트로부터 추상화된 개념이다. `search`, `create`, `update`, `delete`, `approve` 등이 대표적이다. SUIS에서는 [작업](#작업-operation)을 구동하고, IAS에서는 HTTP 엔드포인트에 매핑된다. [SUIS Spec](04-suis-spec.md), [IAS Spec](03-ias-spec.md) 참조.

### 이벤트 (Event)

하나의 워크플로 [전이](#전이-transition)를 트리거하는 명명된 액션. 이벤트는 `submit`, `approve`, `reject` 등 의미 있는 비즈니스 발생을 나타낸다. 이벤트는 정확히 하나의 전이에서 발화되며, [가드](#가드-guard)와 [권한](#권한-permissions)의 적용을 받을 수 있다. [Workflow Spec](05-workflow-spec.md) 참조.

### 작업 (Operation)

[의도](#의도-intent), [트리거](#트리거-trigger), 선택적 [내비게이션](#내비게이션-navigation)으로 정의되는 SUIS 사용자 액션. 작업은 [화면](#화면-screen)에서 사용자가 할 수 있는 행위를 기술한다. 예를 들어 행을 클릭하여 상세 정보를 조회하거나, 버튼을 눌러 신규 레코드를 생성하거나, 항목을 선택하여 일괄 삭제하는 것 등이 있다. [SUIS Spec](04-suis-spec.md) 참조.

### 전이 (Transition)

[이벤트](#이벤트-event)에 의해 트리거되는 워크플로 [상태](#상태-state) 간의 방향성 있는 간선. 전이는 워크플로를 통과하는 합법적인 경로를 정의한다. 각 전이는 출발 상태(`from`), 도착 상태(`to`), 트리거 이벤트, 선택적 [가드](#가드-guard), [액션](#액션-action), [권한](#권한-permissions)을 지정한다. [Workflow Spec](05-workflow-spec.md) 참조.

### 적합성 수준 (Conformance Level)

UASL 사양에 적용되는 점진적 검증 깊이 단계. L1(구조적)은 문서가 JSON Schema에 부합하는지 검사한다. L2(의미론적)은 교차 참조와 타입 일관성을 검증한다. L3(완전)은 사양 간 완전한 정합성을 보장한다. 적합한 [컴파일러](#컴파일러-compiler)는 반드시 지원하는 수준을 선언해야 한다. [개요](01-overview.md) 참조.

### 정규 (Canonical)

초안이나 추론 버전과 대비되는, 권위 있고 검증된 사양 형태. 정규 사양은 선언된 [적합성 수준](#적합성-수준-conformance-level)에 대한 모든 적합성 검사를 통과한 것으로, 유일한 진실의 원천으로 간주된다. LLM이 추론한 사양은 검증되기 전까지 명시적으로 비정규(non-canonical) 상태이다. [Entity Spec](02-entity-spec.md) 참조.

### 제약 조건 (Constraint)

[엔티티](#엔티티-entity) [속성](#속성-attribute)에 적용되어 허용 가능한 값을 제한하는 유효성 검사 규칙. 대표적인 제약 조건으로 `max_length`, `min`, `max`, `pattern`(정규식), `required` 등이 있다. 제약 조건은 엔티티 수준에서 선언되며, [컴파일러](#컴파일러-compiler)가 UI 검증과 API 검증 양쪽에 전파한다. [Entity Spec](02-entity-spec.md) 참조.

### 주제 (Subject)

SUIS [화면](#화면-screen)의 의미론적 앵커로, 화면이 어떤 [엔티티](#엔티티-entity) [도메인](#도메인-domain)을 대상으로 하며 [목적](#목적-purpose)이 무엇인지를 선언한다. 주제는 도메인을 통해 화면을 Entity Spec에 연결하고, 목적을 통해 화면의 행동 범주를 결정한다. [SUIS Spec](04-suis-spec.md) 참조.

### 즉시 실패 (Fail-fast)

UASL이 의무화하는 검증 전략으로, 유효하지 않은 사양을 명확한 오류 메시지와 함께 즉시 거부한다. 잘못된 입력을 변환하거나, 추측하거나, 암묵적으로 수정하지 않는다. 이 원칙은 오류가 코드 생성 시점이 아닌 사양 시점에 발견되도록 보장한다. [개요](01-overview.md) 참조.

### 초기 상태 (Initial State)

워크플로의 시작 [상태](#상태-state)로, 새 [엔티티](#엔티티-entity) 인스턴스가 워크플로에 처음 진입할 때 부여된다. 모든 워크플로는 반드시 정확히 1개의 초기 상태를 선언해야 한다. `draft`, `new`, `pending` 등이 대표적 예시이다. [Workflow Spec](05-workflow-spec.md) 참조.

### 최종 상태 (Final State)

워크플로의 종료 [상태](#상태-state)로, 나가는 [전이](#전이-transition)가 존재하지 않는다. 모든 워크플로는 최소 1개의 최종 상태를 선언해야 한다. [엔티티](#엔티티-entity)가 최종 상태에 도달하면 해당 워크플로는 완료된 것으로 간주한다. `closed`, `approved`, `archived` 등이 대표적 예시이다. [Workflow Spec](05-workflow-spec.md) 참조.

### 컬렉션 (Collection)

다중 레코드를 표시하는 [표시 블록](#표시-블록-display-block) 유형으로, 일반적으로 그리드나 목록으로 렌더링된다. SUIS에서 컬렉션 블록은 행별로 표시할 [필드](#필드-field)와 레코드 배치 방식을 정의한다. IAS에서는 [의도](#의도-intent)가 단일 객체가 아닌 항목 배열로 응답함을 나타내는 [반환 타입](#반환-타입-return-type)으로도 사용된다. [SUIS Spec](04-suis-spec.md) 참조.

### 컴파일러 (Compiler)

UASL 사양을 JSON Schema에 대해 검증하고, 사양 간 일관성을 검사하며, [어댑터](#어댑터-adapter)를 통해 대상 아티팩트로 변환하는 도구 체인. 적합한 컴파일러는 [즉시 실패](#즉시-실패-fail-fast) 검증을 구현해야 하며, 유효하지 않은 입력을 암묵적으로 변환해서는 안 된다. [개요](01-overview.md) 참조.

### 컴포넌트 (Component)

여러 SUIS [화면](#화면-screen) 간에 공유할 수 있는 재사용 가능한 [표시 블록](#표시-블록-display-block). 컴포넌트는 공통 UI 패턴(예: 상태 배지, 주소 카드)을 한 번 정의하고 이름으로 참조할 수 있게 하여, 중복을 줄이고 시각적 일관성을 보장한다. [SUIS Spec](04-suis-spec.md) 참조.

### 트리거 (Trigger)

SUIS에서 [작업](#작업-operation)을 시작하는 의미론적 사용자 상호작용. 트리거는 특정 DOM 이벤트에 매핑되는 것이 아니라, 사용자가 개념적으로 무엇을 하는지(예: `activate_item`, `bulk_selection`, `toolbar_button`)를 기술한다. [어댑터](#어댑터-adapter)가 트리거를 구체적인 UI 상호작용으로 변환한다. [SUIS Spec](04-suis-spec.md) 참조.

### 파라미터 소스 (Parameter Source)

IAS [의도](#의도-intent)가 입력 데이터를 얻는 출처. 네 가지 파라미터 소스는 `filters`(검색 기준), `form`(입력 필드), `selection[]`(선택된 레코드), `context`(현재 사용자 등 애플리케이션 상태)이다. [IAS Spec](03-ias-spec.md) 참조.

### 표시 블록 (Display Block)

[화면](#화면-screen)에서 가시적 데이터의 배치 방식을 정의하는 SUIS 구조. 세 가지 블록 유형은 `collection`(다중 레코드), `single`(단일 레코드), `summary`(집계 개요)이다. 각 블록은 [엔티티](#엔티티-entity) [필드](#필드-field)를 참조하며 레이아웃 힌트를 포함할 수 있다. [SUIS Spec](04-suis-spec.md) 참조.

### 표시 힌트 (Display Hint)

기본 프레젠테이션을 안내하되 정확한 렌더링 방식을 규정하지 않는, [엔티티](#엔티티-entity) [속성](#속성-attribute)에 부여되는 의미론적 제안. `default_sort`(정렬 기준 필드), `default_fields`(우선 표시 필드), 포맷 힌트 등이 대표적이다. [어댑터](#어댑터-adapter)는 표시 힌트를 수용하거나 재정의할 수 있다. [Entity Spec](02-entity-spec.md) 참조.

### 필드 (Field)

SUIS에서 [표시 블록](#표시-블록-display-block)이나 [필터](#필터-filter) 내에 있는 [엔티티](#엔티티-entity) [속성](#속성-attribute) 참조. 필드 참조에는 `format`, `width`, `alignment` 등 [어댑터](#어댑터-adapter)가 데이터 렌더링에 참고하는 선택적 표현 힌트를 포함할 수 있다. 필드는 항상 Entity Spec에서 정의된 속성으로 추적된다. [SUIS Spec](04-suis-spec.md) 참조.

### 필드 매핑 (Field Map)

사양 수준의 명명 규칙(snake_case)과 백엔드 API 명명 규칙(camelCase 등) 간의 IAS 매핑. 필드 매핑을 통해 사양은 일관된 명명 스타일을 사용하면서, 생성된 API는 대상 플랫폼의 관용적 규칙을 따를 수 있다. [IAS Spec](03-ias-spec.md) 참조.

### 필터 (Filter)

[엔티티](#엔티티-entity) [필드](#필드-field)를 연산자(equals, contains, between 등)와 입력 유형(text, select, date picker 등)에 바인딩하는 SUIS 검색 기준. 필터는 사용자가 [컬렉션](#컬렉션-collection) 결과를 좁히는 방법을 정의한다. [어댑터](#어댑터-adapter)가 필터를 플랫폼별 쿼리 메커니즘으로 변환한다. [SUIS Spec](04-suis-spec.md) 참조.

### 화면 (Screen)

SUIS의 기본 단위로, 사용자 대상 뷰를 기술한다. 화면은 [주제](#주제-subject)(어떤 엔티티와 목적), [표시 블록](#표시-블록-display-block)(어떤 데이터를 보여줄지), [작업](#작업-operation)(사용자가 무엇을 할 수 있는지)을 결합한다. 화면은 UI 코드 생성의 출발점이다. [SUIS Spec](04-suis-spec.md) 참조.

---

*UASL v1.0 — 2026-01-29*

---

[홈](README.md) | [개요](01-overview.md) | [Entity](02-entity-spec.md) | [IAS](03-ias-spec.md) | [SUIS](04-suis-spec.md) | [Workflow](05-workflow-spec.md)
