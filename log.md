---
title: ai-wiki Activity Log
---

# Log

> append-only 时间线，记录所有 ingest / query / lint / migrate-next 操作。
> 格式：`## [YYYY-MM-DD HH:MM] <op> | <subject>`，便于 `grep '## \[2026-'`。

## [2026-04-22 16:30] init | ai-wiki 重构落地
- 建立 sources/ wiki/ .claude/commands/ 骨架
- 写入 4 个 slash commands
- 改写 AGENTS.md 为 LLM Wiki schema
- 创建 index.md / log.md / migration-backlog.md / *.base
