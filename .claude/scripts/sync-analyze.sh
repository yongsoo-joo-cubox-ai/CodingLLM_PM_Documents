#!/bin/bash
# sync-analyze.sh — 소스/타겟 동기화 상태 분석 (크기·시간 비교 포함)
set -uo pipefail

SOURCE="/Users/ysjoo/Documents/GitHub/CodingLLM_PM_Documents"
TARGET="/Users/ysjoo/Library/CloudStorage/GoogleDrive-yongsoo.joo@cubox.ai/공유 드라이브/CodingLLM_Project/01_Documents"

EXCLUDE_PATTERN='\.git/|\.obsidian/|\.claude/|\.playwright-mcp/|\.DS_Store|\.gitignore|\.gitattributes|CLAUDE\.md'

###############################################################################
# 사전 검증
###############################################################################
if [ ! -d "$SOURCE" ]; then
  echo "ERROR: 소스 경로 없음: $SOURCE"; exit 1
fi
if [ ! -d "$TARGET" ]; then
  echo "ERROR: 타겟 경로 없음 (Google Drive 마운트 확인): $TARGET"; exit 1
fi

###############################################################################
# 파일 목록 수집
###############################################################################
src_all=$(find "$SOURCE" -type f \
  -not -path '*/.git/*' -not -path '*/.obsidian/*' -not -path '*/.claude/*' \
  -not -path '*/.playwright-mcp/*' -not -name '.DS_Store' \
  -not -name '.gitignore' -not -name '.gitattributes' -not -name 'CLAUDE.md')

src_md=$(echo "$src_all" | grep '\.md$' || true)
src_nonmd=$(echo "$src_all" | grep -v '\.md$' || true)

tgt_all=$(find "$TARGET" -type f -not -name '.DS_Store' 2>/dev/null || true)
tgt_docx=$(echo "$tgt_all" | grep '\.docx$' || true)

src_total=$(echo "$src_all" | grep -c . || echo 0)
src_md_count=$(echo "$src_md" | grep -c . || echo 0)
src_nonmd_count=$(echo "$src_nonmd" | grep -c . || echo 0)
tgt_total=$(echo "$tgt_all" | grep -c . || echo 0)
tgt_docx_count=$(echo "$tgt_docx" | grep -c . || echo 0)

pandoc_ver=$(pandoc --version 2>/dev/null | head -1 || echo "미설치")

###############################################################################
# 전체 현황 출력
###############################################################################
echo "============================================"
echo " 동기화 상태 분석"
echo "============================================"
echo ""
echo "[SUMMARY]"
echo "소스 전체: ${src_total}건 (MD: ${src_md_count}, 비-MD: ${src_nonmd_count})"
echo "타겟 전체: ${tgt_total}건 (DOCX: ${tgt_docx_count})"
echo "pandoc: ${pandoc_ver}"
echo ""

###############################################################################
# 파일별 비교
###############################################################################
sync_needed=0
up_to_date=0
new_files=0
changed_files=0
delete_files=0

echo "[SYNC NEEDED]"
printf "%-8s  %-60s  %10s  %10s  %-16s  %s\n" "상태" "파일" "소스크기" "타겟크기" "소스수정일" "사유"
echo "------  ------------------------------------------------------------  ----------  ----------  ----------------  --------"

# 1) MD 파일 → DOCX 비교
while IFS= read -r md_file; do
  [ -z "$md_file" ] && continue
  rel="${md_file#$SOURCE/}"
  docx_path="$TARGET/${rel%.md}.docx"
  display_rel="${rel%.md}.docx"

  src_size=$(stat -f%z "$md_file" 2>/dev/null || echo 0)
  src_mtime=$(stat -f%m "$md_file" 2>/dev/null || echo 0)
  src_date=$(date -r "$src_mtime" '+%Y-%m-%d %H:%M' 2>/dev/null || echo "?")
  src_size_h=$(numfmt --to=iec "$src_size" 2>/dev/null || echo "${src_size}B")

  if [ ! -f "$docx_path" ]; then
    printf "%-8s  %-60s  %10s  %10s  %-16s  %s\n" "[신규]" "$display_rel" "$src_size_h" "-" "$src_date" "타겟 없음"
    ((new_files++))
    ((sync_needed++))
  else
    tgt_size=$(stat -f%z "$docx_path" 2>/dev/null || echo 0)
    tgt_mtime=$(stat -f%m "$docx_path" 2>/dev/null || echo 0)
    tgt_size_h=$(numfmt --to=iec "$tgt_size" 2>/dev/null || echo "${tgt_size}B")

    if [ "$md_file" -nt "$docx_path" ]; then
      printf "%-8s  %-60s  %10s  %10s  %-16s  %s\n" "[변경]" "$display_rel" "$src_size_h" "$tgt_size_h" "$src_date" "소스가 더 최신"
      ((changed_files++))
      ((sync_needed++))
    else
      ((up_to_date++))
    fi
  fi
done <<< "$src_md"

# 2) 비-MD 파일 비교
while IFS= read -r src_file; do
  [ -z "$src_file" ] && continue
  rel="${src_file#$SOURCE/}"
  tgt_file="$TARGET/$rel"

  src_size=$(stat -f%z "$src_file" 2>/dev/null || echo 0)
  src_mtime=$(stat -f%m "$src_file" 2>/dev/null || echo 0)
  src_date=$(date -r "$src_mtime" '+%Y-%m-%d %H:%M' 2>/dev/null || echo "?")
  src_size_h=$(numfmt --to=iec "$src_size" 2>/dev/null || echo "${src_size}B")

  if [ ! -f "$tgt_file" ]; then
    printf "%-8s  %-60s  %10s  %10s  %-16s  %s\n" "[신규]" "$rel" "$src_size_h" "-" "$src_date" "타겟 없음"
    ((new_files++))
    ((sync_needed++))
  else
    tgt_size=$(stat -f%z "$tgt_file" 2>/dev/null || echo 0)
    tgt_size_h=$(numfmt --to=iec "$tgt_size" 2>/dev/null || echo "${tgt_size}B")

    if [ "$src_size" -ne "$tgt_size" ] || [ "$src_file" -nt "$tgt_file" ]; then
      reason=""
      [ "$src_size" -ne "$tgt_size" ] && reason="크기 차이"
      [ "$src_file" -nt "$tgt_file" ] && { [ -n "$reason" ] && reason="$reason + 시간 차이" || reason="시간 차이"; }
      printf "%-8s  %-60s  %10s  %10s  %-16s  %s\n" "[변경]" "$rel" "$src_size_h" "$tgt_size_h" "$src_date" "$reason"
      ((changed_files++))
      ((sync_needed++))
    else
      ((up_to_date++))
    fi
  fi
done <<< "$src_nonmd"

# 3) 타겟에만 있는 파일 (삭제 대상)
while IFS= read -r tgt_file; do
  [ -z "$tgt_file" ] && continue
  rel="${tgt_file#$TARGET/}"
  [[ "$(basename "$rel")" == ".DS_Store" ]] && continue

  should_flag=false
  if [[ "$rel" == *.docx ]]; then
    [ ! -f "$SOURCE/${rel%.docx}.md" ] && [ ! -f "$SOURCE/$rel" ] && should_flag=true
  elif [[ "$rel" == *.md ]]; then
    should_flag=true
  else
    [ ! -f "$SOURCE/$rel" ] && should_flag=true
  fi

  if $should_flag; then
    tgt_size=$(stat -f%z "$tgt_file" 2>/dev/null || echo 0)
    tgt_size_h=$(numfmt --to=iec "$tgt_size" 2>/dev/null || echo "${tgt_size}B")
    printf "%-8s  %-60s  %10s  %10s  %-16s  %s\n" "[삭제]" "$rel" "-" "$tgt_size_h" "-" "소스 없음"
    ((delete_files++))
    ((sync_needed++))
  fi
done <<< "$tgt_all"

if [ "$sync_needed" -eq 0 ]; then
  echo "(동기화 대상 없음)"
fi

###############################################################################
# 최종 요약
###############################################################################
echo ""
echo "[RESULT]"
echo "  동기화 필요: ${sync_needed}건 (신규: ${new_files}, 변경: ${changed_files}, 삭제: ${delete_files})"
echo "  최신 상태:   ${up_to_date}건"
echo ""
echo "============================================"
