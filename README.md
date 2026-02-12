# Coco 프로젝트 문서

국내 SI 사업을 위한 범용 AI 코딩 어시스턴스 프로젝트 문서 저장소

> 기존 Coder에서 **Coco**로 제품명 변경 (2026-02)

---

## 개요

**Coco** (Coordinated Coding)는 AI 코드 생성이 아닌 **AI 코드 거버넌스** 플랫폼입니다.

- **대상 환경**: 폐쇄망, 온프레미스 LLM, 규제 산업 기업
- **핵심 USP**: 결정론적 출력, 표준 강제, 완전한 온프레미스, 감사 추적, LLM 추상화

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
| [[01_strategy/executive_summary_ko\|executive_summary]] | 경영진 요약 - 프로젝트 개요 및 핵심 가치 |
| [[01_strategy/competitive_strategy_ko\|competitive_strategy]] | 경쟁 전략 - 상세 경쟁사 분석 및 차별화 전략 |
| [[01_strategy/regulatory_environment_ko\|regulatory_environment]] | 규제 환경 - 국내 AI 규제 및 컴플라이언스 |

### 02_implementation/ - 구현 문서

| 문서 | 설명 |
|------|------|
| [[02_implementation/roadmap_ko\|roadmap]] | 구현 로드맵 - Phase 1/2 기능 명세 |
| [[02_implementation/resource_plan_ko\|resource_plan]] | 투입 인력 및 로드맵 |
| [[02_implementation/phase2_tech_stack_ko\|phase2_tech_stack]] | Phase 2 기술 스택 및 스터디 가이드 |
| [[02_implementation/cost_analysis_ko\|cost_analysis]] | 비용 분석 - TCO 및 ROI 계산 |
| [[02_implementation/api_reference_ko\|api_reference]] | API 레퍼런스 - 엔드포인트 명세 |

### 03_development/ - 개발 진행 자료

| 폴더 | 설명 |
|------|------|
| `2026-01-15_project_intro/` | 프로젝트 소개 및 초기 벤치마크 |
| `2026-01-24_progress/` | 1월 4주차 진행 현황 (QA, CLI 테스트) |
| `2026-02-07_progress/` | 2월 1주차 진행 (코드생성, UASL, QA 개선) |

상세: [[03_development/README\|개발 자료 인덱스]]

### 04_meetings/ - 회의록

| 문서 | 설명 |
|------|------|
| [[04_meetings/2025-12-26_softbase_xframe_ko\|2025-12-26_softbase_xframe]] | SOFTBase xFrame AI 기능 도입 논의 |
| [[04_meetings/2026-02-11_ShinsegaeInC\|2026-02-11_ShinsegaeInC]] | 신세계 I&C 솔루션 데모 |

### 05_knowledge_base/ - 기술 참고자료

| 항목 | 설명 |
|------|------|
| xFrame5 | 압축 아카이브로 보관 (332MB, ~26,000 파일) |

상세: [[05_knowledge_base/README\|Knowledge Base 인덱스]]

---

## 읽기 순서

프로젝트를 처음 접하는 경우 아래 순서로 읽기를 권장합니다:

1. **[[01_strategy/executive_summary_ko\|경영진 요약]]** - 프로젝트 개요 파악
2. **[[01_strategy/competitive_strategy_ko\|경쟁 전략]]** - 시장 분석 및 차별화 포인트
3. **[[02_implementation/roadmap_ko\|구현 로드맵]]** - 구현 계획 및 마일스톤
4. **[[02_implementation/cost_analysis_ko\|비용 분석]]** - 투자 대비 효과

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

상세: [[02_implementation/api_reference_ko\|API 레퍼런스]]

### 규제 관련

규제 환경 및 컴플라이언스 요구사항: [[01_strategy/regulatory_environment_ko\|규제 환경]]

---

## 문서 명명 규칙

| 규칙 | 설명 | 예시 |
|------|------|------|
| 언어 | 영문 소문자 + 언더스코어 | `executive_summary.md` |
| 날짜 | `YYYY-MM-DD_` prefix (회의록) | `2025-12-26_softbase.md` |
| suffix | `_ko` (향후 다국어 대비) | `roadmap_ko.md` |

---

*마지막 업데이트: 2026-02-11*
