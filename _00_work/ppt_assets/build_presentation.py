"""
Coco Platform Introduction - PowerPoint Presentation Builder

Secern AI 오렌지 브랜딩 기반 35슬라이드 프레젠테이션 생성 스크립트.
secern_template_helpers 모듈의 색상 상수와 헬퍼 함수를 재사용한다.

Usage:
    python build_presentation.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from pptx import Presentation

# secern_template_helpers에서 모든 헬퍼와 상수를 import
from secern_template_helpers import (
    # Slide dimensions
    SLIDE_WIDTH, SLIDE_HEIGHT,
    # Helpers
    reset_slide_counter,
    add_cover_slide, add_content_slide, add_screenshot_slide,
    add_two_column_slide, add_table_slide, add_section_slide,
    add_closing_slide, add_diagram_slide, add_diagram_image_slide,
    add_cards_slide, add_key_message_slide, add_quote_slide,
    add_three_column_slide, add_code_slide, add_timeline_slide,
    add_image_text_slide,
    # Counter access
    _slide_number,
)
import secern_template_helpers as sth

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
SCREENSHOTS_DIR = SCRIPT_DIR / "screenshots"
DIAGRAMS_DIR = SCRIPT_DIR / "diagram_images"
OUTPUT_PATH = SCRIPT_DIR / "Coco_Platform_Introduction.pptx"


# ---------------------------------------------------------------------------
# Slide Content Definitions (35 slides)
# ---------------------------------------------------------------------------

def build_slides(prs) -> None:
    """35개 슬라이드를 순서대로 생성한다."""

    # ===================================================================
    # Section 1: 도입 (Slides 1-4)
    # ===================================================================

    # --- Slide 1: 표지 ---
    print("[1/35] 표지")
    add_cover_slide(
        prs,
        title="Coco",
        subtitle="AI 코드 거버넌스 플랫폼",
        extra_lines=["Secern AI | 2026"],
    )

    # --- Slide 2: 기업 환경의 AI 코딩 도구 과제 ---
    print("[2/35] 기업 환경의 AI 코딩 도구 과제")
    add_content_slide(prs, "기업 환경의 AI 코딩 도구 과제", [
        "폐쇄망 제약 \u2014 외부 클라우드 AI 서비스 사용 불가",
        "품질 일관성 부재 \u2014 동일 입력에 매번 다른 코드 생성",
        "감사 추적 불가 \u2014 AI 생성 코드의 변경 이력 관리 불가",
        "LLM 종속 \u2014 특정 모델 교체 시 전체 시스템 변경 필요",
    ])

    # --- Slide 3: Coco 솔루션 개요 ---
    print("[3/35] Coco 솔루션 개요")
    add_key_message_slide(
        prs,
        title="Coco 솔루션 개요",
        key_message="단순 AI 코드 생성이 아닌, AI 코드 거버넌스",
        sub_bullets=[
            "기업 표준 자동 적용 + 생성 코드의 완전한 추적 가능성",
            "대상: 폐쇄망, 온프레미스 LLM, 규제 산업 기업",
            "금융권, 공공기관, 대기업 SI 환경 특화",
        ],
    )

    # --- Slide 4: 제품 구성 (다이어그램 이미지) ---
    print("[4/35] 제품 구성")
    diagram_path = DIAGRAMS_DIR / "slide04_product_arch.png"
    if diagram_path.exists():
        add_diagram_image_slide(prs, "제품 구성", str(diagram_path))
    else:
        add_cards_slide(prs, "제품 구성", [
            "Coco Engine \u2014 서버/코어, Rust + Loco.rs, 6단계 파이프라인 \u2705",
            "Coco Studio \u2014 웹 UI, 코드 생성/리뷰/Q&A 통합 \u2705",
            "Coco CLI \u2014 터미널 기반, generate/batch/models 명령 \u2705",
            "Coco Admin \u2014 관리 UI, 모델/사용자 관리 \u2705",
            "MCP Servers \u2014 xframe5-compiler, vue-compiler \u2705",
            "Eclipse Plugin \u2014 IDE 통합 \u2705",
        ], cols=3)

    # ===================================================================
    # Section 2: 핵심 기술 (Slides 5-9)
    # ===================================================================

    # --- Slide 5: 6단계 결정론적 파이프라인 (다이어그램 이미지) ---
    print("[5/35] 6단계 결정론적 파이프라인")
    diagram_path = DIAGRAMS_DIR / "slide05_pipeline.png"
    if diagram_path.exists():
        add_diagram_image_slide(
            prs, "6단계 결정론적 파이프라인", str(diagram_path),
            notes=["동일 입력 \u2192 동일 출력 보장",
                   "각 단계에서 검증/로깅으로 완전한 추적 가능"],
        )
    else:
        add_diagram_slide(
            prs, "6단계 결정론적 파이프라인",
            text_content=(
                "[1] 입력 정규화  \u2192  [2] 컨텍스트 주입  \u2192  [3] LLM 생성\n"
                "                              \u2193\n"
                "[4] 구문 검증    \u2190  [5] 표준 적용      \u2190  [6] 감사 로깅"
            ),
            notes=["동일 입력 \u2192 동일 출력 보장",
                   "각 단계에서 검증/로깅으로 완전한 추적 가능"],
        )

    # --- Slide 6: 두 가지 코드 생성 전략 ---
    print("[6/35] 두 가지 코드 생성 전략")
    add_table_slide(prs, "두 가지 코드 생성 전략 \u2014 CGF-A vs CGF-B", [
        "지표", "CGF-A (Direct)", "CGF-B (Spec-first)", "비고",
    ], [
        ["평균 응답시간", "48,780ms", "16,964ms", "CGF-B 65% 빠름"],
        ["품질 우위", "1/4 (25%)", "3/4 (75%)", "CGF-B 우수"],
        ["코드 일관성", "LLM 의존", "MCP 결정론적", "CGF-B 우수"],
        ["확장성", "모델별 재학습", "스펙 기반 확장", "CGF-B 우수"],
    ])

    # --- Slide 7: UASL/SUIS (다이어그램 이미지) ---
    print("[7/35] UASL/SUIS \u2014 프레임워크 중립 UI 언어")
    diagram_path = DIAGRAMS_DIR / "slide07_uasl_flow.png"
    if diagram_path.exists():
        add_diagram_image_slide(
            prs, "UASL/SUIS \u2014 프레임워크 중립 UI 언어", str(diagram_path),
            notes=[
                "WHAT(의도)을 기술, HOW(구현)는 어댑터 담당",
                "동일 스펙으로 xFrame5, Vue3, React 동시 생성 가능",
                "DOM 이벤트가 아닌 의미적 트리거 사용",
            ],
        )
    else:
        add_diagram_slide(
            prs, "UASL/SUIS \u2014 프레임워크 중립 UI 언어",
            text_content=(
                "사용자 의도  \u2192  LLM  \u2192  SUIS 스펙  \u2192  MCP 서버  \u2192  프레임워크별 코드"
            ),
            notes=[
                "WHAT(의도)을 기술, HOW(구현)는 어댑터 담당",
                "동일 스펙으로 xFrame5, Vue3, React 동시 생성 가능",
                "DOM 이벤트가 아닌 의미적 트리거 사용",
            ],
        )

    # --- Slide 8: 6대 USP (다이어그램 이미지) ---
    print("[8/35] 6대 USP")
    diagram_path = DIAGRAMS_DIR / "slide08_usp_cards.png"
    if diagram_path.exists():
        add_diagram_image_slide(prs, "6대 USP", str(diagram_path))
    else:
        add_cards_slide(prs, "6대 USP", [
            "결정론적 출력 \u2014 동일 입력 \u2192 동일 출력 보장",
            "표준 강제 \u2014 기업 코딩 표준 자동 적용",
            "완전한 온프레미스 \u2014 외부 데이터 전송 제로",
            "Spec-Driven 생성 \u2014 LLM은 스펙만, 코드는 MCP",
            "감사 추적 \u2014 모든 생성 과정 로깅",
            "LLM 추상화 \u2014 특정 모델 종속 없음",
        ], cols=3)

    # --- Slide 9: 지원 프레임워크 ---
    print("[9/35] 지원 프레임워크")
    add_table_slide(prs, "지원 프레임워크", [
        "프레임워크", "코드 생성", "프리뷰", "MCP 서버", "상태",
    ], [
        ["xFrame5", "\u2705 XML + JS", "\u2705 런타임", "xframe5-compiler", "운영 중"],
        ["Vue3", "\u2705 SFC (.vue)", "\u2705 런타임", "vue-compiler", "운영 중"],
        ["Spring Boot", "Phase 2 (예정)", "\u2014", "spring-compiler", "계획"],
        ["React", "Phase 3 (예정)", "\u2014", "\u2014", "계획"],
    ])

    # ===================================================================
    # Section 3: Coco Studio 데모 (Slides 10-23)
    # ===================================================================

    # --- Slide 10: Coco Studio 소개 ---
    print("[10/35] Coco Studio 소개")
    add_screenshot_slide(prs, "Coco Studio 소개", [
        "웹 기반 통합 개발 환경",
        "코드 생성 \u00b7 리뷰 \u00b7 Q&A \u00b7 프리뷰 통합",
        "브라우저 기반 \u2014 설치 불필요",
        "테스트 URL: coco.secernai.net",
    ], "01_login.png", SCREENSHOTS_DIR)

    # --- Slide 11: Workspace 엔티티 그래프 ---
    print("[11/35] Workspace \u2014 엔티티 그래프")
    add_screenshot_slide(prs, "Workspace \u2014 엔티티 그래프", [
        "React Flow 기반 도메인 모델 시각화",
        "엔티티 간 관계선 \u00b7 줌/패닝",
        "user, task, project, comment 4개 엔티티",
    ], "02_workspace_graph.png", SCREENSHOTS_DIR)

    # --- Slide 12: Workspace 엔티티 상세 ---
    print("[12/35] Workspace \u2014 엔티티 상세")
    add_screenshot_slide(prs, "Workspace \u2014 엔티티 상세", [
        "Fields \u2014 필드 목록 (이름, 타입, 제약조건)",
        "Relations \u2014 엔티티 간 관계",
        "Outputs \u2014 생성 이력 관리",
        "Chat \u2014 엔티티 컨텍스트 대화",
    ], "03_workspace_fields.png", SCREENSHOTS_DIR)

    # --- Slide 13: 도메인 모델 Import ---
    print("[13/35] 도메인 모델 Import")
    add_screenshot_slide(prs, "도메인 모델 Import", [
        "SQL DDL, JSON Schema, OpenAPI, YAML 4종 지원",
        "파일 업로드 \u00b7 드래그 앤 드롭 \u00b7 붙여넣기",
        "히스토리 관리: task.schema.json \u2192 4개 엔티티",
    ], "13_import_modal.png", SCREENSHOTS_DIR)

    # --- Slide 14: 코드 생성 ---
    print("[14/35] 코드 생성 (Generate)")
    add_screenshot_slide(prs, "코드 생성 (Generate)", [
        "자연어 프롬프트로 코드 생성 요청",
        "CGF-B 파이프라인 자동 실행",
        "한국어/영어 프롬프트 모두 지원",
    ], "07_chat_generate.png", SCREENSHOTS_DIR)

    # --- Slide 15: 코드 생성 실행 과정 ---
    print("[15/35] 코드 생성 \u2014 실행 과정")
    add_screenshot_slide(prs, "코드 생성 \u2014 실행 과정", [
        "1. Intent Analysis \u2192 엔티티 인식",
        "2. Modeling entities \u2192 도메인 그래프",
        "3. UI Spec 생성 \u2192 confidence: 85%",
        "4. 사용자 승인 게이트 (Approve/Modify/Reject)",
        "5. MCP 코드 컴파일 \u2192 완료",
    ], "09_chat_approval_gate.png", SCREENSHOTS_DIR)

    # --- Slide 16: 코드 생성 결과 ---
    print("[16/35] 코드 생성 \u2014 결과")
    add_screenshot_slide(prs, "코드 생성 \u2014 결과", [
        "XML + JS + Mock JSON 3파일 생성",
        "응답 시간: 12초",
        "코드 블록 복사 및 프리뷰 제공",
    ], "08_chat_generate_result.png", SCREENSHOTS_DIR)

    # --- Slide 17: 코드 프리뷰 ---
    print("[17/35] 코드 프리뷰")
    add_screenshot_slide(prs, "코드 프리뷰", [
        "생성된 코드를 xFrame5 런타임에서 즉시 확인",
        "검색 패널 + 액션 버튼 + 데이터 그리드",
        "20행 mock 데이터, 9개 컬럼",
    ], "12_code_preview.png", SCREENSHOTS_DIR)

    # --- Slide 18: 지식 기반 Q&A ---
    print("[18/35] 지식 기반 Q&A (Ask)")
    add_screenshot_slide(prs, "지식 기반 Q&A (Ask)", [
        "RAG 기반 프레임워크 문서 검색",
        "xFrame5 API 설명 + 코드 예시",
        "정확한 답변 + 출처 명시",
    ], "10_chat_ask.png", SCREENSHOTS_DIR)

    # --- Slide 19: Q&A 답변 품질 ---
    print("[19/35] Q&A \u2014 답변 품질")
    add_screenshot_slide(prs, "Q&A \u2014 답변 품질", [
        "지식 그래프 시각화 (노드 탐색)",
        "출처 명시 + 관련 주제 추천",
        "환각 방지: '정확한 정보가 없습니다' 정직성 고지",
    ], "11_chat_ask_result.png", SCREENSHOTS_DIR)

    # --- Slide 20: 엔티티 컨텍스트 Chat ---
    print("[20/35] 엔티티 컨텍스트 Chat")
    add_screenshot_slide(prs, "엔티티 컨텍스트 Chat", [
        "특정 엔티티 스코프 내 Q&A",
        "Chat context: user (9 fields)",
        "엔티티 특화 답변 제공",
    ], "06_workspace_chat.png", SCREENSHOTS_DIR)

    # --- Slide 21: 일괄 생성 ---
    print("[21/35] 일괄 생성 (Generate System)")
    add_screenshot_slide(prs, "일괄 생성 (Generate System)", [
        "다수 엔티티 \u00d7 Screen Types 조합",
        "4개 엔티티 \u00d7 3 Types = 12 화면 일괄 생성",
        "List Screen, Detail Screen, Editor Screen",
    ], "14_generate_system.png", SCREENSHOTS_DIR)

    # --- Slide 22: 프로젝트 관리 & Settings ---
    print("[22/35] 프로젝트 관리 & Settings")
    add_screenshot_slide(prs, "프로젝트 관리 & Settings", [
        "프로젝트 생성: Spring Boot, Vue 3, xFrame5",
        "모델 설정: Qwen2.5 Coder 32B AWQ",
        "RAG 설정: Token Budget 1500, Similarity 0.70",
    ], "15_settings.png", SCREENSHOTS_DIR)

    # --- Slide 23: 다크모드 & UI ---
    print("[23/35] 다크모드 & UI")
    add_screenshot_slide(prs, "다크모드 & UI", [
        "다크모드 전체 UI 일관 적용",
        "Profile 관리",
        "접근성 향상",
    ], "16_dark_mode.png", SCREENSHOTS_DIR)

    # ===================================================================
    # Section 4: Coco CLI (Slides 24-26)
    # ===================================================================

    # --- Slide 24: Coco CLI 소개 ---
    print("[24/35] Coco CLI 소개")
    add_code_slide(prs, "Coco CLI 소개", [
        "터미널 기반 코드 생성 \u00b7 리뷰 \u00b7 Q&A 도구",
    ], (
        'coco qa "팝업 창을 어떻게 여나요?" --product xframe5 --language ko\n\n'
        "coco review sample_code.xml --product xframe5\n\n"
        'coco generate "user list screen" --product xframe5'
    ))

    # --- Slide 25: CLI Q&A 기능 ---
    print("[25/35] CLI \u2014 Q&A 기능")
    add_table_slide(prs, "CLI \u2014 Q&A 기능", [
        "테스트", "언어", "형식", "응답시간", "결과",
    ], [
        ["팝업 창 여는 법", "한국어", "Text", "23.8초", "\u2705 PASS"],
        ["How to open popup", "영어", "Text", "34.2초", "\u2705 PASS"],
        ["Grid 데이터 필터링", "한국어", "JSON", "\u2014", "\u2705 PASS"],
        ["Add row to Dataset", "영어", "JSON", "\u2014", "\u2705 PASS"],
    ])

    # --- Slide 26: CLI Review 기능 ---
    print("[26/35] CLI \u2014 Review 기능")
    add_table_slide(prs, "CLI \u2014 Review 기능", [
        "항목", "내용",
    ], [
        ["점수", "60/100"],
        ["Syntax", "100점"],
        ["Patterns", "50점"],
        ["Naming", "40점"],
        ["Performance", "60점"],
        ["발견 이슈", "8개 (Error 5, Warning 3)"],
        ["개선 제안", "네이밍 표준화, 페이징 추가"],
    ])

    # ===================================================================
    # Section 5: 배포 & 인프라 (Slides 27-29)
    # ===================================================================

    # --- Slide 27: 온프레미스 배포 아키텍처 (다이어그램 이미지) ---
    print("[27/35] 온프레미스 배포 아키텍처")
    diagram_path = DIAGRAMS_DIR / "slide27_deploy_arch.png"
    if diagram_path.exists():
        add_diagram_image_slide(
            prs, "온프레미스 배포 아키텍처", str(diagram_path),
            notes=["외부 데이터 전송: 0건",
                   "모든 컴포넌트 기업 내부망에서 운영"],
        )
    else:
        add_diagram_slide(
            prs, "온프레미스 배포 아키텍처",
            text_content=(
                "\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"
                "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"
                "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"
                "\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n"
                "\u2502       기업 내부망 (폐쇄망)              \u2502\n"
                "\u251c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"
                "\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"
                "\u2500\u2500\u2500\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500"
                "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2524\n"
                "\u2502 Web 서버    \u2502 App 서버     \u2502 Model 서버   \u2502\n"
                "\u2502 Studio     \u2502 Engine      \u2502 vLLM+LLM    \u2502\n"
                "\u2502 Admin      \u2502 MCP Svrs    \u2502 GPT-OSS     \u2502\n"
                "\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"
                "\u2500\u2500\u2534\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"
                "\u2500\u2500\u2500\u2500\u2500\u2534\u2500\u2500\u2500\u2500\u2500"
                "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518"
            ),
            notes=["외부 데이터 전송: 0건",
                   "모든 컴포넌트 기업 내부망에서 운영"],
        )

    # --- Slide 28: 권장 모델 & 성능 ---
    print("[28/35] 권장 모델 & 성능")
    add_table_slide(prs, "권장 모델 & 성능", [
        "모델", "VRAM", "품질", "응답시간", "권장",
    ], [
        ["GPT-OSS 20B", "40GB", "94%", "~15초", "\u2705 권장"],
        ["Qwen2.5-32B-AWQ", "16GB", "54%", "25-65초", "차선"],
        ["Qwen-7B", "7GB", "\u2014", "빠름", "리뷰/QA용"],
    ])

    # --- Slide 29: MCP 서버 확장 구조 (다이어그램 이미지) ---
    print("[29/35] MCP 서버 확장 구조")
    diagram_path = DIAGRAMS_DIR / "slide29_mcp_hub.png"
    if diagram_path.exists():
        add_diagram_image_slide(prs, "MCP 서버 확장 구조", str(diagram_path))
    else:
        add_diagram_slide(
            prs, "MCP 서버 확장 구조",
            text_content=(
                "Coco Engine (Orchestration)\n"
                "  의도 분석 \u2192 UASL/SUIS \u2192 MCP 호출\n"
                "     \u2193           \u2193           \u2193\n"
                "xframe5-      xframe5-     vue-\n"
                "compiler      validator    compiler\n"
                "  \u2705            \u2705           \u2705\n\n"
                "향후 확장:\n"
                "  spring-compiler (Phase 2)\n"
                "  react-compiler (Phase 3)"
            ),
        )

    # ===================================================================
    # Section 6: 시장 & 전략 (Slides 30-33)
    # ===================================================================

    # --- Slide 30: 타겟 고객 ---
    print("[30/35] 타겟 고객")
    add_three_column_slide(prs, "타겟 고객", [
        ("금융권", [
            "망분리 환경",
            "감사 요건",
            "규제 준수",
            "\u2192 완전 온프레미스 + 감사 추적",
        ]),
        ("공공기관", [
            "국산 SW 우선",
            "높은 보안 요구",
            "표준화 필요",
            "\u2192 국내 SI 특화",
        ]),
        ("대기업 SI", [
            "폐쇄망 운영",
            "자체 표준 보유",
            "대량 화면 생성",
            "\u2192 Spec-Driven + MCP",
        ]),
    ])

    # --- Slide 31: 경쟁 비교 ---
    print("[31/35] 경쟁 비교")
    add_table_slide(prs, "경쟁 비교", [
        "기능", "Cline Enterprise", "GitHub Copilot", "Coco",
    ], [
        ["결정론적 출력", "\u274c", "\u274c", "\u2705"],
        ["API 허용목록", "\u274c", "\u274c", "\u2705"],
        ["완전 온프레미스", "\u25b3", "\u274c", "\u2705"],
        ["Spec-Driven 생성", "\u274c", "\u274c", "\u2705"],
        ["코드 프리뷰", "\u274c", "\u274c", "\u2705"],
        ["웹 기반 Studio", "\u274c", "\u274c", "\u2705"],
        ["국내 SI 특화", "\u274c", "\u274c", "\u2705"],
    ])

    # --- Slide 32: 사용 시나리오 ---
    print("[32/35] 사용 시나리오")
    add_two_column_slide(
        prs,
        title="사용 시나리오",
        left_bullets=[
            "ERD 임포트 \u2192 도메인 모델 생성",
            "자연어로 화면 생성 요청",
            "4 엔티티 \u00d7 3 Screen Types",
            "= 12 화면 자동 생성",
            "코드 리뷰 \u2192 품질 검증",
        ],
        right_bullets=[
            "Sparos DevX 등 자체 플랫폼과 API 연동",
            "VS Code 익스텐션 통합",
            "CLI 기반 CI/CD 파이프라인",
            "REST API로 기존 시스템 통합",
        ],
        left_title="금융 SI \u2014 xFrame5 화면 대량 생성",
        right_title="대기업 내부 플랫폼 연동",
    )

    # --- Slide 33: 고객 반응 ---
    print("[33/35] 고객 반응")
    add_quote_slide(
        prs,
        title="고객 반응",
        quote=(
            "\u201c프로젝트 단위의 스펙을 관리하고 코드를 생성해주는 "
            "접근 방식이 인상적\u201d"
        ),
        attribution="\u2014 신세계 I&C IT개발혁신T/F (2026.02.11)",
        feedback_points=[
            "반복 업무(Boilerplate) 절감 기대",
            "향후 PoC 협의 예정",
            "VS Code 익스텐션/플랫폼 연동 관심",
        ],
    )

    # ===================================================================
    # Section 7: 마무리 (Slides 34-35)
    # ===================================================================

    # --- Slide 34: 향후 로드맵 ---
    print("[34/35] 향후 로드맵")
    add_timeline_slide(prs, "향후 로드맵", [
        (
            "Phase 1 (현재)",
            "xFrame5 + Vue3 코드 생성, Studio, CLI \u2705",
        ),
        (
            "Phase 2 (2026 H2)",
            "Spring Boot + 고급 리뷰 + VS Code 익스텐션",
        ),
        (
            "Phase 3 (2027)",
            "React + 멀티 에이전트 + 자동 테스트",
        ),
    ])

    # --- Slide 35: Thank You ---
    print("[35/35] Thank You")
    add_closing_slide(
        prs,
        title="Thank You",
        subtitle="Coco \u2014 AI 코드 거버넌스 플랫폼",
        contact_lines=["Secern AI", "coco.secernai.net"],
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """프레젠테이션을 빌드하고 파일로 저장한다."""
    print("=" * 60)
    print("  Coco Platform Introduction - PPT Builder")
    print("=" * 60)
    print()

    # 스크린샷 디렉토리 확인
    if SCREENSHOTS_DIR.exists():
        screenshots = list(SCREENSHOTS_DIR.glob("*.png"))
        print(f"스크린샷 디렉토리: {SCREENSHOTS_DIR}")
        print(f"발견된 스크린샷: {len(screenshots)}개")
        if screenshots:
            for s in sorted(screenshots):
                print(f"  - {s.name}")
    else:
        print(f"스크린샷 디렉토리 없음: {SCREENSHOTS_DIR}")
        print("  (스크린샷 없이 텍스트만으로 생성합니다)")

    # 다이어그램 디렉토리 확인
    if DIAGRAMS_DIR.exists():
        diagrams = list(DIAGRAMS_DIR.glob("*.png"))
        print(f"\n다이어그램 디렉토리: {DIAGRAMS_DIR}")
        print(f"발견된 다이어그램: {len(diagrams)}개")
        if diagrams:
            for d in sorted(diagrams):
                print(f"  - {d.name}")
    else:
        print(f"\n다이어그램 디렉토리 없음: {DIAGRAMS_DIR}")
        print("  (텍스트 다이어그램으로 대체합니다)")
    print()

    # Presentation 생성
    sth.reset_slide_counter()
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT

    print("슬라이드 생성 시작...")
    print("-" * 40)

    build_slides(prs)

    print("-" * 40)
    print()

    # 출력 디렉토리 확인
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # 저장
    prs.save(str(OUTPUT_PATH))

    print(f"생성 완료!")
    print(f"  슬라이드 수: {sth._slide_number}")
    print(f"  출력 파일: {OUTPUT_PATH}")
    print(f"  파일 크기: {OUTPUT_PATH.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
