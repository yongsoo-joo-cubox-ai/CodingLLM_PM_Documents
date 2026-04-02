---
description: 서브모듈(SecernCode, secern-vllm-ext)의 origin/dev 최신 변경을 현재 브랜치로 머지. 변경사항 감지 → 충돌 검증 → 머지 → PM 레포 서브모듈 포인터 갱신까지 자동 수행. "시선코드 머지", "dev 동기화", "dev 싱크", "merge-dev", "코드 최신화", "SecernCode 머지", "서브모듈 머지", "vllm-ext 머지", "서브모듈 업데이트", "서브모듈 최신화" 등에 반응.
allowed-tools: Bash(bash:*), Bash(git:*), Read, Glob, Grep
---

# 서브모듈 Dev 브랜치 머지

서브모듈의 `origin/dev` 최신 변경 사항을 현재 작업 브랜치로 안전하게 머지한다.

## 대상 서브모듈

| 서브모듈 | 경로 | 소스 |
|----------|------|------|
| SecernCode | `SecernCode/` | `origin/dev` |
| secern-vllm-ext | `secern-vllm-ext/` | `origin/dev` |

각 서브모듈의 현재 체크아웃 브랜치를 자동 감지하여 `origin/dev`를 머지한다. 브랜치를 하드코딩하지 않는다.

## 사용법

```
/merge-dev                    # 모든 서브모듈 머지 (기본)
/merge-dev secerncode         # SecernCode만
/merge-dev vllm-ext           # secern-vllm-ext만
/merge-dev --dry-run          # 변경사항 확인만 (머지 안 함)
```

`$ARGUMENTS`를 파싱하여 대상과 모드를 결정한다.

## 워크플로

### 0단계: 사전 점검

PM 레포(CodingLLM_PM_Documents)의 루트에서 시작한다.

```bash
cd /Users/ysjoo/Documents/GitHub/_coding_llm/CodingLLM_PM_Documents
git status --short
```

PM 레포에 커밋되지 않은 변경이 있으면 사용자에게 알린다 (중단하지는 않음).

### 1단계: 각 서브모듈 순회

대상 서브모듈 각각에 대해 아래 과정을 순서대로 실행한다. 서브모듈 간에는 독립적이므로 하나가 실패해도 다른 서브모듈은 계속 진행한다.

#### 1-a. 로컬 상태 확인

```bash
cd <서브모듈 경로>
git status --short
git branch --show-current
```

- 커밋되지 않은 변경이 있으면 사용자에게 알리고 `git stash` 제안. 사용자가 거부하면 해당 서브모듈 건너뛰기
- 현재 브랜치가 `dev`이면 경고: "dev 브랜치에 직접 머지하려고 합니다. 작업 브랜치로 전환하시겠습니까?"

#### 1-b. 최신 변경 가져오기

```bash
git fetch origin dev
```

fetch 실패 시 → 네트워크/권한 문제 안내 후 해당 서브모듈 건너뛰기.

#### 1-c. 변경사항 감지

```bash
# 현재 브랜치 기준으로 origin/dev에 있는 새 커밋 확인
git log HEAD..origin/dev --oneline
git diff HEAD..origin/dev --stat
```

- 새 커밋이 없으면 → "이미 최신 상태" 보고 후 다음 서브모듈로
- 새 커밋이 있으면 → 커밋 목록과 변경 파일 요약 출력

#### 1-d. 충돌 사전 검증

머지를 실행하기 전에 반드시 충돌 여부를 먼저 확인한다. 이것이 인수 조건이다.

```bash
# 충돌 확인용 시뮬레이션 (실제 머지하지 않음)
git merge --no-commit --no-ff origin/dev
```

결과에 따라:

**충돌 없음 (머지 성공):**
```bash
# 시뮬레이션 정리
git merge --abort
```
→ 다음 단계(실제 머지)로 진행

**충돌 발생:**
```bash
# 충돌 파일 목록 확인
git diff --name-only --diff-filter=U
# 시뮬레이션 정리
git merge --abort
```
→ 충돌 파일 목록을 보여주고 해당 서브모듈 머지 중단. 사용자에게 수동 해결 안내:
```
## 충돌 발생 — 수동 해결 필요

충돌 파일:
- internal/config/config.go
- internal/api/routes.go

해결 방법:
1. cd <서브모듈 경로>
2. git merge origin/dev
3. 충돌 파일 수동 수정
4. git add <수정한 파일>
5. git merge --continue
```

#### 1-e. 머지 실행

충돌 검증을 통과한 경우에만 실행한다.

```bash
git merge origin/dev --no-edit
```

머지 결과를 확인한다:
```bash
git log --oneline -3
```

#### 1-f. PM 레포 서브모듈 포인터 갱신

서브모듈 머지가 성공하면 PM 레포로 돌아와서:

```bash
cd /Users/ysjoo/Documents/GitHub/_coding_llm/CodingLLM_PM_Documents
git add <서브모듈 경로>
```

### 2단계: 결과 보고

모든 서브모듈 처리가 끝나면 한글로 요약 보고한다:

```
## 서브모듈 머지 결과

### SecernCode (<현재 브랜치> ← origin/dev)
- 상태: 머지 완료
- 새 커밋: 5건 (dc4f469..a1b2c3d)
- 변경 파일: 12건 (+340, -45)
- PM 서브모듈 포인터: 갱신 완료

### secern-vllm-ext (<현재 브랜치> ← origin/dev)
- 상태: 이미 최신
- 새 커밋: 0건

### PM 레포
- git add 대상: SecernCode
- 커밋 필요: 예 (사용자가 직접 커밋)
```

커밋은 사용자가 직접 한다. 자동 커밋하지 않는다.

## dry-run 모드

`$ARGUMENTS`에 `--dry-run`이 포함되면:
- 0단계 ~ 1-c단계(변경사항 감지)까지만 실행
- 충돌 검증(1-d)과 실제 머지(1-e)는 실행하지 않음
- 각 서브모듈의 새 커밋 목록과 변경 파일 요약만 출력

## 오류 처리

| 상황 | 대응 |
|------|------|
| fetch 실패 | 네트워크/인증 안내, 해당 서브모듈 건너뛰기 |
| 충돌 발생 | 충돌 파일 목록 + 수동 해결 가이드 출력, 해당 서브모듈 건너뛰기 |
| merge 실패 | 에러 메시지 보고, merge --abort로 정리 |
| 서브모듈 경로 없음 | 경고 후 건너뛰기 |

## 주의사항

- 충돌 검증을 통과하지 않으면 절대 머지하지 않는다
- 자동 커밋하지 않는다 — PM 레포의 `git add`까지만 수행
- stash한 변경이 있으면 머지 후 `git stash pop` 안내
- 이 스킬은 코드 머지만 담당한다. PM 문서 갱신은 `/sync-pm-from-secerncode` 스킬을 사용
