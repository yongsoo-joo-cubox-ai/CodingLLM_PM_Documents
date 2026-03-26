---
description: SecernCode(시선코드) 코드 변경 사항을 PM 문서(CodingLLM_PM_Documents)에 반영. 07_secerncode_status_ko.md 현황 보고서, 01_roadmap_ko.md Track 2 진행률, glossary_ko.md 용어를 갱신 제안한다. "PM 문서 갱신", "현황 보고서 업데이트", "로드맵 반영", "SecernCode 변경 PM 반영", "Track 2 진행률" 등에 반응. SecernCode 내부 문서(AGENTS.md) 갱신은 sync-secerncode-docs 스킬이 담당하므로 이 스킬과 다름.
allowed-tools: Bash(bash:*), Bash(git:*), Read, Edit, Write, Glob, Grep
---

# PM 문서 갱신 — SecernCode 변경 반영

SecernCode(시선코드) 프로젝트의 코드 변경 사항을 분석하여 CodingLLM_PM_Documents의 PM 문서에 반영한다.

이 스킬은 **제안 방식**으로 동작한다 — 어떤 PM 문서를 어떻게 갱신할지 먼저 보여주고, 사용자가 동의한 항목만 실제로 수정한다.

## 사용법

```
/sync-pm-from-secerncode              # 변경 분석 + 갱신 제안
/sync-pm-from-secerncode --dry-run    # 분석만 (제안 목록 출력, 수정 없음)
```

## 갱신 대상

| PM 문서 | 갱신 트리거 | 갱신 내용 |
|---------|-----------|----------|
| `02_implementation/07_secerncode_status_ko.md` | 기능 변경, 새 패키지, API 변경 | 기능 현황, 기술 스택, 에이전트 구성 |
| `02_implementation/01_roadmap_ko.md` | Stage 진행률 변경 | Track 2 Stage 0~4 상태 |
| `05_knowledge_base/glossary_ko.md` | 새 용어 | 용어 추가 제안 |

## PM 문서 규칙

이 스킬이 PM 문서를 수정할 때 반드시 지켜야 할 규칙이다. CodingLLM_PM_Documents/CLAUDE.md에 정의되어 있으며, 이유는 문서 간 일관성과 이해관계자 신뢰를 유지하기 위해서다.

- **메타데이터**: 버전 번호 올리기 + 개정일 갱신
- **네비게이션 블록**: 이전/다음 링크 유지 (절대 삭제하지 않음)
- **TL;DR 블록**: 변경 내용이 TL;DR에 영향 주면 갱신
- **변경이력 테이블**: 문서 끝에 갱신 기록 추가
- **한글 작성**: 모든 내용 한글
- **AI/Claude/Generated 언급 금지**: 커밋 메시지, 문서 내용 어디에도 없어야 함
- **문서번호**: SAI-{카테고리}-{년도}-{순번} 형식 유지

## 워크플로

### 0단계: SecernCode 스캔

```bash
cd /Users/ysjoo/Documents/GitHub/_coding_llm/SecernCode
bash .claude/scripts/scan-packages.sh --full
```

스캔 결과 JSON에서 활용할 정보:
- `packages`: 패키지별 상태, Go 파일 목록
- `api_endpoints`: API 엔드포인트 현황
- `dependencies`: 의존성 현황
- `target_count`: 전체 패키지 수

### 1단계: SecernCode 변경 분석

스캔 결과에 더해 아래 파일을 읽어 현재 상태를 파악한다:

```
SecernCode/docs/feature_summary.md     → 기능 상태 (✅/🔄/❌)
SecernCode/README.md                    → 제품 개요, 설정 구조
SecernCode/.secerncode.json             → 모델/에이전트 설정
SecernCode/go.mod                       → 의존성 버전
```

최근 변경사항 파악:
```bash
cd /Users/ysjoo/Documents/GitHub/_coding_llm/SecernCode
git log --oneline -20
```

### 2단계: PM 문서 현재 상태 읽기

갱신 대상 PM 문서의 현재 내용을 읽는다:

```
CodingLLM_PM_Documents/02_implementation/07_secerncode_status_ko.md
CodingLLM_PM_Documents/02_implementation/01_roadmap_ko.md
CodingLLM_PM_Documents/05_knowledge_base/glossary_ko.md
```

### 3단계: 차이 분석 및 제안 생성

SecernCode 현재 상태와 PM 문서 내용을 비교하여 갱신이 필요한 항목을 식별한다.

**07_secerncode_status_ko.md 체크리스트:**
- 기능 현황 테이블의 상태(✅/🔄/❌)가 feature_summary.md와 일치하는가?
- 에이전트 구성(Coder/Task/Title/Summarizer)이 .secerncode.json과 일치하는가?
- 기술 스택 버전이 go.mod 의존성과 일치하는가?
- API 엔드포인트 목록이 scan 결과의 api_endpoints와 일치하는가?
- 새 패키지가 아키텍처 섹션에 반영되었는가?

**01_roadmap_ko.md 체크리스트:**
- Track 2 Stage 0~4 진행률이 feature_summary.md 기반 현실과 일치하는가?
- 완료 상태(✅)로 변경해야 할 Stage가 있는가?

**glossary_ko.md 체크리스트:**
- SecernCode에 새로 도입된 기술 용어가 용어집에 없는 경우 (go.mod 새 의존성, 새 패키지명 등)

### 4단계: 제안 보고

분석 결과를 아래 형식으로 보고한다:

```
## PM 문서 갱신 제안

### 07_secerncode_status_ko.md
- [갱신 필요] 기능 현황: Phase 5 eGovFrame RAG 상태 🔄→✅ 변경 필요
- [갱신 필요] API 엔드포인트: 새 엔드포인트 2개 추가 필요
- [최신] 에이전트 구성: 변경 없음

### 01_roadmap_ko.md
- [갱신 필요] Stage 1: "착수 예정" → "진행중" 변경 필요
- [최신] Stage 0: 완료 상태 유지

### glossary_ko.md
- [추가 제안] "opentui" — 새 의존성으로 추가됨
- [변경 없음] 기존 용어 모두 현행

갱신할 항목을 선택해 주세요 (전체/개별/건너뛰기)
```

### 5단계: 사용자 확인 후 갱신

사용자가 동의한 항목만 실제로 수정한다.

각 문서 수정 시:
1. 메타데이터의 버전 번호를 올린다 (minor: +0.1)
2. 개정일을 오늘 날짜로 갱신한다
3. 변경이력 테이블에 갱신 기록을 추가한다
4. 네비게이션 블록과 TL;DR 블록은 유지한다
5. 문서 내용에 AI/Claude/Generated를 언급하지 않는다

### 6단계: 결과 보고

```
## 갱신 완료

- 07_secerncode_status_ko.md: v1.0 → v1.1 (기능 현황 2건, API 1건 갱신)
- 01_roadmap_ko.md: 변경 없음 (사용자 건너뛰기)
- glossary_ko.md: 용어 1건 추가

변경된 파일: 2건
건너뛴 제안: 1건
```

## dry-run 모드

`$ARGUMENTS`에 `--dry-run`이 포함되면:
- 0~3단계(스캔, 분석, 비교)까지만 실행
- 4단계의 제안 목록을 출력
- 실제 파일 수정 없음

## 오류 처리

- scan-packages.sh 실행 실패 → SecernCode 경로 확인 안내
- SecernCode 소스 파일 읽기 실패 → 해당 비교 항목 건너뛰기
- PM 문서 수정 실패 → 해당 파일 건너뛰고 나머지 계속, 최종 보고에 포함

## 이 스킬과 sync-secerncode-docs의 차이

| 항목 | sync-secerncode-docs | 이 스킬 |
|------|---------------------|---------|
| 대상 | SecernCode 내부 AGENTS.md | PM 문서 (CodingLLM_PM_Documents) |
| 방식 | 자동 갱신 | 제안 후 사용자 확인 |
| 스크립트 | scan-packages.sh 직접 실행 | scan-packages.sh 결과 활용 |
| 문서 규칙 | AGENTS.md 형식 | PM 메타데이터/네비게이션/변경이력 규칙 |
