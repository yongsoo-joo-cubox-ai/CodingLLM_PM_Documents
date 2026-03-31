# SecernInfra

vLLM 인프라 고도화 확장 코드 레포. Track 1(IntraGenX) + Track 2(SecernCode) 공유 인프라.

## 개요

| 항목 | 내용 |
|------|------|
| **언어** | Go 1.24 (런타임) + Python 3.10 (빌드/Cython) |
| **역할** | 인증 게이트웨이, 모델 암호화, LiteLLM 배포 설정 |
| **배포** | Docker/K8s, Helm umbrella chart |
| **담당** | 주용수 (PM/인프라) |

## Stage → 컴포넌트 매핑

| Stage | 컴포넌트 | 설명 |
|-------|----------|------|
| Infra-S0 | `python/secernai_crypto/` + `cmd/keygen/` | 모델 가중치 암호화 (Tensorizer + libsodium) |
| Infra-S1 | `deploy/` (Helm, Docker, config) | LiteLLM 멀티 모델 + K8s 배포 |
| Infra-S2 | `cmd/gateway/` + `internal/` | Go 인증/RBAC 게이트웨이 |

## 관련 문서

- [vLLM 인프라 PRD](../02_implementation/08_vllm_infra_prd_ko.md) — 요구사항 (v0.3)
- [vLLM 인프라 로드맵](../02_implementation/09_vllm_infra_roadmap_ko.md) — 실행 계획
- [SecernCode 현황](../02_implementation/07_secerncode_status_ko.md) — Track 2 연계
