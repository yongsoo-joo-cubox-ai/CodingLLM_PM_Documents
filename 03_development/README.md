# 03_development - 개발 진행 자료

이 폴더는 Coco 프로젝트의 개발 진행 과정에서 생성된 기술 문서, 테스트 결과, 벤치마크 리포트를 관리합니다.

---

## 폴더 구조

```
03_development/
├── README.md                         # 이 파일
├── 2026-01-15_project_intro/         # 프로젝트 소개 및 초기 벤치마크
│   ├── project_introduction.md       # CodeGen 프로젝트 소개
│   ├── load_test_qwen32b.md          # vLLM 부하 테스트 결과
│   └── model_benchmark.md            # 모델 품질 비교 벤치마크
│
├── 2026-01-24_progress/              # 1월 4주차 진행 현황
│   ├── vram_sizing.md                # 동시사용자 환경 VRAM 산정
│   ├── architecture_mcp.md           # MCP 아키텍처 변경사항
│   ├── lightweight_model_qa.md       # 경량 모델 QA 기능 테스트
│   ├── qa_test_report/               # 소프트베이스 QA 테스트 결과
│   ├── qa_examples/                  # xFrame5 Q&A 예제
│   ├── qa_update/                    # QA 기능 업데이트 내역
│   └── cli_test/                     # CLI 테스트 결과
│       ├── README.md                 # CLI 소개
│       └── cli_test_report.md        # CLI 테스트 상세 보고서
│
├── 2026-02-07_progress/              # 2월 1주차 진행 현황
│   ├── README.md                     # 1/26~2/7 진행 종합 요약
│   ├── uasl_spec/                    # UASL/SUIS 스펙 문서
│   │   ├── README.md                 # UASL 개요 및 변경 이력
│   │   ├── suis_spec_kr.md           # SUIS UI 스펙 (한글)
│   │   ├── suis_spec_en.md           # SUIS UI 스펙 (영문)
│   │   └── suis_prompts.yaml         # 프롬프트 템플릿
│   └── reports/                      # 보고서 (PDF→MD 변환)
│       ├── cgf_comparison_20260128.md    # CGF 전략 비교 벤치마크
│       └── qa_improvement_20260128.md    # QA 기능 개선 보고서
│
└── 2026-02-12_progress/              # 2월 2주차 진행 현황
    ├── README.md                     # Coco Studio 기능 테스트 요약
    └── coco_studio_test_report.md    # Studio 기능 테스트 보고서 (TC1~TC7)
```

---

## 문서 요약

### 2026-01-15: 프로젝트 시작

| 문서 | 설명 |
|------|------|
| `project_introduction.md` | CodeGen 프로젝트의 목적, 아키텍처, 주요 기능 소개 |
| `load_test_qwen32b.md` | Qwen2.5-Coder-32B-AWQ 모델의 vLLM 부하 테스트 결과 |
| `model_benchmark.md` | 4개 모델(gpt-oss, Qwen32B, Qwen7B, Mistral7B)의 품질 비교 |

**주요 발견사항:**
- vLLM Continuous Batching: 3.8x 성능 향상 확인
- gpt-oss:20b 모델이 94% 품질로 Production 최적
- 10 동시 사용자 기준 0.15 rps, 65초 응답 시간

### 2026-01-24: 1월 4주차 진행

| 문서/폴더 | 설명 |
|----------|------|
| `vram_sizing.md` | 동시 사용자 수에 따른 VRAM 크기 산정 방법 |
| `architecture_mcp.md` | MCP(Model Context Protocol) 기반 아키텍처 변경 공유 |
| `lightweight_model_qa.md` | 경량 모델에서의 QA 기능 테스트 결과 |
| `qa_test_report/` | 소프트베이스 xFrame5 코드 생성 및 QA 기능 검토 |
| `qa_examples/` | xFrame5 실제 Q&A 예제 (그리드, 팝업 등) |
| `qa_update/` | QA 기능 업데이트 내역 |
| `cli_test/` | Coco CLI 테스트 결과 (QA, Review 명령어) |

### 2026-02-07: 2월 1주차 진행

| 문서/폴더 | 설명 |
|----------|------|
| `README.md` | 1/26~2/7 진행 종합 요약 |
| `uasl_spec/` | UASL/SUIS 스펙 문서 (프레임워크 중립 UI 기술 언어) |
| `reports/` | CGF 비교 보고서, QA 기능 개선 보고서 |

**주요 성과:**
- MCP 서버 기반 아키텍처 전환 완료
- Vue3, xFrame5 코드 생성 및 프리뷰 기능 구현
- UASL/SUIS v1.1 스펙 확정
- 제품명 Coder → Coco (Coordinated Coding) 변경
- QA 환각 문제 해결 및 답변 검증 강화

### 2026-02-12: Coco Studio 기능 테스트

| 문서 | 설명 |
|------|------|
| `README.md` | Coco Studio 기능 테스트 요약 |
| `coco_studio_test_report.md` | Studio 기능 테스트 보고서 (TC1~TC7) |

**주요 결과:**
- 7개 테스트 케이스 실행, 통과율 71.4% (5/7)
- CGF-B 파이프라인 코드 생성 정상 동작 확인
- Review 모드 모델 태스크 설정 누락 발견
- 코드 프리뷰, RAG Q&A, Import, 다크모드 등 정상 확인

---

## 관련 링크

- [전략 문서](../01_strategy/) - 경영진 요약, 경쟁 전략, 규제 환경
- [구현 문서](../02_implementation/) - 로드맵, 비용 분석, API 레퍼런스
- [회의록](../04_meetings/) - 주요 미팅 기록
- [기술 참고자료](../05_knowledge_base/) - xFrame5 Knowledge Base 등
