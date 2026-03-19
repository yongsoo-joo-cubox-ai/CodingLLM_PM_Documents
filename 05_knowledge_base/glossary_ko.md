# Coco / IntraGenX 프로젝트 용어집

| 항목 | 내용 |
|------|------|
| **문서번호** | SAI-KB-2026-001 |
| **작성일** | 2026년 3월 19일 |
| **버전** | v1.0 |
| **보안등급** | 일반 |
| **작성** | Secern AI |

---

## 사용법 안내

- **경영진**: 각 용어의 **경영진용** 설명을 읽으면 기술 배경 없이도 핵심 개념을 파악할 수 있습니다.
- **개발자**: **개발자용** 설명에서 기술 사양·프로토콜·버전 정보를 확인하세요.
- 심화 내용은 각 항목의 관련 문서 링크를 참고하세요.
- UASL 내부 용어(엔티티, 속성, 화면, 전이 등)는 별도 문서에서 관리합니다.

---

## 1. 제품/전략 용어

### Coco

> Coordinated Coding | [경영진 요약](../01_strategy/01_executive_summary_ko.md), [제품 기능 소개](../01_strategy/04_product_overview_ko.md)

**경영진용**: AI가 생성한 코드가 회사 표준과 규정을 자동 준수하도록 관리하는 플랫폼. 코드를 "만드는 도구"가 아닌 "감독하는 시스템"입니다.

**개발자용**: CGF-B 파이프라인으로 표준 준수·감사 추적·LLM 추상화를 제공하는 AI 코드 거버넌스 플랫폼. Engine, Studio, CLI, Admin, MCP Servers, Eclipse Plugin으로 구성.

### IntraGenX

> AI 기반 차세대 시스템 개발 플랫폼 | [경영진 요약](../01_strategy/01_executive_summary_ko.md), [로드맵](../02_implementation/01_roadmap_ko.md)

**경영진용**: Coco의 대외 브랜드명. 시선AI(AI 두뇌)와 대보DX(앱·하드웨어)의 합작 제품.

**개발자용**: 2026-03부터 사용되는 대외 브랜드. 시선AI(The Brain, LLM) + 대보DX(The Body, 앱·어플라이언스) 합작, 트랙 1 SI 솔루션을 지칭.

### 투트랙 전략

> Two-Track 전략 | [경영진 요약](../01_strategy/01_executive_summary_ko.md), [로드맵](../02_implementation/01_roadmap_ko.md)

**경영진용**: 트랙 1(대규모 SI 일괄 코드 생성)과 트랙 2(개발자용 AI 코딩 도우미)로 두 시장을 동시 공략하는 전략.

**개발자용**: 트랙 1(IntraGenX, Spec-Driven Top-Down) + 트랙 2(코딩 에이전트, OpenCode Bottom-Up)를 병행. 온프레미스 LLM 인프라 공유.

### 트랙 1

> IntraGenX — Spec-Driven 일괄 코드 생성 | [로드맵](../02_implementation/01_roadmap_ko.md), [제품 기능 소개](../01_strategy/04_product_overview_ko.md)

**경영진용**: UASL 명세서를 입력하면 전체 앱 코드를 한 번에 생성하는 방식. 대형 SI 프로젝트에 적합.

**개발자용**: UASL/SUIS → CGF-B → 결정론적 코드 생성의 Top-Down 방식. 프레임워크별 MCP 서버가 변환 수행.

### 트랙 2

> 코딩 에이전트 — OpenCode 기반 CLI | [트랙 2 기술 전략](../01_strategy/05_track2_tech_strategy_ko.md), [로드맵](../02_implementation/01_roadmap_ko.md)

**경영진용**: 개발자가 터미널에서 AI와 대화하며 코딩하는 도구. 폐쇄망에서도 사용 가능한 Copilot 대안.

**개발자용**: OpenCode 포크 CLI 에이전트. MCP(Model Context Protocol)로 외부 도구 접근. 온프레미스 sLLM 지원이 차별점.

### 6대 USP

> Unique Selling Proposition | [경영진 요약](../01_strategy/01_executive_summary_ko.md), [경쟁 전략](../01_strategy/02_competitive_strategy_ko.md)

**경영진용**: Coco의 6가지 핵심 강점 — (1)같은 입력엔 항상 같은 결과 (2)코딩 표준 자동 적용 (3)인터넷 없이 사내 운영 (4)명세 기반 코드 생성 (5)모든 작업 기록 추적 (6)AI 모델 자유 교체.

**개발자용**: (1)결정론적 출력 (2)표준 강제 (3)완전한 온프레미스 (4)Spec-Driven (5)감사 추적 (6)LLM 추상화. 규제 산업에서 클라우드 경쟁사 대비 핵심 차별점.

### Spec-Driven

> 명세 기반 개발 방식 | [제품 기능 소개](../01_strategy/04_product_overview_ko.md)

**경영진용**: 정해진 양식(명세서)으로 요구사항을 입력하면 AI가 정확하게 코드를 생성하는 방식.

**개발자용**: UASL/SUIS 구조화 명세 입력으로 결정론적 출력을 보장. 적합성 수준(L1~L3)으로 품질 측정.

### CGF-B

> Code Generation Framework - Build | [제품 기능 소개](../01_strategy/04_product_overview_ko.md)

**경영진용**: 코드가 만들어지는 6단계 품질 관리 공정. 자동 필터링·검증·빌드로 불량 코드를 차단.

**개발자용**: Generate → Filter → Build 6단계 결정론적 파이프라인. UASL 적합성 검사, 표준 강제, 컴파일 검증 수행.

### Coco Engine

> 코드 생성 백엔드 서버 | [API 레퍼런스](../02_implementation/05_api_reference_ko.md), [제품 기능 소개](../01_strategy/04_product_overview_ko.md)

**경영진용**: 명세를 받아 코드를 생성·검증하는 핵심 서버.

**개발자용**: Rust(Loco.rs) 기반 백엔드. CGF-B 실행, LLM 호출 추상화, MCP 서버 관리, 감사 로그 기록 담당.

### Coco Studio

> 웹 기반 IDE | [제품 기능 소개](../01_strategy/04_product_overview_ko.md)

**경영진용**: 브라우저에서 코드 생성·리뷰·관리를 하는 웹 작업 환경.

**개발자용**: UASL 편집기, 코드 생성 UI, 리뷰 인터페이스, Q&A를 제공. Engine의 REST/스트리밍 API를 소비.

### Coco CLI

> 명령줄 인터페이스 | [제품 기능 소개](../01_strategy/04_product_overview_ko.md)

**경영진용**: 터미널에서 명령어로 Coco 기능을 사용하는 도구.

**개발자용**: CI/CD 통합, 배치 코드 생성, 스크립트 자동화를 지원하는 터미널 클라이언트.

### Coco Admin

> 관리자 콘솔 | [제품 기능 소개](../01_strategy/04_product_overview_ko.md)

**경영진용**: 사용자 권한, 프로젝트 설정, 사용 통계를 관리하는 관리 화면.

**개발자용**: RBAC 기반 사용자·프로젝트 관리, 감사 로그 조회, API 허용목록 관리를 제공하는 웹 콘솔.

### MCP 서버 (트랙 1)

> 프레임워크별 코드 생성 컴파일러 | [제품 기능 소개](../01_strategy/04_product_overview_ko.md), [기술 스택](../02_implementation/04_phase2_tech_stack_ko.md)

**경영진용**: 각 프레임워크(xFrame5, Vue, React 등)에 맞는 코드를 생성하는 전용 변환기.

**개발자용**: UASL/SUIS → 프레임워크 코드 변환 컴파일러 모듈. rmcp(Rust MCP SDK)로 구현. 트랙 2와 같은 MCP 프로토콜이지만, 코드 생성/검증 목적으로 활용.

### Eclipse Plugin

> IDE 확장 | [제품 기능 소개](../01_strategy/04_product_overview_ko.md)

**경영진용**: Eclipse IDE에서 도구 전환 없이 Coco 기능을 쓸 수 있는 확장 프로그램.

**개발자용**: Eclipse 내에서 Coco Engine API를 호출하여 코드 생성·리뷰·Q&A를 사용하는 플러그인.

### 코딩 에이전트

> 트랙 2 자율형 CLI 에이전트 | [트랙 2 기술 전략](../01_strategy/05_track2_tech_strategy_ko.md)

**경영진용**: AI가 스스로 코드를 분석·수정·테스트하는 자율형 개발 도우미.

**개발자용**: 에이전틱 루프(plan → execute → observe → refine)로 자율 코딩하는 OpenCode 기반 CLI 에이전트.

---

## 2. AI/LLM 기술 용어

### LLM

> Large Language Model | [경영진 요약](../01_strategy/01_executive_summary_ko.md)

**경영진용**: 대량의 텍스트를 학습하여 글·코드를 작성하는 AI 모델. ChatGPT, Claude 등이 해당.

**개발자용**: 수십억~수천억 파라미터 트랜스포머 모델. Coco에서 코드 생성·리뷰·Q&A에 사용, LLM 추상화로 모델 교체 가능.

### sLLM

> Small Large Language Model | [경쟁 전략](../01_strategy/02_competitive_strategy_ko.md), [기술 스택](../02_implementation/04_phase2_tech_stack_ko.md)

**경영진용**: 기업 서버에서 직접 돌릴 수 있는 소형 AI 모델. 데이터가 외부로 나가지 않아 보안에 강함.

**개발자용**: 4B~20B 파라미터 온프레미스 LLM. 단일 GPU(24~80GB VRAM)에서 운용, 파인튜닝·양자화로 도메인 특화.

### vLLM

> 고성능 LLM 추론 서버 | [vLLM R&D 계획](../02_implementation/06_vllm_rd_plan_ko.md)

**경영진용**: AI 모델의 응답 속도와 동시 처리 성능을 최적화하는 서버 소프트웨어.

**개발자용**: PagedAttention 기반 오픈소스 추론 서버. Continuous Batching + KV-Cache 최적화. LiteLLM과 연동.

### MoE

> Mixture of Experts | [기술 스택](../02_implementation/04_phase2_tech_stack_ko.md)

**경영진용**: 모델 안의 여러 "전문가" 중 질문에 맞는 전문가만 답변하는 효율적 방식.

**개발자용**: 게이팅 네트워크가 입력별로 소수 Expert만 활성화. 총 파라미터 대비 활성 파라미터가 적어 추론 비용 절감.

### LoRA

> Low-Rank Adaptation | [기술 스택](../02_implementation/04_phase2_tech_stack_ko.md)

**경영진용**: 모델 전체를 재학습하지 않고 핵심만 조정하여 맞춤 교육하는 기법. 시간·비용 절약.

**개발자용**: 사전학습 가중치 고정, 저랭크 행렬 쌍(A, B)만 학습하는 PEFT 기법. 파라미터의 0.1~1%만 학습.

### QLoRA

> Quantized LoRA | [기술 스택](../02_implementation/04_phase2_tech_stack_ko.md)

**경영진용**: LoRA에 모델 압축을 결합하여 더 적은 GPU로 맞춤 교육하는 방법.

**개발자용**: 4-bit 양자화 상태에서 LoRA 학습. 16-bit 대비 VRAM 60~70% 절감, 유사 성능.

### 파인튜닝

> Fine-Tuning | [기술 스택](../02_implementation/04_phase2_tech_stack_ko.md)

**경영진용**: 범용 AI를 우리 회사 코딩 규칙·프레임워크에 맞게 추가 교육시키는 과정.

**개발자용**: 사전학습 LLM을 도메인 데이터로 추가 학습. LoRA/QLoRA로 프레임워크별 코드 생성 품질 개선.

### RAG

> Retrieval-Augmented Generation | [기술 스택](../02_implementation/04_phase2_tech_stack_ko.md)

**경영진용**: AI가 답변 시 사내 문서를 먼저 검색하고 참고하여 정확도를 높이는 방식.

**개발자용**: 벡터 DB에서 관련 문서를 검색하여 컨텍스트로 주입. xFrame5 KB 등을 임베딩하여 코드 생성·Q&A에 활용.

### 프롬프트

> Prompt | [제품 기능 소개](../01_strategy/04_product_overview_ko.md)

**경영진용**: AI에게 "이런 코드를 만들어줘"라고 지시하는 입력 텍스트.

**개발자용**: 시스템(역할·규칙) + 사용자(태스크) 프롬프트. UASL + 프레임워크 컨텍스트를 포함한 구조화 템플릿 사용.

### 토큰

> Token | [비용 분석](../02_implementation/03_cost_analysis_ko.md)

**경영진용**: AI가 텍스트를 처리하는 최소 단위. 한글 약 1글자, 많을수록 비용 증가.

**개발자용**: 토크나이저의 서브워드 단위. 컨텍스트 윈도우, tokens/s, 토큰당 비용이 핵심 지표.

### 양자화 (AWQ)

> Activation-aware Weight Quantization | [기술 스택](../02_implementation/04_phase2_tech_stack_ko.md)

**경영진용**: AI 모델 크기를 줄여 적은 GPU 메모리로 실행하는 압축 기술.

**개발자용**: FP16 → INT4/INT8 변환. AWQ는 활성화 분포 고려 4-bit 양자화로 GPTQ 대비 품질 손실 적음. vLLM 네이티브 지원.

### 에이전틱 루프

> Agentic Loop | [트랙 2 기술 전략](../01_strategy/05_track2_tech_strategy_ko.md)

**경영진용**: AI가 "계획 → 실행 → 확인 → 수정"을 반복하며 작업을 완수하는 자동화 방식.

**개발자용**: Plan → Execute → Observe → Refine 반복 패턴. 각 사이클에서 Tool Calling으로 파일 I/O, 빌드, 테스트 수행.

### Tool Calling

> 도구 호출 | [트랙 2 기술 전략](../01_strategy/05_track2_tech_strategy_ko.md)

**경영진용**: AI가 필요할 때 외부 도구(파일 탐색, 코드 실행 등)를 직접 호출하는 기능.

**개발자용**: LLM이 JSON 스키마 정의 도구를 호출하는 기능. 트랙 2에서는 MCP로 표준화된 도구 접근 제공.

### Continuous Batching

> 연속 배칭 | [vLLM R&D 계획](../02_implementation/06_vllm_rd_plan_ko.md)

**경영진용**: 여러 사용자의 AI 요청을 쉬지 않고 연속 처리하여 처리량을 높이는 기술.

**개발자용**: 생성 완료 슬롯에 새 요청을 즉시 삽입하는 스케줄링. 정적 배칭 대비 GPU 활용률 대폭 향상.

### PagedAttention

> 페이지드 어텐션 | [vLLM R&D 계획](../02_implementation/06_vllm_rd_plan_ko.md)

**경영진용**: GPU 메모리를 효율적으로 관리하여 더 많은 요청을 동시 처리하는 기술.

**개발자용**: OS 가상 메모리 페이징을 KV-Cache에 적용. 고정 블록 비연속 저장으로 단편화 해소. vLLM 핵심 기술.

### 환각 (Hallucination)

> AI 허위 생성 | [경영진 요약](../01_strategy/01_executive_summary_ko.md)

**경영진용**: AI가 그럴듯하지만 사실과 다른 내용을 만드는 현상. Coco는 Spec-Driven + CGF-B로 완화.

**개발자용**: 존재하지 않는 API 호출, 잘못된 문법 등으로 나타남. 결정론적 파이프라인과 표준 필터링으로 완화.

### GPT-OSS

> 시선AI 자체 개발 온프레미스 LLM | [경영진 요약](../01_strategy/01_executive_summary_ko.md)

**경영진용**: 시선AI가 자체 개발한 코드 생성 전용 AI 모델. 사내 서버에서 운영.

**개발자용**: 20B 파라미터, 코드 생성 94% 정확도. 폐쇄망에서 vLLM으로 서빙.

### Qwen

> 알리바바 오픈소스 LLM 시리즈 | [기술 스택](../02_implementation/04_phase2_tech_stack_ko.md)

**경영진용**: 알리바바가 공개한 다양한 크기(4B~72B)의 오픈소스 AI 모델 시리즈.

**개발자용**: Qwen2.5-Coder가 코드 생성 특화. MoE 변형 제공. 파인튜닝 베이스 모델 후보.

### Vercel AI SDK

> AI 애플리케이션 개발 SDK | [트랙 2 기술 전략](../01_strategy/05_track2_tech_strategy_ko.md)

**경영진용**: AI 기능을 웹 앱에 쉽게 통합하는 개발 도구 모음.

**개발자용**: TypeScript SDK. LLM 스트리밍, 구조화 출력, Tool Calling 추상화. 다양한 프로바이더 단일 인터페이스.

---

## 3. 스펙/코드생성 용어

### UASL

> Unified Application Specification Language | [제품 기능 소개](../01_strategy/04_product_overview_ko.md), [로드맵](../02_implementation/01_roadmap_ko.md)

**경영진용**: 앱의 화면·데이터·로직을 표준 양식으로 정의하는 명세 언어. "건축 설계도" 역할.

**개발자용**: Spec-Driven 코드 생성의 핵심 명세 언어. 화면(SUIS), 데이터 모델, 로직, 전이를 구조화. 내부 용어는 별도 관리.

### SUIS

> Smart UI Specification | [제품 기능 소개](../01_strategy/04_product_overview_ko.md)

**경영진용**: 화면(UI)의 구성 요소와 배치를 정의하는 명세서.

**개발자용**: UASL의 화면 명세. 컴포넌트 트리, 레이아웃, 이벤트, 바인딩을 정의. MCP 서버가 프레임워크별 코드로 변환.

### IAS

> Intelligent Agent Specification | [제품 기능 소개](../01_strategy/04_product_overview_ko.md)

**경영진용**: AI 에이전트의 동작 규칙과 판단 기준을 정의하는 명세서.

**개발자용**: 에이전트 행동 규칙, 도구 접근 권한, 의사결정 로직을 구조화. 결정론적 제어에 사용.

### MCP (트랙 2, Model Context Protocol)

> Anthropic 제안 도구 접근 프로토콜 | [트랙 2 기술 전략](../01_strategy/05_track2_tech_strategy_ko.md)

**경영진용**: AI 도구들이 서로 소통하는 표준 규약. 트랙 1에서도 같은 프로토콜을 코드 생성 용도로 사용.

**개발자용**: LLM 에이전트가 Tool/Resource/Prompt에 접근하는 JSON-RPC 기반 프로토콜. 트랙 1과 같은 프로토콜이지만, 에이전트 도구 접근 목적으로 활용.

### 어댑터

> Adapter, 프레임워크 변환 모듈 | [제품 기능 소개](../01_strategy/04_product_overview_ko.md)

**경영진용**: 하나의 명세를 다른 프레임워크 코드로 변환하는 변환기.

**개발자용**: UASL/SUIS → xFrame5, Vue 3, React 19 등 프레임워크 코드 변환 모듈. MCP 서버(트랙 1) 내부 동작.

### 컴파일러

> Compiler | [기술 스택](../02_implementation/04_phase2_tech_stack_ko.md)

**경영진용**: 명세를 실행 가능한 코드로 변환하는 엔진. MCP 서버가 이 역할 수행.

**개발자용**: UASL/SUIS → AST 파싱 → 프레임워크 코드 변환. 각 MCP 서버(트랙 1)가 프레임워크별 컴파일러.

### 적합성 수준 (L1/L2/L3)

> Conformance Level | [제품 기능 소개](../01_strategy/04_product_overview_ko.md)

**경영진용**: 생성 코드가 명세를 얼마나 정확히 따르는지 3단계 측정. L1(구조) → L2(동작) → L3(완벽).

**개발자용**: L1 구조적(컴포넌트 트리), L2 기능적(이벤트·로직), L3 완전(스타일·성능 포함 100%) 적합성.

### OpenCode

> 오픈소스 터미널 AI 코딩 도구 | [트랙 2 기술 전략](../01_strategy/05_track2_tech_strategy_ko.md)

**경영진용**: 터미널에서 AI와 대화하며 코딩하는 오픈소스 도구. 트랙 2의 기반 기술.

**개발자용**: TypeScript + Bun 런타임 기반(모노레포, Turborepo). MCP 지원, Vercel AI SDK로 멀티 프로바이더 연동. 포크하여 온프레미스 sLLM 최적화 추가 예정.

### Cline

> VS Code 기반 AI 코딩 에이전트 | [트랙 2 기술 전략](../01_strategy/05_track2_tech_strategy_ko.md)

**경영진용**: VS Code에서 동작하는 AI 코딩 도우미. 트랙 2의 주요 경쟁 제품.

**개발자용**: VS Code 확장(Apache 2.0). 클라우드 LLM 최적화로 온프레미스 sLLM 호환성이 약점.

---

## 4. 인프라/배포 용어

### 온프레미스

> On-Premises | [경영진 요약](../01_strategy/01_executive_summary_ko.md), [비용 분석](../02_implementation/03_cost_analysis_ko.md)

**경영진용**: 외부 클라우드 없이 회사 자체 서버에서 운영. 데이터가 외부로 나가지 않음.

**개발자용**: 조직 내부 인프라 배포 모델. vLLM, Coco Engine, Studio 모두 고객 인프라에 설치.

### 폐쇄망 / 에어갭

> Air-Gapped Network | [규제 환경](../01_strategy/03_regulatory_environment_ko.md)

**경영진용**: 외부 인터넷과 완전 분리된 내부 네트워크. 금융·공공 분야에서 사용.

**개발자용**: 물리적 격리 환경. 오프라인 설치, 로컬 모델 서빙, 에어갭 호환 라이선스 필요.

### GPU

> Graphics Processing Unit | [비용 분석](../02_implementation/03_cost_analysis_ko.md)

**경영진용**: AI 연산 전용 하드웨어. 사양에 따라 동시 처리 가능 사용자 수 결정.

**개발자용**: LLM 추론·학습용 병렬 프로세서. NVIDIA CUDA 호환. VRAM이 모델 크기와 배칭 수를 결정.

### VRAM

> Video RAM | [비용 분석](../02_implementation/03_cost_analysis_ko.md)

**경영진용**: GPU 메모리. 클수록 더 큰 모델이나 더 많은 사용자를 동시 처리 가능.

**개발자용**: 모델 가중치 + KV-Cache + 활성화 값 저장. AWQ 4-bit 양자화로 사용량 대폭 절감 가능.

### CUDA

> Compute Unified Device Architecture | [기술 스택](../02_implementation/04_phase2_tech_stack_ko.md)

**경영진용**: NVIDIA GPU를 AI 연산에 활용하는 소프트웨어 플랫폼.

**개발자용**: NVIDIA GPU 병렬 컴퓨팅 플랫폼. PyTorch, vLLM GPU 가속에 필수. Toolkit·드라이버 호환성 관리 필요.

### Docker

> 컨테이너 플랫폼 | [기술 스택](../02_implementation/04_phase2_tech_stack_ko.md)

**경영진용**: 소프트웨어를 독립된 "상자"에 담아 어디서든 동일하게 실행하는 도구.

**개발자용**: 컨테이너 이미지로 일관된 환경 제공. Playground 격리, vLLM 서빙, CI/CD에 사용.

### Rust

> 시스템 프로그래밍 언어 | [기술 스택](../02_implementation/04_phase2_tech_stack_ko.md)

**경영진용**: 안전성·성능이 뛰어난 언어. Coco Engine이 이 언어로 개발됨.

**개발자용**: 메모리 안전성·동시성 보장. Coco Engine이 Rust + Loco.rs로 개발.

### Loco.rs

> Rust 웹 프레임워크 | [기술 스택](../02_implementation/04_phase2_tech_stack_ko.md)

**경영진용**: Coco Engine 서버 개발에 사용된 웹 프레임워크.

**개발자용**: Rails 영감 Rust 프레임워크. HTTP, 라우팅, 미들웨어, 백그라운드 작업. Axum 기반 비동기.

### Hono

> 경량 웹 프레임워크 | [트랙 2 기술 전략](../01_strategy/05_track2_tech_strategy_ko.md)

**경영진용**: 가볍고 빠른 웹 서버 프레임워크.

**개발자용**: TypeScript 경량 프레임워크. Edge Runtime 호환. 트랙 2 프록시/게이트웨이 계층 후보.

### LiteLLM

> LLM 프록시/게이트웨이 | [vLLM R&D 계획](../02_implementation/06_vllm_rd_plan_ko.md)

**경영진용**: 여러 AI 모델을 하나의 창구로 통합 관리. 모델 교체 시 시스템 변경 불필요.

**개발자용**: OpenAI 호환 API 프록시. vLLM, Ollama 등을 단일 엔드포인트로 추상화. 로드 밸런싱·폴백 지원.

### FastAPI

> Python 웹 프레임워크 | [기술 스택](../02_implementation/04_phase2_tech_stack_ko.md)

**경영진용**: Python으로 API 서버를 빠르게 만드는 프레임워크.

**개발자용**: Pydantic 타입 검증, 자동 API 문서. ASGI(Uvicorn) 기반 비동기 프레임워크.

### ASGI

> Asynchronous Server Gateway Interface | [기술 스택](../02_implementation/04_phase2_tech_stack_ko.md)

**경영진용**: Python 서버가 여러 요청을 동시 처리하게 하는 표준 규격.

**개발자용**: Python 비동기 웹 서버 표준. WebSocket, SSE 등 장시간 연결 지원.

### Tensorizer

> 모델 직렬화 도구 | [vLLM R&D 계획](../02_implementation/06_vllm_rd_plan_ko.md)

**경영진용**: AI 모델을 빠르게 저장·로딩하여 서버 재시작 시간을 단축.

**개발자용**: 텐서 스트리밍 직렬화 라이브러리. vLLM 연동으로 콜드 스타트 단축.

### Playground

> 프로젝트별 격리 실행 환경 | [로드맵](../02_implementation/01_roadmap_ko.md)

**경영진용**: 각 프로젝트를 독립 환경에서 실행·테스트하는 Docker 기반 공간.

**개발자용**: Docker 기반 격리 환경. FE-BE 전체 앱 배포·테스트. 포트 동적 할당.

### Demo/Dev 서버

> 시연·개발 환경 | [API 레퍼런스](../02_implementation/05_api_reference_ko.md)

**경영진용**: Demo는 고객 시연용, Dev는 개발·테스트용 환경.

**개발자용**: Demo(안정 버전) / Dev(최신 코드) 분리 운영. 포트 등 상세는 관련 문서 참조.

---

## 5. 보안/거버넌스 용어

### RBAC

> Role-Based Access Control | [제품 기능 소개](../01_strategy/04_product_overview_ko.md)

**경영진용**: 사용자 역할에 따라 접근 권한을 차등 부여하는 보안 방식.

**개발자용**: 역할-권한 매핑 접근 제어 모델. Coco Admin에서 프로젝트별·API 수준 권한 설정.

### SSO

> Single Sign-On | [vLLM R&D 계획](../02_implementation/06_vllm_rd_plan_ko.md)

**경영진용**: 한 번 로그인으로 여러 시스템에 접근하는 통합 인증.

**개발자용**: SAML 2.0/OIDC 기반. 기업 IdP(AD, Okta 등)와 연동.

### SAML

> Security Assertion Markup Language | [vLLM R&D 계획](../02_implementation/06_vllm_rd_plan_ko.md)

**경영진용**: 시스템 간 인증 정보를 안전하게 주고받는 표준 규약.

**개발자용**: XML 기반 인증·인가 교환 OASIS 표준. IdP-SP 어설션 교환으로 SSO 구현.

### JWT

> JSON Web Token | [API 레퍼런스](../02_implementation/05_api_reference_ko.md)

**경영진용**: 로그인 후 발급되는 디지털 신분증. 재로그인 없이 API 사용 가능.

**개발자용**: RFC 7519 자체 포함형 토큰(Header.Payload.Signature). Coco API 인증에 사용.

### 감사 추적

> Audit Trail | [경영진 요약](../01_strategy/01_executive_summary_ko.md), [규제 환경](../01_strategy/03_regulatory_environment_ko.md)

**경영진용**: 누가, 언제, 어떤 코드를 생성·수정했는지 기록하는 기능. 6대 USP 중 하나.

**개발자용**: 코드 생성·LLM 호출·사용자 액션을 타임스탬프·사용자 ID와 함께 기록. 금융권 컴플라이언스 충족.

### 결정론적 출력

> Deterministic Output | [경영진 요약](../01_strategy/01_executive_summary_ko.md), [제품 기능 소개](../01_strategy/04_product_overview_ko.md)

**경영진용**: 같은 입력에 항상 같은 코드가 나오는 특성. 6대 USP 첫 번째.

**개발자용**: CGF-B에서 temperature=0 + 후처리 필터·포맷터로 비결정론적 요소 제거.

### API 허용목록

> API Allowlist | [제품 기능 소개](../01_strategy/04_product_overview_ko.md)

**경영진용**: AI 코드 생성 시 사용 가능한 API만 지정하여 위험 API를 자동 차단.

**개발자용**: CGF-B Filter 단계에서 금지 API를 탐지·차단하는 화이트리스트. 프로젝트별 관리.

### LLM 추상화

> LLM Abstraction Layer | [경영진 요약](../01_strategy/01_executive_summary_ko.md), [vLLM R&D 계획](../02_implementation/06_vllm_rd_plan_ko.md)

**경영진용**: AI 모델 교체 시 시스템 변경 없이 사용 가능한 설계. 6대 USP 중 하나.

**개발자용**: LiteLLM으로 모델 백엔드 교체해도 CGF-B·Studio·CLI에 영향 없는 추상화 계층.

### 인공지능기본법

> AI 기본법 | [규제 환경](../01_strategy/03_regulatory_environment_ko.md)

**경영진용**: AI 개발·활용의 원칙과 규제를 정하는 대한민국 법률.

**개발자용**: 고위험 AI 영향평가, 투명성, 데이터 거버넌스 규정. Coco 기능이 컴플라이언스에 부합.

### 망분리

> Network Segregation | [규제 환경](../01_strategy/03_regulatory_environment_ko.md)

**경영진용**: 업무망과 인터넷망을 분리하는 보안 정책. 금융기관은 법적 의무.

**개발자용**: 물리적/논리적 망분리. 전자금융감독규정 의무. Coco 온프레미스 + 폐쇄망 아키텍처로 충족.

---

## 가나다순 전체 색인

| 용어 | 카테고리 | 간략 설명 |
|------|----------|-----------|
| 6대 USP | 제품/전략 | Coco의 6가지 핵심 차별점 |
| API 허용목록 | 보안/거버넌스 | 허용 API 화이트리스트 |
| ASGI | 인프라/배포 | Python 비동기 서버 표준 |
| CGF-B | 제품/전략 | 6단계 결정론적 파이프라인 |
| Cline | 스펙/코드생성 | VS Code AI 에이전트 (경쟁 제품) |
| Coco | 제품/전략 | AI 코드 거버넌스 플랫폼 |
| Coco Admin | 제품/전략 | 관리자 콘솔 |
| Coco CLI | 제품/전략 | 명령줄 인터페이스 |
| Coco Engine | 제품/전략 | Rust 기반 백엔드 서버 |
| Coco Studio | 제품/전략 | 웹 기반 IDE |
| Continuous Batching | AI/LLM 기술 | 연속 배칭 스케줄링 |
| CUDA | 인프라/배포 | NVIDIA GPU 컴퓨팅 플랫폼 |
| Demo/Dev 서버 | 인프라/배포 | 시연·개발 환경 |
| Docker | 인프라/배포 | 컨테이너 배포 플랫폼 |
| Eclipse Plugin | 제품/전략 | Eclipse IDE용 확장 |
| FastAPI | 인프라/배포 | Python 비동기 프레임워크 |
| GPT-OSS | AI/LLM 기술 | 시선AI 온프레미스 LLM |
| GPU | 인프라/배포 | AI 연산 하드웨어 |
| Hono | 인프라/배포 | TypeScript 경량 프레임워크 |
| IAS | 스펙/코드생성 | 에이전트 명세 |
| IntraGenX | 제품/전략 | 대외 브랜드명 |
| JWT | 보안/거버넌스 | 인증 토큰 |
| LiteLLM | 인프라/배포 | LLM 프록시 |
| LLM | AI/LLM 기술 | 대규모 언어 모델 |
| LLM 추상화 | 보안/거버넌스 | 모델 교체 추상화 계층 |
| Loco.rs | 인프라/배포 | Rust 웹 프레임워크 |
| LoRA | AI/LLM 기술 | 저랭크 파인튜닝 |
| MCP (트랙 2) | 스펙/코드생성 | Model Context Protocol |
| MCP 서버 (트랙 1) | 제품/전략 | 코드 생성 컴파일러 |
| MoE | AI/LLM 기술 | 전문가 혼합 아키텍처 |
| OpenCode | 스펙/코드생성 | 오픈소스 터미널 코딩 도구 |
| PagedAttention | AI/LLM 기술 | KV-Cache 메모리 관리 |
| Playground | 인프라/배포 | 프로젝트 격리 환경 |
| QLoRA | AI/LLM 기술 | 양자화 + LoRA |
| Qwen | AI/LLM 기술 | 알리바바 오픈소스 LLM |
| RAG | AI/LLM 기술 | 검색 증강 생성 |
| RBAC | 보안/거버넌스 | 역할 기반 접근 제어 |
| Rust | 인프라/배포 | 시스템 언어 |
| SAML | 보안/거버넌스 | 인증 교환 표준 |
| sLLM | AI/LLM 기술 | 소형 온프레미스 LLM |
| Spec-Driven | 제품/전략 | 명세 기반 코드 생성 |
| SSO | 보안/거버넌스 | 통합 인증 |
| SUIS | 스펙/코드생성 | 화면 명세 언어 |
| Tensorizer | 인프라/배포 | 모델 직렬화 도구 |
| Tool Calling | AI/LLM 기술 | 도구 호출 기능 |
| UASL | 스펙/코드생성 | 통합 앱 명세 언어 |
| Vercel AI SDK | AI/LLM 기술 | AI 앱 개발 SDK |
| vLLM | AI/LLM 기술 | LLM 추론 서버 |
| VRAM | 인프라/배포 | GPU 메모리 |
| 감사 추적 | 보안/거버넌스 | 작업 기록 로깅 |
| 결정론적 출력 | 보안/거버넌스 | 동일 입력 = 동일 출력 |
| 망분리 | 보안/거버넌스 | 네트워크 격리 |
| 양자화 (AWQ) | AI/LLM 기술 | 모델 압축 |
| 어댑터 | 스펙/코드생성 | 프레임워크 변환 모듈 |
| 에이전틱 루프 | AI/LLM 기술 | 에이전트 실행 루프 |
| 온프레미스 | 인프라/배포 | 자체 서버 운영 |
| 인공지능기본법 | 보안/거버넌스 | AI 규제법 |
| 적합성 수준 (L1/L2/L3) | 스펙/코드생성 | 코드 적합도 3단계 |
| 코딩 에이전트 | 제품/전략 | 트랙 2 CLI 에이전트 |
| 컴파일러 | 스펙/코드생성 | 명세 → 코드 변환 엔진 |
| 토큰 | AI/LLM 기술 | LLM 처리 단위 |
| 투트랙 전략 | 제품/전략 | 트랙 1 + 트랙 2 병행 |
| 트랙 1 | 제품/전략 | Spec-Driven 일괄 생성 |
| 트랙 2 | 제품/전략 | OpenCode 기반 CLI |
| 파인튜닝 | AI/LLM 기술 | 도메인 미세조정 |
| 폐쇄망 / 에어갭 | 인프라/배포 | 인터넷 격리 네트워크 |
| 프롬프트 | AI/LLM 기술 | LLM 입력 지시문 |
| 환각 (Hallucination) | AI/LLM 기술 | AI 허위 생성 |

---

## UASL 내부 용어 참조

UASL 내부 용어(엔티티, 속성, 화면, 전이, 바인딩, 유효성 검사 규칙 등)는 별도로 관리합니다.

- UASL v2/v3 스펙: `../03_development/2026-03-19_progress/uasl_spec/`
- UASL v1 스펙: `../03_development/2026-02-07_progress/uasl_spec/`

---

## 변경이력

| 버전 | 일자 | 변경 내용 | 작성자 |
|------|------|----------|--------|
| 1.0 | 2026-03-19 | 초안 작성 — 5개 카테고리 68개 용어 수록 | 분석팀 |
