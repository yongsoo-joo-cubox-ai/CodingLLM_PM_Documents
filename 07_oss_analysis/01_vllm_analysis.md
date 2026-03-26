# vLLM 심층 기술 분석

| 항목 | 내용 |
|------|------|
| **문서번호** | SAI-KB-2026-002 |
| **작성일** | 2026년 3월 23일 |
| **버전** | v1.0 |
| **보안등급** | 일반 |
| **작성** | Secern AI |
| **분석 대상 버전** | v0.18.x (커밋 `35141a7ee` 기준) |

---

> **TL;DR**
> - vLLM은 UC Berkeley에서 시작된 Apache 2.0 오픈소스 LLM 추론 엔진으로, PagedAttention과 Continuous Batching을 핵심으로 높은 처리량과 메모리 효율을 달성한다.
> - v0.18.x 기준 Python 파일 1,452개, 약 54만 LOC 규모이며, 321개 이상의 모델 아키텍처를 지원한다.
> - V1 엔진 아키텍처는 ZMQ 기반 멀티프로세스 통신, msgspec 직렬화, asyncio 기반 비동기 처리로 재설계되었다.
> - Tensor Parallelism, Pipeline Parallelism, Data Parallelism, Expert Parallelism 등 다양한 분산 추론을 지원하며, EAGLE/Medusa/N-gram 기반 Speculative Decoding을 포함한다.
> - 대상 독자: LLM 인프라 엔지니어, 백엔드 개발자 | 소요 시간: 30~40분

---

## 1. 프로젝트 개요

### 1.1 목적과 배경

vLLM(virtual Large Language Model)은 UC Berkeley Sky Computing Lab에서 2023년 개발을 시작한 고성능 LLM 추론 및 서빙 엔진이다. "PagedAttention" 논문(Kwon et al., 2023)에서 제안한 KV Cache 페이징 기법을 구현한 것이 출발점이며, 현재는 LLM 추론 엔진 분야에서 사실상의 표준으로 자리잡았다.

**라이선스**: Apache 2.0 — 상업적 사용, 수정, 재배포 자유

**핵심 가치**:
- 높은 처리량(Throughput): Continuous Batching + PagedAttention으로 동시 요청 처리 극대화
- 메모리 효율: KV Cache 페이징으로 GPU 메모리 낭비 최소화 (논문 벤치마크 기준, 기존 대비 최대 24배 처리량 향상)
- OpenAI 호환 API: 기존 OpenAI 클라이언트 코드 변경 없이 전환 가능
- 광범위한 모델 지원: HuggingFace 생태계 모델 321개 이상 지원

### 1.2 핵심 수치

| 항목            | 값                                                            |
| ------------- | ------------------------------------------------------------ |
| 분석 버전         | v0.18.1rc0 (커밋 `35141a7ee`)                                  |
| Python 파일 수   | 1,452개 (`vllm/` 패키지)                                         |
| 총 코드 라인 수     | ~544,585 LOC                                                 |
| 지원 모델 아키텍처    | 321개 (`vllm/model_executor/models/`)                         |
| 지원 양자화 방식     | GPTQ, AWQ, FP8, BitsAndBytes, GGUF, Compressed Tensors 등 20+ |
| 지원 Python 버전  | 3.10 ~ 3.13                                                  |
| 핵심 의존성 (CUDA) | PyTorch 2.10.0, transformers >= 4.56.0                       |
| 빌드 시스템        | setuptools + CMake + Ninja (CUDA/C++ 커널 컴파일)                 |

### 1.3 경쟁 제품 대비 차별점

| 비교 항목 | vLLM | TGI (HuggingFace) | TensorRT-LLM (NVIDIA) | Ollama |
|-----------|------|-----|---------------|--------|
| **핵심 기술** | PagedAttention + Continuous Batching | Continuous Batching + Flash Attention | FP8/INT4 최적화 + Inflight Batching | llama.cpp 기반 GGUF |
| **모델 지원** | 321+ 아키텍처 | HF 모델 중심 (제한적) | NVIDIA 최적화 모델 | GGUF 포맷 한정 |
| **분산 추론** | TP/PP/DP/EP 모두 지원 | TP만 지원 | TP/PP 지원 | 미지원 |
| **API 호환** | OpenAI 완전 호환 | OpenAI 부분 호환 | Triton 서버 | 자체 API |
| **양자화** | GPTQ/AWQ/FP8/BnB/GGUF 등 | GPTQ/AWQ/BnB | FP8/INT4/INT8 | GGUF (Q4/Q5/Q8) |
| **라이선스** | Apache 2.0 | Apache 2.0 | Apache 2.0 | MIT |
| **Speculative Decoding** | EAGLE/Medusa/N-gram | 제한적 | 지원 | 미지원 |
| **온프레미스 적합성** | 매우 높음 (순수 Python + CUDA) | 높음 | 높음 (NVIDIA GPU 필수) | 매우 높음 (CPU 가능) |
| **대상** | 프로덕션 서빙 | 프로덕션 서빙 | 최고 성능 추론 | 로컬 개발/테스트 |

vLLM의 가장 큰 차별점은 **모델 지원 범위의 광범위함**과 **분산 추론의 유연성**, 그리고 **활발한 커뮤니티** 기반의 빠른 발전 속도다. TensorRT-LLM이 단일 GPU 성능에서 우위를 점할 수 있지만, vLLM은 다양한 하드웨어(CUDA, ROCm, TPU, XPU)와 모델을 지원하며, OpenAI 호환 API로 통합 비용이 낮다.

---

## 2. 아키텍처 심층 분석

### 2.1 전체 아키텍처 다이어그램

```
                              ┌─────────────────────────────────────┐
                              │         클라이언트 (HTTP/gRPC)         │
                              └──────────────┬──────────────────────┘
                                             │
                              ┌──────────────▼──────────────────────┐
                              │   OpenAI 호환 API 서버 (FastAPI)      │
                              │   vllm/entrypoints/openai/           │
                              │   - /v1/completions                  │
                              │   - /v1/chat/completions             │
                              │   - /v1/embeddings                   │
                              │   - /v1/models                       │
                              └──────────────┬──────────────────────┘
                                             │
                              ┌──────────────▼──────────────────────┐
                              │         AsyncLLM (프론트엔드)          │
                              │   vllm/v1/engine/async_llm.py        │
                              │   - InputProcessor (전처리)            │
                              │   - OutputProcessor (후처리)           │
                              │   - EngineCoreClient (엔진 통신)       │
                              └──────────────┬──────────────────────┘
                                             │ ZMQ (IPC/TCP)
                              ┌──────────────▼──────────────────────┐
                              │     EngineCore (백엔드, 별도 프로세스)    │
                              │   vllm/v1/engine/core.py              │
                              │   - Scheduler (스케줄링)               │
                              │   - KVCacheManager (캐시 관리)         │
                              │   - StructuredOutputManager           │
                              └──────────────┬──────────────────────┘
                                             │
                              ┌──────────────▼──────────────────────┐
                              │         Executor (실행기)              │
                              │   vllm/v1/executor/                   │
                              │   - UniProcExecutor (단일 프로세스)      │
                              │   - MultiprocExecutor (멀티 프로세스)   │
                              │   - RayDistributedExecutor (Ray)      │
                              └──────────────┬──────────────────────┘
                                             │
                              ┌──────────────▼──────────────────────┐
                              │       Worker + GPUModelRunner      │
                              │   vllm/v1/worker/gpu_worker.py        │
                              │   vllm/v1/worker/gpu_model_runner.py  │
                              │   - 모델 로딩 / KV Cache 할당           │
                              │   - Attention 연산 / 토큰 샘플링         │
                              │   - Speculative Decoding               │
                              └──────────────┬──────────────────────┘
                                             │
                              ┌──────────────▼──────────────────────┐
                              │          모델 (PyTorch nn.Module)      │
                              │   vllm/model_executor/models/          │
                              │   - 321+ 아키텍처 (LLaMA, Qwen, etc.) │
                              │   - 양자화 레이어                       │
                              │   - LoRA 어댑터                        │
                              └────────────────────────────────────────┘
```

### 2.2 V1 엔진 아키텍처 상세 분석

v0.18.x에서 vLLM은 V1 엔진을 기본으로 사용한다. V1은 이전 엔진(레거시) 대비 근본적으로 재설계된 아키텍처다.

**V1의 핵심 설계 원칙**:

1. **멀티프로세스 분리**: AsyncLLM(프론트엔드)과 EngineCore(백엔드)를 별도 프로세스로 분리하고 ZMQ 소켓으로 통신한다. 이를 통해 API 서버의 asyncio 이벤트 루프와 GPU 연산이 서로 블로킹하지 않는다.

2. **msgspec 기반 직렬화**: 엔진 간 통신에 `msgspec.msgpack`을 사용하여 직렬화/역직렬화 오버헤드를 최소화한다. `EngineCoreRequest`, `EngineCoreOutput`, `EngineCoreOutputs` 등 핵심 데이터 구조체가 모두 `msgspec.Struct`로 정의되어 있다 (`vllm/v1/engine/__init__.py`).

3. **비동기 스케줄링**: `async_scheduling` 옵션으로 스케줄링과 모델 실행을 오버랩할 수 있다. Pipeline Parallelism에서는 `batch_queue`를 통해 파이프라인 버블을 제거한다.

4. **Zero-copy 텐서 전송**: `TensorIpcSender`/`TensorIpcReceiver` (`vllm/v1/engine/tensor_ipc.py`)를 통해 GPU 텐서를 프로세스 간 복사 없이 공유한다.

**V1 vs 레거시 엔진 차이점**:

| 항목 | V1 엔진 | 레거시 엔진 |
|------|---------|------------|
| 프로세스 모델 | 멀티프로세스 (ZMQ) | 단일 프로세스 |
| 직렬화 | msgspec (고성능) | Python pickle |
| 스케줄러 | Iteration-level Continuous Batching | Sequence-group 기반 |
| KV Cache | BlockPool 기반, 그룹화된 캐시 | 단순 블록 할당자 |
| 텐서 전송 | IPC (Zero-copy) | 메모리 복사 |
| 코드 위치 | `vllm/v1/` | `vllm/engine/` (deprecated) |

현재 `vllm/engine/llm_engine.py`와 `vllm/engine/async_llm_engine.py`는 각각 7줄의 래퍼로, V1 엔진으로 위임하는 구조다.

### 2.3 요청 흐름 추적

HTTP 요청이 최종 응답으로 변환되는 전체 과정:

```
1. HTTP 요청 수신
   └─ FastAPI 라우터 (vllm/entrypoints/openai/api_server.py)
   └─ OpenAIServingChat / OpenAIServingCompletion

2. 전처리 (AsyncLLM)
   └─ InputProcessor (vllm/v1/engine/input_processor.py)
      ├─ 토큰화 (tokenizer)
      ├─ 멀티모달 입력 처리
      ├─ SamplingParams 검증
      └─ EngineCoreRequest 생성

3. 엔진 코어 전송
   └─ EngineCoreClient (vllm/v1/engine/core_client.py)
      ├─ AsyncMPClient: ZMQ 소켓으로 EngineCore 프로세스에 전송
      ├─ SyncMPClient: 동기 ZMQ 통신 (LLM 오프라인 모드)
      └─ InprocClient: 인프로세스 직접 호출

4. 스케줄링
   └─ Scheduler.schedule() (vllm/v1/core/sched/scheduler.py)
      ├─ waiting 큐에서 요청 선택
      ├─ KVCacheManager로 블록 할당
      ├─ Continuous Batching: prefill + decode 혼합 배치
      ├─ Preemption 판단 (메모리 부족 시)
      └─ SchedulerOutput 생성

5. 모델 실행
   └─ Executor.execute_model() (vllm/v1/executor/)
      └─ Worker.execute_model() (vllm/v1/worker/gpu_worker.py)
         └─ GPUModelRunner.execute_model() (vllm/v1/worker/gpu_model_runner.py)
            ├─ 입력 텐서 준비 (InputBatch)
            ├─ Attention 메타데이터 구성
            ├─ nn.Module forward (실제 모델 추론)
            ├─ Speculative Decoding (설정 시)
            └─ 토큰 샘플링

6. 출력 처리
   └─ Scheduler.update_from_output()
      ├─ 생성된 토큰 기록
      ├─ 정지 조건 검사 (stop tokens, max_tokens)
      ├─ KV 블록 해시 업데이트 (prefix caching)
      └─ EngineCoreOutputs 생성

7. 후처리 (AsyncLLM)
   └─ OutputProcessor (vllm/v1/engine/output_processor.py)
      ├─ 디토큰화 (IncrementalDetokenizer)
      ├─ Logprobs 처리
      ├─ RequestOutput 생성
      └─ SSE 스트리밍 or 전체 응답 반환

8. HTTP 응답
   └─ StreamingResponse (SSE) 또는 JSONResponse
```

### 2.4 동시성 모델

- **API 서버**: uvloop 기반 asyncio (`uvloop`이 기본 설정). FastAPI + Uvicorn으로 수천 개의 동시 HTTP 연결 처리.
- **AsyncLLM**: asyncio 이벤트 루프에서 입력 전처리와 출력 후처리를 비동기로 수행. EngineCoreClient가 ZMQ 소켓을 통해 EngineCore의 출력을 비동기로 수신.
- **EngineCore**: 별도 프로세스에서 동기 메인 루프 실행. `run_busy_loop()`에서 ZMQ 소켓으로 요청을 수신하고, `step()` → `schedule()` → `execute_model()` → `update_from_output()` 사이클을 반복.
- **배치 스케줄링**: Iteration-level에서 동적 배치 크기 조정. 매 iteration마다 새 요청을 prefill하거나, 기존 요청의 decode를 이어간다.

---

## 3. 코드베이스 상세 구조

### 3.1 전체 디렉토리 트리

```
vllm/
├── v1/                           # V1 엔진 (현재 기본)
│   ├── engine/                   # 엔진 프론트엔드/백엔드
│   │   ├── async_llm.py          # AsyncLLM 클래스 (41.4K)
│   │   ├── core.py               # EngineCore 클래스 (80.9K)
│   │   ├── core_client.py        # 엔진 통신 클라이언트 (65.5K)
│   │   ├── input_processor.py    # 입력 전처리 (17.7K)
│   │   ├── output_processor.py   # 출력 후처리 (30.4K)
│   │   ├── detokenizer.py        # 디토큰화 (12.4K)
│   │   ├── llm_engine.py         # LLMEngine 래퍼 (16.4K)
│   │   └── utils.py              # 유틸리티 (44.0K)
│   ├── core/                     # 스케줄러 및 KV Cache 관리
│   │   ├── sched/                # 스케줄러 구현
│   │   │   ├── scheduler.py      # Scheduler 메인 클래스
│   │   │   ├── async_scheduler.py
│   │   │   ├── interface.py      # SchedulerInterface 정의
│   │   │   ├── output.py         # SchedulerOutput
│   │   │   └── request_queue.py  # 우선순위 큐
│   │   ├── kv_cache_manager.py   # KVCacheManager (20.8K)
│   │   ├── block_pool.py         # BlockPool — 블록 할당 (19.6K)
│   │   ├── kv_cache_utils.py     # KV 캐시 유틸 (65.0K)
│   │   ├── kv_cache_coordinator.py  # 블록 해시 → 블록 매핑
│   │   └── single_type_kv_cache_manager.py  # 단일 타입 관리자 (47.6K)
│   ├── worker/                   # GPU/CPU/TPU 워커
│   │   ├── gpu_model_runner.py   # GPU 모델 러너 (291.2K) ← 최대 파일
│   │   ├── gpu_worker.py         # GPU 워커 (43.4K)
│   │   ├── gpu_input_batch.py    # 입력 배치 관리 (43.3K)
│   │   ├── block_table.py        # 블록 테이블 (13.0K)
│   │   └── cpu_worker.py         # CPU 워커 (9.7K)
│   ├── executor/                 # 실행기 추상화
│   │   ├── abstract.py           # Executor 인터페이스
│   │   ├── uniproc_executor.py   # 단일 프로세스 실행기
│   │   ├── multiproc_executor.py # 멀티프로세스 실행기
│   │   └── ray_*.py              # Ray 분산 실행기
│   ├── attention/                # Attention 백엔드
│   │   ├── backends/             # Flash Attention, FlashInfer, Triton 등
│   │   ├── backend.py            # 공통 Attention 메타데이터 (32.2K)
│   │   └── selector.py           # 백엔드 자동 선택
│   ├── spec_decode/              # Speculative Decoding
│   │   ├── eagle.py              # EAGLE 구현 (75.9K)
│   │   ├── medusa.py             # Medusa 구현 (2.6K)
│   │   ├── ngram_proposer.py     # N-gram 제안자
│   │   └── metrics.py            # 스펙 디코딩 통계
│   └── sample/                   # 샘플링
│
├── entrypoints/                  # 진입점
│   ├── openai/                   # OpenAI 호환 API 서버
│   │   ├── api_server.py         # 메인 서버 (FastAPI)
│   │   ├── chat_completion/      # Chat Completion 핸들러
│   │   ├── completion/           # Completion 핸들러
│   │   ├── generate/             # 범용 생성 핸들러
│   │   ├── responses/            # Responses API
│   │   └── models/               # 모델 관리
│   ├── mcp/                      # MCP (Model Context Protocol) 서버
│   │   ├── tool.py               # MCP 도구 정의
│   │   └── tool_server.py        # MCP 도구 서버
│   ├── cli/                      # CLI 진입점 (vllm serve, vllm bench 등)
│   ├── llm.py                    # Python SDK (vllm.LLM) (83.1K)
│   ├── chat_utils.py             # 채팅 유틸리티 (58.3K)
│   └── grpc_server.py            # gRPC 서버
│
├── model_executor/               # 모델 실행
│   ├── models/                   # 321개 모델 구현
│   ├── layers/                   # 커스텀 레이어
│   │   ├── attention/            # Attention 레이어
│   │   ├── quantization/         # 양자화 구현 (20+ 방식)
│   │   ├── fused_moe/            # MoE Fused 커널
│   │   ├── rotary_embedding/     # RoPE 구현
│   │   ├── linear.py             # 병렬 Linear 레이어
│   │   └── layernorm.py          # LayerNorm
│   ├── model_loader/             # 모델 로더
│   │   ├── default_loader.py     # HuggingFace 모델 로딩
│   │   ├── sharded_state_loader.py  # 샤딩된 체크포인트
│   │   ├── gguf_loader.py        # GGUF 포맷
│   │   └── weight_utils.py       # 가중치 유틸리티
│   └── parameter.py              # 모델 파라미터 관리
│
├── distributed/                  # 분산 처리
│   ├── parallel_state.py         # 병렬 상태 관리 (74.7K)
│   ├── communication_op.py       # 통신 연산
│   ├── device_communicators/     # 디바이스 통신 (NCCL, Gloo 등)
│   ├── kv_transfer/              # KV Cache 전송 (P/D 분리)
│   ├── eplb/                     # Expert-Level Load Balancing
│   └── elastic_ep/               # Elastic Expert Parallelism
│
├── config/                       # 설정 클래스 (26개 모듈)
│   ├── vllm.py                   # VllmConfig (최상위 설정) (77.7K)
│   ├── model.py                  # ModelConfig (83.7K)
│   ├── cache.py                  # CacheConfig (10.8K)
│   ├── parallel.py               # ParallelConfig (33.9K)
│   ├── scheduler.py              # SchedulerConfig (12.4K)
│   ├── speculative.py            # SpeculativeConfig (36.9K)
│   ├── compilation.py            # CompilationConfig (53.5K)
│   └── ...                       # 기타 설정
│
├── lora/                         # LoRA 어댑터
│   ├── lora_model.py             # LoRA 모델 래퍼
│   ├── lora_weights.py           # LoRA 가중치 관리
│   ├── model_manager.py          # LoRA 모델 매니저
│   ├── punica_wrapper/           # Punica 커널 래퍼
│   └── layers/                   # LoRA 레이어 구현
│
├── compilation/                  # torch.compile / CUDAGraph
├── multimodal/                   # 멀티모달 입력 처리
├── tokenizers/                   # 토크나이저 추상화
├── reasoning/                    # 추론 체인 (CoT 파싱)
├── tool_parsers/                 # 도구 호출 파싱
├── platforms/                    # 플랫폼 추상화 (CUDA, ROCm, TPU, XPU)
├── profiler/                     # 프로파일링
├── tracing/                      # OpenTelemetry 트레이싱
└── third_party/                  # 서드파티 코드
```

### 3.2 핵심 모듈 상세

#### 3.2.1 `vllm/v1/engine/` — 엔진 프론트엔드/백엔드

| 파일 | 크기 | 역할 |
|------|------|------|
| `core.py` | 80.9K | **EngineCore**: 스케줄러+실행기 통합. `step()` 메서드가 한 iteration의 schedule→execute→update 사이클 수행. `EngineCoreProc`는 별도 프로세스에서 메인 루프 실행 |
| `core_client.py` | 65.5K | **EngineCoreClient**: 프론트엔드↔백엔드 통신 추상화. `InprocClient`(인프로세스), `SyncMPClient`(동기 ZMQ), `AsyncMPClient`(비동기 ZMQ) 서브클래스 |
| `async_llm.py` | 41.4K | **AsyncLLM**: API 서버용 비동기 엔진. `generate()` AsyncGenerator로 토큰 스트리밍. InputProcessor/OutputProcessor 관리 |
| `output_processor.py` | 30.4K | **OutputProcessor**: EngineCoreOutput을 RequestOutput으로 변환. 디토큰화, logprobs 처리, 완료 판정 |
| `input_processor.py` | 17.7K | **InputProcessor**: 프롬프트 토큰화, 멀티모달 전처리, EngineCoreRequest 생성 |
| `llm_engine.py` | 16.4K | **LLMEngine**: 동기 엔진 래퍼. `vllm.LLM` Python SDK에서 사용 |
| `detokenizer.py` | 12.4K | **IncrementalDetokenizer** (Fast/Slow 구현): 증분 디토큰화 |

#### 3.2.2 `vllm/v1/core/` — 스케줄러 및 KV Cache 관리

`Scheduler` 클래스 (`vllm/v1/core/sched/scheduler.py`)가 핵심이다:
- **스케줄링 정책**: `SchedulingPolicy` 열거형 — FCFS(기본), Priority 등
- **요청 큐**: `waiting` (대기), `running` (실행 중), `skipped_waiting` (비동기 의존성 대기)
- **KVCacheManager**: 블록 할당/해제, prefix caching, preemption 판단
- **Continuous Batching**: 매 iteration마다 prefill과 decode 요청을 혼합하여 배치 구성

#### 3.2.3 `vllm/model_executor/` — 모델 실행

- `models/`: 321개 모델 구현. 각 파일이 HuggingFace 모델을 vLLM의 PagedAttention과 호환되도록 재구현. `__init__.py`에서 모델 이름 → 클래스 매핑 관리.
- `layers/quantization/`: 20가지 이상의 양자화 구현. `base_config.py`의 `QuantizationConfig` 인터페이스를 따른다.
- `model_loader/`: `DefaultModelLoader`가 HuggingFace 모델을 로드하고, 가중치를 TP 샤딩하여 각 GPU에 분배.

#### 3.2.4 `vllm/distributed/` — 분산 처리

- `parallel_state.py` (74.7K): NVIDIA Megatron-LM 기반 병렬 상태 관리. `init_distributed_environment()` → `initialize_model_parallel()` 흐름으로 TP/PP/DP 그룹 초기화.
- `device_communicators/`: NCCL, Gloo, 커스텀 통신 구현
- `kv_transfer/`: Prefill/Decode 분리 (P/D disaggregation) 아키텍처 지원

### 3.3 진입점

| 진입점 | 경로 | 용도 |
|--------|------|------|
| `vllm serve` | `vllm/entrypoints/cli/serve.py` → `openai/api_server.py` | OpenAI 호환 API 서버 실행 |
| `vllm bench` | `vllm/entrypoints/cli/benchmark/` | 벤치마크 실행 |
| `vllm.LLM` | `vllm/entrypoints/llm.py` | Python SDK (오프라인 배치 추론) |
| `AsyncLLM` | `vllm/v1/engine/async_llm.py` | API 서버 내부에서 사용하는 비동기 엔진 |

### 3.4 빌드 시스템

```
pyproject.toml
├── build-system: setuptools + CMake + Ninja
├── [project.scripts]: vllm → vllm.entrypoints.cli.main:main
└── dynamic: version (setuptools-scm), dependencies

setup.py
├── CMake 확장 빌드 (csrc/ 디렉토리)
├── CUDA 커널 컴파일 (csrc/*.cu)
└── C++ 커스텀 ops 컴파일

CMakeLists.txt
├── csrc/ 하위 CUDA/C++ 소스 컴파일
├── Flash Attention, PagedAttention CUDA 커널
└── 양자화 커널 (GPTQ, AWQ, FP8)
```

`csrc/` 디렉토리에는 성능 핵심 CUDA/C++ 커널이 있으며, 빌드 시 CMake를 통해 컴파일된다. Python 패키지의 `vllm._custom_ops`로 로드된다.

---

## 4. 핵심 기술 메커니즘

### 4.1 PagedAttention

PagedAttention은 vLLM의 근간 기술로, OS의 가상 메모리 페이징 개념을 KV Cache 관리에 적용한 것이다.

**핵심 원리**:
- 기존 방식: 요청마다 `max_seq_len` 크기의 연속 메모리를 미리 할당 → 실제 사용량과 무관하게 메모리 낭비
- PagedAttention: KV Cache를 고정 크기 **블록**(기본 16 토큰)으로 분할하여, 필요할 때 동적 할당

**논리/물리 블록 매핑**:
```
논리 블록 (요청 A):  [0] [1] [2] [3]
                       ↓   ↓   ↓   ↓
물리 블록 (GPU 메모리): [7] [3] [15] [22]    ← 비연속 할당 가능
```

**구현 코드 경로**:

1. **KVCacheBlock** (`vllm/v1/core/kv_cache_utils.py`): 블록의 기본 단위. `block_id`, `block_hash`, `ref_cnt` (참조 카운트) 필드를 가진다.

2. **BlockPool** (`vllm/v1/core/block_pool.py`): 물리 블록의 할당/해제를 관리하는 풀. `FreeKVCacheBlockQueue`(`kv_cache_utils.py`에 정의, 이중 연결 리스트)로 빈 블록을 관리한다. 블록이 해제될 때 즉시 삭제하지 않고 큐 끝에 넣어 prefix caching에 재활용할 수 있게 한다.

3. **KVCacheManager** (`vllm/v1/core/kv_cache_manager.py`): 스케줄러가 사용하는 상위 인터페이스. `allocate_slots()`로 요청에 블록 할당, `free()` 로 해제. `KVCacheBlocks` 데이터클래스가 KV 캐시 그룹별 블록 목록을 담는다.

4. **SingleTypeKVCacheManager** (`vllm/v1/core/single_type_kv_cache_manager.py`, 47.6K): 단일 KV 캐시 타입(예: Attention)에 대한 상세 구현. `KVCacheManager.get_computed_blocks()`로 prefix cache 히트를 검색하고, `allocate_new_blocks()`로 새 블록을 할당한다.

5. **KVCacheCoordinator** (`vllm/v1/core/kv_cache_coordinator.py`): 블록 해시 → 블록 매핑 관리. `BlockHashToBlockMap`이 prefix caching의 핵심 자료구조로, 해시 값으로 이미 계산된 KV 블록을 찾는다.

6. **BlockTable** (`vllm/v1/worker/block_table.py`): GPU 워커 측에서 논리 블록 → 물리 블록 매핑을 관리. `block_table` 텐서가 각 요청의 물리 블록 ID 배열을 담아 Attention 커널에 전달된다.

**함수 호출 체인** (블록 할당):
```
Scheduler.schedule()
  → KVCacheManager.allocate_slots(request, num_tokens)
    → KVCacheManager.get_computed_blocks()  # prefix cache 검색
    → SingleTypeKVCacheManager.allocate_new_blocks()   # 신규 블록 할당
      → BlockPool.get_new_blocks(num_blocks)
        → FreeKVCacheBlockQueue.popleft()             # 빈 블록 꺼내기
    → KVCacheBlocks 반환 (할당된 블록 목록)
```

### 4.2 Continuous Batching

Continuous Batching은 요청을 iteration(단일 forward pass) 단위로 스케줄링하는 기법이다. 전통적인 static batching과 달리, 각 iteration마다 완료된 요청은 빠져나가고 새 요청이 들어올 수 있다.

**구현** (`vllm/v1/core/sched/scheduler.py` — `Scheduler.schedule()`):

1. **Decode 우선**: 이미 실행 중인 `running` 요청들의 decode 토큰을 먼저 예산에 포함
2. **Prefill 삽입**: 남은 토큰 예산 내에서 `waiting` 큐의 새 요청을 prefill
3. **동적 배치**: `max_num_scheduled_tokens` 한도 내에서 prefill + decode 혼합
4. **Chunked Prefill**: 긴 프롬프트를 여러 iteration에 나누어 prefill (decode 지연 최소화)

**Preemption 전략**:
- GPU 메모리(KV Cache 블록)가 부족하면 우선순위가 낮은 요청을 preempt
- preempt된 요청은 `waiting` 큐로 돌아가 재스케줄링
- 블록 스왑(GPU↔CPU) 또는 재계산(recomputation) 방식 선택 가능

**스케줄링 제약**:
```python
# vllm/v1/core/sched/scheduler.py 내부
self.max_num_running_reqs = self.scheduler_config.max_num_seqs
self.max_num_scheduled_tokens = self.scheduler_config.max_num_scheduled_tokens
self.max_model_len = vllm_config.model_config.max_model_len
```

### 4.3 Speculative Decoding

Speculative Decoding은 작은 draft 모델로 여러 토큰을 미리 생성한 뒤, 큰 target 모델로 한번에 검증하여 추론 속도를 높이는 기법이다.

**지원 방식** (`vllm/v1/spec_decode/`):

| 방식 | 파일 | 설명 |
|------|------|------|
| **EAGLE** | `eagle.py` (75.9K) | Feature-level autoregressive 기반. Draft 모델이 hidden states를 입력받아 다음 토큰 예측. EAGLE-2, EAGLE-3 변형 포함 |
| **Medusa** | `medusa.py` (2.6K) | 단일 모델에 여러 prediction head 추가. 각 head가 서로 다른 미래 위치의 토큰 예측 |
| **N-gram** | `ngram_proposer.py` (10.7K) | 학습 없이 이전 생성 토큰의 n-gram 패턴으로 다음 토큰 제안. GPU 버전도 존재 (`ngram_proposer_gpu.py`) |
| **Suffix Decoding** | `suffix_decoding.py` (4.3K) | 접미사 트리 기반 제안 |

**EAGLE 구현 상세** (`vllm/v1/spec_decode/eagle.py`):
- `SpecDecodeBaseProposer`: 공통 기반 클래스. `vllm_config.speculative_config`에서 설정 읽기
- `EagleProposer`: EAGLE 전용 구현. draft 모델의 hidden states를 tree attention으로 처리
- Tree Attention: 여러 후보 토큰을 트리 구조로 동시 검증 (`vllm/v1/attention/backends/tree_attn.py`)

**함수 호출 체인** (Speculative Decoding 시):
```
GPUModelRunner.execute_model()
  → model.forward()                        # target 모델 forward
  → SpecDecodeProposer.propose()           # draft 토큰 생성
    → EagleProposer.propose()
      → draft_model.forward()              # draft 모델 forward
      → TreeAttention으로 후보 검증
  → Sampler.forward()                      # 최종 토큰 선택 (accept/reject)
```

### 4.4 KV Cache 관리

#### 4.4.1 블록 할당자 (Block Allocator)

`BlockPool` (`vllm/v1/core/block_pool.py`)이 물리 블록의 할당/해제를 관리한다.

- **FreeKVCacheBlockQueue**: 이중 연결 리스트 기반 자유 블록 큐. `popleft()`로 할당, `append()`로 해제. 리스트 기반이라 O(1) 연산.
- **참조 카운트**: `KVCacheBlock.ref_cnt`로 여러 요청이 공유하는 블록(prefix caching) 관리. ref_cnt가 0이 되면 자유 블록 큐로 반환.
- **Eviction 정책**: LRU 기반. 자유 블록 큐의 앞쪽(가장 오래된)부터 evict.

#### 4.4.2 Prefix Caching

동일한 시스템 프롬프트나 few-shot 예시를 공유하는 요청들이 KV Cache를 재활용한다.

- **블록 해시**: 블록의 토큰 시퀀스를 해시(SHA-256 기본, xxhash 옵션)하여 `BlockHash` 생성
- **해시 맵**: `BlockHashToBlockMap`이 해시 → 블록 매핑 유지
- **캐시 히트**: 새 요청이 들어오면 `get_computed_blocks()`가 프롬프트의 블록 해시를 검색하여 이미 계산된 블록 재활용
- **캐시 솔트**: `cache_salt` 파라미터로 멀티테넌트 환경에서 캐시 격리 가능

```python
# vllm/config/cache.py
class CacheConfig:
    enable_prefix_caching: bool = True  # 기본 활성화
    prefix_caching_hash_algo: PrefixCachingHashAlgo = "sha256"
```

#### 4.4.3 KV Cache 오프로딩

`vllm/v1/kv_offload/` 디렉토리에서 GPU → CPU 또는 원격 저장소로의 KV Cache 오프로딩을 지원한다. LMCache 백엔드 연동도 가능하다 (`KVOffloadingBackend = Literal["native", "lmcache"]`).

### 4.5 모델 로딩 파이프라인

```
사용자 지정 모델 (HuggingFace ID 또는 로컬 경로)
  │
  ▼
ModelConfig 생성 (vllm/config/model.py)
  ├─ HuggingFace config 다운로드/로드
  ├─ 양자화 설정 감지 (GPTQ, AWQ, FP8 등)
  ├─ max_model_len 결정
  └─ dtype 결정 (auto → bfloat16/float16)
  │
  ▼
DefaultModelLoader.load_model() (vllm/model_executor/model_loader/default_loader.py)
  ├─ 모델 클래스 결정 (registry에서 아키텍처 이름으로 검색)
  ├─ 빈 모델 인스턴스화 (메타 디바이스에서)
  ├─ 가중치 다운로드 (safetensors/pt/gguf)
  │   ├─ safetensors_weights_iterator(): 안전한 텐서 로딩
  │   ├─ multi_thread_safetensors_weights_iterator(): 멀티스레드 로딩
  │   └─ fastsafetensors_weights_iterator(): 병렬 로딩 최적화
  ├─ 가중치 샤딩: TP에 따라 각 GPU에 분배
  │   └─ weight_loader() 콜백으로 레이어별 분할
  └─ 양자화 적용 (QuantizationConfig.apply())
```

**멀티스레드 로딩**: `DefaultModelLoader.DEFAULT_NUM_THREADS = 8`로 가중치 파일을 병렬 로딩하여 로드 시간을 단축한다.

**지원 로더 종류**:

| 로더 | 파일 | 용도 |
|------|------|------|
| `DefaultModelLoader` | `default_loader.py` | HuggingFace safetensors/pt (기본) |
| `ShardedStateLoader` | `sharded_state_loader.py` | 사전 샤딩된 체크포인트 |
| `GGUFModelLoader` | `gguf_loader.py` | GGUF 포맷 (llama.cpp 호환) |
| `BitsAndBytesModelLoader` | `bitsandbytes_loader.py` | BitsAndBytes 양자화 |
| `TensorizerLoader` | `tensorizer_loader.py` | CoreWeave Tensorizer |
| `RunaiModelStreamerLoader` | `runai_streamer_loader.py` | RunAI 스트리밍 로딩 |

### 4.6 양자화

`vllm/model_executor/layers/quantization/` 디렉토리에서 다양한 양자화 방식을 지원한다.

| 양자화 방식 | 파일 | 설명 |
|------------|------|------|
| **GPTQ** | `gptq.py`, `gptq_marlin.py` | Post-training quantization. Marlin 커널로 가속 |
| **AWQ** | `awq.py`, `awq_marlin.py`, `awq_triton.py` | Activation-aware Weight Quantization. Marlin/Triton 백엔드 |
| **FP8** | `fp8.py`, `fbgemm_fp8.py`, `input_quant_fp8.py` | FP8 (E4M3/E5M2) 양자화. CUDA 11.8+ 필요 |
| **BitsAndBytes** | `bitsandbytes.py` | INT8/INT4 NormalFloat 양자화 |
| **GGUF** | `gguf.py` | llama.cpp 호환 양자화 포맷 |
| **Compressed Tensors** | `compressed_tensors/` | Neural Magic의 압축 텐서 포맷 |
| **ModelOpt** | `modelopt.py` | NVIDIA TensorRT Model Optimizer |
| **MXFP4/MXFP8** | `mxfp4.py`, `mxfp8.py` | Microscaling 부동소수점 |
| **TorchAO** | `torchao.py` | PyTorch 네이티브 양자화 |
| **INC** | `inc.py` | Intel Neural Compressor |
| **Quark** | `quark/` | AMD Quark 양자화 |

각 양자화 구현은 `QuantizationConfig` 인터페이스(`base_config.py`)를 따르며, `get_quant_method()` → `QuantizeMethodBase`를 반환한다. 이 메서드가 Linear 레이어의 가중치 로딩과 forward 연산을 양자화 방식에 맞게 오버라이드한다.

### 4.7 분산 추론

#### Tensor Parallelism (TP)

모델의 각 레이어를 여러 GPU에 열(column) 또는 행(row) 단위로 분할한다.

- **구현**: `vllm/distributed/parallel_state.py`의 `get_tp_group()`, `tensor_model_parallel_all_reduce()`, `tensor_model_parallel_all_gather()`
- **레이어 분할**: `vllm/model_executor/layers/linear.py`의 `ColumnParallelLinear`, `RowParallelLinear`이 가중치를 TP 차원으로 자동 분할
- **TP 크기**: `ParallelConfig.tensor_parallel_size`로 설정

#### Pipeline Parallelism (PP)

모델의 레이어 그룹을 서로 다른 GPU에 배치하여 파이프라인으로 실행한다.

- **구현**: `get_pp_group()`으로 PP 그룹 관리. `EngineCore`의 `batch_queue`가 파이프라인 버블 제거를 위한 배치 큐 역할
- **PP 크기**: `ParallelConfig.pipeline_parallel_size`

#### Data Parallelism (DP)

동일 모델을 여러 GPU 그룹에 복제하여 요청을 분배한다.

- **구현**: `DPCoordinator` (`vllm/v1/engine/coordinator.py`)가 DP 랭크 간 요청 분배
- **DP 크기**: `ParallelConfig.data_parallel_size`

#### Expert Parallelism (EP)

MoE(Mixture-of-Experts) 모델에서 전문가(expert)를 여러 GPU에 분산 배치한다.

- **구현**: `vllm/distributed/elastic_ep/`에서 Elastic Expert Parallelism 지원
- **EPLB**: `vllm/distributed/eplb/`에서 Expert-Level Load Balancing으로 전문가 부하 균형

#### Context Parallelism (CP)

긴 시퀀스의 attention 연산을 여러 GPU에 분할한다.

- **설정**: `ParallelConfig.decode_context_parallel_size`, `prefill_context_parallel_size`

---

## 5. 설정 및 의존성 분석

### 5.1 핵심 의존성

`requirements/common.txt` 기준 주요 의존성:

| 패키지 | 버전 요구사항 | 용도 |
|--------|-------------|------|
| `torch` | == 2.10.0 | PyTorch 기반 모델 실행 |
| `transformers` | >= 4.56.0, < 5 | HuggingFace 모델/토크나이저 |
| `tokenizers` | >= 0.21.1 | 빠른 증분 디토큰화 |
| `fastapi[standard]` | >= 0.115.0 | API 서버 프레임워크 |
| `uvloop` | (fastapi 의존) | 고성능 asyncio 이벤트 루프 |
| `pyzmq` | >= 25.0.0 | 엔진 간 IPC 통신 |
| `msgspec` | (최신) | 고속 직렬화/역직렬화 |
| `numpy` | (최신) | 수치 연산 |
| `openai` | >= 2.0.0 | Responses API 지원 |
| `prometheus_client` | >= 0.18.0 | 메트릭 수집 |
| `xgrammar` | >= 0.1.32, < 1.0.0 | 구조화된 출력 (JSON/grammar) |
| `compressed-tensors` | == 0.14.0.1 | Neural Magic 양자화 |
| `gguf` | >= 0.17.0 | GGUF 포맷 지원 |
| `mcp` | (최신) | Model Context Protocol |
| `opentelemetry-*` | >= 1.27.0 | 분산 트레이싱 |

### 5.2 플랫폼별 요구사항

| 플랫폼 | 지원 | Docker | 비고 |
|--------|------|--------|------|
| **CUDA (NVIDIA)** | 주력 | `Dockerfile` | CUDA 11.8+ 필요. Flash Attention, FlashInfer 백엔드 |
| **ROCm (AMD)** | 지원 | `Dockerfile.rocm` | ROCm 6.x. AITER 기반 attention |
| **TPU (Google)** | 지원 | `Dockerfile.tpu` | Pallas 기반 attention |
| **XPU (Intel)** | 지원 | `Dockerfile.xpu` | Intel Extension for PyTorch |
| **CPU** | 제한적 지원 | `Dockerfile.cpu` | 추론만 가능, 성능 제한 |
| **PPC64LE** | 지원 | `Dockerfile.ppc64le` | IBM Power |
| **S390X** | 지원 | `Dockerfile.s390x` | IBM Z |

### 5.3 주요 설정 클래스

`vllm/config/` 디렉토리에 26개의 설정 모듈이 있으며, `VllmConfig`가 최상위 통합 설정이다.

| 설정 클래스 | 파일 | 주요 필드 |
|------------|------|----------|
| **VllmConfig** | `vllm.py` (77.7K) | 모든 설정의 루트. `model_config`, `cache_config`, `parallel_config`, `scheduler_config` 등 포함 |
| **ModelConfig** | `model.py` (83.7K) | `model`, `tokenizer`, `max_model_len`, `dtype`, `quantization`, `enforce_eager` |
| **CacheConfig** | `cache.py` (10.8K) | `block_size`(기본 16), `gpu_memory_utilization`(기본 0.9), `enable_prefix_caching`(기본 True), `cache_dtype` |
| **ParallelConfig** | `parallel.py` (33.9K) | `tensor_parallel_size`, `pipeline_parallel_size`, `data_parallel_size`, `worker_cls` |
| **SchedulerConfig** | `scheduler.py` (12.4K) | `max_num_seqs`, `max_num_batched_tokens`, `enable_chunked_prefill`, `policy` |
| **SpeculativeConfig** | `speculative.py` (36.9K) | `method`, `num_speculative_tokens`, `draft_model_config` |
| **CompilationConfig** | `compilation.py` (53.5K) | `level`(O0~O3), `cudagraph_mode`, `custom_ops` |
| **LoRAConfig** | `lora.py` (4.8K) | `max_lora_rank`, `max_loras`, `lora_extra_vocab_size` |
| **LoadConfig** | `load.py` (5.9K) | `load_format`(auto/safetensors/pt 등), `download_dir` |
| **KVTransferConfig** | `kv_transfer.py` (4.3K) | P/D disaggregation 설정 |

### 5.4 환경변수 기반 설정

`vllm/envs.py`에서 환경변수를 관리한다. 주요 변수:

| 환경변수 | 기본값 | 용도 |
|---------|--------|------|
| `VLLM_ENGINE_READY_TIMEOUT_S` | 600 | 엔진 시작 타임아웃 (초) |
| `VLLM_WORKER_MULTIPROC_METHOD` | fork | 워커 프로세스 생성 방식 |
| `CUDA_VISIBLE_DEVICES` | - | 사용할 GPU 지정 |

### 5.5 Docker 배포

`docker/` 디렉토리에 플랫폼별 Dockerfile이 준비되어 있다.

```bash
# CUDA 기본 이미지 빌드
docker build -f docker/Dockerfile -t vllm .

# ROCm 이미지
docker build -f docker/Dockerfile.rocm -t vllm-rocm .

# CPU 전용
docker build -f docker/Dockerfile.cpu -t vllm-cpu .
```

`docker/versions.json`에서 빌드 매트릭스(CUDA 버전, PyTorch 버전, Python 버전 조합)를 관리한다.

---

## 6. API 및 인터페이스

### 6.1 OpenAI 호환 API 엔드포인트

`vllm/entrypoints/openai/api_server.py`에서 FastAPI 기반 OpenAI 호환 서버를 구현한다.

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/v1/completions` | POST | 텍스트 완성 (Completion API) |
| `/v1/chat/completions` | POST | 채팅 완성 (Chat Completion API) |
| `/v1/embeddings` | POST | 임베딩 생성 |
| `/v1/models` | GET | 사용 가능 모델 목록 |
| `/v1/responses` | POST | Responses API (OpenAI 호환) |
| `/v1/audio/transcriptions` | POST | 음성 → 텍스트 변환 |
| `/health` | GET | 헬스 체크 |
| `/version` | GET | 버전 정보 |
| `/tokenize` | POST | 토큰화 |
| `/detokenize` | POST | 디토큰화 |

### 6.2 스트리밍 구현 (SSE)

```python
# vllm/entrypoints/openai/api_server.py 내부 — StreamingResponse 사용
# AsyncLLM.generate()가 AsyncGenerator로 토큰을 하나씩 yield
async for request_output in engine.generate(prompt, params, request_id):
    # 각 chunk를 SSE 형식으로 변환
    yield f"data: {chunk.model_dump_json()}\n\n"
yield "data: [DONE]\n\n"
```

스트리밍은 `RequestOutputKind`로 제어된다:
- `CUMULATIVE`: 누적 텍스트 반환 (기본)
- `DELTA`: 새 토큰만 반환 (SSE 스트리밍에 적합)
- `FINAL_ONLY`: 최종 결과만 반환

### 6.3 Python SDK (vllm.LLM)

`vllm/entrypoints/llm.py` (83.1K)에서 오프라인 배치 추론용 Python SDK를 제공한다.

```python
from vllm import LLM, SamplingParams

# 모델 로딩
llm = LLM(model="meta-llama/Llama-3-8B-Instruct",
          tensor_parallel_size=2,
          gpu_memory_utilization=0.9)

# 배치 추론
sampling_params = SamplingParams(temperature=0.7, max_tokens=256)
outputs = llm.generate(["Hello, world!", "What is AI?"], sampling_params)

# 채팅 API
messages = [{"role": "user", "content": "Hello!"}]
outputs = llm.chat(messages, sampling_params)
```

**SamplingParams** (`vllm/sampling_params.py`) 주요 필드:
- `temperature`, `top_p`, `top_k`: 샘플링 전략
- `max_tokens`: 최대 생성 토큰 수
- `stop`: 정지 문자열/토큰
- `frequency_penalty`, `presence_penalty`, `repetition_penalty`: 반복 제어
- `structured_outputs`: JSON Schema, regex, grammar 기반 구조화된 출력 강제
- `logprobs`, `prompt_logprobs`: 로그 확률 반환

### 6.4 MCP 서버

`vllm/entrypoints/mcp/` 디렉토리에서 Model Context Protocol 서버를 구현한다.

- `tool_server.py`: `ToolServer` 추상 클래스 + `MCPToolServer(ToolServer)` 구체 구현 + `DemoToolServer(ToolServer)` 데모용
- `tool.py`: `HarmonyBrowserTool`, `HarmonyPythonTool` 등 내장 도구 정의
- `openai_harmony` 패키지 기반으로 OpenAI의 도구 호출 포맷과 호환
- Coco에서 커스텀 MCP 도구를 추가하려면 `MCPToolServer`를 상속하여 구현

### 6.5 미들웨어 체인

API 서버에는 다음 미들웨어가 적용된다:

1. **CORS Middleware**: `CORSMiddleware` — 교차 출처 요청 허용 설정
2. **Scaling Middleware**: `ScalingMiddleware` — Elastic Expert Parallelism 스케일링
3. **Prometheus Instrumentator**: 요청 메트릭 자동 수집
4. **Request Logger**: 요청/응답 로깅

---

## 7. Coco/IntraGenX 통합 분석

### 7.1 IntraGenX 아키텍처에서의 역할

vLLM은 IntraGenX 아키텍처에서 **추론 엔진 백엔드**로 사용된다. 트랙 1(Spec-Driven 코드 생성)과 트랙 2(코딩 에이전트) 모두 vLLM을 통해 LLM 추론을 수행한다.

```
┌─────────────────────────────────────────────────────────────────┐
│                    IntraGenX 배포 토폴로지                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────┐   ┌────────────────┐   ┌────────────────┐  │
│  │  Coco Studio    │   │  Coco CLI      │   │  OpenCode      │  │
│  │  (웹 UI)        │   │  (터미널)       │   │  (트랙 2)       │  │
│  └───────┬────────┘   └───────┬────────┘   └───────┬────────┘  │
│          │                     │                     │           │
│          └─────────┬───────────┘                     │           │
│                    ▼                                 │           │
│          ┌─────────────────┐                         │           │
│          │  Coco Engine     │                         │           │
│          │  (코드 생성/리뷰) │                         │           │
│          └────────┬────────┘                         │           │
│                   │                                  │           │
│                   ▼                                  ▼           │
│          ┌─────────────────────────────────────────────┐        │
│          │          LiteLLM Proxy (AI Gateway)          │        │
│          │  - 라우팅/로드밸런싱                            │        │
│          │  - API 키 인증                                │        │
│          │  - 비용 추적                                   │        │
│          └───────┬────────────────┬────────────────────┘        │
│                  │                │                              │
│          ┌───────▼──────┐ ┌──────▼───────┐                     │
│          │  vLLM #1      │ │  vLLM #2      │                     │
│          │  (Qwen 32B)   │ │  (4B LoRA)    │                     │
│          │  GPU 0-1      │ │  GPU 2        │                     │
│          └──────────────┘ └──────────────┘                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 통합 포인트

| 통합 영역 | 상세 | vLLM 관련 코드/설정 |
|----------|------|-------------------|
| **OpenAI 호환 API** | Coco Engine이 `POST /v1/chat/completions`로 통신. `openai` Python 클라이언트 사용 | `vllm/entrypoints/openai/api_server.py` |
| **토큰 스트리밍** | SSE 기반 `stream=True`. Coco Engine의 `/agent/agentic/v2/stream`이 vLLM 스트리밍 중계 | `RequestOutputKind.DELTA` 모드 |
| **모델 로딩** | HuggingFace 또는 로컬 경로. 4B 파인튜닝 모델(LoRA) 서빙 가능 | `--model`, `--enable-lora` |
| **다중 모델** | LiteLLM Proxy 경유로 여러 vLLM 인스턴스 라우팅 | `06_vllm_rd_plan_ko.md` 참조 |
| **구조화된 출력** | JSON Schema로 코드 생성 출력 형식 강제 (CGF 파이프라인 후처리 감소) | `structured_outputs` 파라미터 |
| **감사 추적** | OpenTelemetry 트레이싱으로 요청별 추적. Coco Admin 대시보드 연동 가능 | `vllm/tracing/`, `--otlp-traces-endpoint` |

**실제 Coco Engine → vLLM 호출 패턴**:

```python
# Coco Engine 내부 — vLLM 호출 예시 (openai 클라이언트 사용)
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:3000/v1",  # LiteLLM Proxy 경유
    api_key="sk-coco-internal"             # LiteLLM API 키
)

response = client.chat.completions.create(
    model="qwen-32b",                      # LiteLLM이 vLLM으로 라우팅
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": uasl_spec}
    ],
    stream=True,
    temperature=0.1,                       # 코드 생성은 낮은 temperature
    extra_body={
        "structured_outputs": {            # JSON Schema 강제
            "type": "json_schema",
            "json_schema": code_output_schema
        }
    }
)
```

### 7.3 커스터마이징 영역

| 영역 | 구현 방안 | 관련 vLLM 코드 | 난이도 |
|------|----------|---------------|--------|
| **인증 미들웨어** | FastAPI 미들웨어로 API 키/JWT 인증 추가 | `api_server.py` lifespan 함수 | 낮음 |
| **모델 암호화** | 커스텀 ModelLoader — 암호화된 가중치를 메모리에서 복호화 후 로딩 | `model_loader/base_loader.py` 상속 | 높음 |
| **모니터링** | Prometheus 메트릭 + OpenTelemetry 트레이싱 | `vllm/v1/metrics/`, `vllm/tracing/` | 낮음 |
| **LoRA 어댑터** | 런타임에 LoRA 교체 — 프로젝트/프레임워크별 코드 스타일 | `vllm/lora/` | 중간 |
| **구조화된 출력** | JSON Schema 기반 코드 생성 출력 강제 | `vllm/v1/structured_output/` | 낮음 |
| **커스텀 MCP 도구** | MCPToolServer 상속으로 Coco 전용 도구 추가 | `vllm/entrypoints/mcp/tool_server.py` | 중간 |

### 7.4 온프레미스/폐쇄망 배포 고려사항

| 항목 | 설정 | 비고 |
|------|------|------|
| **오프라인 모델** | `--model /local/path/to/model` | HuggingFace Hub 접근 불필요 |
| **Docker 배포** | `docker/Dockerfile` 기반 이미지 빌드 | pip 패키지 사전 포함 필요 |
| **GPU 메모리** | `--gpu-memory-utilization 0.9` | 동일 GPU 다중 인스턴스 시 조정 |
| **TLS/SSL** | `--ssl-keyfile`, `--ssl-certfile` | `vllm/entrypoints/ssl.py` |
| **인증** | 리버스 프록시(Nginx) 또는 커스텀 미들웨어 | vLLM 자체 인증은 제한적 |
| **로그 격리** | `--disable-log-requests` + 내부 로깅 | 민감 정보 유출 방지 |
| **방화벽** | vLLM 포트(8000)를 LiteLLM만 접근 허용 | Coco Engine → LiteLLM → vLLM 체인 |

**권장 배포 명령어** (온프레미스):

```bash
# vLLM 서버 시작 (GPU 2장, TP=2, 4B 파인튜닝 모델)
vllm serve /models/coco-qwen-4b-lora \
  --tensor-parallel-size 2 \
  --gpu-memory-utilization 0.9 \
  --enable-lora \
  --lora-modules coco-xframe5=/lora/xframe5 coco-vue3=/lora/vue3 \
  --max-model-len 32768 \
  --ssl-keyfile /certs/server.key \
  --ssl-certfile /certs/server.crt \
  --host 0.0.0.0 --port 8000
```

### 7.5 기존 분석과의 차별점

이 문서와 `06_vllm_rd_plan_ko.md`의 역할 분담:

| 항목 | 이 문서 (01_vllm_analysis) | 06_vllm_rd_plan_ko |
|------|--------------------------|-------------------|
| **목적** | vLLM 코드베이스 자체의 이해 | Coco와의 통합 R&D 계획 |
| **관점** | 오픈소스 분석 (내부 구조) | 프로젝트 실행 계획 (일정/인력) |
| **깊이** | 코드 레벨 메커니즘 | 아키텍처 설계 + 구현 로드맵 |
| **갱신 주기** | vLLM 버전 업데이트 시 | 프로젝트 마일스톤별 |

### 7.6 교차 참조

- vLLM 인프라 고도화 R&D 계획: [`02_implementation/06_vllm_rd_plan_ko.md`](../../02_implementation/06_vllm_rd_plan_ko.md)
  - 모델 암호화, LiteLLM 연동, 인증/인가 미들웨어, 모니터링 고도화 등 구체적 계획 포함
- LiteLLM 심층 분석: [`02_litellm_analysis.md`](./02_litellm_analysis.md) — vLLM 프록시 계층 이해에 필수
- OpenCode 심층 분석: [`03_opencode_analysis.md`](./03_opencode_analysis.md) — vLLM을 최종 추론 엔진으로 사용하는 트랙 2 에이전트
- 프로젝트 용어집: [`05_knowledge_base/glossary_ko.md`](../../05_knowledge_base/glossary_ko.md) — vLLM, PagedAttention, KV Cache 등 용어 정의

---

## 8. 참고자료 및 추가 탐색 가이드

### 8.1 공식 리소스

| 리소스 | URL |
|--------|-----|
| 공식 문서 | https://docs.vllm.ai/en/latest/ |
| GitHub 저장소 | https://github.com/vllm-project/vllm |
| Discord 커뮤니티 | https://discord.gg/vllm |
| Slack | https://slack.vllm.ai/ |
| PyPI | https://pypi.org/project/vllm/ |

### 8.2 추천 코드 읽기 순서

vLLM 코드베이스를 처음 파악하려면 다음 순서를 권장한다:

1. **진입점 이해**: `vllm/entrypoints/llm.py`의 `LLM` 클래스 — `generate()` 메서드부터 읽으면 전체 흐름 파악 가능
2. **엔진 구조**: `vllm/v1/engine/async_llm.py` → `core_client.py` → `core.py` — 프론트엔드→백엔드 통신 구조
3. **스케줄러**: `vllm/v1/core/sched/scheduler.py`의 `schedule()` 메서드 — Continuous Batching의 핵심
4. **KV Cache**: `vllm/v1/core/kv_cache_manager.py` → `block_pool.py` — PagedAttention의 블록 할당 로직
5. **모델 실행**: `vllm/v1/worker/gpu_model_runner.py`의 `execute_model()` — GPU에서 실제 모델이 실행되는 부분
6. **모델 구현**: `vllm/model_executor/models/` 중 하나 (예: `llama.py`) — vLLM 모델 구현 패턴 학습
7. **설정**: `vllm/config/vllm.py`의 `VllmConfig` — 전체 설정 구조 파악
8. **OpenAI API**: `vllm/entrypoints/openai/api_server.py` — API 서버 라우팅과 미들웨어

### 8.3 핵심 논문 및 RFC

| 자료 | 설명 |
|------|------|
| **PagedAttention 논문** | Kwon et al., "Efficient Memory Management for Large Language Model Serving with PagedAttention" (SOSP 2023) |
| **vLLM V1 엔진 RFC** | GitHub Discussion — V1 엔진 재설계 동기와 아키텍처 결정 |
| **EAGLE 논문** | Li et al., "EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty" (ICML 2024) |
| **Continuous Batching** | Yu et al., "Orca: A Distributed Serving System for Transformer-Based Generative Models" (OSDI 2022) |
| **Medusa 논문** | Cai et al., "Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads" (ICML 2024) |

### 8.4 주요 디렉토리 크기 순위 (참고)

| 디렉토리/파일 | 크기 | 비고 |
|-------------|------|------|
| `vllm/v1/worker/gpu_model_runner.py` | 291.2K | 단일 최대 파일. GPU 모델 실행 전체 로직 |
| `vllm/config/model.py` | 83.7K | ModelConfig — 모델 설정의 복잡성 반영 |
| `vllm/entrypoints/llm.py` | 83.1K | Python SDK |
| `vllm/v1/engine/core.py` | 80.9K | EngineCore — 엔진 백엔드 |
| `vllm/config/vllm.py` | 77.7K | VllmConfig — 최상위 설정 |
| `vllm/v1/spec_decode/eagle.py` | 75.9K | EAGLE Speculative Decoding |
| `vllm/distributed/parallel_state.py` | 74.7K | 분산 상태 관리 |
| `vllm/v1/core/kv_cache_utils.py` | 65.0K | KV Cache 유틸리티 |
| `vllm/v1/engine/core_client.py` | 65.5K | 엔진 통신 클라이언트 |

---

## 변경이력

| 버전 | 일자 | 변경 내용 | 작성자 |
|------|------|----------|--------|
| 1.0 | 2026-03-23 | 초안 작성 — vLLM v0.18.x 심층 분석 | 분석팀 |
