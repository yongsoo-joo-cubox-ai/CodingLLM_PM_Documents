# Coco 프로젝트 문서

국내 SI 사업을 위한 범용 AI 코딩 어시스턴스 프로젝트 문서 저장소

> 기존 Coder에서 **Coco**로 제품명 변경 (2026-02)
> 대외 브랜딩 **IntraGenX** 확정 — 시선AI(The Brain) + 대보DX(The Body) 합작 (2026-03)

---

## 개요

**Coco** (Coordinated Coding)는 AI 코드 생성이 아닌 **AI 코드 거버넌스** 플랫폼입니다.

- **대상 환경**: 폐쇄망, 온프레미스 LLM, 규제 산업 기업
- **6대 USP**: 결정론적 출력, 표준 강제, 완전한 온프레미스, Spec-Driven 코드 생성, 감사 추적, LLM 추상화
- **투트랙 전략**: 트랙 1(IntraGenX, SI 일괄 생성) → 트랙 2(코딩 에이전트, 개발자 자율형)

### 제품 구성

- **Coco Engine** (Rust 백엔드)
- **Coco Studio** (웹 기반 IDE)
- **Coco CLI** (명령줄 도구)
- **Coco Admin** (관리 콘솔)
- **MCP Servers** (프레임워크별 컴파일러/검증기)
- **Eclipse Plugin**

---

## 문서 구조

```
CodingLLM_PM_Documents/
├── 01_strategy/           # 전략 문서
├── 02_implementation/     # 구현 문서
├── 03_development/        # 개발 진행 자료
├── 04_meetings/           # 회의록
├── 05_knowledge_base/     # 기술 참고자료
├── _00_work/              # 작업 자료 스테이징
└── .obsidian/             # Obsidian 설정
```

### 01_strategy/ - 전략 문서

| 문서 | 설명 |
|------|------|
| [[01_strategy/01_executive_summary_ko\|executive_summary]] | 경영진 요약 - 프로젝트 개요 및 핵심 가치 |
| [[01_strategy/02_competitive_strategy_ko\|competitive_strategy]] | 경쟁 전략 - 상세 경쟁사 분석 및 차별화 전략 |
| [[01_strategy/03_regulatory_environment_ko\|regulatory_environment]] | 규제 환경 - 국내 AI 규제 및 컴플라이언스 |
| [[01_strategy/04_product_overview_ko\|product_overview]] | 제품 기능 소개 - 투트랙 제품군 정의 |

### 02_implementation/ - 구현 문서

| 문서 | 설명 |
|------|------|
| [[02_implementation/01_roadmap_ko\|roadmap]] | 구현 로드맵 - Phase 1/2 + 트랙 2 에이전트 |
| [[02_implementation/02_resource_plan_ko\|resource_plan]] | 투입 인력 및 로드맵 |
| [[02_implementation/04_phase2_tech_stack_ko\|phase2_tech_stack]] | Phase 2 기술 스택 및 스터디 가이드 |
| [[02_implementation/03_cost_analysis_ko\|cost_analysis]] | 비용 분석 - TCO 및 ROI 계산 |
| [[02_implementation/05_api_reference_ko\|api_reference]] | API 레퍼런스 - 엔드포인트 명세 |
| [[02_implementation/06_vllm_rd_plan_ko\|vllm_rd_plan]] | vLLM 인프라 고도화 R&D 계획 (인증/암호화/멀티 모델) |

### 03_development/ - 개발 진행 자료

| 폴더 | 설명 |
|------|------|
| `2026-01-15_project_intro/` | 프로젝트 소개 및 초기 벤치마크 |
| `2026-01-24_progress/` | 1월 4주차 진행 현황 (QA, CLI 테스트) |
| `2026-02-07_progress/` | 2월 1주차 진행 (코드생성, UASL, QA 개선) |
| `2026-02-12_progress/` | Coco Studio 기능 테스트 (7 TC, 71.4%) |
| `2026-03-19_progress/` | 3월 진행 (4B 파인튜닝, UASL v2/v3, 서버 분리, 부산은행 PoC) |

상세: [[03_development/README\|개발 자료 인덱스]]

### 04_meetings/ - 회의록

| 문서 | 설명 |
|------|------|
| [[04_meetings/2025-12-26_softbase_xframe\|2025-12-26_softbase_xframe]] | SOFTBase xFrame AI 기능 도입 논의 |
| [[04_meetings/2026-02-11_ShinsegaeInC\|2026-02-11_ShinsegaeInC]] | 신세계 I&C 솔루션 데모 |
| [[04_meetings/2026-03-17_dev_update\|2026-03-17_dev_update]] | 개발 현황 업데이트 (서버 분리, Playground, 부산은행 PoC) |

### 05_knowledge_base/ - 기술 참고자료

| 항목 | 설명 |
|------|------|
| xFrame5 | 압축 아카이브로 보관 (332MB, ~26,000 파일) |

상세: [[05_knowledge_base/README\|Knowledge Base 인덱스]]

---

## 읽기 순서

### 빠른 온보딩 (처음 접하는 분) — ~25분
1. [용어집](05_knowledge_base/glossary_ko.md) (~10분)
2. [경영진 요약](01_strategy/01_executive_summary_ko.md) (~15분)

### 전체 파악 (경영진/관리자) — 총 ~60분

| 순서 | 문서 | 소요 시간 | 난이도 | 선행 지식 |
|------|------|----------|--------|----------|
| 1 | [경영진 요약](01_strategy/01_executive_summary_ko.md) | ~15분 | ★☆☆ | 없음 |
| 2 | [경쟁 전략](01_strategy/02_competitive_strategy_ko.md) | ~20분 | ★★☆ | 경영진 요약 |
| 3 | [로드맵](02_implementation/01_roadmap_ko.md) | ~15분 | ★★☆ | 경영진 요약 |
| 4 | [비용 분석](02_implementation/03_cost_analysis_ko.md) | ~10분 | ★☆☆ | 없음 |

### 구현 상세 (개발자/PM) — 총 ~75분

| 순서 | 문서 | 소요 시간 | 난이도 | 선행 지식 |
|------|------|----------|--------|----------|
| 1 | [로드맵](02_implementation/01_roadmap_ko.md) | ~15분 | ★★☆ | 경영진 요약 권장 |
| 2 | [투입 인력](02_implementation/02_resource_plan_ko.md) | ~15분 | ★☆☆ | 로드맵 |
| 3 | [기술 스택](02_implementation/04_phase2_tech_stack_ko.md) | ~20분 | ★★★ | 로드맵 |
| 4 | [API 레퍼런스](02_implementation/05_api_reference_ko.md) | ~30분 | ★★★ | 기술 스택 |

### 개발 진행 현황
[2026-01-15](03_development/2026-01-15_project_intro/) → [2026-01-24](03_development/2026-01-24_progress/) → [2026-02-07](03_development/2026-02-07_progress/) → [2026-02-12](03_development/2026-02-12_progress/) → [2026-03-19](03_development/2026-03-19_progress/) (시간순)

---

## 빠른 참조

### API 엔드포인트

```bash
POST /agent/agentic/v2/stream  # 스트리밍 코드 생성 (권장)
POST /agent/review             # 코드 리뷰
POST /agent/qa                 # 프레임워크 Q&A
GET  /agent/models             # 사용 가능 모델 목록
GET  /_health                  # 헬스 체크
```

상세: [[02_implementation/05_api_reference_ko\|API 레퍼런스]]

### 규제 관련

규제 환경 및 컴플라이언스 요구사항: [[01_strategy/03_regulatory_environment_ko\|규제 환경]]

---

## Google Drive 동기화

이 저장소의 문서를 Google Drive 공유 드라이브(`CodingLLM_Project/01_Documents/`)로 단방향 미러링합니다. MD 파일은 DOCX로 변환되며, 원본 MD는 Git에만 보관합니다.

```bash
# 미리보기
bash .claude/scripts/sync-to-gdrive.sh --dry-run

# 실제 동기화
bash .claude/scripts/sync-to-gdrive.sh
```

- **사전 요구사항**: `brew install pandoc`, Google Drive 데스크톱 앱 마운트
- **Claude Code 사용 시**: `/sync-gdrive` 또는 `/sync-gdrive --dry-run`

---

## 문서 명명 규칙

| 규칙 | 설명 | 예시 |
|------|------|------|
| 언어 | 영문 소문자 + 언더스코어 | `executive_summary.md` |
| 날짜 | `YYYY-MM-DD_` prefix (회의록) | `2025-12-26_softbase.md` |
| suffix | `_ko` (전략/구현 문서만, 향후 다국어 대비) | `roadmap_ko.md` |

---

*마지막 업데이트: 2026-03-19*
