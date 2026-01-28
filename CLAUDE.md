# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

이 저장소는 **Coder 프로젝트의 문서 저장소**입니다. AI 코드 거버넌스 플랫폼인 Coder의 전략 분석, 로드맵, API 레퍼런스 문서를 관리합니다.

## Document Structure

```
CodingLLM_PM_Documents/
├── 01_strategy/           # 전략 문서
│   ├── executive_summary_ko.md
│   ├── competitive_strategy_ko.md
│   └── regulatory_environment_ko.md
│
├── 02_implementation/     # 구현 문서
│   ├── roadmap_ko.md
│   ├── resource_plan_ko.md
│   ├── phase2_tech_stack_ko.md
│   ├── cost_analysis_ko.md
│   └── api_reference_ko.md
│
├── 03_development/        # 개발 진행 자료
│   ├── README.md          # 개발 현황 인덱스
│   ├── 2026-01-15_project_intro/
│   │   ├── project_introduction.md
│   │   ├── load_test_qwen32b.md
│   │   └── model_benchmark.md
│   └── 2026-01-24_progress/
│       ├── vram_sizing.md
│       ├── architecture_mcp.md
│       ├── lightweight_model_qa.md
│       ├── qa_test_report/
│       ├── qa_examples/
│       ├── qa_update/
│       └── cli_test/
│
├── 04_meetings/           # 회의록
│   └── 2025-12-26_softbase_xframe_ko.md
│
├── 05_knowledge_base/     # 기술 참고자료
│   ├── README.md          # xFrame5 아카이브 내용 기록
│   └── xframe5_knowledge_base.zip  # 대용량 (Git 제외)
│
└── .obsidian/             # Obsidian 설정
```

### 문서 목록

| 경로 | 설명 |
|------|------|
| `01_strategy/executive_summary_ko.md` | 경영진 요약 - 프로젝트 개요 및 핵심 가치 |
| `01_strategy/competitive_strategy_ko.md` | 경쟁 전략 - 상세 경쟁사 분석 |
| `01_strategy/regulatory_environment_ko.md` | 규제 환경 - AI 규제 및 컴플라이언스 |
| `02_implementation/roadmap_ko.md` | 구현 로드맵 - Phase 1/2 기능 명세 |
| `02_implementation/resource_plan_ko.md` | 투입 인력 및 로드맵 - Phase별 인력/일정 계획 |
| `02_implementation/phase2_tech_stack_ko.md` | Phase 2 기술 스택 - 학습 자료/구현 가이드 |
| `02_implementation/cost_analysis_ko.md` | 비용 분석 - TCO 및 ROI |
| `02_implementation/api_reference_ko.md` | API 레퍼런스 - 엔드포인트 명세 |
| `03_development/` | 개발 진행 자료 - 테스트, 벤치마크 |
| `05_knowledge_base/README.md` | xFrame5 아카이브 내용 기록 |

## Coder 핵심 개념

- **제품 정체성**: AI 코드 생성이 아닌 **AI 코드 거버넌스** 플랫폼
- **대상 환경**: 폐쇄망, 온프레미스 LLM, 규제 산업 기업
- **5대 USP**: 결정론적 출력, 표준 강제, 완전한 온프레미스, 감사 추적, LLM 추상화

## API 엔드포인트 요약

```bash
# 핵심 엔드포인트
POST /agent/agentic/v2/stream  # 스트리밍 코드 생성 (권장)
POST /agent/review             # 코드 리뷰
POST /agent/qa                 # 프레임워크 Q&A
GET  /agent/models             # 사용 가능 모델 목록
GET  /_health                  # 헬스 체크
```

## 문서 작업 시 참고사항

- 모든 문서는 **한글**로 작성
- 파일명은 **영문 소문자 + 언더스코어** 사용
- 회의록은 `YYYY-MM-DD_` prefix 사용
- `_ko` suffix 유지 (향후 다국어 대비)
- Obsidian으로 문서 관리 중 (`.obsidian/` 폴더 존재)

