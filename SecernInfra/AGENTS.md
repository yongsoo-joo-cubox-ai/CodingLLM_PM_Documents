# AGENTS.md — SecernInfra

## 프로젝트 정보

- **레포명**: SecernInfra
- **언어**: Go 1.24 + Python 3.10 (Cython)
- **역할**: vLLM 인프라 확장 (인증/암호화/배포)

## 디렉토리 구조

- `cmd/keygen/` — Go: secernai-keygen CLI (모델 암호화 키 관리)
- `cmd/gateway/` — Go: secernai-gateway (인증/RBAC 리버스 프록시) [Infra-S2]
- `internal/` — Go 내부 패키지 (auth, proxy, audit) [Infra-S2]
- `python/secernai_crypto/` — Python: 모델 암호화 + vLLM 커스텀 로더
- `deploy/` — Docker, Helm chart, K8s 매니페스트
- `docs/` — Stage별 구현 기획서

## 코드 보안 원칙

- 고객사에는 컴파일된 바이너리(Go→binary, Python→Cython .so)만 전달
- `python/secernai_crypto/encrypt.py`는 사내 전용, 외부 미배포
- 키 관리는 secernai-keygen(Go 바이너리)으로 분리
