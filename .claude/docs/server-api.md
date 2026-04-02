# 서버 환경 및 API 레퍼런스

> 이 문서는 CLAUDE.md의 레퍼런스입니다. 핵심 지침은 [CLAUDE.md](../../CLAUDE.md)를 참조하세요.

## 서버 환경

| 환경 | Studio 포트 | Engine 포트 | 비고 |
|------|-----------|-----------|------|
| **Demo** | 5174 | 3100 | 고객 데모용 (http://172.16.100.116:5174/landing) |
| **Dev** | 5173 | 3000 | 개발용 (기존) |
| **Playground** | 4000 + 프로젝트 ID | 동적 | Docker 기반 전체 앱 배포, FE-BE 연동 |

- Demo 도메인: https://coco.secernai.net

## GPU 서버 (vLLM 추론)

### 접속 정보

| 항목 | 내용 |
|------|------|
| **IP** | 172.100.100.3 |
| **SSH** | `ssh yongsoo@172.100.100.3` |
| **OS** | Ubuntu 22.04.5 LTS |
| **GPU** | 8× NVIDIA A100-SXM4-80GB |
| **CUDA** | 13.0 (Driver 580.95.05) |
| **운영 방식** | Docker 기반 (호스트에 pip 미설치) |
| **vLLM** | `vllm/vllm-openai:v0.14.0` (Python 3.12.12) |

> **주의**: Docker 내 DNS가 불안정하므로 `HF_HUB_OFFLINE=1` 환경변수 필수.

### GPU 할당 현황 (2026-04-01 기준)

| GPU | 컨테이너명 | 모델 | 포트 | 비고 |
|-----|-----------|------|------|------|
| 0, 1 | vllm-qwen-coder | Qwen2.5-Coder-32B-AWQ (TP=2) | 8000 | 코드 생성용 |
| 2 | vllm-secern | Qwen3-8B + LoRA Secern-Coder-Reason | 8001 | SecernCode용 |
| 3 | (비할당) | - | - | 벤치마크 전용 |
| 4, 5, 6, 7 | vllm-glm47 | GLM-4.7-AWQ (TP=4) | 8003 | - |

> GPU 3만 벤치마크/테스트에 사용 가능. 다른 GPU는 운영 중인 서비스에 할당됨.

---

## API 엔드포인트 요약

```bash
# 핵심 엔드포인트
POST /agent/agentic/v2/stream  # 스트리밍 코드 생성 (권장)
POST /agent/review             # 코드 리뷰
POST /agent/qa                 # 프레임워크 Q&A
GET  /agent/models             # 사용 가능 모델 목록
GET  /_health                  # 헬스 체크
```

> API 상세 명세: `02_implementation/05_api_reference_ko.md` 참조
