# OpenCode 심층 기술 분석

| 항목 | 내용 |
|------|------|
| **문서번호** | SAI-KB-2026-004 |
| **작성일** | 2026년 3월 23일 |
| **버전** | v1.0 |
| **보안등급** | 일반 |
| **작성** | Secern AI |
| **분석 대상 버전** | v1.3.0 (커밋 기준) |

---

> **TL;DR**
> - OpenCode는 anomaly.co가 개발한 **100% 오픈소스(MIT), 프로바이더 중립 AI 코딩 에이전트**로, Claude Code의 오픈소스 대안을 지향한다
> - Vercel AI SDK 기반 20+ LLM 프로바이더 지원, MCP 프로토콜 통합, 37개 언어의 LSP 자동 연결로 코드 인텔리전스 제공
> - 클라이언트/서버 분리 아키텍처 — CLI/TUI/웹/데스크톱(Tauri+Electron) 다중 프론트엔드를 하나의 Hono 기반 HTTP API 서버가 지원
> - Effect 라이브러리 기반 함수형 프로그래밍, Drizzle ORM + SQLite 영속 계층, Turborepo + Bun 모노레포 구조
> - IntraGenX 트랙 2 코딩 에이전트의 기반 프로젝트로, MCP 서버 확장 + 로컬 LLM 프로바이더 설정으로 온프레미스 통합 가능
>
> **대상 독자**: 개발팀, 아키텍트 | **소요 시간**: 40~60분

---

## 1. 프로젝트 개요

### 1.1 목적과 배경

OpenCode는 [anomaly.co](https://anomalyco.com) (terminal.shop 개발사)가 만든 **오픈소스 AI 코딩 에이전트**다. Claude Code, Cursor 등 상용 AI 코딩 도구의 오픈소스 대안으로 포지셔닝하며, 특정 LLM 프로바이더에 종속되지 않는 **프로바이더 중립** 설계를 핵심 철학으로 한다. MIT 라이선스로 상업적 사용, 수정, 재배포가 자유롭다.

### 1.2 핵심 수치

| 항목 | 수치 |
|------|------|
| 버전 | v1.3.0 |
| TypeScript 파일 수 (opencode 패키지) | 327개 |
| TypeScript 파일 수 (전체 모노레포) | 1,263개 |
| 모노레포 패키지 수 | 19개 (packages/ 하위) |
| 지원 AI 프로바이더 | 20+ (Anthropic, OpenAI, Google, AWS Bedrock, Azure, xAI, Groq, Mistral, OpenRouter 등) |
| 내장 LSP 서버 | 37개 언어 |
| 내장 도구(Tool) | 20개 (bash, read, edit, write, glob, grep, webfetch, websearch, codesearch, lsp, multiedit, plan, question, task, todo, skill, ls, batch, apply_patch, external-directory) |
| 에이전트 타입 | 7개 (build, plan, general, explore, compaction, title, summary) |
| 패키지 매니저 | Bun 1.3.11 |
| 빌드 시스템 | Turborepo 2.8.13 |
| 데이터베이스 | SQLite (Drizzle ORM) |

### 1.3 경쟁 제품 대비 차별점

| 비교 항목 | OpenCode | Claude Code | Cursor | Aider | Cline |
|-----------|----------|-------------|--------|-------|-------|
| 라이선스 | MIT (100% 오픈소스) | 상용 | 상용 | Apache 2.0 | Apache 2.0 |
| 프로바이더 | 20+ 멀티프로바이더 | Anthropic 전용 | OpenAI 중심 | 멀티프로바이더 | 멀티프로바이더 |
| UI | TUI + 웹 + 데스크톱 | CLI | IDE 통합 | CLI | VS Code 확장 |
| LSP 통합 | 37개 언어 내장 | 없음 | IDE 활용 | 없음 | VS Code 활용 |
| MCP 지원 | 클라이언트 + OAuth | 서버/클라이언트 | 제한적 | 없음 | MCP 클라이언트 |
| 클라이언트/서버 분리 | O (원격 제어 가능) | X | X | X | X |
| ACP 지원 | O | X | X | X | X |
| 데스크톱 앱 | Tauri + Electron | X | Electron | X | X |

### 1.4 포지셔닝

OpenCode의 핵심 포지셔닝은 다음 세 가지다:

1. **100% 오픈소스**: 코어부터 UI까지 전체 소스코드 공개 (MIT)
2. **프로바이더 중립**: 모델 발전에 따라 프로바이더 간 격차가 줄어들고 가격이 하락할 것이라는 전제 하에, 특정 벤더 종속 없이 자유롭게 전환 가능
3. **TUI 퍼스트**: neovim 사용자와 terminal.shop 제작진이 만든 프로젝트답게 터미널 UI를 최우선으로 설계하되, 웹/데스크톱 등 다양한 클라이언트를 지원하는 클라이언트/서버 아키텍처 채택

---

## 2. 아키텍처 심층 분석

### 2.1 전체 아키텍처 다이어그램

```
┌─────────────────────────────────────────────────────────────────────┐
│                        클라이언트 레이어                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────────────┐  │
│  │ TUI/CLI  │  │  웹 앱   │  │ Tauri    │  │ Electron 데스크톱  │  │
│  │(console) │  │  (app)   │  │(desktop) │  │(desktop-electron)  │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────────┬───────────┘  │
│       │              │             │                  │              │
│       └──────────────┴─────────────┴──────────────────┘              │
│                              │                                       │
│                    HTTP API / WebSocket / SSE                        │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
┌─────────────────────────────┴───────────────────────────────────────┐
│                     서버 레이어 (Hono HTTP)                          │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    Server (server.ts)                         │  │
│  │  /session  /project  /provider  /mcp  /config  /event  /tui  │  │
│  └───────────────────────────┬───────────────────────────────────┘  │
│                              │                                       │
│  ┌───────────┐  ┌────────────┴──────────┐  ┌──────────────────┐    │
│  │  Session   │  │    Agent 실행 엔진     │  │   Tool Registry  │    │
│  │  Manager   │  │  (processor.ts)       │  │  (20개 내장 도구)  │    │
│  └─────┬─────┘  └──────────┬────────────┘  └────────┬─────────┘    │
│        │                   │                         │              │
│  ┌─────┴─────────┐  ┌─────┴──────────┐  ┌──────────┴──────────┐  │
│  │ SQLite/Drizzle │  │  LLM Streaming  │  │   MCP Client       │  │
│  │ (세션/메시지    │  │  (ai SDK)       │  │   Manager          │  │
│  │  영속 계층)     │  │                 │  │                    │  │
│  └───────────────┘  └────────┬────────┘  └──────────┬──────────┘  │
│                              │                       │              │
│                   ┌──────────┴──────────┐            │              │
│                   │  Provider Abstraction│            │              │
│                   │  (20+ AI SDK 프로바이더)│           │              │
│                   └──────────┬──────────┘            │              │
└──────────────────────────────┼───────────────────────┼──────────────┘
                               │                       │
                    ┌──────────┴──────────┐  ┌────────┴──────────┐
                    │   LLM APIs          │  │  외부 MCP 서버     │
                    │ (Anthropic, OpenAI,  │  │  (stdio/HTTP)     │
                    │  Google, 로컬 등)    │  │                   │
                    └─────────────────────┘  └───────────────────┘

                    ┌─────────────────────┐
                    │   LSP 서버들         │
                    │ (37개 언어 자동 연결) │
                    └─────────────────────┘
```

### 2.2 모노레포 패키지 관계도

```
opencode (루트)
├── packages/opencode ──────── 핵심 CLI 엔진 (이 프로젝트의 코어)
│   ├── depends on: @opencode-ai/plugin, @opencode-ai/sdk, @opencode-ai/util
│   ├── depends on: ai (Vercel AI SDK), @ai-sdk/* (20+ 프로바이더)
│   ├── depends on: @modelcontextprotocol/sdk, drizzle-orm, effect
│   └── depends on: @agentclientprotocol/sdk (ACP)
│
├── packages/app ───────────── SolidJS 웹 프론트엔드
│   ├── depends on: @opencode-ai/sdk, @opencode-ai/ui, @opencode-ai/util
│   └── depends on: solid-js, @tanstack/solid-query, virtua
│
├── packages/desktop ───────── Tauri 데스크톱 앱
│   ├── depends on: @opencode-ai/app (웹 앱 재사용)
│   └── depends on: @tauri-apps/* (Tauri 플러그인)
│
├── packages/desktop-electron ─ Electron 데스크톱 앱
│   ├── depends on: @opencode-ai/app (웹 앱 재사용)
│   └── depends on: electron, tree-kill
│
├── packages/sdk ───────────── JavaScript SDK (클라이언트/서버)
│   └── OpenAPI 기반 자동 생성 클라이언트
│
├── packages/plugin ────────── 플러그인 인터페이스 정의
│   └── depends on: @opencode-ai/sdk, zod
│
├── packages/ui ────────────── 공유 UI 컴포넌트 라이브러리
├── packages/util ──────────── 공유 유틸리티
├── packages/web ───────────── 랜딩 페이지/마케팅 사이트
├── packages/console ───────── 터미널 UI (SolidJS 기반)
├── packages/enterprise ────── 엔터프라이즈 기능
├── packages/storybook ─────── UI 컴포넌트 문서
├── packages/function ──────── 서버리스 함수
└── packages/containers ────── Docker 컨테이너 빌드
```

### 2.3 클라이언트/서버 아키텍처

OpenCode의 가장 독특한 아키텍처 특징은 **클라이언트/서버 분리**다. 핵심 로직이 Hono 기반 HTTP 서버로 동작하며, TUI/웹/데스크톱은 이 서버의 클라이언트에 불과하다.

**서버 (`packages/opencode/src/server/server.ts`)**:
- Hono 프레임워크 기반 HTTP API 서버
- `Bun.serve()`로 구동, WebSocket 지원
- OpenAPI 3.1.1 스펙 자동 생성 (`hono-openapi`)
- CORS, Basic Auth, mDNS 서비스 디스커버리 지원
- 라우트 구조: `/session`, `/project`, `/provider`, `/mcp`, `/config`, `/event`, `/tui`, `/pty`, `/file`, `/permission`, `/question`, `/global`

**클라이언트 통신**:
- SSE (Server-Sent Events)를 통한 실시간 스트리밍
- WebSocket을 통한 PTY(터미널) 세션
- REST API를 통한 CRUD 작업
- `@opencode-ai/sdk`가 타입 안전한 클라이언트 라이브러리 제공

이 구조 덕분에 **모바일 앱에서 로컬 PC의 OpenCode를 원격 제어**하는 시나리오가 가능하다.

### 2.4 요청 흐름 추적

사용자 입력부터 응답까지의 전체 흐름:

```
1. 사용자 입력
   └─ CLI: yargs 파싱 → RunCommand
   └─ 웹/데스크톱: SDK 클라이언트 → HTTP API

2. 세션 관리 (packages/opencode/src/session/index.ts)
   ├─ Session.create() / Session.chat()
   ├─ MessageV2.User 생성 → DB 저장
   └─ SessionProcessor.create() 호출

3. Agent 실행 루프 (packages/opencode/src/session/processor.ts)
   ├─ while(true) 루프 시작
   │   ├─ LLM.stream() 호출 → AI SDK streamText()
   │   ├─ fullStream 이벤트 순회:
   │   │   ├─ reasoning-start/delta/end → 추론 과정 저장
   │   │   ├─ text-start/delta/end → 텍스트 응답 저장
   │   │   ├─ tool-call → 도구 실행 (Permission 체크 포함)
   │   │   ├─ tool-result → 결과 저장
   │   │   ├─ step-finish → 토큰 사용량/비용 계산
   │   │   └─ error → 재시도 또는 에러 보고
   │   ├─ Snapshot.track() → git 스냅샷 추적
   │   └─ 컴팩션 필요 여부 체크
   ├─ "continue" → 다음 도구 호출 루프
   ├─ "compact" → 컨텍스트 윈도우 압축 후 재시도
   └─ "stop" → 최종 응답 반환

4. LLM 호출 (packages/opencode/src/session/llm.ts)
   ├─ Provider.getLanguage() → AI SDK LanguageModel 획득
   ├─ SystemPrompt 구성 (모델별 프롬프트 선택)
   ├─ Permission 기반 도구 필터링
   ├─ Plugin.trigger("chat.params") → 플러그인 파라미터 변환
   └─ streamText() → Vercel AI SDK 스트리밍 호출

5. 도구 실행 (packages/opencode/src/tool/*.ts)
   ├─ ToolRegistry.tools() → 활성 도구 목록
   ├─ Permission.ask() → 사용자 허가 요청 (필요시)
   ├─ tool.execute() → 실제 도구 실행
   └─ Truncate.output() → 출력 크기 제한

6. 응답 저장
   ├─ MessageV2.Part 단위로 DB 저장
   ├─ Bus.publish() → SSE를 통해 클라이언트에 실시간 전달
   └─ SessionSummary.summarize() → 세션 요약 비동기 생성
```

### 2.5 Effect 라이브러리 기반 함수형 프로그래밍

OpenCode는 TypeScript 함수형 프로그래밍 라이브러리인 [Effect](https://effect.website)를 상태 관리와 서비스 계층에 활용한다.

**사용 패턴**:
- `ServiceMap.Service` — 서비스 인터페이스 정의 (`ToolRegistry.Service`, `Plugin.Service`)
- `Layer.effect` — 서비스 구현의 의존성 주입
- `Effect.gen` / `Effect.fn` — 제너레이터 기반 이펙트 체인
- `InstanceState.make` — 프로젝트 인스턴스별 상태 관리 (초기화/정리 라이프사이클)
- `Effect.acquireRelease` — 리소스 관리 (구독 해제 등)

**핵심 파일**:
- `packages/opencode/src/effect/instance-state.ts` — 인스턴스 상태 관리
- `packages/opencode/src/effect/run-service.ts` — Effect를 Promise로 변환하는 브릿지
- `packages/opencode/src/effect/instance-registry.ts` — 인스턴스 레지스트리

다만 프로젝트 전체가 Effect를 사용하지는 않으며, 대부분의 코드는 일반적인 async/await + namespace 패턴으로 작성되어 있다. Effect는 주로 플러그인 시스템과 도구 레지스트리 등 서비스 계층에서 의존성 주입/라이프사이클 관리 용도로 제한적으로 사용된다.

---

## 3. 코드베이스 상세 구조

### 3.1 전체 디렉토리 트리

```
opencode/
├── packages/
│   ├── opencode/           # 핵심 CLI 엔진 (270 TS 파일)
│   │   ├── bin/            # 실행 바이너리 엔트리
│   │   ├── migration/      # Drizzle DB 마이그레이션
│   │   ├── src/
│   │   │   ├── index.ts    # CLI 엔트리포인트 (yargs)
│   │   │   ├── agent/      # 에이전트 정의 (build/plan/general/explore)
│   │   │   ├── acp/        # Agent Communication Protocol
│   │   │   ├── cli/        # CLI 커맨드 및 TUI
│   │   │   ├── config/     # 설정 관리 (opencode.json)
│   │   │   ├── lsp/        # Language Server Protocol 클라이언트
│   │   │   ├── mcp/        # Model Context Protocol 클라이언트
│   │   │   ├── plugin/     # 플러그인 시스템
│   │   │   ├── provider/   # AI 프로바이더 추상화
│   │   │   ├── server/     # Hono HTTP API 서버
│   │   │   ├── session/    # 세션/대화/메시지 관리
│   │   │   ├── storage/    # Drizzle ORM + SQLite
│   │   │   ├── tool/       # 내장 도구 (bash, edit, read 등)
│   │   │   ├── permission/ # 권한 제어 시스템
│   │   │   ├── project/    # 프로젝트 인스턴스 관리
│   │   │   ├── snapshot/   # git 스냅샷 추적
│   │   │   ├── skill/      # 스킬 디스커버리
│   │   │   ├── shell/      # 셸 실행 환경
│   │   │   ├── file/       # 파일 감시/무시 규칙
│   │   │   ├── effect/     # Effect 라이브러리 통합
│   │   │   └── util/       # 유틸리티 (git, log, hash 등)
│   │   └── test/           # 테스트
│   ├── app/                # SolidJS 웹 프론트엔드
│   │   ├── src/            # 컴포넌트, 라우트, 스타일
│   │   ├── e2e/            # Playwright E2E 테스트
│   │   └── public/         # 정적 에셋
│   ├── console/            # SolidStart 기반 콘솔 (opencode.ai)
│   ├── desktop/            # Tauri 네이티브 데스크톱 앱
│   │   └── src-tauri/      # Rust 사이드카
│   ├── desktop-electron/   # Electron 데스크톱 앱
│   │   └── src/            # main/preload/renderer
│   ├── sdk/js/             # JavaScript SDK
│   ├── plugin/             # 플러그인 타입 정의
│   ├── ui/                 # 공유 UI 컴포넌트
│   ├── util/               # 공유 유틸리티
│   ├── web/                # 마케팅/랜딩 페이지
│   ├── enterprise/         # 엔터프라이즈 기능
│   ├── storybook/          # Storybook UI 문서
│   ├── containers/         # Docker 빌드 스크립트
│   ├── function/           # 서버리스 함수
│   ├── slack/              # Slack 통합
│   └── script/             # 공유 빌드 스크립트
├── sdks/
│   └── vscode/             # VS Code 확장
├── specs/                  # OpenAPI 스펙
├── patches/                # npm 패치 파일
├── infra/                  # 인프라 설정
└── nix/                    # Nix 빌드
```

### 3.2 핵심 패키지 상세

#### 3.2.1 packages/opencode — CLI 엔진 (핵심)

프로젝트의 심장부. v1.3.0 기준 327개 TypeScript 파일로 구성된다.

**엔트리포인트 (`src/index.ts`)**:
- yargs 기반 CLI 파서
- 23개 서브커맨드 등록 (run, serve, mcp, agent, generate, pr, debug, console, attach, tui-thread, workspace-serve 등)
- DB 마이그레이션 미들웨어 (JSON → SQLite 원타임 마이그레이션)
- 로그 초기화, 환경변수 설정 (`AGENT=1`, `OPENCODE=1`)

**주요 모듈**:

| 모듈 | 파일 수 | 역할 |
|------|--------|------|
| `agent/` | 1 | 에이전트 정의 (build, plan, general, explore, compaction, title, summary) |
| `session/` | 15 | 세션 라이프사이클, LLM 스트리밍, 메시지 처리, 컴팩션, 재시도 |
| `tool/` | 26 | 내장 도구 정의 및 레지스트리 |
| `provider/` | 7+ | AI SDK 프로바이더 추상화, 모델 관리 |
| `server/` | 6+ | Hono HTTP API 라우트 |
| `mcp/` | 4 | MCP 클라이언트 관리, OAuth 인증 |
| `lsp/` | 5 | LSP 클라이언트/서버 관리 |
| `config/` | 6 | 설정 로딩 (JSON/JSONC), 마크다운 인스트럭션 |
| `storage/` | 5 | Drizzle ORM, SQLite, JSON 마이그레이션 |
| `plugin/` | 3 | 플러그인 로딩 (Codex, Copilot, GitLab 내장) |
| `cli/` | 21+ | CLI 커맨드, TUI, 부트스트랩 |
| `permission/` | 4 | 도구 실행 권한 체계 |
| `util/` | 25+ | 유틸리티 (git, log, hash, process, glob 등) |

#### 3.2.2 packages/app — SolidJS 웹 프론트엔드

SolidJS + Vite 기반 웹 애플리케이션. 데스크톱 앱(Tauri, Electron) 모두 이 패키지를 재사용한다.

- **프레임워크**: SolidJS 1.9.10 + @solidjs/router
- **상태 관리**: @tanstack/solid-query (서버 상태)
- **UI**: @kobalte/core (헤드리스 컴포넌트), TailwindCSS 4.x
- **코드 하이라이팅**: Shiki
- **가상 스크롤**: virtua
- **터미널 에뮬레이터**: ghostty-web (Ghostty 터미널의 웹 포트)
- **E2E 테스트**: Playwright

#### 3.2.3 packages/console — 터미널 콘솔 (opencode.ai)

SolidStart 기반 웹 콘솔. opencode.ai 웹사이트의 대시보드/관리 인터페이스 역할을 한다. 이메일 템플릿, 리소스 관리 등 SaaS 운영 기능 포함.

#### 3.2.4 packages/sdk — JavaScript SDK

OpenCode 서버 API에 대한 타입 안전한 클라이언트 라이브러리.

- **클라이언트**: `createOpencodeClient()` — fetch 기반 HTTP 클라이언트
- **서버**: 서버사이드 유틸리티
- **v2 API**: 최신 API 버전, OpenAPI 스펙에서 자동 생성 (`@hey-api/openapi-ts`)
- **빌드**: `bun ./script/build.ts`

#### 3.2.5 packages/desktop — Tauri 데스크톱 앱

Tauri 2.x 기반 네이티브 데스크톱 앱. `packages/app` 웹 앱을 WebView로 렌더링하며, 사이드카 프로세스로 OpenCode 서버를 실행한다.

- **Tauri 플러그인**: clipboard, deep-link, dialog, shell, store, updater, window-state, notification, process
- **플랫폼**: macOS (Apple Silicon/Intel), Windows, Linux

#### 3.2.6 packages/desktop-electron — Electron 데스크톱 앱

Electron 40.x 기반 대안 데스크톱 앱. Tauri와 동일하게 `packages/app`을 재사용한다.

- **빌드**: electron-vite + electron-builder
- **사이드카**: OpenCode 바이너리를 자식 프로세스로 관리, `tree-kill`로 프로세스 트리 정리
- **자동 업데이트**: electron-updater
- **플랫폼**: macOS, Windows, Linux (.deb, .rpm, AppImage)

#### 3.2.7 packages/plugin — 플러그인 시스템

플러그인 인터페이스를 정의하는 타입 패키지.

- `Plugin` 타입: `(input: PluginInput) => Promise<Hooks>`
- `PluginInput`: SDK 클라이언트, 프로젝트 정보, 디렉토리, 서버 URL, Bun 셸 접근
- `Hooks`: 다양한 라이프사이클 훅 정의
- `ToolDefinition`: 커스텀 도구 정의 인터페이스

### 3.3 모노레포 빌드 파이프라인

```
Bun (패키지 매니저 + 런타임)
  └─ Turborepo (태스크 오케스트레이션)
       ├─ typecheck → tsgo --noEmit (TypeScript Native Preview)
       ├─ build → 패키지별 빌드 (vite, tsc, electron-vite 등)
       └─ test → bun test (패키지 디렉토리에서 실행)

빌드 의존성:
  - opencode#test → ^build (의존 패키지 빌드 후 테스트)
  - @opencode-ai/app#test → ^build
```

**주요 빌드 도구**:
- **Bun 1.3.11**: 패키지 매니저 + 런타임 + 번들러
- **Turborepo 2.8.13**: 모노레포 빌드 오케스트레이션
- **TypeScript Native Preview (tsgo)**: 네이티브 Go 기반 타입체커 (실험적)
- **Vite 7.x**: 웹 앱 빌드
- **electron-vite**: Electron 앱 빌드

---

## 4. 핵심 기술 메커니즘

### 4.1 Agent 실행 루프

**파일**: `packages/opencode/src/agent/agent.ts`, `packages/opencode/src/session/processor.ts`

#### 에이전트 타입

| 에이전트 | 모드 | 역할 | 권한 |
|---------|------|------|------|
| `build` | primary | 기본 개발 에이전트 | 전체 도구 접근 (edit, write, bash 등) |
| `plan` | primary | 분석/계획 전용 | 읽기 전용, edit 거부, .opencode/plans/ 에만 쓰기 허용 |
| `general` | subagent | 복잡한 검색, 멀티스텝 작업 | 전체 접근 (todoread/todowrite 거부) |
| `explore` | subagent | 빠른 코드베이스 탐색 | grep, glob, list, bash, read, webfetch, websearch, codesearch만 허용 |
| `compaction` | primary (hidden) | 컨텍스트 윈도우 압축 | 도구 없음 |
| `title` | primary (hidden) | 세션 제목 생성 | 도구 없음 |
| `summary` | primary (hidden) | 세션 요약 생성 | 도구 없음 |

에이전트는 `Agent.Info` Zod 스키마로 정의되며, 설정 파일(`opencode.json`)에서 커스텀 에이전트를 추가하거나 기존 에이전트를 수정/비활성화할 수 있다.

#### 도구 호출 체인

`SessionProcessor.create()`가 반환하는 `process()` 함수가 에이전트 루프의 핵심이다.

```typescript
// packages/opencode/src/session/processor.ts — 핵심 루프 구조
while (true) {
  const stream = await LLM.stream(streamInput)
  for await (const value of stream.fullStream) {
    switch (value.type) {
      case "tool-call":
        // 둠 루프 감지: 동일 도구+입력이 3회 연속이면 사용자에게 확인
        // Permission.ask() 호출
        break
      case "tool-result":
        // 도구 결과 DB 저장, 메타데이터 업데이트
        break
      case "finish-step":
        // 토큰 사용량 계산, 스냅샷 패치 생성
        // 컨텍스트 오버플로우 체크 → 컴팩션 트리거
        break
    }
  }
  // 반환값: "continue" | "compact" | "stop"
}
```

#### 컨텍스트 윈도우 관리

`SessionCompaction` 네임스페이스 (`packages/opencode/src/session/compaction.ts`)가 담당한다.

- **오버플로우 감지**: 총 토큰 수가 모델의 `limit.input - reserved`를 초과하면 컴팩션 트리거
- **프루닝**: 최근 40,000 토큰 분량의 도구 호출은 보존, 이전 도구 호출의 출력은 삭제
- **컴팩션 에이전트**: `compaction` 에이전트가 대화 히스토리를 요약, 새 세션으로 전환
- **보호 도구**: `skill` 도구 출력은 프루닝에서 보호

#### 대화 히스토리

`MessageV2` 네임스페이스 (`packages/opencode/src/session/message-v2.ts`)가 메시지 구조를 정의한다. 메시지는 Part 단위로 분할 저장된다:

- `TextPart` — 텍스트 응답
- `ReasoningPart` — 추론 과정 (extended thinking)
- `ToolPart` — 도구 호출 (pending → running → completed/error)
- `StepStartPart` / `StepFinishPart` — LLM 호출 단계 경계
- `PatchPart` — 파일 변경 스냅샷
- `FilePart` — 첨부 파일

### 4.2 MCP 통합

**파일**: `packages/opencode/src/mcp/index.ts`, `packages/opencode/src/mcp/auth.ts`, `packages/opencode/src/mcp/oauth-provider.ts`, `packages/opencode/src/mcp/oauth-callback.ts`

#### MCP SDK 사용 패턴

`@modelcontextprotocol/sdk` v1.25.2를 사용하며, OpenCode는 **MCP 클라이언트** 역할을 한다.

```typescript
// MCP 클라이언트 생성 패턴 (packages/opencode/src/mcp/index.ts)
import { Client } from "@modelcontextprotocol/sdk/client/index.js"
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js"
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js"
import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js"
```

#### MCP 서버 연결 관리

`MCP` 네임스페이스의 `Instance.state()`로 프로젝트별 MCP 클라이언트 풀을 관리한다.

**지원 트랜스포트**:
1. **stdio** (`type: "local"`) — 로컬 프로세스 실행, `StdioClientTransport`
2. **StreamableHTTP** (`type: "remote"`) — HTTP 기반, `StreamableHTTPClientTransport` 우선 시도
3. **SSE** (`type: "remote"`) — StreamableHTTP 실패시 폴백, `SSEClientTransport`

**연결 흐름**:
1. `Config.get()` → `mcp` 설정 로드
2. `MCP.create()` → 트랜스포트 생성, 클라이언트 연결, `listTools()` 호출
3. 연결 실패시 `status: "failed"`, OAuth 필요시 `status: "needs_auth"`
4. 연결 성공시 `registerNotificationHandlers()` — `ToolListChangedNotification` 구독

**OAuth 인증 흐름**:
1. `MCP.startAuth()` → `McpOAuthProvider` 생성, 인증 URL 획득
2. `MCP.authenticate()` → 브라우저 열기, `McpOAuthCallback` 서버에서 콜백 대기
3. `MCP.finishAuth()` → 인증 코드로 토큰 교환, 클라이언트 재연결
4. `McpAuth` — 토큰 영속 저장 (opencode 데이터 디렉토리)

#### 도구/리소스/프롬프트 등록

```typescript
// MCP 도구를 AI SDK Tool로 변환
async function convertMcpTool(mcpTool: MCPToolDef, client: MCPClient): Promise<Tool> {
  return dynamicTool({
    description: mcpTool.description ?? "",
    inputSchema: jsonSchema(schema),
    execute: async (args) => client.callTool({ name: mcpTool.name, arguments: args }),
  })
}
```

- `MCP.tools()` — 모든 연결된 MCP 서버의 도구를 `{serverName}_{toolName}` 키로 병합
- `MCP.prompts()` — MCP 서버 프롬프트 조회 (`{serverName}:{promptName}`)
- `MCP.resources()` — MCP 서버 리소스 조회

### 4.3 LSP 통합

**파일**: `packages/opencode/src/lsp/index.ts`, `packages/opencode/src/lsp/server.ts`, `packages/opencode/src/lsp/client.ts`, `packages/opencode/src/lsp/launch.ts`, `packages/opencode/src/lsp/language.ts`

#### LSP 서버 목록 (37개 언어)

| LSP 서버 | 지원 언어/확장자 |
|----------|----------------|
| Deno | .ts, .tsx, .js, .jsx, .mjs |
| Typescript | .ts, .tsx, .js, .jsx, .mjs |
| Vue | .vue |
| ESLint | .ts, .tsx, .js, .jsx, .vue, .svelte |
| Oxlint | .ts, .tsx, .js, .jsx |
| Biome | .ts, .tsx, .js, .jsx, .json, .jsonc |
| Gopls | .go |
| Rubocop | .rb |
| Ty | .py (실험적, `OPENCODE_EXPERIMENTAL_LSP_TY`) |
| Pyright | .py |
| ElixirLS | .ex, .exs |
| Zls | .zig |
| CSharp | .cs |
| FSharp | .fs, .fsx |
| SourceKit | .swift |
| RustAnalyzer | .rs |
| Clangd | .c, .cpp, .cc, .h, .hpp |
| Svelte | .svelte |
| Astro | .astro |
| JDTLS | .java |
| KotlinLS | .kt, .kts |
| YamlLS | .yml, .yaml |
| LuaLS | .lua |
| PHPIntelephense | .php |
| Prisma | .prisma |
| Dart | .dart |
| Ocaml | .ml, .mli |
| BashLS | .sh, .bash |
| TerraformLS | .tf |
| TexLab | .tex |
| DockerfileLS | Dockerfile |
| Gleam | .gleam |
| Clojure | .clj, .cljs |
| Nixd | .nix |
| Tinymist | .typ |
| HLS | .hs |
| JuliaLS | .jl |

#### LSP 클라이언트 구현

`LSP` 네임스페이스가 파일 확장자 기반으로 적절한 LSP 서버를 자동 스폰하고, `vscode-jsonrpc` 프로토콜로 통신한다.

**지원 LSP 기능**:
- `textDocument/hover` — 심볼 정보
- `textDocument/definition` — 정의로 이동
- `textDocument/references` — 참조 검색
- `textDocument/implementation` — 구현체 검색
- `workspace/symbol` — 워크스페이스 심볼 검색
- `textDocument/documentSymbol` — 문서 심볼
- `textDocument/prepareCallHierarchy` — 호출 계층
- `callHierarchy/incomingCalls` / `outgoingCalls` — 들어오는/나가는 호출
- 진단(Diagnostics) 수집

**자동 관리**: 파일 터치시 LSP 서버가 없으면 자동 스폰하고, 한번 실패한 서버는 `broken` 셋에 기록하여 재시도하지 않는다. 프로젝트별로 Root를 자동 감지한다 (tsconfig.json, go.mod, Cargo.toml 등 탐색).

### 4.4 AI SDK 멀티프로바이더

**파일**: `packages/opencode/src/provider/provider.ts`, `packages/opencode/src/provider/transform.ts`, `packages/opencode/src/provider/schema.ts`

#### Vercel AI SDK 추상화

`ai` (Vercel AI SDK) 5.0.x를 핵심 LLM 추상화 계층으로 사용한다. `Provider` 네임스페이스가 20+ 프로바이더를 통합 관리한다.

**번들된 프로바이더 목록**:

| 패키지 | 프로바이더 |
|--------|-----------|
| `@ai-sdk/anthropic` | Anthropic (Claude) |
| `@ai-sdk/openai` | OpenAI (GPT) |
| `@ai-sdk/google` | Google AI (Gemini) |
| `@ai-sdk/google-vertex` | Google Vertex AI |
| `@ai-sdk/google-vertex/anthropic` | Vertex AI Anthropic |
| `@ai-sdk/amazon-bedrock` | AWS Bedrock |
| `@ai-sdk/azure` | Azure OpenAI |
| `@ai-sdk/xai` | xAI (Grok) |
| `@ai-sdk/groq` | Groq |
| `@ai-sdk/mistral` | Mistral |
| `@ai-sdk/deepinfra` | DeepInfra |
| `@ai-sdk/cerebras` | Cerebras |
| `@ai-sdk/cohere` | Cohere |
| `@ai-sdk/gateway` | AI Gateway |
| `@ai-sdk/togetherai` | Together AI |
| `@ai-sdk/perplexity` | Perplexity |
| `@ai-sdk/vercel` | Vercel AI |
| `@ai-sdk/openai-compatible` | OpenAI 호환 (커스텀 엔드포인트) |
| `@openrouter/ai-sdk-provider` | OpenRouter |
| `gitlab-ai-provider` | GitLab AI |
| `@ai-sdk/github-copilot` | GitHub Copilot |

#### 프로바이더 전환 메커니즘

```typescript
// 번들된 프로바이더 매핑
const BUNDLED_PROVIDERS: Record<string, (options: any) => SDK> = {
  "@ai-sdk/anthropic": createAnthropic,
  "@ai-sdk/openai": createOpenAI,
  // ... 20+ 프로바이더
}
```

- 설정(`opencode.json`)의 `provider` 섹션에서 프로바이더별 SDK 패키지, API 키, 베이스 URL 지정
- `Provider.getLanguage()` → AI SDK의 `LanguageModelV2` 인스턴스 반환
- `ProviderTransform` — 프로바이더별 옵션 변환 (캐싱, 출력 토큰, 온도 등)
- 모델별 시스템 프롬프트 자동 선택: Claude → `anthropic.txt`, GPT → `beast.txt`/`codex.txt`, Gemini → `gemini.txt`

### 4.5 Tree-sitter 코드 파싱

OpenCode는 `web-tree-sitter` 0.25.10과 `tree-sitter-bash` 0.25.0을 의존성으로 포함한다. Tree-sitter는 주로 **코드 검색 도구**(`packages/opencode/src/tool/codesearch.ts`)에서 AST 기반 코드 분석에 활용된다. 패키지의 `trustedDependencies`에 `tree-sitter`, `tree-sitter-bash`, `web-tree-sitter`가 명시되어 있어 네이티브 바이너리 빌드를 허용한다.

### 4.6 데이터 레이어

**파일**: `packages/opencode/src/storage/db.ts`, `packages/opencode/src/storage/schema.ts`, `packages/opencode/src/session/session.sql.ts`

#### Drizzle ORM + SQLite

- **ORM**: `drizzle-orm` 1.0.0-beta.19
- **마이그레이션**: `drizzle-kit` 동일 버전, `packages/opencode/migration/` 하위에 SQL 마이그레이션 파일
- **DB 경로**: `~/.local/share/opencode/opencode.db` (XDG 표준), 채널별 분리 가능
- **PRAGMA 최적화**: WAL 모드, NORMAL 동기화, 5초 busy timeout, 64MB 캐시, 외래키 활성

#### 스키마 구조

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│   Project    │────>│   Session    │────>│   Message    │
│  (project)   │     │  (session)   │     │  (message)   │
│  - id (PK)   │     │  - id (PK)   │     │  - id (PK)   │
│  - ...       │     │  - project_id│     │  - session_id│
│              │     │  - parent_id │     │  - data (JSON)│
│              │     │  - title     │     └──────┬───────┘
│              │     │  - slug      │            │
│              │     │  - summary   │     ┌──────┴───────┐
│              │     │  - share_url │     │    Part       │
│              │     │  - revert    │     │  (part)       │
│              │     │  - permission│     │  - id (PK)    │
│              │     └──────────────┘     │  - message_id │
│              │                          │  - session_id │
│              │     ┌──────────────┐     │  - data (JSON)│
│              │────>│    Todo       │     └──────────────┘
│              │     │  (todo)       │
│              │     │  - session_id │     ┌──────────────┐
│              │     │  - content    │     │  Permission   │
│              │     │  - status     │     │ (permission)  │
│              │     │  - priority   │     │  - project_id │
│              │     │  - position   │     │  - data (JSON)│
│              │     └──────────────┘     └──────────────┘
│              │
│              │     ┌──────────────┐     ┌──────────────┐
│              │     │ SessionShare │     │   Account     │
│              │     │(session_share│     │  (account)    │
│              │     │  - id        │     │  - id         │
│              │     │  - ...       │     │  - ...        │
│              │     └──────────────┘     └──────────────┘
└──────────────┘
                     ┌──────────────┐
                     │  Workspace   │
                     │ (workspace)  │
                     │  - id        │
                     │  - ...       │
                     └──────────────┘
```

**핵심 설계 특징**:
- 메시지(`Message`)와 파트(`Part`)의 JSON 데이터 컬럼: `data TEXT NOT NULL` — 유연한 스키마
- 세션은 `parent_id`로 부모-자식 관계 (서브에이전트 세션)
- `PermissionTable` — 프로젝트별 도구 권한 영속 저장
- `TodoTable` — AI가 관리하는 할일 목록

### 4.7 플러그인 시스템

**파일**: `packages/opencode/src/plugin/index.ts`, `packages/plugin/src/index.ts`

#### 플러그인 로딩 메커니즘

1. **내장 플러그인** (`INTERNAL_PLUGINS`):
   - `CodexAuthPlugin` — OpenAI Codex 인증
   - `CopilotAuthPlugin` — GitHub Copilot 인증
   - `GitlabAuthPlugin` — GitLab 인증

2. **npm 플러그인**: `opencode.json`의 `plugin` 배열에 패키지명 지정 → `BunProc.install()`로 설치 → `import()`로 동적 로딩

3. **로컬 파일 플러그인**: `.opencode/{tool,tools}/*.{js,ts}` 경로에서 자동 발견

#### 확장 포인트 (Hooks)

```typescript
interface Hooks {
  // 시스템 프롬프트 변환
  "experimental.chat.system.transform"?: (input, output: { system: string[] }) => Promise<void>
  // LLM 호출 파라미터 변환
  "chat.params"?: (input, output) => Promise<void>
  // HTTP 헤더 변환
  "chat.headers"?: (input, output: { headers: Record<string, string> }) => Promise<void>
  // 도구 정의 변환
  "tool.definition"?: (input: { toolID: string }, output) => Promise<void>
  // 텍스트 완료 후처리
  "experimental.text.complete"?: (input, output: { text: string }) => Promise<void>
  // 설정 변경 알림
  config?: (config: Config.Info) => void
  // 버스 이벤트 수신
  event?: (input: { event: any }) => void
  // 커스텀 도구 등록
  tool?: Record<string, ToolDefinition>
}
```

#### 커스텀 도구 등록

플러그인은 `tool` 훅을 통해 커스텀 도구를 등록할 수 있다. `.opencode/tools/` 디렉토리에 TypeScript/JavaScript 파일을 배치하면 `ToolRegistry`가 자동 발견하여 등록한다.

### 4.8 TUI 렌더링

OpenCode의 TUI는 **@opentui/core** + **@opentui/solid** 기반으로, SolidJS의 반응성 시스템을 터미널에서 사용한다.

**컴포넌트 구조** (`packages/opencode/src/cli/cmd/tui/`):
- yargs의 TUI 커맨드가 SolidJS 기반 터미널 렌더러를 시작
- @opentui가 터미널 escape 코드를 생성하여 UI 렌더링
- 이벤트 루프: Bus (이벤트 버스) → SSE 수신 → SolidJS 반응형 상태 업데이트 → 터미널 재렌더링

### 4.9 데스크톱 앱

#### Tauri (packages/desktop)

- Tauri 2.x + Rust 사이드카
- `scripts/predev.ts` → OpenCode 바이너리 빌드/복사
- Tauri 플러그인: clipboard, deep-link, dialog, shell, store, updater, window-state, notification, process, http
- Rust 백엔드가 사이드카 프로세스로 OpenCode 서버를 관리

#### Electron (packages/desktop-electron)

- Electron 40.x + electron-vite
- `src/main/` — 메인 프로세스 (사이드카 관리, IPC)
- `src/preload/` — 프리로드 스크립트 (컨텍스트 브릿지)
- `scripts/predev.ts` — 개발시 OpenCode 바이너리 준비
- `tree-kill` 패키지로 사이드카 프로세스 트리 강제 종료 처리

#### IPC 통신 패턴

두 데스크톱 앱 모두 동일한 패턴을 사용한다:
1. 데스크톱 앱 시작 → OpenCode 바이너리를 사이드카로 실행 (`opencode serve`)
2. 내장 웹뷰가 `packages/app` (SolidJS 웹 앱) 로드
3. 웹 앱이 `@opencode-ai/sdk` 클라이언트로 로컬 HTTP API 서버와 통신
4. SSE로 실시간 이벤트 수신

---

## 5. 설정 및 의존성 분석

### 5.1 핵심 의존성

| 패키지 | 버전 | 역할 |
|--------|------|------|
| `ai` (Vercel AI SDK) | 5.0.124 | LLM 추상화 계층 |
| `@ai-sdk/*` | 각 버전 | 20+ AI 프로바이더 어댑터 |
| `@modelcontextprotocol/sdk` | 1.25.2 | MCP 클라이언트 |
| `@agentclientprotocol/sdk` | 0.14.1 | ACP 에이전트 프로토콜 |
| `drizzle-orm` | 1.0.0-beta.19-d95b7a4 | SQLite ORM |
| `effect` | 4.0.0-beta.35 | 함수형 프로그래밍 (상태/서비스 관리) |
| `hono` | 4.10.7 | HTTP 서버 프레임워크 |
| `solid-js` | 1.9.10 | UI 프레임워크 (TUI + 웹) |
| `zod` | 4.1.8 | 스키마 검증 |
| `yargs` | 18.0.0 | CLI 파서 |
| `web-tree-sitter` | 0.25.10 | AST 기반 코드 파싱 |
| `vscode-jsonrpc` | 8.2.1 | LSP 프로토콜 통신 |
| `@octokit/rest` | 22.0.0 | GitHub API |
| `remeda` | 2.26.0 | 함수형 유틸리티 |
| `fuzzysort` | 3.1.0 | 퍼지 검색 |

### 5.2 모노레포 카탈로그 기반 버전 관리

루트 `package.json`의 `workspaces.catalog` 섹션에서 공유 의존성 버전을 중앙 관리한다. 각 패키지에서 `"catalog:"` 프로토콜로 참조하면 카탈로그에 정의된 버전이 자동 적용된다.

```json
// 루트 package.json (카탈로그)
"catalog": {
  "ai": "5.0.124",
  "effect": "4.0.0-beta.35",
  "drizzle-orm": "1.0.0-beta.19-d95b7a4",
  "solid-js": "1.9.10",
  "zod": "4.1.8"
}

// 패키지별 참조
"dependencies": {
  "ai": "catalog:",
  "effect": "catalog:"
}
```

### 5.3 프로젝트 설정

OpenCode는 `opencode.json` (또는 `opencode.jsonc`) 파일로 설정한다. 설정 로딩 우선순위 (낮은 → 높은):

1. Remote `.well-known/opencode` (조직 기본값)
2. 글로벌 설정 (`~/.config/opencode/opencode.json`)
3. 커스텀 설정 (`OPENCODE_CONFIG` 환경변수)
4. 프로젝트 설정 (`./opencode.json`)
5. `.opencode/` 디렉토리 설정
6. 인라인 설정 (`OPENCODE_CONFIG_CONTENT`)
7. 매니지드 설정 (엔터프라이즈, 최상위 우선)

**주요 설정 항목**:
- `provider` — AI 프로바이더별 설정 (API 키, 모델, 베이스 URL)
- `mcp` — MCP 서버 설정 (local/remote, command, url, timeout)
- `agent` — 에이전트 커스터마이징 (프롬프트, 모델, 권한)
- `permission` — 전역 도구 권한
- `lsp` — LSP 서버 설정 (비활성화, 커스텀 서버)
- `plugin` — 플러그인 패키지 목록
- `instructions` — 커스텀 인스트럭션 (마크다운 파일 경로)

### 5.4 빌드 요구사항

- **Bun** >= 1.3.11 (패키지 매니저 + 런타임)
- **Node.js** — Bun이 커버하지 못하는 일부 네이티브 모듈용
- **Rust** — Tauri 데스크톱 빌드시 필요
- **macOS/Linux/Windows** 지원

---

## 6. API 및 인터페이스

### 6.1 CLI 커맨드 상세

| 커맨드 | 설명 |
|--------|------|
| `opencode` (기본) | TUI 모드 실행 |
| `opencode run` | 비대화형 실행 (스크립팅용) |
| `opencode serve` | 헤드리스 HTTP 서버 시작 |
| `opencode web` | 웹 UI 모드 시작 |
| `opencode generate` | 코드 생성 |
| `opencode agent` | 에이전트 관리 |
| `opencode mcp` | MCP 서버 관리 (add, list, auth) |
| `opencode pr` | PR 관련 작업 |
| `opencode models` | 사용 가능 모델 목록 |
| `opencode providers` | 프로바이더 목록 |
| `opencode session` | 세션 관리 |
| `opencode export` | 세션 내보내기 |
| `opencode import` | 세션 가져오기 |
| `opencode stats` | 사용 통계 |
| `opencode upgrade` | 자동 업그레이드 |
| `opencode uninstall` | 언인스톨 |
| `opencode github` | GitHub 연동 |
| `opencode acp` | ACP 서버 모드 |
| `opencode db` | 데이터베이스 관리 |
| `opencode completion` | 셸 자동완성 스크립트 생성 |

**글로벌 옵션**:
- `--print-logs` — stderr에 로그 출력
- `--log-level` — 로그 레벨 (DEBUG, INFO, WARN, ERROR)

### 6.2 서버 API (Hono 기반 HTTP)

`packages/opencode/src/server/server.ts`에 정의된 HTTP API. OpenAPI 3.1.1 스펙 자동 생성.

**주요 엔드포인트**:

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/doc` | OpenAPI 스펙 |
| GET | `/path` | 작업 디렉토리 경로 |
| GET | `/vcs` | VCS (git) 정보 |
| GET | `/agent` | 에이전트 목록 |
| GET | `/skill` | 스킬 목록 |
| GET | `/command` | 커맨드 목록 |
| GET | `/lsp` | LSP 서버 상태 |
| GET | `/formatter` | 포맷터 상태 |
| PUT | `/auth/:providerID` | 인증 정보 설정 |
| DELETE | `/auth/:providerID` | 인증 정보 삭제 |
| POST | `/instance/dispose` | 인스턴스 해제 |
| POST | `/log` | 로그 기록 |

**라우트 그룹**:
- `/session/*` — 세션 CRUD, 메시지 전송, 히스토리
- `/project/*` — 프로젝트 관리
- `/provider/*` — 프로바이더 및 모델 관리
- `/mcp/*` — MCP 서버 관리
- `/config/*` — 설정 조회/수정
- `/event/*` — SSE 이벤트 스트림
- `/tui/*` — TUI 전용 엔드포인트
- `/pty/*` — PTY 터미널 세션 (WebSocket)
- `/file/*` — 파일 조회
- `/permission/*` — 권한 관리
- `/question/*` — 사용자 질문/확인 요청
- `/global/*` — 글로벌 설정
- `/experimental/*` — 실험적 기능

### 6.3 SDK API

`packages/sdk/js/`에서 제공하는 JavaScript SDK.

```typescript
import { createOpencodeClient } from "@opencode-ai/sdk"

const client = createOpencodeClient({
  baseUrl: "http://localhost:4096",
  directory: "/path/to/project",
})

// 세션 생성
const session = await client.session.create({ directory: "." })

// 메시지 전송
await client.session.chat({
  sessionID: session.id,
  message: "파일 구조를 분석해줘",
})
```

**SDK 구조**:
- `src/index.ts` — 메인 내보내기
- `src/client.ts` — HTTP 클라이언트
- `src/server.ts` — 서버 유틸리티
- `src/v2/` — v2 API 클라이언트 (OpenAPI 자동 생성)

### 6.4 MCP 서버/클라이언트 인터페이스

OpenCode는 MCP **클라이언트**로서:
- `opencode.json`의 `mcp` 섹션에 외부 MCP 서버를 등록
- `@modelcontextprotocol/sdk` v1.25.2 사용
- stdio, StreamableHTTP, SSE 트랜스포트 지원
- OAuth 2.0 인증 흐름 (PKCE)
- 도구 목록 변경 알림 (`ToolListChangedNotification`) 구독

OpenCode 자체를 MCP **서버**로 실행하는 것도 가능하다:
- `opencode mcp` 커맨드로 MCP 서버 모드 시작
- OpenCode의 도구들을 MCP 프로토콜을 통해 외부에 노출

### 6.5 Agent Communication Protocol (ACP)

**파일**: `packages/opencode/src/acp/agent.ts`, `packages/opencode/src/acp/session.ts`, `packages/opencode/src/acp/types.ts`

ACP는 `@agentclientprotocol/sdk` v0.14.1을 사용하여 OpenCode를 **ACP 에이전트**로 노출한다. 이를 통해 외부 시스템이 표준 프로토콜로 OpenCode를 자동화할 수 있다.

- `ACPSessionManager` — ACP 세션 관리 (생성, 로드, 메시지 전송)
- `ACPConfig` — SDK 클라이언트 + 기본 모델 설정
- `opencode acp` 커맨드로 ACP 서버 모드 시작

---

## 7. Coco/IntraGenX 통합 분석

### 7.1 IntraGenX 트랙 2에서의 역할

OpenCode는 IntraGenX **트랙 2 (코딩 에이전트)** 의 기반 프로젝트다. 트랙 2의 목표는 OpenCode를 기반으로 자율형 CLI 코딩 에이전트를 구축하는 것이며, Bottom-Up 접근으로 개발자가 직접 사용하는 도구를 지향한다.

관련 문서: [트랙 2 기술 전략 리서치 v2.0](../../01_strategy/05_track2_tech_strategy_ko.md)

### 7.2 통합 포인트

| 통합 영역 | 방법 | 상세 |
|----------|------|------|
| **LLM 프로바이더** | `opencode.json` provider 설정 | 온프레미스 vLLM/LiteLLM 엔드포인트를 `@ai-sdk/openai-compatible`로 연결 |
| **MCP 프로토콜** | `opencode.json` mcp 설정 | xframe5-compiler 등 커스텀 MCP 서버 등록 |
| **도구 확장** | 플러그인 시스템 | `.opencode/tools/` 디렉토리에 커스텀 도구 배치 |
| **에이전트 커스텀** | `opencode.json` agent 설정 | 코드 거버넌스 전용 에이전트 정의 (프롬프트, 권한, 모델) |
| **인스트럭션** | `.opencode/` 마크다운 | 프로젝트별 코딩 규칙/표준 인스트럭션 |
| **API 통합** | Hono HTTP API | Coco Engine에서 OpenCode 서버 API로 자동화 |
| **ACP** | `opencode acp` | Coco 시스템에서 ACP 프로토콜로 에이전트 제어 |

### 7.3 커스터마이징 영역

#### 에이전트 커스텀

```json
// opencode.json 예시
{
  "agent": {
    "build": {
      "model": "openai-compatible/qwen-coder-32b",
      "prompt": "당신은 xFrame5 프레임워크 전문 개발자입니다...",
      "permission": {
        "edit": { "*.java": "allow", "*": "deny" }
      }
    },
    "review": {
      "mode": "primary",
      "description": "코드 리뷰 전용 에이전트",
      "prompt": "코드 품질, 보안, 성능을 검토하세요...",
      "permission": { "*": "deny", "read": "allow", "grep": "allow" }
    }
  }
}
```

#### MCP 서버 추가

```json
{
  "mcp": {
    "xframe5-compiler": {
      "type": "local",
      "command": ["node", "/path/to/xframe5-mcp-server.js"],
      "timeout": 60000
    },
    "jira": {
      "type": "remote",
      "url": "https://jira-mcp.internal.company.com/mcp"
    }
  }
}
```

#### 프로바이더 설정 (온프레미스)

```json
{
  "provider": {
    "local-vllm": {
      "api": "@ai-sdk/openai-compatible",
      "name": "vLLM 로컬",
      "baseURL": "http://gpu-server:8000/v1",
      "models": {
        "qwen-coder-32b": {
          "name": "Qwen Coder 32B",
          "id": "qwen2.5-coder-32b-instruct"
        }
      }
    }
  }
}
```

### 7.4 온프레미스/폐쇄망 배포 고려사항

| 고려사항 | 해결 방법 |
|---------|----------|
| **외부 API 차단** | `@ai-sdk/openai-compatible`로 내부 vLLM/LiteLLM 엔드포인트만 사용 |
| **npm 접근 불가** | Bun 바이너리 + 사전 빌드된 번들 배포 (또는 오프라인 미러) |
| **MCP 서버** | `type: "local"` (stdio) 사용, 외부 HTTP MCP 서버 비활성화 |
| **텔레메트리 비활성화** | `experimental.openTelemetry: false` |
| **공유 기능 비활성화** | `OPENCODE_DISABLE_SHARE=1` 환경변수 |
| **LSP 서버** | 인터넷 없이도 로컬 LSP 서버 자동 검색/스폰 |
| **업데이트** | `opencode upgrade` 비활성화, 수동 배포 |
| **인증** | API 키 대신 내부 인증 시스템 사용 (플러그인으로 커스텀) |
| **OpenCode Zen 비활성** | `provider` 설정에서 `opencode` 프로바이더 미설정 |

폐쇄망 환경에서는 OpenCode 서버 바이너리를 패키징하고, `opencode.json`으로 내부 LLM 엔드포인트만 설정하면 외부 통신 없이 동작한다. 단, 최초 의존성 설치(Bun install)는 오프라인 미러 또는 사전 빌드가 필요하다.

---

## 8. 참고자료 및 추가 탐색 가이드

### 8.1 공식 리소스

| 리소스 | URL |
|--------|-----|
| 공식 문서 | https://opencode.ai/docs |
| GitHub | https://github.com/anomalyco/opencode |
| Discord | https://discord.gg/opencode |
| npm | https://www.npmjs.com/package/opencode-ai |
| 데스크톱 다운로드 | https://opencode.ai/download |

### 8.2 추천 코드 읽기 순서

이 프로젝트를 처음 파악하려면 아래 순서를 권장한다:

1. **`AGENTS.md`** — 코딩 컨벤션, 스타일 가이드 (AGENTS.md 파일)
2. **`packages/opencode/src/index.ts`** — CLI 엔트리포인트, 전체 커맨드 구조 파악
3. **`packages/opencode/src/agent/agent.ts`** — 에이전트 정의, 권한 모델
4. **`packages/opencode/src/session/processor.ts`** — 핵심 실행 루프
5. **`packages/opencode/src/session/llm.ts`** — LLM 호출 메커니즘
6. **`packages/opencode/src/provider/provider.ts`** — 멀티프로바이더 추상화
7. **`packages/opencode/src/tool/registry.ts`** — 도구 등록 시스템
8. **`packages/opencode/src/tool/tool.ts`** — 도구 인터페이스 정의
9. **`packages/opencode/src/mcp/index.ts`** — MCP 클라이언트 관리
10. **`packages/opencode/src/lsp/index.ts`** — LSP 통합
11. **`packages/opencode/src/server/server.ts`** — HTTP API 서버
12. **`packages/opencode/src/config/config.ts`** — 설정 로딩 체계
13. **`packages/opencode/src/plugin/index.ts`** — 플러그인 시스템
14. **`packages/opencode/src/storage/db.ts`** — 데이터베이스 계층
15. **`packages/opencode/src/session/session.sql.ts`** — DB 스키마

### 8.3 AGENTS.md 코딩 컨벤션

OpenCode 프로젝트의 코딩 규칙 (`AGENTS.md`):

- **단일 단어 변수명** 선호 (`foo` O, `fooBar` X)
- **구조 분해 금지** — 점 표기법 사용 (`obj.a` O, `const { a } = obj` X)
- **else 금지** — 얼리 리턴 사용
- **const 선호** — 삼항 연산자 또는 얼리 리턴으로 대체
- **try/catch 최소화**
- **any 타입 금지**
- **Bun API 우선** (`Bun.file()` 등)
- **타입 추론 활용** — 불필요한 타입 어노테이션 지양
- **함수형 배열 메서드** 선호 (`flatMap`, `filter`, `map`)
- **Drizzle 스키마**: snake_case 필드명
- **기본 브랜치**: `dev` (main 아님)
- **테스트**: 패키지 디렉토리에서 실행 (루트에서 실행 금지), mock 최소화

### 8.4 주요 변경 내역

프로젝트는 빠르게 진화하고 있으며, v1.3.0 기준 주요 특징:
- Electron 데스크톱 앱 추가 (Tauri와 병행)
- ACP (Agent Communication Protocol) 지원
- OAuth 기반 MCP 인증
- 37개 언어 LSP 지원
- Effect 라이브러리 기반 서비스 계층 리팩토링
- JSON → SQLite 원타임 마이그레이션

---

## 변경이력

| 버전 | 일자 | 변경 내용 | 작성자 |
|------|------|----------|--------|
| 1.0 | 2026-03-23 | 초안 작성 -- OpenCode v1.3.0 심층 분석 | 분석팀 |
