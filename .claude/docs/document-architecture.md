# 문서 아키텍처

> 이 문서는 CLAUDE.md의 레퍼런스입니다. 핵심 지침은 [CLAUDE.md](../../CLAUDE.md)를 참조하세요.

## 투트랙 문서 체계

| 구분 | 트랙 1 (IntraGenX) | 트랙 2 (SecernCode) |
|------|--------------------|--------------------|
| **레포** | PM 레포 (이 저장소) | SecernCode 서브모듈 (독립 레포) |
| **전략 문서** | `01_strategy/` | `01_strategy/05_track2_tech_strategy_ko.md` |
| **로드맵** | `02_implementation/01_roadmap_ko.md` Phase 1/2 | 같은 파일의 "트랙 2" 섹션 (Stage 0~4) |
| **기술 상세** | `02_implementation/` 정식 문서 | `SecernCode/docs/` 구현 기획서 |
| **현황 추적** | 로드맵 내 Phase 상태 | `02_implementation/07_secerncode_status_ko.md` |
| **문서 소유** | PM (주용수) | 개발팀 (황영준M) — PM이 현황 보고서만 관리 |

#### 공유 인프라 (SecernInfra)

| 구분 | 공유 인프라 (SecernInfra) |
|------|--------------------------|
| **전략·로드맵** | PM 레포 `02_implementation/09_vllm_infra_roadmap_ko.md` |
| **기술 상세** | `SecernInfra/` 서브모듈 `docs/` (stage0_spec, stage1_spec, stage2_spec) |
| **현황 추적** | 09 로드맵 Stage 상태 컬럼 |
| **문서 소유** | PM (주용수) — 코드+문서 모두 |

## Stage / Phase 용어 체계

트랙 2(SecernCode)는 두 계층의 단계 체계를 사용한다.

### Stage (대단계) — PM 로드맵 관리

PM이 `01_roadmap_ko.md`에서 정의하는 비즈니스 마일스톤 단위.

| Stage | 기간 | 핵심 목표 |
|-------|------|----------|
| Stage 0 | ~2026-03 | MVP: Go 바이너리, TUI/CLI/WebUI, vLLM, Model Router |
| Stage 1 | 2026-04~05 | eGovFrame RAG + Qwen3-Coder + 벤치마크 |
| Stage 2 | 2026-06~07 | 다중 에이전트 오케스트레이션, SI용 MCP 서버 |
| Stage 3 | 2026-08~09 | RBAC, 감사 로깅, 보안 스캐닝 |
| Stage 4 | 2026-10~11 | VS Code 확장, 세션 공유, 대시보드 |
| Alpha | 2026-12 | 내부 테스트 + 파일럿 |

### Phase (구현 단위) — 개발팀 기획서 관리

각 Stage 내부에서 개발팀이 세분화하는 구현 단위. Stage마다 Phase 1부터 시작.

**예: Stage 0의 Phase 구조** (구현 기획서 v2.0 기준)

| Phase | 내용 | 상태 |
|-------|------|------|
| Phase 1 | MVP 기반 구축 (포크, vLLM 연동, 도구 검증) | 완료 |
| Phase 2 | 프롬프트 최적화 (브랜딩, 프로바이더 정리) | 완료 |
| Phase 3 | 핵심 기능 확장 (AGENTS.md, /undo, 자동 수정) | 완료 |
| Phase 4 | Intelligent Model Router | 완료 |
| Phase 5 | eGovFrame 특화 (RAG, 벤치마크) | 진행 중 |
| Phase 6 | 고급 기능 (MCP, WebUI, /plan, Skills) | 대부분 완료 |

> **주의**: 트랙 1도 "Phase 1/2"를 사용하지만, 이는 트랙 2의 Stage/Phase와 **독립적**인 체계이다.

#### Stage 네임스페이스 접두사

프로젝트 간 Stage 번호 충돌을 방지하기 위해 접두사를 사용한다:

| 프로젝트 | 접두사 | 예시 |
|----------|--------|------|
| SecernCode | `SC-` | SC-S0, SC-S1, SC-S2 |
| SecernInfra (vLLM) | `Infra-` | Infra-S0, Infra-S1, Infra-S2 |

로드맵 및 현황 문서에서 Stage를 언급할 때 반드시 접두사를 사용하여 어느 프로젝트의 Stage인지 명시한다.

## 레포 간 교차 참조 규칙

### 방향별 링크 방식

| 방향 | 방식 | 이유 |
|------|------|------|
| **PM → SecernCode** | 상대경로 링크 (`../SecernCode/docs/...`) | 서브모듈이 PM 레포 안에 포함 |
| **SecernCode → PM** | **텍스트로 문서명만 참조** (링크 없음) | SecernCode는 독립 레포, PM 경로 접근 불가 |
| **PM → SecernInfra** | 상대경로 링크 (`../SecernInfra/docs/...`) | 서브모듈이 PM 안에 포함 |
| **SecernInfra → PM** | **텍스트로 문서명만 참조** (링크 없음) | 독립 레포, PM 경로 접근 불가 |

### PM에서 SecernCode 참조 시 패턴

```markdown
상세: [구현 기획서 (Phase 상세)](../SecernCode/docs/secerncode_implementation_spec_v2.md)
```

### SecernCode에서 PM 참조 시 패턴

```markdown
> 관련 PM 문서: `01_roadmap_ko.md` (전체 로드맵), `07_secerncode_status_ko.md` (현황 보고서)
```

### 교차 참조 추가 시 체크리스트

- [ ] PM → SecernCode 링크: 서브모듈 내 파일 경로 확인
- [ ] SecernCode → PM 참조: 텍스트만, 상대경로 링크 사용 금지
- [ ] 양방향 모두 고려: 한쪽에 참조 추가 시 반대쪽에도 텍스트 참조 추가 검토

## 서브모듈 문서 관리

### 현재 서브모듈

| 서브모듈 | 경로 | 용도 |
|---------|------|------|
| SecernCode | `SecernCode/` | 트랙 2 Go 프로젝트 (기술 문서: `docs/`) |

### 변경 절차

1. SecernCode 레포에서 문서 수정 + 커밋
2. PM 레포에서 서브모듈 포인터 업데이트 (`git add SecernCode && git commit`)
3. PM 레포의 `02_implementation/README.md`에 서브모듈 문서 참조 테이블 최신화

### 새 서브모듈 추가 시

1. `git submodule add <url> <path>`
2. CLAUDE.md Document Structure 간략 트리에 추가
3. `.claude/docs/document-structure.md`에 상세 트리 + 문서 목록 추가
4. `02_implementation/README.md`에 참조 테이블 추가
5. 교차 참조 방향 규칙 동일 적용 (PM → 서브모듈만 링크, 역방향은 텍스트)

## 모델 버전 관리

- 트랙 1과 트랙 2는 서로 다른 모델을 사용할 수 있음
  - 트랙 1: Qwen2.5-Coder-32B, GPT-OSS 20B 등
  - 트랙 2: Qwen3.5-Coder-27B, Qwen3.5-Coder-8B 등
- 모델 버전은 각 트랙 담당자가 관리
- 로드맵 문서에서 트랙 간 모델 불일치 시 주석으로 명시
- 통합 시점은 Stage 1 이후 확정 예정

## 향후 Stage 기획서 작성 가이드

### 작성 위치

- 기획서: `SecernCode/docs/stage{N}_spec.md` (예: `stage1_spec.md`)
- PM 레포에 기획서 원본을 두지 않음 — 서브모듈 참조만

### PM 레포 반영 사항

새 Stage 기획서 작성 시 PM 레포에서 업데이트할 문서:

1. `02_implementation/01_roadmap_ko.md` — Stage 테이블 상태 업데이트
2. `02_implementation/07_secerncode_status_ko.md` — 현황 보고서 갱신
3. `02_implementation/README.md` — 서브모듈 문서 참조 테이블 갱신

### 기획서 필수 포함 항목

| 항목 | 설명 |
|------|------|
| 목표 | Stage의 비즈니스/기술 목표 |
| Phase 분류 | 내부 구현 단계 정의 (Phase 1~N) |
| 아키텍처 변경점 | 이전 Stage 대비 변경되는 Layer/컴포넌트 |
| 리스크 | 기술적/일정적 리스크 및 대응 방안 |
| 타임라인 | Phase별 예상 일정 |
| PM 문서 매핑 | Stage ↔ Phase 매핑 주석 (PM이 추적할 수 있도록) |
