# Quality Comparison Report: Multi-Model Benchmark

| 항목 | 내용 |
|------|------|
| **Date** | 2026-01-14 |
| **Task** | Task List Screen Generation |

---

## Summary

| Model | Size | XML | JS | Quality | Response Time |
|-------|------|-----|----|---------|--------------|
| gpt-oss | 20B | 5393 chars | 3996 chars | **94%** | ~15s |
| Qwen2.5-32B-AWQ | 32B | 1594 chars | 1279 chars | **54%** | 25s |
| Qwen2.5-7B | 7B | 936 chars | 864 chars | **42%** | 11s |
| Mistral-7B | 7B | 807 chars | 975 chars | **40%** | 8s |

### Visual Quality Comparison

```
Quality Score Distribution:

gpt-oss:20b    ████████████████████████████████████████████  94%
Qwen2.5-32B-AWQ ████████████████████░░░░░░░░░░░░░░░░░░░░░░░░  54%
Qwen2.5-7B     ███████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  42%
Mistral-7B     ██████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  40%
```

---

## Feature Matrix

### XML Structure Comparison

| Feature | gpt-oss:20b | Qwen32B | Qwen7B | Mistral7B |
|---------|-------------|---------|--------|-----------|
| Screen attributes | ✅ | ✅ | ❌ | ❌ |
| script_language="Java" | ✅ | ✅ | ❌ | ❌ |
| Datasets count | 3 | 1 | 1 | 1 |
| Search dataset | ✅ | ❌ | ❌ | ❌ |
| Status code dataset | ✅ | ❌ | ❌ | ❌ |
| Panels count | 4 | 2 | 1 | 1 |
| Grid columns | 4 | 2 | 3 | 3 |
| Korean labels | ✅ | ❌ | ✅ | ✅ |

### JavaScript Function Comparison

| Function | gpt-oss:20b | Qwen32B | Qwen7B | Mistral7B |
|----------|-------------|---------|--------|-----------|
| on_load | ✅ Full | ✅ Full | ✅ Basic | ✅ Basic |
| fn_init | ✅ Focus + combo | Stub | ❌ | ❌ |
| fn_search | ✅ Dataset ops | Stub | Stub | Stub |
| fn_add | ✅ Full popup | ✅ Basic | ✅ Basic | ✅ Basic |
| fn_delete | ✅ Multi-select | Single row | Stub | Stub |
| **Clean output** | ✅ | ✅ | ❌ Extra text | ❌ Extra text |

---

## Detailed Score Breakdown

### gpt-oss:20b (94/100)

| Category | Score | Notes |
|----------|-------|-------|
| XML Structure | 24/25 | Complete with 3 datasets, 4 panels |
| JS Functions | 23/25 | Full CRUD with multi-select delete |
| API Correctness | 24/25 | Proper xFrame5 API usage |

### Qwen2.5-32B-AWQ (54/100)

| Category | Score | Notes |
|----------|-------|-------|
| XML Structure | 12/25 | 1 dataset, 2 panels, missing search input |
| JS Functions | 15/25 | Basic CRUD, single-row delete |

---

## Sample Output Comparison

### XML: Button Definitions

**gpt-oss:20b:**
```xml
<pushbutton control_id="9" name="btn_create"
            x="20" y="10" width="80" height="30"
            text="Create"
            font="Malgun Gothic,9,1,0,0,0"
            back_color="0000FF00"
            text_color="00FFFFFF"
            on_click="eventfunc:fn_add()"/>
```

**Qwen2.5-32B:**
```xml
<pushbutton control_id="3" name="btn_new" x="570" y="24" width="100" height="30"
            text="New" on_click="eventfunc:fn_add()"/>
```

### JS: Delete Function

**gpt-oss:20b (55 lines, multi-select):**
```javascript
this.fn_delete = function() {
    var checkedRows = grid_task.getcheckedrowidx();
    if (!checkedRows || checkedRows.length === 0) {
        var selectedRow = grid_task.getfocusedrowidx();
        if (selectedRow < 0) {
            alert("Please select at least one item to delete.");
            return;
        }
        checkedRows = [selectedRow];
    }
    // ... logic continues
};
```

**Qwen2.5-32B (6 lines, single row):**
```javascript
this.fn_delete = function() {
    var row = this.grid_task.getSelectedRowIndex();
    if (row < 0) { alert("Please select a row."); return; }
    if (!confirm("Delete this item?")) return;
    // TODO: Implement delete
};
```

---

## Key Insights

```
Model Size:  7B ──────────────── 20B ────────────── 32B
             │                   │                  │
Quality:   40-42%               94%                54%
             │                   │                  │
             └── Size alone doesn't determine quality
```

### Template Sensitivity

| Model | Template Used | Output Quality |
|-------|---------------|----------------|
| gpt-oss:20b | v3 (430 lines) | **94%** |
| Qwen2.5-32B | v4 (80 lines) | **54%** |
| Qwen2.5-7B | v3 (430 lines) | **42%** |
| Mistral-7B | v3 (430 lines) | **40%** |

---

## Conclusion

| Rank | Model | Quality | Best For |
|------|-------|---------|----------|
| 1 | gpt-oss:20b | **94%** | Production use |
| 2 | Qwen2.5-32B-AWQ | **54%** | On-premise with improvements |
| 3 | Qwen2.5-7B | **42%** | Prototyping |
| 4 | Mistral-7B | **40%** | Fast iteration |
