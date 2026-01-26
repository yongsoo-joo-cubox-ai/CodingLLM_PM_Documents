# Load Test Report: Qwen2.5-Coder-32B-AWQ

| 항목 | 내용 |
|------|------|
| **Date** | 2026-01-14 |
| **Provider** | vLLM (시선AI Server: 172.16.100.116) |
| **Model** | Qwen/Qwen2.5-Coder-32B-Instruct-AWQ |
| **Hardware** | 4x NVIDIA RTX 2080 Ti (11GB), TP=4 |

---

## Summary

| Users | Success | Throughput | p50 Latency | p95 Latency | Avg XML | Avg JS |
|-------|---------|------------|-------------|-------------|---------|--------|
| 1 | 100% | 0.04 rps | 25.1s | 25.1s | 1594 | 1279 |
| 2 | 100% | 0.07 rps | 27.9s | 28.0s | 1608 | 1290 |
| 5 | 100% | 0.12 rps | 43.5s | 43.6s | 1622 | 1301 |
| 10 | 100% | 0.15 rps | 62.9s | 64.2s | 1655 | 1305 |

---

## Key Findings

### 1. vLLM Continuous Batching Works Efficiently

- **Sequential (no batching):** 10 requests × 25s = 250s
- **Concurrent (with batching):** 10 requests in 65s
- **Speedup: 3.8x faster with batching!**

### 2. Throughput Scales Sub-Linearly

```
1 user  → 0.04 rps (baseline)
2 users → 0.07 rps (1.75x)
5 users → 0.12 rps (3.0x)
10 users → 0.15 rps (3.75x)
```

The system doesn't achieve perfect linear scaling due to GPU memory bandwidth limits, KV cache sharing overhead, and Tensor parallel communication.

### 3. Latency Increases with Concurrency

```
Response Time vs Concurrency

70s │         ████████
60s │
50s │
40s │     ████████
30s │ ████████
25s │████████
    └─────────────────────
      1    2    5   10  users
```

### 4. Output Quality Remains Consistent

- **No quality degradation under load**
- XML size: 1594-1881 chars (±10%)
- JS size: 1279-1323 chars (±3%)
- All outputs contain valid xFrame5 code

---

## Recommendations

### For Production Deployment

1. **Expected Capacity:**
   - ~0.15 rps sustained with 10 concurrent users
   - ~500 generations/hour at full load

2. **Queue Management:** Implement request queuing for >10 concurrent users and set timeout at 120s.

3. **Scaling Options:** Add more GPUs or use multiple vLLM instances with load balancing.

### User Experience

| Concurrency | Expected Wait Time | Acceptable For |
|-------------|-------------------|----------------|
| 1-2 users | 25-28s | Interactive use |
| 5 users | 45s | Batch processing |
| 10 users | 65s | Background jobs |

---

## Test Methodology

### Realistic Workload Simulation

Each concurrent user sent a **different prompt** to prevent artificial caching benefits:

```python
TEST_PROMPTS = [
    "Generate a page to show list of tasks...",      # user 0
    "Create a member management screen...",          # user 1
    "Build a product inventory list screen...",      # user 2
    // ... 7 more unique prompts
]
```

**Why this matters:**

| Scenario | KV Cache Sharing | Expected Throughput |
|----------|------------------|---------------------|
| Same prompt (batch) | Shared prefill | Higher (best case) |
| Different prompts (realistic) | Separate KV caches | Lower (what we tested) |

The **3.8x batching speedup** was achieved even with this realistic workload.

### Test Configuration

```
Backend: Rust + Loco.rs
LLM Server: vLLM v0.6.1.post2
Model: Qwen2.5-Coder-32B-Instruct-AWQ
Quantization: AWQ (4-bit)
Tensor Parallel: 4 GPUs
Max Model Length: 8192
GPU Memory: 85% utilization
Template: xframe5-list v4 (80 lines + dynamic RAG)
```
