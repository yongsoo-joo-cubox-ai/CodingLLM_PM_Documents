# 2026-03-19: 3월 진행 (02/12 ~ 03/19)

이 문서는 2026년 2월 12일 ~ 3월 19일 기간 동안의 개발 진행 사항을 종합 정리합니다.

> **이전 진행**: [2026-02-12 Coco Studio 기능 테스트](../2026-02-12_progress/) - Studio 웹 UI 전체 기능 검증 (7 TC, 통과율 71.4%)

---

## 주요 성과 요약

- 4B 모델(Qwen3-4B-Instruct) LoRA 파인튜닝 실험 완료 — UASL 지식 주입 확인
- UASL 스펙 2차례 업데이트 (v2: 2/25, v3: 3/11) — 복합 화면, 용어 정규화
- 서버 인프라 개선: Demo/Dev 서버 분리, Docker 기반 Playground 서버 구축
- Frontend-Backend 연동 Playground 구현
- **부산은행 PoC 긍정 검토** — 은행 내부 단말 개발 적용 검증 예정
- 제품 대외 명칭 **IntraGenX** 확정 (시선AI + 대보DX 합작 브랜딩)
- IntraGenX 소개서 Ver.1.0 제작 완료 (27슬라이드)

---

## 포함 문서

| 문서/폴더 | 설명 |
|----------|------|
| `model_finetuning_4b.md` | 4B 모델 LoRA 파인튜닝 실험 결과 보고서 |
| `uasl_spec/` | UASL 스펙 v2/v3 업데이트 변경 이력 |

---

## 4B 모델 지식 주입 실험

*2026-02-13 (황영준M)*

자연어 요구사항 → UASL YAML 명세 자동 변환을 위해 Qwen3-4B-Instruct 기반 LoRA 파인튜닝을 진행하였다.

- **Model1** (자연어 → Entity Spec): L1 100%, L2 100% — 목표 초과 달성
- **Model2** (자연어+Entity → IAS/SUIS/Workflow): L1 93.3%, L2 93.3% — 목표 달성. **L3 교차참조 26.7%** — 목표(50%) 미달

L3 미달 원인은 4B 모델이 긴 출력(3,000~5,000 토큰) 생성 시 IAS-SUIS intent 간 일관성을 유지하지 못하는 것이다. SUIS-IAS intent 불일치가 56%로 주요 원인.

향후: 교차참조 패턴 강조 데이터 증강 + RAG 기반 Base 모델 비교 검증 예정.

상세: [model_finetuning_4b.md](./model_finetuning_4b.md)

---

## UASL 스펙 업데이트

*2026-02-25, 2026-03-11*

이전 버전(2026-01-29 초기 릴리스)에서 2차례 업데이트가 진행되었다. 자세한 내용은 [uasl_spec/](./uasl_spec/) 참조.

### v2 (2026-02-25)

- **Entity Spec**: string/integer 타입에 `values` 지원 추가 (드롭다운 렌더링)
- **SUIS**: `values` 프로퍼티, `select` 필터 타입, 복합 화면(`master_detail`, `list_detail_panel`, `tabbed_detail`) 지원 추가

### v3 (2026-03-11)

- **SUIS**: 복합 화면 용어 정규화 — `list_detail_panel` → `split_view`, `tabbed_detail` → `tabbed_view`
- **CDS Schema**: `detected_screen_type` 값 변경 — `editor` → `form`, `detail` → `view` (하위 호환 유지)

---

## 서버 인프라 변경

*2026-03-17*

### Demo/Dev 서버 분리

| 환경 | Studio 포트 | Engine 포트 | 비고 |
|------|-----------|-----------|------|
| **Demo** | 5174 | 3100 | 고객 데모용 |
| **Dev** | 5173 | 3000 | 개발용 (기존 포트) |

- Demo 랜딩: http://172.16.100.116:5174/landing

### Playground Servers

기존 화면별 미리보기에서 **시스템 단위 전체 애플리케이션 배포**로 전환하였다.

- Docker를 이용해 프레임워크별 프론트엔드를 동적 포트에 배포
- 포트 규칙: `4000 + 프로젝트 ID` (프론트엔드)
- **Frontend-Backend 연동**: 생성된 REST API 서버(백엔드)와 연결하여 프론트엔드 화면 실행

---

## 부산은행 PoC 예정

*2026-03-17*

부산은행에서 내부 직원 단말(은행 내부 웹 애플리케이션) 개발에 IntraGenX를 적용하여 사용 가능한지 검증하는 PoC를 **긍정 검토**하기로 하였다.

- 김대표님 지시: 당분간 이 일에 집중
- 준비 사항 논의 필요

상세: [회의록 2026-03-17](../../04_meetings/2026-03-17_dev_update.md)

---

## IntraGenX 대외 브랜딩

*2026-03*

기존 Coco 제품을 대외적으로 **IntraGenX**로 리브랜딩하였다. 시선AI(The Brain — LLM 개발)와 대보DX(The Body — 애플리케이션 & 어플라이언스)의 합작 브랜드.

- IntraGenX 소개서 Ver.1.0 (27슬라이드) 제작 완료
- 소개서 위치: [`_00_work/ppt_assets/`](../../_00_work/ppt_assets/)

---

## 원본 파일 전체 목록

`_00_work/260212-260319/` 내 모든 파일에 대한 처리 현황입니다.

| 원본 파일 | 처리 방식 |
|---------|---------|
| `0213_4B 모델 지식 주입 실험 결과.md` | → `model_finetuning_4b.md` (정식 보고서로 변환) + 이 README에 요약 |
| `0225/0225_UASL_스펙_업데이트.md` | `uasl_spec/README.md`에 인라인 |
| `0225/dist/` | `uasl_spec/README.md`에서 참조 |
| `0312/0312_UASL_스펙_업데이트.md` | `uasl_spec/README.md`에 인라인 |
| `0312/dist/` | `uasl_spec/README.md`에서 참조 |
