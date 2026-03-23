# LiteLLM 심층 기술 분석

| 항목 | 내용 |
|------|------|
| **문서번호** | SAI-KB-2026-003 |
| **작성일** | 2026년 3월 23일 |
| **버전** | v1.0 |
| **보안등급** | 일반 |
| **작성** | Secern AI |
| **분석 대상 버전** | v1.82.6 (커밋 c89496f378 기준) |

---

> **TL;DR**
> - LiteLLM은 120+ LLM 프로바이더를 단일 OpenAI-호환 API로 통합하는 Python SDK + AI Gateway(Proxy) 이중 계층 프로젝트
> - SDK 계층(`litellm.completion()`)은 프로바이더별 요청/응답 변환을 처리하고, Proxy 계층은 FastAPI 기반 AI Gateway로 인증/라우팅/비용추적/캐싱 기능 제공
> - 6가지 라우팅 전략(simple-shuffle, least-busy, usage-based, latency-based, cost-based, provider-budget), DualCache(InMemory+Redis) 캐싱, 토큰 기반 비용 추적 시스템 내장
> - MCP 클라이언트, A2A 프로토콜 등 최신 에이전트 프로토콜 실험적 지원
> - IntraGenX에서는 멀티 모델 라우팅 Gateway, vLLM 백엔드 연결, 비용/사용량 관리 역할로 활용 가능
>
> **대상 독자**: 백엔드 개발자, 인프라 엔지니어, PM | **소요 시간**: 30~40분

---

## 1. 프로젝트 개요

### 1.1 목적 및 배경

LiteLLM은 **BerriAI**에서 개발한 LLM API 통합 라이브러리이자 AI Gateway이다. Y Combinator W23 배치 출신으로, "100+ LLM을 하나의 OpenAI-호환 인터페이스로" 라는 비전을 가지고 있다. 2023년 오픈소스로 시작하여 현재 v1.82.6까지 빠르게 발전했다.

핵심 가치는 두 가지이다:
1. **SDK**: `litellm.completion()` 한 줄로 OpenAI, Anthropic, Bedrock, Vertex AI, vLLM 등 어떤 LLM이든 호출 가능
2. **AI Gateway (Proxy)**: OpenAI API 호환 프록시 서버로 인증, 로드밸런싱, 비용 추적, 레이트 리미팅 등 엔터프라이즈 기능 제공

### 1.2 라이선스

- **커뮤니티**: MIT 라이선스 (핵심 SDK + Proxy 오픈소스)
- **Enterprise**: `litellm-enterprise` 패키지를 통한 상용 기능 (SSO, 감사 로그, 고급 보안 훅 등)

### 1.3 핵심 수치

| 항목 | 수치 |
|------|------|
| 버전 | v1.82.6 |
| Python 파일 수 | 1,707개 |
| 지원 프로바이더 수 | 117개 디렉토리 (`litellm/llms/` 하위) |
| 통합 콜백/로깅 | 70+ 종류 (`litellm/integrations/`) |
| 주요 파일 규모 | `proxy_server.py` 13,609줄, `router.py` 9,862줄, `utils.py` 9,496줄, `main.py` 7,788줄 |
| 핵심 의존성 | `openai`, `httpx`, `tiktoken`, `pydantic`, `fastapi`, `aiohttp` |
| Python 요구사항 | 3.9 이상 |

### 1.4 경쟁 제품 대비 차별점

| 비교 항목 | LiteLLM | OpenRouter | Portkey | Helicone |
|-----------|---------|------------|---------|----------|
| **형태** | 오픈소스 SDK + Proxy | SaaS API Gateway | SaaS AI Gateway | SaaS 관측 플랫폼 |
| **셀프호스팅** | 완전 지원 | 불가 | 제한적 | 제한적 |
| **SDK 직접 호출** | 지원 (Proxy 없이 사용 가능) | 불가 | 불가 | 불가 |
| **프로바이더 추가** | 코드 레벨 확장 가능 | 불가 | 제한적 | 해당 없음 |
| **비용 추적** | 내장 (DB 기반) | SaaS 대시보드 | SaaS 대시보드 | SaaS 대시보드 |
| **폐쇄망 배포** | 완전 지원 | 불가 | 불가 | 불가 |
| **라이선스** | MIT + Enterprise | 상용 | 상용 | 상용 |

LiteLLM의 최대 차별점은 **완전한 셀프호스팅이 가능한 오픈소스**라는 점이다. 폐쇄망/온프레미스 환경에서도 모든 기능을 사용할 수 있어 규제 산업에 적합하다.

---

## 2. 아키텍처 심층 분석

### 2.1 전체 아키텍처 다이어그램

```
┌─────────────────────────────────────────────────────────────────────┐
│                        클라이언트 계층                                │
│   OpenAI SDK  │  Anthropic SDK  │  curl/httpx  │  litellm SDK      │
└──────┬────────┴────────┬────────┴──────┬───────┴──────┬────────────┘
       │                 │               │              │
       ▼                 ▼               ▼              │
┌──────────────────────────────────────────────┐        │
│          AI Gateway (Proxy) 계층              │        │
│  ┌──────────────────────────────────────┐    │        │
│  │  FastAPI App (proxy_server.py)       │    │        │
│  │  ├─ /v1/chat/completions            │    │        │
│  │  ├─ /v1/embeddings                  │    │        │
│  │  ├─ /v1/images/generations          │    │        │
│  │  ├─ /v1/audio/transcriptions        │    │        │
│  │  ├─ /v1/responses                   │    │        │
│  │  └─ /key, /team, /model (관리 API)  │    │        │
│  └──────────┬───────────────────────────┘    │        │
│             │                                │        │
│  ┌──────────▼───────────────────────────┐    │        │
│  │  Auth Layer (proxy/auth/)            │    │        │
│  │  API Key → JWT → OAuth2             │    │        │
│  └──────────┬───────────────────────────┘    │        │
│             │                                │        │
│  ┌──────────▼───────────────────────────┐    │        │
│  │  Hooks/Middleware Chain              │    │        │
│  │  ├─ max_budget_limiter              │    │        │
│  │  ├─ parallel_request_limiter        │    │        │
│  │  ├─ cache_control_check             │    │        │
│  │  └─ custom hooks (Enterprise)       │    │        │
│  └──────────┬───────────────────────────┘    │        │
│             │                                │        │
│  ┌──────────▼───────────────────────────┐    │        │
│  │  Router (router.py)                  │    │        │
│  │  ├─ 로드밸런싱 전략                   │    │        │
│  │  ├─ Fallback / Retry                │    │        │
│  │  ├─ Cooldown 관리                    │    │        │
│  │  └─ 스케줄러 (우선순위 큐)            │    │        │
│  └──────────┬───────────────────────────┘    │        │
└─────────────┼────────────────────────────────┘        │
              │                                         │
              ▼                                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        SDK 계층                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  main.py — completion() / acompletion() / embedding()        │  │
│  │  └─ get_llm_provider() → 프로바이더 결정                      │  │
│  └──────────┬────────────────────────────────────────────────────┘  │
│             │                                                       │
│  ┌──────────▼────────────────────────────────────────────────────┐  │
│  │  BaseLLMHTTPHandler (llms/custom_httpx/llm_http_handler.py)  │  │
│  │  └─ ProviderConfig.transform_request()                       │  │
│  │  └─ HTTPHandler / AsyncHTTPHandler (httpx)                   │  │
│  │  └─ ProviderConfig.transform_response()                      │  │
│  └──────────┬────────────────────────────────────────────────────┘  │
│             │                                                       │
│  ┌──────────▼────────────────────────────────────────────────────┐  │
│  │  llms/{provider}/chat/transformation.py                      │  │
│  │  (117개 프로바이더별 변환 모듈)                                 │  │
│  └──────────┬────────────────────────────────────────────────────┘  │
└─────────────┼───────────────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     LLM Provider API                                │
│   OpenAI  │  Anthropic  │  Bedrock  │  Vertex AI  │  vLLM  │  ...  │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 SDK 계층 vs Proxy(AI Gateway) 계층 분리

LiteLLM의 핵심 설계 원칙은 **SDK와 Proxy의 명확한 분리**이다:

**SDK 계층** (`litellm/`):
- 프로바이더별 요청/응답 변환 (Translation Layer)
- 스트리밍 처리, 토큰 카운팅
- 비용 계산, 콜백/로깅
- Proxy 없이 독립적으로 사용 가능: `litellm.completion(model="gpt-4", messages=[...])`

**Proxy 계층** (`litellm/proxy/`):
- FastAPI 기반 OpenAI-호환 API 서버
- 인증/인가 (API Key, JWT, OAuth2)
- 라우팅, 레이트 리미팅, 예산 관리
- PostgreSQL + Redis 기반 상태 관리
- SDK를 내부적으로 호출하여 실제 LLM API와 통신

```
Proxy는 SDK 위에 구축된 엔터프라이즈 래퍼이다:
AI Gateway → Router → litellm.acompletion() → BaseLLMHTTPHandler → Provider API
```

### 2.3 요청 흐름 추적

클라이언트 요청이 처리되는 전체 과정:

1. **클라이언트** → `POST /v1/chat/completions` 요청
2. **proxy_server.py** → `chat_completion()` 엔드포인트 수신
3. **Auth** → `user_api_key_auth()` — API 키 검증, 권한 확인 (DualCache → Redis → PostgreSQL)
4. **Hooks** → `max_budget_limiter`, `parallel_request_limiter` 등 사전 검증
5. **Router** → `route_request()` — 라우팅 전략에 따라 배포 선택
6. **main.py** → `litellm.acompletion()` — SDK 진입점
7. **get_llm_provider()** → 모델명에서 프로바이더 결정 (예: `bedrock/claude-3` → Bedrock)
8. **BaseLLMHTTPHandler** → `completion()` 호출
9. **ProviderConfig** → `transform_request()` — OpenAI 형식 → 프로바이더 형식 변환
10. **HTTPHandler** → httpx를 통한 실제 HTTP 요청
11. **ProviderConfig** → `transform_response()` — 프로바이더 형식 → OpenAI 형식 변환
12. **cost_calculator.py** → 비용 계산 후 `response._hidden_params["response_cost"]`에 저장
13. **Callbacks** → 비동기로 로깅/비용 기록 (Langfuse, Datadog, DB 등)
14. **응답** → `ModelResponse` + `x-litellm-response-cost` 헤더 반환

### 2.4 미들웨어/훅 체인

Proxy Hooks는 `proxy/hooks/__init__.py`에서 `PROXY_HOOKS` 딕셔너리로 관리된다:

| 훅 | 파일 | 역할 |
|----|------|------|
| `max_budget_limiter` | `proxy/hooks/max_budget_limiter.py` | 키/팀/사용자별 예산 한도 검증 |
| `parallel_request_limiter` | `proxy/hooks/parallel_request_limiter_v3.py` | 동시 요청 수 제한 (TPM/RPM) |
| `cache_control_check` | `proxy/hooks/cache_control_check.py` | 캐시 유효성 검증 |
| `responses_id_security` | `proxy/hooks/responses_id_security.py` | 응답 ID 보안 검증 |
| `litellm_skills` | `proxy/hooks/litellm_skills/` | 스킬 주입 |
| `max_iterations_limiter` | `proxy/hooks/max_iterations_limiter.py` | 최대 반복 횟수 제한 |
| `max_budget_per_session_limiter` | `proxy/hooks/max_budget_per_session_limiter.py` | 세션별 예산 제한 |

Enterprise 라이선스가 있으면 추가 보안 훅(프롬프트 인젝션 탐지, PII 마스킹 등)이 자동 등록된다.

모든 훅은 `CustomLogger` 클래스를 상속하며, `async_pre_call_hook()`, `async_post_call_success_hook()` 등의 메서드를 오버라이드하여 요청 파이프라인에 개입한다.

### 2.5 비동기 처리 모델

- **웹 프레임워크**: FastAPI (Uvicorn/Gunicorn 위에서 실행)
- **HTTP 클라이언트**: `httpx` (AsyncHTTPHandler / HTTPHandler)
- **비동기 콜백**: 콜백은 메인 요청 스레드를 블로킹하지 않고 비동기로 실행
- **백그라운드 작업**: APScheduler로 주기적 작업 관리 (예산 리셋, 비용 로그 플러시, 헬스체크)
- **이벤트 루프**: `uvloop` 옵션 지원 (Linux/macOS)

---

## 3. 코드베이스 상세 구조

### 3.1 전체 디렉토리 트리 (주요 모듈 2단계)

```
litellm/
├── __init__.py              # 글로벌 설정, 콜백 리스트, 상수
├── main.py                  # SDK 진입점: completion(), acompletion(), embedding()
├── router.py                # Router 클래스: 로드밸런싱, Fallback, Retry
├── utils.py                 # 유틸리티: token_counter(), ProviderConfigManager 등 (get_llm_provider()는 litellm_core_utils/에서 정의)
├── cost_calculator.py       # 비용 계산: completion_cost()
├── scheduler.py             # 우선순위 큐 기반 요청 스케줄러
├── constants.py             # 전역 상수
├── exceptions.py            # 커스텀 예외 클래스
│
├── llms/                    # 프로바이더별 변환 모듈 (117개)
│   ├── base_llm/            # 추상 베이스 클래스 (BaseConfig 등)
│   │   ├── chat/transformation.py          # BaseConfig (chat completion)
│   │   ├── embedding/transformation.py     # BaseEmbeddingConfig
│   │   ├── responses/transformation.py     # BaseResponsesAPIConfig
│   │   ├── realtime/transformation.py      # BaseRealtimeConfig
│   │   └── ...                             # 30+ 기능별 서브디렉토리 (chat, embedding, audio, image, responses 등)
│   ├── custom_httpx/        # HTTP 핸들러
│   │   ├── llm_http_handler.py  # BaseLLMHTTPHandler (핵심 오케스트레이터)
│   │   ├── http_handler.py      # HTTPHandler / AsyncHTTPHandler
│   │   └── aiohttp_handler.py   # aiohttp 기반 대안 핸들러
│   ├── openai/              # OpenAI 프로바이더
│   ├── anthropic/           # Anthropic 프로바이더
│   ├── bedrock/             # AWS Bedrock 프로바이더
│   ├── vertex_ai/           # Google Vertex AI 프로바이더
│   ├── gemini/              # Google Gemini 프로바이더
│   ├── azure/               # Azure OpenAI 프로바이더
│   ├── vllm/                # vLLM 프로바이더
│   ├── ollama/              # Ollama 프로바이더
│   └── ...                  # 110+ 추가 프로바이더
│
├── proxy/                   # AI Gateway (Proxy) 서버
│   ├── proxy_server.py      # FastAPI 앱, 모든 API 엔드포인트 (13,609줄)
│   ├── route_llm_request.py # 요청 라우팅 로직
│   ├── auth/                # 인증 모듈
│   │   ├── user_api_key_auth.py  # API 키 인증 메인
│   │   ├── handle_jwt.py         # JWT 처리
│   │   ├── oauth2_check.py       # OAuth2 검증
│   │   └── auth_checks.py        # 권한 검증
│   ├── hooks/               # Proxy 훅/미들웨어
│   ├── db/                  # 데이터베이스 클라이언트
│   │   ├── prisma_client.py      # Prisma ORM 클라이언트
│   │   └── db_spend_update_writer.py  # 비용 배치 기록
│   ├── management_endpoints/     # 관리 API (/key, /team, /model)
│   ├── management_helpers/       # 관리 헬퍼 (예산 리셋, 키 로테이션)
│   ├── pass_through_endpoints/   # 직접 프로바이더 패스스루
│   ├── anthropic_endpoints/      # /v1/messages 엔드포인트
│   ├── vertex_ai_endpoints/      # Vertex AI 패스스루
│   ├── google_endpoints/         # Google AI Studio 패스스루
│   ├── response_api_endpoints/   # OpenAI Responses API
│   ├── guardrails/               # 가드레일 시스템
│   └── schema.prisma             # DB 스키마 정의
│
├── router_strategy/         # 라우팅 전략 모듈
│   ├── simple_shuffle.py         # 기본 랜덤 셔플
│   ├── least_busy.py             # 최소 부하 라우팅
│   ├── lowest_latency.py         # 최저 지연시간 라우팅
│   ├── lowest_cost.py            # 최저 비용 라우팅
│   ├── lowest_tpm_rpm.py         # TPM/RPM 기반 라우팅
│   ├── lowest_tpm_rpm_v2.py      # TPM/RPM v2 (개선판)
│   ├── budget_limiter.py         # 프로바이더별 예산 제한
│   ├── tag_based_routing.py      # 태그 기반 라우팅
│   ├── auto_router/              # 자동 라우팅 (실험적)
│   └── complexity_router/        # 복잡도 기반 라우팅 (실험적)
│
├── router_utils/            # 라우터 유틸리티
│   ├── cooldown_handlers.py      # 배포 쿨다운 관리
│   ├── cooldown_cache.py         # 쿨다운 캐시
│   ├── fallback_event_handlers.py # Fallback 처리
│   ├── pre_call_checks/          # 사전 호출 검증
│   │   ├── deployment_affinity_check.py   # 배포 친화도
│   │   ├── model_rate_limit_check.py      # 모델 레이트 제한
│   │   └── prompt_caching_deployment_check.py  # 프롬프트 캐싱 배포
│   └── pattern_match_deployments.py  # 패턴 매칭 라우터
│
├── caching/                 # 캐싱 시스템
│   ├── caching.py                # Cache 클래스 (통합 인터페이스)
│   ├── dual_cache.py             # DualCache (InMemory + Redis)
│   ├── in_memory_cache.py        # 인메모리 캐시
│   ├── redis_cache.py            # Redis 캐시
│   ├── redis_cluster_cache.py    # Redis Cluster
│   ├── caching_handler.py        # LLM 응답 캐싱 핸들러
│   ├── disk_cache.py             # 디스크 캐시
│   ├── s3_cache.py               # S3 캐시
│   ├── gcs_cache.py              # GCS 캐시
│   └── redis_semantic_cache.py   # Redis 시맨틱 캐시
│
├── litellm_core_utils/      # 핵심 유틸리티
│   ├── litellm_logging.py        # Logging 클래스 (요청 생명주기 추적)
│   ├── get_llm_provider_logic.py # 프로바이더 결정 로직
│   ├── streaming_handler.py      # 스트리밍 응답 처리
│   ├── exception_mapping_utils.py # 예외 매핑
│   ├── llm_cost_calc/            # 비용 계산 유틸리티
│   ├── llm_response_utils/       # 응답 처리 유틸리티
│   └── prompt_templates/         # 프롬프트 템플릿 팩토리
│
├── integrations/            # 외부 서비스 통합 (70+)
│   ├── custom_logger.py          # CustomLogger 베이스 클래스
│   ├── langfuse/                 # Langfuse 통합
│   ├── datadog/                  # Datadog 통합
│   ├── prometheus.py             # Prometheus 메트릭
│   ├── opentelemetry.py          # OpenTelemetry 통합
│   ├── SlackAlerting/            # Slack 알림
│   └── ...                       # 60+ 추가 통합
│
├── secret_managers/         # 시크릿 관리자
│   ├── aws_secret_manager.py
│   ├── google_secret_manager.py
│   ├── hashicorp_secret_manager.py
│   ├── google_kms.py
│   └── cyberark_secret_manager.py
│
├── experimental_mcp_client/ # MCP 클라이언트 (실험적)
│   ├── tools.py                  # MCP 도구 → OpenAI 도구 변환
│   └── client.py                 # MCP 세션 클라이언트
│
├── a2a_protocol/            # A2A 프로토콜 (실험적)
│   ├── main.py                   # A2A SDK 통합
│   ├── client.py                 # A2A 클라이언트
│   ├── streaming_iterator.py     # A2A 스트리밍
│   └── card_resolver.py          # 에이전트 카드 리졸버
│
├── types/                   # 타입 정의 (Pydantic 모델)
│   ├── utils.py                  # ModelResponse, Usage 등
│   ├── router.py                 # Router 관련 타입
│   └── llms/                     # 프로바이더별 타입
│
├── responses/               # OpenAI Responses API 지원
├── realtime_api/            # WebSocket 실시간 API
├── batches/                 # 배치 API
├── fine_tuning/             # 파인튜닝 API
└── passthrough/             # 패스스루 엔드포인트
```

### 3.2 핵심 모듈별 상세

#### `litellm/main.py` (7,788줄) — SDK 진입점

| 함수 | 역할 |
|------|------|
| `completion()` | 동기 chat completion (모든 프로바이더 통합) |
| `acompletion()` | 비동기 chat completion |
| `embedding()` / `aembedding()` | 임베딩 생성 |
| `image_generation()` / `aimage_generation()` | 이미지 생성 |
| `text_completion()` | 텍스트 completion (레거시) |
| `transcription()` / `atranscription()` | 오디오 트랜스크립션 |
| `speech()` / `aspeech()` | TTS |
| `moderation()` | 콘텐츠 모더레이션 |
| `rerank()` / `arerank()` | 리랭킹 |

`completion()` 함수는 `model` 파라미터에서 프로바이더를 결정하고, 해당 프로바이더의 핸들러를 호출하는 거대한 분기 함수이다. 각 프로바이더별 핸들러 인스턴스는 모듈 레벨에서 미리 생성되어 있다 (예: `openai_chat_completions = OpenAIChatCompletion()`, `bedrock_converse_chat_completion = BedrockConverseLLM()`).

#### `litellm/router.py` (9,862줄) — Router 클래스

Router는 여러 모델 배포(Deployment) 간 로드밸런싱, Fallback, Retry를 관리하는 핵심 클래스이다.

주요 구성요소:
- `model_list`: 배포 목록 (모델 이름 → 프로바이더 + 파라미터)
- `cache`: DualCache 인스턴스 (TPM/RPM 추적, 쿨다운 관리)
- `routing_strategy_init()`: 라우팅 전략 초기화
- `acompletion()`, `aembedding()` 등: Router를 통한 API 호출
- `_async_get_available_deployment()`: 가용 배포 선택 (핵심 라우팅 로직)
- Fallback 체인, Retry 정책, Cooldown 관리

#### `litellm/proxy/proxy_server.py` (13,609줄) — AI Gateway

FastAPI 앱 정의와 모든 API 엔드포인트가 포함된 파일이다. `app = FastAPI(...)` 로 생성된 앱에 각종 엔드포인트가 데코레이터로 등록된다.

핵심 엔드포인트: `chat_completion()` — OpenAI Chat Completion API 호환 엔드포인트. 인증 → 훅 → 라우터 → SDK → 응답의 전체 파이프라인을 오케스트레이션한다.

#### `litellm/cost_calculator.py` (2,294줄) — 비용 계산

`completion_cost()` 함수가 핵심이며, 프로바이더별 비용 계산 로직을 분기한다. 모델별 가격 정보는 `model_prices_and_context_window.json` (프로젝트 루트)에서 관리된다.

### 3.3 모듈 간 의존성 흐름

```
__init__.py (글로벌 설정)
    ↓
main.py (SDK 진입)  ←──── router.py (라우팅/밸런싱)
    ↓                         ↑
utils.py (get_llm_provider)   proxy/proxy_server.py (API 서버)
    ↓                         ↑
llms/custom_httpx/            proxy/auth/ (인증)
llm_http_handler.py           proxy/hooks/ (미들웨어)
    ↓
llms/{provider}/chat/         caching/ (캐싱)
transformation.py             integrations/ (콜백/로깅)
    ↓
cost_calculator.py (비용)
```

### 3.4 진입점

| 진입점 | 경로 | 설명 |
|--------|------|------|
| SDK 직접 호출 | `litellm.completion()` | Python 코드에서 직접 사용 |
| Proxy 서버 | `litellm --model gpt-4` | CLI로 프록시 서버 시작 |
| CLI (Proxy) | `litellm-proxy` → `litellm.proxy.client.cli:cli` | Proxy 전용 CLI |
| Docker | `Dockerfile` → `litellm --config config.yaml` | 컨테이너 배포 |

### 3.5 빌드/패키징

- **빌드 시스템**: Poetry (`pyproject.toml`)
- **패키지 이름**: `litellm`
- **엔트리 포인트**: `litellm = 'litellm:run_server'`, `litellm-proxy = 'litellm.proxy.client.cli:cli'`
- **Extras**:
  - `proxy`: FastAPI, Uvicorn, Redis, MCP 등 Proxy 실행에 필요한 의존성
  - `extra_proxy`: Prisma, Azure Key Vault, GCP KMS, A2A SDK 등 추가 인프라 통합
  - `caching`: 디스크 캐시
  - `grpc`: gRPC 지원

---

## 4. 핵심 기술 메커니즘

### 4.1 Provider 추상화 계층

LiteLLM의 가장 핵심적인 설계 패턴은 **BaseConfig를 통한 프로바이더 추상화**이다.

#### 베이스 클래스 구조

`litellm/llms/base_llm/chat/transformation.py`에 정의된 `BaseConfig`는 모든 프로바이더가 구현해야 하는 추상 인터페이스를 정의한다:

```python
class BaseConfig(ABC):
    @abstractmethod
    def get_supported_openai_params(self, model: str) -> list:
        """이 프로바이더가 지원하는 OpenAI 파라미터 목록"""
        pass

    @abstractmethod
    def map_openai_params(self, non_default_params: dict, ...) -> dict:
        """OpenAI 파라미터를 프로바이더 고유 파라미터로 매핑"""
        pass

    def transform_request(self, model, messages, optional_params, litellm_params, headers):
        """OpenAI 형식 → 프로바이더 API 형식 변환"""

    def transform_response(self, model, raw_response, model_response, logging_obj, ...):
        """프로바이더 응답 → OpenAI ModelResponse 형식 변환"""

    def should_fake_stream(self, model, stream, custom_llm_provider) -> bool:
        """스트리밍 미지원 프로바이더의 가짜 스트리밍 여부"""

    def validate_environment(self, headers, model, messages, optional_params, litellm_params, api_key, ...):
        """API 키/환경변수 검증 및 헤더 설정"""

    def get_error_class(self, error_message, status_code, headers) -> BaseLLMException:
        """프로바이더별 에러 매핑"""
```

`BaseConfig` 외에도 기능별 베이스 클래스가 다수 존재한다:
- `BaseEmbeddingConfig` — 임베딩
- `BaseImageGenerationConfig` — 이미지 생성
- `BaseAudioTranscriptionConfig` — 오디오 변환
- `BaseResponsesAPIConfig` — OpenAI Responses API
- `BaseRealtimeConfig` — 실시간 WebSocket
- `BaseRerankConfig` — 리랭킹
- `BaseAnthropicMessagesConfig` — Anthropic Messages API 패스스루
- `BaseContainerConfig` — 컨테이너 관리

#### 프로바이더 핸들러 등록 및 호출

프로바이더별 핸들러는 `main.py`에서 모듈 레벨 변수로 인스턴스화된다:

```python
# main.py (모듈 레벨)
openai_chat_completions = OpenAIChatCompletion()
anthropic_chat_completions = AnthropicChatCompletion()
bedrock_converse_chat_completion = BedrockConverseLLM()
vertex_chat_completion = VertexLLM()
base_llm_http_handler = BaseLLMHTTPHandler()
# ... 30+ 핸들러 인스턴스
```

`completion()` 함수 내부에서 `get_llm_provider(model)` 호출로 프로바이더가 결정되면, 해당 프로바이더의 핸들러를 직접 호출하거나 `BaseLLMHTTPHandler`를 경유하여 호출한다.

#### `BaseLLMHTTPHandler` — 중앙 HTTP 오케스트레이터

`litellm/llms/custom_httpx/llm_http_handler.py`에 정의된 이 클래스는 대부분의 프로바이더 호출을 중앙에서 처리한다:

1. `ProviderConfigManager`를 통해 프로바이더의 Config 클래스 조회
2. `Config.transform_request()` 호출 → 요청 변환
3. `HTTPHandler` 또는 `AsyncHTTPHandler` (httpx 기반)로 실제 HTTP 요청
4. `Config.transform_response()` 호출 → 응답 변환
5. `ModelResponse` 반환

`llm_http_handler.py`는 chat completion 외에도 embedding, image generation, audio, rerank, responses API, realtime, OCR, search, video, containers, skills 등 12+ 기능의 핸들링을 담당하며, 각 기능별 베이스 Config 클래스와 연동한다.

#### `litellm/llms/` 하위 구조 (117개 프로바이더)

각 프로바이더 디렉토리의 표준 구조:

```
llms/{provider}/
├── chat/
│   ├── transformation.py    # ProviderChatConfig(BaseConfig) — 핵심
│   └── handler.py           # 프로바이더 고유 핸들러 (옵션)
├── embed/                   # 임베딩 (해당 시)
├── common_utils.py          # 공통 유틸리티
├── cost_calculation.py      # 프로바이더별 비용 계산
└── types.py                 # 프로바이더별 타입
```

주요 프로바이더 목록 (일부):

| 프로바이더 | 디렉토리 | 비고 |
|-----------|---------|------|
| OpenAI | `llms/openai/` | GPT-4, GPT-5, o1 등 |
| Anthropic | `llms/anthropic/` | Claude 시리즈 |
| AWS Bedrock | `llms/bedrock/` | Converse + Invoke 이중 지원 |
| Google Vertex AI | `llms/vertex_ai/` | Gemini + Partner Models |
| Google Gemini | `llms/gemini/` | AI Studio 직접 호출 |
| Azure OpenAI | `llms/azure/` | Azure 전용 인증/라우팅 |
| vLLM | `llms/vllm/` | 로컬 vLLM 서버 연결 |
| Ollama | `llms/ollama/` | 로컬 Ollama 연결 |
| Hosted vLLM | `llms/hosted_vllm/` | 호스팅 vLLM 서비스 |
| DeepSeek | `llms/deepseek/` | DeepSeek 모델 |
| Mistral | `llms/mistral/` | Mistral AI |
| Groq | `llms/groq/` | Groq 하드웨어 가속 |
| Together AI | `llms/together_ai/` | 오픈소스 모델 호스팅 |
| Fireworks AI | `llms/fireworks_ai/` | 모델 서빙 플랫폼 |
| SageMaker | `llms/sagemaker/` | AWS SageMaker 엔드포인트 |
| WatsonX | `llms/watsonx/` | IBM WatsonX |

### 4.2 AI Gateway (Proxy)

#### FastAPI 앱 구조

`proxy/proxy_server.py`에서 `app = FastAPI(...)` 로 생성된 앱에 다음 엔드포인트들이 등록된다:

| 카테고리 | 엔드포인트 | 핸들러 함수/디렉토리 |
|---------|-----------|---------------------|
| Chat | `POST /v1/chat/completions` | `chat_completion()` |
| Completions | `POST /v1/completions` | `completion()` |
| Embeddings | `POST /v1/embeddings` | `embeddings()` |
| Images | `POST /v1/images/generations` | `proxy/image_endpoints/` |
| Audio | `POST /v1/audio/transcriptions` | `proxy_server.py` |
| Batches | `POST /v1/batches` | `proxy/batches_endpoints/` |
| Files | `POST /v1/files` | `proxy/openai_files_endpoints/` |
| Fine-tuning | `POST /v1/fine_tuning/jobs` | `proxy/fine_tuning_endpoints/` |
| Rerank | `POST /v1/rerank` | `proxy/rerank_endpoints/` |
| Responses | `POST /v1/responses` | `proxy/response_api_endpoints/` |
| Vector Stores | `POST /v1/vector_stores` | `proxy/vector_store_endpoints/` |
| Anthropic | `POST /v1/messages` | `proxy/anthropic_endpoints/` |
| Vertex AI | `/*` (패스스루) | `proxy/vertex_ai_endpoints/` |
| Gemini | `/*` (패스스루) | `proxy/google_endpoints/` |
| 관리 | `/key/*`, `/team/*`, `/model/*` | `proxy/management_endpoints/` |

#### 인증 흐름

인증은 `proxy/auth/user_api_key_auth.py`의 `user_api_key_auth()` 함수에서 처리된다:

```
요청 헤더 (Authorization: Bearer sk-xxx)
    ↓
1. API Key 추출
    ↓
2. DualCache (InMemory → Redis) 에서 키 조회
    ↓ (캐시 미스)
3. PostgreSQL에서 LiteLLM_VerificationToken 테이블 조회
    ↓
4. 키 유효성 검증 (만료, 예산, 모델 권한)
    ↓
5. JWT 토큰인 경우: handle_jwt.py로 분기
    ↓
6. OAuth2인 경우: oauth2_check.py로 분기
    ↓
7. UserAPIKeyAuth 객체 반환 (사용자 정보 + 권한)
```

지원하는 인증 방식:
- **API Key**: `Bearer sk-xxx` 형식 (기본)
- **JWT**: 외부 IdP 발급 JWT 토큰 검증
- **OAuth2**: OAuth2 Proxy 연동
- **Master Key**: 관리자 전용 마스터 키

#### 요청 라우팅 로직

`proxy/route_llm_request.py`에서 요청 종류에 따른 라우팅 매핑을 관리한다. `ROUTE_ENDPOINT_MAPPING` 딕셔너리가 Router 메서드와 API 엔드포인트를 매핑한다:

```python
ROUTE_ENDPOINT_MAPPING = {
    "acompletion": "/chat/completions",
    "aembedding": "/embeddings",
    "aimage_generation": "/image/generations",
    "aspeech": "/audio/speech",
    "arerank": "/rerank",
    "aresponses": "/responses",
    # ... 30+ 매핑
}
```

### 4.3 라우팅 알고리즘

#### Router 클래스 (`router.py`)

Router 클래스는 `model_list`에 정의된 여러 배포(Deployment) 중 어느 것으로 요청을 보낼지 결정한다:

```python
Router(
    model_list=[
        {"model_name": "gpt-4", "litellm_params": {"model": "openai/gpt-4", "api_key": "sk-..."}},
        {"model_name": "gpt-4", "litellm_params": {"model": "azure/gpt-4", "api_key": "az-..."}},
    ],
    routing_strategy="latency-based-routing",
    num_retries=3,
    fallbacks=[{"gpt-4": ["claude-3"]}],
)
```

#### 라우팅 전략 (`router_strategy/`)

`RoutingStrategy` enum으로 정의된 전략들:

| 전략 | 클래스 | 파일 | 동작 |
|------|--------|------|------|
| `simple-shuffle` | `simple_shuffle()` | `simple_shuffle.py` | 랜덤 셔플 (기본값) |
| `least-busy` | `LeastBusyLoggingHandler` | `least_busy.py` | 진행 중 요청이 가장 적은 배포 선택 |
| `usage-based-routing` | `LowestTPMLoggingHandler` | `lowest_tpm_rpm.py` | TPM/RPM이 가장 낮은 배포 선택 |
| `usage-based-routing-v2` | `LowestTPMLoggingHandler_v2` | `lowest_tpm_rpm_v2.py` | TPM/RPM v2 (Redis 최적화) |
| `latency-based-routing` | `LowestLatencyLoggingHandler` | `lowest_latency.py` | 응답 지연시간이 가장 낮은 배포 선택 |
| `cost-based-routing` | `LowestCostLoggingHandler` | `lowest_cost.py` | 비용이 가장 낮은 배포 선택 |
| `provider-budget-routing` | `RouterBudgetLimiting` | `budget_limiter.py` | 프로바이더별 예산 한도 기반 필터링 |

`routing_strategy_init()` 메서드에서 선택된 전략의 로깅 핸들러를 `litellm.callbacks`에 등록하여, 매 요청의 성공/실패 메트릭을 수집한다.

#### 최저 지연시간 라우팅 상세 (`lowest_latency.py`)

`LowestLatencyLoggingHandler`는 `CustomLogger`를 상속하며:

1. **메트릭 수집**: `log_success_event()`에서 응답 시간, TTFT(스트리밍 시), 토큰 수 기록
2. **캐시 키**: `{model_group}_map` 형식으로 DualCache에 배포별 지연시간 이력 저장
3. **배포 선택**: 시간 창(TTL 기본 1시간) 내의 평균 지연시간이 가장 낮은 배포 선택
4. **버퍼**: `lowest_latency_buffer`로 미세 차이 무시 가능

#### 추가 라우팅 기능

- **태그 기반 라우팅** (`tag_based_routing.py`): 요청 메타데이터의 태그로 배포 필터링
- **배포 친화도** (`deployment_affinity_check.py`): 같은 사용자의 요청을 같은 배포로 유지 (프롬프트 캐싱 활용)
- **모델 레이트 제한** (`model_rate_limit_check.py`): 모델별 TPM/RPM 사전 검증
- **프롬프트 캐싱 배포** (`prompt_caching_deployment_check.py`): 프롬프트 캐시가 존재하는 배포 우선 선택

#### Fallback / Retry / Cooldown

- **Retry**: `num_retries` 설정. 실패 시 같은 모델 그룹 내 다른 배포로 재시도
- **Fallback**: `fallbacks=[{"gpt-4": ["claude-3", "gemini-pro"]}]` — 모델 그룹 레벨 폴백
- **Cooldown**: 배포 실패 시 `cooldown_time`(기본 1초) 동안 해당 배포 제외. `allowed_fails` 정책으로 쿨다운 진입 임계값 설정 가능
- **Scheduler** (`scheduler.py`): 우선순위 큐 기반 요청 스케줄링. `FlowItem` 으로 요청을 큐에 넣고, `heapq`로 우선순위(0~255) 관리

### 4.4 캐싱 시스템

#### DualCache (`caching/dual_cache.py`)

DualCache는 InMemoryCache와 RedisCache를 동시에 관리하는 이중 캐시 계층이다:

```python
class DualCache(BaseCache):
    def __init__(self,
        in_memory_cache: Optional[InMemoryCache] = None,
        redis_cache: Optional[RedisCache] = None,
        default_in_memory_ttl: Optional[float] = None,
        default_redis_ttl: Optional[float] = None,
    ):
```

**동작 원리**:
- **쓰기**: InMemory + Redis 동시 기록
- **읽기**: InMemory 먼저 확인 → 캐시 미스 시 Redis 조회
- **TTL**: InMemory와 Redis에 각각 별도 TTL 설정 가능
- **배치**: `redis_batch_cache_expiry`로 Redis 배치 접근 시간 관리

DualCache는 Router, 인증, 레이트 리미팅 등 여러 곳에서 활용된다:

| 사용처 | DualCache 키 패턴 | 용도 |
|--------|-------------------|------|
| Router TPM/RPM | `global_router:{id}:{model}:tpm:{minute}` | 분당 토큰/요청 수 추적 |
| 배포 쿨다운 | `{deployment_id}:cooldown` | 쿨다운 상태 관리 |
| API 키 캐시 | `{api_key_hash}` | 키 정보 캐싱 |
| 레이트 제한 | `{key}:rate_limit:{minute}` | 동시 요청 수 추적 |
| LLM 응답 캐시 | `{cache_key}` | 동일 요청에 대한 응답 캐싱 |

#### 캐시 키 생성 로직

LLM 응답 캐싱 시, 캐시 키는 요청의 모델명 + 메시지 + 주요 파라미터(temperature, max_tokens 등)를 해싱하여 생성한다. `caching/caching_handler.py`의 `LLMCachingHandler`가 이를 담당한다.

#### 캐시 백엔드 옵션

`caching/caching.py`의 `Cache` 클래스가 다양한 백엔드를 지원한다:

| 백엔드 | 파일 | 용도 |
|--------|------|------|
| InMemory | `in_memory_cache.py` | 단일 인스턴스, 빠른 접근 |
| Redis | `redis_cache.py` | 멀티 인스턴스 공유, 영속성 |
| Redis Cluster | `redis_cluster_cache.py` | 대규모 분산 환경 |
| Disk | `disk_cache.py` | 로컬 디스크 (diskcache) |
| S3 | `s3_cache.py` | AWS S3 |
| GCS | `gcs_cache.py` | Google Cloud Storage |
| Redis Semantic | `redis_semantic_cache.py` | 의미적 유사성 기반 캐싱 |
| Qdrant Semantic | `qdrant_semantic_cache.py` | Qdrant 벡터 DB 기반 |

### 4.5 비용 추적

#### 비용 계산 흐름

```
LLM 응답 수신
    ↓
utils.py → update_response_metadata()
    ↓
litellm_logging.py → _response_cost_calculator()
    ↓
cost_calculator.py → completion_cost()
    ↓
프로바이더별 cost_per_token() 분기:
  ├─ openai_cost_per_token()
  ├─ anthropic_cost_per_token()
  ├─ bedrock_cost_per_token()
  ├─ google_cost_per_token()
  ├─ deepseek_cost_per_token()
  └─ generic_cost_per_token() (기본)
    ↓
response._hidden_params["response_cost"] = 계산된 비용
    ↓
x-litellm-response-cost 헤더로 클라이언트 반환
    ↓
DBSpendUpdateWriter → Redis 큐 → PostgreSQL 배치 기록 (60초 간격)
```

#### `completion_cost()` 함수 (`cost_calculator.py`)

```python
def completion_cost(
    completion_response=None,
    model: Optional[str] = None,
    prompt="", messages: List = [],
    completion="",
    total_time: Optional[float] = 0.0,
    call_type: Optional[CallTypesLiteral] = None,
    custom_llm_provider=None,
    custom_cost_per_token: Optional[CostPerToken] = None,
    custom_cost_per_second: Optional[float] = None,
    ...
) -> float:
```

이 함수는:
1. 프로바이더별 `cost_per_token()` 함수를 호출하여 입력/출력 토큰 비용 계산
2. 커스텀 가격 설정이 있으면 그것을 우선 사용
3. 시간 기반 과금(예: Replicate GPU)도 지원
4. 이미지 생성, 오디오 등 비텍스트 모달리티 비용도 처리

#### 모델 가격 데이터

`model_prices_and_context_window.json` (프로젝트 루트)에 모든 모델의 가격 정보가 JSON으로 관리된다. 이 파일은 LiteLLM 팀이 주기적으로 업데이트한다.

#### Spend Log 저장 구조

Proxy에서는 `DBSpendUpdateWriter` (`proxy/db/db_spend_update_writer.py`)가 비용 로그를 PostgreSQL에 배치 기록한다:

1. 각 요청의 비용이 Redis 큐에 적재
2. APScheduler의 `update_spend` 작업이 60초마다 실행
3. 큐의 비용 데이터를 PostgreSQL `LiteLLM_SpendLogs` 테이블에 배치 insert
4. 키/팀/사용자별 누적 비용을 `LiteLLM_VerificationToken`, `LiteLLM_TeamTable`, `LiteLLM_UserTable`에 업데이트

### 4.6 Rate Limiting

Proxy의 레이트 리미팅은 `proxy/hooks/parallel_request_limiter_v3.py`에서 구현된다:

- **TPM (Tokens Per Minute)**: 분당 토큰 사용량 제한
- **RPM (Requests Per Minute)**: 분당 요청 수 제한
- **동시 요청 수**: 키/팀 단위 동시 요청 제한

동작 방식:
1. 요청 진입 시 현재 분의 TPM/RPM 카운터 확인 (DualCache)
2. 한도 초과 시 429 Too Many Requests 반환
3. 요청 완료 시 사용한 토큰 수만큼 TPM 카운터 증분
4. 카운터는 분 단위로 자동 만료 (Redis TTL)

Router 레벨에서는 `LowestTPMLoggingHandler`가 각 배포의 TPM/RPM을 추적하여 사용량이 낮은 배포를 선택한다.

### 4.7 MCP/A2A 통합

#### MCP 클라이언트 (`experimental_mcp_client/`)

MCP(Model Context Protocol) 클라이언트는 실험적 기능으로, MCP 서버의 도구를 OpenAI 호환 도구로 변환하여 LLM에 제공한다:

**`tools.py`** 핵심 함수:
- `transform_mcp_tool_to_openai_tool(mcp_tool)` — MCP Tool → OpenAI `ChatCompletionToolParam` 변환
- `load_mcp_tools(session, format)` — MCP 세션에서 도구 목록 로드
- `call_openai_tool(session, tool_call)` — OpenAI 도구 호출을 MCP `CallToolRequest`로 변환하여 실행

Proxy 설정에서 MCP 서버를 등록할 수 있다 (`proxy_config.yaml`):
```yaml
mcp_servers:
  wikipedia:
    transport: "stdio"
    command: "uvx"
    args: ["mcp-server-fetch"]
  deepwiki:
    transport: "http"
    url: "https://mcp.deepwiki.com/mcp"
```

#### A2A 프로토콜 (`a2a_protocol/`)

A2A(Agent-to-Agent) 프로토콜은 Google이 주도하는 에이전트 간 통신 프로토콜이다. LiteLLM은 `a2a-sdk`를 선택적 의존성으로 포함하여 A2A 에이전트를 "모델"처럼 호출할 수 있게 한다:

- **`main.py`**: `send_message()`, `asend_message()` — A2A 에이전트에 메시지 전송
- **`card_resolver.py`**: `LiteLLMA2ACardResolver` — 에이전트 카드(능력 명세) 조회
- **`streaming_iterator.py`**: A2A 스트리밍 응답 처리
- **모델 접두사**: `a2a/` — 예: `model="a2a/http://localhost:3000"` 형식으로 A2A 에이전트 호출
- **비용 추적**: `cost_calculator.py`에 A2A 전용 비용 계산 로직 포함

---

## 5. 설정 및 의존성 분석

### 5.1 핵심 의존성 (`pyproject.toml`)

| 의존성 | 버전 | 역할 |
|--------|------|------|
| `openai` | >=2.8.0 | OpenAI SDK (타입 정의, 클라이언트 기반) |
| `httpx` | >=0.23.0 | HTTP 클라이언트 (대부분의 프로바이더 호출) |
| `tiktoken` | >=0.7.0 | OpenAI 토크나이저 (토큰 카운팅) |
| `pydantic` | ^2.5.0 | 데이터 검증, 타입 정의 |
| `aiohttp` | >=3.10 | 비동기 HTTP (일부 프로바이더) |
| `jinja2` | ^3.1.2 | 프롬프트 템플릿 |
| `tokenizers` | * | HuggingFace 토크나이저 |
| `click` | * | CLI 프레임워크 |
| `jsonschema` | >=4.23.0 | JSON 스키마 검증 |
| `python-dotenv` | >=0.2.0 | 환경변수 로딩 |

#### Proxy 전용 의존성 (`[proxy]` extra)

| 의존성 | 역할 |
|--------|------|
| `fastapi` >=0.120.1 | 웹 프레임워크 |
| `uvicorn` >=0.32.1 | ASGI 서버 |
| `gunicorn` ^23.0.0 | WSGI 서버 (프로덕션) |
| `pyyaml` ^6.0.1 | YAML 설정 파싱 |
| `orjson` ^3.9.7 | 빠른 JSON 직렬화 |
| `PyJWT` ^2.12.0 | JWT 토큰 처리 |
| `cryptography` * | 암호화 |
| `apscheduler` ^3.10.4 | 백그라운드 작업 스케줄링 |
| `websockets` ^15.0.1 | WebSocket 지원 (Realtime API) |
| `mcp` >=1.25.0 | MCP 프로토콜 |
| `litellm-enterprise` 0.1.35 | Enterprise 기능 |

#### Extra Proxy 의존성 (`[extra_proxy]` extra)

| 의존성 | 역할 |
|--------|------|
| `prisma` ^0.11.0 | PostgreSQL ORM |
| `azure-identity` | Azure 인증 |
| `azure-keyvault-secrets` | Azure Key Vault |
| `google-cloud-kms` | Google Cloud KMS |
| `redisvl` ^0.4.1 | Redis 벡터 라이브러리 |
| `a2a-sdk` ^0.3.22 | A2A 프로토콜 SDK |

### 5.2 Proxy 설정 (`config.yaml` 구조)

```yaml
# 모델 배포 정의
model_list:
  - model_name: gpt-4                    # 외부 노출 모델명
    litellm_params:
      model: openai/gpt-4               # 프로바이더/모델 형식
      api_key: os.environ/OPENAI_API_KEY # 환경변수 참조 지원
      api_base: https://api.openai.com/v1

  - model_name: gpt-4                    # 같은 이름 → 로드밸런싱 대상
    litellm_params:
      model: azure/gpt-4-deployment
      api_key: os.environ/AZURE_API_KEY
      api_base: https://xxx.openai.azure.com

# 라우터 설정
router_settings:
  routing_strategy: "latency-based-routing"
  num_retries: 3
  fallbacks:
    - gpt-4: ["claude-3"]
  cooldown_time: 60

# 일반 설정
general_settings:
  master_key: sk-1234
  database_url: os.environ/DATABASE_URL  # PostgreSQL
  store_model_in_db: true

# Litellm 설정
litellm_settings:
  success_callback: ["langfuse"]
  cache: true
  cache_params:
    type: "redis"
    host: os.environ/REDIS_HOST

# MCP 서버 설정
mcp_servers:
  wikipedia:
    transport: "stdio"
    command: "uvx"
    args: ["mcp-server-fetch"]
```

### 5.3 환경변수 기반 설정

주요 환경변수:

| 변수 | 용도 |
|------|------|
| `LITELLM_MASTER_KEY` | 관리자 API 키 |
| `DATABASE_URL` | PostgreSQL 연결 문자열 |
| `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD` | Redis 연결 |
| `LITELLM_MODE` | DEV / PRODUCTION |
| `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, ... | 프로바이더별 API 키 |
| `LITELLM_LOG` | 로그 레벨 (DEBUG, INFO) |
| `LITELLM_UI_SESSION_DURATION` | UI 세션 지속시간 |

설정 파일에서 `os.environ/VARIABLE_NAME` 형식으로 환경변수를 참조할 수 있다 (`secret_managers/main.py`에서 처리).

### 5.4 Docker/Kubernetes 배포

**Dockerfile** (프로젝트 루트):
- 빌더 스테이지: Wolfi 기반, pip로 빌드
- 런타임 스테이지: 최소 이미지, gunicorn/uvicorn으로 실행
- Admin UI 빌드 포함 (`docker/build_admin_ui.sh`)

**Docker 변형**:
| 파일 | 용도 |
|------|------|
| `Dockerfile` | 표준 이미지 |
| `docker/Dockerfile.non_root` | 비루트 실행 (보안 강화) |
| `docker/Dockerfile.database` | PostgreSQL 통합 |
| `docker/Dockerfile.alpine` | Alpine 기반 경량 |

**docker-compose.yml**:
```yaml
# LiteLLM Proxy + PostgreSQL + Redis 올인원 구성
services:
  litellm:
    image: ghcr.io/berriai/litellm:latest
    ports: ["4000:4000"]
    volumes: ["./config.yaml:/app/config.yaml"]
  postgres:
    image: postgres:16
  redis:
    image: redis:7
```

`docker-compose.hardened.yml`은 보안 강화 구성을 제공한다.

### 5.5 인프라 요구사항

| 컴포넌트 | 필수 여부 | 용도 |
|----------|-----------|------|
| **PostgreSQL** | Proxy 사용 시 권장 | API 키, 팀, 사용자, 비용 로그 영속화 |
| **Redis** | Proxy 사용 시 권장 | 캐싱, 레이트 리미팅, TPM/RPM 추적, 쿨다운 |
| **Python 3.9+** | 필수 | 런타임 |

SDK 단독 사용 시에는 외부 인프라 없이 순수 Python 환경만으로 동작한다.

---

## 6. API 및 인터페이스

### 6.1 Proxy API 엔드포인트 상세

#### LLM 호출 API

| 메서드 | 엔드포인트 | 설명 |
|--------|-----------|------|
| POST | `/v1/chat/completions` | Chat Completion (OpenAI 호환) |
| POST | `/v1/completions` | Text Completion |
| POST | `/v1/embeddings` | 임베딩 생성 |
| POST | `/v1/images/generations` | 이미지 생성 |
| POST | `/v1/images/edits` | 이미지 편집 |
| POST | `/v1/audio/transcriptions` | 오디오 → 텍스트 |
| POST | `/v1/audio/speech` | 텍스트 → 오디오 (TTS) |
| POST | `/v1/moderations` | 콘텐츠 모더레이션 |
| POST | `/v1/rerank` | 리랭킹 |
| POST | `/v1/responses` | OpenAI Responses API |
| POST | `/v1/batches` | 배치 처리 |
| POST | `/v1/files` | 파일 업로드 |
| POST | `/v1/fine_tuning/jobs` | 파인튜닝 |
| POST | `/v1/vector_stores` | 벡터 스토어 |
| GET | `/v1/models` | 사용 가능 모델 목록 |
| GET | `/_health` | 헬스 체크 |

#### Anthropic 패스스루

| 메서드 | 엔드포인트 | 설명 |
|--------|-----------|------|
| POST | `/v1/messages` | Anthropic Messages API 직접 호환 |

#### 관리 API

| 메서드 | 엔드포인트 | 설명 |
|--------|-----------|------|
| POST | `/key/generate` | API 키 생성 |
| POST | `/key/update` | API 키 업데이트 |
| POST | `/key/delete` | API 키 삭제 |
| GET | `/key/info` | API 키 정보 조회 |
| POST | `/team/new` | 팀 생성 |
| POST | `/team/update` | 팀 업데이트 |
| GET | `/team/info` | 팀 정보 조회 |
| GET | `/model/info` | 모델 정보 조회 |
| POST | `/model/new` | 모델 배포 추가 |
| GET | `/spend/logs` | 비용 로그 조회 |
| GET | `/global/spend` | 전체 비용 현황 |

### 6.2 SDK API

#### 핵심 함수

```python
import litellm

# Chat Completion (동기)
response = litellm.completion(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}],
    temperature=0.7,
    max_tokens=100,
)

# Chat Completion (비동기)
response = await litellm.acompletion(
    model="anthropic/claude-3-opus",
    messages=[{"role": "user", "content": "Hello"}],
)

# 임베딩
response = litellm.embedding(
    model="text-embedding-3-small",
    input=["Hello world"],
)

# 이미지 생성
response = litellm.image_generation(
    model="dall-e-3",
    prompt="A cat on the moon",
)

# 스트리밍
response = litellm.completion(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}],
    stream=True,
)
for chunk in response:
    print(chunk.choices[0].delta.content)

# Router 사용
router = litellm.Router(
    model_list=[...],
    routing_strategy="latency-based-routing",
)
response = await router.acompletion(model="gpt-4", messages=[...])
```

#### 프로바이더 지정 방식

모델명에 프로바이더 접두사를 붙여 지정한다:

```python
# OpenAI (기본, 접두사 생략 가능)
litellm.completion(model="gpt-4", ...)

# Anthropic
litellm.completion(model="anthropic/claude-3-opus", ...)

# AWS Bedrock
litellm.completion(model="bedrock/anthropic.claude-3-opus", ...)

# Vertex AI
litellm.completion(model="vertex_ai/gemini-pro", ...)

# vLLM (로컬)
litellm.completion(model="hosted_vllm/my-model", api_base="http://localhost:8000", ...)

# Ollama
litellm.completion(model="ollama/llama3", ...)

# A2A 에이전트
litellm.completion(model="a2a/http://localhost:3000", ...)
```

### 6.3 콜백 시스템

```python
import litellm

# 콜백 설정
litellm.success_callback = ["langfuse", "prometheus"]
litellm.failure_callback = ["slack"]

# 커스텀 콜백
class MyCallback(litellm.integrations.custom_logger.CustomLogger):
    async def async_log_success_event(self, kwargs, response_obj, start_time, end_time):
        print(f"Success: {kwargs['model']}, cost: {response_obj._hidden_params.get('response_cost')}")

    async def async_log_failure_event(self, kwargs, response_obj, start_time, end_time):
        print(f"Failure: {kwargs['model']}")

litellm.callbacks = [MyCallback()]
```

지원하는 콜백 종류 (70+):

| 카테고리 | 콜백 |
|---------|------|
| 관측성 | Langfuse, Datadog, OpenTelemetry, Prometheus, Arize, Helicone, Lunary |
| 알림 | Slack, PagerDuty, Email (Resend/SendGrid/SMTP) |
| 저장소 | S3, GCS Bucket, Azure Storage, DynamoDB |
| 보안 | Azure Sentinel, 감사 로그 |
| 실험 | MLflow, Weights & Biases, Braintrust |
| 기타 | Agentops, Humanloop, PostHog, CloudZero |

### 6.4 웹훅 통합

`generic_api` 콜백을 통해 임의의 HTTP 엔드포인트에 이벤트를 전송할 수 있다:

```yaml
litellm_settings:
  success_callback: ["generic_api"]
  generic_api:
    url: "https://your-webhook.com/events"
    headers:
      Authorization: "Bearer xxx"
```

---

## 7. Coco/IntraGenX 통합 분석

### 7.1 IntraGenX 아키텍처에서의 역할

IntraGenX 아키텍처에서 LiteLLM은 **멀티 모델 라우팅 Gateway** 역할을 담당한다. `02_implementation/06_vllm_rd_plan_ko.md`에서 정의된 "LiteLLM 멀티 모델 라우팅" 구성과 직접 연결된다:

```
클라이언트 (Coco Studio / Coco CLI)
    ↓
Coco Engine (코드 생성 엔진)
    ↓
LiteLLM Proxy (AI Gateway)
    ├─ vLLM 인스턴스 1 (Qwen2.5-32B)
    ├─ vLLM 인스턴스 2 (CodeQwen2.5-7B)
    ├─ vLLM 인스턴스 3 (파인튜닝 4B 모델)
    └─ 외부 API (필요 시 — OpenAI, Anthropic)
```

LiteLLM은 여기서:
- 여러 vLLM 인스턴스를 하나의 모델 그룹으로 묶어 로드밸런싱
- 모델별 Fallback 체인 구성 (32B 실패 → 7B → 4B)
- 토큰 사용량 및 비용 추적
- API 키 기반 접근 제어

### 7.2 통합 포인트

#### vLLM 백엔드 연결

LiteLLM은 `llms/vllm/` 및 `llms/hosted_vllm/` 모듈을 통해 vLLM과 연결된다. vLLM은 OpenAI-호환 API를 제공하므로, LiteLLM 설정에서 `openai/` 또는 `hosted_vllm/` 접두사로 vLLM 서버를 등록한다:

```yaml
model_list:
  - model_name: code-gen-32b
    litellm_params:
      model: hosted_vllm/Qwen2.5-Coder-32B-Instruct
      api_base: http://vllm-server-1:8000/v1
      api_key: "dummy"  # vLLM은 인증 없이도 동작

  - model_name: code-gen-7b
    litellm_params:
      model: hosted_vllm/CodeQwen2.5-7B
      api_base: http://vllm-server-2:8000/v1

router_settings:
  routing_strategy: "latency-based-routing"
  fallbacks:
    - code-gen-32b: ["code-gen-7b"]
```

#### 모델 Fallback

Router의 Fallback 기능을 활용하여 모델 간 자동 전환을 구성할 수 있다:
- 32B 모델 부하 초과 → 7B 모델로 자동 전환
- 특정 vLLM 인스턴스 다운 → 다른 인스턴스로 자동 전환
- 쿨다운 기능으로 장애 인스턴스 자동 제외

#### 비용 관리

- `model_prices_and_context_window.json`에 커스텀 모델 가격 등록 가능
- `custom_cost_per_token` 파라미터로 온프레미스 모델의 내부 비용 단가 설정
- Spend Log를 PostgreSQL에 기록하여 팀/프로젝트별 사용량 리포트 생성
- 프로바이더별 예산 제한 (`provider_budget_config`)으로 비용 통제

### 7.3 커스터마이징 영역

#### 프로바이더 추가

Coco Engine을 LiteLLM의 커스텀 프로바이더로 등록할 수 있다:

1. `llms/coco/chat/transformation.py` 생성
2. `CocoChatConfig(BaseConfig)` 클래스 구현
3. `transform_request()` — Coco Engine 요청 형식으로 변환
4. `transform_response()` — Coco Engine 응답을 OpenAI 형식으로 변환
5. `ProviderConfigManager`에 등록

또는 더 간단하게, `custom_llm` 모듈을 활용하여 `CustomLLM` 클래스를 상속하는 방법도 있다.

#### 인증 통합

Coco의 기존 인증 시스템과 LiteLLM Proxy의 인증을 통합할 수 있다:
- **커스텀 인증**: Proxy config.yaml의 `custom_auth` 옵션에 커스텀 인증 모듈 경로 지정 (`user_custom_auth_path`)
- **JWT 연동**: Coco Admin의 JWT 토큰을 LiteLLM에서 검증하도록 설정
- **API 키 매핑**: LiteLLM 키를 Coco 사용자/프로젝트에 매핑

#### 감사 로그

- `audit_log_callbacks` 리스트에 커스텀 감사 로거 등록
- 모든 LLM 호출에 대한 감사 추적 (누가, 언제, 어떤 모델, 입력/출력)
- Coco의 감사 추적 시스템과 통합하여 규제 컴플라이언스 충족

### 7.4 온프레미스/폐쇄망 배포 고려사항

LiteLLM을 폐쇄망에서 운영할 때의 고려사항:

| 영역 | 고려사항 | 대응 방안 |
|------|---------|---------|
| **외부 API 차단** | 프로바이더 API 접근 불가 | vLLM/Ollama 등 로컬 프로바이더만 사용 |
| **모델 가격 업데이트** | 온라인 가격 DB 접근 불가 | `model_prices_and_context_window.json` 수동 관리 또는 custom pricing 사용 |
| **pip 패키지** | PyPI 접근 불가 | 사전 빌드된 Docker 이미지 또는 내부 PyPI 미러 |
| **시크릿 관리** | 외부 KMS 접근 불가 | 환경변수 또는 로컬 파일 기반 시크릿 |
| **텔레메트리** | 외부 관측 서비스 불가 | Prometheus + 내부 Grafana 구성 |
| **DB** | 내부 PostgreSQL + Redis 구성 | docker-compose로 올인원 배포 |
| **라이선스** | Enterprise 라이선스 검증 | 오프라인 라이선스 키 지원 확인 필요 |
| **Admin UI** | 번들 포함 | Docker 이미지에 사전 빌드 포함 |

### 7.5 교차 참조

- `../../02_implementation/06_vllm_rd_plan_ko.md` — vLLM 인프라 고도화 R&D 계획, LiteLLM 멀티 모델 라우팅 섹션
- `../../01_strategy/04_product_overview_ko.md` — Coco 제품 구성 (Engine, Studio, CLI)
- `../../02_implementation/01_roadmap_ko.md` — Phase 2 구현 로드맵

---

## 8. 참고자료 및 추가 탐색 가이드

### 8.1 공식 자료

| 자료 | URL |
|------|-----|
| 공식 문서 | https://docs.litellm.ai |
| GitHub | https://github.com/BerriAI/litellm |
| Discord | https://discord.gg/litellm |
| PyPI | https://pypi.org/project/litellm |
| Docker Hub | ghcr.io/berriai/litellm |

### 8.2 추천 코드 읽기 순서

1. **`ARCHITECTURE.md`** — 전체 아키텍처 개요, 요청 흐름 다이어그램
2. **`litellm/__init__.py`** — 글로벌 설정, 콜백 리스트, 상수 정의
3. **`litellm/main.py`** — SDK 진입점, `completion()` 함수 흐름 이해
4. **`litellm/litellm_core_utils/get_llm_provider_logic.py`** — 모델명 → 프로바이더 매핑 로직
5. **`litellm/llms/base_llm/chat/transformation.py`** — BaseConfig 추상 클래스, 프로바이더가 구현해야 할 인터페이스
6. **`litellm/llms/custom_httpx/llm_http_handler.py`** — BaseLLMHTTPHandler, 중앙 HTTP 오케스트레이터
7. **`litellm/llms/openai/chat/gpt_transformation.py`** — 가장 기본적인 프로바이더 구현 (OpenAI)
8. **`litellm/router.py`** — Router 클래스, 라우팅 전략, Fallback/Retry
9. **`litellm/router_strategy/`** — 6가지 라우팅 전략 구현 상세
10. **`litellm/proxy/proxy_server.py`** — FastAPI 앱, 엔드포인트 등록
11. **`litellm/proxy/auth/user_api_key_auth.py`** — 인증 흐름
12. **`litellm/caching/dual_cache.py`** — DualCache 이중 캐시 메커니즘
13. **`litellm/cost_calculator.py`** — 비용 계산 로직
14. **`litellm/integrations/custom_logger.py`** — 콜백 시스템 베이스 클래스

### 8.3 주요 설정 파일

| 파일 | 위치 | 용도 |
|------|------|------|
| `pyproject.toml` | 루트 | 패키지 메타데이터, 의존성 |
| `proxy_server_config.yaml` | 루트 | Proxy 기본 설정 예시 |
| `model_prices_and_context_window.json` | 루트 | 모델별 가격/컨텍스트 데이터 |
| `schema.prisma` | `litellm/proxy/` | PostgreSQL 스키마 |
| `Dockerfile` | 루트 | Docker 빌드 |
| `docker-compose.yml` | 루트 | Docker Compose 구성 |
| `provider_endpoints_support.json` | 루트 | 프로바이더별 지원 기능 매트릭스 |

---

## 변경이력

| 버전 | 일자 | 변경 내용 | 작성자 |
|------|------|----------|--------|
| 1.0 | 2026-03-23 | 초안 작성 — LiteLLM v1.82.6 심층 분석 | 분석팀 |
