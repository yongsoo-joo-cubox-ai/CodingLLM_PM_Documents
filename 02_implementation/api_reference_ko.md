# API 레퍼런스

| 항목 | 내용 |
|------|------|
| **문서번호** | SAI-IMPL-2026-005 |
| **작성일** | 2026년 1월 8일 |
| **개정일** | 2026년 2월 12일 |
| **버전** | v2.0 |
| **보안등급** | 대외비 |
| **작성** | Secern AI |

> **구현 문서 5/5** | 이전: [기술 스택](./phase2_tech_stack_ko.md) | [폴더 인덱스](./README.md)

---

## API Stability Levels

| Level | Description | Breaking Changes |
|-------|-------------|------------------|
| **Stable** | Production-ready endpoints | Announced in advance |
| **Beta** | May change without notice | Possible |
| **Internal** | Research/benchmarking only | Frequent |

> **Note**: Internal endpoints should NOT be used in production or customer-facing applications.

---

## Quick Reference - curl Examples

### Code Generation (Streaming)

```bash
# Agentic streaming generation (recommended)
curl -X POST http://localhost:3000/agent/agentic/v2/stream \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "product": "xframe5-ui",
    "prompt": "회원 목록 화면을 생성해주세요",
    "project_structure": {
      "name": "my-project",
      "views_path": "src/views",
      "scripts_path": "src/scripts",
      "existing_entities": []
    },
    "preferences": {
      "language": "ko",
      "autonomous_mode": true,
      "confirm_before_write": false
    }
  }'
```

### Code Review

```bash
curl -X POST http://localhost:3000/agent/review \
  -H "Content-Type: application/json" \
  -d '{
    "product": "xframe5-ui",
    "input": {
      "code": "<Screen id=\"scr_member_list\"><Dataset id=\"ds_member\"/></Screen>",
      "fileType": "xml",
      "context": "회원 목록 화면"
    },
    "options": {
      "language": "ko",
      "reviewFocus": ["syntax", "patterns", "naming"]
    },
    "context": {
      "fileName": "member_list.xml"
    }
  }'
```

### Q&A (Knowledge Base)

```bash
curl -X POST http://localhost:3000/agent/qa \
  -H "Content-Type: application/json" \
  -d '{
    "product": "xframe5-ui",
    "input": {
      "question": "Dataset에서 데이터를 필터링하는 방법은?",
      "context": "그리드와 연결된 목록 화면 개발 중"
    },
    "options": {
      "language": "ko",
      "includeExamples": true,
      "maxReferences": 5
    }
  }'
```

### Health Check

```bash
curl http://localhost:3000/_health
```

### List Available Models

```bash
curl http://localhost:3000/agent/models
```

---

## Endpoints Overview

### Core Endpoints

| Endpoint | Method | Description | Status |
|----------|--------|-------------|--------|
| `/_health` | GET | Server health check | ✅ Stable |
| `/agent/review` | POST | AI-powered code review | ✅ Stable |
| `/agent/qa` | POST | Framework Q&A chatbot | ✅ Stable |
| `/agent/models` | GET | List available LLM models | ✅ Stable |
| `/agent/models/{id}/health` | POST | Check model health | ✅ Stable |
| `/api/knowledge_bases/bulk` | POST | Bulk import knowledge entries | ✅ Stable |

### Streaming Endpoints (SSE)

| Endpoint | Method | Description | Status |
|----------|--------|-------------|--------|
| `/agent/agentic/v2/stream` | POST | **Primary** streaming generation | ✅ **Recommended** |
| `/agent/agentic/stream` | POST | Legacy streaming (v1) | ⚠️ Deprecated |
| `/agent/agentic/respond` | POST | Answer mid-generation questions | ✅ Active |
| `/agent/agentic/session/{session_id}` | GET | Get session status | ✅ Active |
| `/agent/agentic/session/{session_id}` | DELETE | Cancel/delete session | ✅ Active |

### MCP Server Endpoints (v2.0 신규)

> MCP 서버는 Coco Engine이 내부적으로 호출합니다. 직접 사용자가 호출하지 않으며, `product` 파라미터에 따라 자동 라우팅됩니다.

| MCP Server | 역할 | 프로토콜 | Status |
|------------|------|----------|--------|
| `xframe5-compiler` | xFrame5 XML + JS 코드 생성 | stdio | ✅ Active |
| `xframe5-validator` | xFrame5 API 허용목록 검증 | stdio | ✅ Active |
| `vue-compiler` | Vue3 SFC (.vue) 코드 생성 | stdio | ✅ Active |
| `spring-compiler` | Spring 코드 생성 | stdio | 📋 Phase 2 |

### Internal/Experimental Endpoints

| Endpoint | Method | Description | Status |
|----------|--------|-------------|--------|
| `/agent/coding/stream` | POST | Python coding problems (LiveBench) | ⚠️ Internal only |
| `/agent/coding/generate` | POST | Python coding problems (sync) | ⚠️ Internal only |

---

## Agentic Streaming Generation (v2)

**Primary endpoint for multi-step code generation with real-time progress.**

```
POST /agent/agentic/v2/stream
```

### Request

```json
{
  "product": "xframe5-ui",
  "prompt": "회원 관리 화면을 생성해주세요. CRUD 기능 포함.",
  "project_structure": {
    "name": "my-project",
    "views_path": "src/views",
    "scripts_path": "src/scripts",
    "existing_entities": ["Member", "Department"]
  },
  "preferences": {
    "language": "ko",
    "autonomous_mode": true,
    "confirm_before_write": false
  },
  "api_key": "optional-user-key"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `product` | string | ✅ | Product identifier: `xframe5-ui`, `vue3`, `spring` (Phase 2) |
| `prompt` | string | ✅ | Natural language request |
| `project_structure.name` | string | | Project name |
| `project_structure.views_path` | string | | Path for view files |
| `project_structure.scripts_path` | string | | Path for script files |
| `project_structure.existing_entities` | array | | Existing entity names for reference |
| `preferences.language` | string | | Output language (`ko`, `en`) |
| `preferences.autonomous_mode` | boolean | | If true, minimize questions |
| `preferences.confirm_before_write` | boolean | | If true, confirm before writing files |
| `api_key` | string | | User identification (or use `X-API-Key` header) |

### Response (SSE Stream)

Server-Sent Events with JSON payloads. Each event has a `type` field.

**Event Types:**

1. **`session_started`** - Session created
```json
{
  "type": "session_started",
  "session_id": "sess_abc123",
  "message": "Starting agentic generation"
}
```

2. **`progress`** - Phase updates
```json
{
  "type": "progress",
  "phase": "intent_analysis",
  "message": "Analyzing request intent...",
  "detail": "Detected: xFrame5 UI generation"
}
```

3. **`decomposition`** - Task breakdown
```json
{
  "type": "decomposition",
  "level": "entity",
  "parent": "MemberModule",
  "children": ["Member", "MemberHistory"],
  "message": "Decomposed module into 2 entities"
}
```

4. **`file`** - Generated file
```json
{
  "type": "file",
  "path": "src/views/member",
  "filename": "member_list.xml",
  "content": "<?xml version=\"1.0\"?>...",
  "action": "create",
  "message": "Generated member list screen"
}
```

5. **`question`** - Needs user input
```json
{
  "type": "question",
  "id": "q_abc123",
  "message": "목록에 몇 개의 컬럼을 표시할까요?",
  "options": [
    {"id": "5", "label": "5개 (기본)", "description": "표준 목록"},
    {"id": "10", "label": "10개", "description": "상세 목록"}
  ],
  "language": "ko",
  "blocking": true
}
```

6. **`done`** - Generation complete
```json
{
  "type": "done",
  "summary": {
    "files_created": 4,
    "files": ["member_list.xml", "member_list.js", "member_edit.xml", "member_edit.js"],
    "questions_asked": 1
  }
}
```

7. **`error`** - Generation failed
```json
{
  "type": "error",
  "code": "GENERATION_FAILED",
  "message": "LLM generation timeout",
  "recoverable": true,
  "suggestion": "Try again with simpler prompt"
}
```

### curl Example (Streaming)

```bash
curl -N -X POST http://localhost:3000/agent/agentic/v2/stream \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "product": "xframe5-ui",
    "prompt": "회원 목록 화면 생성",
    "preferences": {"language": "ko", "autonomous_mode": true}
  }'
```

The `-N` flag disables buffering to see events in real-time.

---

## Code Review Endpoint

```
POST /agent/review
```

### Request

```json
{
  "product": "xframe5-ui",
  "input": {
    "code": "<?xml version=\"1.0\"?>\n<Screen id=\"scr_member\">...</Screen>",
    "fileType": "xml",
    "context": "회원 목록 화면입니다"
  },
  "options": {
    "language": "ko",
    "reviewFocus": ["syntax", "patterns", "naming", "security"]
  },
  "context": {
    "project": "my-project",
    "fileName": "member_list.xml"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `product` | string | ✅ | Product identifier |
| `input.code` | string | ✅ | Code to review (max 50KB) |
| `input.fileType` | string | ✅ | File type: `xml`, `javascript`, `java` |
| `input.context` | string | | Description of the code |
| `options.language` | string | | Output language (`ko`, `en`) |
| `options.reviewFocus` | array | | Focus areas: `syntax`, `patterns`, `naming`, `security`, `performance` |
| `context.project` | string | | Project name |
| `context.fileName` | string | | File name for context |

### Response

```json
{
  "status": "success",
  "review": {
    "summary": "전반적으로 잘 작성된 코드입니다. 몇 가지 개선 사항이 있습니다.",
    "issues": [
      {
        "severity": "warning",
        "line": 15,
        "message": "Dataset ID가 명명 규칙을 따르지 않습니다",
        "category": "naming"
      },
      {
        "severity": "info",
        "line": 23,
        "message": "Grid 컬럼에 width 속성 추가를 권장합니다",
        "category": "patterns"
      }
    ],
    "score": {
      "overall": 75,
      "categories": {
        "syntax": 90,
        "patterns": 70,
        "naming": 60
      }
    },
    "improvements": [
      "Dataset ID를 'ds_member' 형식으로 변경하세요",
      "Grid 컬럼에 적절한 width를 지정하세요"
    ]
  },
  "meta": {
    "generator": "xframe5-ui-review-v1",
    "generation_time_ms": 1234
  }
}
```

### curl Example

```bash
curl -X POST http://localhost:3000/agent/review \
  -H "Content-Type: application/json" \
  -d '{
    "product": "xframe5-ui",
    "input": {
      "code": "<Screen id=\"scr_test\"><Dataset id=\"ds1\"/><Grid id=\"grd1\" dataset=\"ds1\"/></Screen>",
      "fileType": "xml"
    },
    "options": {
      "language": "ko",
      "reviewFocus": ["syntax", "naming"]
    }
  }'
```

---

## Q&A Endpoint

```
POST /agent/qa
```

### Request

```json
{
  "product": "xframe5-ui",
  "input": {
    "question": "Dataset에서 특정 조건으로 데이터를 필터링하는 방법은?",
    "context": "그리드와 연결된 Dataset을 사용하고 있습니다"
  },
  "options": {
    "language": "ko",
    "includeExamples": true,
    "maxReferences": 5
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `product` | string | ✅ | Product identifier |
| `input.question` | string | ✅ | Question to answer (max 5KB) |
| `input.context` | string | | Additional context |
| `options.language` | string | | Output language (`ko`, `en`) |
| `options.includeExamples` | boolean | | Include code examples |
| `options.maxReferences` | number | | Max knowledge references (default: 5) |

### Response

```json
{
  "status": "success",
  "answer": {
    "text": "Dataset에서 데이터를 필터링하려면 filter() 메서드를 사용합니다...",
    "codeExamples": [
      {
        "title": "기본 필터링",
        "code": "dataset.filter(\"status == 'active'\");",
        "language": "javascript"
      }
    ],
    "relatedTopics": ["Dataset.filter", "Dataset.clearFilter", "Grid.refresh"]
  },
  "references": [
    {
      "name": "Dataset.filter",
      "category": "api",
      "content": "filter(expression) - 데이터를 필터링합니다...",
      "relevance": 0.92
    }
  ],
  "meta": {
    "generator": "xframe5-ui-qa-v1",
    "generation_time_ms": 890
  }
}
```

### curl Example

```bash
curl -X POST http://localhost:3000/agent/qa \
  -H "Content-Type: application/json" \
  -d '{
    "product": "xframe5-ui",
    "input": {
      "question": "Grid에서 셀 편집을 활성화하는 방법은?"
    },
    "options": {
      "language": "ko",
      "includeExamples": true
    }
  }'
```

---

## Models Endpoint

List available LLM models with health status.

```
GET /agent/models
```

### Response

```json
{
  "models": [
    {
      "id": 11,
      "name": "vLLM-Qwen32B",
      "provider": "vllm",
      "model_name": "Qwen/Qwen2.5-Coder-32B-Instruct-AWQ",
      "healthy": true,
      "capability_tier": "large",
      "task_assignments": ["generation", "agentic", "review"]
    },
    {
      "id": 9,
      "name": "Ollama-Qwen7B",
      "provider": "ollama",
      "model_name": "qwen2.5-coder:7b",
      "healthy": true,
      "capability_tier": "small",
      "task_assignments": ["qa", "validation"]
    }
  ],
  "current_session_model": null
}
```

### Check Model Health

```bash
curl -X POST http://localhost:3000/agent/models/11/health
```

Response:
```json
{
  "model_id": 11,
  "model_name": "vLLM-Qwen32B",
  "healthy": true,
  "response_time_ms": 45,
  "error": null
}
```

---

## Health Endpoint

```
GET /_health
```

### Response

```json
{
  "ok": true
}
```

For detailed LLM health, use `/agent/models/{id}/health`.

---

## Agentic Session Management

### Answer a Question

When the stream returns a `question` event with `blocking: true`, answer it:

```bash
curl -X POST http://localhost:3000/agent/agentic/respond \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "sess_abc123",
    "question_id": "q_abc123",
    "answer": "5"
  }'
```

### Get Session Status

```bash
curl http://localhost:3000/agent/agentic/session/sess_abc123
```

Response:
```json
{
  "session_id": "sess_abc123",
  "status": "active",
  "current_phase": "code_generation",
  "files_completed": 2,
  "pending_questions": 0,
  "created_at": "2026-01-21T10:30:00Z"
}
```

### Cancel Session

```bash
curl -X DELETE http://localhost:3000/agent/agentic/session/sess_abc123
```

---

## Bulk Knowledge Import

```
POST /api/knowledge_bases/bulk
```

### Request

```json
{
  "entries": [
    {
      "name": "dataset_filter",
      "category": "api",
      "component": "dataset",
      "section": "method",
      "content": "# filter\n\nFilters data based on expression...",
      "relevance_tags": ["xframe5-ui", "dataset", "api"],
      "priority": "medium",
      "token_estimate": 150,
      "version": 1,
      "is_active": true
    }
  ],
  "options": {
    "generate_embeddings": true,
    "upsert_key": ["name", "component"],
    "batch_size": 100
  }
}
```

### Response

```json
{
  "status": "success",
  "stats": {
    "total": 100,
    "inserted": 95,
    "updated": 5,
    "skipped": 0,
    "failed": 0,
    "embeddings_generated": 100,
    "duration_ms": 7500
  },
  "errors": []
}
```

---

## Error Responses

All endpoints return errors in this format:

```json
{
  "status": "error",
  "error": "Error message description",
  "meta": {
    "generator": "xframe5-ui-v1",
    "timestamp": "2026-01-21T12:00:00Z"
  }
}
```

### HTTP Status Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid input parameters |
| 404 | Not Found | Resource not found |
| 408 | Request Timeout | LLM generation timeout |
| 422 | Unprocessable Entity | Valid JSON but invalid business logic |
| 500 | Internal Server Error | Unexpected server error |
| 503 | Service Unavailable | LLM backend not available |

### Application Error Codes

| Code | Description | Suggestion |
|------|-------------|------------|
| `EMPTY_INPUT` | Input field is empty | Provide required input |
| `INVALID_PRODUCT` | Unknown product type | Check product name |
| `LLM_TIMEOUT` | LLM generation took too long | Retry or simplify prompt |
| `LLM_UNAVAILABLE` | LLM backend not responding | Check `/agent/models` |
| `GENERATION_FAILED` | LLM returned invalid output | Retry request |
| `SESSION_NOT_FOUND` | Session ID doesn't exist | Start new session |
| `SESSION_EXPIRED` | Session timed out | Start new session |

---

## Code Generation Strategies (v2.0)

Coco Engine은 두 가지 코드 생성 전략을 지원합니다:

| 전략 | 설명 | 파이프라인 | 권장 |
|------|------|-----------|------|
| **CGF-A** (Direct) | LLM이 직접 코드 생성 | 의도 파악 → LLM 코드 생성 → Post-processing | 단순 작업 |
| **CGF-B** (Spec-first) | LLM은 스펙만 생성, MCP 서버가 코드 생성 | 의도 파악 → LLM 스펙 생성 → MCP 코드 생성 → 검증 | ✅ **권장** |

> **CGF-B 성능**: CGF-A 대비 65% 속도 개선, 4개 테스트 중 3:1 품질 우위 (CGF 비교 보고서 참조)

### Coco Studio (Web UI)

Coco Studio는 `https://coco.secernai.net`에서 제공되는 웹 기반 UI로, 위 API를 시각적으로 사용할 수 있습니다.

| 기능 | 설명 | 사용 API |
|------|------|----------|
| **코드 생성** | 자연어 프롬프트로 코드 생성 | `/agent/agentic/v2/stream` |
| **코드 리뷰** | 코드 품질 분석 | `/agent/review` |
| **Q&A** | 프레임워크 지식 질의응답 | `/agent/qa` |
| **코드 프리뷰** | 생성된 코드 실행 미리보기 | 내부 프리뷰 서버 |

---

## Embedding Algorithm

The system uses **all-MiniLM-L6-v2** for semantic search (RAG):

| Property | Value |
|----------|-------|
| Model | Sentence-BERT (MiniLM variant) |
| Dimensions | 384 |
| Library | fastembed-rs |
| Similarity | Cosine similarity |

---

## 관련 문서

- [[implementation/roadmap_ko|로드맵]]: 구현 로드맵
- [[strategy/executive_summary_ko|경영진 요약]]: 프로젝트 개요
- [[implementation/cost_analysis_ko|비용 분석]]: 인프라 비용

---

---

## 변경이력

| 버전 | 일자 | 변경 내용 | 작성자 |
|------|------|----------|--------|
| 1.0 | 2026-01-08 | 초안 작성 | 분석팀 |
| 1.1 | 2026-01-21 | 엔드포인트 정리, 세션 관리 추가 | 분석팀 |
| 2.0 | 2026-02-12 | MCP 서버 엔드포인트 추가, CGF-A/CGF-B 전략 문서화, Coco Studio 설명 추가, product 필드 멀티 프레임워크 반영 | 분석팀 |
