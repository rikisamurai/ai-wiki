---
title: Git AI - 追踪 AI 生成代码的 Git 扩展
source: https://usegitai.com/docs/cli
tags:
  - ai-coding
  - git
  - attribution
date: 2026-05-07
ingested-at: 2026-05-08
---

# Git AI

> [!abstract] 一句话定义
> Git AI 是一个开源 git 扩展，给每个 commit 自动附加一条 git note（`refs/notes/ai`），记录"哪几行代码由哪个 agent / 哪个 model / 哪条 prompt 生成"——把"AI 写了多少代码"从模糊感觉变成 commit 级别的可查事实。

标志属性：

- **Local-first**：100% 离线，无需登录
- **Git-native**：复用 git notes 这个早就存在的机制，不发明新存储
- **Survives history rewrites**：rebase / merge / cherry-pick 后 attribution 自动跟着重写，不丢
- **不靠 ML 检测**：AI 代码由 agent 自报（`git ai checkpoint`），不让另一个模型猜
- **跨 agent**：12 家主流 coding agent 已支持，用任意组合都能拿到统一的 attribution

## 解决什么问题

随着 Cursor、Claude Code、Codex、Copilot 等 AI coding 工具普及，团队越来越说不清这件事：

> 这次发版的 1 万行新代码里，有多少是 AI 写的？是哪个 agent 写的？是基于什么 prompt 写的？

之前的解法都不太行：

- **拍脑袋估算**：不可靠
- **基于 ML 检测代码风格**：作者把它点名为 anti-pattern——AI 代码风格越来越像人，靠"嗅探"区分注定不准
- **手工记录**：增加工作量，没人愿意

Git AI 的思路：让 agent 在写代码时**自报家门**——本来 agent 就知道自己生成了哪几行，把这个信息按格式落到 git notes 即可。

跟 in-product 度量（如 Cursor 的 Keep Rate / 得物的采纳率）互补：那些是统计层面的"AI 改动留存比例"，Git AI 给的是 commit 级别的事后 attribution——可以精确到"这条规则错的那一行是 Cursor + Claude Sonnet 4.5 在 X 月 Y 号写的"。

## 怎么工作（三步）

```
Step 1：Agent 边写边 checkpoint
        ─────────────────────────
        每个 supported agent 在生成代码时调用 `git ai checkpoint`，
        实现方式：git hooks / 1p 集成 / IDE 插件，对用户透明。

Step 2：commit 时聚合
        ──────────────
        本次 commit 涉及的所有 checkpoint 凝结成一份 Authorship Log，
        作为 git note 挂到 commit 上（refs/notes/ai/<commitsha>）。

Step 3：history rewrite 后自动跟随
        ───────────────────────────
        rebase / merge / cherry-pick 触发的 commit hash 变化，
        Git AI 自动重写 Authorship Log，attribution 永远跟着代码走。
```

一条 git note 大致长这样（示例化简）：

```
hooks/post_clone_hook.rs
  promptid1 6-8         # 第 6-8 行由 promptid1 那次 prompt 生成
  promptid2 16,21,25    # 第 16/21/25 行由 promptid2 那次 prompt 生成
---
{
  "prompts": {
    "promptid1": {
      "agent_id": { "tool": "copilot", "model": "Codex 5.2" },
      "human_author": "Alice Person",
      "summary": "Reported on GitHub #821: Git AI tries fetching authorship notes for interrupted (CTRL-C) clones. Fix: guard note fetching on successful clone."
    },
    "promptid2": {
      "agent_id": { "tool": "cursor", "model": "Sonnet 4.5" },
      "human_author": "Jeff Coder",
      "summary": "Match the style of Git Clone's output to report success or failure of the notes fetch operation."
    }
  }
}
```

每条 prompt 含：用了哪个 agent / model、对应的 human author、这次 prompt 的语义摘要。**行号映射回到具体代码行**，所以下游可以直接基于这份记录做 `git blame` 风格的查询。

## 五个核心设计选择

| 选择 | 说明 |
|---|---|
| **No workflow changes** | 用户照常 prompt 和 commit，Git AI 在底层透明工作；不要求改任何团队流程 |
| **不"检测"AI 代码** | 作者明确把基于风格的 ML 检测列为 anti-pattern——agent 自报才能精准 |
| **Local-first** | 100% 离线、零账号、零登录；Git AI Cloud 是可选的，自己愿意才用 |
| **Git-native + open standard** | 用 git notes 做存储；attribution 格式遵循公开 spec（`git_ai_standard_v3.0.0`），不锁厂商 |
| **Agent sessions 不进 git** | git notes 里只放轻量元数据；完整对话历史本地存或上 Git AI Cloud / 自托管 prompt store——保持 repo 精简，避免 PII 落到 git 历史 |

## 支持的 12 个 Agent

| Agent | 支持等级 |
|---|---|
| Cursor | ✓ Agent  ✗ CLI |
| Claude Code | ✓ Fully Supported |
| Codex | ✓ Fully Supported |
| GitHub Copilot | ✓ VS Code  ✓ JetBrains |
| Gemini CLI | ✓ CLI |
| OpenCode | ✓ Fully Supported |
| Continue | ✓ CLI  ✗ IDE |
| Droid | ✓ Fully Supported |
| Junie | ✓ Fully Supported |
| Rovo Dev | ✓ Fully Supported |
| Amp | ✓ Fully Supported |
| Windsurf | ✓ All except Model |

> 支持等级里"Fully" / "Agent only" / "CLI only" / "VS Code only" 的差异，主要看 agent 端是否方便挂 hook 或注入 attribution——如 Cursor 的 Agent 模式可以挂、Cursor 的纯 CLI 模式还不行。

## AI Blame

Git AI 顺带扩展了 `git blame`：除了原生的"哪行是哪个人写的、哪个 commit 引入的"，再叠一层"哪个 AI agent / 哪条 prompt 生成的"。把 commit 级 attribution 下放到行级查询，是这个工具最直观的 UX。

## 安装与一些指针

**Mac / Linux / Windows (WSL)**

```bash
curl -sSL https://usegitai.com/install.sh | bash
```

**Windows (非 WSL)**

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -Command "irm http://usegitai.com/install.ps1 | iex"
```

无 per-repo setup，装一次全机生效；如果已有 agent / IDE 在跑，重启一次让 hook 被识别。

**延伸阅读**：

- 官方 spec：[git-ai-project/git-ai · `specs/git_ai_standard_v3.0.0.md`](https://github.com/git-ai-project/git-ai/blob/main/specs/git_ai_standard_v3.0.0.md)
- 技术 deep-dive：<https://usegitai.com/docs/cli/how-git-ai-works>
- AI Blame 详解：<https://usegitai.com/docs/cli/ai-blame>
- 视频 demo：YouTube ID `b_DZTC1PKHI`
- 添加新 agent 支持：<https://usegitai.com/docs/guides/add-your-agent>

## 我的几个观察（待 ingest）

- **"自报 vs 检测"是个值得沉淀的范式判断**——同样思路在 Anthropic 的《Demystifying evals for AI agents》里也出现过：评估 agent 行为时也是"agent 自报 transcript"比"事后用模型逆推"更可靠
- **Git notes 这个被忽视已久的机制重新被启用**——可以引出"用 git 元数据做 AI 工程基础设施"这条线，跟 continuous-checkpoint 那种 WIP commit + 结构化 body 是同源思路
- **跨 12 个 agent 的标准化**——这件事意味着 Git AI 可能成为 multi-agent 团队的事实层 attribution 协议，跟 MCP 之于工具调用、Skills 规范之于 agent 能力分发是同一类"跨厂商共识"
