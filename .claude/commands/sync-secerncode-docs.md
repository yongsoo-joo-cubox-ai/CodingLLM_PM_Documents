---
description: SecernCode(시선코드) Go 프로젝트의 MD 문서를 소스코드 변경에 맞춰 자동 갱신. git pull 후 scan-packages.sh로 outdated 패키지 감지, AGENTS.md(46개)/feature_summary/README 최신화. "sync docs", "문서 갱신", "AGENTS.md 업데이트", "시선코드 문서", "SecernCode 문서", "패키지 스캔", "outdated" 등에 반응. PM 문서(CodingLLM) 갱신이나 Google Drive 동기화와는 다른 스킬.
allowed-tools: Bash(bash:*), Bash(git:*), Read, Edit, Write, Glob, Grep
---

# SecernCode 문서 동기화

SecernCode 프로젝트의 MD 문서를 코드 변경에 맞춰 자동 갱신한다.

## 사용법

```
/sync-docs              # 변경된 패키지만 갱신 (기본)
/sync-docs --full       # 전체 패키지 갱신
/sync-docs --dry-run    # 미리보기 (변경 없음)
/sync-docs internal/api # 특정 패키지만 갱신
```

## 워크플로

아래 단계를 순서대로 실행하세요.

### 0단계: 헬스체크

```bash
bash /Users/ysjoo/Documents/GitHub/_coding_llm/SecernCode/.claude/scripts/scan-packages.sh --health-check
```

- 결과가 `"health": "error"` → 중단. 스킬 업데이트 필요 안내 (어떤 체크가 실패했는지 보고)
- 결과가 `"health": "warning"` → 경고 표시 후 사용자에게 계속 여부 확인
- 결과가 `"health": "ok"` → 다음 단계로 자동 진행

### 1단계: 사전 점검 및 코드 최신화

```bash
cd /Users/ysjoo/Documents/GitHub/_coding_llm/SecernCode
git status --short
```

- 커밋되지 않은 변경이 있으면 사용자에게 알리고 계속할지 확인
- 변경이 있으면 `git stash` 제안

```bash
git pull --ff-only
```

- `--ff-only`로 안전하게 pull. 충돌 시 보고 후 중단
- pull 실패 시 사용자에게 수동 해결 안내

### 2단계: 패키지 스캔

```bash
bash /Users/ysjoo/Documents/GitHub/_coding_llm/SecernCode/.claude/scripts/scan-packages.sh $ARGUMENTS
```

스크립트가 JSON을 출력한다. 결과에서:
- `packages` 배열: 각 패키지의 상태 (`new`, `modified`, `existing`)
- `agents_md_outdated: true`인 패키지가 갱신 대상
- `deleted_packages`: AGENTS.md는 있지만 .go 파일이 없는 디렉토리
- `target_count`: 대상 패키지 수

### 3단계: dry-run 분기

`$ARGUMENTS`에 `--dry-run`이 포함되면:
- 스캔 결과를 보기 좋게 요약하여 보고
- 갱신 대상 파일 목록, 새로 생성될 AGENTS.md, 삭제 경고 출력
- 여기서 중단. 파일 수정 안 함

### 4단계: AGENTS.md 갱신

각 대상 패키지에 대해:

#### 4-a. 새 패키지 (status: "new")

해당 디렉토리의 .go 파일을 읽고 AGENTS.md를 새로 생성한다. 기존 AGENTS.md 파일의 형식을 따를 것.

템플릿 참고: `/Users/ysjoo/Documents/GitHub/_coding_llm/SecernCode/internal/llm/agent/AGENTS.md`

구조:
```markdown
<!-- Generated: YYYY-MM-DD | Updated: YYYY-MM-DD -->
# {패키지명}

## Purpose
{.go 파일의 패키지 주석에서 추출}

## Key Files
| File | Description |
|------|-------------|
| `file.go` | {파일 첫 주석 또는 주요 함수에서 추론} |

## Subdirectories
| Directory | Purpose |
|-----------|---------|
| `sub/` | {하위 AGENTS.md 또는 파일 내용에서 추론} |

## Dependencies
**Internal:** {프로젝트 내 import}
**External:** {go.mod 의존성 중 이 패키지가 사용하는 것}

## For AI Agents
{이 패키지 작업 시 유의사항}

<!-- MANUAL: Any manually added notes below this line are preserved on regeneration -->
```

#### 4-b. 변경 패키지 (status: "modified", agents_md_outdated: true)

기존 AGENTS.md를 읽고 다음 섹션만 갱신:
- **Key Files 테이블**: 현재 .go 파일 목록으로 재생성. 기존 설명은 최대한 보존
- **Subdirectories 테이블**: 현재 하위 디렉토리로 재생성
- **Dependencies**: 현재 import에서 재추출
- **`<!-- Generated: -->` 라인**: Updated 날짜 갱신

**절대 수정하지 않을 섹션:**
- Purpose (수동 작성)
- For AI Agents (수동 작성)
- `<!-- MANUAL: -->` 이후 모든 내용

#### 4-c. 삭제 감지

`deleted_packages`가 비어있지 않으면 경고 메시지 출력. 자동 삭제하지 않음.

### 5단계: Tier 2 판단 (선택적)

`changed_files`에 특정 파일이 포함된 경우 추가 갱신을 **제안**한다 (자동 실행 아님):

| 변경 파일 | 영향 | 제안 |
|----------|------|------|
| `internal/llm/tools/*.go` | 도구 추가/제거 | `docs/feature_summary.md` 도구 목록 갱신 제안 |
| `internal/llm/agent/agent.go` | 에이전트 로직 변경 | `docs/feature_summary.md` 에이전트 기능 갱신 제안 |
| `internal/config/config.go` | 설정 변경 | `README.md` 설정 예시 갱신 제안 |
| `cmd/root.go`, `cmd/serve.go` | CLI 변경 | `README.md` 사용법 갱신 제안 |
| `internal/api/routes.go` | API 변경 | `internal/api/AGENTS.md` 엔드포인트 테이블 갱신 |
| `go.mod` | 의존성 변경 | 루트 `AGENTS.md` Dependencies 갱신 |

사용자가 동의하면 해당 파일도 갱신한다.

### 6단계: 동기화 기록

모든 갱신이 성공하면:

```bash
git rev-parse HEAD > /Users/ysjoo/Documents/GitHub/_coding_llm/SecernCode/.claude/.last-sync
```

하나라도 실패한 경우 `.last-sync`를 갱신하지 않는다.

### 7단계: 결과 보고

한글로 요약 보고:

```
## 동기화 완료

- 스캔 모드: incremental (마지막 동기화: abc1234 → def5678)
- 갱신된 AGENTS.md: 3건
  - internal/api/AGENTS.md (Key Files 갱신)
  - internal/llm/tools/AGENTS.md (새 파일 추가)
  - internal/config/AGENTS.md (Dependencies 갱신)
- 새로 생성: 1건
  - internal/newpkg/AGENTS.md
- 삭제 경고: 0건
- Tier 2 제안: feature_summary.md 도구 목록 갱신 필요
- 실패: 0건
```

## 오류 처리

- git pull 실패 → 보고 후 중단
- scan-packages.sh 실패 → 보고 후 중단
- 개별 AGENTS.md 갱신 실패 → 해당 파일 건너뛰고 나머지 계속, 최종 보고에 포함
- 전체 실패 시 `.last-sync` 미갱신

## 주의사항

- `<!-- MANUAL: -->` 마커 아래 내용은 절대 수정하지 않는다
- Purpose, For AI Agents 섹션은 수동 작성 영역이므로 수정하지 않는다
- Tier 2 갱신은 자동이 아닌 제안 방식이다. 사용자 동의 후 실행한다
- AGENTS.md 외 문서(feature_summary, README)는 직접 수정하지 않고 제안만 한다
