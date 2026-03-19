# UASL — Universal Application Specification Language

> 애플리케이션을 의미론적 수준에서 기술하고, 어떤 프레임워크로든 코드를 생성합니다.

---

## UASL이란?

UASL은 4개의 선언적 사양으로 구성된 패밀리로, 도메인 모델, 사용자 인터페이스 의도, API 계약, 비즈니스 워크플로를 프레임워크, 프로그래밍 언어, 런타임에 종속되지 않고 기술합니다.

적합한 컴파일러가 UASL 문서를 읽고 대상 플랫폼(xframe5, Vue, React, Spring Boot 등)의 프로덕션 코드를 생성하며, 동일한 입력에서 항상 동일한 출력을 생성합니다.

## 사양 패밀리

| # | 사양 | 설명 | 버전 |
|---|------|------|------|
| 1 | [Entity Spec](02-entity-spec.md) | 도메인 모델: 엔티티, 속성, 관계 | v1.0 |
| 2 | [IAS](03-ias-spec.md) | API 계약: 의도-HTTP 매핑 | v1.0 |
| 3 | [SUIS](04-suis-spec.md) | UI 의도: 화면, 작업, 네비게이션 | v1.1 |
| 4 | [Workflow](05-workflow-spec.md) | 상태 기계: 상태, 전이, 가드 | v1.0 |

[개요](01-overview.md)에서 각 사양이 어떻게 연결되는지 먼저 파악하거나, 위의 개별 사양으로 바로 이동할 수 있습니다.

## 빠른 탐색

- [개요 — 아키텍처 및 설계 철학](01-overview.md)
- [Entity Spec — 도메인 모델](02-entity-spec.md)
- [IAS — 의도 API 사양](03-ias-spec.md)
- [SUIS — 의미적 UI 사양](04-suis-spec.md)
- [Workflow Spec — 상태 기계](05-workflow-spec.md)
- [용어집 — 전체 용어](glossary.md)
- [Training Guide — UASL 생성을 위한 LLM 프롬프트 엔지니어링](UASL_TRAINING_GUIDE.md)

## 읽기 순서

처음 읽는 분에게 권장하는 순서:

1. **[개요](01-overview.md)** — 전체 그림 이해
2. **[Entity Spec](02-entity-spec.md)** — 모든 사양의 기반
3. **[IAS](03-ias-spec.md)** — 의도가 HTTP에 매핑되는 방식
4. **[SUIS](04-suis-spec.md)** — UI가 의미론적으로 기술되는 방식
5. **[Workflow](05-workflow-spec.md)** — 상태 기계 동작 방식

[용어집](glossary.md)은 다른 사양을 읽을 때 함께 참조하면 유용합니다.

---

*UASL v1.0 — Candidate Recommendation — 2026-01-29*

[English Version](../en/README.md)
