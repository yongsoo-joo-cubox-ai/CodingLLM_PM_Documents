# SecernCode (Track 2) 현황 보고서

| 항목 | 내용 |
|------|------|
| **문서번호** | SAI-IMPL-2026-007 |
| **작성일** | 2026년 3월 26일 |
| **버전** | v1.1 |
| **개정일** | 2026년 3월 26일 |
| **보안등급** | 대외비 |
| **작성** | Secern AI |

> **문서 7/7** | 이전: [vLLM R&D 계획](./06_vllm_rd_plan_ko.md) | 다음: 없음 | [폴더 인덱스](./README.md)

---

> **TL;DR**
> - SecernCode는 폐쇄망 환경 전용 AI 코딩 에이전트로, Go 단일 바이너리(~50MB) 하나로 배포·실행
> - 외부 API 없이 로컬 vLLM + Qwen3.5-27B로 완전 오프라인 동작하며, TUI/WebUI/CLI 3가지 모드 지원
> - Phase 1~4 및 Phase 6 구현 완료 (2026년 3월 말 기준); eGovFrame RAG(Phase 5)는 진행 중
> - **로드맵 매핑**: Phase 1~6은 로드맵 상 **Stage 0(MVP)**에 해당. Stage 1 이후는 별도 Phase 체계 사용 예정
> - 대상 독자: 경영진, 기술 팀 리더 | 소요 시간: 약 10분
>
> **관련 문서**: [로드맵 — 트랙 2 Stage 체계](./01_roadmap_ko.md) | [구현 기획서 (Phase 상세)](../SecernCode/docs/secerncode_implementation_spec_v2.md)

---

## 1. 프로젝트 개요

| 항목 | 내용 |
|------|------|
| **제품명** | SecernCode |
| **대외 브랜드** | IntraGenX |
| **소속** | SECERN AI Consortium · 시선AI |
| **목적** | 폐쇄망 환경 AI 코딩 에이전트 |
| **대상** | 한국 공공기관·금융·국방 개발자 (약 28만 명) |
| **기반 언어** | Go 1.24 |
| **배포 방식** | 단일 바이너리 (~50MB), USB 복사 → 실행 |
| **기반 오픈소스** | opencode-ai/opencode (Go, MIT License) |

SecernCode는 망분리(에어갭) 환경에서 외부 API 호출 없이 로컬 vLLM 서버와 공개 모델(Qwen3.5-27B)을 활용하여 코드 작성, 디버깅, 분석을 지원하는 AI 코딩 에이전트다. 트랙 2 코딩 에이전트 전략의 핵심 구현체이며, 시선AI가 주도한다.

---

## 2. 핵심 특징

| 특징 | 설명 |
|------|------|
| **완전 오프라인** | 외부 API 호출 없이 로컬 vLLM + 공개 모델만으로 동작 |
| **단일 바이너리** | `go build` 한 줄로 생성, ~50MB, 런타임 의존 없음 |
| **3가지 실행 모드** | TUI (터미널 대화형) / WebUI (브라우저) / CLI (스크립트·CI 연동) |
| **Intelligent Routing** | 태스크 유형별 최적 모델 자동 선택 (27B 고성능 / 8B 경량) |
| **MCP 네이티브** | 폐쇄망 내부 시스템(DB, Git, Jira 등)을 표준 프로토콜로 연결 |
| **eGovFrame 특화** | 한국 공공기관 표준 프레임워크 네이티브 지원 (예정) |

### Go 선택 근거

| 기준 | Go | TypeScript |
|------|-----|-----------|
| 배포 방식 | 단일 바이너리 (50MB) | node_modules + Node.js 런타임 필요 |
| 폐쇄망 적합성 | USB 파일 하나 복사 → 실행 | npm 패키지 수백 개 수동 이관 필요 |
| 런타임 의존 | 없음 (OS만 맞으면 동작) | Node.js 설치 필수 |
| 크로스 컴파일 | `GOOS=linux go build` 한 줄 | 환경별 네이티브 모듈 호환성 관리 |
| 메모리 사용량 | ~20~30 MB | ~100~200 MB (V8 엔진 포함) |
| 동시성 | goroutine (경량 스레드) | 단일 스레드 + async |
| 시작 시간 | 즉시 | 1~2초 (V8 부팅) |

---

## 3. 시스템 아키텍처 (8 Layer)

```
┌─────────────────────────────────────────────────┐
│  Layer 1 — TUI / WebUI / CLI                    │
│  Chat input · IntraGenX brand · /undo /redo     │
│  Session management · Custom commands            │
└──────────────────────┬──────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────┐
│  Layer 2 — App Orchestrator (app.go)            │
│  Sessions · Messages · History · Permissions     │
└──────────────────────┬──────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────┐
│  Layer 3 — Agent Loop (processGeneration)       │
│  Build prompt → Call LLM → Parse resp.          │
│  Tool use? → Execute tool → 루프 재시작          │
└──────────────────────┬──────────────────────────┘
          ▲            │           ▲
          │            │           │
┌─────────┴──┐  ┌──────▼─────┐  ┌─┴──────────────┐
│ Layer 4    │  │ Layer 5    │  │ Layer 6        │
│ Context    │  │ Tools      │  │ Model Router   │
│ Eng.       │  │            │  │                │
│            │  │ File R/W   │  │ Task Classifier│
│ AGENTS.md  │  │ Bash       │  │     ↓          │
│ Sys prompt │  │ Grep/Glob  │  │   Route        │
│ Compaction │  │ LSP        │  │     ↓          │
│ RAG/Skills │  │ Skills     │  │  모델 선택      │
│            │  │ Lint       │  │                │
│            │  │ MCP        │  │                │
└────────────┘  └────────────┘  └───────┬────────┘
                                        │
                        ┌───────────────▼─────────┐
                        │ Layer 7 — LLM Provider  │
                        │ (vLLM, OpenAI-compat.)  │
                        │ Large(27B) / Small(8B)  │
                        └───────────────┬─────────┘
                                        │
                        ┌───────────────▼─────────┐
                        │ Layer 8 — Infrastructure│
                        │ NVIDIA GPU · Go Binary  │
                        │ On-premise · Air-gapped │
                        └─────────────────────────┘
```

| Layer | 구성 요소 | 역할 |
|-------|----------|------|
| 1 | TUI (Bubble Tea) / WebUI / CLI | 사용자 인터페이스, 세션 관리, 커맨드 팔레트 |
| 2 | App Orchestrator (`app.go`) | 세션·메시지·히스토리·권한 관리 |
| 3 | Agent Loop (`processGeneration`) | LLM 호출 → 응답 파싱 → 도구 실행 반복 루프 |
| 4 | Context Engineering | AGENTS.md 자동 로드, 시스템 프롬프트, Compaction, RAG/Skills |
| 5 | Tools (11종) | 파일 R/W, Bash, Grep/Glob, LSP, Skills, Lint, MCP |
| 6 | Model Router | 태스크 분류 → 최적 모델·엔드포인트 라우팅 |
| 7 | LLM Provider | vLLM OpenAI-compatible API, Large(27B) / Small(8B) |
| 8 | Infrastructure | NVIDIA GPU, Go 바이너리, 온프레미스·에어갭 환경 |

---

## 4. 에이전트 구성

| 에이전트 | 모델 | 용도 | 최대 토큰 |
|---------|------|------|---------|
| `coder` | Qwen3.5-27B (Large) | 코드 생성·편집·분석 | 8,192 |
| `task` | Qwen3.5-8B (Small) | 태스크 분류·계획 | 4,096 |
| `title` | Qwen3.5-8B (Small) | 세션 제목 생성 | 1,024 |
| `summarizer` | Qwen3.5-8B (Small) | 대화 요약 (Compaction) | 4,096 |

> **비고**: 현재 운영 환경(`.secerncode.json`)에서는 모든 에이전트가 Qwen3.5-27B 단일 모델을 사용하며, 설정을 통해 Small 모델로 분리 가능하다.

---

## 5. 기술 스택

| 계층 | 기술 | 버전 | 용도 |
|------|------|------|------|
| 언어 | Go | 1.24 | 단일 바이너리, 크로스 컴파일 |
| CLI | Cobra + Viper | v1.9 / v1.20 | 명령어 파싱 + 설정 관리 |
| TUI | Bubble Tea + Lipgloss | v1.3 | 터미널 대화형 UI |
| HTTP | Go net/http (표준 라이브러리) | — | REST API + SSE 스트리밍 |
| DB | SQLite + sqlc + goose | — | 세션·메시지 영속화 |
| LLM 통신 | openai-go | v0.1.0-beta.2 | vLLM OpenAI-compatible API 호출 |
| MCP | mcp-go | v0.17.0 | 외부 도구 연동 |
| 빌드 자동화 | GoReleaser | — | 릴리스 자동화, 크로스 컴파일 |

---

## 6. 기능 현황

### 6.1 구현 완료 (2026년 3월 말 기준)

> **Stage 매핑**: 아래 Phase 1~4 및 Phase 6은 로드맵([01_roadmap_ko.md](./01_roadmap_ko.md))의 **트랙 2 Stage 0(MVP)** 범위에 해당한다. 상세 구현 설계는 [SecernCode 구현 기획서](../SecernCode/docs/secerncode_implementation_spec_v2.md)를 참조.

| Phase | 기능 | 설명 |
|-------|------|------|
| **Phase 1** | vLLM 연동 | OpenAI-compatible API로 로컬 Qwen3.5-27B 연동 |
| | 코딩 도구 11종 | 파일 읽기/쓰기, bash 실행, grep/glob 검색, LSP 연동, patch, fetch 등 |
| | 단일 바이너리 빌드 | `go build -o secerncode .` → ~50MB |
| **Phase 2** | IntraGenX 브랜딩 | ASCII 로고, 주황색 테마, welcome screen |
| | 시스템 프롬프트 최적화 | 한국어 지원, IntraGenX / SECERN AI 아이덴티티 반영 |
| | 외부 프로바이더 제거 | 외부 프로바이더 10개 삭제 (-3,738줄), 공격 표면 축소 |
| | 설정 파일 독립화 | `.secerncode.json` 완전 분리 |
| **Phase 3** | `/undo`, `/redo` | 세션 내 수정 파일 버전 복원·재적용 |
| | 자동 수정 루프 | 빌드 실패 시 에이전트 자동 오류 분석 → 수정 → 재시도 |
| | AGENTS.md 자동 로드 | 프로젝트별 컨텍스트 파일 자동 주입 |
| | Auto Compact | 대화 길어지면 자동 요약, 컨텍스트 윈도우 초과 방지 |
| | 비대화 모드 | `secerncode -p "프롬프트" -f json` — 스크립트·CI 연동 |
| **Phase 4** | Model Router | 에이전트별 다른 모델·엔드포인트 지정 (coder=27B, 나머지=8B) |
| | config 기반 라우팅 | `.secerncode.json`에서 모델-에이전트 매핑 설정 |
| **Phase 6** | MCP 서버 통합 | 폐쇄망 내부 시스템(DB, Git, Jira 등) 도구 자동 연결 |
| | `/plan` 모드 | 파일 수정 없이 코드 분석 + 구현 계획 제시 (읽기 전용) |
| | Skills 시스템 | 반복 작업을 스킬로 패키징 (예: `skill:egov-crud`) |
| | 커스텀 커맨드 | `.secerncode/commands/` 폴더에 마크다운으로 정의 |
| | 멀티세션 병렬 실행 | 세마포어 기반 동시성 제어, GPU 과부하 방지 |
| | WebUI | 브라우저 기반 채팅 UI, REST API + SSE 실시간 스트리밍, 코드 diff 표시 |
| **성능 최적화** | 읽기 전용 도구 병렬 실행 | grep/glob/view 등 파일 수정 없는 도구를 동시 실행하여 응답 속도 개선 |
| | 토큰 기반 히스토리 트리밍 | 대화 기록을 토큰 수 기준으로 자동 정리, 컨텍스트 윈도우 효율 극대화 |
| | vLLM CUDA Graph 최적화 | `--enforce-eager` 제거 + prefix caching 적용 → 응답 속도 **6.9~7.3배** 개선 |

### 6.2 진행 중 / 예정

> **Stage 매핑**: Phase 5(eGovFrame RAG)는 로드맵 상 **Stage 1** 범위에 해당한다.

| Phase | 항목 | 상태 | 설명 |
|-------|------|------|------|
| Phase 5 | eGovFrame RAG | 진행 중 | 팀원 별도 RAG 구축 중, 완성 후 통합 예정 |
| — | 세션 공유 | 예정 | WebUI에서 대화 내역 공유 링크 생성 |

---

## 7. 인프라 요구사항

| 항목 | 요구사항 |
|------|---------|
| GPU | NVIDIA A100/H100 (VRAM 64GB 이상 권장) |
| LLM 서버 | vLLM >= 0.6.0 |
| 네트워크 | 폐쇄망 내부 통신만 (외부 인터넷 불필요) |
| 클라이언트 | Go 바이너리 단일 파일 (~50MB), OS만 맞으면 실행 가능 |
| 설정 | `LOCAL_ENDPOINT` 환경변수 또는 `.secerncode.json` |

### 설정 예시

```json
{
  "providers": {
    "local": {
      "apiKey": "dummy",
      "endpoint": "http://gpu-server:8000/v1"
    }
  },
  "models": {
    "large": {
      "endpoint": "http://gpu-server:8000/v1",
      "apiModel": "Qwen/Qwen3.5-27B",
      "name": "SECERN-Coder",
      "maxTokens": 8192,
      "contextWindow": 262144
    },
    "small": {
      "endpoint": "http://gpu-server:8001/v1",
      "apiModel": "Qwen/Qwen3.5-8B",
      "name": "SECERN-Light",
      "maxTokens": 4096,
      "contextWindow": 32768
    }
  },
  "agents": {
    "coder":      { "model": "local.large", "maxTokens": 8192 },
    "task":       { "model": "local.small", "maxTokens": 4096 },
    "title":      { "model": "local.small", "maxTokens": 1024 },
    "summarizer": { "model": "local.small", "maxTokens": 4096 }
  },
  "maxConcurrentSessions": 3
}
```

---

## 8. Track 1과의 관계

| 항목 | Track 1 (IntraGenX / Coco Engine) | Track 2 (SecernCode) |
|------|----------------------------------|---------------------|
| 접근 방식 | Spec-Driven 일괄 코드 생성, Top-Down | 자율형 CLI 에이전트, Bottom-Up |
| 주 사용자 | SI 프로젝트 PM·설계자 | 개발자 개인 |
| 구현 언어 | TypeScript (Rust 엔진 예정) | Go |
| 실행 환경 | Coco Studio (브라우저) + Eclipse 플러그인 | 터미널 / 브라우저 |
| 주도 조직 | 대보DX + 시선AI | 시선AI |

### 공유 요소

- 온프레미스 sLLM (vLLM + Qwen3.5)
- UASL 코드 표준 및 RBAC 인터페이스 (향후 통합)
- 감사 추적 아키텍처
- MCP 프로토콜 (동일 표준, 용도 상이)

> **MCP 용도 구분**: Track 1에서는 코드 생성 엔진 서버(xframe5-compiler 등)를 MCP로 노출하고, Track 2에서는 개발 도구 접근 서버(Jira, Confluence, 내부 DB 등)를 MCP로 연결한다.

---

## 9. 경쟁 우위 요약

| 항목 | SecernCode | 경쟁 제품 (Claude Code, Cursor 등) |
|------|-----------|----------------------------------|
| 네트워크 | 완전 오프라인 (폐쇄망) | 외부 API 필수 |
| 배포 | Go 단일 바이너리, USB 복사 | 설치 + 런타임 + 패키지 관리 필요 |
| 모델 | 로컬 vLLM + 공개 모델 | 상용 API (Claude, GPT 등) |
| eGovFrame | 네이티브 지원 예정 | 미지원 |
| 비용 구조 | 온프레미스 GPU 1회 투자 | 토큰당 과금 |
| 보안 | 코드 외부 유출 원천 차단 | 클라우드로 코드 전송 |

---

## 변경이력

| 버전 | 일자 | 변경 내용 | 작성자 |
|------|------|----------|--------|
| 1.0 | 2026-03-26 | 초안 작성 | 분석팀 |
| 1.1 | 2026-03-26 | 성능 최적화 기능 3건 추가 (병렬 도구 실행, 토큰 트리밍, CUDA Graph) | 분석팀 |
| 1.2 | 2026-03-31 | Stage/Phase 용어 매핑 주석 추가 (Stage 0 = Phase 1~6, Stage 1 = Phase 5), 로드맵·구현 기획서 교차 참조 추가 | PM (주용수) |
