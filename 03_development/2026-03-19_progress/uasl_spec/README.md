# UASL 스펙 업데이트 이력 (2026-02-25 ~ 2026-03-11)

이 문서는 UASL(Universal Application Specification Language) 스펙의 v2, v3 업데이트 변경 이력을 정리합니다.

> **이전 버전**: [2026-02-07 UASL/SUIS 스펙](../../2026-02-07_progress/uasl_spec/) — 초기 릴리스 (2026-01-29)

---

## 현재 버전

- **UASL Version**: 1.0
- **최신 문서 일자**: 2026-03-11
- **Status**: Candidate Recommendation

---

## 변경 이력

### v3 — 2026-03-11

**SUIS (04-suis-spec.md)**
- 복합 화면 용어 정규화:
  - `list_detail_panel` → `split_view`
  - `tabbed_detail` → `tabbed_view`
- Composition 문서, child properties 테이블, purpose-composition 제약 조건에 새 이름 반영
- `tab_label` 설명에서 `tabbed_view` 참조로 업데이트

**CDS Schema (cds_v1.schema.json)**
- `detected_screen_type` 값 변경:
  - `editor` → `form`
  - `detail` → `view`
  - `list_detail_panel` → `split_view`
  - `tabbed_detail` → `tabbed_view`
- 하위 호환: 기존 이름을 enum에 유지 (엔진이 파싱 시 정규화)

### v2 — 2026-02-25

**Entity Spec (02-entity-spec.md)**
- "Values on Non-Enum Types" 섹션 추가 — `string`/`integer` 속성에서 `values` 지원 (저장 타입 변경 없이 드롭다운 렌더링)
- 예시 변경: `priority`를 `type: enum`에서 `type: string` + `values`로 변경

**SUIS (04-suis-spec.md)**
- "Field Values" 섹션 추가 — `format: enum` 필드의 `values` 프로퍼티
- `select` 필터 입력 타입 추가 (`dropdown`의 별칭)
- 복합 화면 purpose 추가: `master_detail`, `list_detail_panel`, `tabbed_detail`
- "Composition" 섹션 추가 — 부모-자식 엔티티 관계의 복합 화면 구성
- Child properties 참조 테이블 및 purpose-composition 제약 조건 추가

**Dist package**
- `docs/dist/`에서 `docs/specs/dist/`로 이동 (소스 스펙과 같은 위치)

### v1 — 2026-01-29 (초기 릴리스)

- UASL Documentation Package 최초 배포
- 4개 스펙 모두 Candidate Recommendation 상태
- 이중 언어 문서 (English + Korean)
- LLM Training Guide 포함

---

## 스펙 문서 구성

각 버전의 dist 패키지는 `_00_work/260212-260319/` 내 해당 날짜 폴더에 보관되어 있습니다.

| 문서 | 설명 |
|------|------|
| `01-overview.md` | UASL 아키텍처, 설계 철학, 적합성 |
| `02-entity-spec.md` | Entity Spec — 도메인 모델 정의 |
| `03-ias-spec.md` | IAS — intent-to-API 매핑 |
| `04-suis-spec.md` | SUIS — 시맨틱 UI 명세 |
| `05-workflow-spec.md` | Workflow Spec — 상태 머신 정의 |
| `glossary.md` | 용어 사전 |
| `UASL_TRAINING_GUIDE.md` | LLM 학습 가이드 |

### Dist 패키지 위치

| 버전 | 위치 |
|------|------|
| v3 (2026-03-11) | [`_00_work/260212-260319/0312/dist/`](../../../_00_work/260212-260319/0312/dist/) |
| v2 (2026-02-25) | [`_00_work/260212-260319/0225/dist/`](../../../_00_work/260212-260319/0225/dist/) |
| v1 (2026-01-29) | [`_00_work/260127-260211/0129_UASL-dist.zip`](../../../_00_work/260127-260211/0129_UASL-dist.zip) |
