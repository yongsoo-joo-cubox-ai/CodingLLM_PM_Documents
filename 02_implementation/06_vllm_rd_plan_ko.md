# 차세대 엔터프라이즈 AI 코딩 에이전트를 위한 vLLM 기반 인프라 고도화 및 보안 아키텍처 연구개발 계획서

| 항목 | 내용 |
|------|------|
| **문서번호** | SAI-IMPL-2026-006 |
| **작성일** | 2026년 3월 19일 |
| **버전** | v1.0 |
| **보안등급** | 대외비 |
| **작성** | Secern AI (Gemini Deep Research) |

> 참고 문서 | [폴더 인덱스](./README.md)

---

## **1\. 서론: 엔터프라이즈 AI 코딩 환경의 패러다임 변화와 인프라 고도화의 당위성**

현대의 엔터프라이즈 소프트웨어 개발 환경, 특히 대규모 시스템 통합(SI), 금융 기관, 공공 부문에서는 생성형 AI의 도입이 개발 생산성 극대화를 위한 필수 불가결한 요소로 자리 잡고 있다.1 인공지능 기반의 코딩 어시스턴트는 반복적인 보일러플레이트(Boilerplate) 코드를 자동화하고 개발 속도를 혁신적으로 단축하는 데 기여하고 있으며, 머지않아 대다수의 전문 개발자들이 이를 표준 워크플로우로 채택할 것으로 전망된다.1 그러나 이러한 파괴적 혁신 이면에는 기업의 핵심 자산인 소스 코드의 유출, 학습 데이터 오염, 그리고 강력한 규제 프레임워크 위반이라는 심각한 보안 및 컴플라이언스 과제가 존재한다.1

특히 보안 태세가 엄격한 기업의 최고정보보호책임자(CISO)와 보안 팀은 AI 도구를 도입할 때 데이터의 처리 위치와 저장 정책을 가장 우선적으로 평가한다.1 클라우드 API를 경유하여 코드를 전송하는 방식은 내부 정책뿐만 아니라 HIPAA, GDPR, SOC2와 같은 글로벌 보안 규제 프레임워크를 위반할 소지가 다분하며, API 키가 학습 데이터로 유출되어 타 조직의 코드 제안에 자사의 비공개 소스 코드가 노출되는 치명적인 보안 사고 사례도 지속적으로 보고되고 있다.1 이러한 환경적 제약으로 인해 코드가 외부망으로 유출되지 않도록 철저히 차단된 에어갭(Air-Gapped) 인프라 내에서 구동될 수 있는 온프레미스(On-premise) 솔루션의 도입은 선택이 아닌 필수가 되었다.1

현재 시선AI가 개발하여 시장에 선보인 'IntraGenX 1.0'은 코딩 자동화에 특화된 소형 거대언어모델(sLLM) 기반의 기업형 온프레미스 솔루션으로, 외부망이 차단된 폐쇄형 환경에서 구동되어 대기업 및 금융권의 엄격한 데이터 주권 요구사항을 충족하고 있다.1 그러나 기술적 완성도와 보안성에도 불구하고 시장의 반응은 다소 미온적인 상태에 머물러 있는데, 이는 개발자들이 체감하는 도구의 발전 속도와 기대 수준이 현재의 제공 범위를 넘어섰기 때문이다.1 최신의 AI 코딩 도구 시장은 단순히 명령에 따라 코드를 출력해 주는 단방향 엔진이나 IDE 내장형(IDE-First) 자동 완성 도구에서 벗어나, 자연어로 작업 목표를 지시하면 AI가 주도적으로 코드베이스를 읽고 계획(Plan)을 수립하며, 터미널 명령어를 실행(Execute)하여 자율적으로 코드를 수정 및 검증(Verify)하는 '자율형 에이전트(Autonomous Agent)' 중심으로 급격히 재편되고 있다.1

| 도구 철학 및 분류 | 대표 솔루션 아키텍처 | 핵심 상호작용 방식 및 기술적 한계 | 엔터프라이즈 환경 적합성 및 주요 사용 사례 |
| :---- | :---- | :---- | :---- |
| **IDE-First (에디터 내장형)** | Cursor, GitHub Copilot, Tabnine | 개발자가 주도권을 쥐고 코드를 작성하며, AI는 라인 단위의 자동 완성과 인라인 수정(Inline Diff)을 제안한다.1 미시적인 코드 수정에는 유리하나, 복잡한 다중 파일 수정이나 터미널 기반의 자율 실행 영역에서는 한계를 보인다.1 | 기존 IDE 환경을 유지하며 즉각적인 시각적 피드백이 필요한 작업 환경에 최적화되어 있으나, 중앙 집중식 거버넌스와 대규모 리팩토링에는 부적합하다.1 |
| **Agent-First (자율형 터미널)** | Claude Code, OpenCode, 시선AI (목표) | 자연어로 작업 목표를 지시하면, AI가 터미널 환경에서 스스로 코드의 의존성을 파악하고, 테스트 코드를 구동하며, 논리적 오류를 진단 및 수정하는 자율적 추론 능력(Agentic Reasoning)을 발휘한다.1 | 대규모 레거시 코드 리팩토링, 복잡한 시스템 아키텍처 개선, 심도 있는 문맥 파악이 필요한 거시적이고 독립적인 작업에 최적화되어 있다.1 |

이러한 패러다임의 변화를 수용하고 고객의 미온적인 반응을 타개하기 위해, 시선AI는 최신 오픈소스 프로젝트인 'OpenCode' 아키텍처를 기반으로 엔터프라이즈 워크플로우에 최적화된 자율형 CLI 에이전트를 개발하는 투트랙(Two-Track) 전략을 수립해야 한다.1 이 과정에서 필수적으로 요구되는 기술적 기반이 바로 대형 언어 모델의 고성능 추론 엔진인 vLLM의 도입과 맞춤형 고도화이다. vLLM은 PagedAttention 기술을 통해 주의 집중(Attention) 키(Key)와 값(Value) 메모리를 효율적으로 관리하고, 연속 배칭(Continuous Batching)을 통해 상태 최고 수준의 서버 처리량을 제공하는 업계 표준 추론 프레임워크이다.2

본 연구개발 계획서는 vLLM 엔진을 시선AI의 엔터프라이즈 환경에 맞게 커스터마이징하기 위한 기초 조사를 바탕으로 작성되었다. 구체적으로는 프로덕션 환경에서의 안전한 접근을 보장하기 위한 라이선스 인증 및 사내 인증(SSO/SAML) 시스템 적용 방안, 기업의 핵심 지식 재산인 모델 가중치(Weights)를 보호하기 위한 온더플라이(On-the-fly) 모델 암호화 튜닝 방안, 그리고 다중 에이전트 환경에서 다양한 크기와 목적의 모델을 동적으로 선택하고 라우팅하기 위해 LiteLLM 프록시를 활용하는 멀티 모델 셀렉션(Multi-Model Selection) 기능의 통합 방안을 심층적으로 다룬다. 이를 통해 보안과 자율성이라는 상충해 보이는 두 가지 난제를 완벽히 해결하고 글로벌 엔터프라이즈 AI 코딩 플랫폼 시장의 새로운 표준을 제시하고자 한다.1

## **2\. vLLM 코어 아키텍처 분석 및 FastAPI 기반 커스텀 인증 시스템 통합**

자율형 에이전트 시스템이 기업의 내부 네트워크에 성공적으로 안착하기 위해서는 추론 엔진 자체가 강력한 접근 통제 및 거버넌스 기능을 제공해야 한다. vLLM은 기본적으로 OpenAI API 규격과 완벽하게 호환되는 HTTP 서버를 제공하지만, 프로덕션 환경을 위한 복잡한 인증(Authentication) 및 인가(Authorization) 기능은 내장하고 있지 않다.5 기본적으로 제공되는 \--api-key 옵션은 단순한 정적 토큰 검증만을 수행하며, /v1 엔드포인트에 대해서만 보호를 제공할 뿐 다양한 엔드포인트에 대한 세밀한 접근 제어나 기업의 중앙 집중형 디렉토리 서비스와의 연동은 불가능하다.8 따라서 시선AI 자체 라이선스 인증 방식 및 사내 SSO/SAML 시스템을 적용하기 위해서는 vLLM 서버의 기본 프레임워크인 FastAPI의 미들웨어(Middleware) 아키텍처를 활용한 커스터마이징이 필수적이다.

### **2.1. ASGI 미들웨어를 활용한 vLLM 요청 파이프라인 개입**

vLLM의 OpenAI 호환 서버는 내부적으로 FastAPI를 사용하여 구축되어 있으며, 이는 비동기 서버 게이트웨이 인터페이스(ASGI) 표준을 따른다.10 FastAPI 프레임워크는 HTTP 요청이 특정 라우터(Router)나 컨트롤러에 도달하기 전, 그리고 응답이 클라이언트에게 반환되기 전에 요청과 응답을 가로채어 사전 처리(Pre-processing) 및 사후 처리를 수행할 수 있는 미들웨어 계층을 제공한다.12 vLLM은 서버 구동 시 \--middleware 커맨드라인 인수를 통해 외부에서 작성된 커스텀 ASGI 미들웨어 클래스나 함수의 임포트 경로(Import Path)를 전달받아 서버 앱에 동적으로 주입(app.add\_middleware())하는 확장성을 지원한다.15

엔터프라이즈 환경에서는 단순한 API 키 확인을 넘어, 라이선스 서버와의 통신, 요청 발신자의 IP 대역 확인, 속도 제한(Rate Limiting), 그리고 역할 기반 접근 제어(RBAC) 등 복합적인 보안 검증이 필요하다. 이를 위해 시선AI는 vLLM 서버 코드베이스를 직접 수정하는 대신, 독립적인 파이썬 패키지 형태의 보안 미들웨어를 개발하여 \--middleware 인수로 주입하는 방식을 채택해야 한다.16 이러한 접근법은 vLLM 코어 엔진의 업데이트나 버전 변경에 영향을 받지 않고 독자적인 보안 모듈을 유지보수할 수 있는 구조적 이점을 제공한다.17

미들웨어 구현체는 BaseHTTPMiddleware를 상속받거나 순수 ASGI 호출 규약인 \_\_call\_\_(self, scope, receive, send)을 구현하는 방식으로 작성될 수 있다.8 고성능 비동기 처리가 요구되는 LLM 추론 서버의 특성상, 스레드 안전성(Thread Safety)을 보장하고 불필요한 이벤트 루프 오버헤드를 최소화하기 위해 순수 ASGI 규약을 직접 구현하는 방식이 권장된다.8 미들웨어는 scope\["type"\]이 "http" 또는 "websocket"인 경우에만 개입하며, Authorization 헤더를 검사하여 토큰을 파싱하는 역할을 수행한다.8

### **2.2. 사내 인증 시스템(SSO/SAML) 및 자체 라이선스 검증 워크플로우 통합**

보안 태세가 엄격한 에어갭 인프라에서는 개별 개발자가 로컬에서 발급한 API 키를 사용하는 대신, 기업의 중앙 집중형 신원 제공자(IdP)를 통한 통합 인증 체계가 필수적이다.1 시선AI 솔루션은 기업 내부의 Active Directory, Okta, Microsoft Entra ID 등과 연동되는 SAML 2.0 기반의 SSO(Single Sign-On)를 지원해야 한다.1 이를 vLLM 미들웨어 수준에서 구현하기 위한 상세 워크플로우는 다음과 같다.

첫째, 토큰 추출 및 파싱 단계이다. 사용자가 터미널 기반 에이전트(OpenCode CLI 등)를 통해 자연어 명령을 내리면, 에이전트는 로컬에 저장된 세션 토큰(JWT 형태)을 HTTP 요청의 Authorization: Bearer \<token\> 헤더에 담아 vLLM 서버로 전송한다.22 커스텀 미들웨어는 이 헤더를 가로채어 토큰을 추출한다.22 만약 헤더가 누락되어 있거나 토큰 형식이 일치하지 않는 경우, 미들웨어는 vLLM 엔진으로 요청을 넘기지 않고 즉시 HTTP 401(Unauthorized) 응답을 반환하여 불법적인 접근과 리소스 낭비를 차단한다.22

둘째, 로컬 라이선스 및 토큰 유효성 검증 단계이다. 에어갭 환경의 특성상 외부 인터넷을 통한 외부 인증 서버와의 통신이 불가능하므로, 사내망 내부에 구축된 시선AI의 자체 라이선스 관리 서버 또는 사내 IdP 시스템과 통신해야 한다.1 미들웨어는 추출된 토큰의 서명을 검증하고, Redis와 같은 인메모리 데이터 저장소를 활용하여 해당 토큰의 폐기 여부(블랙리스트)와 만료 시간을 밀리초(ms) 단위로 확인한다.5 이 과정에서 라이선스의 동시 접속자 수 제한이나 누적 토큰 사용량 기반의 제한 로직을 함께 처리할 수 있다.5

셋째, 역할 기반 접근 제어(RBAC) 정보 주입 단계이다. 인증이 완료되면 미들웨어는 토큰의 페이로드(Payload)에서 사용자의 역할(Role) 정보를 추출한다.14 예를 들어, 일반 개발자는 소형 코드 자동 완성 모델에만 접근할 수 있고, 시니어 아키텍트는 대규모 리팩토링을 위한 대형 모델 추론 엔드포인트에 접근할 수 있도록 권한을 차등 부여할 수 있다.24 추출된 사용자 정보와 권한 메타데이터는 FastAPI의 request.state.user 객체에 저장되어, 후속 처리 파이프라인이나 로그 기록 시에 활용된다.24

| 인증 및 보안 처리 단계 | 미들웨어의 기술적 역할 및 구현 세부 사항 | 시선AI 엔터프라이즈 환경에서의 이점 |
| :---- | :---- | :---- |
| **요청 가로채기 (Intercept)** | HTTP 및 WebSocket 요청을 scope 레벨에서 분석하여 /v1 엔드포인트 접근을 식별하고 가로챈다. 헬스 체크(/health) 등은 예외 처리하여 서버 오버헤드를 줄인다.8 | 불필요한 모델 엔진 호출을 방지하고, 에이전틱 루프 실행 시 발생하는 대량의 동시 다발적 요청에 대해 1차적인 방어선을 제공한다.9 |
| **라이선스 및 토큰 검증** | Authorization: Bearer 헤더의 JWT 또는 시선AI 고유 라이선스 키를 로컬 라이선스 DB(Redis 등)와 대조하여 무결성 및 유효기간을 검증한다.5 | 클라우드 연결 없이 폐쇄망 내에서 라이선스 만료 및 허가되지 않은 사용자의 접근을 통제할 수 있어 완벽한 에어갭 운영을 보장한다.1 |
| **속도 제한 (Rate Limiting)** | 사용자별, 프로젝트별로 누적된 API 호출 횟수나 소모된 토큰량을 추적하여 초과 시 429(Too Many Requests) 에러를 반환한다.5 | 한정된 GPU 자원을 다수의 개발자가 공유하는 환경에서 특정 사용자의 과도한 호출로 인한 전체 시스템 마비(DoS)를 방지한다.5 |
| **RBAC 및 컨텍스트 주입** | 검증된 사용자 ID와 조직도 기반의 권한 정보를 request.state에 주입하여 이후 라우터에서 모델 접근 권한을 판단하도록 지원한다.14 | "책임 있는 채택(Responsible Adoption)"을 실현하기 위해, 사용자의 직급이나 프로젝트 권한에 따라 사용 가능한 AI 기능과 접근 가능한 코드 범위를 철저히 분리한다.1 |

결과적으로, vLLM의 FastAPI 미들웨어를 활용한 시선AI 자체 인증 아키텍처는 고성능 LLM 추론 파이프라인의 속도를 저하시키지 않으면서도, 엔터프라이즈 환경이 요구하는 엄격한 신원 확인, 상태 검증, 그리고 감사 추적(Audit Trailing) 요건을 완벽하게 충족시키는 기반 기술이 된다.9 이는 기업의 보안 팀과 CISO가 우려하는 인가되지 않은 AI 시스템 접근 및 코드 유출 위험을 원천적으로 차단하는 가장 효과적인 방법이다.1

## **3\. 지식 재산권 보호를 위한 모델 가중치 암호화(Model Weight Encryption) 튜닝 방안**

기업 내부 환경에 최적화되도록 도메인 특화 데이터와 비공개 소스 코드를 바탕으로 파인튜닝(Fine-tuning)된 소형 거대언어모델(sLLM)은 그 자체로 기업의 막대한 자본과 노하우가 집약된 핵심 지식 재산(Intellectual Property)이다.25 온프레미스 기반의 에어갭 환경에 AI 인프라를 배포하더라도, 서버의 물리적 디스크나 컨테이너 볼륨에 저장된 모델의 가중치(Weights) 파일이 평문(Plain-text) 형태로 존재할 경우 심각한 보안 취약점이 발생한다.27 서버에 대한 권한 탈취, 내부자의 악의적 접근, 또는 스토리지 유출 등의 침해 사고 발생 시 모델 파일 전체가 탈취되어 경쟁사에 유출되거나 역공학(Reverse Engineering)의 대상이 될 수 있기 때문이다.9

운영 체제 수준의 디스크 암호화(OS-level Encryption)나 전송 구간 암호화(TLS/mTLS)만으로는 시스템이 구동 중일 때 메모리에 상주하는 데이터나 런타임 환경에서의 유출을 완벽히 방지할 수 없다.29 이를 보안 업계에서는 '추론 신뢰 간극(Inference Trust Gap)'이라고 부르며, 이를 해결하기 위해서는 모델 가중치 파일 자체를 암호화하여 저장하고, 추론 엔진이 텐서를 로드하여 연산을 수행하는 GPU 메모리 적재 시점에만 일시적으로 복호화(On-the-fly Decryption)를 수행하는 튜닝이 필수적이다.30 vLLM은 이러한 고도의 보안 요구사항을 충족하기 위해 여러 확장 기능과 커스텀 모델 로더 생태계를 제공한다.

### **3.1. CoreWeave Tensorizer를 활용한 고속 텐서 암호화 및 런타임 복호화**

vLLM은 대용량 모델 가중치의 고속 로딩과 암호화를 동시에 지원하기 위해 CoreWeave가 개발한 **Tensorizer** 라이브러리를 네이티브로 통합하여 제공한다.31 기존의 PyTorch bin 포맷이나 safetensors 포맷을 사용할 경우 모델을 메모리에 올리고 역직렬화하는 과정에서 높은 CPU 오버헤드와 메모리 소비가 발생하지만, Tensorizer는 디스크나 S3 호환 객체 스토리지에 직렬화된 텐서 데이터를 GPU 메모리로 직접 스트리밍하여 로딩 시간을 극적으로 단축시킨다.31 가장 중요한 점은 이 과정에서 libsodium 라이브러리를 기반으로 한 강력한 텐서 가중치 암호화(Tensor Weight Encryption)를 지원한다는 것이다.32

시선AI의 사내 sLLM 가중치를 보호하기 위해 Tensorizer를 활용한 암호화 및 복호화 파이프라인은 다음과 같이 구축된다.

첫째, 모델 직렬화 및 암호화(Serialization & Encryption) 과정이다. 파인튜닝이 완료된 HuggingFace 표준 포맷의 모델을 배포하기 전에, vLLM이 제공하는 tensorize\_vllm\_model.py 스크립트를 사용하여 모델을 Tensorizer 포맷으로 변환한다.33 이때 커맨드라인 인수로 \--encryption-keyfile을 제공하거나 스크립트 내에서 EncryptionParams.random()을 통해 난수 기반의 강력한 암호화 키를 생성할 수 있다.32 암호화 과정에서 모델의 구조를 나타내는 메타데이터(텐서 이름, 데이터 타입, 형태 등)는 평문으로 남겨두어 빠른 구조 파악을 돕고, 실제 비즈니스 로직을 담고 있는 숫자 가중치 배열 자체만을 암호화하여 성능과 보안의 균형을 맞춘다.32 암호화된 가중치는 시선AI의 로컬 스토리지나 사내 폐쇄망 내의 S3 호환 스토리지에 안전하게 저장된다.34

둘째, vLLM 서버 구동 시의 동적 복호화(On-the-fly Decryption) 과정이다. 에어갭 환경의 추론 서버에서 vLLM을 시작할 때 \--load-format tensorizer 옵션을 부여하여 Tensorizer 로더를 활성화한다.35 암호화된 가중치를 복호화하기 위해서는 \--model-loader-extra-config 인수를 통해 TensorizerConfig의 JSON 문자열 형태로 암호화 키 파일의 경로(encryption\_keyfile)와 필요한 스토리지 자격 증명(S3 Credentials)을 주입해야 한다.37

Bash

\# vLLM 서버 암호화 모델 구동 예시  
vllm serve s3://internal-bucket/seyeon-sllm-encrypted/v1 \\  
  \--load-format tensorizer \\  
  \--model-loader-extra-config '{"encryption\_keyfile": "/secure/keys/master.key", "s3\_access\_key\_id": "...",...}'

vLLM 내부의 TensorizerArgs 클래스는 주입된 설정을 기반으로 암호화 키 파일을 읽어들여 DecryptionParams 객체를 생성하고, 이를 역직렬화(Deserialization) 파라미터로 전달한다.37 모델 로딩 시 데이터는 암호화된 상태로 메모리에 버퍼링되며, GPU로 전송되는 파이프라인의 최종 단계에서 복호화 알고리즘이 적용되어 평문 가중치가 GPU VRAM에 안전하게 적재된다.30 이 아키텍처를 채택하면 파일 시스템 접근 권한이 탈취되어 가중치 파일이 복사되더라도, 별도로 분리되어 안전하게 관리되는 암호화 키(Keyfile) 없이는 모델을 전혀 사용할 수 없게 되므로 데이터 주권과 지식 재산을 완벽하게 방어할 수 있다.9

### **3.2. 커스텀 모델 로더(register\_model\_loader)를 활용한 독자적 보안 체계 확장**

Tensorizer가 제공하는 기본 암호화 체계 외에, 금융권이나 공공기관의 특수한 보안 규정(예: 국정원 인증 암호 모듈 사용 의무화, 전용 하드웨어 보안 모듈(HSM)과의 통신 등)을 만족시켜야 하는 경우, vLLM의 확장성 높은 아키텍처를 활용하여 독자적인 커스텀 모델 로더를 구현할 수 있다.17

vLLM은 vllm.model\_executor.model\_loader.base\_loader.BaseModelLoader라는 추상 클래스를 제공하며, 이를 상속받아 기업 맞춤형 모델 다운로드 및 가중치 적재 로직을 재정의할 수 있다.39 또한 vllm.general\_plugins이라는 엔트리 포인트(Entry Point) 플러그인 시스템을 통해 vLLM의 핵심 코드를 수정하지 않고도 외부 패키지 형태의 보안 로더를 엔진 프로세스에 동적으로 주입할 수 있다.17

* **커스텀 복호화 로더 구현:** 사용자는 register\_model\_loader("seyeon\_secure\_loader") 함수를 호출하여 새로운 로드 포맷을 등록한다.39 이 커스텀 로더 클래스는 load\_weights 메서드 내부에서 사내 KMS(Key Management System)와 통신하여 실시간으로 복호화 키를 가져오는 로직을 수행할 수 있다.39  
* **후처리 파이프라인 튜닝:** vLLM의 weight\_utils.py에 정의된 composed\_weight\_loader와 같은 래퍼(Wrapper) 함수 패턴을 활용하면, 기본 포맷(예: Safetensors)으로 가중치를 읽어들인 직후, 텐서 데이터를 복사(param.data.copy\_)하기 직전의 단계에 커스텀 복호화 연산(fn(param))을 파이프라인으로 삽입할 수 있다.42

이러한 커스터마이징 기능은 최근 학계에서 제안된 **CryptoTensors**와 같이, 텐서 포맷 내부에 암호화된 가중치와 접근 제어 정책(Access Control Policies)을 함께 내장하여 파일 자체가 불법 실행을 방지하는 차세대 보안 포맷을 시선AI의 솔루션에 선도적으로 적용할 수 있는 강력한 기술적 토대가 된다.25 이와 같은 다층적인 모델 암호화 튜닝은 외부 유출에 대한 공포를 불식시키고, 기업이 안심하고 자체 비즈니스 데이터를 기반으로 모델을 고도화할 수 있는 안전한 환경을 보장한다.

## **4\. 멀티 모델 셀렉션(Multi-Model Selection) 기능 추가: LiteLLM 프록시 아키텍처**

엔터프라이즈 환경에서 자율형 AI 코딩 에이전트를 운영하기 위해서는 단일 언어 모델만으로는 모든 요구사항을 효율적으로 충족할 수 없다.1 OpenCode 기반의 에이전틱 루프(Agentic Loop)는 작업의 기획부터 실행, 검증까지 스스로 수행하는 다단계 프로세스로 구성되는데, 각 단계별로 요구되는 모델의 역량과 지연 시간(Latency) 목표가 상이하다.1 예를 들어, 에이전트가 로컬 파일의 단순 문법 오류를 검증(Verify)하거나 짧은 스크립트를 생성할 때는 응답 속도가 빠른 7B\~8B 규모의 소형 파라미터 모델이 적합하며, 복잡한 레거시 시스템의 구조를 파악하고 거시적인 리팩토링 계획(Plan)을 수립할 때는 높은 추론 능력을 갖춘 32B 이상의 대형 모델이 필수적이다.1

따라서 사용자의 지시 내용이나 에이전트의 작업 단계에 따라 가장 적합한 모델을 동적으로 선택하여 호출할 수 있는 '멀티 모델 셀렉션(Multi-Model Selection)' 기능은 비용 효율성과 시스템 성능을 최적화하기 위한 핵심 기술 요건이다.1

### **4.1. vLLM의 구조적 한계와 프록시 레이어의 당위성**

vLLM 엔진은 PagedAttention과 연속 배칭(Continuous Batching)을 통해 압도적인 처리량을 자랑하지만, 아키텍처 구조상 하나의 서버 인스턴스(컨테이너 또는 프로세스)가 메모리에 단일 베이스 모델(Base Model)만을 로드하여 서빙하도록 설계되어 있다.4 물론 동일한 베이스 모델 위에 여러 개의 LoRA 어댑터를 동적으로 교체하며 서빙하는 Multi-LoRA 기능은 지원하지만 2, 아키텍처가 완전히 다른 이종(Heterogeneous)의 다수 모델(예: Qwen-2.5 7B와 DeepSeek 32B)을 하나의 vLLM 프로세스와 단일 엔드포인트 포트에서 동시에 다중 서빙하는 것은 원천적으로 불가능하다.4

사용자의 쿼리에서 언급된 \*"멀티 모델 셀렉션은 liteLM인가 하는 다른 기술을 써야 한다고 봤는데 정확한 파악이 필요하다"\*는 질문에 대한 기술적인 결론은 \*\*"그렇다"\*\*이다.45 vLLM이 처리하지 못하는 멀티 모델 다중화 요구를 해결하기 위해서는 각기 다른 모델을 로드한 여러 개의 독립적인 vLLM 컨테이너를 구동하고, 그 앞단(Frontend)에 클라이언트의 요청을 분석하여 적절한 백엔드로 트래픽을 분배하는 **API 게이트웨이 및 라우팅 프록시(Proxy)** 계층을 별도로 구축해야 한다.4 Nginx와 같은 범용 리버스 프록시를 사용할 수도 있지만 47, LLM 생태계에 특화된 라우팅 정책, 모델 치환, 폴백(Fallback), 그리고 토큰 예산 관리를 통합적으로 제공하는 \*\*LiteLLM (Proxy Server)\*\*이 업계 표준이자 가장 강력한 아키텍처적 대안으로 평가받는다.4

### **4.2. LiteLLM 기반 멀티 모델 라우팅 및 오케스트레이션 아키텍처**

LiteLLM은 vLLM, Ollama, HuggingFace, OpenAI, Anthropic 등 100개 이상의 다양한 제공자와 백엔드를 단일 OpenAI API 규격으로 통합하여 호출할 수 있도록 해주는 지능형 프록시 서버이자 라우터이다.3 시선AI의 온프레미스 에이전트 인프라에 LiteLLM을 도입하면 다음과 같은 고도화된 엔터프라이즈 멀티 모델 셀렉션 및 라우팅 전략을 구현할 수 있다.

#### **(1) 모델 알리아싱(Aliasing) 및 단일 엔드포인트 제공**

개발자는 여러 포트와 IP를 기억할 필요 없이 LiteLLM 프록시의 단일 엔드포인트(예: http://localhost:4000/v1)만을 바라보게 된다.43 LiteLLM의 config.yaml 설정 파일을 통해 클라이언트가 호출하는 가상 모델명(model\_name)과 실제 뒷단에서 구동 중인 vLLM 서버의 주소(api\_base)를 논리적으로 매핑한다.51

**\[멀티 모델 라우팅 설정 예시: config.yaml\]**

YAML

model\_list:  
  \# 빠르고 가벼운 코드 작성용 소형 모델 (예: Qwen 7B)  
  \- model\_name: seyeon-fast-coder  
    litellm\_params:  
      model: openai/Qwen-2.5-Coder-7B   \# vLLM 백엔드임을 명시하는 openai/ 접두사 사용  
      api\_base: "http://vllm-backend-small:8000/v1"  
        
  \# 복잡한 아키텍처 계획용 대형 모델 (예: 파인튜닝된 32B 모델)  
  \- model\_name: seyeon-reasoning-agent  
    litellm\_params:  
      model: openai/Seyeon-IntraGenX-32B  
      api\_base: "http://vllm-backend-large:8001/v1"  
        
  \# Claude Code와 같은 외부 도구 호환성을 위한 와일드카드 라우팅  
  \- model\_name: claude-3-sonnet\*  
    litellm\_params:  
      model: openai/Seyeon-IntraGenX-32B  
      api\_base: "http://vllm-backend-large:8001/v1"

위 설정에서 openai/ 접두사는 해당 백엔드가 OpenAI 호환 API(즉, vLLM)를 사용함을 LiteLLM에게 알려주는 중요한 역할을 한다.51 이 구조를 통해 인프라 관리자는 클라이언트 코드의 수정 없이도 백엔드의 모델 버전을 무중단으로 교체하거나 추가할 수 있는 완벽한 인프라 디커플링(Decoupling)을 달성할 수 있다.53

#### **(2) 프로토콜 변환(Protocol Translation) 및 외부 도구 우회**

OpenCode나 Claude Code와 같이 종속성이 강한 상용 에이전트 도구를 에어갭 환경에서 사용하려면 클라우드 API 호출을 차단하고 로컬 모델로 우회시켜야 한다. LiteLLM은 클라이언트가 전송하는 Anthropic Messages API 포맷의 요청을 실시간으로 가로채어 OpenAI 호환 포맷으로 번역(Translation)한 후 vLLM으로 전달하는 기능을 제공한다.3 설정 파일의 와일드카드(claude-\*) 매핑을 통해 에이전트 도구가 클라우드 모델을 호출하려는 시도를 캡처하고, 이를 내부망의 가장 뛰어난 로컬 코더 모델(예: Qwen3-Coder)로 자동 라우팅하여 투명한 오프라인 환경을 조성할 수 있다.54

#### **(3) 동적 부하 분산(Load Balancing) 및 폴백(Fallback) 메커니즘**

대규모 SI 프로젝트 환경에서는 수백 명의 개발자가 동시에 코드를 생성하고 에이전트를 호출하므로 트래픽 병목이 발생하기 쉽다.1 LiteLLM은 동일한 model\_name 아래에 여러 개의 vLLM 백엔드 배포(Deployments)를 정의하고, 라우터 설정을 통해 가용성을 극대화할 수 있다.51

* **로드 밸런싱:** router\_settings에서 routing\_strategy를 least-busy(가장 대기열이 짧은 서버) 또는 latency-based(지연 시간이 가장 짧은 서버)로 설정하여, 다수의 vLLM 노드로 트래픽을 지능적으로 분산시켜 GPU 클러스터의 활용률을 극대화한다.51  
* **폴백(Fallback):** 주력 대형 모델 서버가 장애로 다운되거나 처리 한계에 도달하여 HTTP 에러를 반환할 경우, 자동으로 2차 모델(예: 여유 리소스가 있는 소형 모델)로 요청을 넘기는 폴백 로직을 구성하여 개발자의 작업 중단(Zero Downtime)을 방지한다.54

#### **(4) 거버넌스 및 비용/사용량 통제**

오픈소스 모델을 직접 호스팅하더라도 GPU 컴퓨팅 자원은 막대한 비용을 수반한다. LiteLLM은 관리자 웹 대시보드(UI)와 가상 키(Virtual Keys) 시스템을 제공하여, 개별 개발자나 팀, 프로젝트 단위로 할당량을 통제할 수 있다.48 분당 요청 수(RPM), 토큰 한도(TPM) 기반의 강력한 속도 제한(Rate Limiting)을 적용함으로써 특정 에이전트의 무한 루프 버그나 악의적인 과도한 호출로 인해 온프레미스 전체 인프라가 마비되는 현상을 사전에 방지하는 중앙 집중식 거버넌스를 제공한다.48

결과적으로, \*\*\[개발자 도구 (OpenCode)\] \-\> \[LiteLLM 프록시 및 라우터\] \-\> \[역할별 vLLM 클러스터\]\*\*로 이어지는 아키텍처는 시선AI가 지향하는 모델 독립적 유연성과 자율형 에이전트의 다중 협업을 엔터프라이즈 환경에서 가장 안정적으로 실현할 수 있는 궁극의 해답이다.1

## **5\. 시선AI 맞춤형 통합 R\&D 실행 로드맵 및 결론**

본 보고서에서 논의된 엔터프라이즈 보안 요구사항, vLLM의 확장 아키텍처, 그리고 LiteLLM의 멀티 모델 오케스트레이션 기술을 통합하여 시선AI의 차세대 에어갭 AI 코딩 에이전트를 구축하기 위한 4단계 R\&D 로드맵을 제안한다.

* **1단계: 코어 추론 엔진 및 암호화 인프라 구축 (M1-M2)**  
  * 사내 sLLM 가중치를 보호하기 위해 CoreWeave Tensorizer를 활용한 libsodium 기반의 텐서 직렬화 및 암호화 파이프라인을 구축한다.32  
  * vLLM 엔진에 \--load-format tensorizer를 적용하고, S3 호환 내부 스토리지와 연동하여 런타임 GPU 적재 시에만 동적 복호화가 이루어지도록 로더 아키텍처를 검증한다.35  
* **2단계: 보안 미들웨어 및 사내 인증 시스템(SSO/SAML) 통합 (M3-M4)**  
  * vLLM의 FastAPI 기반 서버에 순수 ASGI 규격을 따르는 커스텀 인증 미들웨어를 개발하고 \--middleware 옵션으로 주입한다.8  
  * 기업의 SSO/SAML 시스템 연동 및 JWT 파싱 로직을 구현하여 토큰의 유효성을 검사하고, 사용자 역할 정보를 기반으로 RBAC(역할 기반 접근 제어) 인가 프로세스를 완성한다.14  
* **3단계: 멀티 모델 셀렉션(LiteLLM) 기반 게이트웨이 도입 (M5-M6)**  
  * 단일 모델 서빙의 한계를 극복하기 위해 LiteLLM 프록시 서버를 인프라 앞단에 배치하여 중앙 집중형 API 게이트웨이를 구성한다.4  
  * config.yaml 설정을 통해 작업 복잡도에 따라 소형(7B) 및 대형(32B) vLLM 클러스터로 요청을 동적 분배(Load Balancing)하고, 에어갭 환경 내에서 완벽한 프라이빗 멀티 모델 오케스트레이션을 구축한다.43  
* **4단계: OpenCode 기반 자율형 에이전트 통합 및 최적화 (M7-M8)**  
  * 구축된 LiteLLM 게이트웨이의 와일드카드 라우팅(claude-\* \-\> openai/Seyeon-sLLM)을 통해 클라우드 모델 호출을 시도하는 OpenCode 에이전트의 통신을 가로채어 로컬 인프라로 투명하게 연동시킨다.54  
  * 에이전틱 루프(Ask, Plan, Execute, Verify)의 동작 주기에 개입하는 시스템 훅(Hooks)과 명시적 실행 승인 모델을 통해 보안 사고를 방지하고, 에어갭 특화 AI 에이전트를 상용화한다.1

### **결론**

기업용 소프트웨어 개발 생태계는 정적인 코드 완성을 넘어, 터미널 환경에서 주도적으로 문제를 해결하는 자율형 에이전트 파트너를 요구하고 있다.1 이러한 혁신적인 편의성과 강력한 데이터 주권 보장이라는 상충해 보이는 목표를 달성하기 위해, 시선AI는 vLLM이라는 압도적인 성능의 추론 엔진을 근간으로 삼아야 한다.2

단순히 엔진을 도입하는 것에 그치지 않고, FastAPI 미들웨어를 통한 사내 SSO/SAML 시스템의 매끄러운 연동 8, Tensorizer를 활용한 철벽 수준의 텐서 가중치 암호화 및 런타임 복호화 32, 그리고 LiteLLM 프록시를 통한 유연한 멀티 모델 셀렉션 및 로드 밸런싱 아키텍처 48를 성공적으로 결합해야만 한다. 본 연구에서 제안된 통합 아키텍처와 구체적인 튜닝 방안은 보안 우려로 AI 도입을 망설이는 보수적인 엔터프라이즈 고객의 신뢰를 확보하고, 시선AI가 차세대 온프레미스 AI 코딩 플랫폼 시장을 선도하기 위한 가장 확실하고 견고한 기술적 이정표가 될 것이다.

#### **참고 자료**

1. 오픈코드 기반 코딩 툴 개발 계획  
2. GitHub \- vllm-project/vllm: A high-throughput and memory-efficient inference and serving engine for LLMs, 3월 19, 2026에 액세스, [https://github.com/vllm-project/vllm](https://github.com/vllm-project/vllm)  
3. LiteLLM \- vLLM, 3월 19, 2026에 액세스, [https://docs.vllm.ai/en/stable/deployment/frameworks/litellm/](https://docs.vllm.ai/en/stable/deployment/frameworks/litellm/)  
4. Enabling model selection in vLLM Open AI compatible server : r/mlops \- Reddit, 3월 19, 2026에 액세스, [https://www.reddit.com/r/mlops/comments/1okosuq/enabling\_model\_selection\_in\_vllm\_open\_ai/](https://www.reddit.com/r/mlops/comments/1okosuq/enabling_model_selection_in_vllm_open_ai/)  
5. vLLM Quickstart: High-Performance LLM Serving \- in 2026 \- Rost Glukhov, 3월 19, 2026에 액세스, [https://www.glukhov.org/llm-hosting/vllm/vllm-quickstart/](https://www.glukhov.org/llm-hosting/vllm/vllm-quickstart/)  
6. OpenAI-Compatible Server \- vLLM, 3월 19, 2026에 액세스, [https://docs.vllm.ai/en/latest/serving/openai\_compatible\_server.html](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html)  
7. Code Review: Deep Dive into vLLM's Architecture and Implementation Analysis of OpenAI-Compatible Serving (1/2) | Zerohertz, 3월 19, 2026에 액세스, [https://zerohertz.github.io/vllm-openai-1/](https://zerohertz.github.io/vllm-openai-1/)  
8. server\_utils \- vLLM, 3월 19, 2026에 액세스, [https://docs.vllm.ai/en/latest/api/vllm/entrypoints/openai/server\_utils/](https://docs.vllm.ai/en/latest/api/vllm/entrypoints/openai/server_utils/)  
9. vLLM in Production: A Security Hardening Guide for Enterprise Deployments \- Medium, 3월 19, 2026에 액세스, [https://medium.com/@michael.hannecke/vllm-in-production-a-security-hardening-guide-for-enterprise-deployments-56a9c2c213dd](https://medium.com/@michael.hannecke/vllm-in-production-a-security-hardening-guide-for-enterprise-deployments-56a9c2c213dd)  
10. Code Review: Deep Dive into vLLM's Architecture and Implementation Analysis of OpenAI-Compatible Serving (2/2) | Zerohertz, 3월 19, 2026에 액세스, [https://zerohertz.github.io/vllm-openai-2/](https://zerohertz.github.io/vllm-openai-2/)  
11. Architecting Scalable FastAPI Systems for Large Language Model (LLM) Applications and External Integrations | by Ali moradi | Medium, 3월 19, 2026에 액세스, [https://medium.com/@moradikor296/architecting-scalable-fastapi-systems-for-large-language-model-llm-applications-and-external-cf72f76ad849](https://medium.com/@moradikor296/architecting-scalable-fastapi-systems-for-large-language-model-llm-applications-and-external-cf72f76ad849)  
12. Create custom middleware with FastAPI \- YouTube, 3월 19, 2026에 액세스, [https://www.youtube.com/watch?v=P3zdVdb-yn8](https://www.youtube.com/watch?v=P3zdVdb-yn8)  
13. Middleware \- FastAPI, 3월 19, 2026에 액세스, [https://fastapi.tiangolo.com/tutorial/middleware/](https://fastapi.tiangolo.com/tutorial/middleware/)  
14. Building Custom Middleware in FastAPI \- Semaphore, 3월 19, 2026에 액세스, [https://semaphore.io/blog/custom-middleware-fastapi](https://semaphore.io/blog/custom-middleware-fastapi)  
15. vllm serve, 3월 19, 2026에 액세스, [https://docs.vllm.ai/en/stable/cli/serve/](https://docs.vllm.ai/en/stable/cli/serve/)  
16. Chapter 2\. vLLM server usage \- Red Hat Documentation, 3월 19, 2026에 액세스, [https://docs.redhat.com/en/documentation/red\_hat\_ai\_inference\_server/3.1/html/vllm\_server\_arguments/vllm-server-usage\_server-arguments](https://docs.redhat.com/en/documentation/red_hat_ai_inference_server/3.1/html/vllm_server_arguments/vllm-server-usage_server-arguments)  
17. vLLM's Plugin System, 3월 19, 2026에 액세스, [https://docs.vllm.ai/en/v0.7.1/design/plugin\_system.html](https://docs.vllm.ai/en/v0.7.1/design/plugin_system.html)  
18. Architecture Overview \- vLLM, 3월 19, 2026에 액세스, [https://docs.vllm.ai/en/latest/design/arch\_overview.html](https://docs.vllm.ai/en/latest/design/arch_overview.html)  
19. How to write a custom FastAPI middleware class \- Stack Overflow, 3월 19, 2026에 액세스, [https://stackoverflow.com/questions/71525132/how-to-write-a-custom-fastapi-middleware-class](https://stackoverflow.com/questions/71525132/how-to-write-a-custom-fastapi-middleware-class)  
20. Top 5 authentication solutions for secure FastAPI apps in 2026 \- WorkOS, 3월 19, 2026에 액세스, [https://workos.com/blog/top-authentication-solutions-fastapi-2026](https://workos.com/blog/top-authentication-solutions-fastapi-2026)  
21. how to protect an API in fastapi using SAML SSO \- Stack Overflow, 3월 19, 2026에 액세스, [https://stackoverflow.com/questions/70811132/how-to-protect-an-api-in-fastapi-using-saml-sso](https://stackoverflow.com/questions/70811132/how-to-protect-an-api-in-fastapi-using-saml-sso)  
22. How to Build Authentication Middleware in FastAPI \- OneUptime, 3월 19, 2026에 액세스, [https://oneuptime.com/blog/post/2026-01-25-fastapi-authentication-middleware/view](https://oneuptime.com/blog/post/2026-01-25-fastapi-authentication-middleware/view)  
23. SAML Authentication in FastAPI \+ Streamlit using EntraID | by Roberto Hernández \- Medium, 3월 19, 2026에 액세스, [https://medium.com/@robertohdz98/saml-authentication-in-fastapi-streamlit-using-entraid-6c4c2a9a6615](https://medium.com/@robertohdz98/saml-authentication-in-fastapi-streamlit-using-entraid-6c4c2a9a6615)  
24. FastAPI Authentication Middleware Example | Backend APIs, Web Apps, Bots & Automation, 3월 19, 2026에 액세스, [https://hrekov.com/blog/fastapi-authentication-middlewre](https://hrekov.com/blog/fastapi-authentication-middlewre)  
25. CryptoTensors: A Light-Weight Large Language Model File Format for Highly-Secure Model Distribution \- arXiv.org, 3월 19, 2026에 액세스, [https://arxiv.org/html/2512.04580v1](https://arxiv.org/html/2512.04580v1)  
26. CryptoTensors: A Light-Weight Large Language Model File Format for Highly-Secure Model Distribution \- arXiv, 3월 19, 2026에 액세스, [https://arxiv.org/html/2512.04580v2](https://arxiv.org/html/2512.04580v2)  
27. Local LLM Security 2026 | Enterprise Best Practices \- SitePoint, 3월 19, 2026에 액세스, [https://www.sitepoint.com/local-llm-security-best-practices-2026/](https://www.sitepoint.com/local-llm-security-best-practices-2026/)  
28. On-Premise LLM Deployment: Secure & Scalable AI Solutions \- TrueFoundry, 3월 19, 2026에 액세스, [https://www.truefoundry.com/blog/on-prem-llms](https://www.truefoundry.com/blog/on-prem-llms)  
29. Local LLM Deployment: Privacy-First AI Complete Guide, 3월 19, 2026에 액세스, [https://www.digitalapplied.com/blog/local-llm-deployment-privacy-guide-2025](https://www.digitalapplied.com/blog/local-llm-deployment-privacy-guide-2025)  
30. Confidential Computing for AI Agents and Apps \- Super Protocol, 3월 19, 2026에 액세스, [https://superprotocol.com/resources](https://superprotocol.com/resources)  
31. Loading models with CoreWeave's Tensorizer \- vLLM, 3월 19, 2026에 액세스, [https://docs.vllm.ai/en/stable/models/extensions/tensorizer/](https://docs.vllm.ai/en/stable/models/extensions/tensorizer/)  
32. coreweave/tensorizer: Module, Model, and Tensor Serialization/Deserialization \- GitHub, 3월 19, 2026에 액세스, [https://github.com/coreweave/tensorizer](https://github.com/coreweave/tensorizer)  
33. Tensorize vLLM Model, 3월 19, 2026에 액세스, [https://docs.vllm.ai/en/v0.4.1/getting\_started/examples/tensorize\_vllm\_model.html](https://docs.vllm.ai/en/v0.4.1/getting_started/examples/tensorize_vllm_model.html)  
34. Tensorize vLLM Model, 3월 19, 2026에 액세스, [https://docs.vllm.ai/en/latest/examples/others/tensorize\_vllm\_model/](https://docs.vllm.ai/en/latest/examples/others/tensorize_vllm_model/)  
35. Tensorize vLLM Model, 3월 19, 2026에 액세스, [https://docs.vllm.ai/en/stable/examples/others/tensorize\_vllm\_model/](https://docs.vllm.ai/en/stable/examples/others/tensorize_vllm_model/)  
36. Tensorize vLLM Model \- Read the Docs, 3월 19, 2026에 액세스, [https://nm-vllm.readthedocs.io/en/latest/getting\_started/examples/tensorize\_vllm\_model.html](https://nm-vllm.readthedocs.io/en/latest/getting_started/examples/tensorize_vllm_model.html)  
37. tensorizer \- vLLM, 3월 19, 2026에 액세스, [https://docs.vllm.ai/en/latest/api/vllm/model\_executor/model\_loader/tensorizer/](https://docs.vllm.ai/en/latest/api/vllm/model_executor/model_loader/tensorizer/)  
38. Tensorize vLLM Model, 3월 19, 2026에 액세스, [https://docs.vllm.ai/en/v0.5.0.post1/getting\_started/examples/tensorize\_vllm\_model.html](https://docs.vllm.ai/en/v0.5.0.post1/getting_started/examples/tensorize_vllm_model.html)  
39. vllm.model\_executor.model\_loader, 3월 19, 2026에 액세스, [https://docs.vllm.ai/en/latest/api/vllm/model\_executor/model\_loader/](https://docs.vllm.ai/en/latest/api/vllm/model_executor/model_loader/)  
40. Plugin System \- vLLM, 3월 19, 2026에 액세스, [https://docs.vllm.ai/en/v0.10.1/design/plugin\_system.html](https://docs.vllm.ai/en/v0.10.1/design/plugin_system.html)  
41. vllm/vllm/model\_executor/model\_loader/\_\_init\_\_.py at main \- GitHub, 3월 19, 2026에 액세스, [https://github.com/vllm-project/vllm/blob/main/vllm/model\_executor/model\_loader/\_\_init\_\_.py](https://github.com/vllm-project/vllm/blob/main/vllm/model_executor/model_loader/__init__.py)  
42. weight\_utils \- vLLM, 3월 19, 2026에 액세스, [https://docs.vllm.ai/en/latest/api/vllm/model\_executor/model\_loader/weight\_utils/](https://docs.vllm.ai/en/latest/api/vllm/model_executor/model_loader/weight_utils/)  
43. Implementing LLM Model Routing: A Practical Guide with Ollama and LiteLLM \- Medium, 3월 19, 2026에 액세스, [https://medium.com/@michael.hannecke/implementing-llm-model-routing-a-practical-guide-with-ollama-and-litellm-b62c1562f50f](https://medium.com/@michael.hannecke/implementing-llm-model-routing-a-practical-guide-with-ollama-and-litellm-b62c1562f50f)  
44. Run multiple models \- General \- vLLM Forums, 3월 19, 2026에 액세스, [https://discuss.vllm.ai/t/run-multiple-models/1181](https://discuss.vllm.ai/t/run-multiple-models/1181)  
45. 3월 19, 2026에 액세스, [https://discuss.vllm.ai/t/how-to-serve-two-vllm-instance-using-docker/2405\#:\~:text=vLLM%20does%20not%20support%20serving,on%20the%20model%20or%20endpoint.](https://discuss.vllm.ai/t/how-to-serve-two-vllm-instance-using-docker/2405#:~:text=vLLM%20does%20not%20support%20serving,on%20the%20model%20or%20endpoint.)  
46. vLLM serve multiple models? : r/LocalLLaMA \- Reddit, 3월 19, 2026에 액세스, [https://www.reddit.com/r/LocalLLaMA/comments/1jprvw9/vllm\_serve\_multiple\_models/](https://www.reddit.com/r/LocalLLaMA/comments/1jprvw9/vllm_serve_multiple_models/)  
47. Scalable Multi-Model LLM Serving with vLLM and Nginx | by Doil Kim \- Medium, 3월 19, 2026에 액세스, [https://medium.com/@kimdoil1211/scalable-multi-model-llm-serving-with-vllm-and-nginx-f586912e17da](https://medium.com/@kimdoil1211/scalable-multi-model-llm-serving-with-vllm-and-nginx-f586912e17da)  
48. Quick Start \- LiteLLM Proxy CLI, 3월 19, 2026에 액세스, [https://docs.litellm.ai/docs/proxy/quick\_start](https://docs.litellm.ai/docs/proxy/quick_start)  
49. LiteLLM \- Getting Started | liteLLM, 3월 19, 2026에 액세스, [https://docs.litellm.ai/](https://docs.litellm.ai/)  
50. vLLM \- LiteLLM Docs, 3월 19, 2026에 액세스, [https://docs.litellm.ai/docs/providers/vllm](https://docs.litellm.ai/docs/providers/vllm)  
51. Overview \- LiteLLM Docs, 3월 19, 2026에 액세스, [https://docs.litellm.ai/docs/proxy/configs](https://docs.litellm.ai/docs/proxy/configs)  
52. OpenAI-Compatible Endpoints \- LiteLLM, 3월 19, 2026에 액세스, [https://docs.litellm.ai/docs/providers/openai\_compatible](https://docs.litellm.ai/docs/providers/openai_compatible)  
53. Add vLLM Model to LiteLLM \- Cake, 3월 19, 2026에 액세스, [https://docs.cake.ai/docs/add-vllm-model-to-litellm](https://docs.cake.ai/docs/add-vllm-model-to-litellm)  
54. Managing Local LLM Orchestration \- DGX Spark / GB10 Projects \- NVIDIA Developer Forums, 3월 19, 2026에 액세스, [https://forums.developer.nvidia.com/t/managing-local-llm-orchestration/363264](https://forums.developer.nvidia.com/t/managing-local-llm-orchestration/363264)  
55. Load Balancing \- Router \- LiteLLM Docs, 3월 19, 2026에 액세스, [https://docs.litellm.ai/docs/routing](https://docs.litellm.ai/docs/routing)

---

## 변경이력

| 버전 | 일자 | 변경 내용 | 작성자 |
|------|------|----------|--------|
| 1.0 | 2026-03-19 | Gemini Deep Research 기반 초안 작성 (인증/암호화/LiteLLM 멀티 모델 셀렉션) | 시선AI |