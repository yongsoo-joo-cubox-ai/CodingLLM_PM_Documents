# Phase 2 기술 스택 및 스터디 로드맵

**작성일**: 2026-01-28 | **대상**: 시선AI R&D팀 | **기간**: 4-6월 (3.6 FTE)

> **구현 문서 4/5** | 이전: [비용 분석](./cost_analysis_ko.md) | 다음: [API 레퍼런스](./api_reference_ko.md) | [폴더 인덱스](./README.md)

---

## 1. 개요

Phase 2(4-6월) 개발 항목에 대한 **기술 스택, 학습 자료, 구현 가이드**를 정리한 문서입니다.

### 현재 기술 스택
| 구성요소 | 버전/사양 |
|---------|----------|
| LLM 추론 | vLLM >= 0.6.0 |
| 백엔드 | Rust + Loco.rs |
| 모델 | GPT-OSS 20B (94%), Qwen2.5-32B-AWQ (54%) |
| GPU | 4x RTX 2080 Ti (44GB 합계) |

---

## 2. 영역별 기술 스택 및 스터디 가이드

### A. 모델/ML 영역

#### A1. 모델 품질 개선 (Qwen32B 54% → 80%+) `P0`

| 항목             | 권장 스택                                                     | 비고                       |
| -------------- | --------------------------------------------------------- | ------------------------ |
| **파인튜닝 프레임워크** | [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) | Qwen2.5 공식 지원, QLoRA 최적화 |
| **학습 방법**      | QLoRA (r=64, alpha=128)                                   | 메모리 효율적                  |
| **데이터셋 규모**    | 1,200-2,500 예제                                            | 연구 최적점                   |
| **정밀도**        | torch.float16                                             | Qwen 권장                  |
| **LoRA 타겟**    | Attention + MLP blocks                                    | 코드 생성 최적                 |

**학습 자료**:
- [Qwen2.5-Coder Fine-tuning (Kaitchup)](https://kaitchup.substack.com/p/qwen25-qlora-lora-and-full-fine-tuning) - QLoRA vs LoRA 비교
- [LLaMA-Factory Qwen 가이드](https://qwen.readthedocs.io/en/latest/training/llama_factory.html) - 공식 문서
- [QLoRA 논문](https://arxiv.org/abs/2305.14314) - 이론적 배경

**데이터 준비**:
```json
// LLaMA-Factory alpaca 포맷
{
  "instruction": "회원 목록 화면을 생성해주세요",
  "input": "필드: 이름, 이메일, 등록일",
  "output": "<!-- xFrame5 XML -->\n<Screen id=\"memberList\">..."
}
```

**필요 리소스**: A100 80GB 1대 (QLoRA 학습용)

---

#### A2. 경량 모델 최적화 (7B QA 전용 85%+) `P1`

| 항목 | 권장 스택 | 비고 |
|------|----------|------|
| **베이스 모델** | Qwen2.5-Coder-7B-Instruct | 현재 42% 기준선 |
| **학습 방법** | Task-specific LoRA (r=16-32) | QA 범위 좁음 |
| **추론 엔진** | Ollama | QA용 이미 검증 |
| **데이터** | xFrame5 Q&A 페어 | knowledge_base에서 추출 |

**학습 자료**:
- [HuggingFace Qwen2.5-Coder-7B](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct)
- [Efficient Fine-tuning for Small LLMs](https://medium.com/@raquelhvaz/efficient-llm-fine-tuning-with-lora-e5edb88b64a1)

---

#### A3. 멀티 모델 라우팅 `P1`

| 항목 | 권장 스택 | 비고 |
|------|----------|------|
| **라우팅 전략** | Rule-based + Health fallback | 예측 가능, 디버깅 용이 |
| **참조 구현** | [vLLM Semantic Router "Iris"](https://blog.vllm.ai/2026/01/05/vllm-sr-iris.html) | 2026.01 릴리즈 |
| **캐시 인식 라우팅** | [llm-d](https://developers.redhat.com/articles/2026/01/13/accelerate-multi-turn-workloads-llm-d) | 87% 캐시 히트율 |

**학습 자료**:
- [AWS Multi-LLM Routing Strategies](https://aws.amazon.com/blogs/machine-learning/multi-llm-routing-strategies-for-generative-ai-applications-on-aws/) - 30% 비용 절감 전략
- [OpenRouter Architecture](https://medium.com/@milesk_33/a-practical-guide-to-openrouter-unified-llm-apis-model-routing-and-real-world-use-d3c4c07ed170) - 통합 API 게이트웨이

**라우팅 로직 예시**:
```rust
match task_type {
    TaskType::Generation => route_to_large_model(),  // Qwen32B/GPT-OSS
    TaskType::QA => route_to_small_model(),          // Qwen7B
    TaskType::Review => route_to_medium_model(),     // Qwen32B
}
```

---

#### A4. Template 통합 `P1`

| 항목 | 권장 스택 | 비고 |
|------|----------|------|
| **템플릿 엔진** | Jinja2 또는 Handlebars | 모델 무관 |
| **구조** | 모듈식 + 조건부 섹션 | 모델 능력별 적응 |
| **저장** | YAML 설정 파일 | MCP 패턴 |

**현황**: v3 (430줄, GPT-OSS) vs v4 (80줄, Qwen) → **통합 필요**

---

### B. 인프라/배포 영역

#### B1. 동시 사용자 최적화 (65초 → 40초) `P1`

| 최적화 기법 | 도구/설정 | 예상 개선 |
|------------|----------|----------|
| **Prefix Caching** | `--enable-prefix-caching` | 20-30% (반복 패턴) |
| **FP8 KV Cache** | `--kv-cache-dtype fp8` | 15-20% 용량 증가 |
| **CPU Offloading** | [LMCache](https://blog.vllm.ai/production-stack/tutorials/05-offload-kv-cache.html) | 3-10x 지연 감소 |
| **캐시 인식 라우팅** | llm-d | 87% 캐시 히트 |

**학습 자료**:
- [vLLM Optimization Guide](https://docs.vllm.ai/en/latest/configuration/optimization/) - 공식 최적화 문서
- [KV Cache Optimization (Introl)](https://introl.com/blog/kv-cache-optimization-memory-efficiency-production-llms-guide) - 메모리 효율화
- [Quantized KV Cache (vLLM)](https://docs.vllm.ai/en/latest/features/quantization/quantized_kvcache/) - FP8 양자화

**vLLM 최적화 실행 명령**:
```bash
python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-Coder-32B-Instruct-AWQ \
  --enable-prefix-caching \
  --kv-cache-dtype fp8 \
  --max-model-len 12288 \
  --gpu-memory-utilization 0.90
```

---

#### B2. 모니터링 시스템 `P1`

| 구성요소 | 권장 스택 | 비고 |
|---------|----------|------|
| **메트릭 수집** | Prometheus | vLLM 네이티브 `/metrics` |
| **시각화** | Grafana | 대시보드, 알림 |
| **분산 추적** | OpenTelemetry + Jaeger | E2E 요청 추적 |
| **로그** | Loki | Grafana 통합 |

**핵심 메트릭**:
| 카테고리 | 메트릭 |
|---------|--------|
| 지연 | TTFT, 총 응답 시간, p50/p95/p99 |
| 처리량 | Tokens/sec, Requests/sec |
| GPU | 사용률 %, 메모리 사용량, 온도 |
| 비즈니스 | 생성 횟수/시간, 품질 점수 |

**학습 자료**:
- [vLLM Prometheus Metrics](https://docs.vllm.ai/en/latest/design/metrics.html) - 공식 메트릭 문서
- [LLM Observability with Grafana](https://grafana.com/blog/2024/07/18/a-complete-guide-to-llm-observability-with-opentelemetry-and-grafana-cloud/) - 종합 가이드
- [Building Production-Ready Observability for vLLM (IBM)](https://medium.com/@ibm-data-ai/building-production-ready-observability-for-vllm-a2f4924d3949) - 실전 가이드

**Prometheus 설정**:
```yaml
scrape_configs:
  - job_name: 'vllm'
    static_configs:
      - targets: ['172.16.100.116:8000']
    metrics_path: /metrics
    scrape_interval: 15s
```

---

#### B3. 고가용성 구성 `P2 (Phase 3)`

| 구성요소 | 권장 스택 |
|---------|----------|
| 로드밸런서 | HAProxy / NGINX |
| 서비스 디스커버리 | Consul / K8s Services |
| 멀티 인스턴스 | vLLM Data Parallel |

**Phase 2 준비사항**: 아키텍처 설계 문서 작성

---

### C. 백엔드/API 영역

#### C1. 프레임워크 분리 (MCP 기반) `P0`

| 항목 | 권장 스택 | 비고 |
|------|----------|------|
| **MCP SDK** | [rmcp crate v0.8.0](https://github.com/modelcontextprotocol/rust-sdk) | 공식 Rust SDK |
| **전송 방식** | stdio 기반 | MCP 표준 |
| **프리미티브** | tools, resources, prompts | 3대 빌딩 블록 |
| **구현** | `#[tool]` 매크로 | Rust 절차적 매크로 |

**학습 자료**:
- [MCP 공식 스펙](https://modelcontextprotocol.io/specification/2025-11-25) - 프로토콜 명세
- [Anthropic MCP 소개](https://www.anthropic.com/news/model-context-protocol) - 개념 이해
- [Rust MCP Server 튜토리얼 (OneUptime)](https://oneuptime.com/blog/post/2026-01-07-rust-mcp-server/view) - 실전 가이드
- [rmcp 실습 가이드 (HackMD)](https://hackmd.io/@Hamze/SytKkZP01l) - 핸즈온

**MCP 서버 구조 (xFrame5)**:
```rust
use rmcp::{tool, ServerBuilder};

#[tool(description = "xFrame5 XML 화면 생성")]
async fn generate_xml(prompt: String, template: String) -> String {
    // xFrame5 특화 XML 생성 로직
}

#[tool(description = "API 허용목록 검증")]
async fn validate_api(code: String, allowlist: Vec<String>) -> ValidationResult {
    // xFrame5 API 검증 로직
}
```

**아키텍처** (from `architecture_mcp.md`):
```
Coder Core (Orchestration)
  ├─ Output parsing
  ├─ Symbol linking
  └─ Graph validation
        ↓
MCP Servers (Framework-Specific)
  ├─ xFrame5 Server (Phase 2)
  ├─ Spring Server (Phase 3)
  └─ Vue/React Server (Phase 3)
```

---

#### C2. API 고도화 (배치, 비동기) `P1`

| 항목 | 권장 스택 | 비고 |
|------|----------|------|
| **배치 엔드포인트** | `POST /agent/batch` | 다중 요청 |
| **작업 큐** | Redis 또는 PostgreSQL | 상태 추적 |
| **비동기 패턴** | Submit → Poll → Result | 논블로킹 |

**학습 자료**:
- [Loco.rs Workers](https://loco.rs/docs/the-app/workers/) - Rust 백그라운드 작업
- OpenAI Batch API 참조 설계

---

#### C3. 멀티 프레임워크 (Spring, Vue, React) `P2 (Phase 3)`

**Phase 2 준비사항**:
- FrameworkAdapter 트레이트 인터페이스 설계
- 프레임워크별 요구사항 문서화
- 지식 베이스 소스 식별

---

### D. 품질/테스트 영역

#### D1. 모델 품질 벤치마크 자동화 `P0`

| 항목 | 권장 스택 | 비고 |
|------|----------|------|
| **프레임워크** | [DeepEval](https://github.com/confident-ai/deepeval) | "pytest for LLMs" |
| **메트릭** | Correctness, Relevance, Coherence | 표준 LLM 평가 |
| **커스텀 메트릭** | xFrame5 품질 점수 | 기존 벤치마크 기준 |
| **CI 통합** | GitHub Actions | 모델 변경 시 자동 |

**학습 자료**:
- [DeepEval 문서](https://docs.confident-ai.com/) - 공식 가이드
- [LLM Evaluation Landscape 2026](https://research.aimultiple.com/llm-eval-tools/) - 도구 비교
- [Confident AI Blog](https://www.confident-ai.com/blog/llm-testing-in-2024-top-methods-and-strategies) - 테스트 전략

**커스텀 메트릭 예시**:
```python
from deepeval.metrics import BaseMetric

class XFrame5QualityMetric(BaseMetric):
    def measure(self, test_case):
        xml_score = self.score_xml_structure(test_case.actual_output)
        js_score = self.score_js_functions(test_case.actual_output)
        api_score = self.score_api_correctness(test_case.actual_output)
        return (xml_score + js_score + api_score) / 3
```

---

#### D2. 부하 테스트 자동화 `P1`

| 항목 | 권장 스택 | 비고 |
|------|----------|------|
| **프레임워크** | [LLM Locust](https://www.truefoundry.com/blog/llm-locust-a-tool-for-benchmarking-llm-performance) | 토큰 레벨 정밀도 |
| **대안** | [NVIDIA GenAI-Perf](https://docs.nvidia.com/nim/large-language-models/1.0.0/benchmarking.html) | GPU 메트릭 |
| **메트릭** | TTFT, throughput, p50/p95/p99 | 표준 지연 |

**학습 자료**:
- [Locust 공식 문서](https://locust.io/)
- [k6 vs Locust 비교](https://medium.com/@sohail_saifi/load-testing-your-api-k6-vs-artillery-vs-locust-66a8d7f575bd)
- [AWS Locust for SageMaker](https://garystafford.medium.com/finding-your-llms-breaking-point-load-testing-sagemaker-real-time-inference-endpoints-with-locust-5b60cd1dfbf5)

**주의**: Locust Python GIL 제한 - CPU 집약 토큰화 시 병목

---

#### D3. E2E 테스트 `P1`

| 항목 | 권장 스택 | 비고 |
|------|----------|------|
| **프레임워크** | DeepEval + Pytest | 통합 LLM+API 테스트 |
| **대안** | [GenIA-E2ETest](https://arxiv.org/html/2510.01024v1) | 77% 요소, 82% 정밀도 |
| **접근법** | Multi-agent 테스트 생성 | 자동 테스트 케이스 |

**학습 자료**:
- [Checksum Multi-Agent Testing](https://checksum.ai/blog/the-engineering-of-an-llm-agent-system) - 다중 에이전트 시스템

---

## 3. 월별 스터디 및 개발 일정

### 4월: 아키텍처 & 인프라

| 주차 | Backend | ML | MLOps | QA |
|-----|---------|-----|-------|-----|
| W1 | rmcp SDK 학습 | LLaMA-Factory 환경 구성 | Prometheus 설정 | DeepEval 학습 |
| W2 | FrameworkAdapter 설계 | 학습 데이터 준비 | Grafana 대시보드 | 벤치마크 자동화 설계 |
| W3 | xFrame5 MCP 서버 시작 | Qwen32B 파인튜닝 시작 | vLLM 메트릭 통합 | 부하 테스트 설계 |
| W4 | MCP 서버 계속 | 모델 평가 | 알림 설정 | Locust 셋업 |

### 5월: 모델 & 테스트

| 주차 | Backend | ML | MLOps | QA |
|-----|---------|-----|-------|-----|
| W5 | MCP 통합 테스트 | 7B QA 모델 학습 | KV 캐시 분석 | 품질 메트릭 구현 |
| W6 | 배치 API 엔드포인트 | 모델 라우팅 구현 | Prefix Caching 설정 | E2E 테스트 프레임워크 |
| W7 | 비동기 작업 처리 | 템플릿 통합 | FP8 KV 캐시 테스트 | 파이프라인 테스트 |
| W8 | MCP 서버 완료 | A/B 테스트 설정 | 성능 베이스라인 | 통합 테스트 |

### 6월: 통합 & 최적화

| 주차 | Backend | ML | MLOps | QA |
|-----|---------|-----|-------|-----|
| W9 | 통합 테스트 | 모델 품질 검증 | 캐시 최적화 | 전체 회귀 |
| W10 | 버그 수정 | 최종 모델 선정 | 부하 테스트 | 품질 리포트 |
| W11 | 문서화 | 모델 배포 | HA 계획 | CI 자동화 |
| W12 | Phase 2 종료 | 지식 이전 | 운영 설정 | 최종 검증 |

---

## 4. 우선순위 매트릭스

| 항목 | 우선순위 | 복잡도 | 의존성 | 담당 |
|-----|---------|--------|--------|-----|
| C1. 프레임워크 분리 (MCP) | **P0** | 높음 | 없음 | Backend |
| A1. 모델 품질 개선 | **P0** | 높음 | 학습 데이터 | ML |
| D1. 벤치마크 자동화 | **P0** | 중간 | A1 완료 | QA |
| B1. 동시 사용자 최적화 | P1 | 높음 | B2 측정 | MLOps |
| B2. 모니터링 시스템 | P1 | 중간 | 없음 | MLOps |
| A2. 경량 모델 QA | P1 | 중간 | KB | ML |
| A3. 멀티 모델 라우팅 | P1 | 중간 | C1 진행 | Backend+ML |
| D2. 부하 테스트 자동화 | P1 | 중간 | B2 완료 | QA |
| D3. E2E 테스트 | P1 | 중-높 | C1, C2 | QA |

---

## 5. 핵심 참조 파일

| 파일 | 용도 |
|-----|------|
| `03_development/2026-01-24_progress/architecture_mcp.md` | MCP 아키텍처 설계 (C1) |
| `03_development/2026-01-15_project_intro/model_benchmark.md` | 품질 기준선 (A1, D1) |
| `03_development/2026-01-15_project_intro/load_test_qwen32b.md` | 성능 기준선 (B1, D2) |
| `03_development/2026-01-24_progress/vram_sizing.md` | VRAM 계획 (B1) |
| `02_implementation/api_reference_ko.md` | API 명세 (C2, D3) |

---

## 6. 검증 방법

### 모델 품질 검증
```bash
# DeepEval 벤치마크 실행
deepeval test run tests/xframe5_benchmark.py --model qwen32b-finetuned
# 목표: 80%+ 품질 점수
```

### 성능 검증
```bash
# Locust 부하 테스트
locust -f tests/load_test.py --users 10 --spawn-rate 2
# 목표: p50 < 40초
```

### E2E 검증
```bash
# 전체 파이프라인 테스트
pytest tests/e2e/ -v --tb=short
# 목표: 95%+ 통과율
```

---

## 7. 리스크 및 대응

| 리스크 | 확률 | 대응 |
|--------|------|------|
| Qwen32B 80% 미달 | 30% | GPT-OSS 20B 폴백 유지 |
| MCP 통합 복잡도 | 25% | 최소 기능 MCP 서버로 시작 |
| KV 캐시 35% 미만 개선 | 20% | 점진적 개선 수용, HA로 보완 |

---

**작성**: Claude Code 분석 | **검토 필요**: 시선AI R&D팀
