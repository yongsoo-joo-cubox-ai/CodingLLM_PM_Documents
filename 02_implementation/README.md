# 02_implementation - 구현 문서

Coco / IntraGenX 프로젝트의 구현 계획 및 기술 문서입니다.

## 읽기 순서

| 순서 | 문서 | 설명 | 최종 업데이트 |
|------|------|------|-------------|
| 1 | [01_roadmap_ko.md](./01_roadmap_ko.md) | Phase 1/2 기능 + 트랙 2 코딩 에이전트 로드맵 | 2026-03-19 (v5.2) |
| 2 | [02_resource_plan_ko.md](./02_resource_plan_ko.md) | 투입 인력, 트랙별 역할 분담 | 2026-03-19 (v5.1) |
| 3 | [03_cost_analysis_ko.md](./03_cost_analysis_ko.md) | TCO/ROI 비용 분석 | 2026-03-19 (v2.1) |
| 4 | [04_phase2_tech_stack_ko.md](./04_phase2_tech_stack_ko.md) | Phase 2 + 트랙 2 기술 스택 가이드 | 2026-03-19 (v4.3) |
| 5 | [05_api_reference_ko.md](./05_api_reference_ko.md) | API 엔드포인트 명세 (레퍼런스) | 2026-03-19 (v3.1) |

### 참고 문서

| 문서 | 설명 | 비고 |
|------|------|------|
| [06_vllm_rd_plan_ko.md](./06_vllm_rd_plan_ko.md) | vLLM 인프라 고도화 R&D — 인증/암호화/LiteLLM 멀티 모델 셀렉션 (Gemini Deep Research) | 참고자료 |
| [07_secerncode_status_ko.md](./07_secerncode_status_ko.md) | SecernCode(Go) Track 2 구현 현황 보고서 | 현황 |
| [08_vllm_infra_prd_ko.md](./08_vllm_infra_prd_ko.md) | vLLM 인프라 고도화 PRD — 모델 암호화/LiteLLM 멀티 모델/Go 인증 게이트웨이 | PRD (v0.3) |
| [09_vllm_infra_roadmap_ko.md](./09_vllm_infra_roadmap_ko.md) | vLLM 인프라 고도화 로드맵 — Infra-S0~S3 실행 계획 + SecernInfra 레포 | 로드맵 (v1.0) |

### SecernCode 기술 문서 (서브모듈)

| 문서 | 설명 | 비고 |
|------|------|------|
| [secerncode_implementation_spec_v2.md](../SecernCode/docs/secerncode_implementation_spec_v2.md) | SecernCode 구현 기획서 — 8-Layer 아키텍처, Phase 1~6 상세 설계 (Stage 0 범위) | 기술 상세 (v2.0) |
| [feature_summary.md](../SecernCode/docs/feature_summary.md) | SecernCode 기능 요약 | 참고 |

> **참고**: SecernCode 문서는 별도 서브모듈(`SecernCode/`)에서 관리되며, 변경 시 서브모듈 커밋이 별도로 필요하다.

### SecernInfra 기술 문서 (서브모듈)

| 문서 | 설명 | 비고 |
|------|------|------|
| [stage0_spec.md](../SecernInfra/docs/stage0_spec.md) | Infra-S0 구현 기획서 — 모델 가중치 암호화 | 기술 상세 |
| [stage1_spec.md](../SecernInfra/docs/stage1_spec.md) | Infra-S1 구현 기획서 — LiteLLM + K8s 배포 | 기술 상세 |
| [stage2_spec.md](../SecernInfra/docs/stage2_spec.md) | Infra-S2 구현 기획서 — Go 인증 게이트웨이 | 기술 상세 |

> **참고**: SecernInfra 문서는 별도 서브모듈(`SecernInfra/`)에서 관리되며, 변경 시 서브모듈 커밋이 별도로 필요하다.

## 문서 관계

- roadmap이 전체 기능 계획 (트랙 1 Phase 1/2 + 트랙 2 에이전트) → resource_plan이 인력/일정 → cost_analysis가 비용 정당성
- phase2_tech_stack은 Phase 2 및 트랙 2 개발자를 위한 기술 상세
- api_reference는 개발자용 레퍼런스 (필요 시 참조)
- SecernCode 구현 기획서(`SecernCode/docs/`)가 트랙 2 Stage 0의 Phase 상세 설계 → 07_secerncode_status_ko가 PM 관점 현황 요약
- vLLM 인프라 PRD(08)가 요구사항 → 09_vllm_infra_roadmap이 실행 계획 → SecernInfra/가 구현 코드
- 모든 문서 2026-03-31 기준 최신화 완료
