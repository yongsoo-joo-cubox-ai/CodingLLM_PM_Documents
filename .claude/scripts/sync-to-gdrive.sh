#!/bin/bash
# sync-to-gdrive.sh — CodingLLM_PM_Documents → Google Drive 단방향 동기화
# 사용법: bash .claude/scripts/sync-to-gdrive.sh [--dry-run]
set -uo pipefail

###############################################################################
# 공통 설정 로드
###############################################################################
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/sync-config.sh"

DRY_RUN=false
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=true

###############################################################################
# 사전 검증
###############################################################################
if [ ! -d "$SOURCE" ]; then
  echo "ERROR: 소스 경로가 존재하지 않습니다: $SOURCE"
  exit 1
fi

if [ ! -d "$TARGET" ]; then
  echo "ERROR: 타겟 경로가 존재하지 않습니다: $TARGET"
  echo "  Google Drive가 마운트되어 있는지 확인하세요."
  exit 1
fi

if ! command -v pandoc &>/dev/null; then
  echo "ERROR: pandoc이 설치되어 있지 않습니다. brew install pandoc"
  exit 1
fi

###############################################################################
# 카운터 초기화
###############################################################################
copied=0
converted=0
skipped=0
deleted=0
failed=0
declare -a failed_files=()

echo "============================================"
echo " CodingLLM → Google Drive 동기화"
echo "============================================"
echo "소스: $SOURCE"
echo "타겟: $TARGET"
$DRY_RUN && echo "모드: DRY-RUN (실제 변경 없음)"
echo "--------------------------------------------"

###############################################################################
# Step 1: rsync — 비-MD 파일 동기화
###############################################################################
echo ""
echo "[Step 1/4] rsync: 비-MD 파일 동기화..."

RSYNC_EXCLUDES=($(build_rsync_excludes))
RSYNC_OPTS=(
  -rltv
  --no-perms --no-owner --no-group
  "${RSYNC_EXCLUDES[@]}"
)

if $DRY_RUN; then
  RSYNC_OPTS+=(--dry-run)
fi

rsync_output=$(rsync "${RSYNC_OPTS[@]}" "$SOURCE/" "$TARGET/" 2>&1)
rsync_exit=$?
if [ $rsync_exit -ne 0 ] && [ $rsync_exit -ne 23 ]; then
  echo "  WARNING: rsync가 오류 코드 $rsync_exit 로 종료됨"
fi
# rsync 출력에서 실제 파일 전송 건수 세기 (디렉토리 제외)
while IFS= read -r line; do
  # rsync 출력에서 파일 행만 카운트 (끝이 /가 아닌 것)
  if [[ -n "$line" && "$line" != */ && "$line" != "sending "* && "$line" != "total "* && "$line" != "sent "* && "$line" != "" ]]; then
    ((copied++))
  fi
done <<< "$rsync_output"

if [ -n "$rsync_output" ]; then
  echo "$rsync_output" | head -30
  rsync_total=$(echo "$rsync_output" | wc -l)
  if [ "$rsync_total" -gt 30 ]; then
    echo "  ... (총 ${rsync_total}줄, 상위 30줄만 표시)"
  fi
fi

echo "  → 비-MD 파일 전송: ${copied}건"

###############################################################################
# Step 2: pandoc — MD → DOCX 변환
###############################################################################
echo ""
echo "[Step 2/4] pandoc: MD → DOCX 변환..."

while IFS= read -r md_file; do
  rel_path="${md_file#$SOURCE/}"
  docx_path="$TARGET/${rel_path%.md}.docx"

  # 증분: 소스가 더 최신일 때만 변환
  if [ -f "$docx_path" ] && [ ! "$md_file" -nt "$docx_path" ]; then
    ((skipped++))
    continue
  fi

  if $DRY_RUN; then
    if [ ! -f "$docx_path" ]; then
      echo "  [NEW]     ${rel_path} → ${rel_path%.md}.docx"
    else
      echo "  [UPDATE]  ${rel_path} → ${rel_path%.md}.docx"
    fi
    ((converted++))
    continue
  fi

  # 타겟 디렉토리 생성
  mkdir -p "$(dirname "$docx_path")"

  # MD 내 마크다운 링크의 .md를 .docx로 치환 후 pandoc 변환
  # perl 사용: macOS BSD sed의 선택적 캡처 그룹 비호환 문제 회피
  pandoc_err=$(perl -pe 's/\]\(([^)]*?)\.md(#[^)"]*)?\)/"](" . $1 . ".docx" . ($2 \/\/ "") . ")"/ge' "$md_file" | \
    pandoc -o "$docx_path" --from markdown --to docx \
      --resource-path="$(dirname "$md_file")" 2>&1)
  if [ $? -eq 0 ]; then
    echo "  [OK]      ${rel_path%.md}.docx"
    ((converted++))
  else
    echo "  [FAIL]    ${rel_path} — ${pandoc_err}"
    failed_files+=("$rel_path: $pandoc_err")
    ((failed++))
  fi
done < <(eval "find \"$SOURCE\" -name '*.md' $(build_find_excludes)" | sort)

echo "  → 변환: ${converted}건, 스킵(최신): ${skipped}건, 실패: ${failed}건"

###############################################################################
# Step 3: 타겟 전용 파일 정리
###############################################################################
echo ""
echo "[Step 3/4] 타겟 전용 파일 정리..."

deleted_files=()

while IFS= read -r target_file; do
  rel="${target_file#$TARGET/}"

  # .DS_Store는 macOS가 자동 생성하므로 무시
  [[ "$(basename "$rel")" == ".DS_Store" ]] && continue

  should_delete=false

  if [[ "$rel" == *.md ]]; then
    # MD 파일: 타겟에 MD가 있으면 항상 삭제 (DOCX로 변환됨, 원본은 Git에만 보관)
    should_delete=true
  elif [[ "$rel" == *.docx ]]; then
    # DOCX: 소스에 대응 .md 또는 .docx가 있는지 확인
    md_counterpart="$SOURCE/${rel%.docx}.md"
    docx_counterpart="$SOURCE/$rel"
    if [ ! -f "$md_counterpart" ] && [ ! -f "$docx_counterpart" ]; then
      should_delete=true
    fi
  else
    # 기타 파일: 소스에 동일 파일이 있는지 확인
    if [ ! -f "$SOURCE/$rel" ]; then
      should_delete=true
    fi
  fi

  if $should_delete; then
    if $DRY_RUN; then
      echo "  [DELETE]  $rel"
      # 소스에 없는 파일이 삭제될 때 경고
      if [[ "$rel" == 06_infra/* ]]; then
        echo "  ⚠️  경고: 06_infra/ 파일이 소스에 없습니다. 보존이 필요하면 소스에 추가하세요."
      fi
    else
      rm -f "$target_file"
      echo "  [DELETED] $rel"
    fi
    deleted_files+=("$rel")
    ((deleted++))
  fi
done < <(find "$TARGET" -type f 2>/dev/null | sort)

# 빈 디렉토리 정리
if ! $DRY_RUN; then
  find "$TARGET" -type d -empty -delete 2>/dev/null
fi

echo "  → 삭제: ${deleted}건"

###############################################################################
# Step 4: 결과 리포트
###############################################################################
echo ""
echo "============================================"
echo " 동기화 완료 리포트"
echo "============================================"
$DRY_RUN && echo "⚠️  DRY-RUN 모드: 실제 변경 없음"
echo ""
echo "  비-MD 파일 복사:  ${copied}건"
echo "  MD→DOCX 변환:    ${converted}건"
echo "  MD→DOCX 스킵:    ${skipped}건 (이미 최신)"
echo "  불필요 파일 삭제: ${deleted}건"
echo "  변환 실패:        ${failed}건"

if [ ${#failed_files[@]} -gt 0 ]; then
  echo ""
  echo "❌ 변환 실패 파일 목록:"
  for f in "${failed_files[@]}"; do
    echo "  - $f"
  done
fi

if [ ${#deleted_files[@]} -gt 0 ] && $DRY_RUN; then
  echo ""
  echo "🗑️  삭제 예정 파일:"
  for f in "${deleted_files[@]}"; do
    echo "  - $f"
  done
fi

echo ""
echo "============================================"

# 실패가 있으면 비정상 종료
[ "$failed" -gt 0 ] && exit 1
exit 0
