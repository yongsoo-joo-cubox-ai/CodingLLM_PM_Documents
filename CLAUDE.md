# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

이 저장소는 **Coco / IntraGenX 프로젝트의 문서 저장소**입니다. AI 코드 거버넌스 플랫폼인 Coco(구 Coder)의 전략 분석, 로드맵, API 레퍼런스 문서를 관리합니다.

> **대외 브랜딩**: IntraGenX (2026-03~) — 시선AI(The Brain, LLM 개발) + 대보DX(The Body, 애플리케이션 & 어플라이언스) 합작

## Coco / IntraGenX 핵심 개념

- **제품 정체성**: AI 코드 생성이 아닌 **AI 코드 거버넌스** 플랫폼
- **대외 브랜드**: IntraGenX — "AI 기반 차세대 시스템 개발 플랫폼" (시선AI + 대보DX 합작)
- **투트랙 전략**:
  - **트랙 1 (IntraGenX)**: Spec-Driven 일괄 코드 생성 — SI 프로젝트, Top-Down
  - **트랙 2 (코딩 에이전트)**: SecernCode(Go) 기반 자율형 에이전트 — 개발자, Bottom-Up (2026년 3월 MVP 완료, 시선AI 주도)
- **MCP 용어 구분**: 양쪽 모두 MCP(Model Context Protocol) 동일 프로토콜 사용, 용도가 다름 — 트랙 1: 코드 생성 엔진 서버(xframe5-compiler 등), 트랙 2: 개발 도구 접근 서버(Jira, Confluence 등)
- **대상 환경**: 폐쇄망, 온프레미스 LLM, 규제 산업 기업 (금융권 PoC 진행 중)
- **6대 USP**: ①결정론적 출력, ②표준 강제, ③완전한 온프레미스, ④Spec-Driven 코드 생성, ⑤감사 추적, ⑥LLM 추상화
- **제품 구성**: Coco Engine, Coco Studio, Coco CLI, Coco Admin, MCP Servers, Eclipse Plugin
- **지원 프레임워크**: xFrame5, WebSquare, Vue 3, React 19, Spring Boot

## 문서 아키텍처

> 상세: [.claude/docs/document-architecture.md](.claude/docs/document-architecture.md)

### 투트랙 문서 체계

| 구분 | 트랙 1 (IntraGenX) | 트랙 2 (SecernCode) |
|------|--------------------|--------------------|
| **전략·로드맵** | PM 레포 `01_strategy/`, `02_implementation/` | 같은 로드맵의 "트랙 2" 섹션 |
| **기술 상세** | PM 레포 구현 문서 | `SecernCode/` 서브모듈 `docs/` |
| **현황 추적** | 로드맵 내 Phase 상태 | `07_secerncode_status_ko.md` |
| **문서 소유** | PM (주용수) | 개발팀 (황영준M) — PM은 현황 보고서만 |

### Stage / Phase 용어 체계

- **Stage** (대단계): PM 로드맵에서 관리. Stage 0~4 + Alpha
- **Phase** (구현 단위): 각 Stage 내부에서 개발팀이 세분화. 예: Stage 0 = Phase 1~6
- 향후 Stage N마다 자체 Phase 1~M 체계를 가짐
- 트랙 1의 "Phase 1/2"는 트랙 2와 **독립적**인 체계

### 레포 간 교차 참조 규칙

| 방향 | 방식 | 이유 |
|------|------|------|
| **PM → SecernCode** | 상대경로 링크 (`../SecernCode/docs/...`) | 서브모듈이 PM 안에 포함 |
| **SecernCode → PM** | **텍스트로 문서명만 참조** (링크 없음) | 독립 레포, PM 경로 접근 불가 |

### 서브모듈 문서 관리

- SecernCode 문서 변경: SecernCode 레포 커밋 → PM 레포에서 `git add SecernCode`
- PM 레포 `02_implementation/README.md`에 서브모듈 문서 참조 테이블 유지
- 새 서브모듈 추가 시: CLAUDE.md + `.claude/docs/document-structure.md` + README 모두 업데이트

### 모델 버전 관리

- 트랙 1(Qwen2.5)과 트랙 2(Qwen3.5)는 현재 모델이 다를 수 있음
- 각 트랙 담당자가 관리, 불일치 시 로드맵에 주석 명시
- 통합 시점: Stage 1 이후 확정 예정

### 향후 Stage 기획서 작성

- 위치: `SecernCode/docs/stage{N}_spec.md`
- PM 반영: 로드맵 Stage 테이블 + 현황 보고서 + README
- 필수 항목: 목표, Phase 분류, 아키텍처 변경점, 리스크, 타임라인, PM 문서 매핑

## 문서 관리 규칙 (요약)

> 상세: [.claude/docs/document-rules.md](.claude/docs/document-rules.md)

- **파일명**: 영문 소문자 + 언더스코어. `01_strategy/`, `02_implementation/`는 `{NN}_{이름}_ko.md`
- **폴더 README**: 모든 주요 폴더(01~07)에 존재. 새 문서 추가 시 반영 필수
- **네비게이션**: `01_strategy/`, `02_implementation/` 상단에 이전/다음 링크
- **TL;DR**: 정식 문서에 필수 (blockquote, 3~5 불릿, 대상 독자, 소요 시간)
- **메타데이터**: `SAI-{카테고리}-{년도}-{순번}` 문서번호 체계
- **변경이력**: 모든 정식 문서 하단에 테이블 포함
- **용어집**: `05_knowledge_base/glossary_ko.md` — 새 용어 도입 시 반영
- **`_ko` suffix**: `01_strategy/`, `02_implementation/`에만 사용

## 문서 작업 시 참고사항

- 모든 문서는 **한글**로 작성
- 회의록은 `YYYY-MM-DD_` prefix 사용
- Obsidian으로 문서 관리 중 (`.obsidian/`은 gitignore)

## 레퍼런스 문서

상세 정보는 `.claude/docs/` 폴더의 레퍼런스 문서를 참조한다.

| 문서 | 내용 |
|------|------|
| [document-structure.md](.claude/docs/document-structure.md) | 폴더 구조 트리 + 전체 문서 목록 |
| [document-rules.md](.claude/docs/document-rules.md) | 파일명, 네비게이션, TL;DR, 메타데이터 템플릿 상세 |
| [document-architecture.md](.claude/docs/document-architecture.md) | 투트랙 체계, Stage/Phase, 교차 참조, 서브모듈 관리, 확장 가이드 |
| [server-api.md](.claude/docs/server-api.md) | 서버 환경 (Demo/Dev/Playground) + API 엔드포인트 |
| [gdrive-sync.md](.claude/docs/gdrive-sync.md) | Google Drive 동기화 커맨드, 스크립트, 사전 요구사항 |
| [git-lfs.md](.claude/docs/git-lfs.md) | LFS 할당량, 사용량, 추적 대상, 관리 규칙 |
