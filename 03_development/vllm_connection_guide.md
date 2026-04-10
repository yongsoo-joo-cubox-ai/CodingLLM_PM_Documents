# vLLM 서버 연동 가이드 (SecernCode 개발자용)

| 항목 | 내용 |
|------|------|
| **작성일** | 2026년 4월 6일 |
| **버전** | v1.0 |
| **대상** | SecernCode 연동 테스트를 수행할 개발자 |

---

> **TL;DR**
> - GPU 서버 `172.100.100.3`에 vLLM 컨테이너 3개가 운영 중 (포트 8000 / 8001 / 8003)
> - SecernCode에서 연동하려면 `LOCAL_ENDPOINT` 환경변수 또는 `.secerncode.json` 설정만 잡으면 됨
> - API Key 인증 없음 (로컬 vLLM이므로 `dummy` 사용)
> - 사내 네트워크에서만 접근 가능
> - 소요 시간: 약 5분

---

## 1. 서버 정보

| 항목 | 내용 |
|------|------|
| **IP** | `172.100.100.3` |
| **OS** | Ubuntu 22.04.5 LTS |
| **GPU** | 8x NVIDIA A100-SXM4-80GB |
| **vLLM** | `vllm/vllm-openai:v0.14.0` |
| **네트워크** | 사내망 전용 (외부 접근 불가) |

---

## 2. 모델 / 포트 매핑

> 2026-04-06 실측 확인

| 포트 | API 모델 ID (`model` 필드에 사용) | 실제 모델 (root) | GPU | max_model_len | 용도 |
|------|----------------------------------|-----------------|-----|---------------|------|
| **8000** | `qwen2.5-coder` | Qwen/Qwen2.5-Coder-32B-Instruct-AWQ | 0, 1 (TP=2) | 32,768 | 코드 생성 |
| **8001** | `Qwen/Qwen3-8B` | Qwen/Qwen3-8B | 2 | 20,480 | SecernCode 베이스 |
| **8001** | `Secern-Coder-Reason` | /adapters/Secern-Coder-Reason (LoRA) | 2 | - | SecernCode LoRA |
| **8003** | `glm-4.7` | QuantTrio/GLM-4.7-AWQ | 4, 5, 6, 7 (TP=4) | 131,072 | 범용 |

> - GPU 3은 벤치마크 전용으로 비할당 상태입니다.
> - **API 모델 ID**가 `--served-model-name`으로 별칭 설정된 경우가 있습니다. 반드시 위 표의 ID를 사용하세요.

---

## 3. API 접속 확인 (curl)

vLLM은 **OpenAI-compatible API**를 제공합니다. 먼저 curl로 서버 상태를 확인하세요.

### 3.1 헬스 체크

```bash
# 서버 응답 확인
curl http://172.100.100.3:8000/health

# 로드된 모델 목록 조회
curl http://172.100.100.3:8000/v1/models | python3 -m json.tool
```

### 3.2 채팅 요청 테스트

```bash
# Qwen2.5-Coder-32B (포트 8000) — model ID: "qwen2.5-coder"
curl -X POST http://172.100.100.3:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5-coder",
    "messages": [
      {"role": "user", "content": "Hello, are you working?"}
    ],
    "max_tokens": 128
  }'
```

```bash
# Qwen3-8B 베이스 (포트 8001) — model ID: "Qwen/Qwen3-8B"
curl -X POST http://172.100.100.3:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen3-8B",
    "messages": [
      {"role": "user", "content": "Hello, are you working?"}
    ],
    "max_tokens": 128
  }'
```

```bash
# Secern-Coder-Reason LoRA (포트 8001) — model ID: "Secern-Coder-Reason"
curl -X POST http://172.100.100.3:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Secern-Coder-Reason",
    "messages": [
      {"role": "user", "content": "Hello, are you working?"}
    ],
    "max_tokens": 128
  }'
```

```bash
# GLM-4.7 (포트 8003) — model ID: "glm-4.7"
curl -X POST http://172.100.100.3:8003/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "glm-4.7",
    "messages": [
      {"role": "user", "content": "Hello, are you working?"}
    ],
    "max_tokens": 128
  }'
```

> **주의**: `model` 필드에는 반드시 위 예시의 ID를 그대로 사용하세요. 서버에 `--served-model-name` 별칭이 설정되어 있어서 원본 모델 경로(예: `Qwen/Qwen2.5-Coder-32B-Instruct-AWQ`)로는 호출이 안 될 수 있습니다.

### 3.3 스트리밍 요청

```bash
curl -X POST http://172.100.100.3:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5-coder",
    "messages": [
      {"role": "user", "content": "Python으로 피보나치 함수 작성해줘"}
    ],
    "max_tokens": 512,
    "stream": true
  }'
```

---

## 4. SecernCode 연동 설정

### 4.1 방법 A: 환경변수 (가장 간단)

```bash
# vLLM 엔드포인트 지정
export LOCAL_ENDPOINT=http://172.100.100.3:8001/v1

# SecernCode 실행
./secerncode          # TUI 모드
./secerncode serve    # WebUI 모드 (http://localhost:4096)
./secerncode -p "..." # CLI 모드 (단발 질의)
```

> SecernCode용 모델은 포트 **8001** (Qwen3-8B + LoRA)입니다.

### 4.2 방법 B: 설정 파일 (.secerncode.json)

프로젝트 루트 또는 `~/.secerncode.json`에 아래 내용을 작성합니다.

```json
{
  "providers": {
    "local": {
      "apiKey": "dummy",
      "endpoint": "http://172.100.100.3:8001/v1"
    }
  },
  "agents": {
    "coder": {
      "model": "local.Qwen/Qwen3-8B",
      "maxTokens": 8192
    },
    "task": {
      "model": "local.Qwen/Qwen3-8B",
      "maxTokens": 4096
    },
    "summarizer": {
      "model": "local.Qwen/Qwen3-8B",
      "maxTokens": 4096
    },
    "title": {
      "model": "local.Qwen/Qwen3-8B",
      "maxTokens": 1024
    }
  }
}
```

### 4.3 방법 C: 다중 모델 사용 (고급)

서로 다른 포트의 모델을 에이전트별로 분리할 수 있습니다.

```json
{
  "providers": {
    "local": {
      "apiKey": "dummy",
      "endpoint": "http://172.100.100.3:8001/v1"
    }
  },
  "models": {
    "large": {
      "endpoint": "http://172.100.100.3:8000/v1",
      "apiModel": "qwen2.5-coder",
      "maxTokens": 16384
    },
    "small": {
      "endpoint": "http://172.100.100.3:8001/v1",
      "apiModel": "Qwen/Qwen3-8B",
      "maxTokens": 8192
    }
  },
  "agents": {
    "coder": {
      "model": "local.large",
      "maxTokens": 8192
    },
    "task": {
      "model": "local.small",
      "maxTokens": 4096
    },
    "summarizer": {
      "model": "local.small",
      "maxTokens": 4096
    },
    "title": {
      "model": "local.small",
      "maxTokens": 1024
    }
  }
}
```

> coder(코드 생성)는 32B 대형 모델, 나머지는 8B 경량 모델로 라우팅하는 구성입니다.

### 4.4 설정 우선순위

| 순위 | 위치 | 설명 |
|------|------|------|
| 1 | `LOCAL_ENDPOINT` 환경변수 | 최우선 |
| 2 | 프로젝트 루트 `.secerncode.json` | 프로젝트별 설정 |
| 3 | `~/.secerncode.json` | 사용자 글로벌 설정 |
| 4 | `$XDG_CONFIG_HOME/secerncode/.secerncode.json` | XDG 표준 |
| 5 | 기본값 (`localhost:8000`) | 폴백 |

---

## 5. 연동 확인 체크리스트

| 단계 | 명령어 | 기대 결과 |
|------|--------|----------|
| 1. 네트워크 | `ping 172.100.100.3` | 응답 있음 |
| 2. 포트 | `curl http://172.100.100.3:8001/health` | `200 OK` |
| 3. 모델 목록 | `curl http://172.100.100.3:8001/v1/models` | 모델 JSON 응답 |
| 4. 추론 | 3.2절 curl 명령 | 응답 텍스트 생성 |
| 5. SecernCode | `./secerncode` 실행 후 아무 질문 | 정상 응답 |

---

## 6. 트러블슈팅

### 연결이 안 될 때

```bash
# 네트워크 확인
ping 172.100.100.3
telnet 172.100.100.3 8001

# VPN 또는 사내망 연결 상태 확인
# → 172.100.100.x 대역은 사내 전용 네트워크입니다
```

### "Model not found" 에러

```bash
# 실제 로드된 모델명 확인
curl http://172.100.100.3:8001/v1/models | python3 -m json.tool

# 출력된 "id" 값을 model 필드나 .secerncode.json의 apiModel에 그대로 사용
# 현재 실측값: "Qwen/Qwen3-8B", "Secern-Coder-Reason" (포트 8001)
#             "qwen2.5-coder" (포트 8000), "glm-4.7" (포트 8003)
```

### 응답이 매우 느릴 때

- 다른 사용자가 동일 GPU에 요청 중일 수 있음 (GPU 2는 SecernCode 전용이라 경합 적음)
- `max_tokens`를 줄여서 테스트 (128 정도로)
- vLLM 컨테이너 상태 확인은 서버 관리자(주용수)에게 문의

### SecernCode가 모델을 못 찾을 때

```bash
# 환경변수 확인
echo $LOCAL_ENDPOINT

# SecernCode 디버그 모드로 실행
./secerncode --debug
```

---

## 7. 주의사항

- **API Key 불필요**: 로컬 vLLM이므로 인증 없음. 설정에는 `"dummy"` 입력
- **GPU 3번 사용 금지**: 벤치마크 전용 — 임의로 컨테이너 띄우지 말 것
- **동시 요청 제한**: vLLM이 자체 큐잉하지만, 대규모 배치 요청은 다른 사용자에게 영향
- **모델 변경 금지**: 운영 중인 컨테이너의 모델을 임의 변경하지 말 것
- **서버 접속(SSH)**: 컨테이너 재시작 등이 필요하면 서버 관리자에게 요청

---

## 8. 참고 API 엔드포인트

vLLM OpenAI-compatible API 전체 목록:

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/health` | 헬스 체크 |
| GET | `/v1/models` | 로드된 모델 목록 |
| POST | `/v1/chat/completions` | 채팅 완성 (추천) |
| POST | `/v1/completions` | 텍스트 완성 (레거시) |
| POST | `/v1/embeddings` | 임베딩 생성 (모델이 지원하는 경우) |

> 상세 API 명세: [vLLM 공식 문서 — OpenAI Compatible Server](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html)

---

## 변경이력

| 버전 | 날짜 | 작성자 | 내용 |
|------|------|--------|------|
| v1.0 | 2026-04-06 | 주용수 | 초안 작성 |
