---
title: Git AI
tags: [git, attribution, ai-coding]
date: 2026-05-08
sources:
  - "[[sources/posts/aigc/ai-coding/tools/Git AI - 追踪 AI 生成代码的 Git 扩展]]"
last-ingested: 2026-05-08
status: draft
---

开源 git 扩展，给每个 commit 自动附加一条 git note（`refs/notes/ai`），记录"哪几行代码由哪个 agent / 哪个 model / 哪条 prompt 生成"。把"AI 写了多少代码"从模糊感觉变成 commit 级别的可查事实。Local-first、Git-native、跨 12 个主流 coding agent 工作。

> [!note] 标志属性
> - **Local-first**：100% 离线、零账号、零登录，Git AI Cloud 是可选项
> - **Git-native**：复用 git notes 机制不发明新存储——见 [[wiki/agent-engineering/workflow/git-notes-ai-元数据|git notes 作为 AI 元数据载体]]
> - **History-rewrite-safe**：rebase / merge / cherry-pick 后 attribution 自动跟着重写，不丢
> - **不靠 ML 检测**：AI 代码由 agent 自报（`git ai checkpoint`），不让另一个模型猜——见 [[wiki/agent-engineering/workflow/ai-代码-attribution|Attribution 自报 vs 检测]]
> - **跨 agent**：12 家主流 coding agent 已支持，attribution 格式遵循公开 spec（`git_ai_standard_v3.0.0`）

## 三步流程

```
Step 1：Agent 边写边 checkpoint
        每个 supported agent 生成代码时调用 `git ai checkpoint`
        实现：git hooks / 1p 集成 / IDE 插件，对用户透明

Step 2：commit 时聚合
        本次 commit 涉及的所有 checkpoint 凝结成一份 Authorship Log
        作为 git note 挂到 commit（refs/notes/ai/<commitsha>）

Step 3：history rewrite 后自动跟随
        rebase / merge / cherry-pick 触发的 hash 变化
        Git AI 自动重写 Authorship Log，attribution 永远跟着代码走
```

## Authorship Log 长这样

> [!example] 一条 git note 的结构
> ```
> hooks/post_clone_hook.rs
>   promptid1 6-8         # 第 6-8 行由 promptid1 那次 prompt 生成
>   promptid2 16,21,25
> ---
> {
>   "prompts": {
>     "promptid1": {
>       "agent_id": { "tool": "copilot", "model": "Codex 5.2" },
>       "human_author": "Alice Person",
>       "summary": "Reported on GitHub #821: ..."
>     }
>   }
> }
> ```
>
> 每条 prompt 含：用了哪个 agent / model、对应 human author、prompt 的语义摘要。**行号映射回到具体代码行**，下游可以直接做 `git blame` 风格查询。

## AI Blame

Git AI 顺带扩展了 `git blame`：除了原生的"哪行是哪个人写的、哪个 commit 引入的"，再叠一层"哪个 AI agent / 哪条 prompt 生成的"。把 commit 级 attribution 下放到行级查询——这个工具最直观的 UX。

## 五个核心设计选择

| 选择 | 说明 |
|---|---|
| No workflow changes | 用户照常 prompt 和 commit，Git AI 在底层透明工作 |
| 不"检测"AI 代码 | 作者明确把 ML 风格检测列为 anti-pattern——见 [[wiki/agent-engineering/workflow/ai-代码-attribution\|Attribution 自报 vs 检测]] |
| Local-first | 100% 离线，Git AI Cloud 是可选 |
| Git-native + open standard | git notes 存储；spec 公开（`git_ai_standard_v3.0.0`），不锁厂商 |
| Sessions 不进 git | 完整对话历史本地或自托管 prompt store，repo 保持精简、避免 PII 落到 git 历史 |

## 支持矩阵

12 个 agent：Cursor / Claude Code / Codex / GitHub Copilot / Gemini CLI / OpenCode / Continue / Droid / Junie / Rovo Dev / Amp / Windsurf。支持等级（Fully / Agent-only / CLI-only / VS Code-only）取决于 agent 端是否方便挂 hook 或注入 attribution。

## 与 in-product 度量的关系

> [!compare] commit 级 attribution vs in-product 度量
> | 维度 | Git AI Attribution | [[wiki/agent-engineering/workflow/keep-rate\|Keep Rate]] / [[wiki/agent-engineering/workflow/采纳率\|采纳率]] |
> |---|---|---|
> | 时点 | commit / merge 后 | review 当下（采纳率）/ merge 后 N 时间窗（keep rate） |
> | 粒度 | 行级 + prompt 级（精确） | 块级 / PR 级（聚合） |
> | 主要用途 | 事后归因（"那行是谁写的、什么 prompt 写的"） | 实时质量度量（"AI 改动是不是被留下"） |
> | 数据来源 | agent 自报 | reviewer / 用户行为 |
>
> 不替代关系——in-product 度量回答"AI 写得好不好"，attribution 回答"哪一行 AI 写的、用什么 prompt 写的"。两者一起才能把"AI 在我们仓库里实际做了什么"完整还原。

## 安装

```bash
# Mac / Linux / Windows (WSL)
curl -sSL https://usegitai.com/install.sh | bash
```

无 per-repo setup，装一次全机生效。

## 关联

- 底层机制：[[wiki/agent-engineering/workflow/git-notes-ai-元数据|git notes 作为 AI 元数据载体]]
- 范式判断：[[wiki/agent-engineering/workflow/ai-代码-attribution|Attribution 自报 vs 检测]]
- 跨厂商共识同族：[[wiki/agent-engineering/philosophy/跨厂商共识协议|跨厂商共识协议]]、[[wiki/claude-code/mcp|MCP]]、[[wiki/skills/agent-skills|Agent Skills]]
- 度量互补：[[wiki/agent-engineering/workflow/keep-rate|Keep Rate]]、[[wiki/agent-engineering/workflow/采纳率|采纳率]]
