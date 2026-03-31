# Git LFS 관리

> 이 문서는 CLAUDE.md의 레퍼런스입니다. 핵심 지침은 [CLAUDE.md](../../CLAUDE.md)를 참조하세요.

대용량 바이너리 파일은 Git LFS로 관리합니다.

## GitHub LFS 무료 할당량

| 항목 | 한도 |
|------|------|
| 저장소 용량 | 1 GB |
| 월간 대역폭 | 1 GB |

## 현재 LFS 사용량 (2026-02-12 기준)

| 분류 | 파일 수 | 크기 | 비고 |
|------|--------|------|------|
| mov (데모 영상) | 8개 | ~54 MB | `_00_work/260127-260211/` |
| zip (KB/스펙) | 5개 | ~80 MB | xframe5 KB 74MB + UASL/dist 소형 4개 |
| **합계** | **13개** | **~134 MB** | 무료 한도의 ~13% |

## 추적 대상 (`.gitattributes`)

```
*.mov filter=lfs diff=lfs merge=lfs -text
*.zip filter=lfs diff=lfs merge=lfs -text
```

## 관리 규칙

- 대용량 바이너리(영상, 압축파일, 이미지 등) 추가 시 반드시 LFS 추적 확인
- `git lfs ls-files --size`로 현재 사용량 확인 후 추가
- 무료 한도(1GB) 초과 전 정리 또는 유료 전환 검토
- 새로운 확장자 추가 시 `.gitattributes`에 `git lfs track` 반영
