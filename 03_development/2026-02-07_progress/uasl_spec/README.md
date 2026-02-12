# UASL/SUIS 스펙 문서

UASL(Universal Application Specification Language)은 프레임워크 중립적인 UI 기술 언어입니다.
SUIS(Structured UI Specification)는 UASL의 UI 스펙 하위 규격입니다.

---

## 개요

UASL은 LLM이 특정 프레임워크에 종속되지 않는 UI 스펙을 생성하고, MCP 컴파일러가 이를 대상 프레임워크(xFrame5, Vue, Spring 등)의 코드로 변환하는 구조를 지원합니다.

- 사람이 읽기 위한 배포본: UASL-dist
- LLM에게 제공하는 스펙: UASL-specs
- 현재 사용 중인 프롬프트 템플릿: `suis_prompts.yaml`

---

## 포함 문서

| 파일 | 설명 |
|------|------|
| `suis_spec_kr.md` | SUIS UI 스펙 (한글) |
| `suis_spec_en.md` | SUIS UI 스펙 (영문) |
| `suis_prompts.yaml` | 프롬프트 템플릿 |

---

## 관련 배포 파일 (원본 위치)

아래 zip 파일들은 `_00_work/260127-260211/`에 원본이 보관되어 있습니다.

| 파일 | 설명 |
|------|------|
| [`0129_UASL-dist.zip`](../../../_00_work/260127-260211/0129_UASL-dist.zip) | UASL 사람용 배포본 (2026-01-29) |
| [`0129_UASL-specs.zip`](../../../_00_work/260127-260211/0129_UASL-specs.zip) | UASL LLM용 스펙 (2026-01-29) |
| [`0204_dist.zip`](../../../_00_work/260127-260211/0204_dist.zip) | UASL 보완 업데이트 배포 (2026-02-04) |

---

## 변경 이력

### 2026-01-29: 초기 스펙 공유

회의 중에 설명한 UASL(Universal Application Specification Language) 관련 스펙 문서입니다.
읽기는 UASL-dist.zip이 낫고, LLM에게는 UASL-specs.zip를 주는 게 나을 겁니다.
suis_prompts.yaml은 이 스펙에 따라 현재 사용 중인 프롬프트 템플릿입니다.

UI 스펙(SUIS)에 약간의 변경 사항이 있어 해당 파일만 다시 공유합니다. (하나는 영문 스펙, 다른 하나는 한글 스펙)

### 2026-02-04: 스펙 업데이트

몇 가지 보완 사항이 있어서 다시 배포합니다.
- [`dist.zip`](../../../_00_work/260127-260211/0204_dist.zip)
