---
description: 从 migration-backlog.md 取下一条 source 做 ingest
---

# /migrate-next

存量迁移驱动器。一次只处理 backlog 里的 1 条 source。

## 你必须遵守的步骤

1. **读 backlog**：Read `migration-backlog.md`。**如果文件不存在**，说明当前无活跃迁移批次（2026-04 首批已归档至 `wiki/_orphans/migration-2026-04.md`）——告知用户后退出，或在确认后协助创建新 backlog（按 `sources/` 当前内容枚举待 ingest 项）。
2. **取下一条**：找到第一个 `- [ ]` 开头的 source 路径。如果全部勾完了，输出 "Migration complete 🎉" 并退出。
3. **遵循 §3.1 ingest 流程**：把那条 source 当作 `/ingest` 的输入，跑完 6 步流程（见 `.claude/commands/ingest.md`）。
4. **勾掉 backlog**：把这一条的 `- [ ]` 改成 `- [x]`，并在末尾追加 `← YYYY-MM-DD`。
5. **更新进度**：把 backlog 文件顶部的 `进度：X/Y` 数字加 1。
6. **append 到 log.md**：op 字段写 `migrate-next`（不是 `ingest`，便于事后区分主动 ingest 与存量迁移）：

   ```
   ## [YYYY-MM-DD HH:MM] migrate-next | <X>/<Y> · <source 标题>
   - 新建：[[wiki/...]]、[[wiki/...]]
   - source: <path>
   ```

## 失败处理

- 如果 source 太长导致 ingest 失败 → 把 backlog 那条的 `- [ ]` 改成 `- [SKIP]` 并在末尾加 ← YYYY-MM-DD: <原因>，**不阻塞流水线**，输出说明后退出。

## 禁止

- 一次只处理 1 条，不连续跑（context 爆炸）
- 不跳过 backlog 顺序（按从上到下 FIFO）
