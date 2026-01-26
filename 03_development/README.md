# 03_development - 개발 진행 자료

이 폴더는 Coder 프로젝트의 개발 진행 과정에서 생성된 기술 문서, 테스트 결과, 벤치마크 리포트를 관리합니다.

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
└── 2026-01-24_progress/              # 1월 4주차 진행 현황
    ├── vram_sizing.md                # 동시사용자 환경 VRAM 산정
    ├── architecture_mcp.md           # MCP 아키텍처 변경사항
    ├── lightweight_model_qa.md       # 경량 모델 QA 기능 테스트
    ├── qa_test_report/               # 소프트베이스 QA 테스트 결과
    ├── qa_examples/                  # xFrame5 Q&A 예제
    ├── qa_update/                    # QA 기능 업데이트 내역
    └── cli_test/                     # CLI 테스트 결과
        ├── README.md                 # CLI 소개
        └── cli_test_report.md        # CLI 테스트 상세 보고서
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
| `cli_test/` | Coder CLI 테스트 결과 (QA, Review 명령어) |

---

## 관련 링크

- [전략 문서](../01_strategy/) - 경영진 요약, 경쟁 전략, 규제 환경
- [구현 문서](../02_implementation/) - 로드맵, 비용 분석, API 레퍼런스
- [회의록](../04_meetings/) - 주요 미팅 기록
- [기술 참고자료](../05_knowledge_base/) - xFrame5 Knowledge Base 등
