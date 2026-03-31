# Google Drive 동기화

> 이 문서는 CLAUDE.md의 레퍼런스입니다. 핵심 지침은 [CLAUDE.md](../../CLAUDE.md)를 참조하세요.

Git 저장소를 Google Drive 공유 드라이브로 단방향 미러링하는 커맨드가 있다.

- **소스**: 이 저장소 (Git이 원본)
- **타겟**: `CodingLLM_Project/01_Documents/` (Google Drive 공유 드라이브)
- **MD 처리**: DOCX로 변환하여 타겟에 저장, 원본 MD는 Git에만 보관
- **스크립트**: `.claude/scripts/sync-to-gdrive.sh`

## 슬래시 커맨드

| 커맨드 | 설명 |
|--------|------|
| `/sync-gdrive` | 실제 동기화 실행 |
| `/sync-gdrive --dry-run` | 미리보기 (변경 없음) |
| `/sync-gdrive-analyze` | 소스/타겟 차이점 분석 |

## 터미널에서 직접 실행

```bash
bash .claude/scripts/sync-to-gdrive.sh            # 실제 동기화
bash .claude/scripts/sync-to-gdrive.sh --dry-run   # 미리보기
```

## 동작 요약

1. **rsync**: 비-MD 파일 증분 복사 (Google Drive FUSE 호환 옵션)
2. **pandoc**: MD → DOCX 변환 (문서 간 `.md` 링크를 `.docx`로 치환, 이미지 임베드)
3. **정리**: 소스에 없는 타겟 파일 삭제 (`.DS_Store` 제외)
4. **리포트**: 복사/변환/삭제/스킵/실패 건수 출력

## 사전 요구사항

- `pandoc` 설치 필요: `brew install pandoc`
- Google Drive 데스크톱 앱이 마운트되어 있어야 함
