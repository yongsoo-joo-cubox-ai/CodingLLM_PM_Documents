---
allowed-tools: Bash(bash:*), Bash(sh:*)
description: Sync CodingLLM project documents to Google Drive (one-way mirror with MD→DOCX conversion)
---

CodingLLM_PM_Documents를 Google Drive 공유 드라이브로 동기화하는 스크립트를 실행합니다.

## 실행할 작업

1. `.claude/scripts/sync-to-gdrive.sh`를 $ARGUMENTS 인자와 함께 실행
2. 스크립트 출력을 사용자에게 보여줌
3. 결과를 간결하게 요약

## 인자

- `--dry-run`: 실제 변경 없이 미리보기만 수행
- 인자 없음: 실제 동기화 수행

## 동작 설명

- **Step 1**: rsync로 비-MD 파일을 Google Drive로 복사 (증분)
- **Step 2**: pandoc으로 MD 파일을 DOCX로 변환 (증분, .md 링크→.docx 치환)
- **Step 3**: 소스에 없는 타겟 파일 정리
- **Step 4**: 결과 리포트 출력

## 실행

```bash
bash .claude/scripts/sync-to-gdrive.sh $ARGUMENTS
```

실행 후 결과를 한글로 요약해서 보고하세요. 실패 항목이 있으면 원인을 분석하세요.
