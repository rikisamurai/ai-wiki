---
description: 基于 wiki/ 答问，找不到才降级查 sources/
argument-hint: <问题>
---

# /query

问题：`$ARGUMENTS`

## 你必须遵守的步骤

1. **优先在 wiki/ 找答案**
   - 用 Grep 在 `wiki/` 全域搜关键词
   - 命中后阅读相关页面，组合答案
   - 答案中引用的 wiki 页面用 wikilink 列出来

2. **找不到时降级查 sources/**
   - 同样的 Grep，但在 `sources/` 下
   - 答案要明确标注"以下来自未 ingest 的 source，wiki 里还没沉淀"

3. **追问 ingest 价值**
   - 答完后，问用户：「这个答案值得 ingest 回 wiki 吗？」
   - 如果 yes：生成 1-3 个新 wiki 页面草稿（按 /ingest 的页面规范），写入 `wiki/` 对应 domain
   - 如果 no：跳过

4. **append 到 log.md**

   ```
   ## [YYYY-MM-DD HH:MM] query | <问题摘要>
   - 来源：wiki | sources | both
   - 是否 ingest：yes/no
   ```

## 禁止

- 不基于"训练数据"答题（必须有 wiki/ 或 sources/ 的 grep 命中作为依据）
- 不修改 sources/
