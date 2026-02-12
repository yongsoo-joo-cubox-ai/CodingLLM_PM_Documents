# 2026-01-24: 1월 4주차 진행

1월 4주차(01/20 ~ 01/26) 개발 진행 사항을 정리합니다. VRAM 산정, MCP 아키텍처 전환, QA 기능 검증 및 CLI 도구 테스트를 수행했습니다.

> **이전 진행**: [2026-01-15 프로젝트 소개](../2026-01-15_project_intro/) - 초기 벤치마크, 기술 스택 소개
> **다음 진행**: [2026-02-07 2월 1주차 진행](../2026-02-07_progress/) - 코드생성 개선, UASL 스펙, Coco 제품 정의

---

## 주요 성과 요약

- VRAM 크기별 동시사용자 수 산정 (Qwen2.5-32B 기준 7명 최적)
- MCP 기반 아키텍처 전환 설계 (프레임워크 디커플링)
- 경량 모델(Gemma3 1B/4B) QA 기능 테스트
- xFrame5 코드 생성 및 QA 기능 소프트베이스 검토
- CLI 도구(generate, qa, review) 테스트

---

## 포함 문서

### 루트 문서

| 문서 | 설명 |
|------|------|
| `vram_sizing.md` | VRAM 크기 산정 - 동시사용자 수별 KV Cache 계산, 시나리오 분석 |
| `architecture_mcp.md` | MCP 아키텍처 전환 - 프레임워크별 로직을 MCP 서버로 분리하는 설계 |
| `lightweight_model_qa.md` | 경량 모델 QA 테스트 - MacBook에서 Gemma3 1B/4B Ollama 실행 결과 |

### 하위 폴더

| 폴더 | 파일 수 | 설명 |
|------|--------|------|
| `qa_test_report/` | 2 MD + 3 PNG | 소프트베이스 xFrame5 코드 생성 및 QA 기능 검토 보고서 |
| `qa_examples/` | 1 MD + 6 TXT | xFrame5 실제 Q&A 예제 (그리드, 팝업 등 5개 질문) |
| `qa_update/` | 1 MD + 1 PNG | QA 프롬프트 스타일 변경 및 기능 업데이트 내역 |
| `cli_test/` | 1 MD + 1 README | Coco CLI 테스트 결과 (generate, qa, review 명령어) |

---

## 세부 내용

### VRAM 산정

Qwen2.5-32B-AWQ 모델, 4x RTX 2080 Ti (44GB) 환경 기준:

| 시나리오 | max_model_len | 동시사용자 | 용도 |
|---------|--------------|-----------|------|
| Standard | 8,192 | 10명 | 단순 Q&A |
| **Sweet Spot** | **12,288** | **7명** | **코딩 에이전트 (권장)** |
| Deep Context | 16,384 | 5명 | 복잡한 디버깅 |

### MCP 아키텍처 전환

기존: 프레임워크별 로직(xFrame5, Spring 등)이 소스코드에 하드코딩
→ 변경: MCP 서버로 분리하여 설정 기반 통합

- **Coco**: 오케스트레이션 + 범용 패스 (파싱, 심볼 링킹, 검증)
- **MCP 서버**: 프레임워크별 코드 생성, 정규화, 스키마 검증

### QA 기능 검증

- **qa_test_report/**: 소프트베이스 의뢰 xFrame5 코드 생성 품질 + QA 답변 정확성 검토
- **qa_examples/**: 그리드 루핑, 정렬, 필터, 팝업 등 실제 질문 5건과 답변
- **qa_update/**: QA 프롬프트를 "간결한 기술 답변" 스타일로 변경

### CLI 테스트

Eclipse 플러그인, curl 외에 CLI 실행 방식 추가:

> **참고**: 아래 CLI 명령어는 당시 제품명 "Coder" 기준입니다. 이후 제품명이 Coco로 변경되었습니다.

- `coder generate` - 코드 생성
- `coder qa` - 프레임워크 Q&A
- `coder review` - 코드 리뷰
