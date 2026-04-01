# vLLM 인프라 고도화 로드맵

| 항목 | 내용 |
|------|------|
| **문서번호** | SAI-IMPL-2026-009 |
| **작성일** | 2026년 3월 31일 |
| **버전** | v1.0 |
| **보안등급** | 대외비 |
| **작성** | Secern AI |

> **참고 문서** | 이전: [vLLM 인프라 PRD](./08_vllm_infra_prd_ko.md) | 다음: 없음 | [폴더 인덱스](./README.md)

---

> **TL;DR**
> - vLLM 인프라 고도화를 **Infra-S0~S3 + Prod** 5단계 Stage로 세분화한 실행 계획
> - **secern-vllm-ext** 독립 레포(Go+Python)에서 구현: 인증 게이트웨이(Go), 모델 암호화(Cython .so), LiteLLM 프록시 설정
> - 모든 서비스 Docker/K8s 기반 배포, Helm umbrella chart로 오케스트레이션
> - vLLM 자체는 포크하지 않음 — 공식 확장점(`register_model_loader`, `--middleware`)만 사용
> - 고객사에는 컴파일 바이너리(Go→binary, Python→.so)만 전달하는 코드 보안 원칙
>
> **대상**: PM, 인프라 엔지니어 | **소요**: ~15분 | **용어**: [용어집](../05_knowledge_base/glossary_ko.md)
>
> **관련 문서**: [PRD (요구사항)](./08_vllm_infra_prd_ko.md) | [R&D 계획](./06_vllm_rd_plan_ko.md) | [로드맵 — 인프라 섹션](./01_roadmap_ko.md) | [SecernCode 현황](./07_secerncode_status_ko.md)

---

## 1. 개요

### 1.1 목적

본 문서는 [vLLM 인프라 고도화 PRD](./08_vllm_infra_prd_ko.md)(SAI-IMPL-2026-008)의 **실행 계획**이다. PRD가 "무엇을(WHAT)" 정의한다면, 이 로드맵은 "어떻게, 언제(HOW/WHEN)" 구현할지를 정의한다.

### 1.2 현재 상태

| 항목 | 현재 | 목표 |
|------|------|------|
| 모델 보안 | 평문 safetensors 저장 | Tensorizer + libsodium 암호화, GPU 적재 시 복호화 |
| 모델 운영 | 1 vLLM = 1 모델 | LiteLLM 프록시, 동적 라우팅, 폴백 |
| 접근 제어 | 정적 API 키 | Go 인증 게이트웨이, JWT/RBAC, 감사 로깅 |
| 배포 | 수동 | Docker/K8s, Helm chart, 에어갭 번들 |

### 1.3 PRD 원칙 (참조)

1. 에어갭 우선 (Air-Gap First)
2. vLLM 코어 비수정 (Upstream Compatibility)
3. 투트랙 통합 (Dual-Track Convergence)
4. 점진적 배포 (Incremental Delivery)
5. 금융권 보안 기준 충족 (Financial-Grade Security)

---

## 2. secern-vllm-ext 코드 레포

### 2.1 기본 정보

| 항목 | 내용 |
|------|------|
| **레포명** | secern-vllm-ext |
| **GitHub** | CUBOX-Co-Ltd/secern-vllm-ext (비공개) |
| **언어** | Go 1.24 (런타임) + Python 3.10 (빌드/Cython) |
| **PM 서브모듈** | `secern-vllm-ext/` (루트 레벨, dev 브랜치) |
| **담당** | 주용수 (PM/인프라) |

### 2.2 기술스택 ADR

**결정: Go 중심 + Python 최소 + Docker/K8s 배포**

| 컴포넌트 | 언어 | Docker 이미지 | 실행 위치 | 보안 |
|----------|------|--------------|----------|------|
| secernai-gateway (인증/RBAC) | **Go** | `secerninfra/gateway` (~20MB) | 고객사 K8s | 소스 비노출 |
| secernai-keygen (키 관리 CLI) | **Go** | 이미지 또는 USB | 고객사/사내 | 소스 비노출 |
| vLLM 커스텀 로더 (복호화) | Python → **Cython .so** | vLLM 이미지에 번들 | 고객사 K8s (GPU) | .so 소스 비노출 |
| LiteLLM 프록시 | Python (공식) | 공식 이미지 + config | 고객사 K8s | 설정만 노출 |
| Redis | - | `redis:7-alpine` | 고객사 K8s | - |
| encrypt_model.py (암호화) | Python | 사내 빌드 이미지 | **사내 전용** | 외부 미배포 |

**기각 대안**:
- Python 올인: Docker 내에서도 소스 노출(`docker exec`/`docker cp` 접근 가능) → 기각
- Go 올인: Tensorizer Python API 재구현 비현실적 → 기각
- Rust: 팀 경험 없음 → 기각

### 2.3 디렉토리 구조

```
secern-vllm-ext/
├── cmd/
│   ├── gateway/                # Go: secernai-gateway (인증/RBAC 리버스 프록시)
│   └── keygen/                 # Go: secernai-keygen (키 관리 CLI)
├── internal/                   # Go 내부 패키지
│   ├── auth/                   # JWT 검증, RBAC
│   ├── proxy/                  # LiteLLM 리버스 프록시 로직
│   └── audit/                  # 감사 로깅
├── python/
│   ├── secernai_crypto/        # 모델 암호화 + vLLM 로더
│   │   ├── encrypt.py          # Tensorizer + libsodium (사내 전용)
│   │   └── loader.py           # vLLM 커스텀 로더 (Cython → .so)
│   ├── setup.py                # Cython 빌드 설정
│   └── Makefile                # make build-so → .so 생성
├── deploy/
│   ├── docker/                 # Dockerfiles
│   │   ├── Dockerfile.gateway  # Go 멀티스테이지 빌드
│   │   ├── Dockerfile.vllm     # 공식 vLLM + .so 번들
│   │   └── Dockerfile.build    # 사내 빌드 (Cython + encrypt)
│   ├── docker-compose.yml      # 개발/테스트용
│   ├── docker-compose.prod.yml # 프로덕션용
│   ├── helm/                   # K8s Helm charts
│   │   └── secerninfra/        # Umbrella chart
│   │       ├── Chart.yaml
│   │       ├── values.yaml
│   │       ├── charts/         # 서브차트 (vLLM/LiteLLM 공식)
│   │       └── templates/
│   │           ├── gateway-deployment.yaml
│   │           ├── networkpolicy.yaml
│   │           ├── configmap.yaml
│   │           └── secret.yaml
│   └── config/
│       ├── litellm_config.yaml
│       └── redis.conf
├── scripts/
│   ├── encrypt_model.sh        # 모델 암호화 (사내용)
│   ├── benchmark.sh            # 성능 벤치마크
│   └── airgap-bundle.sh        # docker save + helm package → tarball
├── tests/
├── docs/                       # Stage별 구현 기획서
│   ├── stage0_spec.md
│   ├── stage1_spec.md
│   ├── stage2_spec.md
│   └── deploy-guide.md
├── go.mod
├── AGENTS.md
└── README.md
```

### 2.4 Stage → 컴포넌트 매핑

| Stage | secern-vllm-ext 디렉토리 | 산출물 |
|-------|---------------------|--------|
| Infra-S0 | `python/secernai_crypto/` + `cmd/keygen/` | secernai-keygen, Cython .so, Docker 이미지 |
| Infra-S1 | `deploy/` (Helm, Docker, config) | Helm umbrella chart, 에어갭 번들 |
| Infra-S2 | `cmd/gateway/` + `internal/` | secernai-gateway, NetworkPolicy |

### 2.5 레포 생성 전략

**Stage 0 착수 시 최소 구조로 생성**, 점진적 확장:

| 시점 | 추가 디렉토리 | 이유 |
|------|-------------|------|
| Infra-S0 착수 | README + `python/` + `cmd/keygen/` + `deploy/docker/` | 암호화 MVP |
| Infra-S1 착수 | `deploy/helm/` + `deploy/docker-compose.prod.yml` | K8s 인프라 |
| Infra-S2 착수 | `cmd/gateway/` + `internal/` | Go 게이트웨이 |
| Infra-S2 완료 | - | **재평가 게이트**: 독립 레포 유지 vs SecernCode 통합 |

### 2.6 SecernCode와의 대비

| 항목 | SecernCode | secern-vllm-ext |
|------|-----------|-------------|
| 역할 | Track 2 코딩 에이전트 | vLLM 인프라 확장 (공유) |
| 언어 | Go 1.24 | Go 1.24 + Python(Cython) |
| 대상 | Track 2 전용 | Track 1 + Track 2 공유 |
| 담당 | 황영준M | 주용수 |
| 배포 | 단일 Go 바이너리 | Docker 이미지 + Helm chart |

---

## 3. Stage 로드맵 총괄

> **용어 안내 — Stage vs. Phase**: SecernCode와 동일하게 **Stage**(대단계, PM 마일스톤)와 **Phase**(구현 단위, 개발팀 세분화)로 구분한다. Stage별 Phase 상세는 `secern-vllm-ext/docs/stage{N}_spec.md`에서 정의한다.

| 단계 | 기간 | 내용 | secern-vllm-ext 컴포넌트 | PRD 매핑 | 상태 |
|------|------|------|--------------------|---------|------|
| **Infra-S0** | 2026-04~05 | 모델 가중치 암호화 | python/secernai_crypto + cmd/keygen | PRD §4.1 (P0) | **Phase 1 완료** (OQ-4 Go, 2026-04-01) |
| **Infra-S1** | 2026-05~06 | LiteLLM 멀티 모델 + K8s 배포 | deploy/ (Helm, Docker, config) | PRD §4.2 (P1) | 계획 |
| **Infra-S2** | 2026-07~09 | 인증/RBAC 게이트웨이 (Go) | cmd/gateway + internal/ | PRD §4.3 (Go 수정) | 계획 |
| **Infra-S3** | 2026 Q4+ | 엔터프라이즈 보안 강화 | secernai_crypto 확장 | PRD OQ-1 | 조건부 |
| **Prod** | 2026 Q4 | 통합 검증 + 상용 배포 | 전체 E2E + Helm | 전체 | 계획 |

> **Infra-S2 일정**: 7~**9**월로 1개월 버퍼 추가 (SC-S2와 리소스 경합 완화).

---

## 4. Infra-S0: 모델 가중치 암호화 (P0)

### 4.1 목표

Tensorizer + libsodium을 활용하여 모델 가중치를 디스크 암호화 상태로 저장하고, vLLM 로딩 시 GPU에서 On-the-fly 복호화한다. 키 관리는 Go 바이너리(secernai-keygen)로 분리한다.

### 4.2 Phase 상세

| Phase | 기간 | 내용 | 산출물 | secern-vllm-ext | 게이트 |
|-------|------|------|--------|-------------|--------|
| Phase 1 | W1 | VRAM 벤치마크 + Tensorizer 환경 | VRAM 보고서, 로딩 기준선 | scripts/benchmark.sh | **W1**: 32B+7B 동시 서빙 가능? |
| Phase 2 | W1-2 | Tensorizer 직렬화 + MinIO 연동 | 모델 변환 스크립트 | python/secernai_crypto/encrypt.py | |
| Phase 3 | W3-4 | libsodium 암호화 + keygen CLI (Go) | secernai-keygen 바이너리 | cmd/keygen/ | |
| Phase 4 | W5 | vLLM 커스텀 로더 + Cython .so 빌드 | .so 파일 + 벤치마크 보고서 | python/secernai_crypto/loader.py → .so | **W5**: 로딩 오버헤드 ≤2x? |
| Phase 5 | W6 | S3 연동 + E2E 테스트 + Docker 이미지 | 배포 가이드, 테스트 결과 | deploy/docker/Dockerfile.vllm, tests/ | |

### 4.3 성공 기준

- 암호화된 GPT-OSS 20B가 ≤2x 기준선 시간에 로딩됨
- 추론 처리량 변화 없음 (>99% 동등)
- 암호화 키 없이 모델 복원 불가능
- Cython `.so`로 빌드되어 소스 비노출

### 4.4 리스크

| 리스크 | 영향 | 완화 |
|--------|------|------|
| 32B+7B VRAM 부족 | Stage 전체 아키텍처 변경 | W1 게이트에서 조기 판단 |
| Tensorizer 암호화 성능 저하 | 로딩 시간 초과 | W5 벤치마크, 대안 로더 검토 |

---

## 5. Infra-S1: LiteLLM 멀티 모델 + K8s 배포 (P1)

### 5.1 목표

LiteLLM 프록시를 통해 다중 vLLM 인스턴스를 단일 엔드포인트로 통합하고, Helm umbrella chart로 K8s 배포 자동화를 구축한다.

### 5.2 Phase 상세

| Phase | 기간 | 내용 | 산출물 | secern-vllm-ext | 게이트 |
|-------|------|------|--------|-------------|--------|
| Phase 1 | W7 | VRAM Go/No-Go + K8s 환경 확인 | 운영 전략 결정 | docs/stage1_spec.md | **W7**: 멀티인스턴스 vs Multi-LoRA |
| Phase 2 | W7-8 | LiteLLM Docker + Helm chart 스캐폴딩 | Docker 이미지, Chart.yaml | deploy/helm/secerninfra/ | |
| Phase 3 | W9-10 | SecernCode 연동 + NetworkPolicy | 통합 가이드, 네트워크 정책 | helm/templates/networkpolicy.yaml | |
| Phase 4 | W11 | 로드밸런싱/폴백/A/B + 에어갭 번들 | 부하 테스트, tarball | scripts/airgap-bundle.sh | |
| Phase 5 | W12 | Track 1 마이그레이션 + 거버넌스 | 마이그레이션 가이드, 운영 매뉴얼 | deploy/config/ | **W12**: SecernCode 라우팅 동작? |

### 5.3 SecernCode Stage 1 연계

> **"SecernCode가 WHAT(어떤 모델), LiteLLM이 WHERE(어디서 서빙)"**

- SecernCode Model Router: 작업 유형에 따라 모델 선택 (27B coder, 8B task)
- LiteLLM: 물리적 vLLM 엔드포인트로 라우팅, 폴백, Rate Limit
- `.secerncode.json` 모델명 ↔ `litellm_config.yaml` 가상 모델명 동기화

### 5.4 성공 기준

- 2개 이상 vLLM 인스턴스 동시 운영, LiteLLM 단일 엔드포인트
- SecernCode의 Intelligent Routing이 LiteLLM 경유 정상 동작
- Helm install 1회로 전체 스택 배포 가능
- 에어갭 tarball로 오프라인 배포 가능

### 5.5 리스크

| 리스크 | 영향 | 완화 |
|--------|------|------|
| VRAM 부족으로 멀티인스턴스 불가 | 아키텍처 변경 (Multi-LoRA 등) | W7 Go/No-Go 게이트 |
| LiteLLM 에어갭 의존성 | 설치 실패 | Docker 이미지 사전 빌드 |

---

## 6. Infra-S2: 인증/RBAC 게이트웨이 — Go (P1)

### 6.1 목표

Go 리버스 프록시(secernai-gateway)를 LiteLLM 앞단에 배치하여 JWT 인증, RBAC, 감사 로깅을 제공한다. K8s Deployment로 배포하며 HPA 지원.

> **참고**: PRD v0.2에서는 Python FastAPI로 설계되었으나, 코드 보안(컴파일 바이너리 소스 비노출) + 에어갭 배포 용이성을 위해 Go 리버스 프록시로 변경되었다 (PRD v0.3).

### 6.2 Phase 상세

| Phase | 기간 | 내용 | 산출물 | secern-vllm-ext | 게이트 |
|-------|------|------|--------|-------------|--------|
| Phase 1 | W13 | Go 프로젝트 스캐폴딩 + Redis 인프라 | gateway 골격, Redis 연결 | cmd/gateway/, internal/ | |
| Phase 2 | W14-15 | JWT 검증 + RBAC 리버스 프록시 | secernai-gateway 바이너리 | internal/auth/, internal/proxy/ | |
| Phase 3 | W16-17 | Redis 블랙리스트 + 감사 로깅 | 감사 로그 스키마 | internal/audit/ | |
| Phase 4 | W18-19 | E2E: Gateway→LiteLLM→vLLM + Helm 통합 | 통합 테스트, Helm v2 | deploy/helm/, tests/ | |
| Phase 5 | W20 | SSO/SAML 인터페이스 설계 + 레포 재평가 | 인터페이스 스펙 | docs/ | **W20**: 독립 레포 유지? |

### 6.3 성공 기준

- JWT 인증 + RBAC 정상 동작 (role=developer → 7B만, role=architect → 32B 허용)
- 전 요청 감사 로깅 (100% 추적)
- 인증 지연 <5ms, 프록시 오버헤드 <10ms
- Helm chart로 gateway 포함 전체 스택 원클릭 배포

### 6.4 리스크

| 리스크 | 영향 | 완화 |
|--------|------|------|
| Go 게이트웨이 + LiteLLM 언어 경계 디버깅 | 통합 테스트 복잡 | Phase 4에서 충분한 E2E |
| SC-S2와 리소스 경합 | 일정 지연 | 1개월 버퍼 (7~9월) |

---

## 7. Infra-S3: 엔터프라이즈 보안 강화 (조건부)

| 항목 | 내용 | 트리거 |
|------|------|--------|
| HSM/국정원 인증 암호 모듈 | libsodium → 국정원 KCMVP 인증 모듈 | OQ-1 결과 (금융권 감사 요구사항 확정) |
| HA 구성 | Gateway + LiteLLM 이중화 | 고객사 SLA 요건 확정 |
| vLLM 포크 재검토 | Tensorizer 지원 중단 시 | 재검토 트리거 충족 시 |

---

## 8. K8s 서비스 아키텍처

### 8.1 배포 구조

```
[Ingress / NodePort]
       │
[secernai-gateway]  ← Deployment (CPU, HPA 가능)
       │                Go 바이너리, JWT/RBAC, 감사 로깅
       │
[LiteLLM Proxy]     ← Deployment (CPU, HPA 가능)
       │                모델 라우팅, 폴백, Rate Limit
       │
  ┌────┴────┐
  │         │
[vLLM-A]  [vLLM-B]  ← Deployment (GPU, 수동 스케일링)
(32B코드)  (7B QA)     nvidia.com/gpu, nodeSelector
  │         │
[PVC: 암호화된 모델 가중치]
       │
[Redis]              ← StatefulSet (CPU)
                        토큰 블랙리스트, 세션
```

### 8.2 핵심 설계

| 항목 | 설계 | 이유 |
|------|------|------|
| **서비스 분리** | 각 컴포넌트 독립 Deployment | GPU 낭비 방지, 장애 격리, 개별 스케일링 |
| **GPU 스케줄링** | vLLM Pod에 `nvidia.com/gpu` + nodeSelector | GPU 노드에만 배치 |
| **NetworkPolicy** | LiteLLM만 vLLM 8000포트 접근 허용 | PRD "vLLM 직접 접근 차단" 충족 |
| **Secret 관리** | 암호화 키 → K8s Secret | PRD "키-가중치 물리 분리" 자연 충족 |
| **ConfigMap** | LiteLLM config, RBAC 정책 | 설정 변경 시 Pod 재시작 없이 적용 |
| **HPA** | gateway + LiteLLM (무상태) | 부하 기반 자동 스케일링 |
| **Helm 서브차트** | vLLM/LiteLLM 공식 Helm chart 활용 | 개발 공수 절감 |

### 8.3 에어갭 배포 흐름

```
사내 빌드 환경:
  docker build → docker save → images.tar
  helm package → secerninfra-{version}.tgz
  airgap-bundle.sh → secerninfra-airgap-{version}.tar.gz

고객사 환경:
  USB/내부망 전달
  docker load < images.tar
  helm install secerninfra ./secerninfra-{version}.tgz -f values-customer.yaml
```

---

## 9. 트랙 간 통합 일정

| secern-vllm-ext Stage | 기간 | SecernCode Stage | 연계 포인트 |
|-------------------|------|-----------------|------------|
| Infra-S0 (암호화) | 04~05 | SC-S0 (완료) | 투명 — API 변경 없음 |
| Infra-S1 (LiteLLM+K8s) | 05~06 | SC-S1 (eGovFrame RAG) | W9-10 멀티 모델 라우팅 통합 테스트 |
| Infra-S2 (Go 인증) | 07~09 | SC-S2 (MCP, 다중 에이전트) | 인프라는 독립, S2 완료 후 연동 |
| Infra-S2 완료 | 09 | SC-S3 (RBAC/감사) | 서비스 JWT + RBAC 연동 |
| Prod | Q4 | Alpha | 통합 E2E, 파일럿 |

---

## 10. vLLM 포크 ADR

### 10.1 결론: 포크하지 않는다

| 기준 | 업스트림 유지 (채택) | 포크 생성 (기각) |
|------|---------------------|-----------------|
| 유지보수 | `git pull`만 | 54만 LOC 리베이스, 2인 팀 비현실적 |
| 확장성 | `register_model_loader`, `--middleware`로 충족 | 불필요한 오버킬 |
| 암호화 | Tensorizer 네이티브, 코드 수정 불필요 | 이점 없음 |
| 금융 감사 | 공식 릴리스 증빙 유리 | "자체 수정" 증명 부담 |
| 에어갭 | 서브모듈 태그 고정으로 충분 | 추가 이점 없음 |

### 10.2 관리 방안

- `_public/vllm` 서브모듈을 검증된 특정 태그에 고정
- 확장 코드는 secern-vllm-ext 레포에 분리 관리
- 분기 1회 업스트림 호환성 검토

### 10.3 재검토 트리거

- Tensorizer 지원 중단 또는 비호환 변경
- vLLM 라이선스 변경 (현재 Apache 2.0)
- 국정원 인증 암호 모듈 필수 확정 (OQ-1)

---

## 11. 코드 보안

### 11.1 배포 원칙

> **고객사에는 컴파일된 바이너리만 전달한다.**

| 구분 | 형태 | 위치 |
|------|------|------|
| Go 바이너리 (gateway, keygen) | 컴파일 binary | 고객사 서버 |
| Cython .so (vLLM 로더) | 컴파일 shared library | 고객사 vLLM Docker 이미지 |
| Python 소스 (encrypt.py 등) | 평문 스크립트 | **사내 빌드 서버만** |

### 11.2 보호 메커니즘

- **Go 바이너리**: 역공학 난이도 높음 (casual inspection 차단)
- **Cython .so**: `.py`→`.c`→`.so` 변환, 사내 빌드 환경에서 수행
- **키 관리 분리**: 복호화 로직(.so)을 알아도 키(secernai-keygen 관리) 없으면 무용
- **Docker 이미지**: 코드 보호가 아닌 배포 단위. `docker exec`로 접근 가능하므로 Go/.so가 핵심 방어선
- **K8s Secret**: 암호화 키는 K8s Secret으로 관리, Pod 외부 노출 차단

---

## 12. 미결 사항

PRD OQ-1~7에 추가로 K8s 관련 OQ-8~10을 포함한다.

| OQ | 질문 | 결정 시점 | 영향 |
|----|------|----------|------|
| OQ-1 | Tensorizer libsodium이 금융권 감사 충분? 국정원 인증 필요? | Infra-S0 전 (4월 초) | 2~4주 지연 가능 |
| OQ-4 | 32B+7B 동시 VRAM 가능? | **Infra-S0 W1** | Infra-S1 아키텍처 결정 |
| OQ-8 | 고객사 K8s에 NVIDIA GPU Operator 사전 설치? | Infra-S1 전 | GPU Pod 스케줄링 |
| OQ-9 | 에어갭 프라이빗 이미지 레지스트리 종류 (Harbor/Nexus)? | Infra-S1 전 | 에어갭 번들 스크립트 |
| OQ-10 | Ingress Controller 및 TLS 인증서 관리 방식? | Infra-S2 전 | Helm chart 템플릿 |

> 전체 미결 사항은 [PRD §10](./08_vllm_infra_prd_ko.md) 참조.

---

## 변경이력

| 버전 | 일자 | 변경 내용 | 작성자 |
|------|------|----------|--------|
| 1.0 | 2026-03-31 | 초판 — Infra-S0~S3+Prod Stage 체계, secern-vllm-ext 레포 설계, K8s 아키텍처, vLLM 포크 ADR, 코드 보안 | PM (주용수) |
