# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

이 저장소는 **Coco / IntraGenX 프로젝트의 문서 저장소**입니다. AI 코드 거버넌스 플랫폼인 Coco(구 Coder)의 전략 분석, 로드맵, API 레퍼런스 문서를 관리합니다.

> **대외 브랜딩**: IntraGenX (2026-03~) — 시선AI(The Brain, LLM 개발) + 대보DX(The Body, 애플리케이션 & 어플라이언스) 합작

## Document Structure

```
CodingLLM_PM_Documents/
├── 01_strategy/           # 전략 문서
│   ├── 01_executive_summary_ko.md
│   ├── 02_competitive_strategy_ko.md
│   ├── 03_regulatory_environment_ko.md
│   ├── 04_product_overview_ko.md
│   └── 05_track2_tech_strategy_ko.md
│
├── 02_implementation/     # 구현 문서
│   ├── 01_roadmap_ko.md
│   ├── 02_resource_plan_ko.md
│   ├── 03_cost_analysis_ko.md
│   ├── 04_phase2_tech_stack_ko.md
│   ├── 05_api_reference_ko.md
│   └── 06_vllm_rd_plan_ko.md
│
├── 03_development/        # 개발 진행 자료
│   ├── README.md          # 개발 현황 인덱스
│   ├── 2026-01-15_project_intro/
│   │   ├── project_introduction.md
│   │   ├── load_test_qwen32b.md
│   │   └── model_benchmark.md
│   ├── 2026-01-24_progress/
│   │   ├── vram_sizing.md
│   │   ├── architecture_mcp.md
│   │   ├── lightweight_model_qa.md
│   │   ├── qa_test_report/
│   │   ├── qa_examples/
│   │   ├── qa_update/
│   │   └── cli_test/
│   ├── 2026-02-07_progress/
│   │   ├── README.md              # 1/26~2/7 진행 종합 요약
│   │   ├── uasl_spec/             # UASL/SUIS 스펙 문서
│   │   └── reports/               # CGF 비교, QA 개선 보고서
│   ├── 2026-02-12_progress/
│   │   └── coco_studio_test_report.md  # Studio 기능 테스트 (TC1~TC7)
│   └── 2026-03-19_progress/
│       ├── README.md              # 2/12~3/19 진행 종합 요약
│       ├── model_finetuning_4b.md # 4B 모델 LoRA 파인튜닝 실험
│       └── uasl_spec/             # UASL v2/v3 업데이트 이력
│
├── 04_meetings/           # 회의록
│   ├── 2025-12-26_softbase_xframe.md
│   ├── 2026-02-11_ShinsegaeInC.md
│   └── 2026-03-17_dev_update.md
│
├── 05_knowledge_base/     # 기술 참고자료
│   ├── README.md          # xFrame5 아카이브 내용 기록
│   └── xframe5_knowledge_base.zip  # 대용량 (Git LFS)
│
├── 06_infra/              # 인프라/배포 관련 자료
│   └── 코딩에이전트_외부업체데모_환경구성_방안.docx
│
├── _00_work/              # 작업 자료 스테이징
│   ├── 260127-260211/     # 1/26~2/11 작업 원본
│   ├── 260212-260319/     # 2/12~3/19 작업 원본
│   └── ppt_assets/        # PPT 빌드 스크립트, 템플릿, 다이어그램
│
└── .obsidian/             # Obsidian 설정
```

### 문서 목록

| 경로 | 설명 |
|------|------|
| `01_strategy/01_executive_summary_ko.md` | 경영진 요약 - 프로젝트 개요 및 핵심 가치 |
| `01_strategy/02_competitive_strategy_ko.md` | 경쟁 전략 - 상세 경쟁사 분석 |
| `01_strategy/03_regulatory_environment_ko.md` | 규제 환경 - AI 규제 및 컴플라이언스 |
| `01_strategy/04_product_overview_ko.md` | 제품 기능 소개 - Coco 구성 및 핵심 기능 |
| `01_strategy/05_track2_tech_strategy_ko.md` | 트랙 2 기술 전략 리서치 v2.0 — 경쟁 솔루션 + Cline 비교 병합본 |
| `02_implementation/01_roadmap_ko.md` | 구현 로드맵 - Phase 1/2 + 트랙 2 코딩 에이전트 로드맵 |
| `02_implementation/02_resource_plan_ko.md` | 투입 인력 및 로드맵 - Phase별 인력/일정 계획 |
| `02_implementation/04_phase2_tech_stack_ko.md` | Phase 2 기술 스택 - 학습 자료/구현 가이드 |
| `02_implementation/03_cost_analysis_ko.md` | 비용 분석 - TCO 및 ROI |
| `02_implementation/05_api_reference_ko.md` | API 레퍼런스 - 엔드포인트 명세 |
| `02_implementation/06_vllm_rd_plan_ko.md` | vLLM 인프라 고도화 R&D 계획 (인증/암호화/LiteLLM 멀티 모델) |
| `03_development/` | 개발 진행 자료 - 테스트, 벤치마크 |
| `03_development/2026-02-07_progress/` | 2월 1주차 진행 - 코드생성, UASL, QA 개선 |
| `03_development/2026-02-12_progress/` | Coco Studio 기능 테스트 (7 TC, 71.4%) |
| `03_development/2026-03-19_progress/` | 3월 진행 - 4B 파인튜닝, UASL v2/v3, 서버 분리, 부산은행 PoC |
| `04_meetings/2026-02-11_ShinsegaeInC.md` | 신세계 I&C 솔루션 데모 회의록 |
| `04_meetings/2026-03-17_dev_update.md` | 개발 현황 업데이트 (서버 분리, Playground, 부산은행 PoC) |
| `05_knowledge_base/glossary_ko.md` | 프로젝트 용어집 - 경영진/개발자용 이중 설명 (~70개 용어) |
| `05_knowledge_base/README.md` | xFrame5 아카이브 내용 기록 |

## 문서 관리 규칙

### 폴더 README
- 모든 주요 폴더(01~05)에 README.md가 존재하며 읽기 순서를 안내
- 새 문서 추가 시 해당 폴더 README.md에 반영

### 파일명 넘버링
- 01_strategy/, 02_implementation/ 정식 문서는 읽기 순서 번호를 파일명에 prefix로 부여
- 형식: `{NN}_{파일명}_ko.md` (예: `01_executive_summary_ko.md`)
- 참고 문서는 정식 문서 뒤 번호 부여 (예: 정식 4건 → 참고 문서는 05번부터)
- 03_development/, 04_meetings/는 날짜 prefix가 자연 정렬 역할을 하므로 넘버링 미적용

### 네비게이션 블록
- `01_strategy/`, `02_implementation/` 문서 상단에 이전/다음 네비게이션 존재
- 형식: `> **문서 N/M** | 이전: [...] | 다음: [...] | [폴더 인덱스](./README.md)`
- 위치: 메타데이터(날짜/버전) 아래, `---` 구분선 위
- 새 문서 추가 시 기존 문서의 네비게이션도 업데이트

### TL;DR 블록
- 01_strategy/, 02_implementation/ 정식 문서(README, 참고 문서 제외)에 TL;DR 블록 필수
- 위치: `---` 구분선 직후, 본문 첫 섹션 직전
- 형식: blockquote(`>`) 안에 3~5개 불릿 + 대상 독자 + 소요 시간
- 새 문서 추가 시 반드시 TL;DR 포함

### 용어집
- 위치: 05_knowledge_base/glossary_ko.md
- 새로운 기술 용어 도입 시 용어집에도 반영
- 기존 용어의 정의/범위가 변경되면 용어집도 함께 업데이트
- 용어 설명에 자주 바뀌는 수치(버전, 포트 등)를 직접 기입하지 않고 해당 문서 링크로 위임
- UASL 내부 용어는 UASL glossary에서 별도 관리

### 03_development/ 체인
- 각 진행 폴더 README에 `이전 진행`/`다음 진행` 링크 체인 유지
- 새 진행 폴더 추가 시 직전 폴더 README에 다음 링크 추가

### 문서 메타데이터 표준

모든 정식 문서(README 제외)는 아래 테이블 형식의 메타데이터 헤더를 사용한다.

**문서번호 체계**: `SAI-{카테고리}-{년도}-{순번}`

| 카테고리 | 대상 | 보안등급 |
|----------|------|----------|
| `STR` | 01_strategy/ 전략 문서 | 대외비 |
| `IMPL` | 02_implementation/ 구현 문서 | 대외비 |
| `TEST` | 03_development/ 테스트·벤치마크 보고서 | 일반 |
| `MTG` | 04_meetings/ 회의록 | 일반 |
| `KB` | 05_knowledge_base/ 기술 참고자료·용어집 | 일반 |

**보고서 헤더** (01_strategy, 02_implementation, 03_development):

```markdown
# [문서 제목]

| 항목 | 내용 |
|------|------|
| **문서번호** | SAI-STR-2026-001 |
| **작성일** | 2026년 1월 21일 |
| **개정일** | 2026년 2월 12일 |
| **버전** | v3.0 |
| **보안등급** | 대외비 |
| **작성** | Secern AI |
```

**회의록 헤더** (04_meetings):

```markdown
# [회의 제목]

| 항목 | 내용 |
|------|------|
| **문서번호** | SAI-MTG-2026-001 |
| **일시** | 2026년 2월 11일 오전 9시~10시 |
| **장소/형태** | 대면 + Teams 화상 |
| **보안등급** | 일반 |
| **작성** | Secern AI |

### 참석자

| 소속 | 참석자 |
|------|--------|
| **외부** | 홍길동 대표 |
| **Secern AI** | 주용수 매니저 |
```

**공통 하단**: 모든 정식 문서 끝에 변경이력 테이블 포함

```markdown
---
## 변경이력

| 버전 | 일자 | 변경 내용 | 작성자 |
|------|------|----------|--------|
| 1.0 | 2026-01-21 | 초안 작성 | 분석팀 |
```

## Coco / IntraGenX 핵심 개념

- **제품 정체성**: AI 코드 생성이 아닌 **AI 코드 거버넌스** 플랫폼
- **대외 브랜드**: IntraGenX — "AI 기반 차세대 시스템 개발 플랫폼" (시선AI + 대보DX 합작)
- **투트랙 전략**:
  - **트랙 1 (IntraGenX)**: Spec-Driven 일괄 코드 생성 — SI 프로젝트, Top-Down
  - **트랙 2 (코딩 에이전트)**: OpenCode 기반 자율형 CLI 에이전트 — 개발자, Bottom-Up (2026년 4월 착수, 시선AI 주도)
- **MCP 용어 구분**: 양쪽 모두 MCP(Model Context Protocol) 동일 프로토콜 사용, 용도가 다름 — 트랙 1: 코드 생성 엔진 서버(xframe5-compiler 등), 트랙 2: 개발 도구 접근 서버(Jira, Confluence 등)
- **대상 환경**: 폐쇄망, 온프레미스 LLM, 규제 산업 기업 (금융권 PoC 진행 중)
- **6대 USP**: ①결정론적 출력, ②표준 강제, ③완전한 온프레미스, ④Spec-Driven 코드 생성, ⑤감사 추적, ⑥LLM 추상화
- **제품 구성**: Coco Engine, Coco Studio, Coco CLI, Coco Admin, MCP Servers, Eclipse Plugin
- **지원 프레임워크**: xFrame5, WebSquare, Vue 3, React 19, Spring Boot

## 서버 환경

| 환경 | Studio 포트 | Engine 포트 | 비고 |
|------|-----------|-----------|------|
| **Demo** | 5174 | 3100 | 고객 데모용 (http://172.16.100.116:5174/landing) |
| **Dev** | 5173 | 3000 | 개발용 (기존) |
| **Playground** | 4000 + 프로젝트 ID | 동적 | Docker 기반 전체 앱 배포, FE-BE 연동 |

- Demo 도메인: https://coco.secernai.net

## API 엔드포인트 요약

```bash
# 핵심 엔드포인트
POST /agent/agentic/v2/stream  # 스트리밍 코드 생성 (권장)
POST /agent/review             # 코드 리뷰
POST /agent/qa                 # 프레임워크 Q&A
GET  /agent/models             # 사용 가능 모델 목록
GET  /_health                  # 헬스 체크
```

## Google Drive 동기화

Git 저장소를 Google Drive 공유 드라이브로 단방향 미러링하는 커맨드가 있다.

- **소스**: 이 저장소 (Git이 원본)
- **타겟**: `CodingLLM_Project/01_Documents/` (Google Drive 공유 드라이브)
- **MD 처리**: DOCX로 변환하여 타겟에 저장, 원본 MD는 Git에만 보관
- **스크립트**: `.claude/scripts/sync-to-gdrive.sh`

### 슬래시 커맨드

| 커맨드 | 설명 |
|--------|------|
| `/sync-gdrive` | 실제 동기화 실행 |
| `/sync-gdrive --dry-run` | 미리보기 (변경 없음) |
| `/sync-gdrive-analyze` | 소스/타겟 차이점 분석 |

### 터미널에서 직접 실행

```bash
bash .claude/scripts/sync-to-gdrive.sh            # 실제 동기화
bash .claude/scripts/sync-to-gdrive.sh --dry-run   # 미리보기
```

### 동작 요약

1. **rsync**: 비-MD 파일 증분 복사 (Google Drive FUSE 호환 옵션)
2. **pandoc**: MD → DOCX 변환 (문서 간 `.md` 링크를 `.docx`로 치환, 이미지 임베드)
3. **정리**: 소스에 없는 타겟 파일 삭제 (`.DS_Store` 제외)
4. **리포트**: 복사/변환/삭제/스킵/실패 건수 출력

### 사전 요구사항

- `pandoc` 설치 필요: `brew install pandoc`
- Google Drive 데스크톱 앱이 마운트되어 있어야 함

## 문서 작업 시 참고사항

- 모든 문서는 **한글**로 작성
- 파일명은 **영문 소문자 + 언더스코어** 사용
- 회의록은 `YYYY-MM-DD_` prefix 사용
- `_ko` suffix: `01_strategy/`, `02_implementation/` 문서에만 사용 (향후 다국어 대비). 회의록(`04_meetings/`)과 개발 진행(`03_development/`)에는 사용하지 않음
- Obsidian으로 문서 관리 중 (`.obsidian/`은 gitignore)

## Git LFS 관리

대용량 바이너리 파일은 Git LFS로 관리합니다.

### GitHub LFS 무료 할당량

| 항목 | 한도 |
|------|------|
| 저장소 용량 | 1 GB |
| 월간 대역폭 | 1 GB |

### 현재 LFS 사용량 (2026-02-12 기준)

| 분류 | 파일 수 | 크기 | 비고 |
|------|--------|------|------|
| mov (데모 영상) | 8개 | ~54 MB | `_00_work/260127-260211/` |
| zip (KB/스펙) | 5개 | ~80 MB | xframe5 KB 74MB + UASL/dist 소형 4개 |
| **합계** | **13개** | **~134 MB** | 무료 한도의 ~13% |

### 추적 대상 (`.gitattributes`)

```
*.mov filter=lfs diff=lfs merge=lfs -text
*.zip filter=lfs diff=lfs merge=lfs -text
```

### 관리 규칙

- 대용량 바이너리(영상, 압축파일, 이미지 등) 추가 시 반드시 LFS 추적 확인
- `git lfs ls-files --size`로 현재 사용량 확인 후 추가
- 무료 한도(1GB) 초과 전 정리 또는 유료 전환 검토
- 새로운 확장자 추가 시 `.gitattributes`에 `git lfs track` 반영
