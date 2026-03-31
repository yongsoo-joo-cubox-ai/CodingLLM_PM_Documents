# 문서 구조 및 목록

> 이 문서는 CLAUDE.md의 레퍼런스입니다. 핵심 지침은 [CLAUDE.md](../../CLAUDE.md)를 참조하세요.

## 폴더 구조

```
CodingLLM_PM_Documents/
├── 01_strategy/           # 전략 문서
│   ├── 01_executive_summary_ko.md
│   ├── 02_competitive_strategy_ko.md
│   ├── 03_regulatory_environment_ko.md
│   ├── 04_product_overview_ko.md
│   └── 05_track2_tech_strategy_ko.md
│
├── 02_implementation/     # 구현 문서
│   ├── 01_roadmap_ko.md
│   ├── 02_resource_plan_ko.md
│   ├── 03_cost_analysis_ko.md
│   ├── 04_phase2_tech_stack_ko.md
│   ├── 05_api_reference_ko.md
│   ├── 06_vllm_rd_plan_ko.md
│   ├── 07_secerncode_status_ko.md
│   ├── 08_vllm_infra_prd_ko.md
│   └── 09_vllm_infra_roadmap_ko.md
│
├── 03_development/        # 개발 진행 자료
│   ├── README.md          # 개발 현황 인덱스
│   ├── 2026-01-15_project_intro/
│   │   ├── project_introduction.md
│   │   ├── load_test_qwen32b.md
│   │   └── model_benchmark.md
│   ├── 2026-01-24_progress/
│   │   ├── vram_sizing.md
│   │   ├── architecture_mcp.md
│   │   ├── lightweight_model_qa.md
│   │   ├── qa_test_report/
│   │   ├── qa_examples/
│   │   ├── qa_update/
│   │   └── cli_test/
│   ├── 2026-02-07_progress/
│   │   ├── README.md              # 1/26~2/7 진행 종합 요약
│   │   ├── uasl_spec/             # UASL/SUIS 스펙 문서
│   │   └── reports/               # CGF 비교, QA 개선 보고서
│   ├── 2026-02-12_progress/
│   │   └── coco_studio_test_report.md  # Studio 기능 테스트 (TC1~TC7)
│   └── 2026-03-19_progress/
│       ├── README.md              # 2/12~3/19 진행 종합 요약
│       ├── model_finetuning_4b.md # 4B 모델 LoRA 파인튜닝 실험
│       └── uasl_spec/             # UASL v2/v3 업데이트 이력
│
├── 04_meetings/           # 회의록
│   ├── 2025-12-26_softbase_xframe.md
│   ├── 2026-02-11_ShinsegaeInC.md
│   └── 2026-03-17_dev_update.md
│
├── 05_knowledge_base/     # 기술 참고자료
│   ├── README.md          # xFrame5 아카이브 내용 기록
│   └── xframe5_knowledge_base.zip  # 대용량 (Git LFS)
│
├── 06_infra/              # 인프라/배포 관련 자료
│   └── 코딩에이전트_외부업체데모_환경구성_방안.docx
│
├── 07_oss_analysis/       # 오픈소스 프로젝트 심층 분석
│   ├── README.md          # 분석 인덱스 + 비교 요약
│   ├── 01_vllm_analysis.md
│   ├── 02_litellm_analysis.md
│   └── 03_opencode_analysis.md
│
├── _00_work/              # 작업 자료 스테이징
│   ├── 260127-260211/     # 1/26~2/11 작업 원본
│   ├── 260212-260319/     # 2/12~3/19 작업 원본
│   └── ppt_assets/        # PPT 빌드 스크립트, 템플릿, 다이어그램
│
├── SecernCode/            # 서브모듈 (트랙 2 Go 프로젝트)
│   └── docs/              # 기술 문서 (구현 기획서, 기능 분석 등)
│
├── SecernInfra/            # 서브모듈 (vLLM 인프라 확장, Go+Python)
│   ├── src/                # Go 런타임 (gateway, keygen) + Python (Cython)
│   ├── deploy/             # Docker, Helm chart, K8s 매니페스트
│   └── docs/               # Stage별 구현 기획서
│
└── .obsidian/             # Obsidian 설정
```

## 문서 목록

| 경로 | 설명 |
|------|------|
| `01_strategy/01_executive_summary_ko.md` | 경영진 요약 - 프로젝트 개요 및 핵심 가치 |
| `01_strategy/02_competitive_strategy_ko.md` | 경쟁 전략 - 상세 경쟁사 분석 |
| `01_strategy/03_regulatory_environment_ko.md` | 규제 환경 - AI 규제 및 컴플라이언스 |
| `01_strategy/04_product_overview_ko.md` | 제품 기능 소개 - Coco 구성 및 핵심 기능 |
| `01_strategy/05_track2_tech_strategy_ko.md` | 트랙 2 기술 전략 리서치 v2.0 — 경쟁 솔루션 + Cline 비교 병합본 |
| `02_implementation/01_roadmap_ko.md` | 구현 로드맵 - Phase 1/2 + 트랙 2 코딩 에이전트 로드맵 |
| `02_implementation/02_resource_plan_ko.md` | 투입 인력 및 로드맵 - Phase별 인력/일정 계획 |
| `02_implementation/03_cost_analysis_ko.md` | 비용 분석 - TCO 및 ROI |
| `02_implementation/04_phase2_tech_stack_ko.md` | Phase 2 기술 스택 - 학습 자료/구현 가이드 |
| `02_implementation/05_api_reference_ko.md` | API 레퍼런스 - 엔드포인트 명세 |
| `02_implementation/06_vllm_rd_plan_ko.md` | vLLM 인프라 고도화 R&D 계획 (인증/암호화/LiteLLM 멀티 모델) |
| `02_implementation/07_secerncode_status_ko.md` | SecernCode(Go) Track 2 구현 현황 보고서 |
| `02_implementation/08_vllm_infra_prd_ko.md` | vLLM 인프라 고도화 PRD (모델 암호화/LiteLLM/Go 인증 게이트웨이) |
| `02_implementation/09_vllm_infra_roadmap_ko.md` | vLLM 인프라 고도화 로드맵 — Infra-S0~S3 + SecernInfra 실행 계획 |
| `03_development/` | 개발 진행 자료 - 테스트, 벤치마크 |
| `03_development/2026-01-15_project_intro/` | 프로젝트 소개 — 부하 테스트, 모델 벤치마크 |
| `03_development/2026-01-24_progress/` | 1월 진행 — VRAM 산정, MCP 아키텍처, 경량 모델 QA |
| `03_development/2026-02-07_progress/` | 2월 1주차 진행 - 코드생성, UASL, QA 개선 |
| `03_development/2026-02-12_progress/` | Coco Studio 기능 테스트 (7 TC, 71.4%) |
| `03_development/2026-03-19_progress/` | 3월 진행 - 4B 파인튜닝, UASL v2/v3, 서버 분리, 부산은행 PoC |
| `04_meetings/2025-12-26_softbase_xframe.md` | 소프트베이스 xFrame5 기술 미팅 |
| `04_meetings/2026-02-11_ShinsegaeInC.md` | 신세계 I&C 솔루션 데모 회의록 |
| `04_meetings/2026-03-17_dev_update.md` | 개발 현황 업데이트 (서버 분리, Playground, 부산은행 PoC) |
| `05_knowledge_base/glossary_ko.md` | 프로젝트 용어집 - 경영진/개발자용 이중 설명 (~70개 용어) |
| `06_infra/` | 인프라/배포 관련 자료 |
| `07_oss_analysis/01_vllm_analysis.md` | vLLM 심층 분석 — LLM 추론 엔진 |
| `07_oss_analysis/02_litellm_analysis.md` | LiteLLM 심층 분석 — LLM 프록시/라우터 |
| `07_oss_analysis/03_opencode_analysis.md` | OpenCode 심층 분석 — AI 코딩 에이전트 |
| `SecernCode/docs/roadmap.md` | SecernCode 기술 로드맵 — Stage 0~4 + Alpha (개발팀 관점) |
| `SecernCode/docs/secerncode_implementation_spec_v2.md` | SecernCode Stage 0 구현 기획서 — 8-Layer 아키텍처, Phase 1~6 |
| `SecernCode/docs/stage1_spec.md` | SecernCode Stage 1 기획서 — eGovFrame RAG, 모델 검증, 벤치마크 |
| `SecernCode/docs/feature_summary.md` | SecernCode 기능 요약 |
| `SecernInfra/docs/stage0_spec.md` | SecernInfra Infra-S0 구현 기획서 — 모델 암호화 |
| `SecernInfra/docs/stage1_spec.md` | SecernInfra Infra-S1 구현 기획서 — LiteLLM + K8s |
| `SecernInfra/docs/stage2_spec.md` | SecernInfra Infra-S2 구현 기획서 — Go 인증 게이트웨이 |
| `SecernCode/docs/coding_agent_feature_analysis.md` | 코딩 에이전트 기능 분석 — 경쟁 제품 비교 |
