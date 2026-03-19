# 시선AI 차세대 온프레미스 AI 코딩 에이전트 구축을 위한 시장 조사 및 기술 전략 보고서

| 항목 | 내용 |
|------|------|
| **문서번호** | SAI-STR-2026-005 |
| **작성일** | 2026년 3월 19일 |
| **버전** | v1.0 |
| **보안등급** | 대외비 |
| **작성** | 시선AI (Gemini Deep Research 기반 리서치) |

> 트랙 2 기술 전략 리서치 — 참고 문서 | [폴더 인덱스](./README.md)

---

## **1\. 시장 환경 및 엔터프라이즈 AI 코딩 도구의 패러다임 변화**

### **1.1. SI 및 보안 민감형 기업의 AI 도입 현황과 에어갭(Air-Gapped) 인프라의 필수성**

엔터프라이즈 소프트웨어 개발 환경, 특히 대규모 시스템 통합(SI), 금융 기관, 공공 부문에서는 생성형 AI의 도입이 급격히 증가하고 있으나, 동시에 심각한 보안 및 컴플라이언스 문제에 직면해 있다. AI 코딩 어시스턴트는 반복적인 작업을 자동화하고 개발 속도를 극대화하는 데 필수적인 도구로 자리 잡았으며, 업계 예측에 따르면 전문 개발자의 대다수가 향후 수년 내에 이러한 도구를 표준 워크플로우로 채택할 것으로 전망된다.1 그러나 외부 클라우드 기반의 대형 언어 모델(LLM)을 활용한 코딩 지원 도구들은 민감한 소스 코드의 유출, 학습 데이터 오염, 규제 위반 등의 치명적인 위험성을 내포하고 있다.1

보안 태세가 엄격한 기업의 최고정보보호책임자(CISO)와 보안 팀은 AI 도구의 도입을 검토할 때, 데이터의 처리 위치와 저장 정책을 가장 우선적으로 평가한다. 클라우드 API를 경유하는 코드 전송은 내부 정책이나 HIPAA, GDPR, SOC2와 같은 규제 프레임워크를 위반할 소지가 크며, API 키가 학습 데이터로 유출되어 타 조직의 코드 제안에 노출되는 등의 실제 보안 사고 사례도 보고된 바 있다.3 이러한 환경에서는 코드가 외부망으로 유출되지 않도록 철저히 차단된 에어갭(Air-Gapped) 인프라 내에서 구동될 수 있는 온프레미스(On-premise) 솔루션이 필수적이다.5 에어갭 환경은 인터넷 연결 없이도 모델의 추론과 코드 분석이 가능해야 하며, 기업 내부의 인증 시스템(SSO/SAML) 및 역할 기반 접근 제어(RBAC)와 완벽히 연동되어야 한다.3 결과적으로 기업들은 혁신을 포기하지 않으면서도 혁신이 통제를 앞서지 않도록 하는 '책임 있는 채택(Responsible Adoption)'을 요구하고 있다.2

### **1.2. 시선AI IntraGenX의 현 주소와 고객 요구사항의 간극 분석**

현재 시선AI가 개발하여 시장에 선보인 'IntraGenX 1.0'은 코딩 자동화에 특화된 소형 거대언어모델(sLLM) 기반의 기업형 온프레미스 솔루션이다. 이 도구는 설계 문서를 기반으로 코드를 일괄 자동 생성하여 생산성을 높이고, 외부망이 차단된 폐쇄형 환경에서 구동됨으로써 대기업 및 금융권의 엄격한 보안 요구사항을 충족하도록 설계되었다.7 대보DX와의 협력을 통해 입증된 바와 같이, 수백 명의 인력이 투입되는 공공 및 금융기관의 차세대 시스템 구축 프로젝트에서 데이터 주권을 확보하고 내부 정책을 준수할 수 있다는 점은 강력한 경쟁 우위로 작용한다.8

그러나 기술적 완성도와 보안성에도 불구하고, 외부 고객들의 반응은 다소 미온적인 상태에 머물러 있다. 이는 개발자들이 시장에서 경험하고 있는 도구의 발전 속도와 기대 수준이 IntraGenX의 현재 제공 범위를 넘어섰기 때문이다. SI 프로젝트 초기 단계의 보일러플레이트 작성이나 문서 기반의 정적인 코드 생성에는 효과적일지라도, 현대의 개발자들은 이미 Anthropic의 Claude Code나 Cursor와 같이 높은 자율성과 고도화된 컨텍스트 인지 능력을 갖춘 동적인 에이전트 툴에 익숙해져 있다.10 고객들은 단순히 명령에 따라 코드를 출력해 주는 단방향 엔진을 원하는 것이 아니라, 개발자의 로컬 환경에서 직접 터미널 명령어를 실행하고 오류를 추적하며 복잡한 아키텍처 리팩토링을 주도하는 양방향의 '에이전틱 파트너'를 요구하고 있다.13 또한, AI가 기업 내부의 구체적인 위협 모델이나 비즈니스 로직의 제약 조건을 완벽히 이해하지 못하는 상태에서 코드를 일괄 생성할 경우, 오히려 보안 취약점이나 아키텍처 결함을 양산할 수 있다는 점도 고객의 도입을 망설이게 하는 요인으로 분석된다.16

### **1.3. IDE 보조 도구에서 자율형 터미널 에이전트로의 진화**

AI 코딩 도구 시장은 단순한 코드 자동 완성(Autocomplete)을 제공하는 IDE 내장형 보조 도구에서, 작업의 기획부터 실행, 검증까지 스스로 수행하는 '자율형 에이전트(Autonomous Agent)' 중심으로 급격히 재편되고 있다.10 이러한 진화는 도구의 아키텍처 철학과 사용자 경험(UX)에 근본적인 차이를 만들어낸다.

| 도구 철학 및 분류 | 대표 솔루션 | 핵심 상호작용 방식 | 적합한 환경 및 주요 사용 사례 |
| :---- | :---- | :---- | :---- |
| **IDE-First (에디터 내장형)** | Cursor, GitHub Copilot | 개발자가 주도권을 쥐고 코드를 작성하며, AI는 라인 단위의 자동 완성과 인라인 수정(Inline Diff)을 제안한다.10 | 기존 IDE 환경을 유지하며 즉각적인 시각적 피드백과 미시적인 코드 수정이 빈번한 작업 환경에 최적화되어 있다.18 |
| **Agent-First (자율형 터미널)** | Claude Code, OpenCode | 자연어로 작업 목표를 지시하면, AI가 주도적으로 코드베이스를 읽고, 계획을 수립(Plan)하며, 터미널 명령어를 실행하여 다수의 파일을 자율적으로 수정한다.10 | 대규모 레거시 코드 리팩토링, 복잡한 시스템 아키텍처 개선, 심도 있는 문맥 파악이 필요한 거시적이고 독립적인 작업에 적합하다.13 |

개발자들은 자연어로 지시를 내리고 코드 작성을 AI에 일임하는 이른바 '바이브 코딩(Vibe-coding)' 방식에 점차 적응하고 있다.2 이 방식은 신속한 프로토타이핑에는 유리하지만, 명확한 계획이나 테스트 하네스(Test Harness), 엄격한 코드 리뷰 절차 없이 남용될 경우 아키텍처 원칙이 무너지고 디버깅이 불가능한 수준의 기술 부채가 축적되는 부작용을 낳는다.17 따라서 엔터프라이즈 환경에서 요구하는 차세대 AI 에이전트는 단순히 코드를 대량으로 생성하는 기능을 넘어, 터미널 환경에서 스스로 코드의 의존성을 파악하고, 테스트 코드를 구동하며, 논리적 오류를 진단 및 수정하는 자율적 추론 능력(Agentic Reasoning)을 반드시 갖추어야 한다.12 시선AI가 직면한 미온적인 고객 반응을 타개하기 위해서는, 고객이 체감하는 이러한 패러다임의 변화를 적극 수용하여 에이전트 중심의 상호작용 방식을 자사 솔루션에 이식하는 것이 필수적이다.

### **1.4. 엔터프라이즈 경쟁 솔루션 분석 및 시사점**

온프레미스 및 에어갭 환경을 타겟으로 하는 엔터프라이즈 AI 코딩 시장에는 이미 여러 경쟁 솔루션이 진입하여 각자의 아키텍처 철학을 바탕으로 점유율을 확보하고 있다. 이들 솔루션의 강점과 한계를 분석하는 것은 시선AI의 제품 포지셔닝에 중요한 시사점을 제공한다.

첫째, Tabnine은 프라이버시를 최우선으로 하는 엔터프라이즈 솔루션으로, 고객의 VPC(Virtual Private Cloud)나 온프레미스 환경에 Kubernetes 클러스터 형태로 직접 배포할 수 있는 유연성을 제공한다.24 Tabnine Enterprise Context Engine은 사내 보안 정책을 준수하면서도 코드베이스의 맥락을 파악할 수 있도록 지원하지만, 본질적으로 IDE 기반의 자동 완성을 주력으로 삼고 있어 복잡한 다중 파일 수정이나 터미널 기반의 자율 실행 영역에서는 한계를 보인다.26

둘째, Sourcegraph Cody는 대규모 다중 리포지토리(Multi-repository) 환경에서의 통합된 문맥 파악 능력을 무기로 내세운다.28 Qualtrics나 Palo Alto Networks와 같은 대규모 개발 조직에서 수천 명의 개발자가 사용하는 코드를 색인화하여, 파일 단위를 넘어선 마이크로서비스 간의 의존성까지 분석하는 플랫폼을 제공한다.6 Cody 역시 자체 데이터 센터에 구축 가능한 온프레미스 옵션을 제공하며, LLM에 종속되지 않고 원하는 모델을 선택할 수 있는 유연성을 보장한다.29 그러나 대규모 인프라 구축 비용이 수반되며, 초기 도입의 복잡성이 높다는 단점이 있다.

셋째, Continue.dev는 오픈소스 IDE 확장 프레임워크로서, 개발자가 Ollama와 같은 도구를 이용해 로컬 LLM을 직접 연결할 수 있도록 지원한다.6 사용자는 자신만의 모델을 선택하고, 커스텀 컨텍스트를 주입할 수 있는 강력한 제어권을 갖게 되며, 도입 비용 또한 매우 낮거나 무료이다.31 하지만 초기 설정에 대한 높은 기술적 이해도가 요구되고, UI/UX 측면에서의 마감 처리가 상업용 도구에 비해 부족하며, 중앙 집중화된 엔터프라이즈 거버넌스 통제 기능을 기본적으로 제공하지 않는다는 치명적인 약점이 있다.30

이러한 경쟁 구도 속에서 시선AI는 Tabnine의 에어갭 배포 안정성, Sourcegraph Cody의 코드베이스 문맥 이해 능력, 그리고 Continue.dev의 모델 독립적 유연성을 모두 포괄하면서도, 이를 터미널 기반의 자율형 에이전트(Claude Code 형태)로 통합하는 차별화된 아키텍처를 지향해야 한다.

## **2\. 벤치마크 대상 및 핵심 기술 분석: Claude Code vs. 최신 OpenCode 아키텍처**

시선AI의 목표는 현재의 SI 특화 개발 방향을 유지하면서, 궁극적으로 오픈소스 프로젝트인 'OpenCode'를 기반으로 Claude Code 수준의 자율 기능을 제공하는 코딩 에이전트로 확장하는 투트랙 전략이다. 이를 위해 구형 아키텍처에서 진화한 최신 OpenCode(anomalyco/opencode)를 집중적으로 분석한다.

### **2.1. Claude Code의 에이전틱 루프(Agentic Loop)와 아키텍처 심층 분석**

Anthropic이 개발한 Claude Code는 터미널 기반의 CLI 환경에서 작동하는 고도화된 에이전트 도구로, 지능적인 추론 모델과 로컬 시스템 도구 간의 끊임없는 상호작용인 '에이전틱 루프(Agentic Loop)'를 시스템의 핵심 동력으로 삼고 있다.33 이 아키텍처는 개발자가 모든 코드를 직접 작성하는 대신, "무엇이 변경되어야 하는가"를 지시하면 AI가 자율적으로 목표를 달성하도록 설계되었다.10

에이전틱 루프는 다음과 같은 유기적인 단계로 구성된다.12

1. **Ask (지시 및 맥락 수집):** 사용자가 자연어로 작업을 지시하면, 모델은 프로젝트 내의 파일들을 검색하고 코드의 구조를 읽어들여 문제 해결에 필요한 컨텍스트를 수집한다.12  
2. **Plan (계획 수립):** 수집된 정보를 바탕으로 다단계의 논리적 실행 계획을 수립한다.12 이 과정에서 모델은 작업의 순서, 수정해야 할 파일의 위치, 예상되는 의존성 충돌 등을 사전에 분석한다.  
3. **Execute (실행 및 도구 호출):** 계획이 승인되면, 에이전트는 직접 셸(Bash) 명령어를 실행하여 패키지를 설치하거나, 여러 파일에 걸쳐 코드를 삽입 및 수정한다.12  
4. **Verify (검증 및 자가 교정):** 코드 작성이 완료되면 자체적으로 테스트 스크립트나 린터를 구동한다. 만약 컴파일 오류나 테스트 실패가 발생하면, 에러 로그를 분석하여 실패 원인을 논리적으로 추론하고 새로운 해결책을 적용하는 과정을 사람의 개입 없이 자율적으로 반복(Self-Correction)한다.12

보안 측면에서 Claude Code는 모든 셸 명령어 실행이나 파일 쓰기 작업 직전에 사용자에게 명시적인 승인(Approval)을 요청하는 권한 모델을 채택하고 있다.12 이는 에이전트의 파괴적인 행동을 방지하는 필수적인 안전망 역할을 한다. 그러나 Claude Code는 필연적으로 Anthropic의 클라우드 API를 통해서만 작동하도록 설계되어 있으며, 모델의 내부 로직이 폐쇄적이기 때문에 시선AI가 목표로 하는 온프레미스 및 에어갭 환경, 그리고 자체 파인튜닝된 sLLM과의 연동은 불가능하다.15

### **2.2. OpenCode의 구조적 우위와 TypeScript/Bun 기반 클라이언트-서버 아키텍처**

시선AI가 차세대 솔루션의 토대로 채택한 최신 OpenCode(anomalyco/opencode)는 최근 레거시 구조(Go 언어)에서 벗어나 TypeScript와 Bun 런타임 기반의 모노레포(Turborepo) 아키텍처로 전면 개편되었다. 벤더 종속성을 완전히 탈피한 수평적 유연성(Horizontal Flexibility)을 제공하는 획기적인 개방형 프로젝트로서, 시선AI가 목표로 하는 기업형 솔루션으로 확장하는 데 최적화된 아키텍처를 자랑한다.

새롭게 도입된 핵심 구조와 패키지 구성은 다음과 같다.

| 구성 요소 및 아키텍처 | 핵심 기능 및 역할 | 시선AI 통합 관점에서의 시사점 |
| :---- | :---- | :---- |
| **Bun Runtime & Hono HTTP API** | 단순 CLI 툴을 넘어, 백엔드 API 서버(Hono)와 UI 클라이언트를 물리적으로 분리한 클라이언트/서버 구조를 채택했다. | 코어 로직 수정을 최소화하면서, 터미널뿐만 아니라 자체 데스크톱 앱, 웹 기반 사내 대시보드, IDE 등 다양한 프론트엔드 환경에서 동일한 에이전트를 제어할 수 있는 무한한 확장성을 제공한다. |
| **Vercel AI SDK 연동** | 단일 모델에 종속되지 않고 @ai-sdk/openai-compatible 인터페이스를 통해 75개 이상의 대형 및 로컬 모델을 즉시 연결한다. | opencode.json 구성 파일 수정만으로 시선AI의 자체 온프레미스 sLLM API를 손쉽게 커스텀 프로바이더(Provider)로 주입할 수 있다. |
| **Event-driven Agent Teams** | 단일 프로세스 내에서 서브 에이전트들이 P2P 메시징 기반으로 상태를 공유하며 다중 모델(Multi-model) 협업을 수행한다. 65 | 복잡한 SI 프로젝트 워크플로우를 분할하여, '설계 분석', '코드 작성', '보안 검수' 등 고유 역할이 부여된 다중 에이전트 팀을 구성해 대규모 작업을 빠르고 일관되게 처리할 수 있다. 65 |
| **JS/TS Plugin System** | tool.execute.before 와 같은 이벤트 훅(Hook) 기반으로 에이전트 동작 주기에 개입하는 자바스크립트/타입스크립트 기반 플러그인 생태계를 지원한다. | 기업의 내부 보안 정책 준수(민감 파일 접근 차단), 정적 분석 도구 강제 실행 등 고객사 맞춤형 사내 전용 보안 플러그인을 개발하여 손쉽게 덧붙일 수 있다. |

또한, OpenCode 아키텍처의 특징 중 하나는 에이전트의 논리적 사고 과정을 Plan(계획) 모드와 Build(실행) 모드로 철저히 분리하여 설계했다는 점이다.40 이는 복잡한 설계 검토를 거친 후 실제 구현에 돌입하는 SI 프로젝트의 엄격한 엔터프라이즈 워크플로우와 기술적으로 완벽히 부합한다.15

### **2.3. MCP(Model Context Protocol) 및 시스템 훅(Hooks)의 엔터프라이즈 활용성**

자율형 에이전트가 기업 내부 환경에 성공적으로 안착하기 위해서는 단순히 파일 시스템을 읽고 쓰는 것을 넘어, 조직의 다양한 지식 저장소와 보안 파이프라인에 동적으로 접근해야 한다. 이를 가능하게 하는 핵심 기술 표준이 MCP(Model Context Protocol)와 훅(Hooks) 메커니즘이다.

MCP는 AI 모델이 외부 데이터 소스나 도구에 접근할 수 있도록 해주는 개방형 표준 프로토콜이다.20 에어갭 환경에 배포된 에이전트는 외부 클라우드 API에 의존할 수 없으므로, 사내 망에 구축된 Jira, Confluence, GitLab, SonarQube 등과 통신하기 위한 로컬 stdio 방식의 MCP 서버를 활용해야 한다.20 예를 들어, 에이전트가 사내 이슈 트래커(Jira)에서 직접 버그 리포트를 읽어오고, 위키(Confluence)에 저장된 최신 설계 문서를 실시간 컨텍스트로 주입받아 그에 맞는 코드를 생성하는 지능형 워크플로우를 구현할 수 있다.20 이는 모델 자체를 매번 파인튜닝하지 않고도, 에이전트에게 항상 최신의 기업 내부 비즈니스 로직을 제공하는 가장 효과적이고 안전한 방법이다.

훅(Hooks) 메커니즘은 AI 에이전트의 동작 주기(Lifecycle) 사이에 관리자가 정의한 스크립트나 플러그인을 강제로 끼워 넣을 수 있는 제어 장치이다.12 OpenCode는 최신 JavaScript/TypeScript 기반 플러그인 시스템을 통해 tool.execute.before 와 같은 이벤트를 가로채 사내 정적 분석 도구(SAST)나 코드 린터(Linter)를 강제로 실행하도록 파이프라인을 구성할 수 있다. 만약 AI가 생성한 코드에서 보안 취약점이 발견되어 훅 로직이 차단 신호를 반환하면, 파일 쓰기 작업은 즉각 중단되며 AI는 오류 피드백을 받아 코드를 재수정해야 한다. 이러한 기계적이고 자동화된 검증 파이프라인은 AI 생성 코드의 무결성을 보장하고 관리자의 보안 우려를 불식시키는 강력한 방어선이 된다.

## **3\. 2026년 온프레미스 인프라 및 sLLM 최적화 동향**

시선AI의 타겟 고객인 보안이 중요한 기업들은 외부 네트워크와 단절된 환경에서 솔루션을 운영해야 한다. 따라서 클라우드 모델을 배제하고 한정된 온프레미스 하드웨어 자원 내에서 오픈소스 sLLM을 안정적으로 구동하는 최적화 전략이 사업 성공의 성패를 가른다.

### **3.1. 오픈소스 LLM 기술의 진화: MoE와 에이전틱 추론 모델**

2026년 현재, 오픈소스 LLM 생태계는 폭발적으로 진화하여 독점적 벤더 모델(GPT-5, Claude 3.5 Opus)에 필적하거나 오히려 이를 능가하는 코딩 및 추론 능력을 보여주고 있다.43 과거에는 우수한 성능을 얻기 위해 수천억 개의 매개변수를 가진 무거운 모델을 전체 구동해야 했으나, 최근에는 전문가 혼합(MoE, Mixture of Experts) 아키텍처가 대세로 자리 잡으면서 연산 효율성이 극적으로 개선되었다.

DeepSeek-V3.2, Qwen3-235B, GLM-4.5와 같은 최신 MoE 모델들은 전체 파라미터가 수백억에서 수천억 개에 달하지만, 실제 단일 토큰을 처리할 때 활성화되는 파라미터(Active Parameters)는 전체의 10% 내외에 불과하다.45 예를 들어, Qwen3-30B-A3B 모델은 전체 30B 파라미터 중 3B만 활성화하여 동작하므로 단일 80GB A100 GPU 한 장에서도 여유롭게 구동되며, 툴 호출(Tool-calling) 및 에이전트 워크플로우에서 경이로운 성과를 낸다.46

특히 샤오미가 발표한 MiMo-V2-Flash와 같은 최신 모델들은 범용적인 대화형 챗봇의 역할을 넘어, 코딩, 터미널 명령 실행, 디버깅 등 에이전트의 도구 사용 워크플로우에 특화되어 훈련되었다.44 이들은 150 tokens/sec 이상의 놀라운 추론 속도를 제공하면서도 소프트웨어 엔지니어링 벤치마크(SWE-Bench)에서 압도적인 성적을 기록하고 있다.44 시선AI가 개발 중인 자체 sLLM 역시 이러한 MoE 기반의 효율적인 아키텍처를 채택하고, 코드 생성뿐만 아니라 시스템 도구(LSP, Bash, 파일 I/O)를 올바른 JSON 포맷으로 호출할 수 있는 능력을 극대화하는 방향으로 파인튜닝(Fine-tuning)되어야 한다.

### **3.2. 하드웨어 요구사항 및 비용 효율적인 인퍼런스 환경 구축**

온프레미스 에어갭 환경에 AI 코딩 에이전트를 배포할 때, 고객사가 직면하는 가장 큰 물리적 장벽은 GPU 도입 비용과 인프라 구성의 복잡성이다.4 성능과 예산 사이의 최적의 타협점을 찾는 것이 시선AI 영업 전략의 핵심이다.

현재의 최적화 기술(INT4/INT8 양자화 등)을 적용할 때, 기업 규모와 모델 크기에 따른 권장 하드웨어 구성은 다음과 같이 요약할 수 있다.

| 도입 환경 및 목표 타겟 | 권장 모델 스펙 (2026 기준) | 권장 하드웨어 인프라 및 VRAM 요구사항 | 하드웨어 추정 비용 (USD) | 아키텍처 특징 |
| :---- | :---- | :---- | :---- | :---- |
| **소규모 팀 / 엔트리** | DeepSeek-R1-Distill-8B, Qwen 2.5-14B | 단일 워크스테이션, 8GB \~ 16GB VRAM (예: RTX 4080 1기) 49 | $1,500 \~ $3,000 | 소형 파라미터 모델 중심. 가벼운 코드 완성 및 단순 스크립트 생성에 적합. |
| **중규모 조직 / 스윗스팟** | Qwen 2.5 Coder 32B (Q4 양자화 적용), GLM-4.7-Flash | 워크스테이션 또는 소형 서버, 24GB \~ 32GB VRAM (예: RTX 4090 1\~2기 또는 신형 RTX 5090\) 44 | $3,000 \~ $8,000 | GPT-4 수준의 강력한 코딩 능력을 보유하며, 전력 대비 성능이 가장 우수함. 로컬 환경의 주력 구성. |
| **대규모 엔터프라이즈** | Qwen3-235B (MoE), Llama 3.3 70B, 자체 sLLM (Full) | 고성능 랙 마운트 서버, 128GB 이상 VRAM (예: 다중 H100 GPU 또는 512GB 메모리 탑재 Mac Studio 2대 연결) 45 | $20,000 (Mac) \~ $500,000+ (H100 클러스터) 50 | 대규모 코드베이스의 심층 이해, 복잡한 다중 에이전트 추론, 수백 명의 개발자 트래픽을 감당하는 중앙 집중형 인퍼런스 서버. |

시선AI는 고객의 인프라 예산에 맞춰 유연하게 대처해야 한다. 중앙 서버에 강력한 GPU(예: H100 클러스터)를 두고 수십 명의 개발자가 vLLM이나 TGI(Text-Generation-Inference)를 통해 내부 API로 접속하는 '중앙 집중형 호스팅' 방식과, 개별 개발자의 로컬 머신(MacBook Pro 등)에 Ollama나 llama.cpp를 설치하여 경량화된 모델을 직접 구동하는 '분산형 로컬' 방식을 모두 지원하는 아키텍처를 준비해야 한다.38 이는 OpenCode의 유연한 Provider 구조 덕분에 손쉽게 전환이 가능하다.15

## **4\. 레거시 모더니제이션 및 SI 워크플로우 통합 전략**

공공 및 금융 분야의 대형 SI 프로젝트에서 가장 빈번하고 중요한 워크플로우는 수십 년간 누적된 레거시 시스템을 최신 아키텍처로 변환하는 '모더니제이션(Modernization)' 작업이다. 시선AI의 솔루션은 이러한 복잡한 환경에서 개발자들의 작업을 어떻게 실질적으로 혁신할 수 있는지 구체적인 가치를 증명해야 한다.

### **4.1. 레거시 코드베이스의 현대화: 구형 시스템의 프레임워크 전환**

수많은 주요 기관들의 시스템은 여전히 COBOL, 구버전의 C++, 또는 EOL(End of Life)을 맞이한 초기 Java 프레임워크로 구동되고 있다.53 이러한 레거시 시스템은 비즈니스 로직이 방대하고 상호 의존성이 극도로 복잡하며, 당시 코드를 작성했던 개발자들이 은퇴하여 시스템의 작동 원리를 이해하는 인력이 턱없이 부족하다는 공통적인 문제를 지니고 있다.53 문서화조차 제대로 되어 있지 않은 경우가 다반사이다.54

OpenCode 기반의 차세대 코딩 에이전트는 이 지점에서 대체 불가능한 역량을 발휘한다. 기존 방식이 단순히 코드를 한 줄씩 현대적 언어로 번역하는 수준에 그쳤다면, 자율형 에이전트는 다중 스텝에 걸쳐 시스템을 해체하고 재조립한다.

1. **발견 및 추상화:** 먼저 OpenCode의 'Explore' 서브 에이전트가 투입되어 레거시 코드베이스 전체를 순회한다.55 에이전트는 단순히 문법을 읽는 것이 아니라, 낡은 코드 속에 숨겨진 핵심 비즈니스 로직과 데이터 파이프라인 흐름을 추출하여 사람이 읽을 수 있는 아키텍처 문서나 의사 코드(Pseudo-code) 형태로 문서화한다.53  
2. **구조 설계 및 전환:** 이어서 'Plan' 에이전트가 추출된 비즈니스 로직을 바탕으로 최신 프레임워크(예: Node.js, Spring Boot 3.x)에 맞는 새로운 디렉토리 구조와 모듈 분리 계획을 수립한다.42  
3. **코드 생성 및 자가 검증:** 마지막으로 'Build' 에이전트가 새로운 언어로 코드를 작성하고, 기존 시스템과 동일한 결과를 내는지 확인하기 위해 단위 테스트(Unit Test)를 자동 생성하여 실행한다.12 테스트가 실패할 경우, 에이전트는 에러 추적을 통해 코드의 세부 로직을 수정하는 작업을 자율적으로 반복한다.12 이러한 에이전트 주도의 모더니제이션 프로세스는 전환 과정의 위험성을 극적으로 낮추고 시간과 예산을 절약하며, 동시에 클라우드 및 온프레미스 현대화라는 거시적 목표를 빠르고 정확하게 달성할 수 있도록 지원한다.54

### **4.2. 설계 문서(Design-to-Code) 기반 자동화의 한계 극복 및 파이프라인 정교화**

현재 IntraGenX 솔루션이 채택하고 있는 화면 설계서 및 ERD 다이어그램 기반의 일괄 코드 생성 방식은, 체계적으로 문서화된 SI 프로젝트 환경에서 높은 초기 생산성을 보장한다.7 그러나 Design-to-Code 자동화는 입력되는 설계 문서의 품질과 구조에 지나치게 의존적이며, 기존의 복잡한 아키텍처나 코딩 표준과 충돌할 위험이 높다는 한계를 지닌다.57

이러한 한계를 극복하기 위해, 에이전트 파이프라인에 시각적 이해(Vision Analysis) 능력과 검색 증강 생성(RAG) 기술을 융합해야 한다.58 향후 시선AI 솔루션은 다중 모달(Multi-modal) sLLM을 활용하여 개발자가 업로드한 UI 캡처 이미지나 데이터베이스 스키마 이미지를 직접 파싱하고, 사내 문서 관리 시스템(Confluence 등)에 저장된 기존 설계 가이드라인을 RAG 기반으로 동적으로 참조하여 코드를 생성하는 방향으로 진화해야 강점을 유지할 수 있다.60 나아가, 자동 생성된 코드베이스에 대해 변경 사항이 생길 때마다 에이전트가 거꾸로 시스템 주석 및 기술 문서를 자동 업데이트(Self-healing documentation)하도록 파이프라인을 구축함으로써, 설계와 코드 간의 불일치를 영구적으로 방지하는 체계를 완성해야 한다.61

## **5\. 시선AI 투트랙(Two-Track) 전략 기반의 구체적 실행 계획**

앞선 시장 조사와 기술 분석을 바탕으로, 고객의 미온적인 반응을 잠재우고 엔터프라이즈 AI 코딩 플랫폼 시장을 선도하기 위한 시선AI의 개발 목표와 구체적인 실행 계획을 정의한다. 핵심 전략은 기존 고객 기반을 유지하는 트랙 1과, 미래지향적 자율 에이전트 경험을 제공하는 트랙 2를 병행하여 개발하는 '투트랙(Two-Track)' 접근법이다.

### **5.1. 트랙 1: SI 지향적 하향식(Top-Down) 일괄 생성 파이프라인 고도화**

현재 시장에 진입해 있는 IntraGenX 솔루션의 개발 방향은 SI 시장의 특수성을 고려하여 지속적으로 유지 및 고도화한다. 수백 명의 인력이 동시에 투입되는 차세대 시스템 구축 환경에서는 일관된 템플릿과 초기 구조 설정이 무엇보다 중요하다.8 따라서 설계 문서를 입력받아 대규모 보일러플레이트, API 엔드포인트 스켈레톤, 데이터베이스 ORM 모델 등을 일괄적으로 찍어내는 공장형(Factory) 파이프라인 엔진을 더욱 정교화한다. 이 트랙은 프로젝트 아키텍트나 PM 등 관리자 직군의 업무 효율성을 극대화하는 데 초점을 맞추며, 에어갭 환경 내에서의 강력한 보안 준수 모델을 영업의 핵심 무기로 삼는다.8

### **5.2. 트랙 2: OpenCode 기반 상향식(Bottom-Up) 자율형 CLI 에이전트 개발 및 통합**

일괄 생성된 기본 코드를 바탕으로 개별 개발자가 실질적인 비즈니스 로직을 구현하고, 코드를 리팩토링하며, 버그를 디버깅하는 일련의 개발 사이클에는 OpenCode 아키텍처를 기반으로 한 자율형 에이전트 솔루션을 새롭게 투입한다. 개발자가 로컬 IDE나 터미널에서 에이전트를 호출하여 "인증 모듈의 예외 처리 로직을 수정하고 테스트를 실행하라"고 지시하면, 에이전트가 LSP를 통해 코드 컨텍스트를 파악하고 Bash 툴로 테스트를 구동하며 파일을 갱신하는 완벽한 에이전틱 루프를 제공한다.12 이를 통해 기존 도구의 일방향성에 실망한 고급 개발자들에게 주도권과 자율성을 부여하고, Claude Code 이상의 지능적이고 유연한 경험을 선사한다.15

### **5.3. 단계별 로드맵 및 기술적 액션 플랜**

투트랙 전략을 현실화하기 위해, OpenCode 프로젝트의 코어 소스를 포크(Fork)하여 자사의 sLLM 및 기업 환경에 맞게 통합하는 4단계의 구체적인 로드맵을 실행한다.

**1단계: 코어 아키텍처 통합 및 자체 sLLM 연동 (1\~2개월)**

* **커스텀 프로바이더(Provider) 설정:** OpenCode의 최신 설정 시스템인 opencode.json과 @ai-sdk/openai-compatible 어댑터를 활용하여 시선AI의 자체 온프레미스 sLLM 엔드포인트와 인증 체계를 연동한다. 이를 통해 코어 엔진 레벨의 대규모 소스 수정 없이도 안전하게 폐쇄망의 로컬 sLLM을 네이티브 환경처럼 구동할 수 있다.  
* **에이전트 프롬프트 및 도구 호출 튜닝:** 자체 sLLM이 파일 조작, 셸 실행 등 OpenCode가 요구하는 시스템 도구(Tools)를 완벽하게 호출할 수 있도록 시스템 프롬프트를 튜닝한다.20 OpenCode의 동적 마크다운 기반 시스템 프롬프트 체계(.opencode/agents/)에 맞춰 sLLM을 파인튜닝하여, JSON 포맷의 도구 호출에 대한 인식률과 정확도를 극대화한다.20

**2단계: SI 특화 다중 서브 에이전트(Sub-Agents) 및 MCP 도구 개발 (3\~4개월)**

단일 LLM의 한계를 극복하고 엔터프라이즈 워크플로우를 완벽히 소화하기 위해 아키텍처를 확장한다.

* **다중 에이전트 오케스트레이션 적용:** 단일 프로세스 내에서 이벤트 기반 P2P 메시징으로 통신하는 OpenCode의 최신 'Agent Teams' 아키텍처를 도입하여, '설계 분석 에이전트', '코드 생성 에이전트', '테스트 에이전트' 등 역할을 분담한 다중 모델 에이전트 파이프라인을 구축한다.65  
* **기업 통합형 자체 MCP 서버 구축:** 사내 망에 이미 구축되어 있는 레거시 인프라와 AI가 소통할 수 있도록 맞춤형 MCP 서버를 개발하여 번들로 제공한다.20 Jira 연동을 통한 버그 트래킹 자동화, Confluence 연동을 통한 설계 문서 RAG 검색 기능 등을 구현하여, AI가 기업의 동적인 지식 베이스를 즉각적으로 활용할 수 있게 한다.20

**3단계: 엔터프라이즈 보안, 거버넌스 및 에어갭 정책 최적화 (5\~6개월)**

보안이 생명인 고객사를 만족시키기 위해 소프트웨어 아키텍처 레벨의 강력한 통제 장치를 마련한다.

* **권한 제어(RBAC) 및 명시적 승인 프로세스 내장:** OpenCode의 실행 권한 시스템을 엔터프라이즈 조직도와 연동한다. 중요 환경 변수 파일이나 시스템 코어 모듈 수정 시 자체 로직에 의해 차단되거나 다단계 승인을 요구하는 워크플로우를 구현한다.3  
* **보안 스캐닝 자동화 및 커스텀 플러그인 도입:** JavaScript/TypeScript 기반의 플러그인(Plugin) 시스템을 적극 활용하여 에이전트가 코드를 조작하기 직전/직후의 이벤트를 제어한다. 사내 정적 분석 도구(SonarQube 등)를 백그라운드에서 강제 실행시켜 취약점 유입을 원천 차단하고 영구 로깅하는 자체 감사(Audit) 체계를 완성한다.

**4단계: 사용자 경험(UX) 극대화 및 IDE 생태계 통합 (7\~8개월)**

고급 기능의 강력함을 유지하면서도, 다양한 층위의 개발자들이 직관적으로 도구를 활용할 수 있도록 접점을 넓힌다.

* **클라이언트/서버 기반 인터페이스 확장:** OpenCode가 제공하는 최신 클라이언트/서버 아키텍처(Hono HTTP API)를 최대한 활용하여, 터미널 환경뿐만 아니라 개발자 친화적인 자체 데스크톱 앱 및 사내 대시보드 웹 인터페이스를 구축한다.  
* **IDE 플러그인 확장 지원:** 궁극적으로 VS Code, IntelliJ와 같은 주력 IDE 내부에 자연스럽게 통합되는 플러그인 인터페이스를 제공한다.15 이를 통해 사용자들은 기존 편집기 화면을 이탈하지 않고도 코어 에이전트의 강력한 자율 추론 기능을 그대로 활용할 수 있게 되며, 도구 도입에 대한 심리적 장벽을 대폭 낮출 수 있다.

## **6\. 결론**

엔터프라이즈 소프트웨어 개발 환경은 거대한 패러다임의 전환기를 맞이하고 있다. 개발자들은 더 이상 단순한 코드 조각을 제안해 주는 정적인 도구에 만족하지 않으며, 시스템 구조를 분석하고 터미널에서 주도적으로 문제를 해결하는 자율형 에이전트 파트너를 원하고 있다.10 시선AI가 마주한 고객들의 미온적인 반응은 이러한 기대치의 상승을 반영하는 자연스러운 현상이다.

시선AI는 이러한 시장의 요구를 정면으로 돌파하기 위해, 기존 IntraGenX 솔루션의 SI 특화 일괄 생성 기능(트랙 1)을 고도화하여 생산성 파이프라인의 기반을 단단히 다지는 한편, 최신 오픈소스 OpenCode 프로젝트를 확장하여 강력한 지능형 에이전트 경험(트랙 2)을 통합하는 투트랙(Two-Track) 전략을 실행해야 한다. OpenCode가 제공하는 TypeScript와 Bun 기반의 유연한 클라이언트-서버 아키텍처, 물리적으로 분리된 계획 및 실행 모드, 그리고 진보된 다중 에이전트 팀(Agent Teams) 오케스트레이션 기능은 엔터프라이즈 환경이 요구하는 확장성과 통제력을 완벽히 만족시킨다.

또한 2026년 현재 비약적으로 발전한 MoE 기반의 오픈소스 sLLM 최적화 기술은 고가의 클라우드 API에 의존하지 않고도 오프라인 에어갭 인프라 환경에서 최고 수준의 추론 성능을 발휘할 수 있는 물리적 기반을 제공하고 있다.44 자체 sLLM을 OpenCode의 커스텀 제공자(Provider)로 깊숙이 통합하고, 철저한 권한 제어(RBAC)와 플러그인 기반의 보안 스캐닝 파이프라인을 확립하는 기술적 로드맵은 시선AI의 제품을 시장 내 독보적인 위치로 격상시킬 것이다.3

본 보고서에 제시된 4단계의 구체적 실행 계획을 체계적으로 이행한다면, 시선AI는 보안과 자율성이라는 상충해 보이던 두 가지 난제를 완벽히 해결하며, 공공 및 금융 SI 시장을 넘어 글로벌 엔터프라이즈 AI 코딩 플랫폼 시장의 새로운 표준을 제시하는 선도 기업으로 확고히 자리매김할 수 있을 것이다.

#### **참고 자료**

1. Guide to On-Prem AI Coding Servers \- Unigen, 3월 18, 2026에 액세스, [https://unigen.com/guide-to-on-prem-ai-coding-servers/](https://unigen.com/guide-to-on-prem-ai-coding-servers/)  
2. How to Securely Implement AI Coding Assistants Across the Enterprise \- WWT, 3월 18, 2026에 액세스, [https://www.wwt.com/wwt-research/how-to-securely-implement-ai-coding-assistants-across-the-enterprise](https://www.wwt.com/wwt-research/how-to-securely-implement-ai-coding-assistants-across-the-enterprise)  
3. 7 SOC 2-Ready AI Coding Tools for Enterprise Security, 3월 18, 2026에 액세스, [https://www.augmentcode.com/guides/7-soc-2-ready-ai-coding-tools-for-enterprise-security](https://www.augmentcode.com/guides/7-soc-2-ready-ai-coding-tools-for-enterprise-security)  
4. Building a Coding Agent to Meet Enterprise Demands \- Cosine, 3월 18, 2026에 액세스, [https://cosine.sh/blog/secure-ai-coding-agent-for-enterprise](https://cosine.sh/blog/secure-ai-coding-agent-for-enterprise)  
5. Google Distributed Cloud air-gapped | Sovereign Cloud, 3월 18, 2026에 액세스, [https://cloud.google.com/distributed-cloud-air-gapped](https://cloud.google.com/distributed-cloud-air-gapped)  
6. Enterprise AI Code Assistants for Air-Gapped Environments | IntuitionLabs, 3월 18, 2026에 액세스, [https://intuitionlabs.ai/articles/enterprise-ai-code-assistants-air-gapped-environments](https://intuitionlabs.ai/articles/enterprise-ai-code-assistants-air-gapped-environments)  
7. 시선AI, 코딩 자동화 AI 솔루션 'IntraGenX' 출시, 3월 18, 2026에 액세스, [https://www.mydailybyte.com/littlebit/news/239822](https://www.mydailybyte.com/littlebit/news/239822)  
8. 시선AI, 대보DX와 공동개발한 온프레미스 코딩 자동화 AI 솔루션 출시...온프레미스 운영으로 보안성 확보 \- 인공지능신문, 3월 18, 2026에 액세스, [https://www.aitimes.kr/news/articleView.html?idxno=38963](https://www.aitimes.kr/news/articleView.html?idxno=38963)  
9. 시선AI, 대보DX와 공동개발한 sLLM 기반 온프레미스 코딩 자동화 AI 솔루션 출시…공공·금융 차세대 시스템 개발 생산성 혁신 기대 \- SECERN AI %, 3월 18, 2026에 액세스, [https://secern.ai/%EC%8B%9C%EC%84%A0ai-%EB%8C%80%EB%B3%B4dx%EC%99%80-%EA%B3%B5%EB%8F%99%EA%B0%9C%EB%B0%9C%ED%95%9C-sllm-%EA%B8%B0%EB%B0%98-%EC%98%A8%ED%94%84%EB%A0%88%EB%AF%B8%EC%8A%A4-%EC%BD%94%EB%94%A9%EC%9E%90/](https://secern.ai/%EC%8B%9C%EC%84%A0ai-%EB%8C%80%EB%B3%B4dx%EC%99%80-%EA%B3%B5%EB%8F%99%EA%B0%9C%EB%B0%9C%ED%95%9C-sllm-%EA%B8%B0%EB%B0%98-%EC%98%A8%ED%94%84%EB%A0%88%EB%AF%B8%EC%8A%A4-%EC%BD%94%EB%94%A9%EC%9E%90/)  
10. Cursor vs Claude Code, 3월 18, 2026에 액세스, [https://medium.com/data-science-collective/cursor-vs-claude-code-87240ad9265e](https://medium.com/data-science-collective/cursor-vs-claude-code-87240ad9265e)  
11. Claude Code vs Cursor. The best AI Coding tool | by Mehul Gupta | Data Science in Your Pocket | Jan, 2026, 3월 18, 2026에 액세스, [https://medium.com/data-science-in-your-pocket/claude-code-vs-cursor-97b446515d83](https://medium.com/data-science-in-your-pocket/claude-code-vs-cursor-97b446515d83)  
12. Claude Code: Deep Dive into the Agentic CLI Workflow \- SitePoint, 3월 18, 2026에 액세스, [https://www.sitepoint.com/claude-code-deep-dive-into-the-agentic-cli-workflow/](https://www.sitepoint.com/claude-code-deep-dive-into-the-agentic-cli-workflow/)  
13. Cursor vs. Claude Code: in-depth comparison for dev teams | DECODE, 3월 18, 2026에 액세스, [https://decode.agency/article/cursor-vs-claude-code/](https://decode.agency/article/cursor-vs-claude-code/)  
14. OpenCode AI Coding Tool Is Changing How Developers Write Code \- Reddit, 3월 18, 2026에 액세스, [https://www.reddit.com/r/AISEOInsider/comments/1qh838s/opencode\_ai\_coding\_tool\_is\_changing\_how/](https://www.reddit.com/r/AISEOInsider/comments/1qh838s/opencode_ai_coding_tool_is_changing_how/)  
15. OpenCode: The Best Claude Code Alternative \- Tensorlake, 3월 18, 2026에 액세스, [https://www.tensorlake.ai/blog/opencode-the-best-claude-code-alternative](https://www.tensorlake.ai/blog/opencode-the-best-claude-code-alternative)  
16. AI code security: Risks, best practices, and tools | Kiuwan, 3월 18, 2026에 액세스, [https://www.kiuwan.com/blog/ai-code-security/](https://www.kiuwan.com/blog/ai-code-security/)  
17. AI‑Assisted Software Development — 6 Pitfalls to Avoid | by Jérôme Van Der Linden, 3월 18, 2026에 액세스, [https://jeromevdl.medium.com/ai-assisted-software-development-6-pitfalls-to-avoid-91233cf21d14](https://jeromevdl.medium.com/ai-assisted-software-development-6-pitfalls-to-avoid-91233cf21d14)  
18. Claude Code vs Cursor: What to Choose in 2026 \- Builder.io, 3월 18, 2026에 액세스, [https://www.builder.io/blog/cursor-vs-claude-code](https://www.builder.io/blog/cursor-vs-claude-code)  
19. GitHub Copilot vs OpenCode: IDE-Native AI vs Agent-First Development | by Lakshan Banneheke | Feb, 2026, 3월 18, 2026에 액세스, [https://medium.com/@lakshan-banneheke/opencode-vs-github-copilot-agent-first-development-vs-ide-native-ai-f9f1424bb249](https://medium.com/@lakshan-banneheke/opencode-vs-github-copilot-agent-first-development-vs-ide-native-ai-f9f1424bb249)  
20. Claude Code overview \- Claude Code Docs, 3월 18, 2026에 액세스, [https://code.claude.com/docs/en/overview](https://code.claude.com/docs/en/overview)  
21. Claude Code vs Cursor \- Codeaholicguy, 3월 18, 2026에 액세스, [https://codeaholicguy.com/2026/01/10/claude-code-vs-cursor/](https://codeaholicguy.com/2026/01/10/claude-code-vs-cursor/)  
22. Real Pain Points When Building With AI Tools? : r/vibecoding \- Reddit, 3월 18, 2026에 액세스, [https://www.reddit.com/r/vibecoding/comments/1p9sd7o/real\_pain\_points\_when\_building\_with\_ai\_tools/](https://www.reddit.com/r/vibecoding/comments/1p9sd7o/real_pain_points_when_building_with_ai_tools/)  
23. Claude Code Deep Dive: The Terminal-First AI Coding Agent That's Changing How Developers Work \- DEV Community, 3월 18, 2026에 액세스, [https://dev.to/pockit\_tools/claude-code-deep-dive-the-terminal-first-ai-coding-agent-thats-changing-how-developers-work-37ea](https://dev.to/pockit_tools/claude-code-deep-dive-the-terminal-first-ai-coding-agent-thats-changing-how-developers-work-37ea)  
24. Architecture | Tabnine Docs \- Overview, 3월 18, 2026에 액세스, [https://docs.tabnine.com/main/welcome/readme/architecture](https://docs.tabnine.com/main/welcome/readme/architecture)  
25. Deployment options | Tabnine Docs \- Overview, 3월 18, 2026에 액세스, [https://docs.tabnine.com/main/welcome/readme/architecture/deployment-options](https://docs.tabnine.com/main/welcome/readme/architecture/deployment-options)  
26. Enterprise (private installation) | Tabnine Docs \- Overview, 3월 18, 2026에 액세스, [https://docs.tabnine.com/main/welcome/readme/tabnine-subscription-plans/enterprise-private-installation](https://docs.tabnine.com/main/welcome/readme/tabnine-subscription-plans/enterprise-private-installation)  
27. Introducing the Tabnine Enterprise Context Engine, 3월 18, 2026에 액세스, [https://www.tabnine.com/blog/introducing-the-tabnine-enterprise-context-engine/](https://www.tabnine.com/blog/introducing-the-tabnine-enterprise-context-engine/)  
28. Windsurf vs Sourcegraph Cody: Which AI Coding Assistant Handles Enterprise Complexity?, 3월 18, 2026에 액세스, [https://www.augmentcode.com/tools/windsurf-vs-sourcegraph-cody](https://www.augmentcode.com/tools/windsurf-vs-sourcegraph-cody)  
29. Cody is enterprise ready | Sourcegraph Blog, 3월 18, 2026에 액세스, [https://sourcegraph.com/blog/cody-is-enterprise-ready](https://sourcegraph.com/blog/cody-is-enterprise-ready)  
30. AI for software development team in enterprise, : r/LocalLLaMA \- Reddit, 3월 18, 2026에 액세스, [https://www.reddit.com/r/LocalLLaMA/comments/1qj4m3p/ai\_for\_software\_development\_team\_in\_enterprise/](https://www.reddit.com/r/LocalLLaMA/comments/1qj4m3p/ai_for_software_development_team_in_enterprise/)  
31. Continue.dev: The AI Coding Assistant That Actually Respects Your Choices \- Medium, 3월 18, 2026에 액세스, [https://medium.com/@info.booststash/continue-dev-the-ai-coding-assistant-that-actually-respects-your-choices-1960b08e296a](https://medium.com/@info.booststash/continue-dev-the-ai-coding-assistant-that-actually-respects-your-choices-1960b08e296a)  
32. Best AI Coding Tools 2025: 15 Top Picks Compared & Reviewed \- Articsledge, 3월 18, 2026에 액세스, [https://www.articsledge.com/post/best-ai-coding-assistant-tools](https://www.articsledge.com/post/best-ai-coding-assistant-tools)  
33. How Claude Code works \- Claude Code Docs, 3월 18, 2026에 액세스, [https://code.claude.com/docs/en/how-claude-code-works](https://code.claude.com/docs/en/how-claude-code-works)  
34. Agentic Coding: The Basic Concepts \- Reflections, 3월 18, 2026에 액세스, [https://annjose.com/post/agentic-coding-basics/](https://annjose.com/post/agentic-coding-basics/)  
35. Tracing Claude Code's LLM Traffic: Agentic loop, sub-agents, tool use, prompts \- Medium, 3월 18, 2026에 액세스, [https://medium.com/@georgesung/tracing-claude-codes-llm-traffic-agentic-loop-sub-agents-tool-use-prompts-7796941806f5](https://medium.com/@georgesung/tracing-claude-codes-llm-traffic-agentic-loop-sub-agents-tool-use-prompts-7796941806f5)  
36. Let's build our own Agentic Loop, running in our own terminal, from scratch (Baby Manus) : r/AI\_Agents \- Reddit, 3월 18, 2026에 액세스, [https://www.reddit.com/r/AI\_Agents/comments/1js1xjz/lets\_build\_our\_own\_agentic\_loop\_running\_in\_our/](https://www.reddit.com/r/AI_Agents/comments/1js1xjz/lets_build_our_own_agentic_loop_running_in_our/)  
37. OpenCode vs Claude Code: Which Agentic Tool Should You Use in 2026? | DataCamp, 3월 18, 2026에 액세스, [https://www.datacamp.com/es/blog/opencode-vs-claude-code](https://www.datacamp.com/es/blog/opencode-vs-claude-code)  
38. OpenCode vs Claude Code \- Builder.io, 3월 18, 2026에 액세스, [https://www.builder.io/blog/opencode-vs-claude-code](https://www.builder.io/blog/opencode-vs-claude-code)  
39. OpenCode vs Claude Code: Which Agentic Tool Should You Use in 2026? | DataCamp, 3월 18, 2026에 액세스, [https://www.datacamp.com/blog/opencode-vs-claude-code](https://www.datacamp.com/blog/opencode-vs-claude-code)  
40. anomalyco/opencode: The open source coding agent. \- GitHub, 3월 18, 2026에 액세스, [https://github.com/anomalyco/opencode](https://github.com/anomalyco/opencode)  
41. Agents \- OpenCode, 3월 18, 2026에 액세스, [https://opencode.ai/docs/agents/](https://opencode.ai/docs/agents/)  
42. Setting up OpenCode and building stuff as a Product Manager | by Aayush Mishra | Feb, 2026 | Medium, 3월 18, 2026에 액세스, [https://medium.com/@thatshutterboi/setting-up-opencode-and-building-stuff-as-a-product-manager-bf2f57fce447](https://medium.com/@thatshutterboi/setting-up-opencode-and-building-stuff-as-a-product-manager-bf2f57fce447)  
43. Start of 2026 what’s the best open coding model?, 3월 18, 2026에 액세스, [https://www.reddit.com/r/LocalLLaMA/comments/1q82ae8/start\_of\_2026\_whats\_the\_best\_open\_coding\_model/](https://www.reddit.com/r/LocalLLaMA/comments/1q82ae8/start_of_2026_whats_the_best_open_coding_model/)  
44. The Best Open-Source LLMs in 2026 \- BentoML, 3월 18, 2026에 액세스, [https://www.bentoml.com/blog/navigating-the-world-of-open-source-large-language-models](https://www.bentoml.com/blog/navigating-the-world-of-open-source-large-language-models)  
45. Ultimate Guide \- The Best Open Source LLM For Enterprise Deployment in 2026, 3월 18, 2026에 액세스, [https://www.siliconflow.com/articles/en/best-open-source-llm-for-enterprise-deployment](https://www.siliconflow.com/articles/en/best-open-source-llm-for-enterprise-deployment)  
46. Best Open Source LLMs: Complete 2026 Guide | Contabo Blog, 3월 18, 2026에 액세스, [https://contabo.com/blog/open-source-llms/](https://contabo.com/blog/open-source-llms/)  
47. The State of Coding Agents Using Local LLMs — February 2026 | by Tom Ron \- Medium, 3월 18, 2026에 액세스, [https://medium.com/@rontom/the-state-of-coding-agents-using-local-llms-february-2026-83259140e6ec](https://medium.com/@rontom/the-state-of-coding-agents-using-local-llms-february-2026-83259140e6ec)  
48. Hardware and model recommendations for on-prem LLM deployment : r/LocalLLaMA, 3월 18, 2026에 액세스, [https://www.reddit.com/r/LocalLLaMA/comments/1nig0zp/hardware\_and\_model\_recommendations\_for\_onprem\_llm/](https://www.reddit.com/r/LocalLLaMA/comments/1nig0zp/hardware_and_model_recommendations_for_onprem_llm/)  
49. Run DeepSeek & Qwen 2.5 Locally: The 2026 Self-Hosted Guide, 3월 18, 2026에 액세스, [https://createaiagent.net/self-hosted-llm/](https://createaiagent.net/self-hosted-llm/)  
50. Kimi K2.5 in 2026: The Ultimate Guide to Open-Source Visual Agentic Intelligence \- Dev.to, 3월 18, 2026에 액세스, [https://dev.to/czmilo/kimi-k25-in-2026-the-ultimate-guide-to-open-source-visual-agentic-intelligence-18od](https://dev.to/czmilo/kimi-k25-in-2026-the-ultimate-guide-to-open-source-visual-agentic-intelligence-18od)  
51. Local AI Coding \- Full Tutorial 2026: No Enterprise Hardware Required \- YouTube, 3월 18, 2026에 액세스, [https://www.youtube.com/watch?v=ypaNNpi61Bw](https://www.youtube.com/watch?v=ypaNNpi61Bw)  
52. OpenCode: AI-Assisted Coding with Free and Local LLMs \- Infralovers, 3월 18, 2026에 액세스, [https://www.infralovers.com/blog/2026-02-27-opencode-free-local-llms/](https://www.infralovers.com/blog/2026-02-27-opencode-free-local-llms/)  
53. Modernizing legacy code with GitHub Copilot: Tips and examples, 3월 18, 2026에 액세스, [https://github.blog/ai-and-ml/github-copilot/modernizing-legacy-code-with-github-copilot-tips-and-examples/](https://github.blog/ai-and-ml/github-copilot/modernizing-legacy-code-with-github-copilot-tips-and-examples/)  
54. Deloitte Q\&A: Using GenAI to Unlock Legacy Code and Future-Proof Enterprise Systems, 3월 18, 2026에 액세스, [https://theaiinnovator.com/deloitte-qa-using-genai-to-unlock-legacy-code-and-future-proof-enterprise-systems/](https://theaiinnovator.com/deloitte-qa-using-genai-to-unlock-legacy-code-and-future-proof-enterprise-systems/)  
55. OpenCode vs Claude Code (2026): Open Source Freedom vs Anthropic Polish \- Morph, 3월 18, 2026에 액세스, [https://morphllm.com/comparisons/opencode-vs-claude-code](https://morphllm.com/comparisons/opencode-vs-claude-code)  
56. Vibe Coding vs. Agentic Coding: Fundamentals and Practical Implications of Agentic AI, 3월 18, 2026에 액세스, [https://arxiv.org/html/2505.19443v1](https://arxiv.org/html/2505.19443v1)  
57. How Design-to-Code Automation Works \- UXPin, 3월 18, 2026에 액세스, [https://www.uxpin.com/studio/blog/how-design-to-code-automation-works/](https://www.uxpin.com/studio/blog/how-design-to-code-automation-works/)  
58. How to Build an AI Agent: From Basic Components to Enterprise-Grade Systems \- Coveo, 3월 18, 2026에 액세스, [https://www.coveo.com/blog/how-to-build-an-ai-agent/](https://www.coveo.com/blog/how-to-build-an-ai-agent/)  
59. Paper2Code: Automating Code Generation from Scientific Papers in Machine Learning, 3월 18, 2026에 액세스, [https://arxiv.org/html/2504.17192v1](https://arxiv.org/html/2504.17192v1)  
60. Intro | AI coding agent built for the terminal \- OpenCode, 3월 18, 2026에 액세스, [https://opencode.ai/docs/](https://opencode.ai/docs/)  
61. OpenCode Agents: Another Path to Self-Healing Documentation Pipelines \- Medium, 3월 18, 2026에 액세스, [https://medium.com/@richardhightower/opencode-agents-another-path-to-self-healing-documentation-pipelines-51cd74580fc7](https://medium.com/@richardhightower/opencode-agents-another-path-to-self-healing-documentation-pipelines-51cd74580fc7)  
62. Auto Document Your Code: Tools & Best Practices Guide 2025, 3월 18, 2026에 액세스, [https://www.augmentcode.com/learn/auto-document-your-code-tools-and-best-practices](https://www.augmentcode.com/learn/auto-document-your-code-tools-and-best-practices)  
63. GitHub \- opencode-ai/opencode: A powerful AI coding agent. Built for the terminal., 3월 18, 2026에 액세스, [https://github.com/opencode-ai/opencode](https://github.com/opencode-ai/opencode)  
64. Inside OpenCode: How to Build an AI Coding Agent That Actually Works \- Medium, 3월 18, 2026에 액세스, [https://medium.com/@gaharwar.milind/inside-opencode-how-to-build-an-ai-coding-agent-that-actually-works-28c614494f4f](https://medium.com/@gaharwar.milind/inside-opencode-how-to-build-an-ai-coding-agent-that-actually-works-28c614494f4f)  
65. Building Agent Teams in OpenCode: Architecture of Multi-Agent Coordination, 3월 18, 2026에 액세스, [https://dev.to/uenyioha/porting-claude-codes-agent-teams-to-opencode-4hol](https://dev.to/uenyioha/porting-claude-codes-agent-teams-to-opencode-4hol)

---

## 변경이력

| 버전 | 일자 | 변경 내용 | 작성자 |
|------|------|----------|--------|
| 1.0 | 2026-03-19 | 초안 작성 (Gemini Deep Research 기반 시장 조사 및 기술 전략) | 시선AI |