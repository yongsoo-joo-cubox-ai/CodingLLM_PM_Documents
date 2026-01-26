## VRAM Sizing & Concurrency Planning

### The Core Equation

vLLM memory usage splits into two categories:

**A. Static Memory (Startup Cost)**

- **Model Weights**: The neural network files (AWQ compresses ~70% vs FP16)
    
- **KV Cache Overhead**: Metadata for paging
    
- **Activation Buffer**: Temporary GPU computation scratchpad
    

**B. Dynamic Memory (User Cost)**

- **KV Cache**: Scales linearly with concurrent users × max_model_len

### Example: 4x RTX 2080 Ti (44 GB Total)

**Target Model**: Qwen 2.5 32B AWQ

Step 1: Calculate Usable VRAM

| Item | Value |

|------|-------|

| Physical VRAM | 44 GB |

| Utilization Factor | 0.95 (dedicated server) |

| **Effective Budget** | **41.8 GB** |

Step 2: Subtract Static Costs

| Item | Size |

|------|------|

| Model Weights (INT4) | ~17.8 GB |

| System Overhead | ~1.5 GB |

| **Total Static** | **~19.3 GB** |

Step 3: Available for KV Cache

Available = 41.8 GB - 19.3 GB = ~22.5 GB

### Scenario Analysis

**KV Cache Cost**: ~0.25 MB per token (for 32B models)

| Scenario | max_model_len | Cost/User | Max Users | Best For |

|----------|---------------|-----------|-----------|----------|

| **A: Standard** | 8,192 | ~2.0 GB | **10** | Chatbots, simple Q&A |

| **B: Sweet Spot** | 12,288 | ~3.0 GB | **7** | Coding agents, RAG |

| **C: Deep Context** | 16,384 | ~4.0 GB | **5** | Complex debugging |

### Recommendation

For internal AI Coding Agents, **Scenario B (12,288 tokens)** is optimal:

| Feature | 8K Context | **12K Context** | 16K Context |

|---------|------------|-----------------|-------------|

| Max Users | 10 | **7** | 5 |

| Input Capacity | ~300 LOC | **~600 LOC** | ~1000 LOC |

| Use Case | Fast Chat | **Balanced Agent** | Deep Research |

| Risk | High truncation | **Low truncation** | Latency spikes |