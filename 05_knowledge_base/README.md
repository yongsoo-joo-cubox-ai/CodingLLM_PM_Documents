# 05_knowledge_base - 기술 참고자료

이 폴더는 Coder 프로젝트에서 사용하는 프레임워크별 Knowledge Base를 관리합니다.

---

## xFrame5 Knowledge Base (아카이브)

> **위치:** 현재 폴더 (`05_knowledge_base/xframe5_knowledge_base.zip`)
> **참고:** 대용량 파일로 `.gitignore`에 의해 Git에서 제외됩니다.

xFrame5 프레임워크의 도움말 문서가 압축 보관되어 있습니다. RAG(Retrieval-Augmented Generation) 시스템 구축에 사용됩니다.

### 개요

| 항목 | 내용 |
|------|------|
| **용량** | 332MB (압축 전) |
| **파일 수** | ~26,000개 |
| **용도** | xFrame5 프레임워크 Knowledge Base (RAG용) |
| **압축 파일** | `05_knowledge_base/xframe5_knowledge_base.zip` |

### 폴더 구조

| 폴더 | 파일 수 | 설명 |
|------|--------|------|
| XML 스키마 및 샘플 | 2 | 컴포넌트 스키마(xsd) + 샘플(xml) |
| 컴포넌트별 HTML | 94 | 각 컴포넌트 통합 도움말 |
| 컴포넌트별 마크다운 | 94 | 해시 파일명 마크다운 |
| 컴포넌트별 속성별 HTML | ~25,000 | 세부 속성 도움말 |
| 파일 병합 HTML | 9 | 분할된 통합 문서 |

### 상세 폴더 설명

```
xFrame5/
├── xFrame5 XML 스키마 및 샘플 XML/
│   ├── xframe5_component.xsd (2MB) - 컴포넌트 스키마 정의
│   └── xframe5_component_screen.xml (18KB) - 샘플 XML
│
├── xFrame5 도움말 컴포넌트별 HTML 파일/ (94개)
│   └── accordion.html, activex.html, ... 등 컴포넌트별 도움말
│
├── xFrame5 도움말 컴포넌트별 마크다운 파일/ (94개)
│   └── 해시 파일명으로 저장된 마크다운 문서
│
├── xFrame5 도움말 컴포넌트별 속성별 HTML 파일/ (97개 폴더)
│   └── accordion/, activex/, ... 각 컴포넌트의 속성별 세부 도움말
│
└── xFrame5 도움말 컴포넌트별 파일 병합 HTML 파일/ (9개)
    └── XFRAME5_HELP_*.html - 분할된 통합 도움말
```

### 컴포넌트 목록 (94개)

| | | | | |
|---|---|---|---|---|
| accordion | activex | amcharts5 | animate | arrowbox |
| audio | barcode | calendar | canvas | caption |
| checkbox | colorpicker | combobox | control | datepicker |
| db | diamond | div | dll | downloader |
| ellipse | excel | factory | fileinput | fileupload |
| frame | grid | group | htmleditor | htmlview |
| i18n | iframe | image | input | inputpassword |
| json | label | line | linkedbutton | linkedimage |
| listbox | menutab | multilinegrid | output | page |
| pdf | pivotgrid | plugin | polygon | polyline |
| propertygrid | qrcode | radio | rect | richreadonly |
| roundrect | rsa | schemaviewer | screen | scroll |
| segment | select | shape | singleline | tabcontrol |
| textarea | tinyslider | tmap | toast | treegrid |
| treeview | trigger | video | visible | webcam |
| websocket | xml | xplatform | | |

### 압축 해제 방법

```bash
cd /path/to/CodingLLM_PM_Documents/05_knowledge_base
unzip xframe5_knowledge_base.zip
```

### 활용 예시

1. **RAG 시스템 구축**: 마크다운/HTML 파일을 벡터 DB에 임베딩
2. **컴포넌트 문서 조회**: 특정 컴포넌트(grid, combobox 등) 속성 확인
3. **코드 생성 컨텍스트**: LLM 프롬프트에 관련 도움말 주입

---

## 향후 추가 예정

- `spring/` - Spring Framework Knowledge Base
- `vue/` - Vue.js Knowledge Base
- `react/` - React Knowledge Base

---

## 관련 링크

- [개발 자료](../03_development/) - 테스트 결과, 벤치마크
- [API 레퍼런스](../02_implementation/api_reference_ko.md) - Coder API 명세
