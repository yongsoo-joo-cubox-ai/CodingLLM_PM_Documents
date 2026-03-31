# Infra-S0: 모델 가중치 암호화 — 구현 기획서

> **상태**: 초안 스텁. Infra-S0 착수 시 상세 작성 예정.

## 목표

Tensorizer + libsodium을 활용하여 모델 가중치를 디스크 암호화, vLLM GPU On-the-fly 복호화.

## Phase 구성

| Phase | 기간 | 내용 |
|-------|------|------|
| Phase 1 | W1 | VRAM 벤치마크 + Tensorizer 환경 구축 |
| Phase 2 | W1-2 | Tensorizer 직렬화 + MinIO 연동 |
| Phase 3 | W3-4 | libsodium 암호화 + secernai-keygen CLI (Go) |
| Phase 4 | W5 | vLLM 커스텀 로더 + Cython .so 빌드 |
| Phase 5 | W6 | S3 연동 + E2E 테스트 + Docker 이미지 |

## 관련 문서

- PRD §4.1: 모델 가중치 암호화 요구사항
- 로드맵 §4: Infra-S0 상세
