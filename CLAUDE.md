# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

이 저장소는 **Coco 프로젝트의 문서 저장소**입니다. AI 코드 거버넌스 플랫폼인 Coco(구 Coder)의 전략 분석, 로드맵, API 레퍼런스 문서를 관리합니다.

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
│   ├── 2026-01-24_progress/
│   │   ├── vram_sizing.md
│   │   ├── architecture_mcp.md
│   │   ├── lightweight_model_qa.md
│   │   ├── qa_test_report/
│   │   ├── qa_examples/
│   │   ├── qa_update/
│   │   └── cli_test/
│   └── 2026-02-07_progress/
│       ├── README.md              # 1/26~2/7 진행 종합 요약
│       ├── uasl_spec/             # UASL/SUIS 스펙 문서
│       └── reports/               # CGF 비교, QA 개선 보고서
│
├── 04_meetings/           # 회의록
│   ├── 2025-12-26_softbase_xframe_ko.md
│   └── 2026-02-11_ShinsegaeInC.md
│
├── 05_knowledge_base/     # 기술 참고자료
│   ├── README.md          # xFrame5 아카이브 내용 기록
│   └── xframe5_knowledge_base.zip  # 대용량 (Git LFS)
│
├── _00_work/              # 작업 자료 스테이징
│   └── 260127-260211/     # 1/26~2/11 작업 원본
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
| `03_development/2026-02-07_progress/` | 2월 1주차 진행 - 코드생성, UASL, QA 개선 |
| `04_meetings/2026-02-11_ShinsegaeInC.md` | 신세계 I&C 솔루션 데모 회의록 |
| `05_knowledge_base/README.md` | xFrame5 아카이브 내용 기록 |

## 문서 관리 규칙

### 폴더 README
- 모든 주요 폴더(01~05)에 README.md가 존재하며 읽기 순서를 안내
- 새 문서 추가 시 해당 폴더 README.md에 반영

### 네비게이션 블록
- `01_strategy/`, `02_implementation/` 문서 상단에 이전/다음 네비게이션 존재
- 형식: `> **문서 N/M** | 이전: [...] | 다음: [...] | [폴더 인덱스](./README.md)`
- 위치: 메타데이터(날짜/버전) 아래, `---` 구분선 위
- 새 문서 추가 시 기존 문서의 네비게이션도 업데이트

### 03_development/ 체인
- 각 진행 폴더 README에 `이전 진행`/`다음 진행` 링크 체인 유지
- 새 진행 폴더 추가 시 직전 폴더 README에 다음 링크 추가

## Coco 핵심 개념

- **제품 정체성**: AI 코드 생성이 아닌 **AI 코드 거버넌스** 플랫폼
- **대상 환경**: 폐쇄망, 온프레미스 LLM, 규제 산업 기업
- **5대 USP**: 결정론적 출력, 표준 강제, 완전한 온프레미스, 감사 추적, LLM 추상화
- **제품 구성**: Coco Engine, Coco Studio, Coco CLI, Coco Admin, MCP Servers, Eclipse Plugin

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
