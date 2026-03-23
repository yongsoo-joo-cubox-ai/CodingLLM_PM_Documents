#!/bin/bash
# sync-config.sh — 동기화 공통 설정
# sync-to-gdrive.sh, sync-analyze.sh 에서 source하여 사용

###############################################################################
# 경로 설정
###############################################################################
# 스크립트 위치 기반 자동 탐지 (/.claude/scripts/ → 저장소 루트)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE="$(cd "$SCRIPT_DIR/../.." && pwd)"

TARGET="/Users/ysjoo/Library/CloudStorage/GoogleDrive-yongsoo.joo@cubox.ai/공유 드라이브/CodingLLM_Project/01_Documents"

###############################################################################
# 제외 목록
###############################################################################
EXCLUDE_DIRS=(.git .obsidian .claude .playwright-mcp .serena .omc _public)
EXCLUDE_FILES=(.DS_Store .gitignore .gitattributes .gitmodules CLAUDE.md)

###############################################################################
# 유틸리티 함수
###############################################################################

# macOS 호환 human-readable 파일 크기 변환
human_size() {
  awk "BEGIN { s=$1; u=\"BKMGT\"; for(i=0; s>=1024 && i<4; i++) s/=1024; printf \"%.1f%s\", s, substr(u,i+1,1) }"
}

# find 명령용 제외 옵션 생성 (경로 기반)
# 사용: eval "find \$SOURCE $(build_find_excludes) -type f"
build_find_excludes() {
  local opts=""
  for d in "${EXCLUDE_DIRS[@]}"; do
    opts="$opts -not -path '*/${d}/*'"
  done
  for f in "${EXCLUDE_FILES[@]}"; do
    opts="$opts -not -name '${f}'"
  done
  echo "$opts"
}

# rsync 명령용 --exclude 옵션 배열 생성
# 사용: RSYNC_EXCLUDES=($(build_rsync_excludes)); rsync "${RSYNC_EXCLUDES[@]}" ...
build_rsync_excludes() {
  for d in "${EXCLUDE_DIRS[@]}"; do
    echo "--exclude=${d}/"
  done
  for f in "${EXCLUDE_FILES[@]}"; do
    echo "--exclude=${f}"
  done
  # MD 파일은 pandoc으로 별도 처리하므로 rsync에서 제외
  echo "--exclude=*.md"
}
