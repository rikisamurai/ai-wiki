---
title: git notes 作为 AI 元数据载体
tags: [git, infrastructure, ai-coding]
date: 2026-05-08
sources:
  - "[[sources/posts/aigc/ai-coding/tools/Git AI - 追踪 AI 生成代码的 Git 扩展]]"
last-ingested: 2026-05-08
status: stable
---

git notes 是 git 早就内建、长期被忽视的机制：给 commit 挂额外的、可独立同步的注释，**不改 commit hash**。AI Coding 时代被重新启用——存放 attribution、prompt 摘要这类"由 AI 工作产生但不属于代码本身"的元数据。[[wiki/claude-code/git-ai|Git AI]] 的核心选型就是用 `refs/notes/ai` 存 Authorship Log。

> [!note] git notes 的关键属性
> - **不改 commit hash**：notes 是单独的 ref，挂在 commit 上但不参与对象的 SHA 计算
> - **可独立 fetch / push**：`git fetch origin refs/notes/*:refs/notes/*` 才会拉，默认不拉——天然 opt-in
> - **支持 history rewrite 跟随**：rebase / cherry-pick 后用 `git notes copy <old> <new>` 自动跟着改写
> - **多命名空间**：`refs/notes/ai`、`refs/notes/review`、`refs/notes/ci-results` 等可并存

## 为什么 AI 元数据适合放 git notes

> [!compare] git notes vs 其他存储位置
> | 选项 | 不改代码 | 不改 commit hash | 自动跟随 history rewrite | 工具链零改动 |
> |---|---|---|---|---|
> | **commit message body** | ✓ | ✗（修改即换 hash） | rebase 时自动 | ✓ |
> | **代码中的注释** | ✗ | ✓ | ✓ | ✓ |
> | **外部数据库 / SaaS** | ✓ | ✓ | 需要自定义同步 | 引入新依赖 |
> | **git notes** | ✓ | ✓ | ✓（用 notes copy）| ✓ |
>
> AI attribution 天然适合 notes：行号→prompt 的映射在 rebase 后行号会变，必须能跟着重写；同时不能污染代码或改 commit hash。

## 同源思路：用 git 元数据做 AI 工程基础设施

> [!example] 已有的两条线
> - **commit message body 存 AI 状态**：[[wiki/agent-engineering/workflow/continuous-checkpoint|Continuous Checkpoint]] 用 `[gstack-context]` 段落存"已做的决策 / 剩余工作 / 失败过的方案"，会话崩溃后用 `/context-restore` 恢复
> - **git notes 存 AI attribution**：[[wiki/claude-code/git-ai|Git AI]] 的 Authorship Log
>
> 两者都是"用 git 既有元数据机制装 AI 工作的副产品"，避免发明新基础设施。后者更通用——commit body 一旦改 commit 就换 hash，notes 不会。

## 实操：使用 notes 的命令

```bash
# 给 commit 加 note
git notes --ref=ai add -m "..." <commit>

# 显示 commit 的 note
git notes --ref=ai show <commit>

# 同步 notes（默认不会跟 push 一起走）
git push origin refs/notes/ai
git fetch origin refs/notes/ai:refs/notes/ai

# rebase 后跟随（Git AI 自动做）
git notes --ref=ai copy <old-sha> <new-sha>
```

## 限制与注意

> [!warning] 不要把大对象塞进 notes
> notes 仍然在 git 里，每次 fetch 都会拉。Git AI 的做法：
> - **轻量元数据进 notes**：行号映射、agent / model、prompt 摘要
> - **完整对话历史不进 git**：放本地 prompt store 或 Git AI Cloud / 自托管 store
>
> 否则 repo 会膨胀、且 PII 一旦落到 git 历史就很难清干净。

## 关联

- 工具应用：[[wiki/claude-code/git-ai|Git AI]]
- 同源思路：[[wiki/agent-engineering/workflow/continuous-checkpoint|Continuous Checkpoint]]——commit body 装 AI 状态
- 范式上游：[[wiki/agent-engineering/workflow/ai-代码-attribution|Attribution 自报 vs 检测]]
