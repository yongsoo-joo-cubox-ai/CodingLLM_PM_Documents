# Coco CLI 테스트 보고서

| 항목 | 내용 |
|------|------|
| **문서번호** | SAI-TEST-2026-003 |
| **작성일** | 2026년 1월 23일 |
| **버전** | v1.0 |
| **보안등급** | 일반 |
| **작성** | Secern AI |

---

## 테스트 개요

| 항목 | 내용 |
|------|------|
| 테스트 일시 | 2026년 1월 23일 |
| 테스트 대상 | Coco CLI (QA 및 Review 명령어) |
| 테스트 환경 | xFrame5 제품, Agent Server (localhost:3000) |
| 테스트 결과 | **모든 테스트 통과** |

---

## 1. 테스트 입력 파일

### 1.1 샘플 코드 (sample_code.xml)

Review 명령어 테스트에 사용된 xFrame5 화면 정의 XML 파일입니다.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Screen id="scr_member_list">
    <Dataset id="ds1">
        <Column id="member_id" type="STRING"/>
        <Column id="member_name" type="STRING"/>
        <Column id="email" type="STRING"/>
        <Column id="status" type="STRING"/>
    </Dataset>
    <Grid id="grd1" dataset="ds1">
        <Column text="ID" datafield="member_id" width="100"/>
        <Column text="이름" datafield="member_name" width="150"/>
        <Column text="이메일" datafield="email" width="200"/>
        <Column text="상태" datafield="status" width="80"/>
    </Grid>
    <Button id="btn_search" text="조회"/>
    <Button id="btn_add" text="추가"/>
</Screen>
```

---

## 2. QA 명령어 테스트 결과

### 2.1 한국어 텍스트 출력

**질문:** "팝업 창을 어떻게 여나요?"

```bash
$ coder qa "팝업 창을 어떻게 여나요?" --product xframe5 --language ko
```

**응답:**
팝업 창을 여는 방법은 `loadpopup` 또는 `loadpopupex` API를 사용하여 수행할 수 있습니다.
`loadpopup`은 기본적인 팝업 창을 열고, `loadpopupex`는 추가적인 크기와 위치 설정을 할 수 있는 확장 기능을 제공합니다.

**코드 예시:**

```javascript
// loadpopup 사용
function btnloadPopup_on_mouseup() {
    factory.loadpopup("TestPopup", "/PopupEx", "테스트팝업",
        false, XFD_BORDER_RESIZE, 0, 0, true, false, screen);
}

// loadpopupex 사용 (크기 지정)
function btnloadPopupEx_on_mouseup() {
    factory.loadpopupex("TestPopup", "/PopupEx", "테스트팝업",
        false, XFD_BORDER_RESIZE, 0, 0, 400, 300, true, false, false, screen);
}
```

**Related Topics:** 팝업 관리, 모달 팝업, 팝업 위치 및 크기 설정

✓ (5 refs, 23829ms)

### 2.2 영어 텍스트 출력

**Question:** "How to open a popup window?"

```bash
$ coder qa "How to open a popup window?" --product xframe5 --language en
```

**Response:**
To open a popup window in xFrame5, you can use the `loadpopup` or `loadpopupex` API.
These APIs allow you to specify various parameters such as the popup name, screen URL, title, and window properties.

**Related Topics:** closepopup, findpopup, loadpopupex, loadpopupsync

✓ (5 refs, 34203ms)

### 2.3 한국어 JSON 출력

**질문:** "Grid에서 데이터 필터링하는 방법은?"

```bash
$ coder qa "Grid에서 데이터 필터링하는 방법은?" --product xframe5 --language ko --format json
```

```json
{
  "question": "Grid에서 데이터 필터링하는 방법은?",
  "answer": "Grid에서 데이터 필터링을 하는 방법은 주로 `applyfilter`, `applyfilterex`, `applymultifilter`, `applyfilterbyoption` 등의 API를 사용하여 구현할 수 있습니다...",
  "code_examples": [
    {
      "code": "function btn_filter_on_mouseup () {\n    grd.applyfilter(0, \"데이터1\", true);\n}",
      "description": "applyfilter를 사용한 단일 컬럼 필터링 예제",
      "language": "javascript"
    }
  ],
  "references": [
    {"category": "api", "name": "applyfilter", "relevance": 1.9},
    {"category": "api", "name": "applyfilterbyoption", "relevance": 1.9},
    {"category": "api", "name": "applyfilterex", "relevance": 1.9},
    {"category": "api", "name": "applymultifilter", "relevance": 1.9}
  ],
  "related_topics": ["데이터셋 필터링", "이벤트 핸들링", "UI 구성 요소", "데이터 바인딩"]
}
```

### 2.4 영어 JSON 출력

**Question:** "How to add a row to Dataset?"

```bash
$ coder qa "How to add a row to Dataset?" --product xframe5 --language en --format json
```

```json
{
  "question": "How to add a row to Dataset?",
  "answer": "In xFrame5, you can add a row to a Dataset using the `addrow()` method on a TableView component...",
  "code_examples": [
    {
      "code": "function btn_addrow_on_mouseup()\n{\n    tableview.addrow(100);\n}",
      "description": "Example of adding a row to a TableView",
      "language": "javascript"
    }
  ],
  "references": [
    {"category": "api", "name": "addrow", "relevance": 2.0}
  ],
  "related_topics": ["Dataset Manipulation", "TableView Methods", "Event Handling"]
}
```

---

## 3. Review 명령어 테스트 결과

### 3.1 한국어 텍스트 출력

```bash
$ coder review benchmark/cli_test/sample_code.xml --product xframe5 --language ko
```

**점수: 60/100**

**세부 점수:** Syntax: 100 | Patterns: 50 | Naming: 40 | Performance: 60

**요약:** 이 코드에는 명명 규칙, 패턴 및 성능과 관련된 여러 문제가 있습니다. 구문 오류나 보안 문제는 발견되지 않았습니다.

#### 발견된 이슈 (8개)

| 심각도 | 카테고리 | 라인 | 메시지 | 제안 |
|--------|----------|------|--------|------|
| Error | naming | 3 | Dataset ID 'ds1' does not start with 'ds_'. | Rename to 'ds_members' |
| Error | naming | 8 | Grid ID 'grd1' does not start with 'grid_'. | Rename to 'grid_members' |
| Error | pattern | 8 | Grid is missing 'version' attribute. | Add version="1.1" |
| Error | naming | 14 | Button ID 'btn_search' naming convention issue. | Rename to 'btn_search_members' |
| Error | naming | 15 | Button ID 'btn_add' naming convention issue. | Rename to 'btn_add_member' |
| Warning | pattern | 14 | Button missing 'on_click' attribute. | Add on_click handler |
| Warning | pattern | 15 | Button missing 'on_click' attribute. | Add on_click handler |
| Warning | performance | - | No pagination specified for grid. | Add paging='true' and pagesize |

#### 개선 제안

- 모든 컴포넌트가 명명 규칙을 따르도록 하여 코드 가독성과 유지보수성을 향상시키세요.
- xFrame5 모범 사례를 준수하기 위해 모든 그리드에 'version' 속성을 추가하세요.
- 버튼의 기능을 정의하기 위해 이벤트 핸들러를 구현하세요.
- 대용량 데이터셋을 효율적으로 처리하기 위해 그리드에 페이징을 추가하는 것을 고려하세요.

### 3.2 영어 텍스트 출력

```bash
$ coder review benchmark/cli_test/sample_code.xml --product xframe5 --language en
```

**Score: 60/100**

**Component Scores:** Syntax: 100 | Patterns: 50 | Naming: 40 | Performance: 60

**Summary:** The code has several issues related to naming conventions, patterns, and performance. There are no syntax errors or security issues identified.

### 3.3 JSON 출력 (한국어/영어 공통 구조)

```json
{
  "file": "benchmark/cli_test/sample_code.xml",
  "score": 60,
  "below_threshold": false,
  "summary": "The code has several issues related to naming conventions, patterns, and performance.",
  "issues": [
    {"category": "naming", "line": 3, "severity": "error",
     "message": "Dataset ID 'ds1' does not start with 'ds_'.",
     "suggestion": "Rename the dataset ID to 'ds_members'."},
    {"category": "naming", "line": 8, "severity": "error",
     "message": "Grid ID 'grd1' does not start with 'grid_'.",
     "suggestion": "Rename the grid ID to 'grid_members'."}
  ],
  "improvements": [
    "Ensure all components follow the naming conventions...",
    "Add the 'version' attribute to all grids...",
    "Implement event handlers for buttons...",
    "Consider adding pagination to grids..."
  ]
}
```

---

## 4. 테스트 결과 요약

| 테스트 항목 | CLI 명령어 | 출력 언어 | 출력 형식 | 결과 |
|-------------|-----------|----------|----------|------|
| QA #1 | `coder qa "팝업 창을 어떻게 여나요?" -p xframe5 -l ko` | 한국어 | Text | **통과** |
| QA #2 | `coder qa "How to open a popup window?" -p xframe5 -l en` | 영어 | Text | **통과** |
| QA #3 | `coder qa "Grid에서 데이터 필터링하는 방법은?" -p xframe5 -l ko -f json` | 한국어 | JSON | **통과** |
| QA #4 | `coder qa "How to add a row to Dataset?" -p xframe5 -l en -f json` | 영어 | JSON | **통과** |
| Review #1 | `coder review sample_code.xml -p xframe5 -l ko` | 한국어 | Text | **통과** |
| Review #2 | `coder review sample_code.xml -p xframe5 -l en` | 영어 | Text | **통과** |
| Review #3 | `coder review sample_code.xml -p xframe5 -l ko -f json` | 한국어 | JSON | **통과** |
| Review #4 | `coder review sample_code.xml -p xframe5 -l en -f json` | 영어 | JSON | **통과** |

---

## 5. CLI 명령어 참조

### 5.1 QA 명령어

```bash
$ coder qa [질문] [옵션]

옵션:
  -p, --product <PRODUCT>    제품 (기본값: xframe5)
  -l, --language <LANG>      출력 언어: ko, en (기본값: ko)
  -f, --format <FORMAT>      출력 형식: text, json, markdown (기본값: text)
  -c, --context <CONTEXT>    추가 컨텍스트 정보
  -s, --server <URL>         서버 URL (기본값: http://localhost:3000)
```

### 5.2 Review 명령어

```bash
$ coder review [파일] [옵션]

옵션:
  -p, --product <PRODUCT>    제품 (기본값: xframe5)
  -t, --file-type <TYPE>     파일 타입 (자동 감지)
  -l, --language <LANG>      출력 언어: ko, en (기본값: ko)
  -f, --format <FORMAT>      출력 형식: text, json (기본값: text)
  --threshold <SCORE>        최소 점수 임계값 (기본값: 0)
  -s, --server <URL>         서버 URL (기본값: http://localhost:3000)

참고: 파일 대신 "-"를 사용하면 stdin에서 코드를 읽습니다.
```

---

## 6. 결론

**테스트 결과:** 모든 CLI 명령어 테스트가 성공적으로 완료되었습니다.

### 주요 기능 확인 사항

- **QA 명령어:** xFrame5 관련 질문에 대해 정확한 답변과 코드 예제를 제공합니다.
- **Review 명령어:** 코드 품질을 분석하고 명명 규칙, 패턴, 성능 관련 이슈를 식별합니다.
- **다국어 지원:** 한국어와 영어 모두 정상적으로 출력됩니다.
- **출력 형식:** Text와 JSON 형식 모두 정상적으로 동작합니다.

### 성능

- QA 응답 시간: 약 20-35초
- Review 응답 시간: 약 18초

### API 엔드포인트

- QA: `POST /agent/qa`
- Review: `POST /agent/review`

---

## 변경이력

| 버전 | 일자 | 변경 내용 | 작성자 |
|------|------|----------|--------|
| 1.0 | 2026-01-23 | 자동 생성 — Coco CLI Test Suite | 분석팀 |
