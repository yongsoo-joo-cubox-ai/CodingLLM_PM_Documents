# 07. 오픈소스 프로젝트 심층 분석

Coco / IntraGenX 프로젝트에서 활용하는 핵심 오픈소스 프로젝트의 심층 기술 분석 문서입니다.

각 문서는 프로젝트의 아키텍처, 코드 구조, 핵심 메커니즘을 코드 레벨까지 분석하며, Coco/IntraGenX와의 통합 포인트를 상세히 다룹니다.

## 읽기 순서

| # | 파일 | 설명 | 문서번호 |
|---|------|------|----------|
| 1 | [01_vllm_analysis.md](./01_vllm_analysis.md) | vLLM 심층 분석 — LLM 추론 엔진 (PagedAttention, V1 엔진, 분산 추론) | SAI-KB-2026-002 |
| 2 | [02_litellm_analysis.md](./02_litellm_analysis.md) | LiteLLM 심층 분석 — LLM 프록시/라우터 (Provider 추상화, AI Gateway, 비용 추적) | SAI-KB-2026-003 |
| 3 | [03_opencode_analysis.md](./03_opencode_analysis.md) | OpenCode 심층 분석 — AI 코딩 에이전트 (Agent 루프, MCP/LSP, 모노레포) | SAI-KB-2026-004 |

## 프로젝트 비교 요약

| 항목 | vLLM | LiteLLM | OpenCode |
|------|------|---------|----------|
| **역할** | LLM 추론 엔진 | LLM 프록시/라우터 | AI 코딩 에이전트 |
| **언어** | Python | Python | TypeScript |
| **라이선스** | Apache 2.0 | MIT + Enterprise | MIT |
| **코드 규모** | 1,452 파일, 544K LOC | 1,707 파일 | 327 파일 (CLI 패키지) |
| **IntraGenX 역할** | 추론 엔진 백엔드 | 멀티 모델 Gateway | 트랙 2 코딩 에이전트 기반 |
| **핵심 기술** | PagedAttention, Continuous Batching | Provider 추상화, AI Gateway | Agent 루프, MCP/LSP 통합 |

## 관련 문서

- [vLLM 인프라 고도화 R&D 계획](../02_implementation/06_vllm_rd_plan_ko.md) — vLLM 기반 인증/암호화/멀티 모델 계획
- [트랙 2 기술 전략 리서치](../01_strategy/05_track2_tech_strategy_ko.md) — OpenCode 기반 코딩 에이전트 전략
- [프로젝트 용어집](../05_knowledge_base/glossary_ko.md) — vLLM, LiteLLM, OpenCode 용어 정의

## 서브모듈 위치

분석 대상 코드베이스는 `_public/` 하위 서브모듈에 있습니다 (읽기 전용 참조):

- `_public/vllm/` — https://github.com/vllm-project/vllm
- `_public/litellm/` — https://github.com/BerriAI/litellm
- `_public/opencode/` — https://github.com/anomalyco/opencode
