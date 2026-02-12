---
allowed-tools: Bash(bash:*), Bash(sh:*)
description: Analyze sync state between Git repo and Google Drive before syncing
---

CodingLLM_PM_Documents(Git)와 Google Drive 공유 드라이브 간 동기화 상태를 분석합니다.

## 경로

- **소스**: `/Users/ysjoo/Documents/GitHub/CodingLLM_PM_Documents`
- **타겟**: `~/Library/CloudStorage/GoogleDrive-yongsoo.joo@cubox.ai/공유 드라이브/CodingLLM_Project/01_Documents`

## 분석할 항목

아래 스크립트를 실행하고 결과를 종합 분석하세요.

### 분석 스크립트

```bash
bash .claude/scripts/sync-analyze.sh
```

## 출력 형식

스크립트 결과를 기반으로 아래 형식의 한글 테이블로 요약하세요.

### 1. 전체 현황

| 항목 | 소스 | 타겟 | 차이 |
|------|------|------|------|
| 전체 파일 수 | ? | ? | ? |
| MD/DOCX 파일 | ? | ? | ? |
| 비-MD 파일 | ? | ? | ? |
| pandoc 버전 | ? | - | - |

### 2. 동기화 대상 파일 (변경/신규/삭제)

스크립트 출력의 `[SYNC NEEDED]` 섹션을 테이블로 정리:

| 상태 | 파일 | 소스 크기 | 타겟 크기 | 소스 수정일 | 사유 |
|------|------|----------|----------|------------|------|
| 신규 | ... | ... | - | ... | 타겟 없음 |
| 변경 | ... | ... | ... | ... | 크기/시간 차이 |
| 삭제 | ... | - | ... | - | 소스 없음 |

### 3. 동기화 불필요 (최신 상태) 파일 수

동기화 대상이 없으면 "모든 파일이 동기화된 상태입니다"라고 보고.

타겟에만 있는 파일이 있으면 보존 여부를 사용자에게 확인하도록 안내하세요.
