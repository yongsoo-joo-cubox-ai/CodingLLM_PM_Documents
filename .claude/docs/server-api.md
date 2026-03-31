# 서버 환경 및 API 레퍼런스

> 이 문서는 CLAUDE.md의 레퍼런스입니다. 핵심 지침은 [CLAUDE.md](../../CLAUDE.md)를 참조하세요.

## 서버 환경

| 환경 | Studio 포트 | Engine 포트 | 비고 |
|------|-----------|-----------|------|
| **Demo** | 5174 | 3100 | 고객 데모용 (http://172.16.100.116:5174/landing) |
| **Dev** | 5173 | 3000 | 개발용 (기존) |
| **Playground** | 4000 + 프로젝트 ID | 동적 | Docker 기반 전체 앱 배포, FE-BE 연동 |

- Demo 도메인: https://coco.secernai.net

## API 엔드포인트 요약

```bash
# 핵심 엔드포인트
POST /agent/agentic/v2/stream  # 스트리밍 코드 생성 (권장)
POST /agent/review             # 코드 리뷰
POST /agent/qa                 # 프레임워크 Q&A
GET  /agent/models             # 사용 가능 모델 목록
GET  /_health                  # 헬스 체크
```

> API 상세 명세: `02_implementation/05_api_reference_ko.md` 참조
