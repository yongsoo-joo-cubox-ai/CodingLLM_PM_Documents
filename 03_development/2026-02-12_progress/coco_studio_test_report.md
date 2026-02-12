# Coco Studio 기능 테스트 보고서

| 항목 | 내용 |
|------|------|
| **문서번호** | SAI-TEST-2026-004 |
| **작성일** | 2026년 2월 12일 |
| **버전** | v1.0 |
| **보안등급** | 일반 |
| **작성** | Secern AI |

---

> **이전 진행**: [2026-02-07 진행](../2026-02-07_progress/README.md)

---

## 1. 테스트 개요

Coco Studio 웹 UI의 전체 기능을 체계적으로 검증하기 위해 7개 테스트 케이스(TC)를 설계하고 실행하였다. 테스트 대상은 코드 생성(Generate), 코드 리뷰(Review), 지식 기반 Q&A(Ask), Workspace 기능, 코드 프리뷰, 그리고 부가 기능(다크모드, Import, 프로젝트 관리)이다.

### 테스트 환경 구성

| 항목     | 내용                                             |
| ------ | ---------------------------------------------- |
| URL    | https://coco.secernai.net                      |
| 프로젝트   | my-xframe5-project (Product: xFrame5)          |
| 활성 모델  | Qwen2.5 Coder 32B AWQ (vLLM Remote)            |
| RAG 설정 | Token Budget: 1500, Similarity Threshold: 0.70 |
| 도메인 모델 | 4개 엔티티 (user, task, project, comment)          |
| 계정     | ysjoo / yongsoo.joo@secern.ai                  |

---

## 2. 테스트 결과 요약

| TC | 기능 | 우선순위 | 결과 | 비고 |
|----|------|----------|------|------|
| TC1 | Chat - Generate 모드 | P0 | **PASS** | CGF-B 파이프라인 정상 동작 |
| TC2 | Chat - Review 모드 | P0 | **FAIL** | 모델 미설정 (Review 태스크 카테고리) |
| TC3 | Chat - Ask 모드 | P0 | **PASS** | RAG 기반 Q&A 정상 |
| TC4 | Workspace - Regenerate | P1 | **FAIL** | 모델 가용성 에러 |
| TC5 | Workspace - 엔티티 Chat | P1 | **PASS** | 엔티티 컨텍스트 Q&A 정상 |
| TC6 | 코드 프리뷰 | P1 | **PASS** | xFrame5 런타임 프리뷰 정상 |
| TC7 | 부가 기능 | P2 | **PASS** | 다크모드, Import, 프로젝트 관리 정상 |

**전체 통과율: 5/7 (71.4%)** — P0 기능 중 Review 모드 실패, P1 기능 중 Regenerate 실패

---

## 3. 테스트 케이스 상세

### TC1: Chat - Generate 모드 (코드 생성)

**결과: PASS**

**테스트 시나리오:** Chat 페이지 Generate 탭에서 코드 생성 요청

**입력:**
> "user 엔티티의 목록 화면을 xFrame5로 생성해주세요. 검색과 페이징 기능이 포함되어야 합니다."

**실행 과정 (CGF-B Spec-Driven 파이프라인):**

1. **Intent Analysis** → 엔티티 인식 단계 시작
2. **Modeling entities** → "Found entity in domain graph" — user 엔티티를 도메인 그래프에서 매칭
3. **도메인 시각화** → user (10 nodes / 9 edges) 그래프 표시
4. **UI Spec 생성** → "Generated UI specification (confidence: 85%): Generated 1 screen(s): user_browse"
5. **사용자 승인 게이트** → Approve / Modify / Reject 3가지 선택지 제공
6. **Approve 클릭** → "Resuming generation from phase: IntentAnalysis"
7. **코드 컴파일** 완료

**출력 결과 (3개 파일, 12.0초):**

| 파일 | 설명 |
|------|------|
| `user_list.xml` | xFrame5 XML 레이아웃 — `<screen version="2.0" scriptcode="javascript" title="User 목록" screenid="user_list">` |
| `user_list.js` | JavaScript 로직 — `on_load()` → `fn_init()` → `fn_initDatasets()` 라이프사이클 |
| `user_list.mock.json` | Mock 데이터 — 엔티티 "user", 컬럼 정의 포함 |

**검증 포인트:**
- CGF-B 파이프라인 단계별 진행 상태 표시: 정상
- 신뢰도(confidence) 기반 사용자 승인 게이트: 정상 (85%)
- Approve/Modify/Reject 선택지: 정상 표시
- 3파일 생성 (XML + JS + Mock JSON): 정상
- 코드 블록에 복사(📋) 및 프리뷰(👁️) 아이콘 제공: 정상

---

### TC2: Chat - Review 모드 (코드 리뷰)

**결과: FAIL**

**테스트 시나리오:** Chat 페이지 Review 탭에서 코드 리뷰 요청

**입력:**
```javascript
function on_load() {
  var ds = screen.getDataset("ds_user");
  ds.load("/api/users");
}
function fn_search() {
  var name = screen.getControl("txt_name").getValue();
  ds.filter("name", name);
}
```

**에러 메시지:**
> "Review error: Review failed: LLM generation failed: All models exhausted for task Review. Tried 1 models, all failed."

**안내 메시지:**
> "Check that an LLM model with 'review' task category is active and healthy in Settings."

**원인 분석:**
현재 활성 모델(Qwen2.5 Coder 32B AWQ)이 Generate 및 Ask 태스크 카테고리에는 설정되어 있으나, **Review 태스크 카테고리에는 매핑되어 있지 않음**. Settings 페이지에서 모델의 태스크 카테고리 설정을 확인한 결과, Active Models 항목에 "Qwen2.5 Coder 32B AWQ vLLM Remote"만 표시되어 있으며 태스크별 매핑 현황은 UI에서 직접 확인 불가.

**조치 필요 사항:**
- Admin에서 Qwen2.5-32B-AWQ 모델에 Review 태스크 카테고리 추가 설정
- 또는 Review 전용 모델 추가 등록

---

### TC3: Chat - Ask 모드 (지식 기반 Q&A)

**결과: PASS**

**테스트 시나리오:** Chat 페이지 Ask 탭에서 프레임워크 관련 질문

**입력:**
> "xFrame5에서 데이터셋을 생성하고 그리드에 바인딩하는 방법을 알려주세요."

**응답 구조:**
1. **RAG 시각화** — 지식 그래프에서 `xframe5_screen_lifecycle`, `xframe5_naming_conventions` 등 관련 노드 시각 표시
2. **구조화된 답변**:
   - 데이터셋 생성 (`XDataset`) API 설명
   - 그리드 바인딩 (`Grid`) API 설명
   - 주의사항: 컴포넌트 경계 설명
3. **정직성 표시** — "⚠ 결론: 정확한 바인딩 방법은 지식 베이스에 없습니다"
4. **코드 예시** — `<Dataset id="ds_member" />`, `<Grid id="grd_member" />` 등
5. **참고 문서** — `xframe5_crud_patterns > crud`, `xframe5_js_generation > generation_rules` 등 태그 형태로 출처 명시
6. **관련 주제** — `xframe5_screen_lifecycle`, `xframe5_naming_conventions` 등 후속 탐색 가능

**검증 포인트:**
- RAG 검색 결과의 시각적 표현 (지식 그래프): 정상
- 구조화된 답변 (섹션별 구분): 정상
- 불확실한 정보에 대한 정직한 고지 (환각 방지): 정상
- 참고 문서 출처 표시: 정상
- 관련 주제 추천 (후속 탐색 유도): 정상

---

### TC4: Workspace - Regenerate (화면 재생성)

**결과: FAIL**

**테스트 시나리오:** Workspace에서 user 엔티티의 Outputs 탭 → Detail Screen Regenerate 클릭

**실행 과정:**
1. Outputs 탭에서 "Detail Screen" 옆 Regenerate 버튼 클릭
2. "Generate for user" 모달 표시 — Screen Types 중 Detail Screen 체크
3. "Generate 1 Screens" 클릭

**에러 메시지 (Toast):**
> "No model available: No healthy models available for task Generation"

**원인 분석:**
Chat 페이지 Generate(TC1)는 정상 동작했으나, Workspace Regenerate는 실패. 가능한 원인:
- **모델 가용성 타이밍 이슈**: TC1 실행 후 시간이 경과하여 모델 인스턴스 상태 변동
- **백엔드 라우팅 차이**: Chat Generate와 Workspace Regenerate가 서로 다른 API 엔드포인트 사용 가능성
- **모델 Health Check 간격**: Regenerate 호출 시점에 모델 헬스 체크 실패

**비고:**
동일한 Generation 태스크임에도 Chat과 Workspace에서 결과가 다른 점은 추가 조사가 필요하다. 모델 상태 모니터링 및 Health Check 주기를 확인할 필요가 있다.

---

### TC5: Workspace - 엔티티 Chat (엔티티 컨텍스트 Q&A)

**결과: PASS**

**테스트 시나리오:** Workspace에서 user 엔티티 선택 → Chat 탭에서 질문

**컨텍스트 표시:** "Chat context: user (9 fields)"

**입력:**
> "user 엔티티의 role 필드에 대한 enum 값을 어떻게 처리하나요?"

**응답 내용:**
- xFrame5는 enum 타입을 명시적으로 지원하지 않음
- 외부 로직으로 처리 필요 (validation, preprocessing)
- 예시: 'admin', 'user', 'guest' 문자열 값 검증 방법
- enum 검증은 xFrame5 내부 API가 아닌 사용자 코드에서 직접 구현해야 함
- ⚠ 참고: 지식 베이스에 enum 관련 API가 없으므로, enum 값을 처리하는 데 필요한 기능은 제공되지 않습니다.
- 참고 문서 및 관련 주제 태그 표시

**검증 포인트:**
- 엔티티 컨텍스트(user, 9 fields) 반영 여부: 정상 — role 필드에 특화된 답변 제공
- Chat 탭과 Ask 모드의 답변 품질 비교: 동일한 RAG 기반, 엔티티 스코프 제한이 추가
- 정직성 표시 (지식 베이스에 없는 정보 고지): 정상

---

### TC6: 코드 프리뷰 (xFrame5 런타임)

**결과: PASS**

**테스트 시나리오:** TC1에서 생성된 코드의 프리뷰 아이콘(👁️) 클릭

**실행 결과:**
- 새 탭 오픈: `[DEMO] Coco Preview`
- URL: `/preview-runtimes/xframe5/index.html?xframe_screen_url=/user_list`
- xFrame5 런타임이 생성된 XML + JS + Mock 데이터를 로딩하여 실제 화면 렌더링

**렌더링된 화면 구성:**

| 영역 | 내용 |
|------|------|
| 검색 패널 | Full Name, Email, Status(드롭다운), Created At(날짜 선택) — 한 행에 3필드 |
| 액션 버튼 | Search, New, Delete |
| 데이터 그리드 | 20행 mock 데이터, 컬럼: 순번, Email, Avatar Url, Status, Full Name, Id, Role, Department, Created At |

**검증 포인트:**
- 생성된 코드가 실제 xFrame5 런타임에서 렌더링 가능: 정상
- 검색 패널 (조건 입력 UI): 정상 렌더링
- 데이터 그리드 (mock 데이터 바인딩): 정상 — 20행 표시
- 액션 버튼 (CRUD 기본 기능): 정상 표시
- 별도 탭에서 프리뷰 → 원본 작업 화면 유지: 정상

---

### TC7: 부가 기능 (다크모드, Import, 프로젝트 관리 등)

**결과: PASS**

#### 7-1. 다크모드

상단 네비게이션의 🌙 아이콘 클릭 시 전체 UI에 다크모드 적용. 재클릭 시 라이트모드 복귀. 모든 영역(워크스페이스, 사이드 패널, 그래프)에 일관 적용.

#### 7-2. Import Domain Model

| 항목 | 내용 |
|------|------|
| 지원 형식 | SQL DDL, JSON Schema, OpenAPI 3.x, Entity Spec YAML (4종) |
| 입력 방식 | 직접 붙여넣기, 파일 업로드, 드래그 앤 드롭 |
| 보조 기능 | Example Models (5개), Load snippet, Download example |
| Import History | 이력 조회 및 삭제(revert) 가능 |
| 현재 이력 | task.schema.json (2026.2.11, json_schema) → task, comment, project, user 4개 엔티티 |

#### 7-3. Generate System (일괄 생성)

| 항목 | 내용 |
|------|------|
| Screen Types | List Screen, Detail Screen, Editor Screen (3종) |
| 엔티티 선택 | Core 그룹 (4개: comment, project, user, task) |
| 일괄 선택 | Select All / Clear 버튼 |
| 생성 수량 | (선택 엔티티 수) × (선택 Screen Types 수) — 예: 4 × 3 = 12 Screens |

#### 7-4. 프로젝트 관리

| 항목 | 내용 |
|------|------|
| 현재 프로젝트 | my-xframe5-project |
| "+" 버튼 | New Project 모달 표시 |
| 프로젝트 생성 필드 | Name, Description, Product (드롭다운) |
| Product 옵션 | Spring Boot, Vue 3, xFrame5 (3종) |
| 프로젝트 전환 | 드롭다운(∨) — 현재 프로젝트 1개만 존재하여 미동작 추정 |

#### 7-5. 기타 UI 요소

| 항목 | 내용 | 상태 |
|------|------|------|
| Logs 패널 | "Logs panel coming soon." | 미구현 |
| Settings | Project Context, Active Models, RAG Settings 확인 가능 | 정상 (읽기 전용) |
| Profile | 사용자 정보, Edit Name, Change Password, Sign Out | 정상 |
| Output 파일 클릭 | 파일 선택/하이라이트만 되고 코드 뷰어 미열림 | 미구현 또는 UI 제한 |

---

## 4. 발견된 이슈 및 개선 제안

### 이슈 목록

| # | 심각도 | 영역 | 설명 | 제안 |
|---|--------|------|------|------|
| 1 | **Critical** | Review 모드 | Qwen2.5-32B-AWQ 모델에 Review 태스크 카테고리 미설정으로 Review 기능 전면 불가 | Admin에서 모델 태스크 매핑 추가 |
| 2 | **Major** | Workspace Regenerate | Chat Generate는 정상이나 Workspace Regenerate에서 모델 가용성 에러 발생 | 백엔드 라우팅 및 모델 Health Check 로직 점검 |
| 3 | **Minor** | Logs 패널 | "Logs panel coming soon" — 미구현 상태 | Phase 1 범위 확인 후 일정 계획 |
| 4 | **Minor** | Output 파일 뷰어 | Outputs 탭에서 파일 클릭 시 코드 뷰어가 열리지 않음 | 파일 클릭 → 코드 프리뷰 연동 구현 |
| 5 | **Minor** | 프로젝트 전환 | 프로젝트가 1개일 때 드롭다운 미반응 — 의도된 동작인지 확인 필요 | UX 개선: 빈 리스트 표시 또는 비활성화 표시 |

### 긍정적 발견사항

1. **CGF-B 파이프라인 완성도**: 엔티티 인식 → 스펙 생성(신뢰도 85%) → 사용자 승인 게이트 → 컴파일까지 전체 흐름이 매끄러움
2. **코드 프리뷰**: 생성된 xFrame5 코드를 즉시 런타임에서 확인할 수 있어 개발 생산성 향상
3. **RAG 정직성**: 지식 베이스에 없는 정보에 대해 명확히 고지하여 환각(hallucination) 문제 방지
4. **Import 다형식 지원**: SQL DDL, JSON Schema, OpenAPI, YAML 4종 형식을 모두 지원하여 다양한 프로젝트에 대응 가능
5. **다중 프레임워크**: Spring Boot, Vue 3, xFrame5 등 프로젝트별 프레임워크 선택 가능

---

## 5. 페이지 구조 정리

### 5-1. 메인 네비게이션

```
상단 바 (좌 → 우):
  [Coco Studio]  [프로젝트 드롭다운 ∨]  [+]  ...  [Import]  [Generate]
  ...
  [💬 Chat] [📋 Logs] [⚙ Settings] [🌙 Dark Mode] [👤 Profile]
```

### 5-2. Workspace 페이지 (/workspace)

```
좌측: 엔티티 그래프 (React Flow 기반)
  - 4개 엔티티 카드: user, task, project, comment
  - 관계선 표시: author(N:1), assignee(N:1), owner(N:1), task(N:1)
  - 줌/패닝 컨트롤 (🔍+, 🔍-, ⛶)

우측: 엔티티 상세 패널 (클릭 시 표시)
  - [Fields] [Relations] [Outputs] [Chat] 탭
  - Fields: 필드명, 타입 목록 (예: user → 9 fields)
  - Relations: 엔티티 간 관계 (방향, 카디널리티)
  - Outputs: REGENERATE (Screen Types별) + PREVIOUS OUTPUTS (생성 이력)
  - Chat: 엔티티 컨텍스트 Q&A
```

### 5-3. Chat 페이지 (/chat)

```
3가지 모드 (하단 탭):
  [Generate] — 코드 생성 (CGF-B 파이프라인)
  [Review]   — 코드 리뷰 (코드 붙여넣기 → 리뷰 결과)
  [Ask]      — 지식 기반 Q&A (RAG 검색)
```

---

## 6. 결론

Coco Studio의 핵심 기능인 코드 생성(Generate)과 지식 기반 Q&A(Ask)는 안정적으로 동작하며, 특히 CGF-B Spec-Driven 파이프라인의 사용자 승인 게이트와 코드 프리뷰 기능은 실제 개발 워크플로우에서 높은 가치를 제공한다.

다만 Review 모드의 모델 태스크 설정 누락과 Workspace Regenerate의 간헐적 모델 가용성 문제는 데모 및 PoC 진행 전 반드시 해결이 필요하다. Logs 패널과 Output 파일 뷰어 등 일부 기능은 미구현 상태이나, 핵심 워크플로우에는 영향이 없으므로 추후 개선 일정에 반영하면 된다.

**권장 우선 조치사항:**
1. Review 태스크 카테고리에 모델 매핑 추가 (즉시)
2. Workspace Regenerate 모델 가용성 이슈 원인 분석 (1주 내)

---

## 변경이력

| 버전 | 일자 | 변경 내용 | 작성자 |
|------|------|----------|--------|
| 1.0 | 2026-02-12 | 초판 작성 — Coco Studio 기능 테스트 | 주용수 |
