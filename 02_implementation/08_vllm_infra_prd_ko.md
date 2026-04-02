# vLLM 인프라 고도화 PRD (Product Requirements Document)

| 항목 | 내용 |
|------|------|
| **문서번호** | SAI-IMPL-2026-008 |
| **작성일** | 2026년 3월 30일 |
| **버전** | v0.6 |
| **개정일** | 2026년 4월 2일 |
| **보안등급** | 대외비 |
| **작성** | Secern AI |

> **참고 문서** | 이전: [SecernCode 현황 보고서](./07_secerncode_status_ko.md) | 다음: [vLLM 인프라 로드맵](./09_vllm_infra_roadmap_ko.md) | [폴더 인덱스](./README.md)

---

## RALPLAN-DR (Decision Record)

### Principles

1. **에어갭 우선 (Air-Gap First)**: 모든 기능은 외부 네트워크 연결 없이 폐쇄망 환경에서 완전히 동작해야 한다. 클라우드 의존성은 0건을 유지한다.
2. **vLLM 코어 비수정 (Upstream Compatibility)**: vLLM 엔진의 핵심 코드를 직접 수정하지 않고, 공식 확장 포인트(--middleware, register_model_loader, --load-format)만 활용하여 업스트림 업데이트와의 호환성을 보장한다.
3. **투트랙 통합 (Dual-Track Convergence)**: Track 1(IntraGenX/Coco Engine)과 Track 2(SecernCode)가 동일한 vLLM 인프라를 공유하며, 양쪽 모두에 대한 통합 포인트를 명시한다.
4. **점진적 배포 (Incremental Delivery)**: 세 가지 항목을 독립적으로 개발하고 순차 배포하되, 각 단계가 독자적인 가치를 제공할 수 있도록 한다.
5. **금융권 보안 기준 충족 (Financial-Grade Security)**: 금융권 재진입 시 필수 요건인 모델 IP 보호, 감사 추적, 인증/인가를 모두 충족하는 수준으로 설계한다.

### Decision Drivers (상위 3개)

1. **고객사 모델 IP 보호 시급성**: 파인튜닝된 sLLM을 고객사에 배포할 때, 디스크 평문 저장으로 인한 유출 위험이 즉각적인 비즈니스 리스크. 금융권 재진입의 선결 조건.
2. **SecernCode Stage 1 연계**: Stage 1(2026 Q2)에서 eGovFrame RAG + Qwen3-Coder 통합이 진행되므로, 멀티 모델 라우팅이 동기적으로 준비되어야 모델 연구 효율이 극대화됨.
3. **팀 규모 제약**: PM/인프라(주용수) + 프로토타입/모델 연구(황영준M) 2인 체제이므로, 각 항목의 구현 복잡도를 현실적으로 통제해야 함.

### Viable Options

#### Option A: vLLM 네이티브 확장 + LiteLLM 프록시 (권장)

vLLM의 공식 확장 포인트(Tensorizer, --middleware, register_model_loader)와 LiteLLM 프록시를 조합하여 구축.

| Pros | Cons |
|------|------|
| vLLM 업스트림 호환성 유지, 버전 업그레이드 시 영향 최소화 | LiteLLM 자체의 학습 비용 및 운영 복잡도 추가 |
| Tensorizer의 libsodium 암호화가 검증된 성숙 기술 | Tensorizer 포맷 변환 파이프라인 초기 구축 필요 |
| LiteLLM이 100+ 프로바이더 지원, SecernCode의 Intelligent Routing과 자연스럽게 연계 | 에어갭 환경에서 LiteLLM 의존성 패키지 오프라인 설치 필요 |
| 커뮤니티 활성도 높아 장기 유지보수 유리 | |

#### Option B: 완전 자체 구현 (프록시 + 암호화 + 인증)

LiteLLM/Tensorizer 없이 자체 FastAPI 게이트웨이와 커스텀 암호화 로더를 처음부터 구현.

| Pros | Cons |
|------|------|
| 외부 의존성 최소화, 완전한 제어권 | 2인 팀으로 개발/유지보수 부담 과중 (예상 공수 3~4배) |
| 국정원 인증 암호 모듈 등 특수 요건 직접 대응 가능 | 검증되지 않은 자체 암호화 구현의 보안 취약점 리스크 |
| | LiteLLM이 제공하는 로드밸런싱/폴백/대시보드를 모두 재구현해야 함 |

#### Option C: Nginx 리버스 프록시 + SecernCode Model Router (기각)

Nginx를 리버스 프록시로, SecernCode의 Model Router를 라우팅 계층으로 활용하여 LiteLLM 없이 구축.

| 비교 기준 | Nginx + SecernCode Router | LiteLLM (Option A) |
|----------|--------------------------|-------------------|
| 로드밸런싱 | O (Nginx upstream) | O (내장) |
| 자동 폴백 | 수동 설정 (health_check + fallback) | 자동 (model fallback 내장) |
| 프로토콜 변환 (Anthropic→OpenAI) | X (직접 구현 필요) | O (내장, 100+ 프로바이더) |
| 가상 키 / 사용량 추적 | X (직접 구현 필요) | O (거버넌스 패키지 내장) |
| 모델 A/B 테스트 | 수동 (split_clients) | 내장 (config.yaml 트래픽 비율) |

**기각 근거**: 가상 키/사용량 추적과 모델 A/B 테스트는 이 프로젝트의 핵심 거버넌스 요건(LIT-08, LIT-09)이며, Nginx로는 이를 충족하기 위해 상당한 추가 개발이 필요하다. 2인 팀 제약 조건에서 LiteLLM이 기본 제공하는 기능을 재구현하는 것은 비현실적이다.

### 선택 근거

**Option A (vLLM 네이티브 확장 + LiteLLM 프록시)를 권장한다.**

- 2인 팀 제약 조건에서 검증된 오픈소스 컴포넌트를 조합하는 것이 현실적이며, 각 컴포넌트의 커뮤니티 지원을 활용할 수 있다.
- Option B는 금융권 특수 요건(국정원 인증 암호 모듈/HSM 연동) 발생 시 Phase 2 이후에 커스텀 모델 로더(register_model_loader)로 점진 확장하는 방식으로 대응 가능하다. 즉, Option A를 기반으로 하되 필요 시 Option B의 일부를 선택적으로 추가하는 하이브리드 전략이 최적이다.
- Tensorizer의 libsodium 암호화는 업계에서 충분히 검증되었으며, 에어갭 환경에서도 오프라인 설치가 가능하다.

---

## 1. 개요

### 1.1 배경

Secern AI의 Coco / IntraGenX 플랫폼은 폐쇄망 온프레미스 환경에서 vLLM 기반 sLLM을 운용하여 AI 코드 거버넌스 서비스를 제공한다. Phase 1이 완료되어 6개 MCP 서버, Coco Studio, UASL v3, 멀티 모델 라우팅이 운영 중이며, Track 2(SecernCode)도 Stage 0 MVP를 완성했다.

그러나 현재 vLLM 인프라에는 세 가지 핵심 결함이 존재한다:

1. **모델 가중치가 디스크에 평문 저장**: 파인튜닝된 sLLM(Qwen2.5-Coder-32B-AWQ, Qwen3-Coder 등)은 핵심 IP이나, 물리적 접근 시 유출 가능
2. **단일 vLLM 인스턴스 = 단일 모델**: 이종 모델(MoE 30B QA용 + 32B 코드생성용)의 동시 운영 및 동적 라우팅 불가
3. **정적 API 키 인증만 지원**: --api-key 옵션은 단순 토큰 검증만 수행, 엔터프라이즈 수준의 RBAC/SSO/감사 로깅 미비

### 1.2 목적

vLLM 추론 엔진 위에 엔터프라이즈 보안, 멀티 모델 오케스트레이션, 인증/인가 레이어를 구축하여:

- 고객사 배포 시 모델 IP를 보호하고 (금융권 재진입 필수 요건)
- SecernCode의 Intelligent Routing과 연계하여 작업별 최적 모델을 동적 선택하고
- 상용화 단계에서 요구되는 엔터프라이즈 인증/감사 체계를 확보한다

### 1.3 범위

본 PRD는 다음 세 가지 기능 영역을 다룬다:

| 영역 | 우선순위 | 대상 |
|------|---------|------|
| 모델 가중치 암호화 | P0 (1순위) | Track 1 + Track 2 공유 인프라 |
| LiteLLM 멀티 모델 셀렉션 | P1 (2순위) | SecernCode Stage 1 연계 우선, Track 1 후속 적용 |
| 인증/RBAC 미들웨어 | P1 (3순위) | 상용화 시 Track 1 + Track 2 공통 적용 |

> **구현 레포**: 모든 인프라 확장 코드는 [secern-vllm-ext](../secern-vllm-ext/) 레포에서 관리한다. 실행 계획은 [vLLM 인프라 로드맵](./09_vllm_infra_roadmap_ko.md) 참조.

---

## 2. 문제 정의

### 2.1 현재 상태

```
[개발자/에이전트] --> [vLLM 서버 (단일 모델, --api-key 정적 토큰)]
                          |
                    [디스크: 평문 모델 가중치]
```

| 항목 | 현재 상태 | 문제 |
|------|----------|------|
| **모델 보안** | safetensors/bin 포맷 평문 저장 | 서버 접근 권한 탈취 시 모델 전체 유출 가능. OS 디스크 암호화만으로는 런타임 유출 방지 불가 ("추론 신뢰 간극") |
| **모델 운영** | 1 vLLM 프로세스 = 1 베이스 모델 | SecernCode 에이전틱 루프(Plan/Execute/Verify)에서 단계별 최적 모델 선택 불가. 수동으로 포트/IP 관리 필요 |
| **접근 제어** | --api-key 단일 정적 토큰 | 사용자 식별 불가, RBAC 미지원, 감사 로깅 없음, Rate Limiting 없음. 금융권 보안 심사 통과 불가 |

### 2.2 목표 상태

```
[개발자/에이전트]
       |
  [인증 게이트웨이 (Go)] -- JWT 검증, RBAC, 감사 로그 (단일 인증 지점)
       |
  [LiteLLM 프록시] -- 단일 엔드포인트, 동적 모델 라우팅, 폴백, Rate Limit, 가상 키
       |
  ┌────┴────┐
  |         |       ← 내부 네트워크만 허용 (vLLM 직접 접근 차단)
[vLLM-A]  [vLLM-B]  -- 역할별 vLLM 클러스터
(32B코드)  (30B-MoE QA) (선택적: --middleware로 심층 방어)
  |         |
[암호화된 가중치] -- Tensorizer + libsodium, GPU 적재 시에만 복호화
```

| 항목 | 목표 상태 |
|------|----------|
| **모델 보안** | Tensorizer 기반 텐서 가중치 암호화. 디스크/스토리지에는 암호문만 존재. GPU VRAM 적재 시점에 On-the-fly 복호화 |
| **모델 운영** | LiteLLM 프록시 경유 단일 엔드포인트. 작업 복잡도에 따라 소형/대형 모델 자동 라우팅. 로드밸런싱 + 폴백 |
| **접근 제어** | LiteLLM 앞단 Go 인증 게이트웨이(secernai-gateway)에서 JWT/SSO 검증, RBAC 인가, 전 요청 감사 로깅. Rate Limiting은 LiteLLM 가상 키 시스템에 위임. vLLM 직접 접근은 K8s NetworkPolicy로 차단 (선택적 심층 방어로 vLLM --middleware 병용 가능) |

---

## 3. 목표 / 비목표

### 3.1 목표 (In Scope)

- 파인튜닝된 sLLM 가중치를 libsodium 기반 Tensorizer로 암호화하고, vLLM 구동 시 On-the-fly 복호화하는 파이프라인 구축
- LiteLLM 프록시를 통한 멀티 모델 셀렉션: 최소 2종 이상의 이종 모델(코드생성용 대형 + QA/요약용 소형) 동시 서빙
- SecernCode의 .secerncode.json 모델 라우팅 설정과 LiteLLM config.yaml 간의 연계 인터페이스 정의
- Track 1(Coco Engine)의 기존 멀티 모델 라우터와 LiteLLM의 공존/마이그레이션 경로 정의
- Go 인증 게이트웨이(secernai-gateway): JWT 토큰 검증, RBAC, 감사 로깅 (Rate Limiting은 LiteLLM 가상 키에 위임)
- 에어갭 환경에서의 오프라인 설치 패키지(pip wheel + Docker 이미지) 제공
- 암호화 키 관리 운영 절차서 (키 생성, 로테이션, 백업, 폐기)

### 3.2 비목표 (Out of Scope)

- vLLM 엔진 코어 코드의 직접 수정 (포크 유지보수 비용 회피)
- 국정원 인증 암호 모듈/HSM 하드웨어 연동 (Phase 2 이후, 특정 고객사 요건 발생 시 커스텀 모델 로더로 대응)
- GPU 클러스터 HA(High Availability) 구성 (별도 인프라 PRD에서 다룸)
- 모델 파인튜닝/학습 파이프라인 자체 (모델 연구팀 소관)
- LiteLLM의 클라우드 프로바이더 연동 기능 (에어갭 환경에서 비활성화)
- Coco Studio/SecernCode TUI의 UI 변경 (인프라 레이어 PRD)

---

## 4. 기능 요구사항

### 4.1 모델 가중치 암호화 (P0 -- 1순위)

#### 4.1.1 암호화 파이프라인

| ID | 요구사항 | 상세 | 수용 기준 |
|----|---------|------|----------|
| ENC-01 | Tensorizer 직렬화 | 파인튜닝된 HuggingFace 포맷 모델을 `tensorize_vllm_model.py`로 Tensorizer 포맷(.tensors)으로 변환 | Qwen2.5-Coder-32B-AWQ, Qwen3-Coder-30B-A3B-AWQ 2종 이상 변환 성공 |
| ENC-02 | libsodium 암호화 적용 | `EncryptionParams.random()` 또는 지정 키파일로 텐서 가중치 배열 암호화. 메타데이터(텐서명, dtype, shape)는 평문 유지 | 암호화된 .tensors 파일이 키 없이 역직렬화 시도 시 실패 확인 |
| ENC-03 | S3 호환 내부 스토리지 연동 | 암호화된 가중치를 MinIO 등 사내 S3 호환 스토리지에 저장 | MinIO 엔드포인트에서 파일 업로드/다운로드 정상 동작 |
| ENC-04 | 키파일 분리 저장 | 암호화 키파일(.key)은 가중치 파일과 물리적으로 분리된 경로에 저장. 파일시스템 퍼미션 0600 | 키파일과 가중치 파일이 동일 볼륨에 존재하지 않음을 검증 |

#### 4.1.2 런타임 복호화

| ID | 요구사항 | 상세 | 수용 기준 |
|----|---------|------|----------|
| DEC-01 | vLLM Tensorizer 로더 활성화 | `--load-format tensorizer`로 vLLM 서버 구동, `--model-loader-extra-config`로 키파일 경로 및 스토리지 자격증명 주입 | vLLM 서버가 암호화된 모델을 정상 로드하고 추론 응답 반환 |
| DEC-02 | On-the-fly GPU 복호화 | 텐서 데이터가 암호화된 상태로 메모리에 버퍼링된 후, GPU VRAM 전송 파이프라인 최종 단계에서만 복호화 | vLLM 종료 후 /tmp, 시스템 swap, page cache에 평문 가중치 잔존 여부를 검증 (GPU VRAM 내 평문은 정상 동작) |
| DEC-03 | 로딩 성능 오버헤드 | 암호화된 모델의 로딩 시간이 평문 safetensors 대비 **2배 이내** | Phase 1 W1에서 평문 Qwen2.5-32B-AWQ 로딩 시간을 기준선으로 측정 완료 (**35.2초, 68.3 tok/s**). 해당 값의 2배(70.4초)를 상한으로 설정. (v0.4: GPT-OSS 20B 서버 부재로 기준 모델 변경) |
| DEC-04 | 추론 성능 무영향 | GPU VRAM 적재 완료 후 추론 성능(tokens/sec)은 평문 모델과 동일 | 동일 프롬프트 100회 벤치마크에서 throughput 차이 1% 미만 |

#### 4.1.3 키 관리

| ID | 요구사항 | 상세 | 수용 기준 |
|----|---------|------|----------|
| KEY-01 | 키 생성 스크립트 | libsodium 기반 암호화 키 생성 CLI 도구 제공 | `secernai-keygen` 명령어로 키 생성 가능 |
| KEY-02 | 키 로테이션 절차 | 기존 모델을 새 키로 재암호화하는 스크립트 및 절차서 | 키 교체 후 vLLM 재구동 시 정상 동작 확인 |
| KEY-03 | 키 백업/복구 | 키 분실 시 모델 사용 불가를 방지하는 오프라인 백업 절차 | 백업에서 복구 후 모델 로딩 정상 동작 |

#### 4.1.4 통합 포인트

| 소비자 | 연동 방식 |
|--------|----------|
| **Track 1 (Coco Engine)** | Coco Engine이 호출하는 vLLM 엔드포인트는 변경 없음. 암호화는 vLLM 서버 내부에서 투명하게 처리 |
| **Track 2 (SecernCode)** | SecernCode의 vLLM provider가 호출하는 OpenAI 호환 API는 변경 없음. 암호화는 인프라 레이어에서 투명 처리 |
| **모델 연구 (황영준M)** | 파인튜닝 완료 후 `tensorize_vllm_model.py` + 암호화 스크립트 실행 절차 문서화 |

---

### 4.2 LiteLLM 멀티 모델 셀렉션 (P1 -- 2순위)

#### 4.2.1 프록시 아키텍처

| ID | 요구사항 | 상세 | 수용 기준 |
|----|---------|------|----------|
| LIT-01 | LiteLLM 프록시 서버 배포 | Docker 컨테이너로 LiteLLM 프록시 배포, 에어갭 환경용 오프라인 이미지 제공 | `docker run` 으로 프록시 기동, 헬스체크 통과 |
| LIT-02 | config.yaml 모델 매핑 | 최소 2종 모델(코드생성 32B + QA/경량 MoE)을 가상 모델명(model_name)으로 매핑 | `secern-coder-32b`, `secern-light-moe` 호출 시 올바른 백엔드로 라우팅 (예시, 실제 모델명은 .secerncode.json과 동기화) |
| LIT-03 | 단일 엔드포인트 | 개발자/에이전트는 `http://litellm:4000/v1` 하나만 알면 됨 | 기존 vLLM 직접 호출을 LiteLLM 엔드포인트로 교체 후 정상 동작 |
| LIT-04 | OpenAI API 완전 호환 | /v1/chat/completions, /v1/completions, /v1/models 엔드포인트 호환 | SecernCode의 openai-go 클라이언트가 변경 없이 동작 |

#### 4.2.2 라우팅 및 폴백

| ID | 요구사항 | 상세 | 수용 기준 |
|----|---------|------|----------|
| LIT-05 | 동적 부하 분산 | 동일 model_name 하위에 복수 vLLM 배포 시 `least-busy` 또는 `latency-based` 라우팅 | 2대 vLLM 노드에 트래픽이 균등 분산됨을 로그로 확인 |
| LIT-06 | 자동 폴백 | 주력 모델 서버 장애 시 대체 모델로 자동 전환 | 32B 서버 다운 시 30B-MoE로 폴백, 응답 반환 확인 (degraded mode) |
| LIT-07 | 프로토콜 변환 | Anthropic Messages API 포맷 -> OpenAI 포맷 변환 (와일드카드 `claude-*` 매핑) | SecernCode가 `claude-3-sonnet` 모델명으로 요청 시 로컬 vLLM으로 투명 라우팅 |
| LIT-08 | 모델 A/B 테스트 | 동일 요청을 복수 모델로 분배하여 품질 비교 가능 | config.yaml에서 트래픽 비율(예: 80/20) 설정 후 분배 비율 로그 확인 |

#### 4.2.3 거버넌스

| ID | 요구사항 | 상세 | 수용 기준 |
|----|---------|------|----------|
| LIT-09 | 가상 키 시스템 | 개발자/팀/프로젝트별 가상 API 키 발급 및 사용량 추적 | LiteLLM 관리 UI에서 키별 사용량 대시보드 확인 |
| LIT-10 | Rate Limiting | 사용자별 RPM(분당 요청 수), TPM(분당 토큰 수) 제한 | 한도 초과 시 HTTP 429 반환 |
| LIT-11 | 사용량 로깅 | 모든 요청/응답의 메타데이터(모델, 토큰 수, 지연시간, 사용자) 로깅 | JSON 포맷 로그 파일로 출력, 30일 보관 |

#### 4.2.4 라우팅 책임 분리 (SecernCode Model Router vs LiteLLM)

> **한 줄 원칙: "SecernCode는 WHAT, LiteLLM은 WHERE"**

| 계층 | 담당 | 역할 | 예시 |
|------|------|------|------|
| **Application (SecernCode Model Router)** | "어떤 역할에 어떤 논리적 모델을 쓸지" 결정 | 에이전트-모델 매핑. `.secerncode.json`의 `models` 섹션에서 coder/planner/reviewer 등 역할별 논리적 모델명을 지정 | coder → `secern-coder-32b`, reviewer → `secern-light-8b` |
| **Infrastructure (LiteLLM)** | "논리적 모델명이 어떤 물리적 vLLM 인스턴스에 있는지" 결정 | 물리 라우팅 + 로드밸런싱 + 폴백. `config.yaml`에서 논리적 모델명을 실제 vLLM 엔드포인트로 매핑 | `secern-coder-32b` → `http://vllm-a:8000` (주력) + `http://vllm-b:8000` (폴백) |

이 분리에 의해 SecernCode는 물리적 인프라를 알 필요 없고, LiteLLM은 에이전트 로직을 알 필요 없다. 모델 추가/이동/스케일링 시 SecernCode 코드 변경 없이 LiteLLM config.yaml만 수정하면 된다.

#### 4.2.5 통합 포인트

| 소비자 | 연동 방식 |
|--------|----------|
| **Track 2 (SecernCode)** | `.secerncode.json`의 `models` 섹션에서 LiteLLM 엔드포인트를 프로바이더로 지정. SecernCode의 Model Router가 LiteLLM의 가상 모델명을 호출. Intelligent Routing(에이전트별 모델 분리: coder=32B, planner=32B, reviewer=7B) 설정과 LiteLLM config.yaml 매핑을 동기화하는 가이드 문서 제공 |
| **Track 1 (Coco Engine)** | Coco Engine의 기존 멀티 모델 라우터가 직접 vLLM을 호출하는 현재 구조 유지. Phase 2 이후 LiteLLM으로 마이그레이션하는 경로 문서화 (비파괴적 전환: Coco Engine의 vLLM 엔드포인트를 LiteLLM으로 변경만 하면 됨) |
| **모델 연구 (황영준M)** | 새 모델 추가 시 config.yaml에 엔트리 추가 + vLLM 컨테이너 기동만으로 라우팅 자동 적용. 모델 A/B 테스트로 벤치마크 자동화 연계 가능 |

---

### 4.3 인증/RBAC 미들웨어 (P1 -- 3순위)

#### 4.3.1 인증 (Authentication)

| ID | 요구사항 | 상세 | 수용 기준 |
|----|---------|------|----------|
| AUTH-01 | LiteLLM 앞단 Go 인증 게이트웨이 | Go 리버스 프록시(`secernai-gateway`)로 개발. LiteLLM 프록시 앞에 독립 바이너리로 배치하여 단일 인증 지점(Single Authentication Point)을 제공. 컴파일 바이너리로 소스 비노출. vLLM의 `--middleware`는 선택적 심층 방어(Defense-in-Depth)로만 활용 (LiteLLM 우회 방지, 필수 아님). 구현 코드는 secern-vllm-ext 레포(`cmd/gateway/`, `internal/`)에서 관리 | LiteLLM 프록시를 경유하는 모든 요청이 게이트웨이에서 인증됨. vLLM 직접 접근은 K8s NetworkPolicy로 차단 |
| AUTH-02 | JWT 토큰 검증 | `Authorization: Bearer <token>` 헤더에서 JWT 추출, 서명 검증, 만료 시간 확인 | 유효 토큰 -> 200, 무효/만료 토큰 -> 401 |
| AUTH-03 | 로컬 토큰 블랙리스트 | Redis 기반 폐기된 토큰 목록 관리. 밀리초 단위 조회 | 블랙리스트된 토큰으로 요청 시 401 반환, 조회 지연 < 5ms |
| AUTH-04 | 헬스체크 예외 | `/health`, `/_health` 엔드포인트는 인증 없이 접근 허용 | 인증 헤더 없이 헬스체크 200 응답 |

#### 4.3.2 인가 (Authorization / RBAC)

| ID | 요구사항 | 상세 | 수용 기준 |
|----|---------|------|----------|
| RBAC-01 | 역할 기반 모델 접근 제어 | JWT 페이로드의 role 필드로 접근 가능 모델 범위 제한 (예: developer -> 7B만, architect -> 32B 포함) | role=developer로 32B 모델 요청 시 403 반환 |
| RBAC-02 | 모델 접근 제어 | JWT 페이로드의 role + team 필드 조합으로 접근 가능 모델 범위 및 파라미터 상한(max_tokens 등) 제한. Rate Limiting은 LiteLLM 가상 키 시스템(LIT-10)에 위임 | role=developer가 max_tokens=8192 초과 요청 시 403 반환 |
| RBAC-03 | 컨텍스트 주입 | 인증 완료 후 사용자 정보를 `request.state.user`에 저장, 후속 파이프라인에서 활용 가능 | 감사 로그에 사용자 ID, 역할, IP가 기록됨 |

#### 4.3.3 감사 로깅

| ID | 요구사항 | 상세 | 수용 기준 |
|----|---------|------|----------|
| AUDIT-01 | 전 요청 감사 로그 | 모든 인증된 요청에 대해 timestamp, user_id, role, model, endpoint, token_count, response_status 기록 | 구조화된 JSON 로그, 쿼리 응답 < 1초 |
| AUDIT-02 | 실패 요청 로그 | 인증 실패(401), 권한 부족(403), Rate Limit(429) 시도 기록 | 보안 감사 시 실패 시도 추적 가능 |
| AUDIT-03 | 로그 보관 정책 | 최소 90일 보관, 일별 로테이션 | logrotate 설정으로 90일 보관 확인 |

#### 4.3.4 사내 IdP 연동 (확장)

| ID | 요구사항 | 상세 | 수용 기준 |
|----|---------|------|----------|
| IDP-01 | SSO/SAML 2.0 연동 설계 | Active Directory, Okta, Microsoft Entra ID 연동을 위한 인터페이스 설계 (구현은 고객사 요건 확정 후) | 인터페이스 명세서 및 연동 가이드 문서 |
| IDP-02 | 라이선스 서버 연동 | Secern AI 자체 라이선스 서버와의 통신으로 동시 접속자 수 제한 및 누적 토큰 사용량 확인 | 라이선스 만료 시 503 반환, 동시 접속 초과 시 429 반환 |

#### 4.3.5 통합 포인트

| 소비자 | 연동 방식 |
|--------|----------|
| **Track 1 (Coco Engine)** | Coco Engine -> vLLM 요청 시 Authorization 헤더에 서비스 JWT 토큰 첨부. Engine용 서비스 계정 발급 (role: service, Rate Limit 높음) |
| **Track 2 (SecernCode)** | SecernCode 에이전트가 vLLM 호출 시 사용자 세션 토큰을 전달. SecernCode의 auth 모듈과 토큰 포맷 공유 |
| **Coco Admin** | 관리자 웹 UI에서 사용자/역할/Rate Limit 관리. REST API로 RBAC 설정 CRUD |

---

## 5. 비기능 요구사항

### 5.1 성능

| 항목 | 기준 |
|------|------|
| 암호화 모델 로딩 시간 | 평문 모델 대비 **2배 이내** (Qwen2.5-32B-AWQ 기준선: 35.2초, ≤70.4초) |
| 추론 throughput 영향 | 암호화 적용 후 tokens/sec 차이 **1% 미만** (GPU 적재 후에는 평문과 동일) |
| LiteLLM 프록시 지연 | 프록시 경유 시 추가 지연 **< 10ms** (네트워크 hop 제외) |
| 인증 미들웨어 지연 | JWT 검증 + RBAC 확인 **< 5ms** per request |
| 동시 사용자 | 최소 **10명 동시 접속**, 목표 40명 (동시 10명 40초 이내 응답, 기존 목표 지표 유지) |

### 5.2 보안

| 항목 | 기준 |
|------|------|
| 암호화 알고리즘 | libsodium (NaCl) 기반, AES-256 수준 이상 |
| 키 파일 퍼미션 | 0600, 전용 서비스 계정만 읽기 가능 |
| 키-가중치 물리 분리 | 암호화 키와 가중치 파일은 별도 볼륨/경로에 저장 |
| 토큰 만료 | JWT 만료 시간 기본 8시간, 설정 가능 |
| 감사 로그 무결성 | 로그 파일 append-only, 삭제/수정 불가 (파일 퍼미션으로 보장) |

### 5.3 호환성

| 항목 | 기준 |
|------|------|
| vLLM 버전 | >= 0.6.0 (tool calling 지원 필수). 운영 환경: **v0.14.0** (Docker `vllm/vllm-openai:v0.14.0`) |
| Python | >= 3.10. 운영 환경: Docker 내부 **3.12.12** (Cython .so 빌드 시 3.12 기준 필수) |
| LiteLLM | 최신 안정 버전, OpenAI API 호환 |
| 컨테이너 런타임 | Docker >= 24.0 |
| GPU | NVIDIA A40/A100/H100 (기존 요구사항 유지) |

### 5.4 운영

| 항목 | 기준 |
|------|------|
| 에어갭 설치 | 모든 의존성 pip wheel + Docker 이미지를 오프라인 패키지로 제공. Cython 컴파일은 사내 빌드 환경에서 수행, 고객사에는 .so만 배포 |
| 설정 변경 | config.yaml 변경으로 모델 추가/제거, 무중단 리로드 (LiteLLM hot-reload) |
| 모니터링 | LiteLLM 관리 UI 대시보드로 모델별 사용량/지연시간/에러율 확인 |
| 백업/복구 | 암호화 키, config.yaml, RBAC 설정의 백업/복구 절차서 제공 |

### 5.5 K8s 배포 아키텍처

| 항목 | 기준 |
|------|------|
| 컨테이너 오케스트레이션 | Kubernetes, Helm umbrella chart (vLLM/LiteLLM 공식 서브차트 활용) |
| GPU 스케줄링 | vLLM Pod에 `nvidia.com/gpu` 리소스 요청 + GPU 노드 nodeSelector/tolerations |
| 네트워크 정책 | K8s NetworkPolicy: LiteLLM Pod만 vLLM 8000포트 접근 허용, 외부 직접 접근 차단 |
| Secret 관리 | 암호화 키, JWT 시크릿 → K8s Secret. 키-가중치 물리 분리 자연 충족 |
| 설정 관리 | LiteLLM config.yaml, RBAC 정책 → K8s ConfigMap |
| 수평 확장 | secernai-gateway + LiteLLM: HPA 가능 (무상태). vLLM: 수동 스케일링 (모델 로딩 비용) |
| 에어갭 배포 | `docker save` + `helm package` → tarball 번들 (`scripts/airgap-bundle.sh`) |

---

## 6. 의존성 및 제약사항

### 6.1 의존성

| 의존 항목 | 설명 | 상태 |
|----------|------|------|
| vLLM >= 0.6.0 | Tensorizer 통합, --middleware 지원, tool calling 필수 | 운영 중 |
| CoreWeave Tensorizer | libsodium 기반 텐서 암호화 라이브러리 | 오픈소스, vLLM 네이티브 통합 |
| LiteLLM | 멀티 모델 프록시 서버 | 오픈소스 (MIT) |
| Redis | 토큰 블랙리스트, Rate Limiting 카운터 | 사내 인프라 구축 필요 |
| MinIO (또는 S3 호환) | 암호화된 가중치 저장소 | 사내 인프라 구축 필요 |
| SecernCode Stage 1 | Intelligent Routing, Qwen3-Coder tool parser | 2026 Q2 착수 예정 |

### 6.2 제약사항

| 제약 | 영향 | 대응 |
|------|------|------|
| **2인 팀** | 동시 개발 항목 제한 | 순차 개발 (암호화 -> LiteLLM -> 인증), 검증된 오픈소스 컴포넌트 최대 활용 |
| **에어갭 환경** | pip/docker 온라인 설치 불가 | 오프라인 패키지 번들 사전 준비, 의존성 버전 고정 |
| **vLLM 단일 모델 제약** | 1 프로세스 = 1 모델 | LiteLLM 프록시로 복수 vLLM 인스턴스 오케스트레이션 |
| **GPU 자원 한정** | 복수 vLLM 인스턴스 운영 시 GPU 메모리 분할 필요 | 가중치만 ~26GB이나 KV Cache 포함 시 60~80GB 이상. Phase 1 W1 VRAM 실측 후 모델 조합 결정 |
| **금융권 특수 보안 요건** | 국정원 인증 암호 모듈 요구 가능성 | Phase 1에서 Tensorizer 기본 암호화, 요건 발생 시 register_model_loader로 커스텀 확장 |

---

## 7. 마일스톤 및 일정

### 리소스 분담

Phase 1(모델 암호화)은 **주용수**가 주도하며, SecernCode Stage 1(eGovFrame RAG + Qwen3-Coder)은 **황영준M**이 주도한다. 두 트랙은 병렬 진행하되, Phase 1 W5(vLLM 검증)에서 합류 포인트를 둔다. Phase 2부터는 SecernCode Stage 1과의 통합 테스트가 발생하므로 양쪽 담당자의 협업 비중이 증가한다.

### Phase 1: 모델 가중치 암호화 (2026 Q2 전반, 4~5월)

| 주차 | 작업 | 담당 | 산출물 |
|------|------|------|--------|
| W1 | **VRAM 실측 벤치마크** ~~+ Tensorizer 환경 구축~~ | 주용수 | ✅ 완료 (2026-04-01): VRAM 보고서 v1.0, OQ-4 **Go**, 기준선 35.2초/68.3 tok/s. Tensorizer는 Docker 미포함으로 W1-2로 이관 |
| W1-2 | Tensorizer 직렬화 파이프라인 개발 + MinIO/S3 호환 스토리지 가용성 확인 | 주용수 | 모델 변환 스크립트, 테스트 보고서, 스토리지 가용성 확인 결과 |
| W3-4 | libsodium 암호화 적용 + 키 관리 도구 (MinIO 미가용 시 W3에 구축) | 주용수 | secernai-keygen CLI, 키 관리 절차서 |
| W5 | vLLM --load-format tensorizer 검증 + 성능 벤치마크 | 주용수 + 황영준M | 로딩 시간/throughput 벤치마크 보고서 |
| W6 | S3 호환 스토리지(MinIO) 연동 + E2E 테스트 | 주용수 | 배포 가이드, E2E 테스트 결과 |

**마일스톤 체크포인트**:
- **W1 게이트**: ✅ 통과 (2026-04-01). 32B-AWQ + 30B-MoE 동시 서빙 **가능** 확인 (80,149/81,920 MiB). OQ-4 **Go**
- **W5~6**: Qwen2.5-32B-AWQ 암호화 모델이 vLLM에서 정상 추론 동작, 로딩 시간 기준선(35.2초)의 2배 이내

### Phase 2: LiteLLM 멀티 모델 셀렉션 (2026 Q2 후반, 5~6월)

| 주차 | 작업 | 담당 | 산출물 |
|------|------|------|--------|
| W7 | **VRAM Go/No-Go 게이트**: W1 실측 결과에 따라 멀티 인스턴스 vs Multi-LoRA vs 단일 모델+A/B 전환 최종 결정 | 주용수 + 황영준M | 모델 운영 전략 결정 문서 |
| W7-8 | LiteLLM 프록시 배포 + config.yaml 작성 + 에어갭 Docker 이미지 | 주용수 | Docker 이미지, 배포 가이드 |
| W9-10 | SecernCode .secerncode.json 연계 + Intelligent Routing 동기화 | 주용수 + 황영준M | 연계 가이드, 통합 테스트 |
| W11 | 로드밸런싱/폴백 검증 + 모델 A/B 테스트 구조 구축 | 주용수 | 부하 테스트 보고서 |
| W12 | Track 1 마이그레이션 경로 문서화 + 거버넌스(가상 키/Rate Limit) 설정 | 주용수 | 마이그레이션 가이드, 운영 매뉴얼 |

**마일스톤 체크포인트**:
- **W7 게이트**: VRAM 실측 기반 모델 운영 전략 확정
- **W12**: SecernCode Stage 1에서 LiteLLM 경유 멀티 모델 라우팅 정상 동작, 모델 A/B 테스트 1회 이상 실시

### Phase 3: 인증/RBAC 미들웨어 (2026 Q3 전반, 7~8월)

| 주차 | 작업 | 담당 | 산출물 |
|------|------|------|--------|
| W13 | **Redis 인프라 확보** + Go 프로젝트 스캐폴딩 (secernai-gateway) | 주용수 | Redis 가용성 확인, Go gateway 골격 (secern-vllm-ext `cmd/gateway/`) |
| W14-15 | Go 인증 게이트웨이 개발 (JWT 검증 + RBAC 리버스 프록시) | 주용수 | secernai-gateway 바이너리 (secern-vllm-ext `internal/auth/`, `internal/proxy/`) |
| W16-17 | Redis 연동 (블랙리스트) + 감사 로깅 | 주용수 | 감사 로그 스키마, 운영 가이드 (secern-vllm-ext `internal/audit/`) |
| W18-19 | Gateway → LiteLLM → vLLM E2E 통합 테스트 + Helm chart 통합 | 주용수 | 통합 테스트 결과, 성능 벤치마크, Helm v2 |
| W20 | SSO/SAML 연동 인터페이스 설계 + 레포 재평가 게이트 | 주용수 | 인터페이스 명세서, 독립 레포 유지 여부 결정 |

**마일스톤 체크포인트**: Go 인증 게이트웨이에서 JWT 인증 + RBAC가 동작, LiteLLM 경유 전 요청에 감사 로그 정상 기록. Helm chart로 전체 스택 원클릭 배포 가능

> **v0.3 변경 사유**: 인증 게이트웨이를 Python FastAPI에서 **Go 리버스 프록시**로 변경. 사유: ①코드 보안(컴파일 바이너리 소스 비노출) ②에어갭 환경 경량 배포(~20MB 이미지) ③SecernCode(Go)와 기술 스택 일관성. 일정은 W13~W18에서 W13~W20으로 2주 확장 (Go 스캐폴딩 + Helm 통합 포함).

### 전체 타임라인

```
2026 Q2 (4~6월)                          2026 Q3 (7~8월)
┌──────────────────────────────────────┐ ┌──────────────────┐
│ Phase 1: 암호화     │ Phase 2: LiteLLM│ │ Phase 3: 인증    │
│ (W1-W6, 4~5월)     │ (W7-W12, 5~6월) │ │ (W13-W18, 7~8월) │
└──────────────────────────────────────┘ └──────────────────┘
     ↑                      ↑                     ↑
  금융권 재진입         SecernCode            상용화
  선결 조건             Stage 1 연계          필수 요건
```

---

## 8. 성공 지표

| 지표 | 목표 | 측정 방법 |
|------|------|----------|
| 모델 가중치 유출 방지 | 암호화 키 없이 모델 복원 **불가능** | 키 없이 역직렬화 시도 -> 실패 검증 |
| 암호화 로딩 오버헤드 | 평문 대비 **2배 이내** (기준선 35.2초, 상한 70.4초) | Qwen2.5-32B-AWQ 로딩 시간 벤치마크 |
| 암호화 추론 영향 | throughput 차이 **1% 미만** | 동일 프롬프트 100회 벤치마크 |
| 멀티 모델 라우팅 정확도 | 요청이 의도한 모델로 라우팅 **100%** | LiteLLM 로그 분석 |
| LiteLLM 프록시 가용성 | **99.5%** uptime (내부 운영 기준) | 모니터링 대시보드 |
| 인증 미들웨어 지연 | **< 5ms** per request | 부하 테스트 P99 지연 측정 |
| 감사 로그 완전성 | 인증된 요청의 **100%** 로깅 | 요청 수 vs 로그 엔트리 수 대조 |
| 외부 네트워크 호출 | **0건** (에어갭 원칙 유지) | 네트워크 트래픽 모니터링 |

---

## 9. 리스크 및 완화 방안

| # | 리스크 | 발생 확률 | 영향도 | 완화 방안 |
|---|--------|----------|--------|----------|
| R1 | Tensorizer가 최신 vLLM 버전과 호환되지 않음 | 낮음 | 높음 | vLLM 네이티브 통합이므로 호환성 높음. 사전에 타겟 vLLM 버전에서 검증. 대안: register_model_loader로 자체 복호화 로더 구현 |
| R2 | 암호화 키 분실로 모델 사용 불가 | 중간 | 치명적 | 키 백업 절차 의무화 (오프라인 2중 백업). 키 로테이션 스크립트로 정기 교체 |
| R3 | GPU 메모리 부족으로 복수 vLLM 인스턴스 운영 불가 | ~~중간~~ **해소** | 높음 | ✅ **실측 완료 (2026-04-01)**: A100 80GB 1장에서 32B-AWQ(18.14 GiB) + 30B-MoE(15.73 GiB) 동시 서빙 성공 (80,149/81,920 MiB, 97.8%). gpu-util 분할(0.45+0.50) + max-model-len 4096 조건. 동시 추론 시 35~64% 성능 저하 있으나 양쪽 정상 응답. 상세: `secern-vllm-ext/docs/vram_report.md` |
| R4 | LiteLLM 에어갭 설치 시 의존성 누락 | 중간 | 중간 | 오프라인 pip wheel 번들 사전 검증. CI에서 에어갭 시뮬레이션 테스트 |
| R5 | 2인 팀 리소스 부족으로 일정 지연 | 높음 | 중간 | Phase 간 의존성 최소화 (각 Phase가 독립적 가치 제공). 우선순위에 따라 Phase 3 일정 유연하게 조정 |
| R6 | 금융권 고객사가 국정원 인증 암호 모듈을 요구 | 낮음 | 높음 | Phase 1에서 Tensorizer 기본 구축 후, 요건 발생 시 커스텀 모델 로더(register_model_loader)로 HSM 연동 확장. 인터페이스를 미리 설계해 놓음 |
| R7 | SecernCode Stage 1 일정 지연으로 LiteLLM 통합 테스트 불가 | 중간 | 중간 | LiteLLM 자체 기능 검증을 SecernCode 독립적으로 진행. curl/httpie로 API 레벨 테스트 |
| R8 | Python 소스 코드가 고객사에 평문 노출 | 중간 | 중간 | vLLM 커스텀 로더는 Cython `.so`로 컴파일하여 배포 (소스 비노출). 인증 게이트웨이는 Go 컴파일 바이너리. 키 관리 분리로 로직 노출 시에도 키 없이 무용. `docker exec` 접근 가능하므로 Docker만으로 보호 불충분 → Go/.so가 핵심 방어선 |

---

## 10. 미결 사항 (Open Questions)

| # | 질문 | 관련 영역 | 결정 시한 | 영향 |
|---|------|----------|----------|------|
| OQ-1 | Tensorizer의 libsodium 암호화가 금융권 보안 심사에서 충분한 수준으로 인정받을 수 있는가? 국정원 인증 암호 모듈이 필수인 경우 커스텀 모델 로더 개발이 추가로 필요 | 모델 암호화 | Phase 1 착수 전 (4월 초) | 일정 2~4주 추가 가능 |
| OQ-2 | Track 1(Coco Engine)의 기존 멀티 모델 라우터를 LiteLLM으로 즉시 마이그레이션할 것인가, 당분간 병존시킬 것인가? | LiteLLM | Phase 2 착수 전 (5월) | 운영 복잡도 vs 마이그레이션 리스크 |
| OQ-3 | Redis 인프라가 사내에 이미 운영 중인가? 신규 구축이 필요한 경우 인프라 준비 일정 확인 필요 | 인증/RBAC | Phase 3 착수 전 (7월) | Phase 3 일정에 2주 추가 가능 |
| OQ-4 | ~~GPU 서버에서 32B + 7B 두 모델 동시 운영이 가능한가?~~ | LiteLLM | ~~Phase 1 W1~~ | ✅ **해결 (2026-04-01): Go**. A100 80GB 1장에서 Qwen2.5-32B-AWQ + Qwen3-30B-A3B-MoE 동시 서빙 가능. 합산 80,149 MiB (97.8%). 멀티 인스턴스 + LiteLLM 라우팅 전략 채택. 상세: `secern-vllm-ext/docs/vram_report.md` |
| OQ-5 | 암호화 키의 물리적 보관 위치 및 접근 권한 정책은 누가 최종 결정하는가? (인프라팀 vs PM) | 키 관리 | Phase 1 W3 (4월 중순) | 키 관리 절차서 내용에 영향 |
| OQ-6 | SSO/SAML 연동의 구체적 타겟 IdP는? (Active Directory, Okta, Microsoft Entra ID 중) | 인증 | 고객사 확정 시 | Phase 3 인터페이스 설계에 영향 |
| OQ-7 | SecernCode의 Intelligent Routing 설정(.secerncode.json)과 LiteLLM config.yaml 간 설정 동기화를 자동화할 것인가, 매뉴얼로 관리할 것인가? | LiteLLM 연계 | Phase 2 W9 (5월 말) | 자동화 시 추가 개발 2~3일 |
| OQ-8 | 고객사 K8s 환경에 NVIDIA GPU Operator가 사전 설치되어 있는가? | K8s 배포 | Infra-S1 전 | GPU Pod 스케줄링 방식 결정 |
| OQ-9 | 에어갭 프라이빗 이미지 레지스트리 종류는? (Harbor, Nexus 등) | K8s 배포 | Infra-S1 전 | 에어갭 번들 스크립트 타겟 |
| OQ-10 | Ingress Controller 및 TLS 인증서 관리 방식은? | K8s 배포 | Infra-S2 전 | Helm chart Ingress 템플릿 설계 |
| OQ-11 | AWQ 양자화 모델에서 Tensorizer 역직렬화가 정상 동작하는가? | **Phase 2 실측 (2026-04-02)** | ❌ **실패 확인**: 아래 상세 참조 |

**OQ-11 상세 (2026-04-02 실측)**:

vLLM v0.14.0에서 AWQ Marlin + Tensorizer 역직렬화 시 `process_weights_after_loading()` 미호출로 `workspace` 런타임 버퍼 미생성. 직렬화(19GB) 및 역직렬화(15초, 1.3GB/s) 자체는 정상이나, 추론 시 `AttributeError: 'QKVParallelLinear' object has no attribute 'workspace'` 발생.

**이중 변환 위험**: `process_weights_after_loading()`은 ①가중치 포맷 변환 ②workspace 생성을 모두 수행. Tensorizer 직렬화 시점에 가중치는 이미 변환 완료 상태이므로, 이 함수를 그대로 재호출하면 **이중 변환으로 데이터 손상**. workspace 생성만 별도 호출해야 함.

| 대안 | 실현 가능성 | 리스크 |
|------|------------|--------|
| ① 비양자화 FP16 모델 사용 | **확실** | GPU 메모리 3배 (64GB vs 19GB) |
| ② Phase 4 커스텀 로더에서 workspace만 선택 생성 | **가능성 높음** (PoC 검증 필요) | 양자화 레이어 탐지 + 이중 변환 방지 필요. 실제 검증 전 단언 불가 |
| ③ vLLM 업스트림 패치 대기 | 불확실 | 수정 시점 예측 불가 |

---

## ADR (Architecture Decision Record)

### Decision
vLLM의 공식 확장 포인트(Tensorizer, --middleware, register_model_loader)와 LiteLLM 프록시를 조합하여 모델 암호화, 멀티 모델 셀렉션, 인증/RBAC 인프라를 구축한다.

### Drivers
1. 고객사 배포 시 모델 IP 보호 시급성 (금융권 재진입 필수 요건)
2. SecernCode Stage 1과 동기적 멀티 모델 라우팅 준비 필요
3. 2인 팀 제약으로 검증된 오픈소스 컴포넌트 최대 활용 필수

### Alternatives Considered
- **완전 자체 구현**: 프록시/암호화/인증 모두 처음부터 개발. 개발 공수 3~4배 증가, 검증되지 않은 보안 구현 리스크로 기각.
- **Nginx 리버스 프록시 + SecernCode Model Router (Option C)**: 로드밸런싱은 가능하나, 가상 키/사용량 추적 및 모델 A/B 테스트 등 핵심 거버넌스 요건을 직접 구현해야 함. 프로토콜 변환(Anthropic→OpenAI) 미지원. 2인 팀으로 LiteLLM 내장 기능을 재구현하는 것은 비현실적이므로 기각.
- **vLLM Multi-LoRA만 활용**: 동일 베이스 모델 위 LoRA 어댑터 교체로는 이종 모델(7B + 32B) 동시 서빙 불가. 보조적 활용은 가능하나 멀티 모델 셀렉션의 대안이 되지 못함.

### Why Chosen
- vLLM 코어 비수정 원칙을 유지하면서 최대한의 확장성 확보
- Tensorizer는 vLLM 네이티브 통합으로 호환성 리스크 최소
- LiteLLM은 100+ 프로바이더 지원의 업계 표준, MIT 라이선스
- 각 컴포넌트가 독립적이어서 순차 배포 가능 (2인 팀에 적합)

### Consequences
- LiteLLM 프록시라는 추가 인프라 컴포넌트 운영 부담 발생
- Tensorizer 포맷 변환이라는 모델 배포 파이프라인 단계 추가
- 금융권 특수 요건(국정원 암호 모듈) 발생 시 커스텀 모델 로더 추가 개발 필요
- (v0.3) 인증 게이트웨이 Go 전환으로 Go+Python 이중 스택 관리 부담. 다만 런타임 Python은 Cython .so뿐이므로 실질적 부담 제한적

### Follow-ups
- Infra-S0 완료 후: 금융권 보안 심사 대응 가능 여부 평가
- Infra-S1 완료 후: Track 1 LiteLLM 마이그레이션 여부 결정
- Infra-S2 완료 후: 실제 고객사 환경에서 E2E 보안 테스트 실시. secern-vllm-ext 독립 레포 유지 여부 재평가
- 장기: 국정원 인증 암호 모듈/HSM 연동 커스텀 로더 개발 (고객사 요건 발생 시)
- (v0.3) Go 게이트웨이의 OpenAPI spec 정의 → 향후 기술 재평가 시 Python 회귀 경로 확보

---

## 관련 문서

- [vLLM 인프라 고도화 R&D 계획](./06_vllm_rd_plan_ko.md): 기초 기술 조사 보고서
- [구현 로드맵](./01_roadmap_ko.md): 전체 프로젝트 로드맵 (Phase/Stage)
- [트랙 2 기술 전략 리서치](../01_strategy/05_track2_tech_strategy_ko.md): SecernCode 기술 전략
- [SecernCode 현황 보고서](./07_secerncode_status_ko.md): Track 2 개발 현황
- [비용 분석](./03_cost_analysis_ko.md): 인프라 비용 TCO/ROI

---

## 변경이력

| 버전 | 일자 | 변경 내용 | 작성자 |
|------|------|----------|--------|
| 0.1 | 2026-03-30 | PRD 초안 작성 | PM (주용수) |
| 0.2 | 2026-03-30 | Architect/Critic 피드백 반영: 인증 게이트웨이 배치 모순 해소(C1), VRAM 산정 정정 및 W1 실측 게이트(C2), 라우팅 책임 분리 ADR(M1), Option C 비교 분석(M2), 리소스 충돌 해소(M3), Rate Limiting 단일 책임(G1~G7) 등 | PM (주용수) |
| 0.3 | 2026-03-31 | 인증 게이트웨이 Python FastAPI → Go 리버스 프록시(secernai-gateway) 전환, K8s 배포 아키텍처(§5.5) 추가, R8(Python 소스 보안) 추가, OQ-8~10(K8s) 추가, secern-vllm-ext 레포 참조 추가, Phase 3 마일스톤 Go/Helm 반영, ADR Follow-ups 갱신, 로드맵(09) 네비게이션 연결 | PM (주용수) |
| 0.4 | 2026-04-02 | **Phase 1 W1 실측 결과 반영**: OQ-4 Go 결정(32B+30B 동시 서빙 가능), R3 리스크 해소, 기준선 모델 GPT-OSS 20B→Qwen2.5-32B-AWQ 변경(서버 부재), DEC-03 기준선 확정(35.2초/68.3 tok/s), 운영 환경 반영(vLLM v0.14.0 Docker, Python 3.12), 모델명 7B→30B-MoE 갱신(ENC-01/LIT-02/LIT-06), W1 마일스톤 통과 기록 | PM (주용수) |
| 0.5 | 2026-04-02 | OQ-11 추가 — AWQ+Tensorizer 역직렬화 호환성 문제 실측 확인, Phase 2 실행 결과 반영 | PM (주용수) |
| 0.6 | 2026-04-02 | OQ-11 상세화 — 이중 변환 위험 분석, 대안별 실현 가능성·리스크 평가 추가 | PM (주용수) |
